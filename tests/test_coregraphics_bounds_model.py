import math
import unittest

from research.scripts.model_coregraphics_coordinate_bounds import (
    INT32_MAX,
    INT32_MIN,
    SAFE_LIMIT,
    checked_span,
    safe_fixed_coordinate,
)


class CoreGraphicsBoundsModelTests(unittest.TestCase):
    def test_non_finite_coordinates_are_handled_before_narrowing(self):
        self.assertEqual(safe_fixed_coordinate(float("nan")), 0)
        self.assertEqual(safe_fixed_coordinate(float("inf")), 0)
        self.assertEqual(safe_fixed_coordinate(float("-inf")), 0)

    def test_coordinate_conversion_rejects_boolean_and_nonnumeric_inputs(self):
        with self.assertRaises(TypeError):
            safe_fixed_coordinate(True)
        with self.assertRaises(TypeError):
            safe_fixed_coordinate("1.0")
    def test_coordinate_conversion_clamps_both_extremes(self):
        self.assertEqual(safe_fixed_coordinate(1e100), SAFE_LIMIT)
        self.assertEqual(safe_fixed_coordinate(-1e100), -SAFE_LIMIT)
        self.assertEqual(safe_fixed_coordinate(1e308), SAFE_LIMIT)
        self.assertEqual(safe_fixed_coordinate(-1e308), -SAFE_LIMIT)

    def test_normal_coordinates_convert_to_fixed_point(self):
        self.assertEqual(safe_fixed_coordinate(0.0), 0)
        self.assertEqual(safe_fixed_coordinate(1.0), 4096)
        self.assertEqual(safe_fixed_coordinate(-1.0), -4095)

    def test_checked_span_accepts_safe_interval(self):
        self.assertEqual(checked_span(100, 20), (100, 120))

    def test_checked_span_rejects_negative_or_oversized_extent(self):
        with self.assertRaises(ValueError):
            checked_span(0, -1)
        with self.assertRaises(ValueError):
            checked_span(0, SAFE_LIMIT + 1)

    def test_checked_span_rejects_signed_32_bit_overflow(self):
        with self.assertRaises(ValueError):
            checked_span(INT32_MAX - 2, 10)
        with self.assertRaises(ValueError):
            checked_span(INT32_MIN - 1, 0)

    def test_checked_span_rejects_booleans_and_invalid_max_extent(self):
        with self.assertRaises(TypeError):
            checked_span(True, 1)
        with self.assertRaises(TypeError):
            checked_span(1, False)
        with self.assertRaises(ValueError):
            checked_span(1, 1, max_extent=-1)
        with self.assertRaises(ValueError):
            checked_span(1, 1, max_extent=True)
    def test_checked_span_rejects_non_integer_inputs(self):
        with self.assertRaises(TypeError):
            checked_span(1.5, 2)
        with self.assertRaises(TypeError):
            checked_span(1, 2.5)


if __name__ == "__main__":
    unittest.main()
