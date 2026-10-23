# Next-step assessment: what the public lead does and does not establish

**Review date:** 2026-10-23  
**Freedom27 target:** iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`  
**Assessment type:** public-source review only; no Freedom27 device test performed

## New comparison: Veilpath

Veilpath's public README is useful because it distinguishes the upstream `bad_query` version range from the narrower range its own implementation says it has physically validated. It reports physical-device validation on an iPhone 17 Pro running iOS 27 beta 3 (build `24A5390f`) and an iPad Air on iPadOS 27 beta 3 (build `24A5380l`). It says not to assume that every version in the upstream proof-of-concept range is validated by Veilpath.

Source: https://github.com/everettjf/veilpath

That is a different device/build from Freedom27's configured iPhone 16 Plus / iOS 26.6.1 / 23G83. It therefore cannot be used as exact-target proof.

## Updated finding for bad_query

The public README calls `bad_query` a sandbox-escape proof of concept for iOS 26.0–26.6.1 and iOS 27.0 beta 4, but explicitly says it is not meaningfully usable as-is. Its listed capabilities are path-scoped container/data access. These are not evidence of kernel read/write, root, code-signing bypass, persistence, or a complete jailbreak.

Source: https://github.com/forcequitOS/bad_query

## Related customization lead: Erosion

Erosion describes itself as a customization toolbox built around `bad_query`, with limited functionality on iOS 26 and some tweaks unavailable. Its compatibility claims remain upstream project claims; this report does not independently reproduce them on Freedom27's target.

Source: https://github.com/jailbreakdotparty/Erosion

## Decision

**Do not start a kernel or privilege-escalation implementation based on these sources alone.** The public evidence reviewed here does not provide a verified, reproducible kernel primitive or complete chain for the configured exact target.

The next evidence-producing step is narrower:
1. Obtain a device-generated diagnostic result from a supported, trusted project only if it can be installed through a legitimate signing/development path available to the user.
2. Record the exact device model, OS version, build, app version, and result.
3. Keep the result scoped to the capability it actually tests (for example, container access); do not infer kernel access or full jailbreak status.
4. Do not change or downgrade the daily-use phone, install unknown configuration profiles, or run unreviewed payloads to fill evidence gaps.

## Current evidence status

- Public source lead exists: **yes**
- Some public implementations report physical-device validation on other builds: **yes**
- Freedom27 has reproduced the lead on `iPhone17,4 / 23G83`: **no**
- Kernel-level primitive established for that target: **no**
- Complete jailbreak established: **no**

This report is research tracking, not a claim of device compatibility.
