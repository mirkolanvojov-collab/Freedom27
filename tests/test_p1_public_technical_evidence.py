"""Regression checks for the P1 public technical-evidence ledger."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "p1_public_technical_evidence_2026-10-24.json"
EXPECTED = {"CVE-2026-84607", "CVE-2026-43689"}

class P1PublicTechnicalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(PATH.read_text(encoding="utf-8"))
        cls.records = {item["cve_id"]: item for item in cls.doc["records"]}

    def test_scope_and_unique_ids(self):
        self.assertEqual(set(self.records), EXPECTED)
        self.assertEqual(len(self.doc["records"]), 2)
        self.assertEqual(self.doc["target"]["build"], "23G83")
        self.assertEqual(self.doc["target"]["os_version"], "iOS 26.6.1")

    def test_provenance_and_source_urls(self):
        for cve in EXPECTED:
            item = self.records[cve]
            self.assertTrue(item["primary_sources"])
            self.assertTrue(all(s["url"].startswith("https://") for s in item["primary_sources"]))
            self.assertEqual(item["exact_build_applicability"], "not_independently_verified")
            self.assertEqual(item["exploitability"], "not_established")
            self.assertTrue(item["patch_diff_status"])

    def test_public_84607_report_is_caveated(self):
        item = self.records["CVE-2026-84607"]
        self.assertEqual(len(item["public_leads"]), 1)
        lead = item["public_leads"][0]
        self.assertEqual(lead["verification_status"], "unverified_third_party_binary_analysis_hypothesis")
        self.assertIn("AI-generated", lead["source_authorship"])
        self.assertIn("23G83", lead["target_mismatch"])
        self.assertTrue(lead["stated_limitations"])
        self.assertFalse(lead["code_executed"])

    def test_no_unsupported_success_claims(self):
        self.assertEqual(self.doc["summary"]["exact_build_confirmations"], 0)
        self.assertEqual(self.doc["summary"]["freedom27_reproductions"], 0)
        self.assertFalse(self.doc["summary"]["full_jailbreak_chain_verified"])
        self.assertEqual(self.doc["summary"]["authoritative_patch_diffs_found"], 0)

if __name__ == "__main__":
    unittest.main()
