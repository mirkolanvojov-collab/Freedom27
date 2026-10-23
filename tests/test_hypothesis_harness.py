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


if __name__ == "__main__":
    unittest.main()
