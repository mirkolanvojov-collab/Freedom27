"""Fail-closed checks for exact-target compatibility claims in public research metadata."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent


def _https(value: object) -> bool:
    parsed = urlparse(value) if isinstance(value, str) else None
    return bool(parsed and parsed.scheme == "https" and parsed.netloc)


def check_claim_evidence(root: Path = ROOT) -> list[str]:
    """Reject verified claims lacking exact device/version/build and public evidence."""
    errors: list[str] = []
    registry_path = root / "research" / "vulnerability_registry.json"
    ledger_path = root / "research" / "evidence_ledger.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"claim-evidence metadata could not be loaded: {exc}"]

    entries = registry.get("entries") if isinstance(registry, dict) else None
    if not isinstance(entries, list):
        return ["vulnerability registry entries must be a list"]
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"registry entry {index} must be an object")
            continue
        if entry.get("status") == "verified":
            for field in ("target_device", "target_os_version", "target_build"):
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    errors.append(
                        f"registry entry {index} verified claim requires exact {field}"
                    )
            if not _https(entry.get("verification_url")):
                errors.append(
                    f"registry entry {index} verified claim requires HTTPS verification_url"
                )
            if not _https(entry.get("source_url")):
                errors.append(
                    f"registry entry {index} verified claim requires HTTPS source_url"
                )

    ledger_entries = ledger.get("entries") if isinstance(ledger, dict) else None
    if not isinstance(ledger_entries, list):
        return errors + ["evidence ledger entries must be a list"]
    for index, item in enumerate(ledger_entries):
        if not isinstance(item, dict):
            errors.append(f"evidence ledger entry {index} must be an object")
            continue
        if item.get("target_applicability") == "reported_single_device_build":
            if not isinstance(item.get("exact_target_build"), str) or not item["exact_target_build"].strip():
                errors.append(
                    f"evidence ledger entry {index} reported single-device applicability "
                    "requires exact_target_build"
                )
            if item.get("reproduction_status") != "reported_demo_not_independently_reproduced":
                errors.append(
                    f"evidence ledger entry {index} reported single-device applicability "
                    "must clearly label independent reproduction status"
                )
    return errors


def main() -> int:
    errors = check_claim_evidence()
    if errors:
        print("\n".join(errors))
        return 1
    print("Exact-target claim-evidence checks passed; no device was tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
