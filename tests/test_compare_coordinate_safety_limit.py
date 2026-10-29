import struct
import tempfile
import unittest
from pathlib import Path

from research.scripts.compare_coordinate_safety_limit import compare


class CoordinateSafetyLimitTests(unittest.TestCase):
    def _fixture(self, root: Path, name: str, value: float, section_address: int, file_offset: int):
        # Allocate enough bytes for the production section-relative offset.
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

    def test_resolves_actual_function_load_address_in_each_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self._fixture(root, "target", 4096.0, 0x100000, 0x100)
            fixed = self._fixture(root, "fixed", 8192.0, 0x200000, 0x100)
            # Place the semantic constants at different offsets and verify that
            # disassembly-derived addresses, not the legacy offset, are read.
            target_binary, target_load = target
            fixed_binary, fixed_load = fixed
            target_blob = bytearray(target_binary.read_bytes())
            fixed_blob = bytearray(fixed_binary.read_bytes())
            struct.pack_into("<d", target_blob, 0x100 + 0x80, 123456.0)
            struct.pack_into("<d", fixed_blob, 0x100 + 0x90, 123456.0)
            target_binary.write_bytes(target_blob)
            fixed_binary.write_bytes(fixed_blob)
            target_dis = root / "target.dis"
            fixed_dis = root / "fixed.dis"
            target_dis.write_text(
                "0x1000: adrp x8, 0x100000\n0x1004: ldr d4, [x8, #0x80]\n",
                encoding="utf-8",
            )
            fixed_dis.write_text(
                "0x2000: adrp x8, 0x200000\n0x2004: ldr d4, [x8, #0x90]\n",
                encoding="utf-8",
            )
            report = compare(target_binary, target_load, fixed_binary, fixed_load,
                             target_dis, fixed_dis)
            self.assertTrue(report["raw_bytes_equal"])
            self.assertEqual(report["comparison_basis"], "resolved_load_addresses")
            self.assertEqual(report["target"]["section_relative_offset"], "0x80")
            self.assertEqual(report["fixed_reference"]["section_relative_offset"], "0x90")
            self.assertEqual(report["target"]["float64_little_endian"], 123456.0)


if __name__ == "__main__":
    unittest.main()
