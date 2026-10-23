import unittest

from Framework.registry import validate_entry


class RegistryTests(unittest.TestCase):
    def test_empty_entry_is_rejected(self):
        self.assertFalse(validate_entry({}))

    def test_entry_with_required_public_research_fields_is_accepted(self):
        entry = {
            "title": "Public advisory",
            "source_url": "https://example.org/advisory",
            "status": "unverified",
            "affected_builds": [],
        }
        self.assertTrue(validate_entry(entry))

    def test_unknown_status_is_rejected(self):
        entry = {
            "title": "Public advisory",
            "source_url": "https://example.org/advisory",
            "status": "guaranteed",
            "affected_builds": [],
        }
        self.assertFalse(validate_entry(entry))


if __name__ == "__main__":
    unittest.main()
