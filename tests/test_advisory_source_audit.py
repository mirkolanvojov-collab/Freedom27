import copy
import json
import unittest

from Framework.advisory_source_audit import audit_document


class AdvisorySourceAuditTests(unittest.TestCase):
    def setUp(self):
        self.document = {
            "source": {
                "url": "https://support.apple.com/en-us/149041",
                "verified_against": ["https://support.apple.com/en-us/148282"],
            },
            "candidates": [
                {"id": "CVE-2026-84607", "source_url": "https://support.apple.com/en-us/149041"},
            ],
            "excluded_candidates": [
                {"id": "CVE-2026-65343", "source_url": "https://support.apple.com/en-us/148282"},
            ],
        }

    def test_ids_present_in_declared_sources_pass(self):
        pages = {
            "https://support.apple.com/en-us/149041": "CVE-2026-84607",
            "https://support.apple.com/en-us/148282": "CVE-2026-65343",
        }
        report = audit_document(self.document, pages.__getitem__)
        self.assertTrue(report["ok"])
        self.assertEqual(report["checked"], 2)

    def test_missing_cve_id_fails_closed(self):
        pages = {
            "https://support.apple.com/en-us/149041": "CVE-2026-84607",
            "https://support.apple.com/en-us/148282": "some other CVE",
        }
        report = audit_document(self.document, pages.__getitem__)
        self.assertFalse(report["ok"])
        self.assertTrue(any("CVE-2026-65343: not found" in error for error in report["errors"]))

    def test_fetch_failure_is_reported(self):
        def fail(_url):
            raise OSError("offline")
        report = audit_document(self.document, fail)
        self.assertFalse(report["ok"])
        self.assertTrue(any("source fetch failed" in error for error in report["errors"]))

    def test_non_object_input_rejected(self):
        report = audit_document([], lambda _url: "")
        self.assertFalse(report["ok"])
        self.assertIn("document root must be an object", report["errors"])


if __name__ == "__main__":
    unittest.main()
