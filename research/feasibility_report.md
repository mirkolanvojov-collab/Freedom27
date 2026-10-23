# Freedom27 — Feasibility and Evidence Report

**Status:** Research scaffold only. **No working iOS 27 jailbreak or installer has been produced or verified.**

## Executive finding

The repository currently contains metadata validation, read-only diagnostics, a vulnerability evidence registry, and automated tests. These are useful project infrastructure, but they do not compromise iOS, install packages, or modify the device.

A jailbreak for a specific iPhone and iOS build generally requires a compatible vulnerability chain and a reliable method to turn that access into the required privileges. A public exploit for an older release is not evidence that it works on iOS 27 or on a particular device/build.

## Public research reviewed

- **Google Threat Intelligence Group, DarkSword (18 March 2026):** reports a historical exploit chain targeting iOS 18.4–18.7; the report says the vulnerabilities were patched by iOS 26.3. This is historical context, not evidence of compatibility with iOS 27.  
  https://cloud.google.com/blog/topics/threat-intelligence/darksword-ios-exploit-chain
- **Google Project Zero, iOS exploit-chain analysis (2019):** useful historical explanation of multi-stage iOS exploitation, not a current compatibility claim.  
  https://projectzero.google/2019/08/a-very-deep-dive-into-ios-exploit.html
- **Apple Security Research Device Program:** Apple describes a specially fused iPhone for controlled iOS security research. Applications are reviewed; devices are loaned under program terms, not made available automatically. The current page says the application period ends 30 October 2026.  
  https://security.apple.com/research-device/

## Evidence rules

1. Record exact device model, iOS version, and build before making compatibility claims.
2. Each vulnerability entry must include a primary or reputable source, affected versions, patch information, evidence status, and a clear distinction between historical and current evidence.
3. Keep all unverified claims labelled `unverified` or `under-review`.
4. Do not label the project as a working jailbreak until a reproducible, authorized test on the exact target build demonstrates the relevant privilege level and a safe installation/recovery path.
5. Do not test exploit chains on devices or systems without authorization.

## Remaining technical gates

- [ ] Identify the exact target device and OS build.
- [ ] Find credible, build-specific vulnerability evidence for that target.
- [ ] Validate any candidate research in an authorized lab or Apple Security Research Device, if access is granted.
- [ ] Establish a reproducible privilege-escalation result and document limitations.
- [ ] Design a recovery-safe, non-destructive validation path.
- [ ] Only after those gates pass, assess package-manager and tweak-framework feasibility.

## Current limitations

- No private physical iOS lab or device farm is available through this chat.
- GitHub Actions can test the project's Python logic, but cannot prove an exploit works on a physical iPhone.
- No verified iOS 27 exploit chain, persistence mechanism, Cydia integration, tweak framework, or installable jailbreak package is included.
- This project does not run experiments in the background after the conversation ends.

## Next actionable step

Apply to Apple's Security Research Device Program if eligible, or arrange an authorized test device/lab. Meanwhile, keep building the evidence registry and safe test infrastructure; do not attempt to install an unverified jailbreak on a daily-use phone.
