import unittest

from Framework.advisory_inventory import validate


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


class AdvisoryInventoryTests(unittest.TestCase):
    def test_valid_inventory_passes(self):
        self.assertEqual(validate(minimal_inventory()), [])

    def test_rejects_non_apple_url(self):
        data = minimal_inventory()
        data["sources"][0]["url"] = "https://example.com/advisory"
        self.assertTrue(any("HTTPS support.apple.com" in e for e in validate(data)))

    def test_rejects_invalid_cve_format(self):
        data = minimal_inventory()
        data["entries"][0]["cve_id"] = "CVE-26-12"
        self.assertTrue(any("cve_id is invalid" in e for e in validate(data)))

    def test_malformed_cve_list_is_reported_without_crashing(self):
        data = minimal_inventory()
        data["sources"][0]["cve_ids"] = [["not", "hashable"], {"bad": "value"}]
        errors = validate(data)
        self.assertTrue(any("invalid CVE identifier" in error for error in errors))

    def test_rejects_unknown_release(self):
        data = minimal_inventory()
        data["entries"][0]["advisory_release"] = "iOS 99.0"
        self.assertTrue(any("unknown or invalid advisory_release" in e for e in validate(data)))

    def test_malformed_release_does_not_crash(self):
        data = minimal_inventory()
        data["entries"][0]["advisory_release"] = ["not", "hashable"]
        self.assertTrue(any("unknown or invalid advisory_release" in e for e in validate(data)))

    def test_malformed_target_assessment_does_not_crash(self):
        data = minimal_inventory()
        data["entries"][0]["target_assessment"] = {"unexpected": "object"}
        self.assertTrue(any("target_assessment is invalid" in e for e in validate(data)))

    def test_rejects_url_mismatch(self):
        data = minimal_inventory()
        data["entries"][0]["advisory_url"] = "https://support.apple.com/en-us/999999"
        self.assertTrue(any("does not match verified source URL" in e for e in validate(data)))

    def test_empty_source_cve_list_is_allowed_when_partial(self):
        data = minimal_inventory()
        data["sources"][0]["cve_ids"] = []
        data["entries"] = []
        self.assertEqual(validate(data), [])

    def test_complete_source_requires_verified_url(self):
        data = minimal_inventory()
        data["sources"][0]["url"] = None
        data["sources"][0]["extraction_status"] = "complete"
        self.assertTrue(any("cannot be complete without a verified URL" in e for e in validate(data)))


if __name__ == "__main__":
    unittest.main()
