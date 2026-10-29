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

    def test_vector_fcvtzs_followed_by_xtn_reports_narrowing(self):
        records = [
            {"address": "0x3500", "instruction": "fmla v0.2d, v17.2d, v1.2d"},
            {"address": "0x3504", "instruction": "fcvtzs v0.2d, v0.2d"},
            {"address": "0x3508", "instruction": "xtn v0.2s, v0.2d"},
            {"address": "0x350c", "instruction": "str d0, [sp, #0x38]"},
            {"address": "0x3510", "instruction": "ret"},
        ]
        conversion = analyze_function("_aa_lineto", "target", records)["conversions"][0]
        self.assertTrue(conversion["followed_by_same_register_xtn_2d_to_2s"])
        self.assertEqual(conversion["narrowing_address"], "0x3508")
        self.assertIn("low 32 bits", conversion["narrowing_semantics_note"])

    def test_scalar_conversion_is_not_misclassified_as_vector_narrowing(self):
        records = [
            {"address": "0x3600", "instruction": "fcvtzs w9, d1"},
            {"address": "0x3604", "instruction": "csel w8, w8, w9, gt"},
            {"address": "0x3608", "instruction": "ret"},
        ]
        conversion = analyze_function("_aa_lineto", "fixed", records)["conversions"][0]
        self.assertFalse(conversion["followed_by_same_register_xtn_2d_to_2s"])
        self.assertIsNone(conversion["narrowing_address"])

    def test_unresolved_indirect_branch_is_reported(self):
        records = [
            {"address": "0x3000", "instruction": "br x9"},
            {"address": "0x3004", "instruction": "fcvtzs w0, d0"},
        ]
        report = analyze_function("_aa_lineto", "target", records)
        self.assertEqual(report["unresolved_control_transfers"][0]["reason"], "indirect control transfer")
        self.assertFalse(report["conversions"][0]["reachable_in_cfg"])


    def test_path_guard_coverage_when_all_paths_pass_guard(self):
        records = [
            {"address": "0x4000", "instruction": "fcmp d0, d0"},
            {"address": "0x4004", "instruction": "b.vs loc_4010"},
            {"address": "0x4008", "instruction": "fcvtzs w0, d0"},
            {"address": "0x400c", "instruction": "ret"},
            {"address": "0x4010", "instruction": "mov w0, #0"},
            {"address": "0x4014", "instruction": "ret"},
        ]
        conversion = analyze_function("_aa_moveto", "fixed", records)["conversions"][0]
        self.assertTrue(conversion["cfg_nan_guard_cutset_coverage"])
        self.assertEqual(conversion["cfg_nan_guard_branches"][0]["address"], "0x4004")

    def test_path_guard_coverage_false_when_entry_bypasses_guard(self):
        records = [
            {"address": "0x5000", "instruction": "cbz w1, loc_500c"},
            {"address": "0x5004", "instruction": "fcmp d0, d0"},
            {"address": "0x5008", "instruction": "b.vs loc_5014"},
            {"address": "0x500c", "instruction": "fcvtzs w0, d0"},
            {"address": "0x5010", "instruction": "ret"},
            {"address": "0x5014", "instruction": "mov w0, #0"},
            {"address": "0x5018", "instruction": "ret"},
        ]
        conversion = analyze_function("_aa_moveto", "target", records)["conversions"][0]
        self.assertFalse(conversion["cfg_nan_guard_cutset_coverage"])



    def test_bvc_nan_fallthrough_guard(self):
        records = [
            {"address": "0x6000", "instruction": "fcmp d4, d4"},
            {"address": "0x6004", "instruction": "b.vc loc_6010"},
            {"address": "0x6008", "instruction": "mov w10, #0"},
            {"address": "0x600c", "instruction": "ret"},
            {"address": "0x6010", "instruction": "fcvtzs w10, d4"},
            {"address": "0x6014", "instruction": "ret"},
        ]
        conversion = analyze_function("_aa_clip_edge", "fixed", records)["conversions"][0]
        self.assertTrue(conversion["cfg_nan_guard_cutset_coverage"])
        self.assertEqual(conversion["cfg_nan_guard_branches"][0]["address"], "0x6004")


    def test_bal_is_unconditional_branch_without_fallthrough(self):
        records = [
            {"address": "0x7000", "instruction": "b.al loc_7008"},
            {"address": "0x7004", "instruction": "fcvtzs w0, d0"},
            {"address": "0x7008", "instruction": "ret"},
        ]
        report = analyze_function("_aa_moveto", "target", records)
        self.assertFalse(report["conversions"][0]["reachable_in_cfg"])
        self.assertEqual(report["unresolved_control_transfers"], [])


    def test_retaa_is_a_terminal_return(self):
        records = [
            {"address": "0x8000", "instruction": "retaa"},
            {"address": "0x8004", "instruction": "fcvtzs w0, d0"},
        ]
        report = analyze_function("_aa_moveto", "target", records)
        self.assertFalse(report["conversions"][0]["reachable_in_cfg"])
        self.assertEqual(report["unresolved_control_transfers"], [])

if __name__ == "__main__":
    unittest.main()
