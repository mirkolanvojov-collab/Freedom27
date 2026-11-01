#!/usr/bin/env python3
"""Validate an IPSW BuildManifest against the expected Apple product/build."""
from __future__ import annotations
import argparse
import hashlib
import json
import plistlib
import sys
from pathlib import Path


def verify(path: Path, product_type: str, product_version: str, build: str) -> dict:
    raw = path.read_bytes()
    manifest = plistlib.loads(raw)
    if not isinstance(manifest, dict):
        raise ValueError("BuildManifest root is not a dictionary")
    actual_version = str(manifest.get("ProductVersion", ""))
    actual_build = str(manifest.get("ProductBuildVersion", ""))
    products = manifest.get("SupportedProductTypes", [])
    identities = manifest.get("BuildIdentities", [])
    if actual_version != product_version:
        raise ValueError(f"ProductVersion mismatch: expected {product_version}, got {actual_version or '<missing>'}")
    if actual_build != build:
        raise ValueError(f"ProductBuildVersion mismatch: expected {build}, got {actual_build or '<missing>'}")
    if not isinstance(products, list) or product_type not in products:
        raise ValueError(f"SupportedProductTypes does not include {product_type}")
    if not isinstance(identities, list) or not identities:
        raise ValueError("BuildIdentities is missing or empty")
    summaries = []
    for index, identity in enumerate(identities):
        info = identity.get("Info", {}) if isinstance(identity, dict) else {}
        if isinstance(info, dict):
            summaries.append({
                "index": index,
                "device_class": info.get("DeviceClass"),
                "variant": info.get("Variant"),
                "restore_behavior": info.get("RestoreBehavior"),
                "ap_chip_id": identity.get("ApChipID"),
                "ap_board_id": identity.get("ApBoardID"),
            })
    if not summaries or not any(item["device_class"] for item in summaries):
        raise ValueError("BuildIdentities contain no Info.DeviceClass values")
    return {
        "schema_version": 1,
        "verification": "passed",
        "manifest_file": str(path),
        "manifest_size_bytes": len(raw),
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "expected_identity": {"product_type": product_type, "product_version": product_version, "product_build_version": build},
        "manifest_identity": {
            "product_version": actual_version,
            "product_build_version": actual_build,
            "supported_product_types": products,
            "build_identity_count": len(identities),
            "build_identities": summaries,
        },
        "limitations": [
            "This validates the BuildManifest retrieved through exact-device/build IPSW catalog selection; it is not a full-IPSW SHA-256 or Apple signature verification.",
            "The dyld extraction remains a separate request to the resolved Apple CDN URL; this report alone is not cryptographic proof of the complete IPSW bytes.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--product-type", required=True)
    parser.add_argument("--product-version", required=True)
    parser.add_argument("--build", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = verify(args.manifest, args.product_type, args.product_version, args.build)
    except (OSError, ValueError, plistlib.InvalidFileException, AttributeError, TypeError) as exc:
        print(f"restore BuildManifest verification failed: {exc}", file=sys.stderr)
        return 2
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
