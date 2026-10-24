#!/usr/bin/env python3
"""Resilient, read-only streaming verification of the pinned target IPSW.

Uses HTTP Range to resume after transient connection failures. No firmware is
written to disk, and no device is contacted or modified.
"""
from __future__ import annotations

import hashlib
import http.client
import json
import re
import time
import urllib.error
import urllib.request

URL = "https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw"
EXPECTED_SHA256 = "101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f"
EXPECTED_SIZE_BYTES = 11225458130
CHUNK_SIZE = 8 * 1024 * 1024
TIMEOUT_SECONDS = 180
MAX_RETRIES = 8
RETRYABLE = (urllib.error.URLError, http.client.HTTPException, TimeoutError, OSError)


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


def stream_url_sha256(url: str = URL, expected_size: int = EXPECTED_SIZE_BYTES,
                      opener=urllib.request.urlopen, sleep=time.sleep,
                      max_retries: int = MAX_RETRIES) -> tuple[str, int, int]:
    """Hash a URL stream and resume via Range after transient interruptions.

    Returns (sha256, bytes_read, final_http_status). Refuses to append a response
    unless the server confirms the exact requested byte offset.
    """
    digest = hashlib.sha256()
    total = 0
    retries = 0
    last_status = 0

    while total < expected_size:
        headers = {
            "User-Agent": "Freedom27-read-only-ipsw-integrity-check/1.1",
            "Accept-Encoding": "identity",
        }
        if total:
            headers["Range"] = f"bytes={total}-"
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with opener(request, timeout=TIMEOUT_SECONDS) as response:
                last_status = getattr(response, "status", response.getcode())
                if total == 0 and last_status == 200:
                    pass
                elif last_status == 206:
                    content_range = response.headers.get("Content-Range", "")
                    match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+|\*)", content_range)
                    if not match or int(match.group(1)) != total:
                        raise RuntimeError(f"Unsafe/missing Content-Range for offset {total}: {content_range!r}")
                else:
                    raise RuntimeError(f"Unexpected HTTP status {last_status} at offset {total}")

                while total < expected_size:
                    chunk = response.read(min(CHUNK_SIZE, expected_size - total))
                    if not chunk:
                        break
                    digest.update(chunk)
                    total += len(chunk)
                if total == expected_size:
                    break
                # EOF before expected size: reconnect at the exact byte offset.
                retries += 1
        except RETRYABLE:
            retries += 1

        if total > expected_size:
            raise RuntimeError(f"Response exceeded pinned size: {total} > {expected_size}")
        if retries > max_retries:
            raise RuntimeError(f"Stream interrupted after {max_retries} retries at byte offset {total}")
        if total < expected_size:
            sleep(min(2 ** min(retries, 6), 60))

    return digest.hexdigest(), total, last_status


def main() -> int:
    try:
        actual_sha256, actual_size, http_status = stream_url_sha256()
        result = {
            "source_url": URL,
            "expected_sha256": EXPECTED_SHA256,
            "actual_sha256": actual_sha256,
            "sha256_matches": actual_sha256.lower() == EXPECTED_SHA256.lower(),
            "expected_size_bytes": EXPECTED_SIZE_BYTES,
            "actual_size_bytes": actual_size,
            "size_matches": actual_size == EXPECTED_SIZE_BYTES,
            "verified": actual_sha256.lower() == EXPECTED_SHA256.lower() and actual_size == EXPECTED_SIZE_BYTES,
            "http_status": http_status,
            "resumable_range_requests": True,
            "file_written_to_disk": False,
            "device_modified": False,
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["verified"] else 1
    except (RETRYABLE + (RuntimeError,)) as exc:
        print(json.dumps({
            "source_url": URL,
            "verified": False,
            "error": f"{type(exc).__name__}: {exc}",
            "file_written_to_disk": False,
            "device_modified": False,
        }, indent=2, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
