#!/usr/bin/env python3
"""Verify a locally obtained IPSW against a pinned SHA-256.

This tool deliberately does not download firmware or interact with a device.
Obtain the IPSW from Apple's CDN through a trusted channel, then run:
  python research/scripts/verify_ipsw_sha256.py /path/to/iPhone17,4_26.6.1_23G83_Restore.ipsw
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

TARGET = {
    "device_model": "iPhone 16 Plus",
    "model_identifier": "iPhone17,4",
    "ios_version": "26.6.1",
    "build_number": "23G83",
    "expected_sha256": "101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f",
    "source_url": "https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(path: Path) -> dict[str, object]:
    result: dict[str, object] = {
        **TARGET,
        "file": str(path),
        "verified": False,
        "verification_method": "local streaming SHA-256; 1 MiB chunks",
    }
    if not path.is_file():
        result["error"] = "Input path is not a regular file."
        return result
    result["size_bytes"] = path.stat().st_size
    actual = sha256_file(path)
    result["actual_sha256"] = actual
    result["verified"] = actual.lower() == TARGET["expected_sha256"].lower()
    if not result["verified"]:
        result["error"] = "SHA-256 mismatch; do not use this file as the target firmware."
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ipsw", type=Path, help="path to an already downloaded IPSW")
    args = parser.parse_args()
    result = verify(args.ipsw)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
