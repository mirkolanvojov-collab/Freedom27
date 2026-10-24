#!/usr/bin/env python3
"""Fast, read-only CoreGraphics binary comparison for pre-extracted dyld caches.

Firmware download/cache construction can take minutes. Once both caches exist,
this tool extracts only CoreGraphics and records hashes, Mach-O UUIDs, sizes,
and architectures. It does not execute a PoC or interact with a device.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_capture(args: list[str]) -> str | None:
    executable = shutil.which(args[0])
    if not executable:
        return None
    result = subprocess.run([executable, *args[1:]], text=True, capture_output=True, check=False)
    if result.returncode:
        return None
    return (result.stdout + result.stderr).strip() or None


def find_coregraphics(root: Path) -> Path:
    matches = [p for p in root.rglob("*") if p.is_file() and p.name.lower() == "coregraphics"]
    if not matches:
        matches = [p for p in root.rglob("*") if p.is_file() and "coregraphics" in p.name.lower()]
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one CoreGraphics binary under {root}, found {len(matches)}")
    return matches[0]


def binary_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "file_type": run_capture(["file", str(path)]),
        "macho_uuid": run_capture(["dwarfdump", "--uuid", str(path)]),
    }


def extract(cache: Path, out_dir: Path) -> Path:
    if not cache.is_file():
        raise FileNotFoundError(f"dyld cache does not exist: {cache}")
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ipsw", "dyld", "extract", str(cache), "CoreGraphics", "--output", str(out_dir)],
        check=True,
    )
    return find_coregraphics(out_dir)


def compare(target_cache: Path, fixed_cache: Path, output: Path) -> dict[str, object]:
    work = output.parent / (output.stem + "-components")
    target_binary = extract(target_cache, work / "target")
    fixed_binary = extract(fixed_cache, work / "fixed")
    target = binary_record(target_binary)
    fixed = binary_record(fixed_binary)
    report = {
        "schema_version": 1,
        "mode": "read_only_binary_metadata_comparison",
        "target": {"build": "23G83", "device": "iPhone17,4", **target},
        "fixed_reference": {"build": "23H30", "device": "iPhone17,4", **fixed},
        "byte_identical": target["sha256"] == fixed["sha256"],
        "interpretation": (
            "Identical bytes for these extracted files."
            if target["sha256"] == fixed["sha256"]
            else "Binary bytes differ; this alone does not attribute the difference to CVE-2026-86950."
        ),
        "limitations": [
            "A hash difference does not identify the changed function or prove vulnerability.",
            "Version/build metadata and extraction provenance must be independently verified.",
            "No exploit was run and no device was accessed or modified.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-cache", type=Path, required=True, help="dyld_shared_cache for target build 23G83")
    parser.add_argument("--fixed-cache", type=Path, required=True, help="dyld_shared_cache for fixed reference build 23H30")
    parser.add_argument("--output", type=Path, default=Path("coregraphics-comparison.json"))
    args = parser.parse_args()
    try:
        report = compare(args.target_cache, args.fixed_cache, args.output)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"comparison failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
