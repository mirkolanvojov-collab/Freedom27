"""Fail-closed validation for source-pinned Freedom27 research leads.

This validates metadata only. It does not discover vulnerabilities, execute
proofs of concept, or establish that a claim applies to an iOS build.
"""
from __future__ import annotations

import re
from typing import Any, Iterable

STATUSES = {"queued", "reviewed", "not_applicable", "reproduced_in_lab"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_TARGET_FIELDS = ("device_model", "model_identifier", "os_version", "build")


def validate_manifest(items: Iterable[dict[str, Any]]) -> list[str]:
    """Return errors for incomplete, mutable, duplicate, or overclaimed records."""
    errors: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(items):
        prefix = f"item[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: record must be an object")
            continue
        record_id = item.get("id")
        if not isinstance(record_id, str) or not record_id.strip():
            errors.append(f"{prefix}: id must be a non-empty string")
        elif record_id in seen:
            errors.append(f"{prefix}: duplicate id {record_id!r}")
        else:
            seen.add(record_id)

        for field in ("title", "source_url", "source_revision", "claim", "status"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{prefix}: {field} must be a non-empty string")

        source_url = item.get("source_url", "")
        if isinstance(source_url, str) and source_url and not source_url.startswith("https://"):
            errors.append(f"{prefix}: source_url must use HTTPS")

        revision = item.get("source_revision", "")
        if isinstance(revision, str) and revision and not SHA40.fullmatch(revision):
            errors.append(f"{prefix}: source_revision must be a full 40-character commit SHA")

        status = item.get("status")
        if status not in STATUSES:
            errors.append(f"{prefix}: status must be one of {', '.join(sorted(STATUSES))}")

        target = item.get("target")
        if not isinstance(target, dict):
            errors.append(f"{prefix}: target must specify the exact target tuple")
        else:
            for field in REQUIRED_TARGET_FIELDS:
                value = target.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{prefix}: target.{field} must be a non-empty string")

        evidence = item.get("evidence_note", "")
        if status == "reproduced_in_lab":
            if not isinstance(evidence, str) or not evidence.strip():
                errors.append(f"{prefix}: reproduced_in_lab requires an evidence_note")
            if item.get("independent_reproduction") is not True:
                errors.append(f"{prefix}: reproduced_in_lab requires independent_reproduction=true")
        if status == "not_applicable" and not isinstance(evidence, str):
            errors.append(f"{prefix}: evidence_note must be a string when supplied")
    return errors


def target_key(target: dict[str, str]) -> str:
    """Stable human-readable exact-target key; does not imply compatibility."""
    return "|".join(target.get(field, "").strip() for field in REQUIRED_TARGET_FIELDS)
