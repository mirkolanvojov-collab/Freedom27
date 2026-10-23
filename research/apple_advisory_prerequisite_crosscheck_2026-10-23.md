# Apple advisory and prerequisite cross-check — 2026-10-23

## Purpose and limits

This is a read-only, source-based triage pass for the 12 Freedom27 candidates against Apple's iOS 26.7 / iPadOS 26.7 security bulletin. It extracts the publicly stated component, impact, and high-level precondition where the advisory makes one explicit. It is not a reproduction guide. No exploit was run, no device was accessed or modified, and no private or non-public patch material was used.

## Primary source

Apple, “About the security content of iOS 26.7 and iPadOS 26.7,” released September 14, 2026:
https://support.apple.com/en-us/149041

The bulletin states the listed issues were addressed in 26.7. NVD records independently show the iPhone OS/iPadOS CPE upper bound excluding 26.7 for the candidate set; this makes 26.6.1 a published version-range match, not proof for exact build 23G83 or proof of exploitability.

## Candidate triage

| CVE | Apple-listed component / issue | Publicly stated impact | High-level prerequisite indicated by public wording | Research interpretation |
|---|---|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder; race condition | Sandboxed app may execute arbitrary code with kernel privileges | Local sandboxed app; race condition | Potentially relevant to kernel-privilege research, but no race schedule, controllability, or build-specific validation established. |
| CVE-2026-43689 | Kernel; permissions / additional restrictions | Malicious app may gain root privileges | Local malicious app | Root-privilege impact is stated, but root and kernel privilege are not interchangeable claims; no primitive or chain is established. |
| CVE-2026-84523 | APFS; out-of-bounds write | App may cause unexpected system termination or write kernel memory | Local app interacting with the affected APFS path (exact trigger not disclosed in bulletin summary) | Kernel-memory write wording is not proof of controlled write or code execution. |
| CVE-2026-86876 | CoreMedia; out-of-bounds write | Sandboxed process may circumvent sandbox restrictions | Process handling affected media path; exact trigger unspecified | Sandbox escape is a distinct goal from kernel privilege; no further impact should be inferred. |
| CVE-2026-86886 | TCC; path traversal / input validation | App may modify protected system files | App reaches affected TCC/path-handling logic | Protected-file modification does not by itself establish arbitrary code execution or kernel access. |
| CVE-2026-84566 | Kernel; memory handling | Local attacker may cause system termination or corrupt kernel memory | Local access; exact trigger unspecified | Possible memory-corruption candidate, but no control, reliability, or privilege escalation is demonstrated. |
| CVE-2026-43687 | Kernel/NFS; memory handling | Connecting to a malicious NFS server may disclose kernel memory | Connection to a malicious NFS server | Requires an NFS/network setup and the affected code path; do not expose a daily-use phone to a malicious server. Public impact is disclosure, not execution. |
| CVE-2026-43684 | Kernel; use-after-free | Local attacker may cause system termination or corrupt kernel memory | Local access; exact trigger unspecified | A lifetime bug is named, but trigger, controllability, and privilege effect remain unknown. |
| CVE-2026-43686 | Kernel/NFS; use-after-free | Connecting to a malicious NFS server may cause kernel-memory corruption | Connection to a malicious NFS server | NFS prerequisite matters; corruption wording does not establish controlled execution. |
| CVE-2026-65405 | Kernel; information disclosure | May reveal kernel memory layout | Local access implied by app/kernel context; exact trigger unspecified | Layout disclosure could be a supporting information primitive in theory, but no usable leak or chain compatibility is established. |
| CVE-2026-84622 | Kernel; uninitialized-memory read | Requires root privileges to read uninitialized kernel memory | Root privileges already required | Poor candidate as an initial privilege-escalation entry point absent an independent root path; disclosure impact only. |
| CVE-2026-28968 | Kernel; out-of-bounds write | App may cause system termination or corrupt kernel memory | Local app | Kernel-memory corruption is not proof of controllability, code execution, or jailbreak feasibility. |

**Attribution note:** the table's impact wording is paraphrased from Apple's bulletin and the candidate ledger. For CVE-2026-84523, 86876, 86886, 43689, 43687, 43684, 84566, 65405, 84622, 28968, and 84607, the component/impact summaries were cross-checked against the Apple bulletin at the source URL above. The public advisory gives concise impact and fix summaries, not full exploit prerequisites; where the exact trigger is not specified, the table explicitly says so rather than guessing.

## What this pass establishes

1. The candidates have materially different security outcomes: kernel-privilege execution (84607), root privilege (43689), sandbox restriction bypass (86876), protected-file modification (86886), memory disclosure (43687 / 65405 / 84622), and kernel memory corruption or termination (84523 / 84566 / 43684 / 43686 / 28968).
2. The NFS candidates (43687 and 43686) have a clear environmental prerequisite in the public wording: connection to a malicious NFS server. CVE-2026-84622 explicitly requires root privileges for the described read. Those prerequisites should lower their priority as standalone entry points unless independent evidence changes the picture.
3. A CVE's advisory impact is not evidence that the primitive is controllable, reachable on this hardware/build, repeatable, or composable into a jailbreak.
4. Apple states these issues were fixed in iOS/iPadOS 26.7. NVD's upper bound excluding 26.7 supports a version-range match for 26.6.1. The user's reported build 23G83 was not independently inspected, and no on-device testing was performed.

## Safe next research step

For each candidate, search only public vendor/research references for a bug identifier, patch discussion, or documented invariant. If no public technical detail exists, mark it “advisory-only / prerequisite unresolved” rather than attempting to trigger it. Suitable validation at this stage is a non-exploitative checklist or model-level regression test of a documented invariant, not kernel-memory corruption, sandbox escape, or privilege escalation on the target device.

## Safety and evidence status

- Read-only public-source review only.
- No exploit executed or weaponized.
- No CVE “cracked.”
- No device accessed or modified.
- Exact build applicability and exploitability remain unverified.
- NVD raw-response artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40029354991/artifacts/12534521313


## Follow-up: public patch-detail and invariant check — 2026-10-24

### Evidence located

- NVD's record for CVE-2026-84607 gives the public description “A race condition was addressed with improved state management,” identifies CWE-362, and links to Apple's security-content bulletin. It does not disclose a public source diff, precise state invariant, race window, or reproducible trigger. Source: https://nvd.nist.gov/vuln/detail/cve-2026-84607
- NVD's iOS 26.7 candidate listing includes CVE-2026-86876 and describes an out-of-bounds write fixed with improved bounds checking; its stated outcome is that a sandboxed process may circumvent sandbox restrictions. Source: https://nvd.nist.gov/vuln/search?cpeFilterMode=cpe&cpeName=cpe%3A2.3%3Ao%3Aapple%3Aiphone_os%3A18.1.1%3A%2A%3A%2A%3A%2A%3A%2A%3A%2A%3A%2A%3A%2A&resultType=records
- NVD documents that CVE records can be awaiting enrichment or enriched, and that NVD's enrichment includes reference links, CWE, and CPE applicability data; lack of further detail on a page should not be interpreted as proof the bug lacks technical detail elsewhere. Source: https://nvd.nist.gov/vuln/vulnerability-status

### Result

The current public vendor/NVD summaries support only high-level remediation categories (state management, bounds checking, input validation, memory management, and permissions restrictions). They do not expose enough implementation detail to write a grounded patch-invariant test or verify the exact iPhone build. No patch diff or independent technical write-up was found in this pass for the 12-candidate set. This is an evidence gap, not a claim that no such source exists.

### Missing pieces appended to the existing ledger

For each candidate, future research should add one or more of:
1. Public upstream source/patch diff or Apple security research note identifying the corrected invariant.
2. Independent technical write-up tying the same bug identifier to a specific affected component and OS branch.
3. Build provenance for the user's exact reported build `23G83` and a vendor-supported mapping to iOS 26.6.1.
4. A safe, non-exploitative regression test of the documented invariant, where source code and a legitimate test harness are available.

### Candidate priority adjustment

- **Highest research priority (public impact suggests kernel privilege / kernel memory relevance):** CVE-2026-84607, CVE-2026-43689, CVE-2026-84523, CVE-2026-84566, CVE-2026-43684, CVE-2026-28968. This is prioritization for further public-source evidence only, not an exploitability ranking.
- **Separate sandbox/file-protection outcomes:** CVE-2026-86876 and CVE-2026-86886. Do not assume these provide kernel privilege escalation.
- **Prerequisite/utility concerns:** CVE-2026-43687 and CVE-2026-43686 require a malicious NFS server in the published summary; CVE-2026-84622's stated read requires root privileges; CVE-2026-65405 is an information-disclosure candidate. These are not established as standalone initial entry points.

### Status

No missing source diff, invariant, exact-build confirmation, or regression test was fabricated. The next step is to attach actual public patch evidence if found; until then, the candidates remain advisory-level rather than technically validated.
