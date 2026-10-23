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

    @property
    def is_verified(self) -> bool:
        return self.status.strip().lower() == "verified" and bool(self.source_url.strip())

def validate_profile(profile: TargetProfile) -> list[str]:
    return [f"{field} is required" for field in ("device_model", "os_version", "build_number") if not getattr(profile, field).strip()]

def claim_is_usable(claim: CompatibilityClaim) -> bool:
    return claim.is_verified
