"""Freedom27 unified read-only security research engine.

Aggregates existing evidence and advisory metadata into a prioritized report.
It performs no network requests, exploit execution, payload generation, or
device access. It cannot prove a vulnerability applies to a target build.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ADVISORY = ROOT / "research" / "ios_26_7_advisory_candidates_2026-10-23.json"
DEFAULT_OUTPUT = ROOT / "research" / "unified_research_report.json"


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def analyze_advisories(document: dict) -> dict:
    target = document.get("target", {})
    candidates = document.get("candidates", [])
    excluded = document.get("excluded_candidates", [])
    errors = []
    if not isinstance(target, dict) or not all(target.get(k) for k in ("model_identifier", "os_version", "build")):
        errors.append("target identity is incomplete")
    if not isinstance(candidates, list):
        errors.append("candidates must be a list")
        candidates = []
    if not isinstance(excluded, list):
        errors.append("excluded_candidates must be a list")
        excluded = []

    source_metadata = document.get("source", {})
    if not isinstance(source_metadata, dict):
        errors.append("source metadata must be an object")
        source_metadata = {}

    seen_ids: set[str] = set()
    scored = []
    for item in candidates:
        if not isinstance(item, dict):
            errors.append("candidate entry must be an object")
            continue
        raw_candidate_id = item.get("id", "<unknown>")
        candidate_id = raw_candidate_id if isinstance(raw_candidate_id, str) and raw_candidate_id.strip() else "<unknown>"
        if candidate_id == "<unknown>":
            errors.append("candidate entry has a missing or invalid ID")
        elif candidate_id in seen_ids:
            errors.append(f"{candidate_id}: duplicate candidate ID")
        seen_ids.add(candidate_id)
        url = item.get("source_url") or source_metadata.get("url", "")
        try:
            parsed = urlparse(url) if isinstance(url, str) else None
            valid_url = (
                parsed is not None and parsed.scheme == "https"
                and bool(parsed.hostname) and not parsed.username and not parsed.password
            )
        except ValueError:
            valid_url = False
        if not valid_url:
            errors.append(f"{candidate_id}: source URL is not a valid HTTPS URL")
        status = item.get("target_applicability", "not_established")
        repro = item.get("reproduction_status", "not_reproduced_by_Freedom27")
        # Scores rank review work only; they are not exploitability estimates.
        score = {"high": 30, "medium": 20, "low": 10}.get(item.get("priority"), 0)
        if status != "not_established":
            score += 0
        if repro != "not_reproduced_by_Freedom27":
            errors.append(f"{item.get('id', '<unknown>')}: advisory record overstates reproduction status")
        scored.append({
            "id": item.get("id", "unknown"),
            "component": item.get("component", "unknown"),
            "review_priority_score": score,
            "published_impact": item.get("published_impact", ""),
            "target_applicability": "not_established",
            "reproduction_status": "not_reproduced_by_Freedom27",
            "next_action": "Verify exact affected/fixed versions against primary sources; do not infer target exposure from the patched release alone."
        })
    scored.sort(key=lambda x: (-x["review_priority_score"], x["id"]))
    return {
        "candidate_count": len(scored),
        "excluded_candidate_count": len(excluded),
        "candidates_ranked_for_review": scored,
        "excluded_candidates": [
            {"id": x.get("id", "unknown"), "status": x.get("status", "unclassified"),
             "fixed_release": x.get("fixed_release", "unknown")}
            for x in excluded if isinstance(x, dict)
        ],
        "validation_errors": errors
    }


def build_report(document: dict) -> dict:
    advisory = analyze_advisories(document)
    target = document.get("target", {})
    tasks = [
        {"id": "R1", "priority": "P0", "task": "Verify each candidate against the exact iOS 26.6.1 advisory and fixed-release record", "done": False},
        {"id": "R2", "priority": "P0", "task": "Record primary-source URLs, source revision/date, and exact quoted impact for every retained lead", "done": False},
        {"id": "R3", "priority": "P1", "task": "Separate impact, affected-version scope, exploit primitive, and complete-chain evidence", "done": False},
        {"id": "R4", "priority": "P1", "task": "Review public mitigation documentation and identify evidence gaps without running exploits on the daily-use phone", "done": False},
        {"id": "R5", "priority": "P2", "task": "Build bootstrap/package manager only after prerequisite capabilities have independent evidence", "done": False},
        {"id": "R6", "priority": "P2", "task": "Add authorized controlled-lab reproduction and recovery criteria before any on-device validation", "done": False}
    ]
    return {
        "tool": "Freedom27 Unified Research Engine",
        "schema_version": 1,
        "mode": "read_only_advisory_and_evidence_triage",
        "target": target,
        "assessment": "blocked",
        "summary": {
            "advisory_candidates": advisory["candidate_count"],
            "excluded_candidates": advisory["excluded_candidate_count"],
            "verified_exact_target_vulnerabilities": 0,
            "verified_complete_jailbreak": False,
            "device_accessed": False,
            "device_modified": False,
            "exploit_executed": False
        },
        "advisory_analysis": advisory,
        "prioritized_tasks": tasks,
        "limitations": [
            "A published CVE impact does not establish vulnerability on this exact build.",
            "A fixed release does not, by itself, establish whether earlier builds were affected; consult each advisory's version scope.",
            "Review priority scores organize research work only; they are not exploitability probabilities.",
            "This engine is read-only and does not fetch or independently authenticate live remote sources."
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_ADVISORY)
    parser.add_argument("--output", type=Path, default=None, help="write JSON report here; default prints to stdout")
    args = parser.parse_args()
    try:
        report = build_report(load_json(args.input))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"assessment": "invalid_input", "error": str(exc)}, indent=2))
        return 2
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if report["advisory_analysis"]["validation_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
