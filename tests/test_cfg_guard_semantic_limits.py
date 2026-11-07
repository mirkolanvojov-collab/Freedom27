"""Regression cases demonstrating limits of structural guard classification.

These are synthetic instruction sequences, not CoreGraphics execution.
"""
import unittest
from research.scripts.analyze_coregraphics_conversion_cfg import analyze_function


def site(lines):
    records = [{"address": f"0x{0x1000 + 4*i:x}", "instruction": s} for i, s in enumerate(lines)]
    return analyze_function("_aa_lineto", "fixed", records)["conversions"][0]


class StructuralGuardLimitTests(unittest.TestCase):
    def test_guarded_register_can_be_redefined_before_conversion(self):
        conversion = site([
            "fcmp d0, d0", "b.vs loc_1010",
            "fmov d0, d1", "fcvtzs w0, d0", "ret",
        ])
        # Structural cutset is positive, despite a new untested d0 definition.
        self.assertTrue(conversion["cfg_nan_guard_cutset_coverage"])

    def test_guard_can_check_different_register(self):
        conversion = site([
            "fcmp d1, d1", "b.vs loc_1010",
            "nop", "fcvtzs w0, d0", "ret",
        ])
        self.assertTrue(conversion["cfg_nan_guard_cutset_coverage"])

    def test_guard_does_not_prove_infinity_or_range_check(self):
        conversion = site([
            "fcmp d0, d0", "b.vs loc_1010",
            "nop", "fcvtzs w0, d0", "ret",
        ])
        self.assertTrue(conversion["cfg_nan_guard_cutset_coverage"])


if __name__ == "__main__":
    unittest.main()
