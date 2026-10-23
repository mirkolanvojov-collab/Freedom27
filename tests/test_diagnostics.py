import unittest

from Framework.diagnostics import collect_diagnostics, format_diagnostics


class DiagnosticsTests(unittest.TestCase):
    def test_report_is_read_only_and_does_not_claim_jailbreak(self):
        report = collect_diagnostics()
        self.assertEqual(report["project"], "Freedom27")
        self.assertFalse(report["device_modification_attempted"])
        self.assertFalse(report["jailbreak_verified"])

    def test_report_formats_as_text(self):
        rendered = format_diagnostics({"a": 1, "b": True})
        self.assertEqual(rendered, "a: 1\nb: True")


if __name__ == "__main__":
    unittest.main()
