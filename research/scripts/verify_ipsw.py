#!/usr/bin/env python3
"""Verify a locally downloaded, exact-target IPSW without touching a device.

The script deliberately does not download, restore, mount, decrypt, or execute
firmware. It streams the file for SHA-256 and optionally checks ZIP CRCs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

TARGET_FILENAME = "iPhone17,4_26.6.1_23G83_Restore.ipsw"
EXPECTED_SHA256 = "101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f"
EXPECTED_SIZE_BYTES = 11225458130


def calculate_sha256(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    """Hash a file in bounded memory, suitable for multi-gigabyte IPSWs."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def verify_ipsw(
    path: Path,
    expected_sha256: str = EXPECTED_SHA256,
    expected_size: int = EXPECTED_SIZE_BYTES,
    check_zip: bool = False,
) -> dict:
    """Return a machine-readable result; never modifies the input file."""
    path = Path(path)
    result = {
        "path": str(path),
        "target_filename": TARGET_FILENAME,
        "expected_sha256": expected_sha256,
        "expected_size_bytes": expected_size,
        "exists": path.is_file(),
        "filename_matches": path.name == TARGET_FILENAME,
        "actual_size_bytes": None,
        "actual_sha256": None,
        "sha256_matches": False,
        "size_matches": False,
        "zip_crc_check_requested": check_zip,
        "zip_crc_check_passed": None,
        "verified": False,
        "device_modified": False,
        "download_performed": False,
    }
    if not path.is_file():
        result["error"] = "Input path is not a regular file."
        return result

    result["actual_size_bytes"] = path.stat().st_size
    result["size_matches"] = result["actual_size_bytes"] == expected_size
    result["actual_sha256"] = calculate_sha256(path)
    result["sha256_matches"] = result["actual_sha256"].lower() == expected_sha256.lower()

    if check_zip:
        try:
            with zipfile.ZipFile(path) as archive:
                bad_member = archive.testzip()
            result["zip_crc_check_passed"] = bad_member is None
            if bad_member is not None:
                result["error"] = f"ZIP CRC failure in member: {bad_member}"
        except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
            result["zip_crc_check_passed"] = False
            result["error"] = f"ZIP validation failed: {type(exc).__name__}: {exc}"

    result["verified"] = (
        result["filename_matches"]
        and result["size_matches"]
        and result["sha256_matches"]
        and (not check_zip or result["zip_crc_check_passed"] is True)
    )
    if not result["filename_matches"]:
        result["error"] = "Filename does not match the pinned target IPSW."
    elif not result["size_matches"]:
        result["error"] = "File size differs from the published target size."
    elif not result["sha256_matches"]:
        result["error"] = "SHA-256 differs from the published reference value."
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ipsw", type=Path, help="Path to the already-downloaded target IPSW")
    parser.add_argument(
        "--check-zip",
        action="store_true",
        help="Also read and CRC-check every ZIP member; this can take substantial time",
    )
    args = parser.parse_args()
    result = verify_ipsw(args.ipsw, check_zip=args.check_zip)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
