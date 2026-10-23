import unittest

from Framework.ios_security_audit import build_audit


TARGET = {
    "device_model": "iPhone 16 Plus",
    "model_identifier": "iPhone17,4",
    "exact_os_version": "iOS 26.6.1",
    "build_number": "23G83",
}


class IOSSecurityAuditTests(unittest.TestCase):
    def test_report_is_read_only_and_covers_controls(self):
        report = build_audit(TARGET)
        self.assertEqual(report["mode"], "read_only_defensive_audit")
        self.assertFalse(report["device_modified"])
        self.assertFalse(report["bypass_attempted"])
        self.assertGreaterEqual(report["controls_reviewed"], 8)

    def test_unknown_status_fails_closed(self):
        report = build_audit(TARGET, {"sandbox": "bypassed"})
        sandbox = next(c for c in report["controls"] if c["control"] == "sandbox")
        self.assertEqual(sandbox["status"], "invalid_status")

    def test_malformed_status_fails_closed_without_crashing(self):
        report = build_audit(TARGET, {"sandbox": ["reviewed"]})
        sandbox = next(c for c in report["controls"] if c["control"] == "sandbox")
        self.assertEqual(sandbox["status"], "invalid_status")

    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):
            build_audit([])


if __name__ == "__main__":
    unittest.main()
