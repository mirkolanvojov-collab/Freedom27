import unittest
from unittest.mock import patch

from Framework.advisory_source_audit import audit_document, fetch_text


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

    def test_candidate_specific_source_is_fetched(self):
        doc = {
            "source": {"url": "https://support.apple.com/en-us/149041"},
            "candidates": [
                {"id": "CVE-2026-12345", "source_url": "https://support.apple.com/en-us/128066"}
            ],
        }
        pages = {
            "https://support.apple.com/en-us/149041": "base page",
            "https://support.apple.com/en-us/128066": "CVE-2026-12345",
        }
        report = audit_document(doc, pages.__getitem__)
        self.assertTrue(report["ok"])
        self.assertEqual(report["checked"], 1)
        self.assertEqual(report["source_count"], 2)

    def test_non_apple_source_is_rejected(self):
        doc = {
            "source": {"url": "https://support.apple.com/en-us/149041"},
            "candidates": [
                {"id": "CVE-2026-12345", "source_url": "https://example.com/advisory"}
            ],
        }
        def fetch(url):
            if "example.com" in url:
                raise ValueError("refusing non-Apple or non-HTTPS source")
            return "base page"
        report = audit_document(doc, fetch)
        self.assertFalse(report["ok"])
        self.assertTrue(any("source fetch failed" in error for error in report["errors"]))

    def test_invalid_cve_id_rejected(self):
        doc = {
            "source": {"url": "https://support.apple.com/en-us/149041"},
            "candidates": [{"id": "not-a-cve"}],
        }
        report = audit_document(doc, lambda _url: "")
        self.assertFalse(report["ok"])
        self.assertTrue(any("invalid CVE identifier" in error for error in report["errors"]))

    def test_non_object_input_rejected(self):
        report = audit_document([], lambda _url: "")
        self.assertFalse(report["ok"])
        self.assertIn("document root must be an object", report["errors"])

    def test_fetch_text_rejects_redirect_outside_apple_support(self):
        class FakeHeaders:
            def get_content_charset(self):
                return "utf-8"

        class FakeResponse:
            headers = FakeHeaders()

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return None

            def geturl(self):
                return "https://example.com/redirected"

            def read(self):
                return b"CVE-2026-12345"

        with patch("Framework.advisory_source_audit.urllib.request.urlopen", return_value=FakeResponse()):
            with self.assertRaisesRegex(ValueError, "redirect outside"):
                fetch_text("https://support.apple.com/en-us/149041")

    def test_fetch_text_rejects_embedded_credentials(self):
        with self.assertRaisesRegex(ValueError, "non-Apple or non-HTTPS"):
            fetch_text("https://user@support.apple.com/en-us/149041")


if __name__ == "__main__":
    unittest.main()
