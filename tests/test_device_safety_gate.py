import unittest

from Framework.device_safety_gate import REQUIRED_ATTESTATIONS, assess_safety


class DeviceSafetyGateTests(unittest.TestCase):
    def setUp(self):
        self.target_status = {
            "status": "blocked",
            "verified_complete_jailbreak": False,
            "generated_for": {
                "device_model": "iPhone 16 Plus",
                "model_identifier": "iPhone17,4",
                "exact_os_version": "iOS 26.6.1",
                "build_number": "23G83",
            },
        }

    def test_current_project_fails_closed(self):
        report = assess_safety(self.target_status)
        self.assertFalse(report["preflight_passed"])
        self.assertFalse(report["device_execution_authorized"])
        self.assertFalse(report["guarantees_no_crash"])
        self.assertGreater(report["blocker_count"], 0)

    def test_bare_true_flags_do_not_satisfy_attestations(self):
        attestations = {gate_id: True for gate_id, _ in REQUIRED_ATTESTATIONS}
        report = assess_safety(self.target_status, attestations)
        self.assertFalse(report["preflight_passed"])
        self.assertIn("exact_target_chain_verified", report["blockers"])

    def test_claimed_chain_does_not_authorize_execution(self):
        target = dict(self.target_status)
        target["status"] = "verified"
        target["verified_complete_jailbreak"] = True
        attestations = {
            gate_id: {"status": "verified", "evidence_url": "https://example.org/evidence",
                      "evidence_note": "Reviewed test evidence"}
            for gate_id, _ in REQUIRED_ATTESTATIONS
        }
        report = assess_safety(target, attestations)
        self.assertTrue(report["preflight_passed"])
        self.assertFalse(report["device_execution_authorized"])
        self.assertFalse(report["guarantees_no_crash"])


if __name__ == "__main__":
    unittest.main()
