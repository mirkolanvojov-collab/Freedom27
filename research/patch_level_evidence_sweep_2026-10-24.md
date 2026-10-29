# Patch-level evidence sweep — 2026-10-24

## Executive result

The existing 12-candidate reconciliation remains valid for the iOS 26.7 advisory set: all 12 are present in Apple's primary bulletin and their published iOS/iPadOS version ranges include versions below 26.7, but none is independently confirmed on target build 23G83. The public-source sweep did not find a public patch diff tying those 12 advisory entries to exact vulnerable source lines or a reproducible target-build behavior.

A more concrete lead is **CVE-2026-86950 (CoreGraphics)**, fixed in iOS 26.7.1. Apple states that processing a maliciously crafted file may lead to arbitrary code execution and that the issue may have been exploited in highly targeted attacks on versions before iOS 27. A public Calif research write-up reports a binary patch comparison between iOS 26.7 and 26.7.1 and identifies the corrected bounds behavior in CoreGraphics path rasterization. Freedom27's later static comparison of target build 23G83 against fixed reference 23H30 found guard patterns consistent with that analysis in seven functions. This is stronger target-specific static evidence than the earlier advisory-only status, but it is not proof of runtime reachability, exploitability, or a jailbreak.

## Evidence record: CVE-2026-86950

| Field | Finding |
|---|---|
| Vendor source | Apple iOS 26.7.1 / iPadOS 26.7.1 security advisory |
| Vendor component | CoreGraphics |
| Vendor fix class | Out-of-bounds write; improved bounds checking |
| Vendor impact | Crafted-file processing may permit arbitrary code execution |
| Vendor exploitation statement | Apple says it is aware of a report of possible exploitation against specific targeted individuals on versions before iOS 27 |
| Public patch analysis | Calif, “The Great Glyph Grift,” dated 2026-09-30 |
| Comparison described by researcher | iOS 26.7 versus iOS 26.7.1 CoreGraphics binaries |
| Patch-level interpretation | Researcher reports a bounds guard added around floating-point-to-fixed-point coordinate conversion in anti-aliased path rasterization; the same pattern appears across multiple changed functions |
| Target relation | iOS 26.6.1 build 23G83 predates iOS 26.7.1, but Apple does not identify 23G83 specifically |
| Exact target-binary mapping | **Not independently verified** |
| Freedom27 reproduction | **Not reproduced** |
| Jailbreak-chain contribution | **Not established** |

Sources:
- Apple advisory: https://support.apple.com/en-us/149226
- Calif technical write-up: https://calif.io/research/the-great-glyph-grift
- Apple iOS 26.7 advisory for version context: https://support.apple.com/en-us/149041

### What the public patch analysis establishes

The researcher reports comparing the CoreGraphics binary before and after the 26.7.1 fix and identifies a repeated code change related to safe conversion of rasterization coordinates into a fixed-point integer representation. The reported fix constrains the converted value before the integer cast, addressing the out-of-bounds-write root cause described in Apple's advisory.

This is a public, technically specific patch attribution for the 26.7.1 fix. The later target/fixed CoreGraphics comparison now provides a static function-level correspondence in seven functions to the same coordinate-conversion guard pattern. The project's earlier AVE and KernelCache member hashes remain unrelated archive-member hashes and are not evidence for CoreGraphics. The static mapping does not establish runtime reachability on 23G83 or independent target reproduction.

The public article includes exploit demonstration material. Freedom27 does not adopt or execute its PoC, weaponization steps, or target-specific trigger sequence. The useful result for this project is the patch-level description and a testable *defensive invariant*: conversion must clamp or otherwise safely handle non-finite and out-of-range coordinates before narrowing, and subsequent bounding-box arithmetic must not wrap.

## Existing 12 candidates: patch-evidence disposition

The 12 CVEs in `research/cve_program_reconciliation_2026-10-24_canonical.json` remain at **public advisory/version-range evidence**. The reviewed source set did not reveal an authoritative public patch diff or independently validated technical report that establishes exact 23G83 code presence and reachability for these candidates.

- **CVE-2026-84607 (AVEVideoEncoder):** advisory says race condition/state management; the AVE raw member changed across releases, but no source or binary patch is mapped to this CVE.
- **CVE-2026-43689 (Kernel):** advisory says permissions restrictions; no specific permission path or patch hunk is publicly established in the reviewed sources.
- **CVE-2026-84523 (APFS):** advisory says out-of-bounds write; no public source-level bounds invariant or exact target mapping established.
- **CVE-2026-86876 (CoreMedia):** advisory says sandbox restrictions may be circumvented; no exact code path/patch mapping established.
- **CVE-2026-86886 (TCC):** advisory says path traversal; no canonicalization/authorization patch hunk established.
- **CVE-2026-84566, CVE-2026-43684, CVE-2026-43686, CVE-2026-28968:** kernel memory-safety descriptions lack a mapped target-build code path; NFS candidates also have explicit environment preconditions.
- **CVE-2026-43687, CVE-2026-65405, CVE-2026-84622:** disclosure candidates do not independently establish an entry primitive; CVE-2026-84622 explicitly presupposes root.

The absence of a public patch diff in this sweep is a time-bounded search result, not proof that no private, embargoed, or unindexed analysis exists.

## Remaining validation gate

1. Preserve the public source and its date/URL as provenance; do not copy exploit steps into Freedom27.
2. **Completed:** verified the pinned target IPSW provenance, extracted CoreGraphics from target 23G83 and fixed reference 23H30, and compared 25 shared executable `aa_*` symbols with zero disassembly failures.
3. **Completed, static only:** correlated guard patterns in seven changed functions with the public coordinate-conversion patch description. Review relocation-sensitive references before making stronger semantic claims.
4. Keep synthetic coordinate-conversion and bounding-box model tests separate from Apple's implementation; do not trigger memory corruption on a live device.
5. Keep runtime reachability, exploitability, kernel privilege, persistence, and complete-jailbreak status unverified until independently supported by safe, authorized evidence.

## Safety statement

Read-only public-source research only. No exploit or PoC was executed, no payload was built, and no device was accessed, installed on, restored, downgraded, or modified. No crash-free guarantee or working jailbreak is claimed.
