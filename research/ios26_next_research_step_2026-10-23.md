# Freedom27 — next research step completed: version-evidence reconciliation

Reviewed: 2026-10-23  
Target context: reported iPhone17,4 / iOS 26.6.1 / build 23G83  
Scope: public-source verification and evidence bookkeeping only. No exploit was run; no CVE was cracked; no device was accessed or modified.

## Outcome

The validation ledger now separates candidates with an explicitly captured NVD affected-version range from those where the Apple 26.7 fix context is known but the exact NVD configuration has not yet been captured. This prevents the project from incorrectly treating every advisory entry as a verified affected build.

### Stronger version-range evidence captured

- **CVE-2026-84607 — AVEVideoEncoder:** NVD lists iOS versions below 26.7. This includes the reported 26.6.1 version, but does not demonstrate the exact build or a working race.
- **CVE-2026-43689 — Kernel:** NVD lists iOS/iPadOS versions below 26.7. The published impact is root privilege gain by a malicious app; this does not establish kernel privilege or a jailbreak.
- **CVE-2026-86876 — CoreMedia:** NVD lists iOS/iPadOS versions below 26.7. The advisory's sandbox-impact wording is not proof of a reproducible sandbox escape.
- **CVE-2026-84523 — APFS:** Previously recorded as below 26.7 from the NVD record. Exact build remains unverified.

### Candidates still needing precise configuration capture

CVE-2026-43684, CVE-2026-43686, CVE-2026-65405, and CVE-2026-86886 have been annotated with their source references and explicit uncertainty. Do not mark these as exact-build confirmed until the full NVD affected-software configuration and primary advisory wording have been checked and captured.

## Safe validation status

No candidate has a demonstrated exploit, confirmed primitive, or verified jailbreak chain. The current step establishes version-range evidence only. The next step is to capture each candidate's full NVD configuration and locate public patch/bug references; if none exist, record that limitation rather than infer implementation details.

## Sources

- Apple iOS 26.7 security content: https://support.apple.com/en-us/149041
- NVD CVE-2026-84607: https://nvd.nist.gov/vuln/detail/CVE-2026-84607
- NVD CVE-2026-43689: https://nvd.nist.gov/vuln/detail/CVE-2026-43689
- NVD CVE-2026-86876: https://nvd.nist.gov/vuln/detail/CVE-2026-86876
- NVD CVE-2026-84523: https://nvd.nist.gov/vuln/detail/CVE-2026-84523
