import copy
import json
import unittest

from Framework.advisory_candidates import DEFAULT_PATH, validate_document


class AdvisoryCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(DEFAULT_PATH.read_text(encoding="utf-8"))

    def test_current_document_passes(self):
        self.assertEqual(validate_document(self.document), [])

    def test_duplicate_candidate_ids_rejected(self):
        doc = copy.deepcopy(self.document)
        doc["candidates"].append(copy.deepcopy(doc["candidates"][0]))
        self.assertTrue(any("duplicate id" in e for e in validate_document(doc)))

    def test_missing_source_url_rejected(self):
        doc = copy.deepcopy(self.document)
        doc["source"]["url"] = "http://example.invalid"
        self.assertTrue(any("source.url must be HTTPS" in e for e in validate_document(doc)))

    def test_target_confirmation_cannot_be_asserted_without_separate_evidence(self):
        doc = copy.deepcopy(self.document)
        doc["candidates"][0]["target_applicability"] = "confirmed_by_primary_source"
        self.assertTrue(any("target-specific evidence record" in e for e in validate_document(doc)))

    def test_advisory_cannot_claim_jailbreak_completion(self):
        doc = copy.deepcopy(self.document)
        doc["candidates"][0]["chain_status"] = "verified_complete_jailbreak"
        self.assertTrue(any("complete jailbreak" in e for e in validate_document(doc)))

    def test_device_execution_policy_is_fail_closed(self):
        doc = copy.deepcopy(self.document)
        doc["policy"]["exploit_executed"] = True
        self.assertTrue(any("exploit_executed must remain false" in e for e in validate_document(doc)))


if __name__ == "__main__":
    unittest.main()
