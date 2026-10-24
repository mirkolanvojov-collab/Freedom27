# Freedom27 — priority execution update (2026-10-24)

> **Historical checkpoint:** the later [exact-target CVE assessment](target_build_cve_assessment_2026-10-24.md) supersedes this note's provisional source-reconciliation and version-range status. Retain this document as the record of the earlier research pass; use the linked assessment for the current 12-CVE result.

## Scope and safety

This update advances public-evidence and non-exploit regression work for the existing 12-CVE research set. It is a source-traceability plan, not exploit implementation. No payloads, exploit triggers, kernel writes, privilege-escalation code, or device changes are included.

Primary source: Apple, “About the security content of iOS 26.7 and iPadOS 26.7” — https://support.apple.com/en-us/149041. Apple says iOS/iPadOS 26.7 was released September 14, 2026. The bulletin gives impact/fix summaries but no source diffs or enough detail to reconstruct exploitability. [Apple's iOS 26.7 security advisory](https://support.apple.com/en-us/149041)

## Priority 0 — correct source-of-truth mapping

The two previously flagged CVE mappings can now be resolved against Apple’s bulletin:

- **CVE-2026-86876 — CoreMedia.** Apple says a sandboxed process may circumvent sandbox restrictions; an out-of-bounds write was addressed with improved bounds checking. Credit: Chris Bailey / Short Circuit.
- **CVE-2026-86886 — TCC.** Apple says an app may modify protected system files; a path-traversal issue was addressed with improved input validation. Credits include Constantin Clerc and others as listed by Apple.

Do not conflate CVE-2026-86886 with CVE-2026-86887 (Time Zone/privacy) or CVE-2026-86890 (Siri Suggestions/physical access). These are separate entries. [Apple's iOS 26.7 security advisory](https://support.apple.com/en-us/149041)

## Priority 1 — evidence ledger for the current 12 candidates

The following summary records Apple’s public impact/fix language where directly visible. It is not a claim of reproducibility on a particular device or build.

| CVE | Component / public impact summary | Published fix class | Research interpretation |
|---|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder; sandboxed app may execute code with kernel privileges | Race condition; improved state management | High-priority advisory correlation; no trigger or chain inferred |
| CVE-2026-43689 | Kernel permissions issue; malicious app may gain root (from prior collected public-advisory notes; recheck Apple entry) | Additional restrictions (prior notes) | Verify exact Apple entry and version scope before relying on it |
| CVE-2026-84523 | APFS; app may cause system termination or write kernel memory | Out-of-bounds write; improved bounds checking | Public fix class known; no source diff |
| CVE-2026-86876 | CoreMedia; sandbox restrictions may be circumvented | Out-of-bounds write; improved bounds checking | Confirmed against Apple bulletin |
| CVE-2026-86886 | TCC; app may modify protected system files | Path traversal; improved input validation | Confirmed against Apple bulletin |
| CVE-2026-84566 | Kernel; unexpected termination or kernel-memory corruption | Improved memory handling | Exact function/reproducer not disclosed |
| CVE-2026-43687 | Kernel/NFS; malicious NFS server may disclose kernel memory (prior notes) | Recheck exact Apple wording | Network exposure is not equivalent to local privilege escalation |
| CVE-2026-43684 | Kernel; unexpected termination or kernel-memory corruption | Use-after-free; improved memory management | Do not infer exploitability from class alone |
| CVE-2026-43686 | Kernel/NFS; malicious NFS server may cause kernel-memory corruption | Use-after-free; improved memory management | NFS threat model; not a standalone jailbreak |
| CVE-2026-65405 | App may determine kernel memory layout (prior notes) | Memory initialization fix (prior notes) | Information disclosure alone is not code execution |
| CVE-2026-84622 | App with root privileges may read uninitialized kernel memory (prior notes) | Verify exact Apple entry | Prerequisite already includes root; not an initial escalation path |
| CVE-2026-28968 | Kernel; out-of-bounds write, termination or kernel-memory corruption (prior notes) | Verify exact Apple entry | Do not promote without primary-source confirmation |

Evidence labels: “Confirmed against Apple bulletin” means the component and summary above were found in Apple’s bulletin. “Prior notes” means the earlier ledger contains the claim but this update does not independently verify it. Rows marked for recheck remain provisional. [Apple's iOS 26.7 security advisory](https://support.apple.com/en-us/149041)

## Priority 2 — version applicability and device-specific evidence

The existing NVD CPE capture reportedly returns a range ending before 26.7. A broad CPE range can support potential version applicability but does not prove the exact installed build (such as 23G83), that vulnerable code exists on a specific hardware model, exploitability, a usable primitive, that issues can be chained, or that a mitigation is absent.

Keep these as separate ledger fields: vendor_range_match, exact_build_verified, hardware_path_verified, public_fix_detail_available, reproducer_available, exploitability_established. Do not collapse them into one “affected” boolean.

## Priority 3 — safe regression specifications

Use non-weaponized invariants and unit-test abstractions only. Do not attempt malformed kernel-facing inputs or reproduce memory corruption on a live phone.

- **Bounds checking (APFS / CoreMedia):** a parser rejects lengths and offsets outside the enclosing buffer; boundary cases return controlled errors; a mock/parser harness observes no out-of-bounds access.
- **State/race handling (AVEVideoEncoder):** model state transitions under serialized and concurrent scheduling; invalid transitions are rejected and state remains consistent. Do not race the production driver.
- **Use-after-free class (Kernel/NFS):** in a toy object-lifetime model, operations after release are rejected and references cannot outlive ownership. No live NFS exploit or kernel interaction.
- **Path traversal (TCC):** a policy unit test rejects paths resolving outside an authorized root after canonicalization; include symlink and normalization cases in the abstract suite.
- **Memory initialization / disclosure:** newly allocated test objects are initialized before reads; outputs never include sentinel bytes from prior allocations.
- **Permission/entitlement checks:** deny by default; unauthorized callers fail and authorized callers succeed in a mock policy layer.

These are proposed test properties, not assertions about Apple’s internal implementation.

## Priority 4 — repository automation and audit output

The next automation should fetch Apple’s public advisory HTML as a versioned evidence snapshot; parse the 12 exact CVE IDs and require one primary-advisory entry per ID; store component, impact, fix wording, affected-platform statement, publication/update date and source URL; flag absent/duplicate IDs, changed wording and component/impact disagreements; compare NVD version ranges without treating CPE matches as exact-build proof; emit JSON and Markdown reports; and run in GitHub Actions with artifacts. It must not infer a jailbreak path or generate payloads.

## Current blockers (evidence blockers, not exploit blockers)

1. Apple does not publish source-level diffs in the bulletin.
2. Exact device build/hardware applicability is not established by a broad CPE range.
3. Several rows require fresh exact-CVE matches against Apple’s current bulletin and NVD before being promoted to confirmed.
4. No public reproducer or independently validated primitive is established here.
5. A vulnerability chain cannot be inferred from impact descriptions alone.

## Acceptance criteria for the next research pass

- All 12 IDs have exact primary-source matches or are explicitly unresolved.
- Every claim has a URL and capture timestamp.
- Apple and NVD records are stored separately and disagreements are surfaced.
- Unit tests cover parser behavior and ledger consistency only.
- No exploit execution, security bypass, or device modification occurs.
