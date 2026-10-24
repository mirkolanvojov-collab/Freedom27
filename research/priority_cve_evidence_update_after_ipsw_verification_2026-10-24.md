# Priority CVE evidence update after exact IPSW verification — 2026-10-24

## Scope and evidence standard

This is a read-only public-source research update for Freedom27's recorded target: iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`. It follows the successful streaming SHA-256 verification recorded in GitHub Actions run https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40046497529.

The firmware digest and size match the pinned values:
- SHA-256: `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`
- Bytes: `11225458130`
- Stream source: Apple CDN URL recorded in `research/reproducible_ipsw_verification.md`
- Firmware file written to runner disk: no
- Device modified: no

A matching stream hash establishes byte-level integrity relative to the pinned digest. It does not prove exploitability or exact-build vulnerable-code reachability.

## Primary-source result

Apple's iOS 26.7/iPadOS 26.7 security bulletin, released 2026-09-14, directly lists all 12 tracked CVEs and describes them as fixed in 26.7: https://support.apple.com/en-us/149041. NVD's CVE-2026-84607 record independently lists the iPhone OS/iPadOS affected range as below 26.7: https://nvd.nist.gov/vuln/detail/CVE-2026-84607. The same version-range boundary is captured for the 12 records in the repository's prior NVD capture.

This gives a strong published version-range match for iOS 26.6.1, and Apple's device scope (iPhone 11 and later) includes iPhone 16 Plus. It does not identify build 23G83 as individually tested, and it does not prove that a vulnerable code path is reachable on the exact device.

## Priority findings

| Priority | CVE | Publicly confirmed | Research assessment | Next safe evidence gate |
|---|---|---|---|---|
| P1 | CVE-2026-84607 | Apple identifies AVEVideoEncoder race condition; sandboxed app may execute code with kernel privileges; fixed via improved state management | Highest research relevance by stated impact. A third-party report proposes a state-consistency guard from comparisons of later binaries, but labels itself AI-generated/not fully human reviewed and does not prove target-build applicability or the CVE-to-code mapping. | Independently validate component identity and version provenance from pinned firmware metadata; seek primary researcher disclosure or checkable patch evidence. Do not infer a race schedule or primitive from the advisory. |
| P1 | CVE-2026-43689 | Apple identifies a kernel permissions issue; malicious app may gain root privileges; fixed by additional restrictions; credits Andreas Jaegersberger and Ro Achterberg (Nosebeard Labs) | Root privilege is not synonymous with kernel privilege. No public patch diff or exact authorization check was established in this review. | Seek primary disclosure or independently checkable public patch evidence; preserve the root-vs-kernel distinction. |
| P2 | CVE-2026-84523 | APFS out-of-bounds write; possible termination or kernel-memory write; improved bounds checking | The advisory does not establish write controllability, code execution, or exact target reachability. | Record APFS component/build provenance and use non-exploitative boundary-property tests only in a controlled model. |
| P2 | CVE-2026-84566 | Kernel memory-handling issue; possible termination or kernel-memory corruption | Corruption impact does not prove control or privilege escalation. | Public patch/invariant evidence, otherwise keep advisory-only. |
| P2 | CVE-2026-43684 | Kernel use-after-free; possible termination or kernel-memory corruption | Object and lifetime invariant are not disclosed in the advisory. | Public technical disclosure or vendor patch evidence; no trigger development. |
| P2 | CVE-2026-43686 | Kernel/NFS use-after-free; malicious NFS server may cause kernel-memory corruption | Requires an NFS-related path; not a demonstrated local entry point. | Validate public prerequisite and component scope; do not test against a daily-use phone or malicious server. |
| P2 | CVE-2026-28968 | Kernel out-of-bounds write; possible termination or kernel-memory corruption | No evidence of controlled write or execution. | Public patch/invariant evidence; abstract bounds tests only. |
| P2 | CVE-2026-86876 | CoreMedia out-of-bounds write; sandboxed process may circumvent sandbox restrictions | Sandbox escape impact is distinct from kernel privilege and is not a complete jailbreak. | Confirm component/build metadata and public technical evidence; no crafted media trigger. |
| P2 | CVE-2026-86886 | TCC path traversal; app may modify protected system files | Advisory impact does not prove arbitrary code execution or kernel access. | Canonical-path authorization model tests and public patch evidence. |
| P3 | CVE-2026-43687 | Kernel/NFS memory disclosure; connecting to malicious NFS server may disclose kernel memory | Disclosure, not execution; NFS prerequisite limits entry-point value. | Public disclosure and exact output/invariant evidence. |
| P3 | CVE-2026-65405 | Kernel memory-layout disclosure | Practical value and exact disclosed data remain unknown. | Public source evidence; do not infer a usable address leak. |
| P4 | CVE-2026-84622 | Kernel uninitialized-memory read; described read requires root privileges | Poor standalone entry point without a separately established root path. | Keep prerequisite explicit; no promotion absent independent root-path evidence. |

## What the evidence supports now

- Exact IPSW byte stream matches the pinned SHA-256 and byte count.
- All 12 CVEs have primary Apple advisory entries and captured NVD version-range evidence below 26.7.
- iOS 26.6.1 is within those published ranges.
- CVE-2026-84607 has the strongest stated impact, but the technical report located is only a hypothesis and does not validate build 23G83.
- CVE-2026-43689 has improved disclosure attribution, but no checkable patch detail.
- Exact-build reachability: 0/12 independently verified.
- Freedom27 reproductions: 0/12.
- Complete jailbreak chain: not verified.

## Next research action

The remaining evidence gap is no longer firmware transfer or checksum calculation. It is exact-build component provenance and patch-level technical evidence. The next non-invasive task should be a reproducible, read-only inventory/comparison of relevant firmware component metadata across pinned builds, recording hashes, build identifiers, extraction-tool versions, and limitations. A string or symbol difference alone must not be treated as proof of CVE attribution. If public evidence does not identify the affected function/invariant, record it as unavailable rather than reconstructing an exploit.

No exploit was executed, no payload was built or run, and no device was accessed or modified.
