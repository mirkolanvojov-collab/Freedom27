#!/usr/bin/env python3
"""Validate the source-pinned iOS 26 public advisory inventory.

This tool performs metadata validation only. It does not fetch advisories,
test vulnerabilities, or infer exploitability.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

CVE_RE = re.compile(r"^CVE-20\d{2}-\d{4,7}$")
ALLOWED_STATUSES = {"partial", "complete", "url_unverified", "source_url_unverified"}
ALLOWED_TARGET_ASSESSMENTS = {"not_assessed", "fixed_in_target_release", "candidate_for_review", "not_applicable"}
REQUIRED_SOURCE_FIELDS = {"release", "url", "extraction_status", "cve_ids", "notes"}
REQUIRED_ENTRY_FIELDS = {"cve_id", "advisory_release", "advisory_url", "evidence_status", "target_assessment"}


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a JSON object"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    sources = data.get("sources")
    entries = data.get("entries")
    if not isinstance(sources, list):
        return errors + ["sources must be a list"]
    if not isinstance(entries, list):
        return errors + ["entries must be a list"]

    by_release: dict[str, dict] = {}
    source_urls: set[str] = set()
    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"sources[{i}] must be an object")
            continue
        missing = REQUIRED_SOURCE_FIELDS - source.keys()
        if missing:
            errors.append(f"sources[{i}] missing fields: {', '.join(sorted(missing))}")
            continue
        release = source.get("release")
        if not isinstance(release, str) or not release.strip():
            errors.append(f"sources[{i}].release must be a non-empty string")
        elif release in by_release:
            errors.append(f"duplicate release source: {release}")
        else:
            by_release[release] = source
        if source.get("extraction_status") not in ALLOWED_STATUSES:
            errors.append(f"sources[{i}].extraction_status is invalid")
        url = source.get("url")
        if url is not None:
            parsed = urlparse(url) if isinstance(url, str) else None
            if not parsed or parsed.scheme != "https" or parsed.hostname != "support.apple.com":
                errors.append(f"sources[{i}].url must be an HTTPS support.apple.com URL")
            elif url in source_urls:
                errors.append(f"duplicate source URL: {url}")
            else:
                source_urls.add(url)
        ids = source.get("cve_ids")
        if not isinstance(ids, list):
            errors.append(f"sources[{i}].cve_ids must be a list")
        else:
            valid_ids = [cve for cve in ids if isinstance(cve, str)]
            if len(valid_ids) != len(set(valid_ids)):
                errors.append(f"sources[{i}].cve_ids contains duplicates")
            for cve in ids:
                if not isinstance(cve, str) or not CVE_RE.fullmatch(cve):
                    errors.append(f"sources[{i}] has invalid CVE identifier: {cve!r}")
        if source.get("extraction_status") == "complete" and not url:
            errors.append(f"sources[{i}] cannot be complete without a verified URL")

    target_context = data.get("target_context", {})
    target_os = target_context.get("os_version_reported_by_user") if isinstance(target_context, dict) else None
    seen_entries: set[tuple[str, str]] = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{i}] must be an object")
            continue
        missing = REQUIRED_ENTRY_FIELDS - entry.keys()
        if missing:
            errors.append(f"entries[{i}] missing fields: {', '.join(sorted(missing))}")
            continue
        cve = entry.get("cve_id")
        release = entry.get("advisory_release")
        url = entry.get("advisory_url")
        if not isinstance(cve, str) or not CVE_RE.fullmatch(cve):
            errors.append(f"entries[{i}].cve_id is invalid")
        if not isinstance(release, str) or release not in by_release:
            errors.append(f"entries[{i}] references unknown or invalid advisory_release: {release!r}")
        elif url != by_release[release].get("url") or not isinstance(url, str) or not url:
            errors.append(f"entries[{i}] advisory_url does not match verified source URL")
        if entry.get("evidence_status") != "public_advisory_only":
            errors.append(f"entries[{i}].evidence_status must be public_advisory_only")
        assessment = entry.get("target_assessment")
        if not isinstance(assessment, str) or assessment not in ALLOWED_TARGET_ASSESSMENTS:
            errors.append(f"entries[{i}].target_assessment is invalid")
        if isinstance(target_os, str) and release == target_os and assessment != "fixed_in_target_release":
            errors.append(f"entries[{i}] is from the reported target release and must be assessed fixed_in_target_release")
        key = (str(release), str(cve))
        if key in seen_entries:
            errors.append(f"duplicate entry for {release}: {cve}")
        seen_entries.add(key)

    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "research/ios26_advisory_cve_master_index_2026-10-23.json"
    )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON from {path}: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    sources = data["sources"]
    print(f"OK: {len(sources)} advisory sources, {len(data['entries'])} normalized CVE entries")
    print("Extraction status counts:", dict(Counter(s["extraction_status"] for s in sources)))
    print("Inventory overall status:", data.get("overall_status", "unspecified"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
