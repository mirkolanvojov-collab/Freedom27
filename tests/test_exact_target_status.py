import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "research" / "current_exact_target_status.json"


class ExactTargetStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))

    def test_report_identifies_the_intended_device_and_build(self):
        target = self.status["generated_for"]
        self.assertEqual(target["device_model"], "iPhone 16 Plus")
        self.assertEqual(target["model_identifier"], "iPhone17,4")
        self.assertEqual(target["exact_os_version"], "iOS 26.6.1")
        self.assertEqual(target["build_number"], "23G83")

    def test_unverified_target_cannot_be_reported_as_a_complete_jailbreak(self):
        self.assertEqual(self.status["status"], "blocked")
        self.assertIs(self.status["verified_complete_jailbreak"], False)
        self.assertEqual(
            self.status["assessment_type"],
            "repository evidence review; not a device test",
        )

    def test_all_required_security_milestones_remain_explicit(self):
        gates = {gate["id"]: gate for gate in self.status["gates"]}
        required = {
            "entry",
            "sandbox_escape",
            "kernel_primitive",
            "privilege_escalation",
            "platform_mitigations",
            "persistence_or_bootstrap",
            "package_manager",
            "independent_reproduction",
        }
        self.assertTrue(required.issubset(gates))
        for gate_id in required:
            with self.subTest(gate=gate_id):
                self.assertEqual(gates[gate_id]["status"], "missing")
                self.assertTrue(gates[gate_id]["note"].strip())

    def test_ci_results_are_not_misrepresented_as_device_testing(self):
        interpretation = self.status["repository_checks"]["interpretation"].lower()
        self.assertIn("metadata only", interpretation)
        self.assertIn("physical iphone", interpretation)


if __name__ == "__main__":
    unittest.main()
