import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path("Framework/advisory_inventory.py")
spec = importlib.util.spec_from_file_location("advisory_inventory", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def minimal_inventory():
    return {
        "schema_version": 1,
        "sources": [{
            "release": "iOS 26.6.1",
            "url": "https://support.apple.com/en-us/148282",
            "extraction_status": "partial",
            "cve_ids": ["CVE-2026-12345"],
            "notes": "Partial extraction."
        }],
        "entries": [{
            "cve_id": "CVE-2026-12345",
            "advisory_release": "iOS 26.6.1",
            "advisory_url": "https://support.apple.com/en-us/148282",
            "evidence_status": "public_advisory_only",
            "target_assessment": "not_assessed"
        }]
    }


def test_valid_inventory_passes():
    assert module.validate(minimal_inventory()) == []


def test_rejects_non_apple_url():
    data = minimal_inventory()
    data["sources"][0]["url"] = "https://example.com/advisory"
    assert any("HTTPS support.apple.com" in e for e in module.validate(data))


def test_rejects_invalid_cve_format():
    data = minimal_inventory()
    data["entries"][0]["cve_id"] = "CVE-26-12"
    assert any("cve_id is invalid" in e for e in module.validate(data))


def test_malformed_cve_list_is_reported_without_crashing():
    data = minimal_inventory()
    data["sources"][0]["cve_ids"] = [["not", "hashable"], {"bad": "value"}]
    errors = module.validate(data)
    assert any("invalid CVE identifier" in error for error in errors)


def test_rejects_unknown_release():
    data = minimal_inventory()
    data["entries"][0]["advisory_release"] = "iOS 99.0"
    assert any("unknown advisory_release" in e for e in module.validate(data))


def test_rejects_url_mismatch():
    data = minimal_inventory()
    data["entries"][0]["advisory_url"] = "https://support.apple.com/en-us/999999"
    assert any("does not match verified source URL" in e for e in module.validate(data))


def test_empty_source_cve_list_is_allowed_when_partial():
    data = minimal_inventory()
    data["sources"][0]["cve_ids"] = []
    data["entries"] = []
    assert module.validate(data) == []


def test_complete_source_requires_verified_url():
    data = minimal_inventory()
    data["sources"][0]["url"] = None
    data["sources"][0]["extraction_status"] = "complete"
    assert any("cannot be complete without a verified URL" in e for e in module.validate(data))
