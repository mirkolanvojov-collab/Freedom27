import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "research" / "scripts" / "capture_nvd_configurations.py"
SPEC = importlib.util.spec_from_file_location("capture_nvd_configurations", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NvdCaptureTests(unittest.TestCase):
    def test_import_does_not_create_output_or_make_requests(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "should-not-exist"
            self.assertFalse(output.exists())
            self.assertTrue(callable(MODULE.capture_records))
            self.assertFalse(output.exists())

    def test_capture_records_writes_summary_and_raw_responses(self):
        calls = []

        def fake_request(url, api_key):
            calls.append((url, api_key))
            return 200, {"totalResults": 1, "vulnerabilities": []}, None

        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "capture"
            summary = MODULE.capture_records(
                cve_ids=["CVE-2026-12345"],
                output_dir=out,
                api_key="test-key",
                request_json=fake_request,
                sleep=lambda _seconds: None,
            )
            self.assertEqual(len(calls), 2)
            self.assertTrue(all(key == "test-key" for _, key in calls))
            self.assertEqual(summary["successful_cve_records"], 1)
            self.assertEqual(summary["successful_cpe_match_records"], 1)
            self.assertEqual(summary["failed_record_count"], 0)
            self.assertTrue((out / "CVE-2026-12345_cves_2.0.json").exists())
            self.assertTrue((out / "CVE-2026-12345_cpematch_2.0.json").exists())
            self.assertTrue((out / "capture_summary.json").exists())

    def test_non_success_http_status_is_not_saved_as_success(self):
        with tempfile.TemporaryDirectory() as temp:
            summary = MODULE.capture_records(
                cve_ids=["CVE-2026-12345"],
                output_dir=Path(temp),
                request_json=lambda _url, _key: (429, {"error": "rate limited"}, None),
                sleep=lambda _seconds: None,
            )
            self.assertEqual(summary["successful_cve_records"], 0)
            self.assertEqual(summary["successful_cpe_match_records"], 0)
            self.assertEqual(summary["failed_record_count"], 1)

    def test_invalid_identifier_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                MODULE.capture_records(
                    cve_ids=["not-a-cve"],
                    output_dir=Path(temp),
                    request_json=lambda _url, _key: (200, {}, None),
                    sleep=lambda _seconds: None,
                )


if __name__ == "__main__":
    unittest.main()
