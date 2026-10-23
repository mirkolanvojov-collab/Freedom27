"""Benign abstract security-invariant models for research regression tests.

These models do not emulate Apple implementation details, trigger CVEs, access a
device, or provide exploit primitives. They are examples of properties that a
vendor-controlled harness could test once a primary-source invariant is known.
"""
from __future__ import annotations

import posixpath
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Iterable


def authorization_allows(is_authorized: bool) -> bool:
    """Fail closed when a mock authorization decision is false."""
    return is_authorized is True


def range_is_valid(offset: int, length: int, capacity: int) -> bool:
    """Validate a half-open range using subtraction to avoid addition overflow."""
    if any(type(value) is not int for value in (offset, length, capacity)):
        return False
    if offset < 0 or length < 0 or capacity < 0:
        return False
    if offset > capacity:
        return False
    return length <= capacity - offset


@dataclass
class ObjectLifetime:
    """Small abstract ownership model; terminal release is irreversible."""
    references: int = 1
    released: bool = False

    def retain(self) -> bool:
        if self.released or self.references <= 0:
            return False
        self.references += 1
        return True

    def release(self) -> bool:
        if self.released or self.references <= 0:
            return False
        self.references -= 1
        if self.references == 0:
            self.released = True
        return True

    def can_use(self) -> bool:
        return not self.released and self.references > 0


def transition_allowed(current: str, requested: str, transitions: dict[str, set[str]]) -> bool:
    """Accept only explicitly enumerated state transitions."""
    return requested in transitions.get(current, set())


def output_is_fully_initialized(required_fields: Iterable[str], output: dict[str, object]) -> bool:
    """Require every expected field to be present and non-sentinel."""
    fields = tuple(required_fields)
    return bool(fields) and all(field in output and output[field] is not None for field in fields)


def path_is_within_root(root: str, candidate: str) -> bool:
    """Lexically normalize synthetic POSIX paths and check root containment.

    This is deliberately not a substitute for descriptor-based filesystem
    authorization or platform-specific path resolution.
    """
    if not PurePosixPath(root).is_absolute() or not PurePosixPath(candidate).is_absolute():
        return False
    normalized_root = posixpath.normpath(root)
    normalized_candidate = posixpath.normpath(candidate)
    try:
        PurePosixPath(normalized_candidate).relative_to(PurePosixPath(normalized_root))
        return True
    except ValueError:
        return False
