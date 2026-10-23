"""Safe, local harness for testing a candidate bug hypothesis.

This deliberately does not contain an iOS exploit, payload delivery, privilege
escalation, sandbox escape, or device-modification code. It gives researchers
a reproducible place to record a hypothesis, expected safe observation, actual
observation, and evidence without claiming a vulnerability exists.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_RESULTS = {"not_tested", "not_reproduced", "reproduced_in_lab", "needs_review"}


def validate_record(record: dict) -> list[str]:
    errors = []
    for field in ("id", "hypothesis", "safe_test", "expected_observation", "result"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            errors.append(f"missing required non-empty field: {field}")
    if record.get("result") not in ALLOWED_RESULTS:
        errors.append("result must be one of: " + ", ".join(sorted(ALLOWED_RESULTS)))
    for field in ("source_url", "device", "os_version", "build"):
        if field in record and not isinstance(record[field], str):
            errors.append(f"{field} must be a string when supplied")
    if record.get("result") == "reproduced_in_lab" and not record.get("evidence_note", "").strip():
        errors.append("reproduced_in_lab requires an evidence_note")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init", action="store_true", help="print a blank hypothesis record")
    parser.add_argument("--check", type=Path, help="validate a JSON hypothesis record")
    args = parser.parse_args(argv)
    if args.init:
        print(json.dumps({
            "id": "hypothesis-001",
            "hypothesis": "",
            "safe_test": "Describe a non-destructive, local test in an authorized lab.",
            "expected_observation": "",
            "result": "not_tested",
            "source_url": "",
            "device": "",
            "os_version": "",
            "build": "",
            "evidence_note": "",
            "last_updated_utc": datetime.now(timezone.utc).isoformat()
        }, indent=2))
        return 0
    if args.check:
        try:
            record = json.loads(args.check.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"could not load JSON record: {exc}")
            return 2
        if not isinstance(record, dict):
            print("record must be a JSON object")
            return 2
        errors = validate_record(record)
        if errors:
            print("\n".join(errors))
            return 1
        print("Hypothesis record schema passed; this does not validate exploitability.")
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
