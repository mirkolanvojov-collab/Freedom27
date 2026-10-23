"""Defensive iOS security-control audit planner for Freedom27.

This tool inventories and explains security boundaries. It does not bypass,
disable, exploit, or modify iOS protections or the device.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONTROL_CATALOG = {
    "code_signing": {
        "purpose": "Restricts which executable code can run.",
        "safe_review": "Document platform requirements and public, source-backed limitations; do not attempt signature bypasses.",
    },
    "sandbox": {
        "purpose": "Limits app access to files, services, and other apps.",
        "safe_review": "Use documented APIs and published reports; distinguish app-container access from system compromise.",
    },
    "entitlements": {
        "purpose": "Gate privileged platform capabilities.",
        "safe_review": "Inventory required entitlements and document which are unavailable to ordinary apps.",
    },
    "kernel_memory_protections": {
        "purpose": "Protects kernel memory and privileged execution paths.",
        "safe_review": "Track public mitigation documentation and exact-build evidence; do not run kernel payloads on a daily-use device.",
    },
    "secure_boot_and_boot_chain": {
        "purpose": "Establishes a chain of trust during startup.",
        "safe_review": "Document the hardware/software trust chain and avoid restore or downgrade experiments on the primary phone.",
    },
    "signed_system_volume": {
        "purpose": "Protects the integrity of the operating-system volume.",
        "safe_review": "Record supported customization boundaries and do not claim writable system access without controlled evidence.",
    },
    "code_signing_cache_and_trust": {
        "purpose": "Supports code-signing and trust decisions across the system.",
        "safe_review": "Review official documentation and source-backed research; do not install unknown profiles or certificates.",
    },
    "persistence": {
        "purpose": "Controls whether changes survive restarts and boot.",
        "safe_review": "Treat persistence as a separate, unproven requirement; never infer it from a temporary app-level capability.",
    },
}


def build_audit(target: dict[str, Any], observed: dict[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(target, dict):
        raise ValueError("target must be an object")
    if observed is None:
        observed = {}
    if not isinstance(observed, dict):
        raise ValueError("observed must be an object")

    controls = []
    for name, info in CONTROL_CATALOG.items():
        value = observed.get(name, "not_assessed")
        if not isinstance(value, str) or value not in {"not_assessed", "documented", "reviewed"}:
            value = "invalid_status"
        controls.append({
            "control": name,
            "purpose": info["purpose"],
            "status": value,
            "safe_next_step": info["safe_review"],
        })

    return {
        "project": "Freedom27",
        "target": {
            "device_model": target.get("device_model", "unknown"),
            "model_identifier": target.get("model_identifier", "unknown"),
            "os_version": target.get("exact_os_version", "unknown"),
            "build": target.get("build_number", "unknown"),
        },
        "mode": "read_only_defensive_audit",
        "controls_reviewed": len(controls),
        "controls": controls,
        "device_modified": False,
        "bypass_attempted": False,
        "warning": "This is a documentation and planning report, not a technical test of the device and not a jailbreak.",
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    status_path = root / "research" / "current_exact_target_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    print(json.dumps(build_audit(status["generated_for"]), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
