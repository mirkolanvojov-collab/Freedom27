#!/usr/bin/env python3
"""Compare the raw coordinate-safety limit bytes in two CoreGraphics Mach-Os.

This read-only check maps the known __TEXT,__const section-relative offset to
file offsets in each binary. It reports the bytes and decoded little-endian
float64 without assuming an expected limit value or claiming runtime safety.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import re
from pathlib import Path
from typing import Any

SECTION_OFFSET = 0x5A28
WIDTH = 8
SECTION_FIELDS = ("sectname", "segname", "addr", "size", "offset")


def parse_sections(load_commands: str) -> list[dict[str, Any]]:
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


def read_limit(binary_path: Path, load_commands_path: Path) -> dict[str, Any]:
    sections = [s for s in parse_sections(load_commands_path.read_text(encoding="utf-8"))
                if s["segment"] == "__TEXT" and s["section"] == "__const"]
    if len(sections) != 1:
        raise ValueError(f"{binary_path}: expected exactly one __TEXT,__const section; found {len(sections)}")
    section = sections[0]
    if SECTION_OFFSET < 0 or SECTION_OFFSET + WIDTH > section["size"]:
        raise ValueError(f"{binary_path}: section-relative offset {SECTION_OFFSET:#x} is outside __TEXT,__const")
    blob = binary_path.read_bytes()
    file_offset = section["file_offset"] + SECTION_OFFSET
    if file_offset < 0 or file_offset + WIDTH > len(blob):
        raise ValueError(f"{binary_path}: mapped file offset {file_offset:#x} is outside the binary")
    raw = blob[file_offset:file_offset + WIDTH]
    return {
        "binary": str(binary_path),
        "binary_size_bytes": len(blob),
        "binary_sha256": hashlib.sha256(blob).hexdigest(),
        "section": {
            "segment": section["segment"],
            "name": section["section"],
            "virtual_address": hex(section["address"]),
            "size": hex(section["size"]),
            "file_offset": hex(section["file_offset"]),
        },
        "section_relative_offset": hex(SECTION_OFFSET),
        "virtual_address": hex(section["address"] + SECTION_OFFSET),
        "file_offset": hex(file_offset),
        "raw_bytes_little_endian": raw.hex(),
        "float64_little_endian": struct.unpack("<d", raw)[0],
    }


def compare(target_binary: Path, target_load_commands: Path,
            fixed_binary: Path, fixed_load_commands: Path) -> dict[str, Any]:
    target = read_limit(target_binary, target_load_commands)
    fixed = read_limit(fixed_binary, fixed_load_commands)
    equal = target["raw_bytes_little_endian"] == fixed["raw_bytes_little_endian"]
    return {
        "schema_version": 1,
        "mode": "read_only_coordinate_safety_limit_byte_comparison",
        "section_relative_offset": hex(SECTION_OFFSET),
        "width_bytes": WIDTH,
        "raw_bytes_equal": equal,
        "target": target,
        "fixed_reference": fixed,
        "interpretation": (
            "The bytes at the recorded section-relative offset are identical across these builds."
            if equal else
            "The bytes at the recorded section-relative offset differ; confirm that this offset still refers to the same semantic constant before interpreting the difference."
        ),
        "limitations": [
            "The offset is a research lead derived from prior disassembly; this check does not independently prove the value is loaded by the intended function.",
            "Equal bytes do not establish equivalent control flow, correct bounds checks, NaN handling, reachability, or exploitability.",
            "No binary was executed and no device was accessed or modified.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-binary", type=Path, required=True)
    parser.add_argument("--target-load-commands", type=Path, required=True)
    parser.add_argument("--fixed-binary", type=Path, required=True)
    parser.add_argument("--fixed-load-commands", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("coordinate-safety-limit-validation.json"))
    args = parser.parse_args()
    try:
        report = compare(args.target_binary, args.target_load_commands,
                         args.fixed_binary, args.fixed_load_commands)
    except (OSError, ValueError, KeyError, struct.error) as exc:
        print(f"coordinate-safety limit comparison failed: {exc}", file=sys.stderr)
        return 2
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
