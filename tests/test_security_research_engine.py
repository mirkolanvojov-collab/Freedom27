import unittest

from Framework.security_research_engine import (
    EvidenceLevel,
    Hypothesis,
    Target,
    readiness_report,
)


TARGET = Target("iPhone 16 Plus", "iPhone17,4", "iOS 26.6.1", "23G83")


class SecurityResearchEngineTests(unittest.TestCase):
    def test_hypothesis_requires_falsifiable_claim_and_sources(self):
        h = Hypothesis(
            hypothesis_id="H-001",
            boundary="app sandbox",
            claim="A documented operation exposes data outside the intended container",
            expected_observation="The test reads a harmless marker file in the test fixture",
            falsifying_observation="The marker remains inaccessible",
            source_urls=("https://example.com/research",),
        )
        self.assertEqual(h.validate(TARGET), [])

    def test_exact_target_label_fails_closed_for_wrong_device(self):
        other = Target("Other phone", "other1,1", "iOS 26.6.1", "23G83")
        h = Hypothesis(
            hypothesis_id="H-002",
            boundary="kernel privilege",
            claim="Example claim",
            expected_observation="Expected output",
            falsifying_observation="No output",
            source_urls=("https://example.com/research",),
            evidence_level=EvidenceLevel.EXACT_TARGET_VERIFIED,
            tested_target=other,
            observed_result="Example output",
        )
        self.assertIn(
            "exact-target label does not match the configured target",
            h.validate(TARGET),
        )

    def test_destructive_test_needs_recovery_plan(self):
        h = Hypothesis(
            hypothesis_id="H-003",
            boundary="runtime",
            claim="Example",
            expected_observation="Expected",
            falsifying_observation="Not expected",
            source_urls=("https://example.com/research",),
            non_destructive=False,
        )
        self.assertIn("potentially destructive test lacks a recovery plan", h.validate(TARGET))

    def test_report_never_calls_incomplete_record_verified(self):
        h = Hypothesis(
            hypothesis_id="H-004",
            boundary="kernel privilege",
            claim="Unverified idea",
            expected_observation="Expected",
            falsifying_observation="Not expected",
            evidence_level=EvidenceLevel.EXACT_TARGET_VERIFIED,
        )
        report = readiness_report(TARGET, [h])
        self.assertEqual(report["fully_verified_hypothesis_count"], 0)
        self.assertFalse(report["hypotheses"][0]["record_complete"])


if __name__ == "__main__":
    unittest.main()
