"""Evidence-first blocker resolution engine for Freedom27.

This engine prioritizes work and validates evidence records. It does not bypass
OS protections, generate exploit payloads, or modify a device.
"""
from __future__ import annotations

from typing import Any
import json
from pathlib import Path

REQUIRED_GATES = (
    "entry",
    "sandbox_escape",
    "kernel_primitive",
    "privilege_escalation",
    "platform_mitigations",
    "persistence_or_bootstrap",
    "package_manager",
    "independent_reproduction",
)

# Order reflects dependency: later stages cannot be considered established
# merely because an earlier stage has evidence.
DEPENDENCIES = {
    "entry": (),
    "sandbox_escape": ("entry",),
    "kernel_primitive": ("sandbox_escape",),
    "privilege_escalation": ("kernel_primitive",),
    "platform_mitigations": ("entry",),
    "persistence_or_bootstrap": ("privilege_escalation", "platform_mitigations"),
    "package_manager": ("persistence_or_bootstrap",),
    "independent_reproduction": ("entry", "sandbox_escape", "kernel_primitive", "privilege_escalation"),
}

SAFE_ACTIONS = {
    "entry": "Review immutable upstream sources for a documented entry point on this exact target.",
    "sandbox_escape": "Check source and published reproduction notes; do not run an unreviewed PoC on the daily-use phone.",
    "kernel_primitive": "Require source-backed exact-build evidence of kernel-level capability; a CVE alone is not proof.",
    "privilege_escalation": "Require documented, reproducible privilege-escalation evidence for this exact target.",
    "platform_mitigations": "Map relevant mitigations to primary sources and record known limitations.",
    "persistence_or_bootstrap": "Review documented bootstrap designs only after prerequisite capabilities are evidenced.",
    "package_manager": "Check package-manager compatibility only after required privilege and bootstrap gates are evidenced.",
    "independent_reproduction": "Keep blocked until an authorized controlled environment reproduces the result on the exact target.",
}


def _target_matches(record: dict[str, Any], target: dict[str, Any]) -> bool:
    keys = ("device_model", "model_identifier", "exact_os_version", "build_number")
    return all(
        isinstance(target.get(key), str)
        and target.get(key)
        and record.get("target", {}).get(key) == target.get(key)
        for key in keys
    )


def validate_evidence_record(record: Any, target: dict[str, Any]) -> list[str]:
    """Return reasons a claim must remain unverified."""
    problems: list[str] = []
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    if not isinstance(target, dict):
        return ["target must be a JSON object"]

    if not _target_matches(record, target):
        problems.append("target does not exactly match device model, identifier, OS version, and build")

    source = record.get("source_url")
    revision = record.get("source_revision")
    status = record.get("status")
    if not isinstance(source, str) or not source.startswith("https://"):
        problems.append("source_url must be an HTTPS URL")
    if not isinstance(revision, str) or len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        problems.append("source_revision must be a full 40-character lowercase Git commit SHA")
    if status not in {"lead", "reviewed", "evidence-recorded", "verified"}:
        problems.append("status must be lead, reviewed, evidence-recorded, or verified")

    if status == "verified":
        if not record.get("evidence_note") or not isinstance(record.get("evidence_note"), str):
            problems.append("verified claims require a non-empty evidence_note")
        if record.get("independent_reproduction") is not True:
            problems.append("verified claims require independent_reproduction=true")
        if record.get("scope_confirmed") is not True:
            problems.append("verified claims require scope_confirmed=true")
    return problems


def build_plan(status_document: dict[str, Any], evidence_records: list[Any] | None = None) -> dict[str, Any]:
    """Create a fail-closed plan for safe research and repository work."""
    if not isinstance(status_document, dict):
        raise ValueError("status document must be an object")
    target = status_document.get("generated_for")
    gates = status_document.get("gates")
    if not isinstance(target, dict) or not isinstance(gates, list):
        raise ValueError("status document must contain generated_for object and gates list")

    by_id = {item.get("id"): item for item in gates if isinstance(item, dict) and isinstance(item.get("id"), str)}
    evidence_results = []
    for record in evidence_records or []:
        errors = validate_evidence_record(record, target)
        evidence_results.append({
            "claim_id": record.get("claim_id", "unnamed") if isinstance(record, dict) else "invalid",
            "accepted_as_verified": not errors and record.get("status") == "verified",
            "validation_errors": errors,
        })
    evidence_verified_ids = {
        result["claim_id"] for result in evidence_results
        if result["accepted_as_verified"]
    }

    tasks = []
    verified_ids: set[str] = set()
    # A "verified" status label is insufficient: require a valid evidence record
    # keyed to the gate, then satisfy prerequisites transitively.
    changed = True
    while changed:
        changed = False
        for gate_id in REQUIRED_GATES:
            item = by_id.get(gate_id, {})
            deps = DEPENDENCIES[gate_id]
            if (
                item.get("status") == "verified"
                and gate_id in evidence_verified_ids
                and all(dep in verified_ids for dep in deps)
                and gate_id not in verified_ids
            ):
                verified_ids.add(gate_id)
                changed = True
    for gate_id in REQUIRED_GATES:
        item = by_id.get(gate_id, {})
        status = item.get("status", "missing")
        deps = list(DEPENDENCIES[gate_id])
        unmet = [dep for dep in deps if dep not in verified_ids]
        # Do not let a "verified" label alone satisfy a gate if its prerequisites are unmet.
        if status != "verified" or gate_id not in verified_ids or unmet:
            tasks.append({
                "gate": gate_id,
                "status": status,
                "priority": "prerequisite" if unmet else ("evidence_review" if status in {"lead", "reviewed", "evidence-recorded"} else "blocked"),
                "unmet_prerequisites": unmet,
                "next_action": SAFE_ACTIONS[gate_id],
            })

    verified_complete = status_document.get("verified_complete_jailbreak") is True and not tasks and len(verified_ids) == len(REQUIRED_GATES)
    return {
        "project": "Freedom27",
        "target": {
            "device_model": target.get("device_model", "unknown"),
            "model_identifier": target.get("model_identifier", "unknown"),
            "exact_os_version": target.get("exact_os_version", "unknown"),
            "build_number": target.get("build_number", "unknown"),
        },
        "assessment": "complete" if verified_complete else "blocked",
        "verified_complete_jailbreak": verified_complete,
        "required_gate_count": len(REQUIRED_GATES),
        "open_task_count": len(tasks),
        "tasks": tasks,
        "evidence_record_results": evidence_results,
        "execution_policy": {
            "mode": "read_only_research",
            "device_modified": False,
            "exploit_execution_authorized": False,
            "never_infer_support_from_version_overlap": True,
        },
        "warning": (
            "This engine prioritizes evidence work; it does not bypass security controls. "
            "Only independently reproduced, exact-target evidence can close a gate."
        ),
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    status_path = root / "research" / "current_exact_target_status.json"
    document = json.loads(status_path.read_text(encoding="utf-8"))
    print(json.dumps(build_plan(document), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
