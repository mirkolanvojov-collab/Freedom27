# Public patch / bug-reference search — 2026-10-23

## Scope

Read-only review of public sources for the 12 selected iOS 26.7 CVE candidates. The purpose is to identify publicly documented bug IDs, patch commits, or technical invariants that would support a safe regression-test plan. This review does not retrieve private Apple source, execute proof-of-concept code, or test the target device.

## Source hierarchy used

1. Apple iOS 26.7 / iPadOS 26.7 security bulletin: https://support.apple.com/en-us/149041
2. Official CVE Program record repository: https://github.com/CVEProject/cvelistV5
3. NVD records and the previously captured raw API artifact in the project.
4. Secondary vulnerability indexes were used only as discovery aids, not as proof of a patch commit or reproducible exploit.

Apple explains that it does not disclose, discuss, or confirm security issues until an investigation has occurred and patches or releases are available. The bulletin gives component, impact, fix-summary wording, and researcher attribution where available; it does not publish a source patch diff for the selected candidates.

## Candidate-by-candidate public-reference result

| CVE | Public technical reference found in this pass | What the public source supports | Remaining evidence gap |
|---|---|---|---|
| CVE-2026-84607 | Apple AVEVideoEncoder entry; researcher attribution | Race condition; improved state management; sandboxed app may execute code with kernel privileges | No public patch commit, detailed trigger, or synchronization invariant identified in reviewed sources. |
| CVE-2026-43689 | Apple Kernel entry; researcher attribution | Permissions issue; additional restrictions; malicious app may gain root privileges | No public patch commit or exact authorization invariant identified. |
| CVE-2026-84523 | Apple APFS entry; public CVE record | Out-of-bounds write / possible system termination or kernel-memory write; bounds-checking fix summary | No public patch commit or safe, precise bounds invariant identified. |
| CVE-2026-86876 | Apple CoreMedia entry; researcher attribution | Out-of-bounds write; bounds-checking fix; sandbox restrictions may be circumvented | No public patch commit or precise sandbox boundary / trigger documented in reviewed sources. |
| CVE-2026-86886 | Apple TCC entry; researcher attribution | Path traversal; improved input validation; protected system files may be modified | No public patch commit or precise canonicalization/authorization invariant documented. |
| CVE-2026-84566 | Apple Kernel entry; researcher attribution | Improved memory handling; system termination or kernel-memory corruption | No public patch commit, allocation/lifetime detail, or regression invariant identified. |
| CVE-2026-43687 | Apple Kernel/NFS entry; researcher attribution | Connecting to a malicious NFS server may disclose kernel memory | NFS prerequisite is explicit; no public patch commit or exact disclosure invariant identified. |
| CVE-2026-43684 | Apple Kernel entry; researcher attribution | Use-after-free; improved memory management; possible termination or kernel-memory corruption | No public patch commit or precise object-lifetime invariant identified. |
| CVE-2026-43686 | Apple Kernel/NFS entry; researcher attribution | Use-after-free; NFS connection prerequisite; possible kernel-memory corruption | No public patch commit or precise lifetime invariant identified. |
| CVE-2026-65405 | Apple Kernel entry; researcher attribution | Kernel-memory-layout disclosure; initialization-related fix wording in public records | No public patch commit or precise initialization invariant identified in primary sources reviewed. |
| CVE-2026-84622 | Apple Kernel entry; researcher attribution | An app with root privileges may read uninitialized kernel memory | Root is a prerequisite for the stated impact; no public patch commit or precise initialization invariant identified. |
| CVE-2026-28968 | Apple Kernel entry; public CVE record | Out-of-bounds write; possible termination or kernel-memory corruption; bounds-checking fix | No public patch commit or precise bounds invariant identified. |

**Important:** “No public reference identified in this pass” is deliberately narrower than “no reference exists.” It means the reviewed public advisory/CVE sources did not provide a patch commit or enough technical detail to establish a testable invariant.

## Public Bugzilla / patch-link distinction

Apple's bulletin does expose specific WebKit Bugzilla identifiers for some other CVEs in the same release, but that does not establish a corresponding public bug identifier for these 12 candidates. No matching Apple-source patch diff or explicit bug tracker identifier was confirmed for the 12 candidates in the sources reviewed here. Contributor names in the bulletin are attribution, not patch references.

A secondary vulnerability index advertises a public PoC for CVE-2026-65405, but its page does not provide independently verified exploit code or a primary-source patch reference in the content reviewed for this report. It is therefore **not** treated as validated PoC evidence and is not used as a basis for exploit testing.

## Outcome and next safe gate

Current result: all 12 remain **advisory/CVE-record only for technical reproduction purposes**. The published version ranges are relevant to 26.6.1, but exact build 23G83 applicability and exploitability are unverified.

Do not advance a candidate to a device test or exploit implementation until public evidence supplies a narrow, testable invariant. If such evidence later appears, the next safe deliverable is a non-privileged model/unit test that demonstrates the invariant without kernel memory access, sandbox escape, privilege escalation, or a live malicious server.

## Sources

- Apple iOS 26.7 / iPadOS 26.7 security bulletin: https://support.apple.com/en-us/149041
- Official CVE Program records: https://github.com/CVEProject/cvelistV5
- NVD evidence capture artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40029354991/artifacts/12534521313
- Project candidate ledger: https://github.com/mirkolanvojov-collab/Freedom27/blob/main/research/ios26_7_candidate_validation_results_2026-10-23.json

## Safety status

No exploit executed; no vulnerability weaponized; no device accessed or modified.
