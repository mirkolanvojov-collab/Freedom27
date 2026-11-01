#!/usr/bin/env python3
"""Validate an IPSW BuildManifest against the expected Apple product/build."""
from __future__ import annotations

import argparse
import hashlib
import json
import plistlib
import sys
import zipfile
from pathlib import Path


def sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def verify(
    path: Path,
    product_type: str,
    product_version: str,
    build: str,
    ipsw_path: Path | None = None,
) -> dict:
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

    report = {
        "schema_version": 2,
        "verification": "passed",
        "manifest_file": str(path),
        "manifest_size_bytes": len(raw),
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "expected_identity": {
            "product_type": product_type,
            "product_version": product_version,
            "product_build_version": build,
        },
        "manifest_identity": {
            "product_version": actual_version,
            "product_build_version": actual_build,
            "supported_product_types": products,
            "build_identity_count": len(identities),
            "build_identities": summaries,
        },
        "restore_image": None,
        "limitations": [
            "This validates manifest identity; it does not verify Apple's restore authorization/signature.",
        ],
    }

    if ipsw_path is not None:
        image_digest, image_size = sha256_file(ipsw_path)
        with zipfile.ZipFile(ipsw_path) as archive:
            try:
                embedded = archive.read("BuildManifest.plist")
            except KeyError as exc:
                raise ValueError("restore IPSW has no root BuildManifest.plist member") from exc
        if embedded != raw:
            raise ValueError("embedded IPSW BuildManifest.plist differs byte-for-byte from the separately retrieved manifest")
        report["restore_image"] = {
            "file": str(ipsw_path),
            "sha256": image_digest,
            "size_bytes": image_size,
            "manifest_member": "BuildManifest.plist",
            "archive_manifest_matches": True,
        }
        report["limitations"].append(
            "The full IPSW digest is locally computed; no independent Apple-published SHA-256 or cryptographic restore-signature verification is asserted."
        )
    else:
        report["limitations"].append(
            "No full IPSW was supplied: the report does not bind the manifest to the restore image bytes or the extracted dyld cache."
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--ipsw", type=Path, help="optional complete restore IPSW to hash and bind by its embedded BuildManifest")
    parser.add_argument("--product-type", required=True)
    parser.add_argument("--product-version", required=True)
    parser.add_argument("--build", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = verify(args.manifest, args.product_type, args.product_version, args.build, args.ipsw)
    except (OSError, ValueError, plistlib.InvalidFileException, zipfile.BadZipFile, AttributeError, TypeError) as exc:
        print(f"restore BuildManifest verification failed: {exc}", file=sys.stderr)
        return 2
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
