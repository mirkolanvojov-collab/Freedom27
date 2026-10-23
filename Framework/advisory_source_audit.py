"""Verify candidate CVE IDs against their declared primary Apple source pages.

This is a source-presence check only. It does not establish affected-version
scope, exploitability, or applicability to a target device.
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "research" / "ios_26_7_advisory_candidates_2026-10-23.json"
DEFAULT_TIMEOUT = 20
CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,}")


def fetch_text(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Fetch a public primary-source page over HTTPS with a bounded timeout."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "support.apple.com":
        raise ValueError(f"refusing non-Apple or non-HTTPS source: {url}")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Freedom27-AdvisorySourceAudit/1.1"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def _valid_cve(value: object) -> bool:
    return isinstance(value, str) and CVE_PATTERN.fullmatch(value) is not None


def audit_document(document: object, fetcher: Callable[[str], str]) -> dict:
    """Check candidate and excluded CVE IDs on each item's declared source URL."""
    errors: list[str] = []
    if not isinstance(document, dict):
        return {"ok": False, "checked": 0, "errors": ["document root must be an object"]}

    source = document.get("source")
    if not isinstance(source, dict) or not isinstance(source.get("url"), str):
        return {"ok": False, "checked": 0, "errors": ["source.url is missing"]}

    candidates = document.get("candidates")
    if not isinstance(candidates, list):
        errors.append("candidates must be a list")
        candidates = []
    excluded = document.get("excluded_candidates", [])
    if not isinstance(excluded, list):
        errors.append("excluded_candidates must be a list")
        excluded = []

    records: list[tuple[str, str, str]] = []
    for section, items in (("candidate", candidates), ("excluded_candidate", excluded)):
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{section}[{index}] must be an object")
                continue
            cve = item.get("id")
            if not _valid_cve(cve):
                errors.append(f"{section}[{index}] has invalid CVE identifier")
                continue
            url = item.get("source_url") or source["url"]
            if not isinstance(url, str):
                errors.append(f"{cve}: source URL must be a string")
                continue
            records.append((cve, url, section))

    urls = {url for _, url, _ in records}
    urls.add(source["url"])
    verified = source.get("verified_against", [])
    if isinstance(verified, list):
        urls.update(url for url in verified if isinstance(url, str))

    source_text: dict[str, str] = {}
    for url in sorted(urls):
        try:
            source_text[url] = fetcher(url)
        except Exception as exc:
            errors.append(f"source fetch failed for {url}: {type(exc).__name__}: {exc}")

    checked = 0
    for cve, url, section in records:
        if url not in source_text:
            errors.append(f"{cve}: {section} source was not successfully fetched: {url}")
            continue
        checked += 1
        if cve not in source_text[url]:
            errors.append(f"{cve}: not found in cited Apple source {url}")

    return {
        "ok": not errors,
        "checked": checked,
        "source_count": len(source_text),
        "errors": errors,
        "note": "Source presence only; affected-version scope and exploitability remain separate questions.",
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
