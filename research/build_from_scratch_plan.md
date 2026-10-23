# Freedom27: build-from-scratch plan

**Target:** iPhone 16 Plus (iPhone17,4), iOS 26.6.1, build 23G83  
**Approach:** original implementation, evidence-first, no copied exploit chain and no assumed compatibility.

## The honest starting point

We can author Freedom27's own code, tests, research tools, interfaces, and documentation. We cannot manufacture a vulnerability by writing more project files. A full jailbreak requires a real, reproducible path through the target's security boundaries. Until that exists, Freedom27 is a research project, not an installable jailbreak, and Cydia integration is a later milestone.

## Workstreams

### A. Core project (build now)
- Keep the target/device/build manifest machine-readable.
- Add a source-evidence registry with provenance, version scope, prerequisites, limitations, and reproduction status.
- Add a fail-closed readiness report. Unknown evidence must never count as success.
- Add automated tests and CI so every change is checked.
- Write a plain-language status page distinguishing verified facts, hypotheses, and missing proof.

### B. Public-source analysis (build now)
- Review public candidate projects at source level, including their licenses, dependencies, setup requirements, claimed scope, and destructive side effects.
- Record whether a claim is only in a README, supported by code, independently reproduced, or tested on the exact target.
- Do not run downloaded payloads on the daily-use phone during initial review.

### C. Device validation (only when safe and supported)
- Define a non-destructive test protocol and recovery/backup checklist before any device test.
- A test counts as target-specific only when it records the exact device identifier, iOS version, build, steps, observed output, and evidence.
- Never label simulator or other-device results as proof for iPhone17,4 / 23G83.

### D. Security-boundary milestones (evidence required)
1. **Entry point:** a documented and reproducible vulnerability applicable to the exact target.
2. **Privilege boundary:** a demonstrated, authorized path beyond the initial app/container context.
3. **Required system control:** a technically documented way to obtain the control needed for the intended features.
4. **Mitigations and stability:** measured behavior and known failure modes on the exact build.
5. **Bootstrap:** only after prior milestones are proven, evaluate whether a supported bootstrap/package manager is technically and legally feasible.
6. **User-facing customization:** implement only features that the demonstrated privileges actually permit.

These are proof gates, not claims that a specific exploit exists or that each gate requires a separate vulnerability.

## Definition of done for the current phase

- CI passes.
- All public claims have sources and scope.
- Unknowns remain explicitly unknown.
- No unverified payload is run on the daily-use phone.
- The repo makes no claim of a working jailbreak or Cydia support until exact-target evidence exists.

## Next implementation order

1. Review the source and license of the closest public leads; write a limitations matrix.
2. Extend the evidence registry with source-level observations, each linked to an exact file/line or upstream commit where possible.
3. Add tests that reject unsupported claims of device compatibility or jailbreak readiness.
4. Create a safe test protocol with explicit stop conditions and recovery preparation.
5. Reassess feasibility based on evidence—not on version-number overlap alone.

## Constraints

The project is being managed from an iPhone. Prefer repository-hosted edits and automated CI; do not make a Mac/PC or local terminal a prerequisite unless a later build/test step genuinely requires one.
