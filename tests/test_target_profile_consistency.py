"""Ensure the target profile agrees with the exact-build status record."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "research" / "target_profile.json"
STATUS_PATH = ROOT / "research" / "current_exact_target_status.json"


class TargetProfileConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        cls.status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))["generated_for"]

    def test_profile_and_exact_target_status_agree(self):
        expected = {
            "device_model": "device_model",
            "model_identifier": "model_identifier",
            "exact_os_version": "exact_os_version",
            "build_number": "build_number",
        }
        for profile_key, status_key in expected.items():
            with self.subTest(field=profile_key):
                self.assertEqual(self.profile[profile_key], self.status[status_key])

    def test_target_os_is_the_exact_device_os_not_the_future_goal(self):
        self.assertEqual(self.profile["target_os"], self.profile["exact_os_version"])
        self.assertIn("iOS 27 remains a planned research goal", self.profile["notes"])

    def test_profile_keeps_research_only_status(self):
        self.assertIn("research-only", self.profile["target_status"])
        self.assertEqual(self.status["build_number"], "23G83")


if __name__ == "__main__":
    unittest.main()
