"""Evidence-aware compatibility matrix helpers for Freedom27.

This module tracks research claims. It does not exploit devices or prove that a
jailbreak works. A claim becomes verified only after an explicit evidence review.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable
from urllib.parse import urlparse

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
        def text_field(name: str) -> str:
            value = item.get(name, "")
            return value.strip() if isinstance(value, str) else ""

        return cls(
            device_family=text_field("device_family"),
            model_identifier=text_field("model_identifier"),
            os_version=text_field("os_version"),
            build=text_field("build"),
            status=text_field("status"),
            evidence_url=text_field("evidence_url"),
            notes=text_field("notes"),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        for field_name in ("device_family", "model_identifier", "os_version", "build"):
            if not getattr(self, field_name):
                errors.append(f"{field_name} must not be empty")
        if self.status not in VALID_STATUSES:
            errors.append(f"status must be one of: {', '.join(sorted(VALID_STATUSES))}")
        if self.status == "verified":
            try:
                parsed = urlparse(self.evidence_url)
                valid_url = (
                    parsed.scheme == "https" and bool(parsed.hostname)
                    and not parsed.username and not parsed.password
                )
            except ValueError:
                valid_url = False
            if not valid_url:
                errors.append("verified claims require a valid HTTPS evidence_url")
            if not self.notes:
                errors.append("verified claims require review notes")
        if self.status == "not-supported" and not self.notes:
            errors.append("not-supported claims require explanatory notes")
        return errors


def validate_claims(items: Iterable[dict[str, Any]]) -> list[str]:
    """Validate claims and reject malformed or duplicate device/version/build tuples."""
    errors: list[str] = []
    seen: set[tuple[str, str, str, str]] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"claim[{index}]: must be an object")
            continue
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
