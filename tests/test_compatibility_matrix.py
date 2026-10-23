import unittest

from Framework.compatibility_matrix import (
    CompatibilityClaim,
    build_target_matrix,
    validate_claims,
)


class CompatibilityMatrixTests(unittest.TestCase):
    def test_target_matrix_contains_all_requested_families_and_os_families(self):
        rows = build_target_matrix()
        self.assertEqual(len(rows), 10)
        self.assertEqual({row["device_family"] for row in rows}, {
            "iPhone 14", "iPhone 15", "iPhone 16", "iPhone 17", "iPhone 18"
        })
        self.assertEqual({row["os_family"] for row in rows}, {"iOS 26", "iOS 27"})
        self.assertTrue(all(row["status"] == "not-investigated" for row in rows))

    def test_verified_claim_requires_https_evidence_and_notes(self):
        claim = CompatibilityClaim(
            device_family="iPhone 18 Pro",
            model_identifier="example-model",
            os_version="iOS 27.0.1",
            build="24A446",
            status="verified",
        )
        errors = claim.validate()
        self.assertTrue(any("HTTPS evidence_url" in error for error in errors))
        self.assertTrue(any("review notes" in error for error in errors))

    def test_valid_research_claim_can_be_unverified_without_evidence(self):
        claim = CompatibilityClaim(
            device_family="iPhone 14",
            model_identifier="example-model",
            os_version="iOS 26",
            build="unknown-build",
            status="researching",
        )
        self.assertEqual(claim.validate(), [])

    def test_unknown_status_is_rejected(self):
        claim = CompatibilityClaim(
            device_family="iPhone 14",
            model_identifier="example-model",
            os_version="iOS 26",
            build="example-build",
            status="works",
        )
        self.assertTrue(any("status must be one of" in error for error in claim.validate()))

    def test_duplicate_claims_are_rejected(self):
        item = {
            "device_family": "iPhone 14",
            "model_identifier": "example-model",
            "os_version": "iOS 26",
            "build": "example-build",
            "status": "researching",
        }
        errors = validate_claims([item, item])
        self.assertTrue(any("duplicate" in error for error in errors))

    def test_non_object_claim_is_reported_without_crashing(self):
        errors = validate_claims([None, {"device_family": "iPhone 14"}])
        self.assertTrue(any("claim[0]: must be an object" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
