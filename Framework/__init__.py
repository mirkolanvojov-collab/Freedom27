"""Freedom27 research framework.

This package provides validation helpers only; it does not modify devices.
"""

from .compatibility import CompatibilityClaim, TargetProfile, claim_is_usable, validate_profile
from .registry import validate_entry

__all__ = [
    "CompatibilityClaim",
    "TargetProfile",
    "claim_is_usable",
    "validate_profile",
    "validate_entry",
]
