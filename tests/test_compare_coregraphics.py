import tempfile
import unittest
from pathlib import Path

from research.scripts.compare_coregraphics import binary_record, find_coregraphics, sha256_file


class CoreGraphicsComparisonToolTests(unittest.TestCase):
    def test_sha256_is_stable_and_known(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CoreGraphics"
            path.write_bytes(b"test-binary")
            self.assertEqual(
                sha256_file(path),
                "6f850b10b66ff0af26a1151306cbc59427ae2572330935d95ab5febdef8763bf",
            )

    def test_find_coregraphics_requires_one_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CoreGraphics").write_bytes(b"binary")
            self.assertEqual(find_coregraphics(root), root / "CoreGraphics")
            (root / "nested").mkdir()
            (root / "nested" / "CoreGraphics").write_bytes(b"binary")
            with self.assertRaises(RuntimeError):
                find_coregraphics(root)

    def test_binary_record_reports_size_and_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CoreGraphics"
            path.write_bytes(b"abc")
            record = binary_record(path)
            self.assertEqual(record["size_bytes"], 3)
            self.assertEqual(record["sha256"], "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")


if __name__ == "__main__":
    unittest.main()
