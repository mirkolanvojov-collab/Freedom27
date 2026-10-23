# Security Research Engine

The Security Research Engine is Freedom27's original evidence-management layer. It is intentionally not an exploit runner.

## Files

- `Framework/security_research_engine.py`: typed target/hypothesis records and fail-closed completeness checks.
- `Framework/safe_test_planner.py`: creates a human-readable plan with expected/falsifying observations and explicit stop conditions.
- `tests/test_security_research_engine.py` and `tests/test_safe_test_planner.py`: regression tests for evidence handling.

## Use

From a Python environment with the repository checked out:

```python
from Framework.security_research_engine import Hypothesis, Target, readiness_report
from Framework.safe_test_planner import build_test_plan

target = Target("iPhone 16 Plus", "iPhone17,4", "iOS 26.6.1", "23G83")
hypothesis = Hypothesis(
    hypothesis_id="H-EXAMPLE",
    boundary="state the boundary being studied",
    claim="state a testable claim",
    expected_observation="what would support the claim",
    falsifying_observation="what would weaken or disprove it",
    source_urls=("https://example.org/primary-source",),
)
print(readiness_report(target, [hypothesis]))
print(build_test_plan(target, hypothesis))
```

Replace the example source with a real primary source before treating the plan as research-ready.

## Meaning of "ready"

`ready_for_review` means only that the record passes basic completeness checks. It does not mean the test is approved, safe in every environment, technically valid, or evidence that a vulnerability exists. A human must review the source, prerequisites, impact, and recovery path.

## Deliberate limitations

This module does not fetch URLs, execute third-party code, access the phone, bypass iOS protections, or make changes to the device. Keep those boundaries until source provenance, impact, and safe validation methods are understood.
