"""Regression checks preventing AppleAVE2 cross-CVE conflation."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research" / "ave2_cross_cve_triage_2026-10-24.md"


class Ave2CrossCveTriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = REPORT.read_text(encoding="utf-8")

    def test_firmware_hash_provenance_is_explicit(self):
        self.assertIn("101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f", self.text)
        self.assertIn("11225458130", self.text)
        self.assertIn("streaming verification succeeded", self.text)
        self.assertIn("without being written to disk", self.text)
        self.assertIn("does not establish that the digest is an Apple-signed attestation", self.text)

    def test_distinct_cves_are_not_conflated(self):
        self.assertIn("CVE-2026-64747", self.text)
        self.assertIn("CVE-2026-84607", self.text)
        self.assertIn("not independent validation of iOS CVE-2026-84607", self.text)
        self.assertIn("separate CVE identifier", self.text)

    def test_no_exploit_or_device_execution_claim(self):
        self.assertIn("No exploit code built or run", self.text)
        self.assertIn("No device accessed", self.text)
        self.assertIn("does not establish applicability", self.text)


if __name__ == "__main__":
    unittest.main()
