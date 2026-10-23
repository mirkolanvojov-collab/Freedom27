"""Read-only readiness checklist for a proposed Freedom27 exploit chain.

This tool does not exploit the device or execute payloads. It reports which
evidence gates are missing before any implementation could be responsibly
claimed compatible with the exact target.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_GATES = (
    ("entry", "Publicly documented entry vulnerability for the exact device/build"),
    ("sandbox_escape", "Reproducible sandbox escape on the exact device/build"),
    ("kernel_primitive", "Documented and reproducible kernel-level primitive"),
    ("privilege_escalation", "Evidence of required privilege escalation on the exact build"),
    ("platform_mitigations", "Documented handling of relevant platform mitigations"),
    ("persistence_or_bootstrap", "Defined bootstrap/persistence approach and limitations"),
    ("package_manager", "Verified package-manager/bootstrap compatibility"),
    ("independent_reproduction", "Independent reproduction on the exact device/build"),
)

def assess(target: dict, evidence: dict) -> dict:
    """Return a fail-closed report; only literal True satisfies a gate."""
    device = target.get("device_model", "")
    os_version = target.get("exact_os_version", "")
    build = target.get("build_number", "")
    target_key = {"device_model": device, "exact_os_version": os_version, "build_number": build}
    records = evidence.get("target_evidence", {})
    exact_record = records.get(f"{device}|{os_version}|{build}", {}) if isinstance(records, dict) else {}
    gates = []
    for gate_id, description in REQUIRED_GATES:
        passed = exact_record.get(gate_id) is True
        gates.append({
            "id": gate_id,
            "description": description,
            "status": "evidence-recorded" if passed else "missing",
        })
    missing = [g["id"] for g in gates if g["status"] == "missing"]
    return {
        "target": target_key,
        "mode": "read-only evidence assessment",
        "gates": gates,
        "ready_for_implementation_claim": not missing,
        "missing_gate_count": len(missing),
        "missing_gates": missing,
        "warning": (
            "A recorded checkbox is not proof by itself. Every gate requires reviewable "
            "public evidence and reproducibility. This tool does not test hardware, discover "
            "vulnerabilities, execute exploits, or establish jailbreak compatibility."
        ),
    }

def main() -> int:
    target_path = ROOT / "research" / "target_profile.json"
    evidence_path = ROOT / "research" / "chain_evidence.json"
    target = json.loads(target_path.read_text(encoding="utf-8"))
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    report = assess(target, evidence)
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
