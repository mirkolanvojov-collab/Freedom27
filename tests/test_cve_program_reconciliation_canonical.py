"""Checks for pinned public CVE record reconciliation metadata."""
import json
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "research" / "cve_program_reconciliation_2026-10-24_canonical.json"
EXPECTED = {"CVE-2026-84607", "CVE-2026-43689", "CVE-2026-84523", "CVE-2026-86876", "CVE-2026-86886", "CVE-2026-84566", "CVE-2026-43687", "CVE-2026-43684", "CVE-2026-43686", "CVE-2026-65405", "CVE-2026-84622", "CVE-2026-28968"}

class CanonicalCveReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(PATH.read_text(encoding="utf-8"))
        cls.records = cls.doc["records"]

    def test_expected_ids_and_unique_records(self):
        ids = [item["cve_id"] for item in self.records]
        self.assertEqual(set(ids), EXPECTED)
        self.assertEqual(len(ids), len(set(ids)))

    def test_cve_program_record_provenance(self):
        self.assertEqual(self.doc["cve_list_snapshot"]["commit"], "c21430318b4b48252dd6ba344df26d60e6354f12")
        for item in self.records:
            self.assertEqual(item["record"]["state"], "PUBLISHED")
            self.assertEqual(item["record"]["assigner_short_name"], "apple")
            self.assertTrue(item["record"]["apple_ios_26_7_advisory_referenced"])
            self.assertTrue(item["cve_record_impact"])
            self.assertTrue(item["cve_record_description"])
            self.assertTrue(any(r["less_than"] == "26.7" for r in item["record"]["ios_ipados_affected_ranges"]))

    def test_nvd_capture_and_target_uncertainty(self):
        self.assertIn("40041118442", self.doc["sources"]["nvd_capture_run"])
        self.assertEqual(self.doc["sources"]["nvd_artifact_sha256"], "e21723d4911c67ca86efbfa74b845c595070ca39ca80856bf1d8e4af3fd9f236")
        self.assertEqual(self.doc["summary"]["exact_build_confirmations"], 0)
        self.assertEqual(self.doc["summary"]["exploitability_confirmations"], 0)
        for item in self.records:
            self.assertEqual(item["nvd"]["iphone_os_version_end_excluding"], "26.7")
            self.assertEqual(item["target"]["exact_build_applicability"], "not_independently_verified")
            self.assertEqual(item["target"]["exploitability"], "not_established")

if __name__ == "__main__":
    unittest.main()
