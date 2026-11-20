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


def read_limit(binary_path: Path, load_commands_path: Path,
               disassembly_path: Path | None = None) -> dict[str, Any]:
    sections = [s for s in parse_sections(load_commands_path.read_text(encoding="utf-8"))
                if s["segment"] == "__TEXT" and s["section"] == "__const"]
    if len(sections) != 1:
        raise ValueError(f"{binary_path}: expected exactly one __TEXT,__const section; found {len(sections)}")
    section = sections[0]
    # Prefer the address actually loaded by _path_coordinates_are_safe. The
    # historical section offset remains available only as an explicitly labeled
    # fallback for older callers; offsets are not stable semantic identifiers.
    section_offset = SECTION_OFFSET
    address_source = "legacy_section_relative_offset"
    if disassembly_path is not None:
        disassembly = disassembly_path.read_text(encoding="utf-8", errors="replace")
        adrp_pages: dict[str, int] = {}
        effective_address = None
        for line in disassembly.splitlines():
            adrp = re.search(r"\badrp\s+(x\d+),\s*(0x[0-9a-fA-F]+)", line)
            if adrp:
                adrp_pages[adrp.group(1)] = int(adrp.group(2), 16)
                continue
            load = re.search(r"\bldr\s+d4,\s*\[(x\d+),\s*#(0x[0-9a-fA-F]+)\]", line)
            if load and load.group(1) in adrp_pages:
                candidate = adrp_pages[load.group(1)] + int(load.group(2), 16)
                if section["address"] <= candidate and candidate + WIDTH <= section["address"] + section["size"]:
                    effective_address = candidate
                    break
        if effective_address is None:
            raise ValueError(f"{binary_path}: could not resolve the d4 load address from _path_coordinates_are_safe disassembly")
        section_offset = effective_address - section["address"]
        address_source = "resolved_adrp_ldr_from_path_coordinates_are_safe"
    if section_offset < 0 or section_offset + WIDTH > section["size"]:
        raise ValueError(f"{binary_path}: section-relative offset {section_offset:#x} is outside __TEXT,__const")
    blob = binary_path.read_bytes()
    file_offset = section["file_offset"] + section_offset
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
        "section_relative_offset": hex(section_offset),
        "address_source": address_source,
        "virtual_address": hex(section["address"] + section_offset),
        "file_offset": hex(file_offset),
        "raw_bytes_little_endian": raw.hex(),
        "float64_little_endian": struct.unpack("<d", raw)[0],
    }


def compare(target_binary: Path, target_load_commands: Path,
            fixed_binary: Path, fixed_load_commands: Path,
            target_disassembly: Path | None = None,
            fixed_disassembly: Path | None = None) -> dict[str, Any]:
    target = read_limit(target_binary, target_load_commands, target_disassembly)
    fixed = read_limit(fixed_binary, fixed_load_commands, fixed_disassembly)
    semantic_resolution = target_disassembly is not None and fixed_disassembly is not None
    equal = target["raw_bytes_little_endian"] == fixed["raw_bytes_little_endian"]
    return {
        "schema_version": 1,
        "mode": "read_only_coordinate_safety_limit_byte_comparison",
        "section_relative_offset": hex(SECTION_OFFSET) if not semantic_resolution else None,
        "comparison_basis": "resolved_load_addresses" if semantic_resolution else "legacy_section_relative_offset",
        "width_bytes": WIDTH,
        "raw_bytes_equal": equal,
        "target": target,
        "fixed_reference": fixed,
        "interpretation": (
            "The bytes loaded into d4 by _path_coordinates_are_safe are identical across these builds."
            if equal and semantic_resolution else
            "The bytes loaded into d4 by _path_coordinates_are_safe differ across these builds; verify surrounding dataflow and intended semantics."
            if not equal and semantic_resolution else
            "The bytes at the recorded section-relative offset are identical across these builds."
            if equal else
            "The bytes at the recorded section-relative offset differ; confirm that this offset still refers to the same semantic constant before interpreting the difference."
        ),
        "limitations": [
            "The legacy section offset is not a stable semantic identifier; when disassembly is supplied, the tool resolves the d4 load in _path_coordinates_are_safe but does not prove all uses or runtime reachability.",
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
    parser.add_argument("--target-disassembly", type=Path, help="disassembly of target _path_coordinates_are_safe")
    parser.add_argument("--fixed-disassembly", type=Path, help="disassembly of reference _path_coordinates_are_safe")
    parser.add_argument("--output", type=Path, default=Path("coordinate-safety-limit-validation.json"))
    args = parser.parse_args()
    try:
        if bool(args.target_disassembly) != bool(args.fixed_disassembly):
            raise ValueError("provide both --target-disassembly and --fixed-disassembly, or neither")
        report = compare(args.target_binary, args.target_load_commands,
                         args.fixed_binary, args.fixed_load_commands,
                         args.target_disassembly, args.fixed_disassembly)
    except (OSError, ValueError, KeyError, struct.error) as exc:
        print(f"coordinate-safety limit comparison failed: {exc}", file=sys.stderr)
        return 2
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
