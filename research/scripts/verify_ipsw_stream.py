#!/usr/bin/env python3
"""Stream and verify the pinned target IPSW directly from Apple's CDN.

No file is written to disk. This is intended for an explicitly dispatched,
read-only CI job; it never installs or modifies a device.
"""
from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request

URL = "https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw"
EXPECTED_SHA256 = "101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f"
EXPECTED_SIZE_BYTES = 11225458130
CHUNK_SIZE = 8 * 1024 * 1024


def digest_stream(stream, chunk_size: int = CHUNK_SIZE) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        digest.update(chunk)
        total += len(chunk)
    return digest.hexdigest(), total


def verify_stream(stream, expected_sha256: str = EXPECTED_SHA256,
                  expected_size: int = EXPECTED_SIZE_BYTES) -> dict:
    actual_sha256, actual_size = digest_stream(stream)
    return {
        "source_url": URL,
        "expected_sha256": expected_sha256,
        "actual_sha256": actual_sha256,
        "sha256_matches": actual_sha256.lower() == expected_sha256.lower(),
        "expected_size_bytes": expected_size,
        "actual_size_bytes": actual_size,
        "size_matches": actual_size == expected_size,
        "verified": actual_sha256.lower() == expected_sha256.lower() and actual_size == expected_size,
        "file_written_to_disk": False,
        "device_modified": False,
    }


def main() -> int:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Freedom27-read-only-ipsw-integrity-check/1.0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            result = verify_stream(response)
            result["http_status"] = response.status
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(json.dumps({
            "source_url": URL,
            "verified": False,
            "error": f"{type(exc).__name__}: {exc}",
            "file_written_to_disk": False,
            "device_modified": False,
        }, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
