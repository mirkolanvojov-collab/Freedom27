#!/usr/bin/env python3
"""Create a read-only, hash-gated inventory of an IPSW BuildManifest.plist.

This reads only the ZIP central directory and BuildManifest.plist. It does not
extract firmware components, decrypt files, contact a device, or execute code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import plistlib
import sys
import zipfile
from pathlib import Path
from typing import Any


def _hex(value: Any) -> str | None:
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, str):
        return value.lower()
    return None


def inventory_ipsw(path: str | Path, expected_sha256: str, expected_size: int,
                   product_type: str, device_class: str, hash_components: list[str] | None = None) -> dict[str, Any]:
    """Verify full IPSW bytes, then inventory matching BuildManifest identities."""
    image = Path(path)
    if not isinstance(expected_sha256, str):
        raise ValueError("expected_sha256 must be a string of 64 hexadecimal characters")
    expected_sha256 = expected_sha256.strip().lower()
    if len(expected_sha256) != 64 or any(c not in "0123456789abcdef" for c in expected_sha256):
        raise ValueError("expected_sha256 must be 64 hexadecimal characters")
    if type(expected_size) is not int or expected_size <= 0:
        raise ValueError("expected_size must be a positive integer")
    if not isinstance(product_type, str) or not product_type.strip():
        raise ValueError("product_type is required")
    if not isinstance(device_class, str) or not device_class.strip():
        raise ValueError("device_class is required")
    if hash_components is not None and (
        not isinstance(hash_components, list)
        or any(not isinstance(name, str) or not name.strip() for name in hash_components)
    ):
        raise ValueError("hash_components must be a list of non-empty strings")
    if not image.is_file():
        raise FileNotFoundError(str(image))

    digest = hashlib.sha256()
    size = 0
    with image.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
    actual_sha256 = digest.hexdigest()
    if actual_sha256 != expected_sha256:
        raise ValueError(f"SHA-256 mismatch: expected {expected_sha256}, got {actual_sha256}")
    if size != expected_size:
        raise ValueError(f"size mismatch: expected {expected_size}, got {size}")

    with zipfile.ZipFile(image, "r") as archive:
        try:
            info = archive.getinfo("BuildManifest.plist")
        except KeyError as exc:
            raise ValueError("IPSW has no root BuildManifest.plist") from exc
        if info.file_size > 64 * 1024 * 1024:
            raise ValueError("BuildManifest.plist exceeds 64 MiB safety limit")
        manifest = plistlib.loads(archive.read(info))

    if not isinstance(manifest, dict):
        raise ValueError("BuildManifest.plist root must be a dictionary")
    supported_products = manifest.get("SupportedProductTypes", [])
    if not isinstance(supported_products, list) or any(not isinstance(item, str) for item in supported_products):
        raise ValueError("BuildManifest.plist SupportedProductTypes must be a list of strings")
    if product_type not in supported_products:
        raise ValueError(f"product type {product_type!r} is not listed in SupportedProductTypes")

    identities = manifest.get("BuildIdentities")
    if not isinstance(identities, list):
        raise ValueError("BuildManifest.plist has no BuildIdentities array")

    selected = []
    wanted_hashes = set(hash_components or [])
    member_hash_cache: dict[str, dict[str, Any]] = {}
    for index, identity in enumerate(identities):
        if not isinstance(identity, dict):
            continue
        identity_info = identity.get("Info", {})
        if not isinstance(identity_info, dict):
            continue
        identity_device_class = identity_info.get("DeviceClass")
        if not isinstance(identity_device_class, str) or identity_device_class.lower() != device_class.lower():
            continue
        components = []
        component_map = identity.get("Manifest", {})
        if not isinstance(component_map, dict):
            continue
        for name, component in sorted(component_map.items()):
            if not isinstance(component, dict):
                continue
            component_info = component.get("Info", {})
            if not isinstance(component_info, dict):
                component_info = {}
            component_path = component.get("Path", component_info.get("Path"))
            component_result = {
                "name": str(name),
                "path": component_path,
                "digest_hex": _hex(component.get("Digest", component_info.get("Digest"))),
                "partial_digest_hex": _hex(component.get("PartialDigest", component_info.get("PartialDigest"))),
                "is_encrypted": component.get("IsEncrypted", component_info.get("IsEncrypted")),
                "trusted": component.get("Trusted", component_info.get("Trusted")),
                "personalized": component.get("Personalized", component_info.get("Personalized")),
            }
            if str(name) in wanted_hashes:
                if not isinstance(component_path, str) or not component_path:
                    raise ValueError(f"selected component {name!r} has no manifest path")
                if component_path not in member_hash_cache:
                    member_digest = hashlib.sha256()
                    member_size = 0
                    try:
                        with zipfile.ZipFile(image, "r") as member_archive:
                            member_info = member_archive.getinfo(component_path)
                            with member_archive.open(member_info, "r") as member_stream:
                                while True:
                                    chunk = member_stream.read(1024 * 1024)
                                    if not chunk:
                                        break
                                    member_digest.update(chunk)
                                    member_size += len(chunk)
                    except KeyError as exc:
                        raise ValueError(f"selected component path missing from IPSW: {component_path}") from exc
                    member_hash_cache[component_path] = {
                        "member_sha256": member_digest.hexdigest(),
                        "member_size_bytes": member_size,
                        "member_hash_algorithm": "sha256",
                    }
                component_result.update(member_hash_cache[component_path])
            components.append(component_result)
        selected.append({
            "identity_index": index,
            "device_class": identity_info.get("DeviceClass"),
            "product_type": product_type,
            "variant": identity_info.get("Variant"),
            "build_train": identity_info.get("BuildTrain") or manifest.get("BuildTrain"),
            "build_version": identity_info.get("BuildVersion") or identity_info.get("BuildNumber"),
            "restore_behavior": identity_info.get("RestoreBehavior"),
            "components": components,
        })

    if not selected:
        raise ValueError(f"no BuildIdentity matched device class {device_class!r}")

    return {
        "schema_version": 1,
        "source_file_name": image.name,
        "source_sha256": actual_sha256,
        "source_size_bytes": size,
        "integrity_verified_against_pinned_values": True,
        "product_type": product_type,
        "device_class": device_class,
        "build_manifest_entry": "BuildManifest.plist",
        "build_identities": selected,
        "method_limits": [
            "Only BuildManifest.plist metadata was read; no firmware component was extracted or decrypted.",
            "Requested component member hashes, when enabled, are SHA-256 hashes of the exact uncompressed ZIP member bytes; they are not decrypted code hashes.",
            "Manifest component digests are recorded as metadata and are not independent verification of component bytes.",
            "A matching IPSW hash proves consistency with the pinned digest, not Apple-signed authenticity by itself.",
            "Component names or digest changes do not attribute a CVE or prove exploitability.",
        ],
        "device_modified": False,
        "exploit_executed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ipsw", help="path to a locally available IPSW")
    parser.add_argument("--sha256", required=True, help="pinned whole-file SHA-256")
    parser.add_argument("--size", required=True, type=int, help="pinned whole-file byte count")
    parser.add_argument("--product-type", required=True, help="e.g. iPhone17,4; checked against SupportedProductTypes")
    parser.add_argument("--device-class", required=True, help="board config from authoritative device metadata, e.g. D48AP")
    parser.add_argument("--hash-component", action="append", default=[], help="also SHA-256 hash this exact IPSW member by manifest component name; repeatable")
    parser.add_argument("--output", help="optional JSON output path; stdout if omitted")
    args = parser.parse_args(argv)
    try:
        result = inventory_ipsw(args.ipsw, args.sha256, args.size, args.product_type, args.device_class, args.hash_component)
    except (OSError, ValueError, zipfile.BadZipFile, plistlib.InvalidFileException) as exc:
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
