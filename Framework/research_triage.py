"""Read-only triage of Freedom27 public research metadata."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    with Path(path).open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def triage(target, registry_doc, ledger_doc):
    registry = {x["id"]: x for x in registry_doc.get("entries", []) if isinstance(x, dict) and x.get("id")}
    ledger = {x["id"]: x for x in ledger_doc.get("entries", []) if isinstance(x, dict) and x.get("id")}
    target_triplet = " ".join(str(target.get(k, "")).strip().lower()
                              for k in ("device_model", "exact_os_version", "build_number"))
    rows = []
    for key in dict.fromkeys([*registry, *ledger]):
        reg, ev = registry.get(key, {}), ledger.get(key, {})
        exact = " ".join(str(ev.get("exact_target_build", "")).strip().lower().split())
        if exact and exact == target_triplet:
            category = "exact-target-mentioned"
            reason = "Ledger records the exact target triplet; primary-source verification is still required."
            action = "Verify the source and seek independent reproduction for this exact target."
        elif reg.get("status") == "verified" and ev.get("reproduction_status") != "reproduced_by_Freedom27":
            category = "verified-claim-evidence-gap"
            reason = "Registry says verified, but the ledger does not record Freedom27 reproduction for the exact target; do not treat this as target compatibility."
            action = "Downgrade the claim to unverified until exact-target evidence and independent reproduction are recorded."
        elif ev.get("target_applicability") == "older_hardware_only":
            category = "hardware-mismatch"
            reason = "The recorded upstream scope is older hardware; it does not establish support for this target."
            action = "Recheck only if upstream documents support for this hardware."
        elif ev.get("target_applicability") == "reported_single_device_build":
            category = "different-device-demo"
            reason = "A report about another device/build is not evidence of target compatibility."
            action = "Wait for primary technical disclosure and exact-target reproduction."
        elif ev.get("patch_state") in ("historical_patched", "patched_for_reported_scope"):
            category = "historical-or-patched"
            reason = "The lead is historical or marked patched for its reported scope; target applicability is unproven."
            action = "Check advisory patch scope for this exact build; do not infer a jailbreak from a CVE."
        else:
            category = "not-established"
            reason = "The available metadata does not establish compatibility with the exact target."
            action = "Find a primary source naming the exact device, OS version and build."
        if key not in registry:
            reason = "Missing registry counterpart. " + reason
        if key not in ledger:
            reason = "Missing evidence-ledger counterpart. " + reason
        rows.append({
            "id": key, "title": reg.get("title", key), "category": category,
            "registry_status": reg.get("status", "missing"),
            "patch_state": ev.get("patch_state", "missing"),
            "target_applicability": ev.get("target_applicability", "missing"),
            "reproduction_status": ev.get("reproduction_status", "missing"),
            "exact_target_build": ev.get("exact_target_build", ""),
            "source_url": ev.get("evidence_url") or reg.get("source_url", ""),
            "reason": reason, "next_action": ev.get("next_action") or action,
            "reproduced_by_freedom27": ev.get("reproduction_status") == "reproduced_by_Freedom27"
        })
    counts = {}
    for row in rows:
        counts[row["category"]] = counts.get(row["category"], 0) + 1
    return {
        "target": {k: target.get(k, "") for k in
                   ("device_model", "model_identifier", "exact_os_version", "build_number")},
        "summary": {
            "registry_entries": len(registry), "ledger_entries": len(ledger),
            "joined_entries": len(set(registry) & set(ledger)),
            "unmatched_registry_entries": len(set(registry) - set(ledger)),
            "unmatched_ledger_entries": len(set(ledger) - set(registry)),
            "exact_target_mentions": counts.get("exact-target-mentioned", 0),
            "reproduced_by_freedom27": sum(row["reproduced_by_freedom27"] for row in rows),
            "categories": counts
        },
        "results": rows,
        "warning": "Metadata triage only; it does not establish exploitability or device-tested compatibility."
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=ROOT / "research/target_profile.json")
    parser.add_argument("--registry", type=Path, default=ROOT / "research/vulnerability_registry.json")
    parser.add_argument("--ledger", type=Path, default=ROOT / "research/evidence_ledger.json")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)
    report = triage(load(args.target), load(args.registry), load(args.ledger))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Freedom27 research triage")
        print("Target: " + " / ".join(str(report["target"][k]) for k in
              ("device_model", "exact_os_version", "build_number")))
        print(report["warning"])
        for row in report["results"]:
            print(f"\n[{row['category']}] {row['id']} — {row['title']}")
            print(f"  Patch: {row['patch_state']} | Reproduction: {row['reproduction_status']}")
            print("  " + row["reason"])
            print("  Next: " + row["next_action"])
            print("  Source: " + row["source_url"])
        print("\nSummary: " + json.dumps(report["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
