"""Build-specific compatibility checks for the Freedom27 research scaffold."""

from dataclasses import dataclass


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
        return self.status.strip().lower() == "verified" and bool(self.source_url.strip())


def validate_profile(profile: TargetProfile) -> list[str]:
    """Return validation errors; an empty list means all profile fields are present."""
    return [
        f"{field} is required"
        for field in ("device_model", "os_version", "build_number")
        if not getattr(profile, field).strip()
    ]


def claim_is_usable(claim: CompatibilityClaim, target_build: str = "") -> bool:
    """Only trust sourced, verified claims; when a target build is supplied it must match."""
    if not claim.is_verified:
        return False
    if target_build and claim.build_number != target_build:
        return False
    return True
