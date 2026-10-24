"""Offline tests for streamed IPSW digest verification."""
import hashlib
import io
import unittest

from research.scripts.verify_ipsw_stream import (
    digest_stream, stream_url_sha256, verify_stream,
)


class FakeResponse(io.BytesIO):
    def __init__(self, data, status, headers=None):
        super().__init__(data)
        self.status = status
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def getcode(self):
        return self.status


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

    def test_resume_uses_exact_range_and_produces_full_digest(self):
        data = b"abcdef"
        responses = [
            FakeResponse(b"abc", 200),
            FakeResponse(b"def", 206, {"Content-Range": "bytes 3-5/6"}),
        ]
        requests = []

        def opener(request, timeout):
            requests.append((request, timeout))
            return responses.pop(0)

        digest, size, status = stream_url_sha256(
            "https://example.invalid/test", len(data), opener=opener, sleep=lambda _: None
        )
        self.assertEqual(digest, hashlib.sha256(data).hexdigest())
        self.assertEqual(size, len(data))
        self.assertEqual(status, 206)
        self.assertEqual(requests[1][0].get_header("Range"), "bytes=3-")
        self.assertEqual(len(requests), 2)

    def test_resume_rejects_wrong_content_range(self):
        responses = [
            FakeResponse(b"abc", 200),
            FakeResponse(b"def", 206, {"Content-Range": "bytes 2-4/6"}),
        ]

        def opener(request, timeout):
            return responses.pop(0)

        with self.assertRaisesRegex(RuntimeError, "Unsafe/missing Content-Range"):
            stream_url_sha256(
                "https://example.invalid/test", 6, opener=opener,
                sleep=lambda _: None, max_retries=1,
            )

    def test_resume_rejects_wrong_total_in_content_range(self):
        responses = [
            FakeResponse(b"abc", 200),
            FakeResponse(b"def", 206, {"Content-Range": "bytes 3-5/7"}),
        ]

        def opener(request, timeout):
            return responses.pop(0)

        with self.assertRaisesRegex(RuntimeError, "Unsafe/missing Content-Range"):
            stream_url_sha256(
                "https://example.invalid/test", 6, opener=opener,
                sleep=lambda _: None, max_retries=1,
            )

    def test_rejects_non_numeric_content_length(self):
        responses = [FakeResponse(b"abcdef", 200, {"Content-Length": "six"})]

        def opener(request, timeout):
            return responses.pop(0)

        with self.assertRaisesRegex(RuntimeError, "Invalid Content-Length"):
            stream_url_sha256(
                "https://example.invalid/test", 6, opener=opener,
                sleep=lambda _: None, max_retries=1,
            )

    def test_rejects_full_response_with_wrong_content_length(self):
        responses = [FakeResponse(b"abcdef", 200, {"Content-Length": "7"})]

        def opener(request, timeout):
            return responses.pop(0)

        with self.assertRaisesRegex(RuntimeError, "Content-Length does not match pinned size"):
            stream_url_sha256(
                "https://example.invalid/test", 6, opener=opener,
                sleep=lambda _: None, max_retries=1,
            )

    def test_rejects_extra_bytes_after_pinned_full_response(self):
        responses = [FakeResponse(b"abcdefX", 200)]

        def opener(request, timeout):
            return responses.pop(0)

        with self.assertRaisesRegex(RuntimeError, "exceeded pinned size"):
            stream_url_sha256(
                "https://example.invalid/test", 6, opener=opener,
                sleep=lambda _: None, max_retries=1,
            )

    def test_rejects_content_length_inconsistent_with_content_range(self):
        responses = [
            FakeResponse(b"abc", 200),
            FakeResponse(
                b"defx", 206,
                {"Content-Range": "bytes 3-5/6", "Content-Length": "4"},
            ),
        ]

        def opener(request, timeout):
            return responses.pop(0)

        with self.assertRaisesRegex(RuntimeError, "Content-Length does not match"):
            stream_url_sha256(
                "https://example.invalid/test", 6, opener=opener,
                sleep=lambda _: None, max_retries=1,
            )

    def test_rejects_invalid_expected_size_and_retry_count(self):
        with self.assertRaises(ValueError):
            stream_url_sha256("https://example.invalid/test", 0)
        with self.assertRaises(ValueError):
            stream_url_sha256("https://example.invalid/test", 6, max_retries=-1)

    def test_interrupted_read_resumes_from_bytes_already_hashed(self):
        class InterruptedResponse(FakeResponse):
            def __init__(self):
                super().__init__(b"abc", 200)
                self.read_calls = 0

            def read(self, size=-1):
                self.read_calls += 1
                if self.read_calls == 1:
                    return super().read(size)
                raise ConnectionResetError("synthetic interrupted stream")

        responses = [
            InterruptedResponse(),
            FakeResponse(b"def", 206, {"Content-Range": "bytes 3-5/6"}),
        ]
        requests = []

        def opener(request, timeout):
            requests.append(request)
            return responses.pop(0)

        digest, size, status = stream_url_sha256(
            "https://example.invalid/test", 6, opener=opener,
            sleep=lambda _: None, max_retries=2,
        )
        self.assertEqual(digest, hashlib.sha256(b"abcdef").hexdigest())
        self.assertEqual(size, 6)
        self.assertEqual(status, 206)
        self.assertEqual(requests[1].get_header("Range"), "bytes=3-")


if __name__ == "__main__":
    unittest.main()
