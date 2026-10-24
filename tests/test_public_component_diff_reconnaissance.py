"""Regression checks for public component-diff scope and evidence boundaries."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research" / "public_component_diff_reconnaissance_2026-10-24.md"


class PublicComponentDiffReconnaissanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = REPORT.read_text(encoding="utf-8")

    def test_other_model_is_not_mislabeled_as_exact_target(self):
        self.assertIn("iPhone18,1", self.text)
        self.assertIn("iPhone17,4", self.text)
        self.assertIn("cannot be represented as an exact-target binary comparison", self.text)

    def test_component_diffs_are_not_attributed_without_evidence(self):
        self.assertIn("AppleAVE2", self.text)
        self.assertIn("APFS", self.text)
        self.assertIn("not that those changes map to any of the 12 tracked CVEs", self.text)
        self.assertIn("Exact-target component comparison: still not established.", self.text)

    def test_no_jailbreak_or_exploit_claim(self):
        self.assertIn("End-to-end jailbreak: not verified.", self.text)
        self.assertIn("No exploit was run", self.text)
        self.assertIn("No device was accessed or modified", self.text)


if __name__ == "__main__":
    unittest.main()
