#!/usr/bin/env python3
"""Verify fixed CoreGraphics coordinate-clamp constants from a Mach-O binary.

Read-only static analysis: map __TEXT,__const virtual addresses to file offsets,
read constants referenced by fixed-build disassembly, and check their IEEE-754
values against public patch analysis. The binary is never executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any

EXPECTED_BY_OPERAND = {0x6F8: -1073737729.0, 0x700: 1073737729.0}
SECTION_FIELDS = ("sectname", "segname", "addr", "size", "offset")


def parse_sections(load_commands: str) -> list[dict[str, Any]]:
    """Parse section records from otool -l output, including file offsets."""
    sections: list[dict[str, Any]] = []
    for block in re.split(r"(?m)^\s*Section\s*$", load_commands)[1:]:
        fields: dict[str, str] = {}
        for key in SECTION_FIELDS:
            match = re.search(rf"(?m)^\s*{key}\s+(\S+)", block)
            if match:
                fields[key] = match.group(1)
        if all(key in fields for key in SECTION_FIELDS):
            sections.append({
                "section": fields["sectname"],
                "segment": fields["segname"],
                "address": int(fields["addr"], 0),
                "size": int(fields["size"], 0),
                "file_offset": int(fields["offset"], 0),
            })
    return sections


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_references(function_diff: dict[str, Any]) -> list[dict[str, Any]]:
    """Find actual disassembly references to the two documented clamp constants."""
    references: list[dict[str, Any]] = []
    for site in function_diff.get("symbols", []):
        for item in site.get("fixed_relocation_sensitive_sites", []):
            for ref in item.get("derived_references", []):
                instruction = ref.get("access_instruction", "")
                match = re.search(r"\[x\d+,\s*#?(0x[0-9a-fA-F]+|[0-9]+)\]", instruction)
                if not match or not instruction.lower().startswith("ldr d"):
                    continue
                operand_offset = int(match.group(1), 0)
                if operand_offset not in EXPECTED_BY_OPERAND:
                    continue
                resolution = ref.get("section_resolution", {})
                if (resolution.get("classification") != "inside_section"
                        or resolution.get("segment") != "__TEXT"
                        or resolution.get("section") != "__const"):
                    raise ValueError(f"constant reference is not resolved to __TEXT,__const: {ref}")
                references.append({
                    "symbol": site.get("symbol"),
                    "instruction": instruction,
                    "operand_offset": operand_offset,
                    "effective_address": int(ref["effective_address"], 0),
                    "section_offset": int(resolution["section_offset"], 0),
                })
    if not references:
        raise ValueError("no fixed-build ldr-double references to offsets 0x6f8/0x700 were found")
    return references


def verify(binary: Path, load_commands_path: Path, diff_path: Path) -> dict[str, Any]:
    sections = parse_sections(load_commands_path.read_text(encoding="utf-8"))
    const_sections = [s for s in sections if s["segment"] == "__TEXT" and s["section"] == "__const"]
    if len(const_sections) != 1:
        raise ValueError(f"expected exactly one __TEXT,__const section; found {len(const_sections)}")
    section = const_sections[0]
    blob = binary.read_bytes()
    diff = json.loads(diff_path.read_text(encoding="utf-8"))
    references = extract_references(diff)
    unique: dict[tuple[int, int], dict[str, Any]] = {}
    for ref in references:
        section_offset = ref["section_offset"]
        if section_offset < 0 or section_offset + 8 > section["size"]:
            raise ValueError(f"constant offset falls outside __TEXT,__const: {ref}")
        if ref["effective_address"] != section["address"] + section_offset:
            raise ValueError(f"effective address does not match section-relative address: {ref}")
        unique.setdefault((ref["operand_offset"], section_offset), ref)

    results: list[dict[str, Any]] = []
    for (operand_offset, section_offset), ref in sorted(unique.items()):
        file_offset = section["file_offset"] + section_offset
        if file_offset < 0 or file_offset + 8 > len(blob):
            raise ValueError(f"constant file offset falls outside binary: {file_offset:#x}")
        raw = blob[file_offset:file_offset + 8]
        actual = struct.unpack("<d", raw)[0]
        expected = EXPECTED_BY_OPERAND[operand_offset]
        results.append({
            "symbol_example": ref["symbol"],
            "instruction_operand_offset": hex(operand_offset),
            "section_offset": hex(section_offset),
            "file_offset": hex(file_offset),
            "raw_bytes_little_endian": raw.hex(),
            "actual_float64": actual,
            "expected_float64": expected,
            "matches_expected": actual == expected,
        })
    all_match = all(item["matches_expected"] for item in results)
    return {
        "schema_version": 1,
        "mode": "read_only_macho_constant_validation",
        "binary": str(binary),
        "binary_size_bytes": len(blob),
        "binary_sha256": sha256_file(binary),
        "section": {
            "segment": section["segment"], "name": section["section"],
            "virtual_address": hex(section["address"]), "size": hex(section["size"]),
            "file_offset": hex(section["file_offset"]),
        },
        "references_found": len(references),
        "unique_constants_checked": len(results),
        "all_constants_match_expected": all_match,
        "constants": results,
        "interpretation": (
            "Both referenced clamp constants match the expected values."
            if all_match else
            "One or more referenced constants do not match the expected values; review required."
        ),
        "limitations": [
            "This verifies constant bytes and address mapping only; it does not prove runtime reachability.",
            "Expected values are grounded in the cited public technical analysis.",
            "No binary was executed and no device was accessed or modified.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True, help="fixed-reference CoreGraphics Mach-O")
    parser.add_argument("--load-commands", type=Path, required=True, help="otool -l output for the same binary")
    parser.add_argument("--function-diff", type=Path, required=True, help="function-diff JSON")
    parser.add_argument("--output", type=Path, default=Path("coregraphics-constant-validation.json"))
    args = parser.parse_args()
    try:
        report = verify(args.binary, args.load_commands, args.function_diff)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, struct.error) as exc:
        print(f"constant validation failed: {exc}", file=sys.stderr)
        return 2
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["all_constants_match_expected"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
