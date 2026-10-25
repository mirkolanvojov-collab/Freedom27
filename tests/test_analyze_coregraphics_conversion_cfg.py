import unittest

from research.scripts.analyze_coregraphics_conversion_cfg import analyze_function


class CoreGraphicsConversionCfgTests(unittest.TestCase):
    def test_nan_and_clamp_instructions_are_reported_as_dominators(self):
        records = [
            {"address": "0x1000", "instruction": "fcmp d0, d0"},
            {"address": "0x1004", "instruction": "b.vs loc_101c"},
            {"address": "0x1008", "instruction": "ldr d1, [x8, #0x6f8]"},
            {"address": "0x100c", "instruction": "fcmp d0, d1"},
            {"address": "0x1010", "instruction": "b.pl loc_1018"},
            {"address": "0x1014", "instruction": "b loc_1020"},
            {"address": "0x1018", "instruction": "fcvtzs w0, d0"},
            {"address": "0x101c", "instruction": "mov w0, #0"},
            {"address": "0x1020", "instruction": "ret"},
        ]
        report = analyze_function("_aa_moveto", "fixed", records)
        conversion = report["conversions"][0]
        self.assertTrue(conversion["structural_nan_guard_in_dominators"])
        self.assertTrue(conversion["structural_clamp_reference_in_dominators"])
        self.assertEqual(conversion["address"], "0x1018")
        self.assertEqual(report["unresolved_control_transfers"], [])

    def test_bypass_path_means_guard_does_not_dominate_conversion(self):
        records = [
            {"address": "0x2000", "instruction": "cbz w1, loc_2010"},
            {"address": "0x2004", "instruction": "fcmp d0, d0"},
            {"address": "0x2008", "instruction": "b.vs loc_2014"},
            {"address": "0x200c", "instruction": "nop"},
            {"address": "0x2010", "instruction": "fcvtzs w0, d0"},
            {"address": "0x2014", "instruction": "ret"},
        ]
        report = analyze_function("_aa_moveto", "target", records)
        conversion = report["conversions"][0]
        self.assertFalse(conversion["structural_nan_guard_in_dominators"])

    def test_unresolved_indirect_branch_is_reported(self):
        records = [
            {"address": "0x3000", "instruction": "br x9"},
            {"address": "0x3004", "instruction": "fcvtzs w0, d0"},
        ]
        report = analyze_function("_aa_lineto", "target", records)
        self.assertEqual(report["unresolved_control_transfers"][0]["reason"], "indirect control transfer")
        self.assertFalse(report["conversions"][0]["reachable_in_cfg"])


if __name__ == "__main__":
    unittest.main()
