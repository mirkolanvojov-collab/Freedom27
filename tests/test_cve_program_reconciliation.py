"""Regression tests for the pinned CVE Program / Apple / NVD reconciliation."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "cve_program_reconciliation_2026-10-24.json"
EXPECTED = {
    "CVE-2026-84607", "CVE-2026-43689", "CVE-2026-84523",
    "CVE-2026-86876", "CVE-2026-86886", "CVE-2026-84566",
    "CVE-2026-43687", "CVE-2026-43684", "CVE-2026-43686",
    "CVE-2026-65405", "CVE-2026-84622", "CVE-2026-28968",
}
PINNED_COMMIT = "c21430318b4b48252dd6ba344df26d60e6354f12"
NVD_SHA256 = "e21723d4911c67ca86efbfa74b845c595070ca39ca80856bf1d8e4af3fd9f236"


class CveProgramReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(PATH.read_text(encoding="utf-8"))
        cls.records = cls.doc["records"]
        cls.by_id = {r["cve_id"]: r for r in cls.records}

    def test_exactly_the_expected_unique_cves_are_present(self):
        ids = [r["cve_id"] for r in self.records]
        self.assertEqual(set(ids), EXPECTED)
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(set(ids)), 12)

    def test_upstream_snapshot_is_pinned(self):
        self.assertEqual(self.doc["cve_list_snapshot"]["commit"], PINNED_COMMIT)
        self.assertIn(PINNED_COMMIT, self.doc["cve_list_snapshot"]["commit_url"])

    def test_every_record_is_published_by_apple_and_links_advisory(self):
        for record in self.records:
            with self.subTest(cve=record["cve_id"]):
                self.assertEqual(record["record"]["state"], "PUBLISHED")
                self.assertEqual(record["record"]["assigner_short_name"], "apple")
                self.assertTrue(record["record"]["apple_ios_26_7_advisory_referenced"])
                self.assertTrue(record["record"]["url"].endswith(f"{record['cve_id']}.json"))
                self.assertTrue(record["cve_record_impact"])
                self.assertTrue(record["cve_record_description"])

    def test_all_cve_program_ranges_include_pre_26_7_ios(self):
        for record in self.records:
            with self.subTest(cve=record["cve_id"]):
                ranges = record["record"]["ios_ipados_affected_ranges"]
                self.assertTrue(any(
                    r["status"] == "affected" and r["less_than"] == "26.7"
                    for r in ranges
                ))

    def test_nvd_capture_provenance_is_preserved(self):
        sources = self.doc["sources"]
        self.assertIn("/actions/runs/40041118442", sources["nvd_capture_run"])
        self.assertEqual(sources["nvd_artifact_sha256"], NVD_SHA256)
        for record in self.records:
            with self.subTest(cve=record["cve_id"]):
                self.assertTrue(record["nvd"]["cve_record_captured"])
                self.assertTrue(record["nvd"]["cpe_match_record_captured"])
                self.assertEqual(record["nvd"]["iphone_os_version_end_excluding"], "26.7")
                self.assertTrue(record["nvd"]["target_release_version_range_match"])

    def test_target_and_uncertainty_are_not_upgraded(self):
        self.assertEqual(self.doc["target"]["build_number"], "23G83")
        self.assertEqual(self.doc["summary"]["exact_build_confirmations"], 0)
        self.assertEqual(self.doc["summary"]["exploitability_confirmations"], 0)
        for record in self.records:
            with self.subTest(cve=record["cve_id"]):
                self.assertEqual(record["target"]["exact_build_applicability"], "not_independently_verified")
                self.assertEqual(record["target"]["exploitability"], "not_established")

    def test_nfs_and_root_prerequisites_remain_distinct(self):
        self.assertIn("malicious NFS server", self.by_id["CVE-2026-43687"]["cve_record_impact"])
        self.assertIn("malicious NFS server", self.by_id["CVE-2026-43686"]["cve_record_impact"])
        self.assertIn("root privileges", self.by_id["CVE-2026-84622"]["cve_record_impact"])
        self.assertEqual(self.by_id["CVE-2026-43684"]["record"]["ios_ipados_affected_ranges"], [
            {"version": "0", "status": "affected", "less_than": "26.7", "version_type": "custom"}
        ])


if __name__ == "__main__":
    unittest.main()
