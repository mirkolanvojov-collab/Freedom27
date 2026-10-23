# Historical Apple advisory inventory for Freedom27 target

**Reviewed:** 2026-10-23  
**Target:** iPhone 16 Plus / `iPhone17,4` / iOS 26.6.1 / build `23G83`  
**Scope:** Source-backed inventory of the target release's own published security fixes, plus the already-recorded later iOS 26.7 leads. This is not a complete global vulnerability census and does not claim exploitability.

## Why this matters

Apple's iOS 26.6.1 advisory says the release was published August 17, 2026 and contains security fixes. Apple lists the affected product scope as iPhone 11 and later for these entries, which includes this hardware generation. That product scope does **not** mean each issue remained vulnerable in earlier OS versions; the page describes fixes shipped in 26.6.1. Treat the CVEs below as **fixed in the target release**, not as unpatched leads.

Primary source: https://support.apple.com/en-us/148282

## Target-release fixes relevant to privilege-boundary research

| CVE | Component | Apple's published impact / fix | Freedom27 disposition |
|---|---|---|---|
| CVE-2026-65346 | ImageIO | Processing an image may lead to arbitrary code execution; integer overflow fixed with improved input validation | Fixed in target release; not an unpatched lead |
| CVE-2026-64788 | IOGPUFamily | Maliciously crafted web content may lead to memory corruption; improved memory handling | Fixed in target release; not an unpatched lead |
| CVE-2026-64736 | IOMobileFrameBuffer | App may cause unexpected termination or corrupt kernel memory; out-of-bounds access fixed with bounds checking | Fixed in target release; not an unpatched lead |
| CVE-2026-65343 | Kernel | Remote attacker may cause unexpected system termination; use-after-free fixed with improved memory management | Fixed in target release; not an unpatched lead |
| CVE-2026-65349 | Kernel | App may cause unexpected termination or read kernel memory; out-of-bounds read fixed with input validation | Fixed in target release; not an unpatched lead |
| CVE-2026-65330 | Kernel | App may cause unexpected termination or corrupt kernel memory; improved memory handling | Fixed in target release; not an unpatched lead |
| CVE-2026-28935 | Kernel | Listed under the same kernel advisory section; do not infer an impact beyond the Apple entry without checking its individual CVE record | Fixed in target release; details require separate source confirmation |
| CVE-2026-65329 | Telephony | Attacker in a privileged network position may bypass IPSec authentication and intercept traffic; authentication/state-management issue fixed | Fixed in target release; not a local jailbreak primitive on current evidence |
| CVE-2026-65341 | WebKit | Malicious web content may cause memory corruption; improved memory handling | Fixed in target release; not an unpatched lead |
| CVE-2026-64782 | WebKit | Memory-corruption vulnerability may cause Safari crash; improved locking | Fixed in target release; not an unpatched lead |
| CVE-2026-65391 | WebRTC | Malicious web content may cause memory corruption; out-of-bounds write fixed with bounds checking | Fixed in target release; not an unpatched lead |
| CVE-2026-65390 | WebRTC | Malicious web content may cause memory corruption; integer overflow fixed with input validation | Fixed in target release; not an unpatched lead |

Apple's 26.6.1 advisory contains additional Audio, Authentication Services, ImageIO, WebKit, WebKit History, WebKit Storage, and WebRTC entries, including information disclosure and crash-only issues. The table intentionally prioritizes entries whose published descriptions most directly mention code execution, kernel memory, or memory corruption. It is **not** a full enumeration of every CVE in that advisory.

## Cross-release leads

The existing file `research/ios_26_7_advisory_candidates_2026-10-23.json` tracks eight CVEs described in Apple's iOS 26.7 advisory as fixed in 26.7. Each remains `target_applicability: not_established`, `reproduction_status: not_reproduced_by_Freedom27`, and `chain_status: not_established`. The fact that a fix is listed in a later release is a research lead, not conclusive proof that build 23G83 is affected. Apple documents product support scope, but generally does not provide complete per-build vulnerable-version ranges in these summaries.

Primary source: https://support.apple.com/en-us/149041

## Coverage and evidence gaps

1. **Not every vulnerability:** This inventory is bounded to selected entries from Apple's 26.6.1 advisory and the separate 26.7 candidate list. It does not cover every Apple platform advisory, third-party component, privately disclosed issue, or unpublished vulnerability.
2. **Version history still needed:** Review every iOS 26.x advisory before 26.6.1, and capture all CVEs, components, first fixed releases, and source dates in structured data.
3. **Independent CVE validation still needed:** Cross-check each CVE against its CVE.org record and, where available, NVD and credible technical disclosures. Do not treat a database's generic version range as exact build evidence unless it actually specifies it.
4. **No exploit claim:** No exploit was executed, no device was accessed or modified, and no candidate has been reproduced by Freedom27. Public impact descriptions do not establish a usable primitive or a compatible chain.
5. **No upgrade recommendation implied:** This is a research inventory, not a device security recommendation. Keep the daily-use device unchanged for this project unless the user separately decides otherwise.

## Sources

- Apple Support, “About the security content of iOS 26.6.1 and iPadOS 26.6.1,” released August 17, 2026; entry updates/additions shown September 14, 2026: https://support.apple.com/en-us/148282
- Apple Support, “About the security content of iOS 26.7 and iPadOS 26.7”: https://support.apple.com/en-us/149041
- Apple Support, “Apple security releases”: https://support.apple.com/en-euro/100100 (the page lists iOS 26.6.2 as having no published CVE entries; that statement is not evidence that 26.6.2 contains no undisclosed fixes).

**Status:** Research inventory in progress. No entry in this document establishes an unpatched vulnerability on build `23G83` or a working Freedom27 jailbreak.
