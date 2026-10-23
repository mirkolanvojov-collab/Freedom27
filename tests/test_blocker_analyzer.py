import unittest

from Framework.blocker_analyzer import analyze


TARGET = {
    "device_model": "iPhone 16 Plus",
    "model_identifier": "iPhone17,4",
    "exact_os_version": "iOS 26.6.1",
    "build_number": "23G83",
}


class BlockerAnalyzerTests(unittest.TestCase):
    def test_missing_gates_are_reported_as_blockers(self):
        report = analyze({"generated_for": TARGET, "gates": [], "verified_complete_jailbreak": False})
        self.assertEqual(report["assessment"], "blocked")
        self.assertFalse(report["verified_complete_jailbreak"])
        self.assertGreaterEqual(report["blocker_count"], 8)
        self.assertTrue(report["safe_to_continue_read_only_research"])
        self.assertFalse(report["device_modified"])

    def test_verified_label_without_evidence_remains_a_blocker(self):
        report = analyze({
            "generated_for": TARGET,
            "gates": [{"id": "entry", "status": "verified", "note": "source reviewed"}],
            "verified_complete_jailbreak": False,
        })
        entry = next(item for item in report["blockers"] if item["id"] == "entry")
        self.assertIn("lacks valid source-pinned", entry["blocker"])

    def test_verified_gate_with_exact_target_evidence_is_not_a_blocker(self):
        evidence = {
            "target": TARGET,
            "source_url": "https://example.org/research",
            "source_revision": "a" * 40,
            "evidence_note": "Primary source scope and independent reproduction reviewed.",
            "independent_reproduction": True,
            "scope_confirmed": True,
        }
        report = analyze({
            "generated_for": TARGET,
            "gates": [{"id": "entry", "status": "verified", "evidence": evidence}],
            "verified_complete_jailbreak": False,
        })
        self.assertNotIn("entry", [item["id"] for item in report["blockers"]])

    def test_unrecognized_status_fails_closed(self):
        report = analyze({
            "generated_for": TARGET,
            "gates": [{"id": "entry", "status": "maybe"}],
            "verified_complete_jailbreak": False,
        })
        entry = next(item for item in report["blockers"] if item["id"] == "entry")
        self.assertEqual(entry["current_status"], "maybe")

    def test_invalid_document_rejected(self):
        with self.assertRaises(ValueError):
            analyze([])


if __name__ == "__main__":
    unittest.main()
