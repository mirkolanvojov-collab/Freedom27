"""Generate a reviewable, non-destructive test plan from research hypotheses."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable
from urllib.parse import urlparse

from Framework.security_research_engine import Hypothesis, Target


@dataclass(frozen=True)
class TestStep:
    number: int
    action: str
    expected: str
    stop_if: str


def valid_https_source(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username and not parsed.password


def build_test_plan(target: Target, hypothesis: Hypothesis) -> dict:
    """Return a plan document, not an executable device test."""
    blockers = hypothesis.validate(target)
    blockers.extend(
        f"source is not a valid HTTPS URL: {url}"
        for url in hypothesis.source_urls
        if not valid_https_source(url)
    )
    if not hypothesis.non_destructive and not hypothesis.recovery_plan.strip():
        # Keep this check here too so callers see it even if validation evolves.
        blockers.append("no recovery plan for a potentially destructive test")
    steps = [
        TestStep(1, "Review primary sources and the exact upstream revision", "Mechanism, scope, prerequisites, and license are documented", "Stop if the code's effects or provenance are unclear"),
        TestStep(2, "Define a harmless test fixture and baseline", "Baseline observations are recorded without changing system state", "Stop if the test requires unknown payloads or privileged changes"),
        TestStep(3, "Run only the non-destructive observation described by the hypothesis", hypothesis.expected_observation, "Stop on unexpected writes, crashes, privacy exposure, or instability"),
        TestStep(4, "Record the result and compare it with the falsifying observation", "Result supports or weakens the hypothesis without overstating scope", "Stop and classify as inconclusive if evidence is ambiguous"),
        TestStep(5, "Record device/build and independent reproduction status", "The exact scope and limitations are explicit", "Never generalize results from a different device or build"),
    ]
    return {
        "target": asdict(target),
        "hypothesis_id": hypothesis.hypothesis_id,
        "boundary": hypothesis.boundary,
        "claim": hypothesis.claim,
        "prerequisites": list(hypothesis.prerequisites),
        "sources": list(hypothesis.source_urls),
        "blockers": sorted(set(blockers)),
        "ready_for_review": not blockers,
        "execution_mode": "human-reviewed, non-destructive only",
        "steps": [asdict(step) for step in steps],
        "warning": "This generated plan is not a jailbreak and must not be treated as authorization to run unreviewed code.",
    }
