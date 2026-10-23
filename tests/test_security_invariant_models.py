"""Tests for benign abstract security-invariant models; not CVE reproductions."""
import unittest

from Framework.security_invariant_models import (
    ObjectLifetime,
    authorization_allows,
    output_is_fully_initialized,
    path_is_within_root,
    range_is_valid,
    transition_allowed,
)


class SecurityInvariantModelTests(unittest.TestCase):
    def test_authorization_fails_closed(self):
        self.assertTrue(authorization_allows(True))
        self.assertFalse(authorization_allows(False))
        self.assertFalse(authorization_allows(None))
        self.assertFalse(authorization_allows(1))

    def test_range_boundaries(self):
        self.assertTrue(range_is_valid(0, 0, 8))
        self.assertTrue(range_is_valid(0, 8, 8))
        self.assertTrue(range_is_valid(7, 1, 8))
        self.assertTrue(range_is_valid(8, 0, 8))
        self.assertFalse(range_is_valid(8, 1, 8))
        self.assertFalse(range_is_valid(9, 0, 8))
        self.assertFalse(range_is_valid(-1, 1, 8))
        self.assertFalse(range_is_valid(0, -1, 8))
        self.assertFalse(range_is_valid(0, 1, -1))
        self.assertFalse(range_is_valid(True, 1, 8))
        self.assertFalse(range_is_valid(0, 10**100, 8))

    def test_lifetime_rejects_use_after_terminal_release(self):
        obj = ObjectLifetime()
        self.assertTrue(obj.can_use())
        self.assertTrue(obj.retain())
        self.assertTrue(obj.release())
        self.assertTrue(obj.can_use())
        self.assertTrue(obj.release())
        self.assertFalse(obj.can_use())
        self.assertFalse(obj.retain())
        self.assertFalse(obj.release())

    def test_state_machine_requires_explicit_transition(self):
        graph = {"new": {"validated"}, "validated": {"complete"}, "complete": set()}
        self.assertTrue(transition_allowed("new", "validated", graph))
        self.assertFalse(transition_allowed("new", "complete", graph))
        self.assertFalse(transition_allowed("unknown", "complete", graph))
        self.assertFalse(transition_allowed("complete", "new", graph))

    def test_output_requires_all_declared_fields(self):
        required = ("status", "count", "payload")
        self.assertTrue(output_is_fully_initialized(required, {
            "status": "ok", "count": 0, "payload": b"",
        }))
        self.assertFalse(output_is_fully_initialized(required, {
            "status": "ok", "count": 0,
        }))
        self.assertFalse(output_is_fully_initialized(required, {
            "status": "ok", "count": None, "payload": b"",
        }))
        self.assertFalse(output_is_fully_initialized((), {}))

    def test_synthetic_path_containment(self):
        self.assertTrue(path_is_within_root("/safe/root", "/safe/root/file"))
        self.assertTrue(path_is_within_root("/safe/root", "/safe/root"))
        self.assertFalse(path_is_within_root("/safe/root", "/safe/rootsibling/file"))
        self.assertFalse(path_is_within_root("/safe/root", "/other/file"))
        self.assertFalse(path_is_within_root("safe/root", "/safe/root/file"))
        self.assertFalse(path_is_within_root("/safe/root", "safe/root/file"))


if __name__ == "__main__":
    unittest.main()
