# Patch-level evidence sweep — 2026-10-24

## Executive result

The existing 12-candidate reconciliation remains valid for the iOS 26.7 advisory set: all 12 are present in Apple's primary bulletin and their published iOS/iPadOS version ranges include versions below 26.7, but none is independently confirmed on target build 23G83. The public-source sweep did not find a public patch diff tying those 12 advisory entries to exact vulnerable source lines or a reproducible target-build behavior.

A more concrete, newly identified lead is **CVE-2026-86950 (CoreGraphics)**, fixed in iOS 26.7.1. Apple states that processing a maliciously crafted file may lead to arbitrary code execution and that the issue may have been exploited in highly targeted attacks on versions before iOS 27. A public Calif research write-up reports a binary patch comparison between iOS 26.7 and 26.7.1 and identifies the corrected bounds behavior in CoreGraphics path rasterization. This is stronger patch-level evidence than the generic advisory summaries for the existing 12 candidates, but it is not proof that build 23G83 is vulnerable or that the issue yields a jailbreak.

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

This is a public, technically specific patch attribution for the 26.7.1 fix. It does not automatically map the same code to the target IPSW: the project's earlier AVE and KernelCache member hashes are unrelated archive-member hashes and cannot be used as evidence for CoreGraphics. No decrypted target CoreGraphics binary, exact 23G83 function mapping, or independent target reproduction has been captured here.

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

## Safe next validation gate

1. Preserve the public source and its date/URL as provenance; do not copy exploit steps into Freedom27.
2. Seek a lawful, reproducible way to compare the relevant CoreGraphics code in verified 23G83 and 26.7.1 images. Verify each full IPSW digest before extraction, and document tool versions and whether the extracted payload is decrypted.
3. If code is inspectable, compare only the relevant defensive invariant and record exact binary identity, function mapping, and limitations. Do not infer a patch from unrelated component hashes or strings.
4. Add synthetic tests for coordinate conversion and bounding-box arithmetic in a standalone model; do not trigger memory corruption on a live device.
5. Keep the target status at `not_established` until exact-build evidence supports an upgrade. A patch diff alone does not establish a reliable exploit, kernel privilege, persistence, or a complete jailbreak.

## Safety statement

Read-only public-source research only. No exploit or PoC was executed, no payload was built, and no device was accessed, installed on, restored, downgraded, or modified. No crash-free guarantee or working jailbreak is claimed.
