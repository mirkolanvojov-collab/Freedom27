import unittest
from pathlib import Path
from unittest.mock import patch

from research.scripts.compare_coregraphics_functions import (
    digest_instructions,
    disassemble,
    normalize_disassembly,
)


class CoreGraphicsFunctionComparisonTests(unittest.TestCase):
    def test_normalizes_addresses_but_preserves_bounds_constants(self):
        output = """
0x1000: 1f 20 03 d5 nop
0x1004: 00 00 00 14 b #0x1010
0x1008: mov x0, #0x3ffff001
"""
        self.assertEqual(
            normalize_disassembly(output),
            ["nop", "b <branch-target>", "mov x0, #0x3ffff001"],
        )

    def test_normalizes_branch_addresses_across_builds(self):
        first = normalize_disassembly("0x1000: bl #0x1010\n0x1004: ret")
        second = normalize_disassembly("0x2000: bl #0x2020\n0x2004: ret")
        self.assertEqual(first, second)


    def test_disassembler_uses_supported_count_flag(self):
        from research.scripts import compare_coregraphics_functions as module
        with patch.object(module, "run", return_value="0x1000: ret") as mocked:
            result = disassemble(Path("CoreGraphics"), "_aa_render", 600)
        self.assertEqual(result, ["ret"])
        args = mocked.call_args.args[0]
        self.assertIn("--count", args)
        self.assertIn("--force", args)
        self.assertNotIn("--instrs", args)

    def test_disassembler_fails_closed_on_empty_output(self):
        from research.scripts import compare_coregraphics_functions as module
        with patch.object(module, "run", return_value=""):
            with self.assertRaisesRegex(RuntimeError, "no parseable instructions"):
                disassemble(Path("CoreGraphics"), "_aa_render", 600)

    def test_digest_is_stable_and_order_sensitive(self):
        self.assertEqual(
            digest_instructions(["cmp x0, #1", "ret"]),
            digest_instructions(["cmp x0, #1", "ret"]),
        )
        self.assertNotEqual(
            digest_instructions(["cmp x0, #1", "ret"]),
            digest_instructions(["ret", "cmp x0, #1"]),
        )


if __name__ == "__main__":
    unittest.main()
