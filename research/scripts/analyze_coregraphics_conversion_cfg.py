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

        if mnemonic in {"ret", "retaa", "retab", "eret"} or mnemonic == "br" or mnemonic.startswith(("braa", "brab")):
            if mnemonic == "br" or mnemonic.startswith(("braa", "brab")):
                unresolved.append({"address": record["address"], "instruction": text,
                                   "reason": "indirect control transfer"})
            continue

        unconditional = mnemonic in {"b", "b.al"}
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


def _reachable_from(start: int, successors: list[set[int]], blocked: set[int] | None = None) -> set[int]:
    blocked = blocked or set()
    seen: set[int] = set()
    pending = [] if start in blocked else [start]
    while pending:
        node = pending.pop()
        if node in seen or node in blocked:
            continue
        seen.add(node)
        pending.extend(successors[node] - seen - blocked)
    return seen


def _path_nan_guard_nodes(records: list[dict[str, str]], successors: list[set[int]],
                          conversion_index: int) -> list[int]:
    """Find structural NaN-guard branches relevant to a conversion.

    Recognizes both b.vs (unordered/NaN takes the branch) and b.vc
    (ordered takes the branch, so NaN falls through). The NaN successor must
    have no CFG path to the conversion. This does not track NZCV or data flow.
    """
    index = {int(record["address"], 16): i for i, record in enumerate(records)}
    guards: list[int] = []
    for i, record in enumerate(records):
        text = record["instruction"].strip()
        if i == 0:
            continue
        if not SELF_COMPARE.match(records[i - 1]["instruction"].strip()):
            continue
        if re.match(r"^b\.vs\b", text):
            target = _target_address(text)
            nan_successor = index.get(target) if target is not None else None
        elif re.match(r"^b\.vc\b", text):
            # b.vc is taken for ordered values; unordered/NaN falls through.
            nan_successor = i + 1 if i + 1 < len(records) else None
        else:
            continue
        if nan_successor is None:
            continue
        if conversion_index not in _reachable_from(nan_successor, successors):
            guards.append(i)
    return guards


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

        path_guard_nodes = _path_nan_guard_nodes(records, successors, i)
        bypass_reachable = i in _reachable_from(0, successors, blocked=set(path_guard_nodes))
        path_guard_coverage = (not bypass_reachable) if i in reachable else False
        next_record = records[i + 1] if i + 1 < len(records) else None
        next_text = next_record["instruction"].strip() if next_record else ""
        vector_narrow = re.match(r"^xtn\s+v(\d+)\.2s,\s*v(\d+)\.2d$", next_text)
        source_vector = re.match(r"^fcvtzs\s+v(\d+)\.2d,\s*v(\d+)\.2d$", text)
        narrows_64_to_32 = bool(
            vector_narrow and source_vector
            and vector_narrow.group(1) == source_vector.group(1)
            and vector_narrow.group(2) == source_vector.group(2)
        )
        conversions.append({
            "address": record["address"],
            "instruction": text,
            "followed_by_same_register_xtn_2d_to_2s": narrows_64_to_32,
            "narrowing_instruction": next_text if narrows_64_to_32 else None,
            "narrowing_address": next_record["address"] if narrows_64_to_32 else None,
            "narrowing_semantics_note": (
                "XTN keeps the low 32 bits of each 64-bit lane; it does not clamp to signed 32-bit range."
                if narrows_64_to_32 else None
            ),
            "reachable_in_cfg": i in reachable,
            "dominating_self_compares": [{"address": r["address"], "instruction": r["instruction"]} for r in self_compares],
            "dominating_nan_branches": [{"address": r["address"], "instruction": r["instruction"]} for r in nan_branches],
            "dominating_clamp_loads": [{"address": r["address"], "instruction": r["instruction"]} for r in clamp_loads],
            "dominating_float_compares": [{"address": r["address"], "instruction": r["instruction"]} for r in float_compares],
            "structural_nan_guard_in_dominators": bool(self_compares and nan_branches),
            "cfg_nan_guard_cutset_coverage": path_guard_coverage,
            "cfg_nan_guard_branches": [
                {"address": records[j]["address"], "instruction": records[j]["instruction"]}
                for j in path_guard_nodes
            ],
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
        "mode": "static_cfg_nan_guard_coverage_audit",
        "source_schema_version": document.get("schema_version"),
        "functions": reports,
        "limitations": [
            "Branch structure is reconstructed from disassembler text and direct branch labels.",
            "Dominance is structural; it does not prove the compared value is the converted value.",
            "CFG guard-cutset coverage removes candidate self-compare/b.vs or self-compare/b.vc branch nodes and checks reachability; it does not prove flag/register dataflow or sentinel correctness. Loop-back edges may revisit the same conversion with a later value, so false coverage is not proof of a missing guard and true coverage is not proof of safety.",
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
