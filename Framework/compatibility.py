"""Build-specific compatibility checks for the Freedom27 research scaffold."""

from dataclasses import dataclass
from urllib.parse import urlparse


def _valid_https_url(value: str) -> bool:
    try:
        parsed = urlparse(value.strip())
        valid = (
            parsed.scheme == "https"
            and bool(parsed.hostname)
            and not parsed.username
            and not parsed.password
        )
        if valid:
            _ = parsed.port  # Reject malformed port values.
        return valid
    except (AttributeError, ValueError):
        return False


@dataclass(frozen=True)
class TargetProfile:
    device_model: str
    os_version: str
    build_number: str


@dataclass(frozen=True)
class CompatibilityClaim:
    component: str
    status: str
    source_url: str = ""
    notes: str = ""
    build_number: str = ""

    @property
    def is_verified(self) -> bool:
        return (
            isinstance(self.status, str)
            and self.status.strip().lower() == "verified"
            and isinstance(self.source_url, str)
            and _valid_https_url(self.source_url)
            and isinstance(self.build_number, str)
            and bool(self.build_number.strip())
        )


def validate_profile(profile: TargetProfile) -> list[str]:
    """Return validation errors; an empty list means all profile fields are present."""
    return [
        f"{field} is required"
        for field in ("device_model", "os_version", "build_number")
        if not isinstance(getattr(profile, field), str) or not getattr(profile, field).strip()
    ]


def claim_is_usable(claim: CompatibilityClaim, target_build: str = "") -> bool:
    """Only trust sourced, build-specific verified claims for an explicitly named target build."""
    if not target_build or not claim.is_verified:
        return False
    return claim.build_number == target_build
