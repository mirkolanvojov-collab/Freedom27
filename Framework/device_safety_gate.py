"""Fail-closed preflight report for any future device-testing workflow.

This is a metadata gate, not a device safety guarantee. It never executes an
exploit, installs software, modifies an iPhone, or authorizes execution.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
TARGET_FIELDS = ("device_model", "model_identifier", "exact_os_version", "build_number")
SHA40 = re.compile(r"^[0-9a-f]{40}$")

REQUIRED_ATTESTATIONS = (
    ("exact_target_chain_verified", "Complete chain independently verified on the exact device/build"),
    ("backup_verified", "A current backup exists and its completion was checked"),
    ("recovery_path_tested", "A device recovery/restore path is available and understood"),
    ("source_review_complete", "All executable code and dependencies were reviewed from pinned sources"),
    ("non_destructive_test_passed", "A narrowly scoped non-destructive test passed on the exact target"),
    ("crash_recovery_tested", "Recovery from a test-induced crash/reboot was tested"),
)
REQUIRED_CHAIN_GATES = (
    "entry", "sandbox_escape", "kernel_primitive", "privilege_escalation",
    "platform_mitigations", "persistence_or_bootstrap", "package_manager",
    "independent_reproduction",
)


def _verified_attestation(value: Any, target: dict[str, Any]) -> bool:
    """Require an evidence note, pinned source revision, and exact target tuple."""
    if not isinstance(value, dict) or value.get("status") != "verified":
        return False
    url = value.get("evidence_url")
    parsed = urlparse(url) if isinstance(url, str) else None
    note = value.get("evidence_note")
    revision = value.get("source_revision")
    recorded_target = value.get("target")
    return (
        parsed is not None
        and parsed.scheme == "https"
        and bool(parsed.hostname)
        and not parsed.username
        and not parsed.password
        and isinstance(note, str)
        and bool(note.strip())
        and isinstance(revision, str)
        and SHA40.fullmatch(revision) is not None
        and isinstance(recorded_target, dict)
        and all(
            isinstance(target.get(field), str)
            and bool(target[field].strip())
            and recorded_target.get(field) == target[field]
            for field in TARGET_FIELDS
        )
    )


def assess_safety(target_status: dict, attestations: dict | None = None) -> dict:
    """Report blockers; even a clean report never authorizes device execution."""
    if not isinstance(target_status, dict):
        target_status = {}
    attestations = attestations if isinstance(attestations, dict) else {}
    generated_for = target_status.get("generated_for", {})
    target = generated_for if isinstance(generated_for, dict) else {}
    target_complete = all(
        isinstance(target.get(field), str) and bool(target[field].strip())
        for field in TARGET_FIELDS
    )
    gates = [{
        "id": "exact_target_record",
        "description": "Exact device model, OS version, and build are recorded",
        "passed": target_complete,
        "reason": "" if target_complete else "Exact target metadata is incomplete",
    }]
    for gate_id, description in REQUIRED_ATTESTATIONS:
        passed = _verified_attestation(attestations.get(gate_id), target)
        gates.append({
            "id": gate_id,
            "description": description,
            "passed": passed,
            "reason": "" if passed else "No target-matched, source-pinned verified evidence recorded",
        })

    status_gates = target_status.get("gates", [])
    gate_map = {
        item.get("id"): item for item in status_gates
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    } if isinstance(status_gates, list) else {}
    chain_evidence_complete = all(
        gate_map.get(gate_id, {}).get("status") == "verified"
        and _verified_attestation(gate_map.get(gate_id, {}).get("evidence"), target)
        for gate_id in REQUIRED_CHAIN_GATES
    )
    chain_verified = (
        target_status.get("status") == "verified"
        and target_status.get("verified_complete_jailbreak") is True
        and chain_evidence_complete
    )
    gates.append({
        "id": "project_exact_target_chain",
        "description": "Every required chain milestone has target-matched source-pinned evidence",
        "passed": chain_verified,
        "reason": "" if chain_verified else "Exact-target chain and all required milestone evidence are not independently established",
    })
    blockers = [gate["id"] for gate in gates if not gate["passed"]]
    return {
        "mode": "metadata-only fail-closed preflight",
        "target": {field: target.get(field) for field in TARGET_FIELDS},
        "preflight_passed": not blockers,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "gates": gates,
        "device_execution_authorized": False,
        "guarantees_no_crash": False,
        "warning": (
            "This report cannot establish that a jailbreak is safe or crash-free. "
            "It does not execute code or test the physical device. Passing metadata "
            "checks never authorizes exploit execution; a human must independently "
            "review evidence and use a separate, recoverable test device."
        ),
    }


def main() -> int:
    target_path = ROOT / "research" / "current_exact_target_status.json"
    attestations_path = ROOT / "research" / "device_safety_attestations.json"
    try:
        target_status = json.loads(target_path.read_text(encoding="utf-8"))
        attestations = json.loads(attestations_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Safety preflight input error: {exc}")
        return 2
    report = assess_safety(target_status, attestations)
    print(json.dumps(report, indent=2))
    return 0 if report["preflight_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
