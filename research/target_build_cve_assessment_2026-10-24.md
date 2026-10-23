# Exact-target CVE version-range assessment — 2026-10-24

## Decision

**All 12 tracked CVEs match the NVD iPhone OS version range below 26.7, which includes the recorded target release iOS 26.6.1.** Apple's iOS 26.7 advisory lists all 12 and states the relevant entries apply to iPhone 11 and later, which includes iPhone 16 Plus.

This is a strong **version-range match**, not proof that each vulnerability is reachable on exact build 23G83, not proof of exploitability, and not a working jailbreak chain. The NVD CPE range does not pin an exact iOS build or demonstrate a code path on this device.

## Target and source provenance

- Device: iPhone 16 Plus (`iPhone17,4`)
- Reported OS/build: iOS 26.6.1 / `23G83`
- Primary Apple bulletin: [iOS 26.7 and iPadOS 26.7 security content](https://support.apple.com/en-us/149041), released September 14, 2026.
- NVD capture workflow: [run 40041118442](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40041118442)
- Captured records: 12/12 CVE endpoints and 12/12 CPE Match endpoints succeeded (HTTP 200); zero failed records.
- Artifact SHA-256: `e21723d4911c67ca86efbfa74b845c595070ca39ca80856bf1d8e4af3fd9f236`
- Machine-readable detail: [`target_build_cve_assessment_2026-10-24.json`](target_build_cve_assessment_2026-10-24.json)

## CVE-by-CVE result

| CVE | Apple component / impact | NVD iPhone OS range | Target version-range result | Priority / key limitation |
|---|---|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder: A sandboxed app may execute arbitrary code with kernel privileges | < 26.7 | Match (26.6.1) | P1; sandboxed_app |
| CVE-2026-43689 | Kernel: A malicious app may gain root privileges | < 26.7 | Match (26.6.1) | P1; malicious_app |
| CVE-2026-84523 | APFS: An app may cause system termination or write kernel memory | < 26.7 | Match (26.6.1) | P2; local_app |
| CVE-2026-86876 | CoreMedia: A sandboxed process may circumvent sandbox restrictions | < 26.7 | Match (26.6.1) | P2; sandboxed_process |
| CVE-2026-86886 | TCC: An app may modify protected system files | < 26.7 | Match (26.6.1) | P2; app |
| CVE-2026-84566 | Kernel: A local attacker may cause system termination or corrupt kernel memory | < 26.7 | Match (26.6.1) | P2; local_attacker |
| CVE-2026-43687 | Kernel: Connecting to a malicious NFS server may disclose kernel memory | < 26.7 | Match (26.6.1) | P3; malicious_nfs_server |
| CVE-2026-43684 | Kernel: An app may cause system termination or corrupt kernel memory | < 26.7 | Match (26.6.1) | P2; app |
| CVE-2026-43686 | Kernel: Connecting to a malicious NFS server may lead to kernel-memory corruption | < 26.7 | Match (26.6.1) | P2; malicious_nfs_server |
| CVE-2026-65405 | Kernel: An app may determine kernel memory layout | < 26.7 | Match (26.6.1) | P3; app |
| CVE-2026-84622 | Kernel: An app with root privileges may read uninitialized kernel memory | < 26.7 | Match (26.6.1) | P4; root_privileges |
| CVE-2026-28968 | Kernel: An app may cause system termination or corrupt kernel memory | < 26.7 | Match (26.6.1) | P2; app |

## Interpretation and remaining proof

1. **Version boundary:** Each captured NVD CVE 2.0 record contains an iPhone OS CPE with `versionEndExcluding: 26.7`. Since the recorded target version is 26.6.1, it falls inside that published range.
2. **Hardware family:** Apple's bulletin scope for each listed entry is iPhone 11 and later; the iPhone 16 Plus is within that family.
3. **Exact build:** The advisory/CPE evidence does not independently prove that the vulnerable code is present and reachable in build 23G83. No device-level test or independent reproduction was performed.
4. **Chain relevance:** CVE-2026-84607 has the strongest stated impact (sandboxed app to kernel-privileged code execution); CVE-2026-43689 reports root-privilege impact. Neither has been reproduced by Freedom27. CVE-2026-84622 explicitly requires root privileges, while CVE-2026-43687 and CVE-2026-43686 involve a malicious NFS server; those prerequisites matter when evaluating entry-point value.
5. **No weaponization:** This review records source-backed version metadata and abstract constraints only. It adds no exploit trigger, payload, race choreography, or kernel-memory manipulation.

## Outcome

- CVE IDs matched to Apple primary advisory: **12/12**
- NVD CVE records captured successfully: **12/12**
- NVD CPE Match endpoints captured successfully: **12/12**
- NVD iPhone OS version-range matches for 26.6.1: **12/12**
- Exact-build reachability independently verified: **0/12**
- Exploitability reproduced by Freedom27: **0/12**
- Complete jailbreak chain verified: **No**
- Device modified / exploit run: **No**

The next evidence milestone is exact-build technical confirmation from primary source material or independent, non-invasive reproduction. Do not infer a usable primitive from the advisory impact alone, and do not run exploit code on the daily-use phone based on this assessment.
