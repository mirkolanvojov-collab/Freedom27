import json
import tempfile
import unittest
from pathlib import Path

from Framework.hypothesis_harness import validate_record


class HypothesisHarnessTests(unittest.TestCase):
    def test_empty_record_fails(self):
        self.assertTrue(validate_record({}))

    def test_hypothesis_record_can_be_valid_without_claiming_exploitability(self):
        record = {
            "id": "h1",
            "hypothesis": "Example testable hypothesis",
            "safe_test": "Non-destructive local test in authorized lab",
            "expected_observation": "Documented observable behavior",
            "result": "not_tested",
        }
        self.assertEqual(validate_record(record), [])

    def test_reproduced_result_requires_evidence_note(self):
        record = {
            "id": "h1", "hypothesis": "Hypothesis", "safe_test": "Safe test",
            "expected_observation": "Observation", "result": "reproduced_in_lab",
        }
        self.assertTrue(any("evidence_note" in error for error in validate_record(record)))

    def test_malformed_record_root_fails_without_crashing(self):
        self.assertTrue(validate_record([]))

    def test_non_string_evidence_note_fails_without_crashing(self):
        record = {
            "id": "h1", "hypothesis": "Hypothesis", "safe_test": "Safe test",
            "expected_observation": "Observation", "result": "reproduced_in_lab",
            "evidence_note": None,
        }
        errors = validate_record(record)
        self.assertTrue(any("evidence_note must be a string" in error for error in errors))
        self.assertTrue(any("requires an evidence_note" in error for error in errors))

    def test_invalid_source_url_is_rejected(self):
        record = {
            "id": "h1", "hypothesis": "Hypothesis", "safe_test": "Safe test",
            "expected_observation": "Observation", "result": "not_tested",
            "source_url": "file:///tmp/payload",
        }
        self.assertTrue(any("valid HTTPS URL" in error for error in validate_record(record)))


if __name__ == "__main__":
    unittest.main()
