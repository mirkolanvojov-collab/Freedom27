"""Fail-closed preflight report for any future device-testing workflow.

This is a metadata gate, not a device safety guarantee. It never executes an
exploit, installs software, modifies an iPhone, or authorizes execution.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ATTESTATIONS = (
    ("exact_target_chain_verified", "Complete chain independently verified on the exact device/build"),
    ("backup_verified", "A current backup exists and its completion was checked"),
    ("recovery_path_tested", "A device recovery/restore path is available and understood"),
    ("source_review_complete", "All executable code and dependencies were reviewed from pinned sources"),
    ("non_destructive_test_passed", "A narrowly scoped non-destructive test passed on the exact target"),
    ("crash_recovery_tested", "Recovery from a test-induced crash/reboot was tested"),
)


def _verified_attestation(value: Any) -> bool:
    """Require a reviewable HTTPS evidence URL and note, not a bare boolean."""
    if not isinstance(value, dict) or value.get("status") != "verified":
        return False
    url = value.get("evidence_url")
    note = value.get("evidence_note")
    return (
        isinstance(url, str)
        and url.startswith("https://")
        and len(url) > len("https://")
        and isinstance(note, str)
        and bool(note.strip())
    )


def assess_safety(target_status: dict, attestations: dict | None = None) -> dict:
    """Report blockers; passing this metadata check is never a no-crash guarantee."""
    attestations = attestations if isinstance(attestations, dict) else {}
    target = target_status.get("generated_for", {})
    target_fields = ("device_model", "model_identifier", "exact_os_version", "build_number")
    target_complete = all(
        isinstance(target.get(field), str) and bool(target.get(field).strip())
        for field in target_fields
    )
    gates = [{
        "id": "exact_target_record",
        "description": "Exact device model, OS version, and build are recorded",
        "passed": target_complete,
        "reason": "" if target_complete else "Exact target metadata is incomplete",
    }]
    for gate_id, description in REQUIRED_ATTESTATIONS:
        passed = _verified_attestation(attestations.get(gate_id))
        gates.append({
            "id": gate_id,
            "description": description,
            "passed": passed,
            "reason": "" if passed else "No reviewable verified evidence recorded",
        })

    chain_verified = (
        target_status.get("status") == "verified"
        and target_status.get("verified_complete_jailbreak") is True
    )
    gates.append({
        "id": "project_exact_target_chain",
        "description": "Project records a complete jailbreak independently verified on this exact target",
        "passed": chain_verified,
        "reason": "" if chain_verified else "Project status is not an independently verified exact-target jailbreak",
    })
    blockers = [gate["id"] for gate in gates if not gate["passed"]]
    return {
        "mode": "metadata-only fail-closed preflight",
        "target": {field: target.get(field) for field in target_fields},
        "preflight_passed": not blockers,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "gates": gates,
        "device_execution_authorized": False,
        "guarantees_no_crash": False,
        "warning": (
            "This report cannot establish that a jailbreak is safe or crash-free. "
            "It does not execute code or test the physical device. Never run an "
            "unverified chain on a daily-use phone; passing metadata checks alone "
            "must not authorize device execution."
        ),
    }


def main() -> int:
    target_path = ROOT / "research" / "current_exact_target_status.json"
    attestations_path = ROOT / "research" / "device_safety_attestations.json"
    target_status = json.loads(target_path.read_text(encoding="utf-8"))
    if attestations_path.exists():
        attestations = json.loads(attestations_path.read_text(encoding="utf-8"))
    else:
        attestations = {}
    report = assess_safety(target_status, attestations)
    print(json.dumps(report, indent=2))
    return 0 if report["preflight_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
