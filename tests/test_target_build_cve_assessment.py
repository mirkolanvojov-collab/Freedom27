"""Regression tests for the exact-target advisory/CPE assessment metadata."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT_PATH = ROOT / "research" / "target_build_cve_assessment_2026-10-24.json"
EXPECTED_IDS = {
    "CVE-2026-84607", "CVE-2026-43689", "CVE-2026-84523",
    "CVE-2026-86876", "CVE-2026-86886", "CVE-2026-84566",
    "CVE-2026-43687", "CVE-2026-43684", "CVE-2026-43686",
    "CVE-2026-65405", "CVE-2026-84622", "CVE-2026-28968",
}


class TargetBuildCveAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(ASSESSMENT_PATH.read_text(encoding="utf-8"))

    def test_target_identity_is_pinned(self):
        self.assertEqual(self.doc["target"], {
            "device_model": "iPhone 16 Plus",
            "model_identifier": "iPhone17,4",
            "os_version": "iOS 26.6.1",
            "build_number": "23G83",
        })

    def test_exactly_the_12_expected_cves_are_present_once(self):
        ids = [item["cve_id"] for item in self.doc["records"]]
        self.assertEqual(len(ids), 12)
        self.assertEqual(set(ids), EXPECTED_IDS)
        self.assertEqual(len(set(ids)), len(ids))

    def test_each_record_has_primary_sources_and_version_boundary(self):
        for item in self.doc["records"]:
            with self.subTest(cve=item["cve_id"]):
                self.assertEqual(item["apple_advisory_url"], "https://support.apple.com/en-us/149041")
                self.assertEqual(item["nvd_url"], f"https://nvd.nist.gov/vuln/detail/{item['cve_id'].lower()}")
                self.assertEqual(item["advisory_device_scope"], "iPhone 11 and later")
                self.assertEqual(item["fix_release"], "iOS 26.7")
                self.assertEqual(item["nvd_iphone_os_version_end_excluding"], "26.7")
                self.assertEqual(item["target_release"], "iOS 26.6.1")
                self.assertEqual(item["target_build"], "23G83")
                self.assertTrue(item["version_range_match"])

    def test_no_record_claims_exact_build_or_exploitability_verified(self):
        for item in self.doc["records"]:
            with self.subTest(cve=item["cve_id"]):
                self.assertEqual(item["exact_build_applicability"], "not_independently_verified")
                self.assertEqual(item["exploitability_on_target"], "not_established")
                self.assertEqual(item["jailbreak_chain_role"], "not_established")

    def test_capture_provenance_is_complete_and_successful(self):
        capture = self.doc["capture"]
        self.assertEqual(capture["workflow_run_id"], 40041118442)
        self.assertEqual(capture["successful_cve_records"], 12)
        self.assertEqual(capture["successful_cpe_match_records"], 12)
        self.assertEqual(capture["failed_record_count"], 0)
        self.assertEqual(len(capture["artifact_sha256"]), 64)

    def test_root_and_nfs_prerequisites_are_not_misrepresented(self):
        by_id = {item["cve_id"]: item for item in self.doc["records"]}
        self.assertEqual(by_id["CVE-2026-84622"]["prerequisite_context"], "root_privileges")
        self.assertEqual(by_id["CVE-2026-43687"]["prerequisite_context"], "malicious_nfs_server")
        self.assertEqual(by_id["CVE-2026-43686"]["prerequisite_context"], "malicious_nfs_server")

    def test_global_conclusion_does_not_overstate_exact_build_evidence(self):
        conclusion = self.doc["conclusions"]
        self.assertIn("not independently verified", conclusion["exact_build"])
        self.assertIn("No CVE", conclusion["exploitability"])
        self.assertIn("No device", conclusion["safety"])


if __ (name__) == "__main__":
    unittest.main()
