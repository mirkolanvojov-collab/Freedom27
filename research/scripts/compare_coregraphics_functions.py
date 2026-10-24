#!/usr/bin/env python3
"""Read-only, symbol-scoped CoreGraphics disassembly comparison.

Discovers aa_* symbols in two extracted Mach-O binaries, disassembles only
those functions, and compares normalized instruction streams. It does not
execute either binary or generate a vulnerability trigger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SYMBOL_RE = re.compile(r"(?<![A-Za-z0-9_$])_?aa_[A-Za-z0-9_$]+")
LINE_RE = re.compile(r"^\s*0x[0-9a-fA-F]+:\s*(.*)$")
HEX_BYTES_RE = re.compile(r"^(?:(?:[0-9a-fA-F]{2})\s+){4}(.*)$")
BRANCH_RE = re.compile(r"^(?:b(?:\.[a-z]+)?|bl|cbz|cbnz|tbz|tbnz)\s+(.+)$", re.I)


def run(args: list[str]) -> str:
    executable = shutil.which(args[0])
    if not executable:
        raise RuntimeError(f"required tool not found: {args[0]}")
    result = subprocess.run([executable, *args[1:]], text=True, capture_output=True, check=False)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()[-1500:]
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(args)}: {detail}")
    return result.stdout + result.stderr


def discover_symbols(binary: Path) -> list[str]:
    output = run(["ipsw", "macho", "info", "--symbols", str(binary)])
    # Preserve the exact spelling printed by ipsw for use with --symbol.
    found = {match.group(0) for line in output.splitlines() for match in SYMBOL_RE.finditer(line)}
    return sorted(found)


def normalize_disassembly(output: str) -> list[str]:
    instructions: list[str] = []
    for line in output.splitlines():
        match = LINE_RE.match(line)
        if not match:
            continue
        text = match.group(1).strip()
        byte_match = HEX_BYTES_RE.match(text)
        if byte_match:
            text = byte_match.group(1).strip()
        if not text:
            continue
        text = re.sub(r"\s+", " ", text)
        branch = BRANCH_RE.match(text)
        if branch:
            operands = re.sub(r"#?0x[0-9a-fA-F]+", "<branch-target>", branch.group(1))
            text = text.split()[0] + " " + operands
        instructions.append(text)
    return instructions


def disassemble(binary: Path, symbol: str, instruction_limit: int) -> list[str]:
    output = run([
        "ipsw", "macho", "disass", "--symbol", symbol,
        "--count", str(instruction_limit), str(binary),
    ])
    instructions = normalize_disassembly(output)
    if not instructions:
        raise RuntimeError(
            f"disassembler returned no parseable instructions for {symbol} in {binary}"
        )
    return instructions


def digest_instructions(instructions: list[str]) -> str:
    payload = "\n".join(instructions).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def compare(target_binary: Path, fixed_binary: Path, instruction_limit: int = 600) -> dict[str, Any]:
    if not target_binary.is_file() or not fixed_binary.is_file():
        raise FileNotFoundError("both CoreGraphics Mach-O paths must exist")
    target_symbols = discover_symbols(target_binary)
    fixed_symbols = discover_symbols(fixed_binary)
    common = sorted(set(target_symbols) & set(fixed_symbols))
    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for symbol in common:
        try:
            target_ins = disassemble(target_binary, symbol, instruction_limit)
            fixed_ins = disassemble(fixed_binary, symbol, instruction_limit)
        except RuntimeError as exc:
            failures.append({"symbol": symbol, "error": str(exc)})
            continue
        same = target_ins == fixed_ins
        item: dict[str, Any] = {
            "symbol": symbol,
            "target_instruction_count": len(target_ins),
            "fixed_instruction_count": len(fixed_ins),
            "target_instruction_sha256": digest_instructions(target_ins),
            "fixed_instruction_sha256": digest_instructions(fixed_ins),
            "instruction_stream_identical": same,
        }
        if not same:
            item["target_instructions"] = target_ins
            item["fixed_instructions"] = fixed_ins
        results.append(item)

    changed = [item for item in results if not item["instruction_stream_identical"]]
    return {
        "schema_version": 1,
        "mode": "read_only_symbol_scoped_disassembly_comparison",
        "target_binary": str(target_binary),
        "fixed_reference_binary": str(fixed_binary),
        "instruction_limit_per_symbol": instruction_limit,
        "target_aa_symbol_count": len(target_symbols),
        "fixed_aa_symbol_count": len(fixed_symbols),
        "common_aa_symbol_count": len(common),
        "successfully_compared_symbol_count": len(results),
        "changed_symbol_count": len(changed),
        "changed_symbols": [item["symbol"] for item in changed],
        "symbols": results,
        "disassembly_failures": failures,
        "interpretation": (
            "One or more shared aa_* symbol instruction streams differ; inspect the recorded disassembly before attributing changes to CVE-2026-86950."
            if changed else
            "No differences were established among successfully compared shared aa_* symbol instruction streams. Missing symbols, truncated streams, or failed disassemblies may limit coverage."
        ),
        "limitations": [
            "Only symbols discoverable through ipsw's Mach-O symbol listing are compared.",
            "Each disassembly is capped at the configured instruction limit.",
            "Compiler/build changes may alter instructions for reasons unrelated to the CVE.",
            "This static comparison does not establish runtime reachability or exploitability.",
            "No binary was executed; no crafted input or device was used.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-binary", type=Path, required=True)
    parser.add_argument("--fixed-binary", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("coregraphics-function-diff.json"))
    parser.add_argument("--instruction-limit", type=int, default=600)
    args = parser.parse_args()
    if args.instruction_limit < 1 or args.instruction_limit > 5000:
        parser.error("--instruction-limit must be between 1 and 5000")
    try:
        report = compare(args.target_binary, args.fixed_binary, args.instruction_limit)
    except (OSError, RuntimeError) as exc:
        print(f"function comparison failed: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "symbols"}, indent=2))
    if report["common_aa_symbol_count"] and report["successfully_compared_symbol_count"] == 0:
        print("no shared aa_* symbols were successfully disassembled; refusing a false-success result", file=sys.stderr)
        return 3
    if report["disassembly_failures"]:
        print(f"warning: {len(report['disassembly_failures'])} symbol disassembly attempt(s) failed", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
