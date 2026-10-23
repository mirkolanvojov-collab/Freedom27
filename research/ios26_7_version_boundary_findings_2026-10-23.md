# Freedom27 — public version-boundary findings

**Reviewed:** 2026-10-23  
**Reported target:** iPhone17,4 / iOS 26.6.1 / build 23G83  
**Scope:** public-source version-boundary review only. No CVE was cracked or executed; no device was accessed or modified.

## Findings

### CVE-2026-84607 — AVEVideoEncoder

- Apple advisory: https://support.apple.com/en-us/149041
- NVD record: https://nvd.nist.gov/vuln/detail/cve-2026-84607
- NVD's known-affected-software configuration lists Apple iPhone OS versions below 26.7, with 26.7 as the exclusive upper bound.
- Therefore, the reported software version 26.6.1 falls inside the published version range.
- The record describes a race condition and says a sandboxed app may be able to execute arbitrary code with kernel privileges.
- **Not established:** exact build 23G83 behavior, hardware-specific applicability, reproducibility, control over the race, a usable exploit primitive, or a complete jailbreak chain.

This is a version-range result, not an exploit result.

### CVE-2026-84523 — APFS

- NVD record: https://nvd.nist.gov/vuln/detail/cve-2026-84523
- The candidate ledger records NVD's stated affected range as iOS versions below 26.7.
- Apple describes an out-of-bounds write that may cause unexpected system termination or write kernel memory.
- **Not established:** whether an attacker can control the write, exact-build behavior, reliability, or code execution.

### CVE-2026-43689 — Kernel

- Apple advisory: https://support.apple.com/en-us/149041
- Secondary advisory record: https://github.com/advisories/GHSA-4jgx-p7cx-g39r
- The public description says a permissions issue was fixed in iOS 26.7 and that a malicious app may gain root privileges. The secondary record lists affected versions as unknown.
- **Conclusion:** do not assign a precise affected range based only on the fix release. The target-version assessment remains unestablished pending a better primary/version record.

### CVE-2026-86876 — CoreMedia; CVE-2026-86886 — TCC

- Apple advisory: https://support.apple.com/en-us/149041
- NVD index: https://nvd.nist.gov/vuln/search?cpeFilterMode=cpe&cpeName=cpe%3A2.3%3Ao%3Aapple%3Aiphone_os%3A18.1.1%3A%2A%3A%2A%3A%2A%3A%2A%3A%2A%3A%2A%3A%2A&resultType=records
- Public descriptions establish high-level impacts and fixes: CoreMedia out-of-bounds write/sandbox restriction bypass; TCC path traversal/protected-file modification.
- This review did not capture a precise CPE affected-version boundary for either record.
- **Conclusion:** target-version applicability remains unestablished; do not turn the fixed-release statement into a stronger claim.

## Evidence boundary

The reported target version is older than iOS 26.7, and Apple states these issues were fixed in 26.7. For CVE-2026-84607 and CVE-2026-84523, the NVD version configuration provides direct version-range evidence that includes 26.6.1. For the other reviewed candidates, the exact affected-version range remains unverified in this pass.

None of these version records demonstrates that an exploit works. Public advisory language such as “may be able to” is an impact statement, not proof of a reproducible attack path.

## Next validation step

1. Obtain and archive the exact affected-software configuration for each remaining CVE from its individual NVD record.
2. Locate public patch/bug references and record them only when verifiable.
3. Where a public patch describes a discrete invariant, create a benign unit test or synthetic model test for that invariant.
4. Leave exploitability and exact-build applicability unestablished unless direct, reproducible evidence supports a stronger conclusion.

No kernel corruption, sandbox escape, protected-file modification, or exploit execution is part of this work.
