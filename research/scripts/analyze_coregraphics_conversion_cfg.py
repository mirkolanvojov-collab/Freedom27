#!/usr/bin/env python3
"""Conservative CFG/dominator audit for CoreGraphics conversion instructions.

Consumes the comparison JSON; never executes or modifies a binary. Dominance is
structural only and does not establish register/data-flow semantics or exploitability.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SYMBOLS = (
    "_aa_moveto", "_aa_lineto", "_aa_clip_edge", "_aa_clipping",
    "_aa_cubeto", "_aa_quadto", "_aa_rectat",
)
BRANCH_TARGET = re.compile(r"(?:loc_)?(0x[0-9a-fA-F]+|[0-9a-fA-F]+)$")
CONDITIONAL = re.compile(r"^(?:b\.(?!al\b)[a-z]+|cbz|cbnz|tbz|tbnz)\b")
SELF_COMPARE = re.compile(r"^fcmp\s+([sd]\d+),\s*\1$")
CLAMP_LOAD = re.compile(r"\[(?:x\d+|sp),\s*#0x(?:6f8|700)\]")


def _target_address(text: str) -> int | None:
    match = BRANCH_TARGET.search(text.strip())
    if not match:
        return None
    raw = match.group(1)
    try:
        return int(raw, 16)
    except ValueError:
        return None


def build_cfg(records: list[dict[str, str]]) -> tuple[list[set[int]], list[dict[str, str]]]:
    addresses = [int(record["address"], 16) for record in records]
    index = {address: i for i, address in enumerate(addresses)}
    successors: list[set[int]] = [set() for _ in records]
    unresolved: list[dict[str, str]] = []

    for i, record in enumerate(records):
        text = record["instruction"].strip()
        mnemonic = text.split(maxsplit=1)[0] if text else ""
        next_index = i + 1 if i + 1 < len(records) else None

        if mnemonic in {"ret", "retab", "eret"} or mnemonic.startswith(("br ", "braa", "brab")):
            if mnemonic.startswith(("br ", "braa", "brab")):
                unresolved.append({"address": record["address"], "instruction": text,
                                   "reason": "indirect control transfer"})
            continue

        unconditional = mnemonic == "b"
        conditional = bool(CONDITIONAL.match(text))
        if unconditional or conditional:
            target = _target_address(text)
            if target is None:
                unresolved.append({"address": record["address"], "instruction": text,
                                   "reason": "could not parse direct branch target"})
            elif target in index:
                successors[i].add(index[target])
            else:
                unresolved.append({"address": record["address"], "instruction": text,
                                   "reason": "branch target is outside this function listing"})
            if conditional and next_index is not None:
                successors[i].add(next_index)
        elif next_index is not None:
            successors[i].add(next_index)

    return successors, unresolved


def compute_dominators(successors: list[set[int]]) -> tuple[list[set[int]], set[int]]:
    count = len(successors)
    predecessors: list[set[int]] = [set() for _ in successors]
    for source, targets in enumerate(successors):
        for target in targets:
            predecessors[target].add(source)

    reachable: set[int] = set()
    pending = [0] if count else []
    while pending:
        node = pending.pop()
        if node in reachable:
            continue
        reachable.add(node)
        pending.extend(successors[node] - reachable)

    dominators = [set(reachable) if i in reachable else set() for i in range(count)]
    if count:
        dominators[0] = {0}
    changed = True
    while changed:
        changed = False
        for node in range(1, count):
            if node not in reachable:
                continue
            incoming = [p for p in predecessors[node] if p in reachable]
            common = set.intersection(*(dominators[p] for p in incoming)) if incoming else set()
            updated = {node} | common
            if updated != dominators[node]:
                dominators[node] = updated
                changed = True
    return dominators, reachable


def analyze_function(symbol: str, side: str, records: list[dict[str, str]]) -> dict[str, Any]:
    successors, unresolved = build_cfg(records)
    dominators, reachable = compute_dominators(successors)
    conversions = []
    for i, record in enumerate(records):
        text = record["instruction"].strip()
        if "fcvtzs" not in text:
            continue
        dom_records = [records[j] for j in sorted(dominators[i])]
        self_compares = [r for r in dom_records if SELF_COMPARE.match(r["instruction"].strip())]
        nan_branches = [r for r in dom_records if re.match(r"^b\.vs\b", r["instruction"].strip())]
        clamp_loads = [r for r in dom_records if CLAMP_LOAD.search(r["instruction"])]
        float_compares = [r for r in dom_records if re.match(r"^fcmp\b", r["instruction"].strip())]
        conversions.append({
            "address": record["address"],
            "instruction": text,
            "reachable_in_cfg": i in reachable,
            "dominating_self_compares": [{"address": r["address"], "instruction": r["instruction"]} for r in self_compares],
            "dominating_nan_branches": [{"address": r["address"], "instruction": r["instruction"]} for r in nan_branches],
            "dominating_clamp_loads": [{"address": r["address"], "instruction": r["instruction"]} for r in clamp_loads],
            "dominating_float_compares": [{"address": r["address"], "instruction": r["instruction"]} for r in float_compares],
            "structural_nan_guard_in_dominators": bool(self_compares and nan_branches),
            "structural_clamp_reference_in_dominators": bool(clamp_loads and float_compares),
        })
    return {
        "symbol": symbol,
        "side": side,
        "instruction_count": len(records),
        "reachable_instruction_count": len(reachable),
        "conversion_count": len(conversions),
        "unresolved_control_transfers": unresolved,
        "conversions": conversions,
    }


def analyze_document(document: dict[str, Any]) -> dict[str, Any]:
    symbols = document.get("symbols")
    if not isinstance(symbols, list):
        raise ValueError("function-diff JSON must contain a symbols list")
    reports = []
    for symbol in SYMBOLS:
        item = next((entry for entry in symbols if entry.get("symbol") == symbol), None)
        if item is None:
            reports.append({"symbol": symbol, "status": "missing_from_comparison"})
            continue
        for side in ("target", "fixed"):
            records = item.get(f"{side}_addressed_instructions")
            if not isinstance(records, list):
                reports.append({"symbol": symbol, "side": side, "status": "addressed_records_missing"})
                continue
            reports.append({"status": "analyzed", **analyze_function(symbol, side, records)})
    return {
        "schema_version": 1,
        "mode": "static_control_flow_dominator_audit",
        "source_schema_version": document.get("schema_version"),
        "functions": reports,
        "limitations": [
            "Branch structure is reconstructed from disassembler text and direct branch labels.",
            "Dominance is structural; it does not prove the compared value is the converted value.",
            "A dominating conditional branch does not alone prove the unsafe branch is excluded.",
            "No full register/flag data-flow, alias analysis, or symbolic execution is performed.",
            "No binary was executed and no device was accessed or modified.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--function-diff", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.function_diff.read_text(encoding="utf-8"))
        report = analyze_document(document)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
