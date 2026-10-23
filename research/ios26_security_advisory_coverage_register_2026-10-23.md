# iOS 26 security-advisory coverage register

**Reviewed:** 2026-10-23  
**Freedom27 target:** iPhone 16 Plus / `iPhone17,4` / iOS 26.6.1 / build `23G83`

This register tracks the official Apple advisory pages that must be reviewed for a complete public-CVE inventory relevant to the target release. A release's security fixes are not evidence that those vulnerabilities were present on the target before the fix, and a later release's fix is not by itself proof that build 23G83 is vulnerable.

## Official release map

| Release | Apple release date (per Apple Security Releases) | Official security-content source | Triage status |
|---|---:|---|---|
| iOS 26.7 | 2026-09-14 | https://support.apple.com/en-us/149041 | Partially inventoried; candidate JSON exists, not a complete CVE enumeration |
| iOS 26.6.2 | 2026-09-08 | https://support.apple.com/en-us/100100 | Apple says no published CVE entries; do not infer no undisclosed fixes |
| iOS 26.6.1 | 2026-08-17 | https://support.apple.com/en-us/148282 | Partially inventoried; historical file explicitly not complete |
| iOS 26.6 | 2026-07-27 | https://support.apple.com/en-us/128066 | Source located; full CVE extraction and triage pending |
| iOS 26.5.2 | 2026-06-29 | https://support.apple.com/en-us/127594 | Selected kernel/WebKit entries recorded; full CVE extraction pending |
| iOS 26.5.1 | 2026-06-01 | https://support.apple.com/en-us/100100 | Apple says no published CVE entries; do not infer no undisclosed fixes |
| iOS 26.5 | 2026-05-11 | https://support.apple.com/en-ca/127110 | Source located; full CVE extraction and triage pending |
| iOS 26.4.2 | 2026-04-22 | https://support.apple.com/en-us/127002 | Source located; one notification-services entry located; full review pending |
| iOS 26.4 | 2026-03-24 | https://support.apple.com/en-us/126792 | Source located; full CVE extraction and triage pending |
| iOS 26.2.1 | 2026-01-26 | https://support.apple.com/en-us/100100 | Apple says no published CVE entries; do not infer no undisclosed fixes |
| iOS 26.2 | 2025-12-12 | https://support.apple.com/en-us/100100 | Official release listed; dedicated security page still needs locating/review |
| iOS 26.1 | 2025-11-03 | https://support.apple.com/en-us/100100 | Official release listed; dedicated security page still needs locating/review |
| iOS 26.0.1 | 2025-09-29 | https://support.apple.com/en-us/100100 | Official release listed; dedicated security page still needs locating/review |
| iOS 26.0 | 2025-09-15 | https://support.apple.com/en-us/100100 | Official release listed; dedicated security page still needs locating/review |

Apple's canonical release index: https://support.apple.com/en-us/100100

## Rules for finishing the inventory

1. Capture every CVE-ID present in each official iOS/iPadOS advisory, including non-kernel entries, rather than selecting only high-impact descriptions.
2. Record advisory release date and page URL, component, exact Apple impact text, exact Apple fix summary, and whether Apple says the entry was added or updated later.
3. Deduplicate CVEs across advisories without discarding the advisory page where the entry is mentioned.
4. Keep two separate assessments: (a) release in which Apple says the fix shipped, and (b) whether there is credible evidence of applicability to build 23G83. Do not infer (b) solely from product model coverage.
5. Cross-check CVE records and technical disclosures where available, preserving source attribution and marking gaps explicitly.
6. Treat Apple pages that state “no published CVE entries” as such; do not translate that wording into “no security fixes” or “no vulnerabilities.”
7. Do not execute exploit code or modify the user's device for this inventory. A CVE entry is not a reproduction, primitive, or complete jailbreak chain.

## Current evidence boundary

- The 26.6.1 and 26.5.2 Markdown files in this repository are selected historical triage, not complete advisory dumps.
- `research/ios_26_7_advisory_candidates_2026-10-23.json` contains 12 candidates, all marked not established for target applicability, not reproduced by Freedom27, and not established as a chain.
- No exploit has been executed by Freedom27; the device has not been accessed or modified.
- Public Apple advisories cannot enumerate private or undisclosed vulnerabilities. “Every single vulnerability” is not a verifiable promise; this register aims for exhaustive coverage of published CVE entries in the selected official iOS 26 release pages.

## Sources checked during this update

- Apple Security Releases: https://support.apple.com/en-us/100100
- iOS 26.7 security content: https://support.apple.com/en-us/149041
- iOS 26.6 security content: https://support.apple.com/en-us/128066
- iOS 26.5 security content: https://support.apple.com/en-ca/127110
- iOS 26.4.2 security content: https://support.apple.com/en-us/127002
- iOS 26.4 security content: https://support.apple.com/en-us/126792
