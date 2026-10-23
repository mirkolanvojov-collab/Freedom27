import unittest

from Framework.research_manifest import validate_manifest, target_key


TARGET = {
    "device_model": "iPhone 16 Plus",
    "model_identifier": "iPhone17,4",
    "os_version": "iOS 26.6.1",
    "build": "23G83",
}
VALID = {
    "id": "lead-001",
    "title": "Public research lead",
    "source_url": "https://github.com/example/project/commit/",
    "source_revision": "0123456789abcdef0123456789abcdef01234567",
    "claim": "Research lead only; applicability to the target is unproven.",
    "status": "queued",
    "target": TARGET,
    "evidence_note": "",
    "independent_reproduction": False,
}


class ResearchManifestTests(unittest.TestCase):
    def test_complete_unverified_lead_passes(self):
        self.assertEqual(validate_manifest([VALID]), [])

    def test_missing_exact_target_fields_are_rejected(self):
        item = {**VALID, "target": {"device_model": "iPhone 16 Plus"}}
        errors = validate_manifest([item])
        self.assertTrue(any("target.model_identifier" in e for e in errors))
        self.assertTrue(any("target.os_version" in e for e in errors))
        self.assertTrue(any("target.build" in e for e in errors))

    def test_mutable_or_short_revision_is_rejected(self):
        item = {**VALID, "source_revision": "main"}
        self.assertTrue(any("full 40-character commit SHA" in e for e in validate_manifest([item])))

    def test_non_https_source_is_rejected(self):
        item = {**VALID, "source_url": "http://example.org"}
        self.assertTrue(any("must use HTTPS" in e for e in validate_manifest([item])))

    def test_reproduction_claim_requires_evidence_and_independent_replication(self):
        item = {**VALID, "status": "reproduced_in_lab"}
        errors = validate_manifest([item])
        self.assertTrue(any("requires an evidence_note" in e for e in errors))
        self.assertTrue(any("independent_reproduction=true" in e for e in errors))

    def test_duplicate_ids_are_rejected(self):
        errors = validate_manifest([VALID, VALID])
        self.assertTrue(any("duplicate id" in e for e in errors))

    def test_unknown_status_is_rejected(self):
        item = {**VALID, "status": "works"}
        self.assertTrue(any("status must be one of" in e for e in validate_manifest([item])))

    def test_target_key_is_exact_and_ordered(self):
        self.assertEqual(target_key(TARGET), "iPhone 16 Plus|iPhone17,4|iOS 26.6.1|23G83")


if __name__ == "__main__":
    unittest.main()
