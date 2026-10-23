"""Validate source-pinned iOS 26.7 advisory candidate metadata.

This is a documentation validator only; it never interacts with an iOS device.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = ROOT / "research" / "ios_26_7_advisory_candidates_2026-10-23.json"
REQUIRED_CANDIDATE_FIELDS = (
    "id", "component", "published_impact", "fix_summary", "fixed_release",
    "target_applicability", "reproduction_status", "chain_status", "priority", "reason",
)
# This file is advisory metadata only. Positive target/reproduction claims must
# be supported in a separate evidence record, never asserted in this dataset.
# This explicit status records version-range evidence only; it must not be
# interpreted as confirmation for the exact device/build.
ALLOWED_TARGET_STATUS = {
    "not_established",
    "public_version_range_includes_26_6_1_exact_build_unverified",
}
ALLOWED_REPRODUCTION = {"not_reproduced_by_Freedom27"}


def validate_document(document: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["root must be an object"]
    if document.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    target = document.get("target")
    if not isinstance(target, dict):
        errors.append("target must be an object")
    else:
        for key in ("device_model", "model_identifier", "os_version", "build"):
            if not isinstance(target.get(key), str) or not target[key].strip():
                errors.append(f"target.{key} must be non-empty")
    source = document.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        url = source.get("url", "")
        parsed = urlparse(url) if isinstance(url, str) else None
        if not parsed or parsed.scheme != "https" or not parsed.netloc:
            errors.append("source.url must be HTTPS")
        for key in ("title", "published", "reviewed"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                errors.append(f"source.{key} must be non-empty")
    policy = document.get("policy")
    if not isinstance(policy, dict):
        errors.append("policy must be an object")
    else:
        for key in ("device_accessed", "device_modified", "exploit_executed", "third_party_jailbreak_toolchain_used"):
            if policy.get(key) is not False:
                errors.append(f"policy.{key} must remain false for this research workflow")
    candidates = document.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append("candidates must be a non-empty list")
        return errors
    seen: set[str] = set()
    for i, item in enumerate(candidates):
        prefix = f"candidate[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in REQUIRED_CANDIDATE_FIELDS:
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{prefix}.{key} must be non-empty")
        candidate_id = item.get("id")
        if isinstance(candidate_id, str) and candidate_id:
            if candidate_id in seen:
                errors.append(f"{prefix} duplicate id {candidate_id}")
            seen.add(candidate_id)
        target_applicability = item.get("target_applicability")
        if not isinstance(target_applicability, str) or target_applicability not in ALLOWED_TARGET_STATUS:
            errors.append(f"{prefix}.target_applicability is not allowed")
        reproduction_status = item.get("reproduction_status")
        if not isinstance(reproduction_status, str) or reproduction_status not in ALLOWED_REPRODUCTION:
            errors.append(f"{prefix}.reproduction_status is not allowed")
        if item.get("chain_status") != "not_established":
            errors.append(f"{prefix}.chain_status must remain not_established in advisory-only metadata")
    required = document.get("required_evidence_for_upgrade")
    if not isinstance(required, list) or not required or not all(isinstance(x, str) and x.strip() for x in required):
        errors.append("required_evidence_for_upgrade must be a non-empty list of strings")
    return errors


def check_file(path: Path = DEFAULT_PATH) -> list[str]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"candidate document could not be loaded: {exc}"]
    return validate_document(document)


def main() -> int:
    errors = check_file()
    if errors:
        print("\n".join(errors))
        return 1
    document = json.loads(DEFAULT_PATH.read_text(encoding="utf-8"))
    print(f"Advisory candidate metadata valid: {len(document['candidates'])} candidates; metadata only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
