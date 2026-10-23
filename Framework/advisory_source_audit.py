"""Verify advisory candidate IDs against the cited primary Apple security pages.

This is a source-presence check only: it does not establish affected-version
scope, exploitability, or applicability to the target device.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "research" / "ios_26_7_advisory_candidates_2026-10-23.json"
DEFAULT_TIMEOUT = 20


def fetch_text(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Fetch a public primary-source page over HTTPS with a bounded timeout."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "support.apple.com":
        raise ValueError(f"refusing non-Apple or non-HTTPS source: {url}")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Freedom27-AdvisorySourceAudit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def audit_document(document: object, fetcher: Callable[[str], str]) -> dict:
    """Check each candidate CVE appears on its declared Apple source page."""
    errors: list[str] = []
    if not isinstance(document, dict):
        return {"ok": False, "checked": 0, "errors": ["document root must be an object"]}

    source = document.get("source")
    if not isinstance(source, dict) or not isinstance(source.get("url"), str):
        return {"ok": False, "checked": 0, "errors": ["source.url is missing"]}
    source_urls = {source["url"]}
    verified = source.get("verified_against", [])
    if isinstance(verified, list):
        source_urls.update(url for url in verified if isinstance(url, str))

    source_text: dict[str, str] = {}
    for url in sorted(source_urls):
        try:
            source_text[url] = fetcher(url)
        except Exception as exc:
            errors.append(f"source fetch failed for {url}: {type(exc).__name__}: {exc}")

    checked = 0
    candidates = document.get("candidates")
    if not isinstance(candidates, list):
        errors.append("candidates must be a list")
        candidates = []
    for index, item in enumerate(candidates):
        if not isinstance(item, dict):
            errors.append(f"candidate[{index}] must be an object")
            continue
        cve = item.get("id")
        if not isinstance(cve, str) or not re.fullmatch(r"CVE-\d{4}-\d{4,}", cve):
            errors.append(f"candidate[{index}] has invalid CVE identifier")
            continue
        url = item.get("source_url") or source.get("url")
        if url not in source_text:
            errors.append(f"{cve}: source URL was not successfully fetched: {url}")
            continue
        checked += 1
        if cve not in source_text[url]:
            errors.append(f"{cve}: not found in cited Apple source {url}")

    excluded = document.get("excluded_candidates", [])
    if not isinstance(excluded, list):
        errors.append("excluded_candidates must be a list")
        excluded = []
    for index, item in enumerate(excluded):
        if not isinstance(item, dict):
            errors.append(f"excluded_candidates[{index}] must be an object")
            continue
        cve = item.get("id")
        url = item.get("source_url")
        if not isinstance(cve, str) or not isinstance(url, str):
            errors.append(f"excluded_candidates[{index}] requires id and source_url")
            continue
        if url not in source_text:
            errors.append(f"{cve}: excluded-candidate source was not successfully fetched: {url}")
            continue
        checked += 1
        if cve not in source_text[url]:
            errors.append(f"{cve}: not found in cited Apple source {url}")

    return {
        "ok": not errors,
        "checked": checked,
        "source_count": len(source_text),
        "errors": errors,
        "note": "Source presence only; exact affected-version scope and exploitability remain separate questions.",
    }


def main() -> int:
    try:
        document = json.loads(DEFAULT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not load advisory candidate document: {exc}")
        return 2
    report = audit_document(document, fetch_text)
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
