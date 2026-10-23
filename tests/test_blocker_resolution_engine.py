import unittest

from Framework.blocker_resolution_engine import build_plan, validate_evidence_record


TARGET = {
    "device_model": "iPhone 16 Plus",
    "model_identifier": "iPhone17,4",
    "exact_os_version": "iOS 26.6.1",
    "build_number": "23G83",
}
STATUS = {
    "generated_for": TARGET,
    "verified_complete_jailbreak": False,
    "gates": [
        {"id": gate, "status": "missing", "note": "No verified evidence"}
        for gate in (
            "entry", "sandbox_escape", "kernel_primitive", "privilege_escalation",
            "platform_mitigations", "persistence_or_bootstrap", "package_manager",
            "independent_reproduction",
        )
    ],
}


class BlockerResolutionEngineTests(unittest.TestCase):
    def test_plan_fails_closed_for_missing_gates(self):
        plan = build_plan(STATUS)
        self.assertEqual(plan["assessment"], "blocked")
        self.assertEqual(plan["open_task_count"], 8)
        self.assertFalse(plan["execution_policy"]["device_modified"])
        self.assertFalse(plan["execution_policy"]["exploit_execution_authorized"])

    def test_verified_labels_without_evidence_records_do_not_close_gates(self):
        doc = {
            "generated_for": TARGET,
            "verified_complete_jailbreak": True,
            "gates": [
                {"id": gate, "status": "verified"}
                for gate in (
                    "entry", "sandbox_escape", "kernel_primitive", "privilege_escalation",
                    "platform_mitigations", "persistence_or_bootstrap", "package_manager",
                    "independent_reproduction",
                )
            ],
        }
        plan = build_plan(doc)
        self.assertEqual(plan["assessment"], "blocked")
        self.assertEqual(plan["open_task_count"], 8)
        self.assertFalse(plan["verified_complete_jailbreak"])

    def test_verified_downstream_gate_still_requires_prerequisites(self):
        doc = {
            "generated_for": TARGET,
            "verified_complete_jailbreak": False,
            "gates": [{"id": "package_manager", "status": "verified"}],
        }
        plan = build_plan(doc)
        package_task = next(t for t in plan["tasks"] if t["gate"] == "package_manager")
        self.assertIn("persistence_or_bootstrap", package_task["unmet_prerequisites"])

    def test_exact_target_evidence_record_can_validate(self):
        record = {
            "claim_id": "test",
            "target": TARGET,
            "source_url": "https://example.org/research",
            "source_revision": "a" * 40,
            "status": "verified",
            "evidence_note": "Independently reproduced in a controlled test environment.",
            "independent_reproduction": True,
            "scope_confirmed": True,
        }
        self.assertEqual(validate_evidence_record(record, TARGET), [])

    def test_version_overlap_does_not_match_exact_target(self):
        record = {
            "target": {**TARGET, "build_number": "23G90"},
            "source_url": "https://example.org/research",
            "source_revision": "a" * 40,
            "status": "verified",
            "evidence_note": "Claim",
            "independent_reproduction": True,
            "scope_confirmed": True,
        }
        errors = validate_evidence_record(record, TARGET)
        self.assertTrue(any("exactly match" in error for error in errors))

    def test_verified_record_requires_independent_reproduction(self):
        record = {
            "target": TARGET,
            "source_url": "https://example.org/research",
            "source_revision": "a" * 40,
            "status": "verified",
            "evidence_note": "Claim",
            "independent_reproduction": False,
            "scope_confirmed": True,
        }
        errors = validate_evidence_record(record, TARGET)
        self.assertTrue(any("independent_reproduction=true" in error for error in errors))

    def test_bad_sha_is_rejected(self):
        record = {
            "target": TARGET,
            "source_url": "https://example.org/research",
            "source_revision": "latest",
            "status": "reviewed",
        }
        self.assertTrue(any("40-character" in error for error in validate_evidence_record(record, TARGET)))

    def test_invalid_status_document_rejected(self):
        with self.assertRaises(ValueError):
            build_plan([])

    def test_malformed_gate_status_fails_closed_without_crashing(self):
        doc = {
            "generated_for": TARGET,
            "verified_complete_jailbreak": False,
            "gates": [{"id": "entry", "status": ["verified"]}],
        }
        plan = build_plan(doc)
        self.assertEqual(plan["assessment"], "blocked")
        self.assertTrue(any(task["status"] == "invalid" for task in plan["tasks"]))

    def test_malformed_evidence_target_and_url_fail_closed(self):
        record = {
            "target": [],
            "source_url": "https://",
            "source_revision": "a" * 40,
            "status": ["verified"],
        }
        errors = validate_evidence_record(record, TARGET)
        self.assertTrue(any("exactly match" in error for error in errors))
        self.assertTrue(any("valid HTTPS URL" in error for error in errors))
        self.assertTrue(any("status must be" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
