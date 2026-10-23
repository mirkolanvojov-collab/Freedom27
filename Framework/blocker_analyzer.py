"""Evidence-first blocker analyzer for the Freedom27 exact target.

This tool prioritizes research tasks that can be done safely from an iPhone.
It does not generate exploit code, execute payloads, or modify a device.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

NEXT_ACTIONS = {
    "entry": (
        "Search primary sources for a publicly documented entry point on this exact "
        "device/build; record immutable source revision and explicit scope."
    ),
    "sandbox_escape": (
        "Review source and published reproduction notes for exact-target sandbox escape "
        "evidence; do not execute a proof of concept on the daily-use phone."
    ),
    "kernel_primitive": (
        "Require primary-source evidence of a kernel primitive on the exact build; "
        "a CVE or version overlap alone is insufficient."
    ),
    "privilege_escalation": (
        "Require a documented, reproducible privilege-escalation result for this target; "
        "do not infer it from app-container access."
    ),
    "platform_mitigations": (
        "Document relevant hardware/software mitigations and source-backed limitations "
        "before assessing whether the chain is feasible."
    ),
    "persistence_or_bootstrap": (
        "Review documented bootstrap options and their constraints; do not claim persistence "
        "or root access without independent evidence."
    ),
    "package_manager": (
        "Check upstream compatibility requirements for a package manager only after the "
        "required security capabilities are evidenced."
    ),
    "independent_reproduction": (
        "Keep this gate blocked until an authorized, controlled test environment reproduces "
        "the result on the exact model, OS version, and build."
    ),
}

def analyze(status_document: dict[str, Any]) -> dict[str, Any]:
    """Summarize blockers and propose safe, evidence-oriented next actions."""
    if not isinstance(status_document, dict):
        raise ValueError("status document must be an object")
    target = status_document.get("generated_for", {})
    gates = status_document.get("gates", [])
    if not isinstance(target, dict) or not isinstance(gates, list):
        raise ValueError("status document must contain generated_for object and gates list")

    blockers = []
    seen: set[str] = set()
    for item in gates:
        if not isinstance(item, dict):
            continue
        gate_id = item.get("id")
        if not isinstance(gate_id, str) or not gate_id:
            continue
        seen.add(gate_id)
        status = item.get("status")
        if status != "verified":
            blockers.append({
                "id": gate_id,
                "current_status": status if isinstance(status, str) else "unknown",
                "blocker": item.get("note", "No verified evidence recorded."),
                "next_safe_action": NEXT_ACTIONS.get(
                    gate_id,
                    "Review primary sources, exact-target scope, and reproducibility; keep unverified."
                ),
            })

    for gate_id, action in NEXT_ACTIONS.items():
        if gate_id not in seen:
            blockers.append({
                "id": gate_id,
                "current_status": "missing",
                "blocker": "No status record exists for this required gate.",
                "next_safe_action": action,
            })

    verified = status_document.get("verified_complete_jailbreak") is True
    return {
        "project": "Freedom27",
        "target": {
            "device_model": target.get("device_model", "unknown"),
            "model_identifier": target.get("model_identifier", "unknown"),
            "os_version": target.get("exact_os_version", "unknown"),
            "build": target.get("build_number", "unknown"),
        },
        "assessment": "complete" if verified and not blockers else "blocked",
        "verified_complete_jailbreak": verified,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "safe_to_continue_read_only_research": True,
        "device_modified": False,
        "warning": (
            "This report is an evidence checklist, not an exploit or compatibility test. "
            "It cannot turn an unverified claim into a verified result."
        ),
    }


def main() -> int:
    path = ROOT / "research" / "current_exact_target_status.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(analyze(document), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
