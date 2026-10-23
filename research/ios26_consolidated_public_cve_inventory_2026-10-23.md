# Freedom27 — consolidated public iOS 26 CVE source inventory

**Updated:** 2026-10-23  
**Target context:** iPhone 16 Plus / `iPhone17,4` / iOS 26.6.1 / build `23G83`

This is the consolidated tracking index for public CVE identifiers disclosed in Apple security advisories for iOS 26. It intentionally distinguishes a verified page-level extraction from a candidate list. Do not treat a release advisory's CVEs as unpatched on 26.6.1: CVEs fixed in 26.6 or earlier are historical fixes; later fixes are research leads only until exact-version evidence exists.

## Official source register

| Release advisory | Apple source | Current extraction status |
|---|---|---|
| iOS 26.7 | https://support.apple.com/en-us/149041 | Selected candidate JSON; not exhaustive |
| iOS 26.6.2 | https://support.apple.com/en-us/100100 | Apple release index lists no CVE entry for this version; this does not prove no undisclosed fixes |
| iOS 26.6.1 | https://support.apple.com/en-us/148282 | Selected historical CVEs in Markdown; not exhaustive |
| iOS 26.6 | https://support.apple.com/en-us/128066 | ID extraction file exists; marked not certified exhaustive |
| iOS 26.5.2 | https://support.apple.com/en-us/127594 | Search-indexed full advisory text contains multiple entries; selected historical triage only |
| iOS 26.5.1 | https://support.apple.com/en-us/100100 | Apple release index; no dedicated CVE advisory located in current review |
| iOS 26.5 | https://support.apple.com/en-us/100100 | Dedicated advisory not yet extracted |
| iOS 26.4.2 | https://support.apple.com/en-euro/127002 | CVE-2026-28950 |
| iOS 26.4 | https://support.apple.com/en-us/126792 | Multiple entries; extraction pending |
| iOS 26.3.1 | https://support.apple.com/en-us/100100 | Apple release index; dedicated CVE advisory not yet extracted |
| iOS 26.3 | https://support.apple.com/en-ae/126346 | Multiple entries; extraction pending |
| iOS 26.2.1 | https://support.apple.com/en-us/100100 | Apple release index; no CVE entry located in current review |
| iOS 26.2 | https://support.apple.com/en-us/100100 | Dedicated advisory not yet extracted |
| iOS 26.1 | https://support.apple.com/en-us/100100 | Dedicated advisory not yet extracted |
| iOS 26.0.1 | https://support.apple.com/en-us/100100 | Dedicated advisory not yet extracted |
| iOS 26.0 | https://support.apple.com/en-am/125108 | Multiple entries; extraction pending |

Apple release index: https://support.apple.com/en-us/100100

## CVEs explicitly visible in the official iOS 26.5.2 advisory

Source: https://support.apple.com/en-us/127594

- CVE-2026-43743 — IOGPUFamily
- CVE-2026-43724 — Kernel
- CVE-2026-43722 — Kernel
- CVE-2026-39868 — Kernel
- CVE-2026-43706 — libxslt
- CVE-2026-43703 — libxslt
- CVE-2026-43807 — MobileAccessoryUpdater
- CVE-2026-43704 — Web Extensions
- CVE-2026-43700 — WebKit
- CVE-2026-43735 — WebKit
- CVE-2026-43734 — WebKit
- CVE-2026-43726 — WebKit
- CVE-2026-43709 — WebKit
- CVE-2026-43699 — WebKit
- CVE-2026-43742 — WebKit
- CVE-2026-43732 — WebKit
- CVE-2026-43731 — WebKit
- CVE-2026-43715 — WebKit
- CVE-2026-43727 — WebKit
- CVE-2026-43725 — WebKit
- CVE-2026-43663 — WebKit
- CVE-2026-39872 — WebKit
- CVE-2026-43712 — WebKit
- CVE-2026-43716 — WebKit
- CVE-2026-43676 — WebKit
- CVE-2026-43740 — WebKit
- CVE-2026-43713 — WebKit
- CVE-2026-43708 — WebKit
- CVE-2026-43707 — WebKit
- CVE-2026-43705 — WebKit
- CVE-2026-43701 — WebKit
- CVE-2026-43745 — WebKit
- CVE-2026-43720 — WebKit Canvas
- CVE-2026-43721 — WebKit Storage
- CVE-2026-28979 — WebRTC
- CVE-2026-43718 — WebRTC
- CVE-2026-43717 — WebRTC
- CVE-2026-43746 — WebKit

**Important:** Apple labels some entries as added or updated after the initial 26.5.2 release, including entries first made available in the 26.6 beta. Preserve the current advisory content and its update notes; do not assume every entry was initially shipped in the same release.

## CVEs explicitly visible in the official iOS 26.4.2 advisory

Source: https://support.apple.com/en-euro/127002

- CVE-2026-28950 — Notification Services

## CVEs explicitly visible in the official iOS 26.4 advisory excerpt

Source: https://support.apple.com/en-us/126792

- CVE-2026-28822 — Audio
- CVE-2026-28874 — Baseband
- CVE-2026-28875 — Baseband (listed for iPhone 16e; hardware scope differs from target)
- CVE-2026-28872 — Calendar
- CVE-2026-28894 — Calling Framework
- CVE-2026-28876 — DeviceLink
- CVE-2026-28870 — GeoServices
- CVE-2026-28880 — iCloud
- CVE-2026-28833 — iCloud
- CVE-2025-64505 — ImageIO
- CVE-2026-20692 — Mail
- CVE-2026-28896 — ppp
- CVE-2026-20688 — Printing
- CVE-2026-28873 — Privacy
- CVE-2026-28967 — Telephony
- CVE-2026-28852 — UIFoundation

The search-indexed advisory continues beyond the excerpt above; this is not the complete iOS 26.4 list.

## CVEs explicitly visible in the official iOS 26.3 advisory excerpt

Source: https://support.apple.com/en-ae/126346

- CVE-2026-20645 — Accessibility
- CVE-2026-20674 — Accessibility
- CVE-2026-20637 — AppleKeyStore

The source page has more entries; extraction is incomplete.

## Existing repo inventories

- `research/ios_26_7_advisory_candidates_2026-10-23.json`: 12 later-release research candidates; all target applicability, reproduction, and chain status remain unestablished.
- `research/ios_26_6_1_historical_advisory_inventory_2026-10-23.md`: selected entries fixed in the target release, not an exhaustive list.
- `research/ios_26_5_2_historical_advisory_triage_2026-10-23.md`: selected historical triage, not an exhaustive list.
- `research/ios_26_6_apple_advisory_cve_extraction_2026-10-23.json`: initial iOS 26.6 extraction, explicitly not certified exhaustive.
- `research/ios26_security_advisory_coverage_register_2026-10-23.md`: version/source coverage checklist.

## Required completion and validation rules

1. Retrieve each official Apple advisory in full and extract every literal CVE-ID, including IDs embedded after a shared component description.
2. Save per-advisory extraction files with a machine-checked count, unique IDs, source URL, page retrieval date, and explicit extraction status.
3. Compare the extracted identifiers against the full rendered page text; where search snippets truncate, mark pending rather than inferring completeness.
4. Deduplicate cross-release CVEs while preserving all advisory references and later “entry added/updated” notes.
5. Record component, exact Apple impact, fix summary, and release in which Apple published the fix.
6. Separate public CVE enumeration from exact-build applicability. Do not label a candidate exploitable on build 23G83 without direct evidence.
7. No device access, exploit execution, or modification is part of this static advisory inventory.

## Current conclusion

The repository contains useful source-backed subsets, but a verified, exhaustive union of all published CVEs across every iOS 26 release has **not yet been completed**. Apple also states it does not disclose every security issue before investigation and fixes; no public-advisory inventory can reveal private or undisclosed vulnerabilities.
