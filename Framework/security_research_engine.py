"""Freedom27 Security Research Engine.

This module is deliberately non-invasive. It evaluates the completeness of a
research hypothesis and records safe test plans; it does not exploit the OS,
bypass code-signing, escalate privileges, or modify the device.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable


class EvidenceLevel(str, Enum):
    HYPOTHESIS = "hypothesis"
    SOURCE_SUPPORTED = "source_supported"
    DEMONSTRATED = "demonstrated"
    INDEPENDENTLY_REPRODUCED = "independently_reproduced"
    EXACT_TARGET_VERIFIED = "exact_target_verified"


@dataclass(frozen=True)
class Target:
    device: str
    identifier: str
    os_version: str
    build: str


@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    boundary: str
    claim: str
    expected_observation: str
    falsifying_observation: str
    source_urls: tuple[str, ...] = ()
    prerequisites: tuple[str, ...] = ()
    non_destructive: bool = True
    recovery_plan: str = ""
    evidence_level: EvidenceLevel = EvidenceLevel.HYPOTHESIS
    tested_target: Target | None = None
    observed_result: str = ""

    def validate(self, target: Target) -> list[str]:
        """Return blockers; an empty list means only that the record is complete."""
        issues: list[str] = []
        if not self.hypothesis_id.strip():
            issues.append("missing hypothesis ID")
        if not self.boundary.strip():
            issues.append("security boundary is not defined")
        if not self.claim.strip():
            issues.append("claim is empty")
        if not self.expected_observation.strip():
            issues.append("expected observation is missing")
        if not self.falsifying_observation.strip():
            issues.append("falsifying observation is missing")
        if not self.source_urls:
            issues.append("no source URLs supplied")
        if not self.non_destructive and not self.recovery_plan.strip():
            issues.append("potentially destructive test lacks a recovery plan")
        if self.evidence_level is EvidenceLevel.EXACT_TARGET_VERIFIED:
            if self.tested_target != target:
                issues.append("exact-target label does not match the configured target")
            if not self.observed_result.strip():
                issues.append("exact-target label lacks an observed result")
        if self.evidence_level in (
            EvidenceLevel.DEMONSTRATED,
            EvidenceLevel.INDEPENDENTLY_REPRODUCED,
        ) and not self.observed_result.strip():
            issues.append("demonstration label lacks an observed result")
        return issues


def readiness_report(target: Target, hypotheses: Iterable[Hypothesis]) -> dict:
    records = []
    for hypothesis in hypotheses:
        blockers = hypothesis.validate(target)
        records.append({
            "id": hypothesis.hypothesis_id,
            "boundary": hypothesis.boundary,
            "evidence_level": hypothesis.evidence_level.value,
            "blockers": blockers,
            "record_complete": not blockers,
        })
    return {
        "target": asdict(target),
        "hypotheses": records,
        "fully_verified_hypothesis_count": sum(
            1 for item in records
            if item["evidence_level"] == EvidenceLevel.EXACT_TARGET_VERIFIED.value
            and item["record_complete"]
        ),
        "warning": (
            "Record completeness is not proof that a vulnerability exists or that "
            "a jailbreak works. This engine performs no device exploitation."
        ),
    }
