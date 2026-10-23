"""Safe, read-only diagnostics for the Freedom27 research scaffold."""

from __future__ import annotations

import platform
import sys
from typing import Any


def collect_diagnostics() -> dict[str, Any]:
    """Return basic Python/runtime information without probing or changing a device."""
    return {
        "project": "Freedom27",
        "mode": "research-scaffold",
        "python_version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": sys.platform,
        "device_modification_attempted": False,
        "jailbreak_verified": False,
    }


def format_diagnostics(report: dict[str, Any]) -> str:
    """Format a diagnostics report as readable plain text."""
    return "\n".join(f"{key}: {value}" for key, value in sorted(report.items()))
