import unittest

from Framework.compatibility import (
    CompatibilityClaim,
    TargetProfile,
    claim_is_usable,
    validate_profile,
)


class CompatibilityTests(unittest.TestCase):
    def test_incomplete_profile_is_rejected(self):
        profile = TargetProfile(device_model="", os_version="", build_number="")
        self.assertTrue(validate_profile(profile))

    def test_complete_profile_is_accepted(self):
        profile = TargetProfile(
            device_model="ExamplePhone",
            os_version="27.0",
            build_number="21A000",
        )
        self.assertEqual(validate_profile(profile), [])

    def test_unverified_claim_is_not_usable(self):
        claim = CompatibilityClaim(
            component="example",
            status="unverified",
            source_url="https://example.org/research",
            build_number="21A000",
        )
        self.assertFalse(claim_is_usable(claim, target_build="21A000"))

    def test_verified_claim_requires_source_and_matching_build(self):
        claim = CompatibilityClaim(
            component="example",
            status="verified",
            source_url="https://example.org/research",
            build_number="21A000",
        )
        self.assertTrue(claim_is_usable(claim, target_build="21A000"))
        self.assertFalse(claim_is_usable(claim, target_build="21A001"))
        self.assertFalse(claim_is_usable(
            CompatibilityClaim(component="example", status="verified"),
            target_build="21A000",
        ))


if __name__ == "__main__":
    unittest.main()
