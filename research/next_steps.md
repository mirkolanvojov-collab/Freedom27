# Freedom27 next-step execution plan

## Current verified project state

- Project status: research scaffold; no working jailbreak is included.
- Owner's available development device: iPhone only.
- Target recorded in `research/target_profile.json`: iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`.
- The GitHub Actions workflow validates source metadata and Python tests. It does not run code on the iPhone, test USB/DFU behavior, or prove exploitability.
- The exact-target evidence and claim-evidence checks must remain fail-closed. Version overlap alone is not compatibility evidence.

## Work completed

1. Added read-only research triage that joins the vulnerability registry and evidence ledger.
2. Added CI validation for evidence metadata and exact-target verified claims.
3. Added tests to flag a registry entry marked `verified` when the evidence ledger does not record Freedom27 reproduction.
4. Documented the limits of the `bad_query` sandbox-escape proof of concept and the exact-target status.

## Next actions, in order

### 1. Keep the CI baseline green
- Run the complete GitHub Actions workflow after each change.
- Treat a failed run as a blocker; do not label the repository healthy until the latest full run passes.
- Keep generated triage output machine-readable and assert that registry/ledger joins and reproduction counts are consistent.

### 2. Review only primary public evidence
For every new research lead, record:
- the original source URL and the date reviewed;
- exact device model or hardware family, OS version and build when disclosed;
- the capability actually demonstrated (app sandbox access, privilege escalation, kernel control, persistence, or package-manager support);
- patch scope and any limitations stated by the source;
- whether the result is only a report, an upstream claim, or independently reproducible.

Do not upgrade a lead based solely on a headline, CVE, version overlap, or a demonstration on another device.

### 3. Maintain a clear target decision
- Keep the iPhone 16 Plus / iOS 26.6.1 / 23G83 conclusion marked unverified until exact-target evidence exists.
- Do not install unknown configuration profiles, certificates, apps, payloads, or online-jailbreak offers.
- Do not downgrade or restore the phone as a speculative research step.
- Recheck the public tracker and original upstream project only when new primary evidence or a release appears.

### 4. Make progress with iPhone-only access
- Use GitHub's web interface and GitHub Actions for source control and metadata tests.
- Use read-only source review and documentation tasks that do not require local Xcode, macOS, signing credentials, or a second device.
- Mark hardware-dependent tasks as blocked until an appropriate, authorized test environment is available.
- Do not describe GitHub Actions passing as proof the physical iPhone is exploitable or compatible.

### 5. Only begin implementation after evidence supports it
A future implementation phase requires a public technical source and exact-target support evidence, a documented safety review, and a reproducible test plan. A sandbox escape alone is not a complete jailbreak and does not establish root access, persistence, Cydia, or tweak-framework compatibility.

## Definition of done for the current research phase

- All automated tests and metadata checks pass.
- Every lead has a clear status, source, limitations and next action.
- No unsupported exact-target compatibility claim is presented as verified.
- The project status continues to say research-only until a working chain is independently reproduced on the exact target.

This plan is a repository workflow, not a promise that a jailbreak exists or can be built for the current target.

### Latest source-review checkpoint (2026-10-23)
- Read-only audit recorded at [research/read_only_source_audit_2026-10-23.md](read_only_source_audit_2026-10-23.md).
- The public CVE report reviewed does not establish a working issue on build `23G83`; its own stated affected scope ends at iOS 26.6 / build `23G71`.
- `bad_query`, Erosion, and EscapeOS remain leads for separate, limited capabilities—not proof of a complete jailbreak for this exact target.
- Next action: check the push-triggered GitHub Actions result for the documentation update; then continue primary-source review only. Do not install or execute the reviewed projects on the phone.

### Public compatibility checkpoint (2026-10-23)
- Read-only tracker review recorded at [research/public_compatibility_checkpoint_2026-10-23.md](public_compatibility_checkpoint_2026-10-23.md).
- The Apple Wiki tracker currently lists no jailbreak tool for iOS 26.6.1 / iPhone 16 Plus.
- The `bad_query` README still labels itself a developer PoC, not meaningfully usable; it does not establish a complete jailbreak.
- Combined CI status for commit `40e99982b23061b994c4df776f270ad5fce81d8f` returned no statuses, so its workflow result remains unknown. Check the Actions page; do not infer success from an empty status list.

### Official advisory scope check (2026-10-23)
- Updated [research/exact_target_status.md](exact_target_status.md) to clarify the scope of Apple's official [iOS 26.6.1 security-content advisory](https://support.apple.com/en-us/148282): issues described as fixed in build `23G83` are not evidence of vulnerabilities that remain usable on that build, and a single CVE does not establish a jailbreak chain.
- GitHub's available commit-workflow lookup returned no workflow runs for the documentation commit `2daf87df7a6d0ad79b14d1ecef3f3f2233724437`. This is **unknown**, not a passing CI result. Check [GitHub Actions](https://github.com/mirkolanvojov-collab/Freedom27/actions) for the push-triggered run.
- Next action remains read-only validation: inspect the latest Actions run and its test results, then continue primary-source review. No exploit was run and no phone settings were changed.


### Latest CI and primary-advisory follow-up (2026-10-23)
- Verified [GitHub Actions run #146](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40013306243) for main commit `c3be5c919cfae2d33476d97506516456819f2c93`: the workflow and all listed steps completed successfully. This is repository validation only, not device validation.
- Added [research/ios_26_7_primary_advisory_followup_2026-10-23.md](ios_26_7_primary_advisory_followup_2026-10-23.md). Apple's iOS 26.7 advisory documents TCC, CoreMedia, and kernel issues fixed in 26.7. Because the recorded target is 26.6.1, these are potentially relevant pre-fix leads, but the advisory alone does not prove exact build 23G83 applicability or exploitability.
- Current next blocker: obtain primary technical evidence that establishes the exact affected-version range and a specific, relevant primitive. Keep the chain blocked; no exploit was run and no phone was accessed or modified.
