# Apple advisory cross-check: CVE-2026-65343 — 2026-10-23

## Primary source
Apple's security-content page for iOS 26.6.1:
https://support.apple.com/en-us/148282

Apple lists CVE-2026-65343 under Kernel with impact: "A remote attacker may be able to cause unexpected system termination." Apple describes a use-after-free addressed with improved memory management and credits Drinor Selmanaj (Sentry) and Surya Narayan Kushwaha.

## Important correction
A third-party GitHub repository found during research describes CVE-2026-65343 as an out-of-bounds read leading to kernel pointer disclosure/KASLR defeat and says it affects iOS 26.6 and earlier. That description does not match Apple's description for CVE-2026-65343. Do not use that repository's CVE mapping as established fact.

Apple's same advisory separately lists CVE-2026-65349 as a kernel out-of-bounds read that may cause unexpected system termination or kernel-memory read, addressed with improved input validation. The third-party report may have conflated CVE identifiers; this requires source-level clarification before any registry entry is promoted.

## Freedom27 applicability
- The advisory covers iOS 26.6.1 and compatible iPhone 11-and-later models, so it is relevant background for the target platform.
- The advisory is not a jailbreak, and it does not establish that the issue is exploitable on iPhone 16 Plus build 23G83.
- No exploit was run; no device reproduction was performed.
- Status for exact-target exploitability: NOT VERIFIED.
- Do not build or run exploit payloads based on the third-party report. Keep this as a source-attribution discrepancy pending primary-source clarification.

## Next evidence gate
Compare the third-party repository's CVE references against Apple's full advisory and any primary researcher disclosure, then record only the correctly attributed facts.