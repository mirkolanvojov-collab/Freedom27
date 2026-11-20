"""Discover the synthetic boundary tests in the standard CI test suite."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: str | None):
    source = Path(__file__).resolve().parents[1] / "research/scripts/test_synthetic_conversion_boundaries.py"
    spec = importlib.util.spec_from_file_location("synthetic_conversion_boundaries", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load synthetic boundary tests: {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tests.addTests(loader.loadTestsFromModule(module))
    return tests
