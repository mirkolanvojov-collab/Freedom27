"""Regression checks for target firmware release provenance claims."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research" / "target_release_provenance_2026-10-24.md"


class TargetReleaseProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = REPORT.read_text(encoding="utf-8")

    def test_target_tuple_is_recorded(self):
        for value in ("iPhone 16 Plus", "iPhone17,4", "26.6.1", "23G83"):
            self.assertIn(value, self.text)

    def test_primary_and_secondary_sources_are_distinguished(self):
        self.assertIn("https://support.apple.com/en-us/148282", self.text)
        self.assertIn("https://ipsw.me/download/iPhone17%2C4/23G83/", self.text)
        self.assertIn("Primary source", self.text)
        self.assertIn("Secondary firmware catalogue", self.text)

    def test_no_unsupported_exact_build_claim(self):
        self.assertIn("does **not** establish whether any particular CVE", self.text)
        self.assertIn("no Freedom27 reproduction", self.text)
        self.assertIn("No exploit code retrieved or executed", self.text)
        self.assertIn("No device accessed", self.text)


if __name__ == "__main__":
    unittest.main()
