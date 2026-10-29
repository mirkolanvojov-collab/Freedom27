import struct
import tempfile
import unittest
from pathlib import Path

from research.scripts.compare_coordinate_safety_limit import compare


class CoordinateSafetyLimitTests(unittest.TestCase):
    def _fixture(self, root: Path, name: str, value: float, section_address: int, file_offset: int):
        blob = bytearray(0x300)
        struct.pack_into("<d", blob, file_offset + 0x5A28 if file_offset + 0x5A28 + 8 <= len(blob) else 0x120, value)
        # Use a small fixture-friendly section-relative offset by translating the
        # production offset to the section start and allocating enough bytes.
        section_size = 0x5A28 + 8
        actual_file_offset = 0x100
        blob = bytearray(actual_file_offset + section_size + 0x20)
        struct.pack_into("<d", blob, actual_file_offset + 0x5A28, value)
        binary = root / name
        binary.write_bytes(blob)
        load = root / f"{name}.load"
        load.write_text(f"""Load command 0
      cmd LC_SEGMENT_64
   Section
     sectname __const
      segname __TEXT
         addr {hex(section_address)}
         size {hex(section_size)}
       offset {actual_file_offset}
""", encoding="utf-8")
        return binary, load

    def test_reports_raw_bytes_and_equal_value(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self._fixture(root, "target", 4096.0, 0x100000, 0x100)
            fixed = self._fixture(root, "fixed", 4096.0, 0x200000, 0x100)
            report = compare(*target, *fixed)
            self.assertTrue(report["raw_bytes_equal"])
            self.assertEqual(report["target"]["raw_bytes_little_endian"], struct.pack("<d", 4096.0).hex())
            self.assertEqual(report["fixed_reference"]["float64_little_endian"], 4096.0)

    def test_reports_different_bytes_without_asserting_expected_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self._fixture(root, "target", 4096.0, 0x100000, 0x100)
            fixed = self._fixture(root, "fixed", 8192.0, 0x200000, 0x100)
            report = compare(*target, *fixed)
            self.assertFalse(report["raw_bytes_equal"])

    def test_rejects_section_too_small(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / "binary"
            binary.write_bytes(bytes(0x400))
            load = root / "load"
            load.write_text("""Load command 0
      cmd LC_SEGMENT_64
   Section
     sectname __const
      segname __TEXT
         addr 0x1000
         size 0x100
       offset 256
""", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "outside __TEXT,__const"):
                compare(binary, load, binary, load)


if __name__ == "__main__":
    unittest.main()
