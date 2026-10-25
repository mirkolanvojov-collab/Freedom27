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
RECORD_LINE_RE = re.compile(r"^\s*(0x[0-9a-fA-F]+):\s*(.*)$")
HEX_BYTES_RE = re.compile(r"^(?:(?:[0-9a-fA-F]{2})\s+){4}(.*)$")
BRANCH_RE = re.compile(r"^(?:b(?:\.[a-z]+)?|bl|cbz|cbnz|tbz|tbnz)\s+(.+)$", re.I)
ADDRESS_PRESERVED_SYMBOLS = {
    # Coordinate conversion and its direct consumers.
    "_aa_moveto", "_aa_lineto", "_aa_clip_edge", "_aa_clipping",
    "_aa_cubeto", "_aa_quadto", "_aa_rectat", "_aa_add_edges",
    # Preserve dispatch/initialization context for a caller-side invariant trace.
    "_aa_path_iterate", "_aa_path_begin", "_aa_create", "_aa_render_shape",
}


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
    # Disassemble only symbols explicitly located in executable __TEXT,__text.
    # The previous whole-line regex also matched data labels in __TEXT,__const
    # and suffixes such as aa_path_iterator_create.callbacks, then treated them
    # as function entry points. That caused false failures and misleading counts.
    found: set[str] = set()
    for line in output.splitlines():
        row = re.match(r"^\s*(0x[0-9a-fA-F]+):\s+\(([^,]+),([^)]+)\)\s+.*?\s(_?aa_[A-Za-z0-9_$]+)\s*$", line)
        if not row or int(row.group(1), 16) == 0:
            continue
        segment, section, symbol = row.group(2), row.group(3), row.group(4)
        if segment == "__TEXT" and section == "__text":
            found.add(symbol)
    return sorted(found)


def parse_instruction_records(output: str) -> list[dict[str, str]]:
    """Parse instruction addresses and operands before any layout normalization."""
    records: list[dict[str, str]] = []
    for line in output.splitlines():
        match = RECORD_LINE_RE.match(line)
        if not match:
            continue
        address, text = match.group(1), match.group(2).strip()
        byte_match = HEX_BYTES_RE.match(text)
        if byte_match:
            text = byte_match.group(1).strip()
        text = text.split(";", 1)[0].strip()
        text = re.sub(r"\s+", " ", text)
        if text:
            records.append({"address": address, "instruction": text})
    return records


def extract_relocation_sites(output: str, context_size: int = 4) -> list[dict[str, Any]]:
    """Retain raw ADR/ADRP targets plus nearby instructions for manual static review.

    These are review leads only: a displayed address is not a resolved relocation
    or proof that the referenced object has equivalent semantics across builds.
    """
    records = parse_instruction_records(output)
    sites: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not re.match(r"^adrp?\s+", record["instruction"], re.I):
            continue
        start = max(0, index - 1)
        stop = min(len(records), index + context_size + 1)
        instruction = record["instruction"]
        adrp_match = re.match(
            r"^adrp\s+(x[0-9]+),\s*#?(0x[0-9a-fA-F]+)$",
            instruction,
            re.I,
        )
        derived_references: list[dict[str, str]] = []
        if adrp_match:
            base_register = adrp_match.group(1).lower()
            page_address = int(adrp_match.group(2), 16)
            # Only derive addresses from an explicit following memory operand
            # that uses this ADRP destination as its base. Do not guess at
            # chained loads, pointer authentication, or dynamic relocation.
            for candidate in records[index + 1:min(len(records), index + context_size + 1)]:
                access = re.match(
                    r"^(ldr|str|ldur|stur|ldrsw|prfm)\s+.*?\["
                    + re.escape(base_register)
                    + r",\s*#?(0x[0-9a-fA-F]+|[0-9]+)\]$",
                    candidate["instruction"],
                    re.I,
                )
                if access:
                    offset = int(access.group(2), 0)
                    derived_references.append({
                        "access_address": candidate["address"],
                        "access_instruction": candidate["instruction"],
                        "base_page_address": hex(page_address),
                        "offset": hex(offset),
                        "effective_address": hex(page_address + offset),
                        "derivation": "ADRP page target + explicit memory operand offset",
                    })
                    break
        sites.append({
            "instruction_index": index,
            "address": record["address"],
            "instruction": instruction,
            "derived_references": derived_references,
            "context": records[start:stop],
        })
    return sites


def normalize_disassembly(output: str) -> list[str]:
    """Normalize layout/presentation noise for triage, not semantic proof.

    Absolute ADR/ADRP targets and generated local labels vary across builds.
    A matching normalized stream does not prove relocated references resolve
    to equivalent objects; those cases still require manual symbol/relocation review.
    """
    instructions: list[str] = []
    for record in parse_instruction_records(output):
        text = record["instruction"]
        # ADR/ADRP image addresses commonly move between builds. Preserve the
        # opcode/register but mark the target as relocation-sensitive.
        address_match = re.match(r"^(adrp?)\s+([^,]+),\s*#?(0x[0-9a-fA-F]+)(.*)$", text, re.I)
        if address_match:
            text = f"{address_match.group(1)} {address_match.group(2).strip()}, <image-address>{address_match.group(4)}"
        branch = BRANCH_RE.match(text)
        if branch:
            operands = re.sub(r"#?0x[0-9a-fA-F]+", "<branch-target>", branch.group(1))
            operands = re.sub(r"\b(?:loc|sub|LAB|L)_?[0-9a-fA-F]{5,}\b", "<local-label>", operands)
            text = text.split()[0] + " " + operands
        else:
            text = re.sub(r"\b(?:loc|sub|LAB|L)_?[0-9a-fA-F]{5,}\b", "<local-label>", text)
        instructions.append(text)
    return instructions

def disassemble_raw(binary: Path, symbol: str) -> str:
    # ipsw's symbol listing can omit Mach-O's leading C-symbol underscore for
    # an individual entry. Retry that one documented naming variant only when
    # ipsw explicitly reports that the original spelling is absent.
    candidates = [symbol]
    if symbol.startswith("_"):
        candidates.append(symbol[1:])
    else:
        candidates.append("_" + symbol)
    last_error: RuntimeError | None = None
    for candidate in candidates:
        try:
            output = run([
                # Do not pass --count: ipsw then uses Mach-O function boundaries
                # instead of reading a fixed number of instructions past the start.
                "ipsw", "macho", "disass", "--force", "--symbol", candidate,
                str(binary),
            ])
        except RuntimeError as exc:
            last_error = exc
            if "symbol not found in macho symtab" in str(exc).lower():
                continue
            raise
        if re.search(r"disassembling 100 instructions at", output, re.IGNORECASE):
            raise RuntimeError(
                f"ipsw could not determine the function boundary for {candidate} in {binary}; "
                "refusing its 100-instruction fallback"
            )
        if parse_instruction_records(output):
            return output
        last_error = RuntimeError(
            f"disassembler returned no parseable instructions for {candidate} in {binary}"
        )
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"unable to disassemble {symbol} in {binary}")


def disassemble(binary: Path, symbol: str) -> list[str]:
    return normalize_disassembly(disassemble_raw(binary, symbol))


def digest_instructions(instructions: list[str]) -> str:
    payload = "\n".join(instructions).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def parse_macho_sections(load_commands: str) -> list[dict[str, Any]]:
    """Parse section virtual-address ranges from `otool -l` output."""
    sections: list[dict[str, Any]] = []
    for block in re.split(r"(?m)^\s*Section\s*$", load_commands)[1:]:
        fields: dict[str, str] = {}
        for key in ("sectname", "segname", "addr", "size"):
            match = re.search(rf"(?m)^\s*{key}\s+(\S+)", block)
            if match:
                fields[key] = match.group(1)
        if not all(key in fields for key in ("sectname", "segname", "addr", "size")):
            continue
        try:
            address, size = int(fields["addr"], 0), int(fields["size"], 0)
        except ValueError:
            continue
        if size > 0:
            sections.append({"segment": fields["segname"], "section": fields["sectname"], "address": address, "size": size})
    return sections


def classify_address(address: int, sections: list[dict[str, Any]]) -> dict[str, Any]:
    """Classify an effective address against parsed Mach-O section ranges."""
    for section in sections:
        start = section["address"]
        if start <= address < start + section["size"]:
            return {"classification": "inside_section", "segment": section["segment"],
                    "section": section["section"], "section_offset": hex(address - start)}
    return {"classification": "outside_listed_sections"}


def annotate_references(report: dict[str, Any], target_sections: list[dict[str, Any]],
                        fixed_sections: list[dict[str, Any]]) -> None:
    """Add conservative section-relative labels to explicit ADRP+memory references."""
    for symbol in report.get("symbols", []):
        for side, sections in (("target", target_sections), ("fixed", fixed_sections)):
            for site in symbol.get(f"{side}_relocation_sensitive_sites", []):
                for reference in site.get("derived_references", []):
                    try:
                        address = int(reference["effective_address"], 0)
                    except (KeyError, ValueError):
                        continue
                    reference["section_resolution"] = classify_address(address, sections)


def compare(target_binary: Path, fixed_binary: Path, target_sections: list[dict[str, Any]] | None = None, fixed_sections: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if not target_binary.is_file() or not fixed_binary.is_file():
        raise FileNotFoundError("both CoreGraphics Mach-O paths must exist")
    target_symbols = discover_symbols(target_binary)
    fixed_symbols = discover_symbols(fixed_binary)
    common = sorted(set(target_symbols) & set(fixed_symbols))
    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for symbol in common:
        try:
            target_raw = disassemble_raw(target_binary, symbol)
            fixed_raw = disassemble_raw(fixed_binary, symbol)
            target_ins = normalize_disassembly(target_raw)
            fixed_ins = normalize_disassembly(fixed_raw)
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
            item["target_relocation_sensitive_sites"] = extract_relocation_sites(target_raw)
            item["fixed_relocation_sensitive_sites"] = extract_relocation_sites(fixed_raw)
        # Preserve raw addresses for conversion sites and the downstream edge
        # consumer even when normalized streams are identical. Normalization
        # erases branch destinations needed for CFG and bounds review.
        if symbol in ADDRESS_PRESERVED_SYMBOLS:
            item["target_addressed_instructions"] = parse_instruction_records(target_raw)
            item["fixed_addressed_instructions"] = parse_instruction_records(fixed_raw)
        results.append(item)

    changed = [item for item in results if not item["instruction_stream_identical"]]
    report = {
        "schema_version": 3,
        "mode": "read_only_symbol_scoped_disassembly_comparison",
        "target_binary": str(target_binary),
        "fixed_reference_binary": str(fixed_binary),
        "function_boundary_mode": "ipsw Mach-O function metadata; no fixed instruction count",
        "target_aa_symbol_count": len(target_symbols),
        "fixed_aa_symbol_count": len(fixed_symbols),
        "common_aa_symbol_count": len(common),
        "successfully_compared_symbol_count": len(results),
        "changed_symbol_count": len(changed),
        "layout_normalization_note": "ADR/ADRP image addresses, generated local labels, branch targets, and disassembler comments are normalized for triage. For changed functions, raw ADR/ADRP addresses and nearby instructions are also retained as relocation-review leads; these do not resolve relocations or prove semantic equivalence.",
        "changed_symbols": [item["symbol"] for item in changed],
        "symbols": results,
        "disassembly_failures": failures,
        "interpretation": (
            "One or more layout-normalized shared aa_* instruction streams differ; inspect changes and relocation-sensitive references before attributing anything to CVE-2026-86950."
            if changed else
            "No differences were established among successfully compared shared aa_* symbol instruction streams. Missing symbols, truncated streams, or failed disassemblies may limit coverage."
        ),
        "limitations": [
            "Only symbols discoverable through ipsw's Mach-O symbol listing are compared.",
            "Function boundaries depend on Mach-O function metadata; symbols without reliable boundaries may fail closed.",
            "Compiler/build changes may alter instructions for reasons unrelated to the CVE.",
            "Layout normalization is triage only: matching ADR/ADRP placeholders do not prove references resolve to equivalent objects.",
            "This static comparison does not establish runtime reachability or exploitability.",
            "No binary was executed; no crafted input or device was used.",
        ],
    }
    if target_sections is not None and fixed_sections is not None:
        annotate_references(report, target_sections, fixed_sections)
        report["section_resolution_note"] = (
            "Effective addresses are classified only against supplied otool section ranges. "
            "Addresses outside listed sections may belong to another image or unresolved shared-cache mapping; "
            "section membership does not establish data semantics or vulnerability attribution."
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-binary", type=Path, required=True)
    parser.add_argument("--fixed-binary", type=Path, required=True)
    parser.add_argument("--target-load-commands", type=Path, help="otool -l output for the target binary")
    parser.add_argument("--fixed-load-commands", type=Path, help="otool -l output for the fixed binary")
    parser.add_argument("--output", type=Path, default=Path("coregraphics-function-diff.json"))
    args = parser.parse_args()
    try:
        if bool(args.target_load_commands) != bool(args.fixed_load_commands):
            raise RuntimeError("both load-command files must be supplied together")
        if args.target_load_commands and args.fixed_load_commands:
            target_sections = parse_macho_sections(args.target_load_commands.read_text(encoding="utf-8"))
            fixed_sections = parse_macho_sections(args.fixed_load_commands.read_text(encoding="utf-8"))
            report = compare(args.target_binary, args.fixed_binary, target_sections, fixed_sections)
        else:
            report = compare(args.target_binary, args.fixed_binary)
    except (OSError, RuntimeError) as exc:
        print(f"function comparison failed: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "symbols"}, indent=2))
    if report["common_aa_symbol_count"] == 0:
        print("no shared executable aa_* symbols were found; refusing a false-success result", file=sys.stderr)
        return 3
    if report["successfully_compared_symbol_count"] == 0:
        print("no shared aa_* symbols were successfully disassembled; refusing a false-success result", file=sys.stderr)
        return 3
    if report["disassembly_failures"]:
        print(
            f"comparison incomplete: {len(report['disassembly_failures'])} symbol disassembly attempt(s) failed; refusing a false-success result",
            file=sys.stderr,
        )
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
