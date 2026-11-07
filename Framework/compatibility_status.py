"""Read-only, exact-build compatibility report for Freedom27.

This tool evaluates repository evidence metadata only. It never probes or modifies
an iPhone, downloads exploits, or claims that absence of a public tool proves
that no vulnerability exists.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
ALLOWED = {"not-investigated", "researching", "theoretical", "experimental", "verified", "not-supported"}


def _text(value: object) -> str:
    """Normalize only actual strings; null and other types stay missing."""
    return value.strip() if isinstance(value, str) else ""

def _valid_evidence_url(value: object) -> bool:
    """Accept only well-formed HTTPS evidence URLs without embedded credentials."""
    try:
        parsed = urlparse(value) if isinstance(value, str) else None
        if not (
            parsed and parsed.scheme == "https" and parsed.hostname
            and not parsed.username and not parsed.password
        ):
            return False
        _ = parsed.port
        return True
    except ValueError:
        return False

def _read(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def assess_target(root: Path = ROOT) -> dict[str, Any]:
    """Return target identity and a cautious status derived from exact-build evidence."""
    profile = _read(root / "research" / "target_profile.json")
    status_path = root / "research" / "target_status.json"
    status_data = _read(status_path) if status_path.exists() else {"claims": []}
    if not isinstance(profile, dict):
        return {
            "target": {"device_model": "", "model_identifier": "", "os_version": "", "build_number": ""},
            "status": "invalid-input",
            "summary": "Target profile root must be a JSON object.",
            "matching_claims": [],
            "errors": ["target profile root must be a JSON object"],
            "scope_note": "Repository metadata check only; not a device test.",
        }
    input_errors: list[str] = []
    if not isinstance(status_data, dict):
        input_errors.append("target status root must be a JSON object")
        status_data = {"claims": []}
    claims = status_data.get("claims", [])
    if not isinstance(claims, list):
        input_errors.append("target status claims must be a list")
        claims = []
    identity = {
        "device_model": _text(profile.get("device_model")),
        "model_identifier": _text(profile.get("model_identifier")),
        "os_version": _text(profile.get("exact_os_version")),
        "build_number": _text(profile.get("build_number")),
    }
    errors = input_errors + [f"{key} is missing" for key, value in identity.items() if not value]
    matches = []
    for item in claims:
        if not isinstance(item, dict):
            continue
        if all(_text(item.get(key)) == identity[key] for key in ("device_model", "model_identifier", "os_version", "build_number")):
            matches.append(item)

    valid = []
    for item in matches:
        status = _text(item.get("status"))
        url = _text(item.get("evidence_url"))
        notes = _text(item.get("notes"))
        if status not in ALLOWED:
            errors.append(f"matching claim has invalid status: {status}")
            continue
        if status in {"verified", "not-supported"} and (not _valid_evidence_url(url) or not notes):
            errors.append(f"{status} claim requires an HTTPS evidence URL and review notes")
            continue
        # Store the normalized status used by validation so whitespace cannot
        # leak back into the report or evade conflict detection.
        valid.append({**item, "status": status})

    # Conflicting exact-build claims are not silently resolved by choosing one.
    statuses = {item["status"] for item in valid}
    if len(statuses) > 1:
        result_status = "conflicting-evidence"
        summary = "Conflicting exact-build claims need manual review."
    elif valid:
        result_status = valid[0]["status"]
        summary = str(valid[0].get("summary", "Exact-build evidence record found."))
    else:
        result_status = "unknown"
        summary = "No reviewed evidence record matches this exact model, OS version, and build."

    return {
        "target": identity,
        "status": result_status,
        "summary": summary,
        "matching_claims": valid,
        "errors": errors,
        "scope_note": (
            "Repository metadata check only; not a device test. 'not-supported' means "
            "no supported public tool is documented for this exact target in the cited "
            "sources, not proof that no exploitable vulnerability exists."
        ),
    }


def format_report(report: dict[str, Any]) -> str:
    target = report["target"]
    lines = [
        "Freedom27 exact-build compatibility report",
        f"Device: {target['device_model']} ({target['model_identifier']})",
        f"OS: {target['os_version']} (build {target['build_number']})",
        f"Status: {report['status']}",
        f"Finding: {report['summary']}",
        f"Evidence records matched: {len(report['matching_claims'])}",
        report["scope_note"],
    ]
    for item in report["matching_claims"]:
        if item.get("evidence_url"):
            lines.append(f"Evidence: {item['evidence_url']}")
        if item.get("notes"):
            lines.append(f"Review: {item['notes']}")
    if report["errors"]:
        lines.append("Metadata errors:")
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines)


def main() -> int:
    try:
        report = assess_target()
    except (OSError, json.JSONDecodeError, TypeError, AttributeError) as exc:
        print(f"Compatibility check failed: {exc}")
        return 2
    print(format_report(report))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
