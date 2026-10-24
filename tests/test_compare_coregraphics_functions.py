import unittest
from pathlib import Path
from unittest.mock import patch

from research.scripts.compare_coregraphics_functions import (
    digest_instructions,
    disassemble,
    normalize_disassembly,
)


class CoreGraphicsFunctionComparisonTests(unittest.TestCase):
    def test_discovery_ignores_zero_address_unresolved_symbols(self):
        from research.scripts import compare_coregraphics_functions as module
        output = """SYMBOLS
0x00001000: S _aa_render
0x00000000: U _aa_path_iterator_create"""
        with patch.object(module, "run", return_value=output):
            self.assertEqual(module.discover_symbols(Path("CoreGraphics")), ["_aa_render"])

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


    def test_disassembler_uses_function_boundaries_not_fixed_count(self):
        from research.scripts import compare_coregraphics_functions as module
        with patch.object(module, "run", return_value="0x1000: ret") as mocked:
            result = disassemble(Path("CoreGraphics"), "_aa_render")
        self.assertEqual(result, ["ret"])
        args = mocked.call_args.args[0]
        self.assertIn("--force", args)
        self.assertIn("--symbol", args)
        self.assertNotIn("--count", args)
        self.assertNotIn("--instrs", args)

    def test_disassembler_retries_leading_underscore_for_missing_symbol(self):
        from research.scripts import compare_coregraphics_functions as module
        with patch.object(
            module, "run",
            side_effect=[
                RuntimeError("command failed: symbol not found in macho symtab"),
                "0x1000: ret",
            ],
        ) as mocked:
            result = disassemble(Path("CoreGraphics"), "aa_path_iterator_create")
        self.assertEqual(result, ["ret"])
        self.assertEqual(mocked.call_count, 2)
        self.assertIn("aa_path_iterator_create", mocked.call_args_list[0].args[0])
        self.assertIn("_aa_path_iterator_create", mocked.call_args_list[1].args[0])

    def test_disassembler_rejects_ipsw_100_instruction_fallback(self):
        from research.scripts import compare_coregraphics_functions as module
        output = "WARN disassembling 100 instructions at 0x1000\\n0x1000: ret"
        with patch.object(module, "run", return_value=output):
            with self.assertRaisesRegex(RuntimeError, "function boundary"):
                disassemble(Path("CoreGraphics"), "_aa_render")

    def test_disassembler_fails_closed_on_empty_output(self):
        from research.scripts import compare_coregraphics_functions as module
        with patch.object(module, "run", return_value=""):
            with self.assertRaisesRegex(RuntimeError, "no parseable instructions"):
                disassemble(Path("CoreGraphics"), "_aa_render")

    def test_main_fails_closed_on_partial_comparison(self):
        import tempfile
        import sys
        from research.scripts import compare_coregraphics_functions as module

        report = {
            "common_aa_symbol_count": 28,
            "successfully_compared_symbol_count": 27,
            "changed_symbol_count": 2,
            "changed_symbols": ["_aa_one", "_aa_two"],
            "disassembly_failures": [{"symbol": "_aa_failed", "error": "tool error"}],
            "symbols": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            with patch.object(module, "compare", return_value=report), patch.object(
                sys, "argv",
                ["compare_coregraphics_functions.py", "--target-binary", "target",
                 "--fixed-binary", "fixed", "--output", str(output)],
            ):
                self.assertEqual(module.main(), 4)
            self.assertTrue(output.is_file())

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
