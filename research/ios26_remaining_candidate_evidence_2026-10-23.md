# Freedom27 — Remaining iOS 26.7 Candidate Evidence Review

Reviewed: 2026-10-23  
Target context: iPhone17,4 / iOS 26.6.1 / build 23G83 (user-reported; exact-build verification not performed)

## What this pass established

- **CVE-2026-43684 (Kernel):** public CVE record explicitly lists affected iOS/iPadOS versions below 26.7. Described as a use-after-free; advisory-level impact includes system termination or kernel-memory corruption.
- **CVE-2026-43686 (Kernel/NFS):** public CVE record lists iOS/iPadOS versions below 26.7. The public summary says connecting to a malicious NFS server may lead to kernel-memory corruption. This is a prerequisite/risk note, not a recommendation to run a malicious server against a personal device.
- **CVE-2026-84523 (APFS):** NVD explicitly lists iPhone OS and iPadOS CPE upper bounds excluding 26.7; range evidence supports 26.6.1 as within the listed version range.
- **CVE-2026-65405 (Kernel):** a secondary public record corroborates the fix in 26.7 and the kernel-layout disclosure summary, but exact NVD CPE configuration remains unrecorded. Status intentionally remains pending.
- **CVE-2026-84566, CVE-2026-84622, CVE-2026-28968, and CVE-2026-86886:** this search pass did not capture reliable exact NVD affected-software configuration. They remain unresolved; release timing alone is not treated as proof.

## Sources

- Apple iOS/iPadOS 26.7 security advisory: https://support.apple.com/en-us/149041
- NVD CVE-2026-84523 (includes affected CPE range): https://nvd.nist.gov/vuln/detail/CVE-2026-84523
- Public CVE record for CVE-2026-43684: https://db.gcve.eu/vuln/ncsc-2026-0371?page=2
- Public CVE record for CVE-2026-43686: https://db.gcve.eu/vuln/ncsc-2026-0370
- Secondary record for CVE-2026-65405: https://vulnerability.circl.lu/vuln/cve-2026-65405
- Apple security releases list: https://support.apple.com/en-us/100100

## Interpretation and limits

A version range below 26.7 is consistent with the reported iOS 26.6.1 version, but it does **not** establish the exact build's vulnerability state, a reliable trigger, a controllable primitive, successful privilege escalation, or a jailbreak chain. Apple advisory descriptions summarize impact and patch category, not full reproduction details.

No exploit was executed. No CVE was cracked. The target device was not accessed or modified. No exploit chain is claimed.

## Next research action

Capture each remaining NVD record's complete affected-software configuration and any publicly linked patch/bug references. Only then update each status. Where public technical details are absent, keep the candidate as evidence-incomplete and use only non-destructive model-level regression tests based on documented invariants.
