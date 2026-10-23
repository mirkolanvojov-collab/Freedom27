import json
import unittest
from pathlib import Path

from Framework.universal_research_engine import DEFAULT_ADVISORY, analyze_advisories, build_report, load_json


class UnifiedResearchEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = load_json(DEFAULT_ADVISORY)

    def test_report_fails_closed_without_claiming_jailbreak(self):
        report = build_report(self.document)
        self.assertEqual(report["assessment"], "blocked")
        self.assertFalse(report["summary"]["verified_complete_jailbreak"])
        self.assertFalse(report["summary"]["device_modified"])
        self.assertEqual(report["summary"]["verified_exact_target_vulnerabilities"], 0)

    def test_candidate_statuses_are_not_upgraded(self):
        report = build_report(self.document)
        for item in report["advisory_analysis"]["candidates_ranked_for_review"]:
            self.assertEqual(item["target_applicability"], "not_established")
            self.assertEqual(item["reproduction_status"], "not_reproduced_by_Freedom27")

    def test_reports_excluded_candidates(self):
        report = build_report(self.document)
        self.assertGreaterEqual(report["summary"]["excluded_candidates"], 2)

    def test_non_https_candidate_source_is_flagged(self):
        document = json.loads(json.dumps(self.document))
        document["candidates"][0]["source_url"] = "http://example.invalid"
        self.assertTrue(analyze_advisories(document)["validation_errors"])

    def test_review_priority_is_not_named_exploitability(self):
        report = build_report(self.document)
        self.assertIn("review_priority_score", report["advisory_analysis"]["candidates_ranked_for_review"][0])
        self.assertNotIn("exploitability_score", report["advisory_analysis"]["candidates_ranked_for_review"][0])


if __name__ == "__main__":
    unittest.main()
