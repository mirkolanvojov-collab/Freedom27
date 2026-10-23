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
        self.assertFalse(validate_profile(profile))

    def test_complete_profile_is_accepted(self):
        profile = TargetProfile(
            device_model="ExamplePhone",
            os_version="27.0",
            build_number="21A000",
        )
        self.assertTrue(validate_profile(profile))

    def test_unverified_claim_is_not_usable(self):
        claim = CompatibilityClaim(status="unverified", source_url="", build_number="")
        self.assertFalse(claim_is_usable(claim))

    def test_verified_claim_needs_source_and_build_match(self):
        claim = CompatibilityClaim(
            status="verified",
            source_url="https://example.org/research",
            build_number="21A000",
        )
        self.assertTrue(claim_is_usable(claim, target_build="21A000"))
        self.assertFalse(claim_is_usable(claim, target_build="21A001"))


if __name__ == "__main__":
    unittest.main()
