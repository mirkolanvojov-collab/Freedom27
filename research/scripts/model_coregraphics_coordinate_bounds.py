#!/usr/bin/env python3
"""Safe synthetic model of a coordinate-narrowing defensive invariant.

This is not Apple's CoreGraphics implementation, an exploit, or a target test.
It models the policy that coordinates are checked before conversion to int32
and that bounding-box arithmetic is validated before use.
"""
from __future__ import annotations

import math

INT32_MIN = -(2**31)
INT32_MAX = 2**31 - 1
SAFE_LIMIT = 0x3FFFF001


def safe_fixed_coordinate(px: float) -> int:
    """Convert a pixel coordinate to a bounded 1/4096 fixed-point integer."""
    scaled = 0.5 + 4096.0 * px
    if not math.isfinite(scaled):
        return 0
    if scaled < -SAFE_LIMIT:
        return -SAFE_LIMIT
    if scaled > SAFE_LIMIT:
        return SAFE_LIMIT
    return int(scaled)


def checked_span(origin: int, extent: int, *, max_extent: int = SAFE_LIMIT) -> tuple[int, int]:
    """Return a validated half-open interval without signed-int wraparound."""
    if type(origin) is not int or type(extent) is not int:
        raise TypeError("origin and extent must be integers (booleans are not accepted)")
    if type(max_extent) is not int or max_extent < 0:
        raise ValueError("max_extent must be a non-negative integer")
    if extent < 0 or extent > max_extent:
        raise ValueError("extent outside permitted range")
    end = origin + extent
    if origin < INT32_MIN or origin > INT32_MAX or end < INT32_MIN or end > INT32_MAX:
        raise ValueError("interval exceeds signed 32-bit bounds")
    return origin, end


if __name__ == "__main__":
    # Small, non-exploit demonstration of the model's boundary policy.
    examples = [float("nan"), float("inf"), -1e20, -1.0, 0.0, 1.0, 1e20]
    for coordinate in examples:
        print(f"{coordinate!r} -> {safe_fixed_coordinate(coordinate)}")
