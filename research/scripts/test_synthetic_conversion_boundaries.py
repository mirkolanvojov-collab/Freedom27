#!/usr/bin/env python3
"""Synthetic numerical boundary checks; no CoreGraphics execution or exploit inputs."""
from __future__ import annotations

import math
import unittest

I32_MIN = -(1 << 31)
I32_MAX = (1 << 31) - 1


def classify_float_to_i32(value: float) -> str:
    """Classify input-domain preconditions; do not emulate ARM FCVTZS semantics."""
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "infinite"
    if value < I32_MIN or value >= I32_MAX + 1:
        return "out_of_range"
    return "in_range"


def narrow_u64_to_u32(value: int) -> int:
    """Mathematical low-32-bit extraction, not a CoreGraphics execution."""
    if not 0 <= value < (1 << 64):
        raise ValueError("expected unsigned 64-bit input")
    return value & 0xFFFFFFFF


class BoundaryModelTests(unittest.TestCase):
    def test_nonfinite_classification(self):
        self.assertEqual(classify_float_to_i32(float("nan")), "nan")
        self.assertEqual(classify_float_to_i32(float("inf")), "infinite")
        self.assertEqual(classify_float_to_i32(float("-inf")), "infinite")

    def test_signed_integer_boundaries(self):
        for value in (float(I32_MIN), -1.0, 0.0, float(I32_MAX)):
            self.assertEqual(classify_float_to_i32(value), "in_range")
        for value in (float(I32_MIN) - 1, float(I32_MAX) + 1):
            self.assertEqual(classify_float_to_i32(value), "out_of_range")

    def test_fractional_truncation_domain(self):
        self.assertEqual(classify_float_to_i32(-0.75), "in_range")
        self.assertEqual(classify_float_to_i32(0.75), "in_range")

    def test_narrowing_discards_high_bits(self):
        self.assertEqual(narrow_u64_to_u32(0x100000001), 1)
        self.assertEqual(narrow_u64_to_u32(0xFFFFFFFFFFFFFFFF), 0xFFFFFFFF)
        self.assertEqual(narrow_u64_to_u32(0), 0)

    def test_narrowing_rejects_invalid_domain(self):
        for value in (-1, 1 << 64):
            with self.assertRaises(ValueError):
                narrow_u64_to_u32(value)


if __name__ == "__main__":
    unittest.main()
