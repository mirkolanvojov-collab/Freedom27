# Freedom27

Freedom27 is a research scaffold for investigating iOS customization and jailbreak feasibility. It does **not** contain a working jailbreak or a verified exploit chain.

## Current status

- **Project state:** research-only.
- **Recorded target:** iPhone 16 Plus (iPhone17,4), iOS 26.6.1, build 23G83.
- **Compatibility:** no exact-target jailbreak has been independently verified by this project.
- **Package manager / tweaks:** Cydia integration, system-wide privilege escalation, persistence, and tweak-framework support are not established.
- **Development environment:** the project owner has an iPhone only. Repository work and metadata tests can run through GitHub; hardware-specific validation cannot be inferred from CI.

## Research safeguards

- Public-source links and limitations are tracked in the vulnerability registry and evidence ledger.
- Exact-target status report records what is and is not known for the current device/build.
- Public jailbreak status checkpoint records the latest reviewed public compatibility trackers and why the target remains blocked.
- Next-step execution plan describes the safe order of work and gates before implementation.
- Blocker-resolution engine prioritizes missing evidence and prerequisites, and requires exact-target, independently reproduced evidence to close gates.
- Read-only iOS security audit planner catalogs security controls and safe research tasks without attempting bypasses or modifying the device.
- Fail-closed device preflight documents crash-risk gates. The metadata gate is deliberately not a claim that any jailbreak is safe.
- Automated checks reject incomplete verified claims and flag claims without exact-target reproduction.
- GitHub Actions runs unit tests, research-metadata checks, and validates machine-readable blocker and audit reports.

## Important limitations

A sandbox escape is not by itself a full jailbreak. A public report, CVE, demonstration on another device, or overlap in OS version numbers does not establish support for this exact iPhone and build. Passing GitHub Actions validates repository code and metadata only; it does not test the physical device.

**Do not run a purported “full jailbreak” from this repository on the daily-use phone.** There is no complete jailbreak implementation here, and no process can honestly guarantee that kernel-level exploit code will never crash or require a restore. Do not install unknown configuration profiles, certificates, payloads, or unofficial jailbreak offers, and do not downgrade or restore the phone based on speculative compatibility claims.

## Current phase definition of done

1. Automated tests and metadata checks pass.
2. Each research lead has a source, clear status, limitations, and next action.
3. No unsupported exact-target claim is described as verified.
4. Implementation starts only after credible exact-target evidence and a safe, reproducible test plan exist.
5. No future device-testing entry point may treat this metadata preflight as proof of safety or as automatic authorization to execute an exploit.
