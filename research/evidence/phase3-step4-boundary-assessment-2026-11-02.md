# Phase 3 Step 4 — caller boundary assessment

Date: 2026-11-02. Read-only evidence review; no device execution.

## Observations

The existing static comparison reports `_aa_path_iterate` as normalized-identical across the target 23G83 and reference 23H30 builds. Previous research recorded caller-side bound selection, an optional private autohint transformation, a floating-point precision conversion, and downstream rasterizer handling. These are static observations, not an end-to-end dynamic trace.

## Invariant boundary

The review cannot establish that a bound selected before the optional transformation is preserved after that transformation. Neither the private transformation's full input/output contract nor all downstream register and control-flow paths have been verified. This is an **unknown**, not evidence that the transformation actually produces an unsafe coordinate.

## Source limitations

Apple's public CGAffineTransform documentation describes coordinate mapping but does not specify the private autohint routine. Archived comparison evidence: GitHub Actions run 41373870159, artifact 13112055091. Related register observations: `research/evidence/CVE-2026-86950-phase3-step3-register-trace-2026-11-02.md`.

## Disposition

Step 4 is complete as a **bounded caller-to-rasterizer evidence assessment**. Post-transformation range preservation remains unverified and is carried into Step 5 and the final Phase 3 limitations. No causal CVE attribution, exploitability claim, or safety guarantee is made. PR #37 remains draft.
