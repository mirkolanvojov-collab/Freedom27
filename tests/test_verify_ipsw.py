"""Offline tests for the pinned IPSW integrity verifier."""
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from research.scripts.verify_ipsw import TARGET_FILENAME, verify_ipsw


class VerifyIpswTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.payload = b"small synthetic test payload; not firmware"
        self.path = self.root / TARGET_FILENAME
        self.path.write_bytes(self.payload)
        self.digest = hashlib.sha256(self.payload).hexdigest()

    def test_accepts_matching_filename_size_and_hash(self):
        result = verify_ipsw(self.path, expected_sha256=self.digest, expected_size=len(self.payload))
        self.assertTrue(result["verified"])
        self.assertTrue(result["sha256_matches"])
        self.assertFalse(result["device_modified"])
        self.assertFalse(result["download_performed"])

    def test_rejects_hash_mismatch(self):
        result = verify_ipsw(self.path, expected_sha256="0" * 64, expected_size=len(self.payload))
        self.assertFalse(result["verified"])
        self.assertFalse(result["sha256_matches"])

    def test_rejects_size_mismatch(self):
        result = verify_ipsw(self.path, expected_sha256=self.digest, expected_size=len(self.payload) + 1)
        self.assertFalse(result["verified"])
        self.assertFalse(result["size_matches"])

    def test_rejects_wrong_filename_even_when_hash_matches(self):
        other = self.root / "wrong.ipsw"
        other.write_bytes(self.payload)
        result = verify_ipsw(other, expected_sha256=self.digest, expected_size=len(self.payload))
        self.assertFalse(result["verified"])
        self.assertFalse(result["filename_matches"])

    def test_optional_zip_crc_validation(self):
        with zipfile.ZipFile(self.path, "w") as archive:
            archive.writestr("manifest.txt", "synthetic test")
        digest = hashlib.sha256(self.path.read_bytes()).hexdigest()
        result = verify_ipsw(self.path, expected_sha256=digest, expected_size=self.path.stat().st_size, check_zip=True)
        self.assertTrue(result["verified"])
        self.assertTrue(result["zip_crc_check_passed"])


if __name__ == "__main__":
    unittest.main()
