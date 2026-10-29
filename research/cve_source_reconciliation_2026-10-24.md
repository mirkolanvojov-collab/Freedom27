# CVE source reconciliation: iOS 26.6.1 build 23G83 — 2026-10-24

## Scope and conclusion

This is a source-level reconciliation of two previously prioritized candidates for the Freedom27 research target: iPhone17,4 (iPhone 16 Plus), iOS 26.6.1 build 23G83. It is not a complete reconciliation of every candidate in the project, a binary patch analysis, or evidence that a working exploit exists.

**Version-level conclusion:** both CVE-2026-84607 and CVE-2026-43689 are documented by public sources as fixed in iOS 26.7. Since target build 23G83 is iOS 26.6.1, it predates that fixed release and falls within the broad version range described by NVD/advisory metadata. This makes them credible research candidates, not confirmed exact-build vulnerabilities. The public records do not identify build 23G83 specifically, prove vulnerable code is reachable on the target device, or supply a reproducible exploit.

## Candidate A — CVE-2026-84607 (AVEVideoEncoder)

| Evidence field | Finding |
|---|---|
| Public component | AVEVideoEncoder |
| Public impact | A sandboxed app may execute arbitrary code with kernel privileges |
| Public weakness/fix description | Race condition; addressed with improved state management |
| Fixed release | iOS 26.7 / iPadOS 26.7 and later releases listed by NVD |
| Target relation | iOS 26.6.1 (23G83) is earlier than the stated iOS 26.7 fix |
| Exact-build status | **Unconfirmed** |
| Patch attribution status | **Unconfirmed** |
| Reproduction status | **Not reproduced by this project** |

Sources:
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-84607
- Apple iOS 26.7 security content: https://support.apple.com/en-us/149041

The target-vs-fixed-build IPSW study recorded changes in the raw AVE firmware archive member and in KernelCache. Those are byte-level differences only. The AVE firmware member is not a source-level mapping to the AVEVideoEncoder vulnerable function, and neither hash difference proves this CVE's fix location. No decrypted executable comparison, patch hunk, vulnerable-state reachability, or crash/reliability result is available.

**Research status:** strongest of these two as a high-level lead because the public impact explicitly describes sandboxed-app-to-kernel-privilege execution. That impact statement must not be treated as a usable exploit primitive or proof of target-build exploitability.

## Candidate B — CVE-2026-43689 (Kernel permissions issue)

| Evidence field | Finding |
|---|---|
| Public component | Kernel |
| Public impact | A malicious app may gain root privileges |
| Public weakness/fix description | Permissions issue; addressed with additional restrictions |
| Fixed release | iOS 26.7 / iPadOS 26.7 and other releases listed by NVD/advisory records |
| Target relation | iOS 26.6.1 (23G83) is earlier than the stated iOS 26.7 fix |
| Exact-build status | **Unconfirmed** |
| Patch attribution status | **Unconfirmed** |
| Reproduction status | **Not reproduced by this project** |

Sources:
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-43689
- GitHub Advisory Database: https://github.com/advisories/GHSA-4jgx-p7cx-g39r
- Apple iOS 26.7 security content: https://support.apple.com/en-us/149041

The public description indicates a privilege/permission boundary issue but does not disclose the specific permission check, kernel interface, vulnerable code path, or conditions needed to trigger it. A changed KernelCache hash between 23G83 and 24A437 is not evidence that this specific issue was patched in that binary.

**Research status:** credible kernel-privilege candidate at the release-family level; insufficient detail for a code-path or exploitability conclusion.

## Evidence hierarchy used

1. **Primary vendor advisory:** Apple confirms the component, broad impact, fix description, and fixed release.
2. **NVD record:** provides the CVE description and affected/fixed version metadata.
3. **Target IPSW inventory:** establishes the exact target image/build metadata and repeatable raw-member hashes.
4. **Not yet available:** build-specific vulnerable-code mapping, decrypted code diff, patch hunk, reachability proof, independent reproduction, and a complete privilege-escalation chain.

The fixed comparison build is iOS 27.0 build 24A437 on the same product type (iPhone17,4) and board class (D48AP). This is a version-gap comparison, not a minimal patch comparison. Manifest metadata and raw member hashes cannot identify which CVE accounts for any individual byte change.

## Next validation gates

- Capture dated source snapshots or structured records for all remaining candidate CVEs and normalize each to vendor, component, impact, fixed version, and exact-build applicability.
- For each candidate, distinguish a public fixed-version range from a build-specific affected statement.
- Do not promote any candidate to “confirmed” without a source-level/binary-level patch reference or independently reproducible exact-build evidence.
- Keep device execution disabled. No payload, exploit, firmware installation, or device modification is part of this reconciliation.

## Safety and stability statement

This evidence does not establish a runnable jailbreak. There is no verified chain to test for stability, and no-crash guarantees are not possible. Unit tests and IPSW hash checks validate research tooling and artifact identity, not exploit safety on an iPhone.
