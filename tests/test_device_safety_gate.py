import unittest

from Framework.device_safety_gate import REQUIRED_ATTESTATIONS, REQUIRED_CHAIN_GATES, TARGET_FIELDS, assess_safety


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
            "gates": [{"id": gate_id, "status": "missing"} for gate_id in REQUIRED_CHAIN_GATES],
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

    def test_generic_url_without_target_tuple_and_revision_is_rejected(self):
        attestations = {
            gate_id: {"status": "verified", "evidence_url": "https://example.org/evidence",
                      "evidence_note": "Reviewed evidence"}
            for gate_id, _ in REQUIRED_ATTESTATIONS
        }
        report = assess_safety(self.target_status, attestations)
        self.assertFalse(report["preflight_passed"])
        self.assertIn("backup_verified", report["blockers"])

    def test_attestation_for_different_build_is_rejected(self):
        target = self.target_status["generated_for"]
        attestations = {
            gate_id: {
                "status": "verified",
                "evidence_url": "https://example.org/evidence",
                "evidence_note": "Reviewed evidence",
                "source_revision": "a" * 40,
                "target": {**target, "build_number": "23G84"},
            }
            for gate_id, _ in REQUIRED_ATTESTATIONS
        }
        report = assess_safety(self.target_status, attestations)
        self.assertFalse(report["preflight_passed"])
        self.assertIn("backup_verified", report["blockers"])

    def test_claimed_chain_without_all_source_pinned_gates_does_not_pass(self):
        target = dict(self.target_status)
        target["status"] = "verified"
        target["verified_complete_jailbreak"] = True
        target["gates"] = [{"id": gate_id, "status": "verified"} for gate_id in REQUIRED_CHAIN_GATES]
        attestations = {
            gate_id: {
                "status": "verified",
                "evidence_url": "https://example.org/evidence",
                "evidence_note": "Reviewed evidence",
                "source_revision": "a" * 40,
                "target": target["generated_for"],
            }
            for gate_id, _ in REQUIRED_ATTESTATIONS
        }
        report = assess_safety(target, attestations)
        self.assertFalse(report["preflight_passed"])
        self.assertIn("project_exact_target_chain", report["blockers"])
        self.assertFalse(report["device_execution_authorized"])
        self.assertFalse(report["guarantees_no_crash"])

    def test_malformed_ipv6_evidence_url_fails_closed_without_crashing(self):
        target = self.target_status["generated_for"]
        attestations = {
            gate_id: {
                "status": "verified",
                "evidence_url": "https://[::1",
                "evidence_note": "Reviewed evidence",
                "source_revision": "a" * 40,
                "target": target,
            }
            for gate_id, _ in REQUIRED_ATTESTATIONS
        }
        report = assess_safety(self.target_status, attestations)
        self.assertFalse(report["preflight_passed"])
        self.assertIn("backup_verified", report["blockers"])

    def test_duplicate_chain_gate_ids_fail_closed_even_if_last_entry_is_verified(self):
        target = dict(self.target_status)
        target["status"] = "verified"
        target["verified_complete_jailbreak"] = True
        evidence = {
            "status": "verified",
            "evidence_url": "https://example.org/evidence",
            "evidence_note": "Reviewed evidence",
            "source_revision": "a" * 40,
            "target": target["generated_for"],
        }
        target["gates"] = (
            [{"id": "entry", "status": "missing"}]
            + [{"id": gate_id, "status": "verified", "evidence": evidence}
               for gate_id in REQUIRED_CHAIN_GATES]
        )
        attestations = {gate_id: dict(evidence) for gate_id, _ in REQUIRED_ATTESTATIONS}
        report = assess_safety(target, attestations)
        self.assertFalse(report["preflight_passed"])
        self.assertIn("project_exact_target_chain", report["blockers"])
        chain_gate = next(gate for gate in report["gates"] if gate["id"] == "project_exact_target_chain")
        self.assertIn("Duplicate milestone gate IDs", chain_gate["reason"])

    def test_invalid_input_fails_closed(self):
        report = assess_safety(None, None)
        self.assertFalse(report["preflight_passed"])
        self.assertFalse(report["device_execution_authorized"])


if __name__ == "__main__":
    unittest.main()
