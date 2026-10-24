"""Offline tests for streamed IPSW digest verification."""
import hashlib
import io
import unittest

from research.scripts.verify_ipsw_stream import digest_stream, verify_stream


class VerifyIpswStreamTests(unittest.TestCase):
    def test_stream_hash_and_byte_count(self):
        data = b"synthetic firmware stream"
        digest, size = digest_stream(io.BytesIO(data), chunk_size=4)
        self.assertEqual(digest, hashlib.sha256(data).hexdigest())
        self.assertEqual(size, len(data))

    def test_expected_digest_and_size_pass(self):
        data = b"synthetic firmware stream"
        result = verify_stream(io.BytesIO(data), hashlib.sha256(data).hexdigest(), len(data))
        self.assertTrue(result["verified"])
        self.assertFalse(result["file_written_to_disk"])
        self.assertFalse(result["device_modified"])

    def test_wrong_digest_or_size_fails_closed(self):
        data = b"synthetic firmware stream"
        result = verify_stream(io.BytesIO(data), "0" * 64, len(data) + 1)
        self.assertFalse(result["verified"])
        self.assertFalse(result["sha256_matches"])
        self.assertFalse(result["size_matches"])


if __name__ == "__main__":
    unittest.main()
