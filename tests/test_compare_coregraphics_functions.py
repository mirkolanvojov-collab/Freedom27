import unittest
from pathlib import Path
from unittest.mock import patch

from research.scripts.compare_coregraphics_functions import (
    digest_instructions,
    disassemble,
    extract_relocation_sites,
    normalize_disassembly,
)


class CoreGraphicsFunctionComparisonTests(unittest.TestCase):
    def test_discovery_keeps_only_executable_text_symbols(self):
        from research.scripts import compare_coregraphics_functions as module
        output = """SYMBOLS
0x00001000: (__TEXT,__text) private _aa_render
0x00001040: (__TEXT,__text) private _aa_path_iterate
0x00002000: (__TEXT,__const) private _aa_gray_levels
0x00002040: (__TEXT,__const) private _aa_mono_levels
0x00003000: (__AUTH_CONST,__const) private aa_path_iterator_create.callbacks
0x00000000: U _aa_unresolved"""
        with patch.object(module, "run", return_value=output):
            self.assertEqual(
                module.discover_symbols(Path("CoreGraphics")),
                ["_aa_path_iterate", "_aa_render"],
            )

    def test_parses_and_classifies_macho_sections(self):
        output = """Load command 0
      cmd LC_SEGMENT_64
   Section
     sectname __const
      segname __TEXT
         addr 0x1847c1200
         size 0x00001000
   Section
     sectname __text
      segname __TEXT
         addr 0x1847c0000
         size 0x00001000
"""
        sections = parse_macho_sections(output)
        self.assertEqual(len(sections), 2)
        self.assertEqual(classify_address(0x1847c1720, sections),
                         {"classification": "inside_section", "segment": "__TEXT",
                          "section": "__const", "section_offset": "0x520"})
        self.assertEqual(classify_address(0x1e5d9ec30, sections),
                         {"classification": "outside_listed_sections"})

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

    def test_relocation_audit_preserves_raw_addresses_and_nearby_instructions(self):
        output = (
            "0x1000: 09 00 00 90 adrp x9, 0x180000000\n"
            "0x1004: 29 01 40 f9 ldr x9, [x9, #0x20]\n"
            "0x1008: 20 01 3f d6 blr x9\n"
            "0x100c: c0 03 5f d6 ret\n"
        )
        sites = extract_relocation_sites(output)
        self.assertEqual(len(sites), 1)
        self.assertEqual(sites[0]["address"], "0x1000")
        self.assertEqual(sites[0]["instruction"], "adrp x9, 0x180000000")
        self.assertEqual(sites[0]["context"][1]["instruction"], "ldr x9, [x9, #0x20]")
        self.assertEqual(
            sites[0]["derived_references"],
            [{
                "access_address": "0x1004",
                "access_instruction": "ldr x9, [x9, #0x20]",
                "base_page_address": "0x180000000",
                "offset": "0x20",
                "effective_address": "0x180000020",
                "derivation": "ADRP page target + explicit memory operand offset",
            }],
        )

    def test_normalizes_layout_addresses_and_comments(self):
        first = normalize_disassembly(
            "0x1000: adrp x9, 0x1847c2000\n"
            "0x1004: b.eq loc_18430e230 ; ⤵ <branch-target>\n"
        )
        second = normalize_disassembly(
            "0x2000: adrp x9, 0x1847e9000\n"
            "0x2004: b.eq loc_1843353d8 ; ⤵ <branch-target>\n"
        )
        self.assertEqual(first, second)
        self.assertEqual(first[0], "adrp x9, <image-address>")
        self.assertEqual(first[1], "b.eq <local-label>")

    def test_preserves_non_address_immediates(self):
        output = "0x1000: mov x13, #0xfff800000000\n"
        self.assertEqual(
            normalize_disassembly(output),
            ["mov x13, #0xfff800000000"],
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
        output = "WARN disassembling 100 instructions at 0x1000\n0x1000: ret"
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

    def test_main_fails_closed_when_no_shared_symbols_exist(self):
        import tempfile
        import sys
        from research.scripts import compare_coregraphics_functions as module

        report = {
            "common_aa_symbol_count": 0,
            "successfully_compared_symbol_count": 0,
            "changed_symbol_count": 0,
            "changed_symbols": [],
            "disassembly_failures": [],
            "symbols": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            with patch.object(module, "compare", return_value=report), patch.object(
                sys, "argv",
                ["compare_coregraphics_functions.py", "--target-binary", "target",
                 "--fixed-binary", "fixed", "--output", str(output)],
            ):
                self.assertEqual(module.main(), 3)
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
