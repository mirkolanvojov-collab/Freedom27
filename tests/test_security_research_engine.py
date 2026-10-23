import unittest

from Framework.security_research_engine import (
    EvidenceLevel,
    Hypothesis,
    Target,
    readiness_report,
)


TARGET = Target("iPhone 16 Plus", "iPhone17,4", "iOS 26.6.1", "23G83")
URL = ("https://example.com/research",)


class SecurityResearchEngineTests(unittest.TestCase):
    def make_hypothesis(self, **overrides):
        values = dict(
            hypothesis_id="H-BASE",
            boundary="app sandbox",
            claim="A documented operation exposes data outside the intended container",
            expected_observation="The test reads a harmless marker file in the test fixture",
            falsifying_observation="The marker remains inaccessible",
            source_urls=URL,
        )
        values.update(overrides)
        return Hypothesis(**values)

    def test_hypothesis_requires_falsifiable_claim_and_sources(self):
        self.assertEqual(self.make_hypothesis().validate(TARGET), [])

    def test_invalid_or_non_http_source_url_fails_closed(self):
        for url in ("not-a-url", "file:///tmp/research", "https:///missing-host"):
            with self.subTest(url=url):
                h = self.make_hypothesis(source_urls=(url,))
                self.assertIn("source URLs must be absolute HTTP(S) URLs", h.validate(TARGET))

    def test_exact_target_requires_target_result_artifact_and_timestamp(self):
        h = self.make_hypothesis(
            evidence_level=EvidenceLevel.EXACT_TARGET_VERIFIED,
            tested_target=TARGET,
            observed_result="Marker read succeeded",
        )
        issues = h.validate(TARGET)
        self.assertIn("exact-target label lacks a test artifact reference", issues)
        self.assertIn("exact-target label lacks a test timestamp", issues)

    def test_independent_reproduction_requires_reviewer_and_artifact(self):
        h = self.make_hypothesis(
            evidence_level=EvidenceLevel.INDEPENDENTLY_REPRODUCED,
            observed_result="Marker read succeeded",
        )
        issues = h.validate(TARGET)
        self.assertIn("independent reproduction lacks reviewer attribution", issues)
        self.assertIn("independent reproduction lacks a test artifact reference", issues)
        self.assertIn("independent reproduction lacks a test timestamp", issues)

    def test_exact_target_label_fails_closed_for_wrong_device(self):
        other = Target("Other phone", "other1,1", "iOS 26.6.1", "23G83")
        h = self.make_hypothesis(
            evidence_level=EvidenceLevel.EXACT_TARGET_VERIFIED,
            tested_target=other,
            observed_result="Example output",
            test_artifact="artifact.txt",
            test_timestamp_utc="2026-10-23T12:00:00Z",
        )
        self.assertIn("exact-target label does not match the configured target", h.validate(TARGET))

    def test_destructive_test_needs_recovery_plan(self):
        h = self.make_hypothesis(non_destructive=False, recovery_plan="")
        self.assertIn("potentially destructive test lacks a recovery plan", h.validate(TARGET))

    def test_report_never_calls_incomplete_record_verified(self):
        h = self.make_hypothesis(
            hypothesis_id="H-004",
            boundary="kernel privilege",
            claim="Unverified idea",
            evidence_level=EvidenceLevel.EXACT_TARGET_VERIFIED,
        )
        report = readiness_report(TARGET, [h])
        self.assertEqual(report["fully_verified_hypothesis_count"], 0)
        self.assertFalse(report["hypotheses"][0]["record_complete"])


if __name__ == "__main__":
    unittest.main()
