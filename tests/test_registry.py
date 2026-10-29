import unittest

from Framework.registry import validate_entry


class RegistryTests(unittest.TestCase):
    def test_empty_entry_is_rejected(self):
        self.assertTrue(validate_entry({}))

    def test_entry_with_required_fields_is_accepted(self):
        entry = {
            "id": "public-advisory-example",
            "title": "Public advisory",
            "source_url": "https://example.org/advisory",
            "status": "unverified",
        }
        self.assertEqual(validate_entry(entry), [])

    def test_unknown_status_is_rejected(self):
        entry = {
            "id": "public-advisory-example",
            "title": "Public advisory",
            "source_url": "https://example.org/advisory",
            "status": "guaranteed",
        }
        self.assertTrue(validate_entry(entry))

    def test_malformed_https_port_is_rejected(self):
        entry = {
            "id": "public-advisory-example",
            "title": "Public advisory",
            "source_url": "https://example.org:bad/advisory",
            "status": "unverified",
        }
        self.assertTrue(any("valid HTTPS URL" in error for error in validate_entry(entry)))

    def test_unhashable_status_and_invalid_https_url_are_rejected(self):
        entry = {
            "id": "public-advisory-example",
            "title": "Public advisory",
            "source_url": "https://",
            "status": ["verified"],
        }
        errors = validate_entry(entry)
        self.assertTrue(any("status must be one of" in error for error in errors))
        self.assertTrue(any("valid HTTPS URL" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
