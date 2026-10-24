#!/usr/bin/env python3
"""Compare verified IPSW BuildManifest inventories without overclaiming binary diffs."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

FIELDS = ("path", "digest_hex", "partial_digest_hex", "is_encrypted", "trusted", "personalized")


def load_inventory(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("integrity_verified_against_pinned_values") is not True:
        raise ValueError(f"{path}: inventory is not hash-verified")
    if not data.get("product_type"):
        raise ValueError(f"{path}: missing product_type")
    if not isinstance(data.get("source_sha256"), str) or len(data["source_sha256"]) != 64:
        raise ValueError(f"{path}: missing or invalid source SHA-256")
    if not isinstance(data.get("source_size_bytes"), int) or data["source_size_bytes"] <= 0:
        raise ValueError(f"{path}: missing or invalid source size")
    identities = data.get("build_identities")
    if not isinstance(identities, list) or not identities:
        raise ValueError(f"{path}: missing build identities")
    return data


def _components(inventory: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    found: dict[tuple[str, str], dict[str, Any]] = {}
    for identity in inventory["build_identities"]:
        variant = identity.get("variant") or "<unspecified-variant>"
        for component in identity.get("components", []):
            name = component.get("name")
            if isinstance(name, str):
                record = dict(component)
                record["variant"] = variant
                found[(variant, name)] = record
    return found


def _build_metadata(inventory: dict[str, Any]) -> dict[str, Any]:
    identities = inventory["build_identities"]
    return {
        "source_file_name": inventory.get("source_file_name"),
        "build_versions": sorted({str(item.get("build_version")) for item in identities if item.get("build_version")}),
        "build_trains": sorted({str(item.get("build_train")) for item in identities if item.get("build_train")}),
        "device_class": inventory.get("device_class"),
        "sha256": inventory.get("source_sha256"),
        "size_bytes": inventory.get("source_size_bytes"),
    }


def compare_inventories(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    for label, inventory in (("before", before), ("after", after)):
        if inventory.get("integrity_verified_against_pinned_values") is not True:
            raise ValueError(f"{label} inventory is not hash-verified")
    if before.get("product_type") != after.get("product_type"):
        raise ValueError("product_type mismatch: cross-device comparison is not allowed")
    if before.get("device_class") != after.get("device_class"):
        raise ValueError("device_class mismatch: cross-board comparison is not allowed")

    left = _components(before)
    right = _components(after)
    shared = left.keys() & right.keys()
    changes = []
    field_counts: Counter[str] = Counter()
    for variant, name in sorted(left.keys() | right.keys()):
        key = (variant, name)
        old = left.get(key)
        new = right.get(key)
        if old is None:
            changes.append({"variant": variant, "name": name, "status": "added_in_after", "before": None, "after": new})
            continue
        if new is None:
            changes.append({"variant": variant, "name": name, "status": "absent_in_after", "before": old, "after": None})
            continue
        changed_fields = [field for field in FIELDS if old.get(field) != new.get(field)]
        if changed_fields:
            field_counts.update(changed_fields)
            changes.append({
                "variant": variant,
                "name": name,
                "status": "metadata_changed",
                "changed_fields": changed_fields,
                "before": old,
                "after": new,
            })

    status_counts = Counter(item["status"] for item in changes)
    return {
        "schema_version": 2,
        "product_type": before["product_type"],
        "before_build": _build_metadata(before),
        "after_build": _build_metadata(after),
        "component_entries_before": len(left),
        "component_entries_after": len(right),
        "shared_entry_count": len(shared),
        "metadata_changed_entry_count": status_counts["metadata_changed"],
        "added_entry_count": status_counts["added_in_after"],
        "absent_entry_count": status_counts["absent_in_after"],
        "change_record_count": len(changes),
        "field_change_counts": dict(sorted(field_counts.items())),
        "changes": changes,
        "interpretation": {
            "component_payload_bytes_compared": False,
            "cve_attribution_performed": False,
            "exact_build_vulnerability_confirmed": False,
            "note": "Manifest metadata differences are triage leads only; they do not establish payload differences, patch attribution, vulnerable-code reachability, or exploitability.",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", help="hash-verified inventory JSON for older build")
    parser.add_argument("after", help="hash-verified inventory JSON for comparison build")
    parser.add_argument("--output", help="optional output JSON path")
    args = parser.parse_args(argv)
    try:
        result = compare_inventories(load_inventory(args.before), load_inventory(args.after))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"verified": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
