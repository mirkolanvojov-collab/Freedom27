# Freedom27 — next research step completed: version-evidence reconciliation

Reviewed: 2026-10-23  
Target context: reported iPhone17,4 / iOS 26.6.1 / build 23G83  
Scope: public-source verification and evidence bookkeeping only. No exploit was run; no CVE was cracked; no device was accessed or modified.

## Outcome

The original validation ledger separated candidates whose NVD affected-version range had been captured from those still awaiting direct configuration data. A later GitHub Actions run completed the direct NVD capture for all 12 candidates; this update supersedes the interim collection status without changing the exact-build or exploitability conclusions.

### Stronger version-range evidence captured

- **CVE-2026-84607 — AVEVideoEncoder:** NVD lists iOS versions below 26.7. This includes the reported 26.6.1 version, but does not demonstrate the exact build or a working race.
- **CVE-2026-43689 — Kernel:** NVD lists iOS/iPadOS versions below 26.7. The published impact is root privilege gain by a malicious app; this does not establish kernel privilege or a jailbreak.
- **CVE-2026-86876 — CoreMedia:** NVD lists iOS/iPadOS versions below 26.7. The advisory's sandbox-impact wording is not proof of a reproducible sandbox escape.
- **CVE-2026-84523 — APFS:** Previously recorded as below 26.7 from the NVD record. Exact build remains unverified.

### Direct configuration capture completed

The latest official NVD workflow captured CVE 2.0 JSON and CPE Match JSON for all 12 candidates. Each of the 24 requests returned HTTP 200 and the raw responses were uploaded as a 25-file artifact. The data supports version-range review, not confirmation of exact build 23G83, a usable exploit primitive, or a complete jailbreak.

## Safe validation status

No candidate has a demonstrated exploit, confirmed primitive, or verified jailbreak chain. The direct NVD configuration collection task is complete. The next step is to reconcile each raw response with the Apple advisory and CVE Program record, locate public patch/bug references, and preserve uncertainty where implementation details are not public.

## Sources

- Apple iOS 26.7 security content: https://support.apple.com/en-us/149041
- NVD CVE-2026-84607: https://nvd.nist.gov/vuln/detail/CVE-2026-84607
- NVD CVE-2026-43689: https://nvd.nist.gov/vuln/detail/CVE-2026-43689
- NVD CVE-2026-86876: https://nvd.nist.gov/vuln/detail/CVE-2026-86876
- NVD CVE-2026-84523: https://nvd.nist.gov/vuln/detail/CVE-2026-84523


## Follow-up capture evidence

- Latest workflow: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40038959123
- Raw artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40038959123/artifacts/12538253226
- Result: 12/12 CVE API responses and 12/12 CPE Match responses saved; all HTTP 200; no API key configured.
- SHA-256: `4885397b1c735aa870ee3c0c3ff76819d72a1f90b44e1aec58788421827fc56b`
- Exact build and exploitability remain unverified.
