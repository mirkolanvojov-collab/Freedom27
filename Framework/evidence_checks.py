"""Read-only validation of public evidence metadata for Freedom27."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_ROW_FIELDS = ("device_family", "variant", "os_family", "status", "notes")
REQUIRED_VULN_FIELDS = ("id", "title", "source_url", "status", "summary")
VERIFIED_STATUSES = {"experimental", "verified"}


def _https_url(value: Any) -> bool:
    parsed = urlparse(value) if isinstance(value, str) else None
    return bool(parsed and parsed.scheme == "https" and parsed.netloc)


def check_evidence(root: Path = ROOT) -> list[str]:
    """Return schema/evidence-policy errors; never interacts with a device."""
    errors: list[str] = []
    matrix_path = root / "research" / "compatibility_matrix.json"
    registry_path = root / "research" / "vulnerability_registry.json"
    ledger_path = root / "research" / "evidence_ledger.json"

    try:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"compatibility_matrix.json could not be loaded: {exc}"]
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"vulnerability_registry.json could not be loaded: {exc}"]

    if not isinstance(matrix, dict):
        return ["compatibility matrix root must be an object"]
    allowed = matrix.get("allowed_statuses")
    rows = matrix.get("rows")
    if not isinstance(allowed, list) or not all(isinstance(s, str) for s in allowed):
        errors.append("matrix allowed_statuses must be a list of strings")
        allowed = []
    if not isinstance(rows, list):
        errors.append("matrix rows must be a list")
        rows = []
    for index, row in enumerate(rows):
        prefix = f"matrix row {index}"
        if not isinstance(row, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in REQUIRED_ROW_FIELDS:
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{prefix} missing non-empty {field}")
        status = row.get("status")
        if status not in allowed:
            errors.append(f"{prefix} has disallowed status {status!r}")
        if status in VERIFIED_STATUSES:
            if not _https_url(row.get("evidence_url")):
                errors.append(f"{prefix} status {status} requires an HTTPS evidence_url")
            if status == "verified":
                for field in ("model_identifier", "os_version", "build"):
                    if not isinstance(row.get(field), str) or not row[field].strip():
                        errors.append(f"{prefix} verified status requires {field}")
                notes = str(row.get("notes", "")).lower()
                if any(term in notes for term in ("reported demonstration", "news report", "demo only")):
                    errors.append(f"{prefix} cannot be verified using demo/report-only notes")

    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [f"evidence_ledger.json could not be loaded: {exc}"]

    if not isinstance(ledger, dict):
        errors.append("evidence ledger root must be an object")
        ledger = {}
    ledger_entries = ledger.get("entries")
    if not isinstance(ledger_entries, list):
        errors.append("evidence ledger entries must be a list")
        ledger_entries = []
    allowed_values = ledger.get("allowed_values", {})
    if not isinstance(allowed_values, dict):
        errors.append("evidence ledger allowed_values must be an object")
        allowed_values = {}
    ledger_required = ("id", "evidence_type", "patch_state", "target_applicability",
                       "reproduction_status", "evidence_url", "next_action")
    ledger_ids: set[str] = set()
    for index, item in enumerate(ledger_entries):
        prefix = f"evidence ledger entry {index}"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ledger_required:
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{prefix} missing non-empty {field}")
        item_id = item.get("id")
        if isinstance(item_id, str) and item_id:
            if item_id in ledger_ids:
                errors.append(f"{prefix} duplicate id {item_id}")
            ledger_ids.add(item_id)
        if not _https_url(item.get("evidence_url")):
            errors.append(f"{prefix} evidence_url must be HTTPS")
        for field in ("evidence_type", "patch_state", "target_applicability", "reproduction_status"):
            choices = allowed_values.get(field, [])
            if not isinstance(choices, list) or item.get(field) not in choices:
                errors.append(f"{prefix} has disallowed {field} {item.get(field)!r}")
        if item.get("reproduction_status") == "reported_demo_not_independently_reproduced" and item.get("target_applicability") != "reported_single_device_build":
            errors.append(f"{prefix} reported demo must be scoped to a single reported device/build")
    if not isinstance(registry, dict):
        errors.append("vulnerability registry root must be an object")
        registry = {}
    registry_entries_for_ids = registry.get("entries", [])
    if not isinstance(registry_entries_for_ids, list):
        errors.append("vulnerability registry entries must be a list")
        registry_entries_for_ids = []
    registry_ids = {entry.get("id") for entry in registry_entries_for_ids if isinstance(entry, dict)}
    if ledger_ids != registry_ids:
        errors.append("evidence ledger IDs must match vulnerability registry IDs exactly")
    entries = registry.get("entries")
    if not isinstance(entries, list):
        errors.append("vulnerability registry entries must be a list")
        return errors
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"vulnerability entry {index}"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in REQUIRED_VULN_FIELDS:
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{prefix} missing non-empty {field}")
        entry_id = entry.get("id")
        if isinstance(entry_id, str) and entry_id:
            if entry_id in seen:
                errors.append(f"{prefix} duplicate id {entry_id}")
            seen.add(entry_id)
        if not _https_url(entry.get("source_url")):
            errors.append(f"{prefix} source_url must be HTTPS")
        title_summary = (str(entry.get("title", "")) + " " + str(entry.get("summary", ""))).lower()
        if entry_id in {"apple-cve-2026-28968-kernel-lead", "apple-cve-2026-86886-tcc-lead"}:
            if entry.get("status") != "unverified":
                errors.append(f"{prefix} CVE research lead must remain unverified")
            if "not" not in title_summary and "not equivalent" not in title_summary and "not a public jailbreak" not in title_summary:
                errors.append(f"{prefix} CVE lead must explicitly avoid claiming a confirmed jailbreak chain")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args()
    errors = check_evidence(args.root)
    if errors:
        print("\n".join(errors))
        return 1
    print("Evidence metadata checks passed (no device was tested).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
