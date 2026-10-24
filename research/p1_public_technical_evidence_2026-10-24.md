# P1 public technical-evidence review — 2026-10-24 (follow-up 2)

## Outcome

This pass added a useful provenance correction for CVE-2026-43689: Apple's iOS 26.7 advisory credits **Andreas Jaegersberger and Ro Achterberg of Nosebeard Labs**. Nosebeard Labs' public CVE index lists the issue as a kernel root-privilege escalation affecting iOS, iPadOS, macOS, and visionOS, with a disclosure date of 2026-04-26. That improves attribution and disclosure history, but the index does not provide the technical implementation detail needed to identify the exact permission check changed by Apple's fix.

The public CVE-2026-84607 report remains a concrete but unverified binary-analysis hypothesis. Neither P1 candidate is confirmed for iOS 26.6.1 build `23G83`, and no complete Freedom27 chain is verified.

## CVE-2026-84607 — public static-analysis hypothesis

- Apple advisory: https://support.apple.com/en-us/149041
- Third-party report: https://github.com/Ping-2o/ios.CVE-2026-84616-84607/blob/main/REPORT_AVE_84607.md
- Repository metadata: https://api.github.com/repos/Ping-2o/ios.CVE-2026-84616-84607

The report proposes that a new state-consistency guard in Apple's AppleAVE2 driver is associated with the race-condition fix, based on static comparison across iOS 27.0 beta/GM binaries. It explicitly describes itself as AI-generated and not line-by-line human reviewed, says Apple's per-CVE code mapping is not published, withdraws one method for proving pre-fix absence, and says userspace AVEVideoEncoder components were not diffed.

**Assessment:** a specific third-party hypothesis exists, but the CVE-to-code mapping is inferential and the report's iOS 27.0 analysis does not establish applicability to iOS 26.6.1 build `23G83`.

## CVE-2026-43689 — attribution found, patch detail still missing

### Primary source

- Apple iOS 26.7/iPadOS 26.7 security advisory: https://support.apple.com/en-us/149041
- NVD record: https://nvd.nist.gov/vuln/detail/cve-2026-43689

Apple describes a permissions issue fixed with additional restrictions and warns that a malicious app may gain root privileges. The advisory credits Andreas Jaegersberger and Ro Achterberg of Nosebeard Labs.

### Disclosure provenance

- Nosebeard Labs public CVE index: https://nosebeard.co/
- Archived Apple advisory distribution: https://www.mail-archive.com/fulldisclosure%40seclists.org/msg09572.html

Nosebeard Labs' index lists CVE-2026-43689 as “Kernel: Root LPE” for iOS, iPadOS, macOS, and visionOS, with a disclosure date of 2026-04-26. The mailing-list archive reproduces the Apple advisory and attribution. These sources help establish who disclosed the issue and its public timeline, but **do not provide a checkable patch diff or enough implementation detail to identify the specific authorization change**.

## Target and evidence status

- Target recorded in Freedom27: iPhone 16 Plus, `iPhone17,4`, iOS 26.6.1, build `23G83`.
- Public technical hypotheses/reports reviewed: one detailed third-party static-analysis report for CVE-2026-84607.
- CVE-2026-43689 researcher attribution: confirmed from the Apple advisory text and cross-checked against the research group's public CVE index.
- Authoritative patch diffs found: **0**.
- Exact-build confirmations: **0**.
- Freedom27 reproductions: **0**.
- Full jailbreak chain verified: **no**.

## What remains unsolved

1. Independently validate the CVE-2026-84607 binary-analysis hypothesis and its CVE attribution.
2. Establish whether either candidate's affected implementation is present and reachable on build `23G83`; version-range matching alone is insufficient.
3. Obtain implementation-level evidence for CVE-2026-43689's permission restriction from a primary patch or independently checkable vendor binary comparison.
4. Validate the full chain only through safe, authorized, non-destructive research and controlled test evidence.

No exploit was run. No device was accessed, installed on, downgraded, restored, or modified. These are evidence updates, not a claim that the jailbreak or either exploit has been solved.
