import json
import struct
import tempfile
import unittest
from pathlib import Path

from research.scripts.verify_coregraphics_constants import verify


class CoreGraphicsConstantVerificationTests(unittest.TestCase):
    def _fixture(self, root: Path, values: tuple[float, float]):
        binary = bytearray(0x200)
        struct.pack_into("<d", binary, 0x120, values[0])
        struct.pack_into("<d", binary, 0x128, values[1])
        binary_path = root / "CoreGraphics"
        binary_path.write_bytes(binary)
        load_commands = root / "load-commands.txt"
        load_commands.write_text("""Load command 0
      cmd LC_SEGMENT_64
   Section
     sectname __const
      segname __TEXT
         addr 0x1000
         size 0x100
       offset 256
""", encoding="utf-8")
        refs = []
        for operand, addr, offset in ((0x6F8, 0x1020, 0x20), (0x700, 0x1028, 0x28)):
            refs.append({"derived_references": [{
                "access_instruction": f"ldr d3, [x8, #{hex(operand)}]",
                "effective_address": hex(addr),
                "section_resolution": {
                    "classification": "inside_section",
                    "segment": "__TEXT",
                    "section": "__const",
                    "section_offset": hex(offset),
                },
            }]})
        diff = root / "function-diff.json"
        diff.write_text(json.dumps({"symbols": [{
            "symbol": "_aa_moveto",
            "fixed_relocation_sensitive_sites": refs,
        }]}), encoding="utf-8")
        return binary_path, load_commands, diff

    def test_reads_and_verifies_referenced_float64_constants(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = self._fixture(Path(directory), (-1073737729.0, 1073737729.0))
            report = verify(*paths)
            self.assertTrue(report["all_constants_match_expected"])
            self.assertEqual(report["unique_constants_checked"], 2)
            self.assertEqual(
                [row["actual_float64"] for row in report["constants"]],
                [-1073737729.0, 1073737729.0],
            )

    def test_reports_a_constant_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = self._fixture(Path(directory), (-1.0, 1.0))
            report = verify(*paths)
            self.assertFalse(report["all_constants_match_expected"])


if __name__ == "__main__":
    unittest.main()
