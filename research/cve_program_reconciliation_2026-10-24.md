# CVE Program, Apple advisory, and NVD reconciliation — 2026-10-24

## Result

I reviewed all 12 selected CVE Program records at a pinned upstream snapshot and cross-checked them against Apple's iOS 26.7 advisory and the previously captured NVD CVE/CPE records.

- **12/12** records are published by Apple's CNA identity in the CVE Program list.
- **12/12** records link to Apple's iOS 26.7 advisory.
- **12/12** have an iOS/iPadOS affected-version range with an upper boundary below 26.7.
- **12/12** have successful CVE and CPE Match capture entries in NVD workflow [40041118442](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40041118442).
- **0/12** have independent confirmation for exact build 23G83; **0/12** have exploitability established by Freedom27.

## Sources and provenance

- Apple primary advisory: https://support.apple.com/en-us/149041
- CVE Program snapshot: [CVEProject/cvelistV5 commit c21430318b4b48252dd6ba344df26d60e6354f12](https://github.com/CVEProject/cvelistV5/commit/c21430318b4b48252dd6ba344df26d60e6354f12)
- NVD capture run: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40041118442
- NVD artifact SHA-256: `e21723d4911c67ca86efbfa74b845c595070ca39ca80856bf1d8e4af3fd9f236`
- Machine-readable record-level reconciliation: [cve_program_reconciliation_2026-10-24_canonical.json](cve_program_reconciliation_2026-10-24_canonical.json)

The JSON stores the canonical CVE Program impact wording, record state, Apple CNA attribution, publication/update timestamps, iOS/iPadOS version boundaries, Apple-advisory reference presence, and NVD capture provenance.

## Per-record result

| CVE | Component | Canonical CVE Program impact | Published iOS/iPadOS upper bound |
|---|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder | Sandboxed app may execute code with kernel privileges | `<26.7` |
| CVE-2026-43689 | Kernel | Malicious app may gain root privileges | `<26.7` |
| CVE-2026-84523 | APFS | App may cause system termination or write kernel memory | `<26.7` |
| CVE-2026-86876 | CoreMedia | Sandboxed process may circumvent sandbox restrictions | `<26.7` |
| CVE-2026-86886 | TCC | App may modify protected system files | `<26.7` |
| CVE-2026-84566 | Kernel | Local attacker may cause termination or corrupt kernel memory | `<26.7` |
| CVE-2026-43687 | Kernel / NFS | Malicious NFS server may disclose kernel memory | `<26.7` |
| CVE-2026-43684 | Kernel | App may cause termination or corrupt kernel memory | `<26.7` |
| CVE-2026-43686 | Kernel / NFS | Malicious NFS server may cause kernel-memory corruption | `<26.7` |
| CVE-2026-65405 | Kernel | App may determine kernel memory layout | `<26.7` |
| CVE-2026-84622 | Kernel | App with root privileges may read uninitialized kernel memory | `<26.7` |
| CVE-2026-28968 | Kernel | App may cause termination or corrupt kernel memory | `<26.7` |

The table shortens descriptions for readability; the JSON retains canonical wording. CVE-2026-43684 has only the `<26.7` iOS/iPadOS affected range in the pinned CVE Program record. Most of the other records list both `<26.7` and `<27` ranges. This difference does **not** change the conclusion for iOS 26.6.1 because all twelve records explicitly include a range below 26.7.

## Reconciliation interpretation

1. **CVE Program vs Apple advisory:** all twelve records are published under Apple's CNA identity and cite the iOS 26.7 advisory. The high-level impacts align with the advisory's wording. The CVE Program record provides the canonical impact statement; Apple's advisory provides the component context and fix summary.
2. **CVE Program vs NVD:** the pinned CVE Program records and NVD capture agree on the relevant iOS 26.7 upper boundary. NVD capture success is evidence of successful retrieval, not a separate reproduction of the issue.
3. **Target version:** iOS 26.6.1 is below 26.7, so the target matches the published version ranges. These records do not identify build 23G83 specifically.
4. **No exploitability inference:** advisory impacts such as kernel-privileged code execution or root privilege are descriptions of potential impact, not proof that Freedom27 has a trigger, reliable primitive, mitigation bypass, or usable jailbreak chain.
5. **Prerequisites remain important:** CVE-2026-84622's impact requires root privileges; CVE-2026-43687 and CVE-2026-43686 refer to interaction with a malicious NFS server. Neither class should be mislabeled as a demonstrated initial entry point.

## Open blockers

- Public patch diffs, affected functions, and exact security invariants remain unavailable in the reviewed source set for these candidates.
- No independent build-specific source evidence or non-invasive reproduction establishes vulnerability presence/reachability on 23G83.
- No candidate has been reproduced by Freedom27 and no full jailbreak chain is verified.

The correct next step is to monitor the pinned source records for updates and look for credible, explicitly published patch notes or researcher write-ups. If no patch-level evidence is public, record that gap and do not infer hidden implementation details from the impact summary.

## Safety and scope

This was read-only public-source reconciliation. No exploit was executed and no device was accessed, installed on, downgraded, restored, or modified.
