"""Evidence-aware compatibility matrix helpers for Freedom27.

This module tracks research claims. It does not exploit devices or prove that a
jailbreak works. A claim becomes verified only after an explicit evidence review.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

VALID_STATUSES = {
    "not-investigated",
    "researching",
    "theoretical",
    "experimental",
    "verified",
    "not-supported",
}

@dataclass(frozen=True)
class CompatibilityClaim:
    device_family: str
    model_identifier: str
    os_version: str
    build: str
    status: str
    evidence_url: str = ""
    notes: str = ""

    @classmethod
    def from_mapping(cls, item: dict[str, Any]) -> "CompatibilityClaim":
        return cls(
            device_family=str(item.get("device_family", "")).strip(),
            model_identifier=str(item.get("model_identifier", "")).strip(),
            os_version=str(item.get("os_version", "")).strip(),
            build=str(item.get("build", "")).strip(),
            status=str(item.get("status", "")).strip(),
            evidence_url=str(item.get("evidence_url", "")).strip(),
            notes=str(item.get("notes", "")).strip(),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        for field_name in ("device_family", "model_identifier", "os_version", "build"):
            if not getattr(self, field_name):
                errors.append(f"{field_name} must not be empty")
        if self.status not in VALID_STATUSES:
            errors.append(f"status must be one of: {', '.join(sorted(VALID_STATUSES))}")
        if self.status == "verified":
            if not self.evidence_url.startswith("https://"):
                errors.append("verified claims require an HTTPS evidence_url")
            if not self.notes:
                errors.append("verified claims require review notes")
        if self.status == "not-supported" and not self.notes:
            errors.append("not-supported claims require explanatory notes")
        return errors


def validate_claims(items: Iterable[dict[str, Any]]) -> list[str]:
    """Validate claims and reject duplicate device/version/build tuples."""
    errors: list[str] = []
    seen: set[tuple[str, str, str, str]] = set()
    for index, item in enumerate(items):
        claim = CompatibilityClaim.from_mapping(item)
        errors.extend(f"claim[{index}]: {error}" for error in claim.validate())
        key = (claim.model_identifier, claim.os_version, claim.build, claim.status)
        if key in seen:
            errors.append(f"claim[{index}]: duplicate model/version/build/status tuple")
        seen.add(key)
    return errors


def build_target_matrix() -> list[dict[str, str]]:
    """Return planning rows; these are targets, not support claims."""
    rows: list[dict[str, str]] = []
    for family in ("iPhone 14", "iPhone 15", "iPhone 16", "iPhone 17", "iPhone 18"):
        for os_family in ("iOS 26", "iOS 27"):
            rows.append({
                "device_family": family,
                "os_family": os_family,
                "status": "not-investigated",
                "evidence": "",
                "notes": "Planning target only; exact model, OS version and build required.",
            })
    return rows
