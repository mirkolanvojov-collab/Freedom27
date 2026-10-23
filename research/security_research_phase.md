# Freedom27 security research phase

**Status:** research-only; no working jailbreak is claimed.

## Target
- Device: iPhone 16 Plus (`iPhone17,4`)
- OS/build recorded by the project: iOS 26.6.1 (`23G83`)
- Development constraint: iPhone-only access
- Goal: investigate whether a reproducible, original Freedom27 implementation is technically feasible. Cydia and tweak-framework support are downstream goals, not assumed capabilities.

## Independence rule
Freedom27 must not depend on another jailbreak tool, installer, exploit runner, or payload as its implementation. Public advisories, source code, and technical write-ups may be used as research evidence, with attribution and limitations recorded. Borrowing a claim is not reproducing a result.

## Research sequence

1. **Inventory security boundaries.** Maintain a versioned map of relevant protections and the evidence needed to demonstrate each capability: app sandbox boundary, privileged service boundary, kernel boundary, code-signing / platform policy, persistence, and package bootstrap.
2. **Build an evidence ledger.** For every candidate issue, record the primary advisory/source, affected and fixed versions, hardware scope, patch/build boundary, demonstrated primitive, prerequisites, and confidence. Mark unknown fields as unknown; do not infer compatibility from version-number overlap.
3. **Prioritize target-specific leads.** Prefer original vendor advisories and researcher-authored technical analyses that disclose enough detail to assess applicability to build `23G83`. Reject marketing pages and unsubstantiated installer claims as proof.
4. **Develop original, non-invasive tests first.** Add unit tests for parsing, version/build matching, evidence provenance, and fail-closed decisions. Keep the test harness read-only with respect to the phone; it must not attempt privilege escalation, persistence, security-control disabling, or payload installation.
5. **Set explicit proof gates.** Do not promote a lead to reproduced until there is a documented, repeatable test result for the exact device/build and independent review. A single primitive does not imply kernel control, root access, persistence, or a complete jailbreak.
6. **Implementation gate.** Before any exploit execution or device test, stop for explicit owner approval and a documented risk review. No unknown profiles, certificates, apps, payloads, downgrades, restores, or tests on the daily-use phone without that approval.
7. **Report honestly.** CI success proves only the repository tests passed. Keep the target status blocked until evidence demonstrates otherwise.

## Immediate deliverables
- Keep source/evidence metadata validation fail-closed.
- Add regression tests for build-specific affected-version boundaries and unknown evidence.
- Maintain a machine-readable research ledger and human-readable decision log.
- Re-review primary sources when new evidence appears; do not treat a list of public projects as a dependency plan.

## Exit criteria
The research phase can advance only when a primary technical source supports a plausible lead for the exact target, its scope and patch status are understood, and a safe reproducible validation plan exists. A complete jailbreak remains unverified until all required capabilities are independently demonstrated.

This document is a research plan, not a claim that a vulnerability exists or that the target can be jailbroken.
