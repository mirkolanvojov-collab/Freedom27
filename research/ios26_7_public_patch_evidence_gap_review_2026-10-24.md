# Public patch-evidence gap review — 2026-10-24

## Scope

This is the next read-only step after NVD capture and Apple advisory cross-check: compare public Apple patch descriptions against what would be required to validate the reported security invariant. This review uses only the public Apple iOS 26.7 bulletin and existing CVE Program / NVD records. It does not infer hidden implementation details from the fix wording, and it does not attempt exploitation.

Primary source: https://support.apple.com/en-us/149041

## Result

The Apple bulletin provides high-level fix descriptions, but no source diff, affected function, patch commit, reproducer, or exact invariant for these 12 entries in the public advisory text. Accordingly, the missing piece is **technical patch-level evidence**, not more version-range data.

| CVE | Publicly stated fix / issue | What remains unproven |
|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder race condition; improved state management | Which state invariant was violated, whether the race is reachable/reproducible on the target build, and whether any controllable kernel primitive exists |
| CVE-2026-43689 | Kernel permissions issue; additional restrictions | Which permission check changed, relevant entitlement/caller context, and whether the issue yields root on the target build |
| CVE-2026-84523 | APFS out-of-bounds write | Bounds invariant, reachable input path, and whether writes are controllable |
| CVE-2026-86876 | CoreMedia out-of-bounds write | Bounds invariant and whether the public sandbox-impact statement applies to the target build/path |
| CVE-2026-86886 | TCC path traversal | Path normalization/authorization invariant and exact protected-file boundary |
| CVE-2026-84566 | Kernel memory handling | Affected object/state invariant and whether corruption is controllable beyond denial of service |
| CVE-2026-43687 | Kernel/NFS memory disclosure | Disclosure source and conditions; public impact is disclosure, not execution |
| CVE-2026-43684 | Kernel use-after-free | Object lifetime invariant and reachability conditions |
| CVE-2026-43686 | Kernel/NFS use-after-free | Object lifetime invariant and NFS-specific reachability conditions |
| CVE-2026-65405 | Kernel memory initialization / layout disclosure | Which data is exposed and whether the disclosure is useful on the target build |
| CVE-2026-84622 | Root-context uninitialized kernel-memory read | Read invariant; advisory says root privileges are already required, so this is not established as an initial entry point |
| CVE-2026-28968 | Kernel out-of-bounds write | Bounds invariant and whether any corruption is controllable beyond denial of service |

## Candidate triage update

This evidence does not justify selecting a CVE as a working exploit. For research prioritization only:

- **Highest relevance for further public-source review:** CVE-2026-84607 because Apple explicitly states kernel-privilege code execution as impact; the actual race conditions and required primitive remain unknown.
- **Potentially relevant but currently under-specified:** CVE-2026-43689 (root privilege), CVE-2026-86876 (sandbox restrictions), CVE-2026-86886 (protected files). These are distinct outcomes and must not be treated as equivalent to a jailbreak.
- **Memory-corruption candidates with no demonstrated control:** CVE-2026-84523, CVE-2026-84566, CVE-2026-43684, CVE-2026-43686, CVE-2026-28968.
- **Information disclosure / prerequisite-limited:** CVE-2026-43687, CVE-2026-65405, CVE-2026-84622. CVE-2026-43687 requires a malicious NFS server according to the public wording; CVE-2026-84622's described read requires root.

These are triage labels, not a claim that the bugs are reproducible or usable. No exploit was executed and no device was accessed or modified.

## Exact next step

Search for public researcher write-ups, source diffs, patch commits, or vendor clarifications that provide a verifiable technical invariant. If none is public, keep the invariant marked `unavailable_publicly`; do not reverse-engineer a weaponized exploit from the impact summary. A safe validation artifact can then be written as a non-exploitative regression specification describing the expected security property, without a trigger or memory-corruption payload.

## Evidence references

- Apple iOS 26.7 / iPadOS 26.7 security content: https://support.apple.com/en-us/149041
- CVE Program records and NVD raw capture artifact are linked in `research/ios26_7_candidate_validation_results_2026-10-23.json` and `research/nvd_affected_configuration_capture_2026-10-23.md`.
