"""Tests for the local IPSW checksum verifier; no firmware download required."""
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "research" / "scripts" / "verify_ipsw_sha256.py"
SPEC = importlib.util.spec_from_file_location("verify_ipsw_sha256", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class VerifyIpswSha256Tests(unittest.TestCase):
    def test_hashes_in_chunks_and_accepts_matching_digest(self):
        payload = b"Freedom27 checksum test fixture\x00" * 1000
        expected = hashlib.sha256(payload).hexdigest()
        old = MODULE.TARGET["expected_sha256"]
        try:
            MODULE.TARGET["expected_sha256"] = expected
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "fixture.ipsw"
                path.write_bytes(payload)
                result = MODULE.verify(path)
            self.assertTrue(result["verified"])
            self.assertEqual(result["actual_sha256"], expected)
            self.assertEqual(result["size_bytes"], len(payload))
        finally:
            MODULE.TARGET["expected_sha256"] = old

    def test_rejects_mismatching_digest(self):
        old = MODULE.TARGET["expected_sha256"]
        try:
            MODULE.TARGET["expected_sha256"] = "0" * 64
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "fixture.ipsw"
                path.write_bytes(b"not the expected firmware")
                result = MODULE.verify(path)
            self.assertFalse(result["verified"])
            self.assertIn("SHA-256 mismatch", result["error"])
        finally:
            MODULE.TARGET["expected_sha256"] = old

    def test_missing_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            result = MODULE.verify(Path(directory) / "missing.ipsw")
        self.assertFalse(result["verified"])
        self.assertIn("not a regular file", result["error"])


if __name__ == "__main__":
    unittest.main()
