import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from research.scripts.compare_coregraphics import binary_record, compare, find_coregraphics, sha256_file


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

    @patch("research.scripts.compare_coregraphics.extract")
    def test_compare_records_explicit_build_and_device_labels(self, mocked_extract):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target_cache = root / "target-cache"
            fixed_cache = root / "fixed-cache"
            target_cache.write_bytes(b"cache")
            fixed_cache.write_bytes(b"cache")
            target_binary = root / "target-CoreGraphics"
            fixed_binary = root / "fixed-CoreGraphics"
            target_binary.write_bytes(b"target")
            fixed_binary.write_bytes(b"fixed")
            mocked_extract.side_effect = [target_binary, fixed_binary]
            output = root / "comparison.json"

            report = compare(
                target_cache, fixed_cache, output,
                target_build="23H24", fixed_build="23H30",
                target_device="iPhone17,4", fixed_device="iPhone17,4",
            )

            self.assertEqual(report["target"]["build"], "23H24")
            self.assertEqual(report["fixed_reference"]["build"], "23H30")
            self.assertEqual(report["target"]["device"], "iPhone17,4")
            self.assertEqual(report["fixed_reference"]["device"], "iPhone17,4")
            self.assertTrue(output.is_file())

    def test_binary_record_reports_size_and_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CoreGraphics"
            path.write_bytes(b"abc")
            record = binary_record(path)
            self.assertEqual(record["size_bytes"], 3)
            self.assertEqual(record["sha256"], "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")


if __name__ == "__main__":
    unittest.main()
