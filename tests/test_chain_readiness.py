import unittest

from Framework.chain_readiness import REQUIRED_GATES, assess


class ChainReadinessTests(unittest.TestCase):
    def test_missing_evidence_fails_closed(self):
        report = assess(
            {"device_model": "iPhone 16 Plus", "exact_os_version": "iOS 26.6.1", "build_number": "23G83"},
            {"target_evidence": {}},
        )
        self.assertFalse(report["ready_for_implementation_claim"])
        self.assertEqual(report["missing_gate_count"], len(REQUIRED_GATES))

    def test_only_literal_true_counts_as_evidence(self):
        target = {"device_model": "Phone", "exact_os_version": "OS", "build_number": "BUILD"}
        key = "Phone|OS|BUILD"
        evidence = {"target_evidence": {key: {gate_id: "true" for gate_id, _ in REQUIRED_GATES}}}
        report = assess(target, evidence)
        self.assertFalse(report["ready_for_implementation_claim"])

    def test_all_gates_need_literal_true(self):
        target = {"device_model": "Phone", "exact_os_version": "OS", "build_number": "BUILD"}
        key = "Phone|OS|BUILD"
        evidence = {"target_evidence": {key: {gate_id: True for gate_id, _ in REQUIRED_GATES}}}
        report = assess(target, evidence)
        self.assertTrue(report["ready_for_implementation_claim"])
        self.assertEqual(report["missing_gate_count"], 0)


if __name__ == "__main__":
    unittest.main()
