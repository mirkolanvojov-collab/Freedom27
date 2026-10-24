"""Tests for the read-only exact-build compatibility report."""
import json
import tempfile
import unittest
from pathlib import Path

from Framework.compatibility_status import assess_target, format_report


class CompatibilityStatusTests(unittest.TestCase):
    def make_root(self, claim_status="not-supported", matching=True):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "research").mkdir()
        profile = {
            "device_model": "iPhone 16 Plus",
            "model_identifier": "iPhone17,4",
            "exact_os_version": "iOS 26.6.1",
            "build_number": "23G83",
        }
        claim = {
            "device_model": "iPhone 16 Plus",
            "model_identifier": "iPhone17,4" if matching else "iPhone17,3",
            "os_version": "iOS 26.6.1",
            "build_number": "23G83",
            "status": claim_status,
            "summary": "Test finding",
            "evidence_url": "https://example.com/evidence",
            "notes": "Reviewed test evidence",
        }
        (root / "research" / "target_profile.json").write_text(json.dumps(profile), encoding="utf-8")
        (root / "research" / "target_status.json").write_text(json.dumps({"claims": [claim]}), encoding="utf-8")
        return temp, root

    def test_exact_build_claim_matches(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        report = assess_target(root)
        self.assertEqual(report["status"], "not-supported")
        self.assertEqual(len(report["matching_claims"]), 1)
        self.assertFalse(report["errors"])

    def test_different_model_does_not_match(self):
        temp, root = self.make_root(matching=False)
        self.addCleanup(temp.cleanup)
        report = assess_target(root)
        self.assertEqual(report["status"], "unknown")
        self.assertEqual(len(report["matching_claims"]), 0)

    def test_conflicting_claims_are_flagged(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        path = root / "research" / "target_status.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["claims"].append({**data["claims"][0], "status": "experimental"})
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertEqual(assess_target(root)["status"], "conflicting-evidence")

    def test_report_warns_it_is_not_a_device_test(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        report_text = format_report(assess_target(root))
        self.assertIn("not a device test", report_text)
        self.assertIn("23G83", report_text)

    def test_verified_claim_requires_evidence_and_notes(self):
        temp, root = self.make_root(claim_status="verified")
        self.addCleanup(temp.cleanup)
        path = root / "research" / "target_status.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["claims"][0]["evidence_url"] = ""
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(assess_target(root)["errors"])

    def test_different_device_name_does_not_match_even_if_identifier_matches(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        path = root / "research" / "target_status.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["claims"][0]["device_model"] = "iPhone 16"
        path.write_text(json.dumps(data), encoding="utf-8")
        report = assess_target(root)
        self.assertEqual(report["status"], "unknown")
        self.assertEqual(len(report["matching_claims"]), 0)

    def test_malformed_https_evidence_url_is_rejected(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        path = root / "research" / "target_status.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["claims"][0]["evidence_url"] = "https://user:pass@example.com/evidence"
        path.write_text(json.dumps(data), encoding="utf-8")
        report = assess_target(root)
        self.assertEqual(report["status"], "unknown")
        self.assertTrue(any("HTTPS evidence URL" in error for error in report["errors"]))
    def test_malformed_https_port_is_rejected(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        path = root / "research" / "target_status.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["claims"][0]["evidence_url"] = "https://example.org:bad/evidence"
        path.write_text(json.dumps(data), encoding="utf-8")
        report = assess_target(root)
        self.assertEqual(report["status"], "unknown")
        self.assertTrue(any("HTTPS evidence URL" in error for error in report["errors"]))
    def test_null_target_fields_are_reported_as_missing(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        path = root / "research" / "target_profile.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["device_model"] = None
        path.write_text(json.dumps(data), encoding="utf-8")
        report = assess_target(root)
        self.assertTrue(any("device_model is missing" in error for error in report["errors"]))

    def test_null_claim_status_is_not_stringified(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        path = root / "research" / "target_status.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["claims"][0]["status"] = None
        path.write_text(json.dumps(data), encoding="utf-8")
        report = assess_target(root)
        self.assertEqual(report["status"], "unknown")
        self.assertTrue(any("invalid status" in error for error in report["errors"]))
    def test_malformed_status_claims_fail_closed(self):
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        path = root / "research" / "target_status.json"
        path.write_text(json.dumps({"claims": {}}), encoding="utf-8")
        report = assess_target(root)
        self.assertEqual(report["status"], "unknown")
        self.assertTrue(any("claims must be a list" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
