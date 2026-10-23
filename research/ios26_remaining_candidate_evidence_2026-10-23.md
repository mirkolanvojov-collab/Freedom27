# Freedom27 — Remaining iOS 26.7 Candidate Evidence Review

Reviewed: 2026-10-23  
Target context: iPhone17,4 / iOS 26.6.1 / build 23G83 (user-reported; exact-build verification not performed)

## What this pass established

- **CVE-2026-43684 (Kernel):** public CVE record explicitly lists affected iOS/iPadOS versions below 26.7. Described as a use-after-free; advisory-level impact includes system termination or kernel-memory corruption.
- **CVE-2026-43686 (Kernel/NFS):** public CVE record lists iOS/iPadOS versions below 26.7. The public summary says connecting to a malicious NFS server may lead to kernel-memory corruption. This is a prerequisite/risk note, not a recommendation to run a malicious server against a personal device.
- **CVE-2026-84523 (APFS):** NVD explicitly lists iPhone OS and iPadOS CPE upper bounds excluding 26.7; range evidence supports 26.6.1 as within the listed version range.
- **CVE-2026-65405 (Kernel):** the secondary record corroborates the fix in 26.7 and the kernel-layout disclosure summary. The later direct NVD capture also archived this candidate's CVE and CPE Match JSON; exact build 23G83 and exploitability remain unverified.
- **CVE-2026-84566, CVE-2026-84622, CVE-2026-28968, and CVE-2026-86886:** this initial search pass did not capture direct NVD affected-software configuration. A later workflow captured the raw CVE and CPE Match JSON for all four (and the other eight candidates). They remain unresolved for exact-build applicability and exploitability; release timing alone is not treated as proof.

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

Reconcile the archived NVD CVE/CPE payloads against Apple's advisory and CVE Program records, then continue searching for publicly linked patch/bug references. The raw capture task is complete; the exact-build applicability, exploit primitive, and complete-chain gates remain blocked. Where public technical details are absent, keep the candidate evidence-incomplete and use only non-destructive model-level regression tests based on documented invariants.


## Follow-up NVD capture evidence

The later workflow captured CVE JSON and CPE Match JSON for all 12 candidates (HTTP 200 for every request): https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40038959123. Raw artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40038959123/artifacts/12538253226. ZIP SHA-256: `4885397b1c735aa870ee3c0c3ff76819d72a1f90b44e1aec58788421827fc56b`.
