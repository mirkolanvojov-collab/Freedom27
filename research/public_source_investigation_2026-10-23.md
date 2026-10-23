# Freedom27 public-source investigation — 2026-10-23

## Exact target
- iPhone 16 Plus (`iPhone17,4`)
- iOS 26.6.1, build `23G83`
- iPhone-only development setup

## Current public status

### Apple Wiki tracker
The current [iOS 26.x jailbreak tracker](https://theapplewiki.com/wiki/Jailbreak/26.x) lists **No Tool Available** for iOS 26.6.1 and no iPhone 16 Plus support on that row. Its [overall jailbreak status table](https://theapplewiki.com/wiki/Jailbreaking) also lists the iPhone 16 family with no jailbreak tool. These are community-maintained trackers, not proof that no private research exists, but they are useful public-status references.

### iClarified
The [iClarified jailbreak status guide](https://www.iclarified.com/jailbreak) says there is no public iOS 26 jailbreak for A18/A19 devices, including the iPhone 16 lineup. Its [iPhone 16 Plus firmware page](https://www.iclarified.com/ipsw/iphone-16-plus) identifies build `23G83` as iOS 26.6.1 and lists that firmware as unsigned. **Do not attempt a downgrade or restore** based on this; signing status is not a path to jailbreak.

### bad_query
The [upstream README](https://github.com/forcequitOS/bad_query) claims sandbox/container access for iOS 26.0–26.6.1 and iOS 27.0 beta 4, but calls itself a developer proof-of-concept and says it is not meaningfully usable. This does not establish a complete jailbreak, kernel control, privilege escalation, persistence, or Cydia.

### Erosion
The [upstream Erosion README](https://github.com/jailbreakdotparty/Erosion) currently claims iOS 26.0–26.6.2 support, but explicitly says functionality is limited on iOS 26, including no MobileGestalt tweaks. Its use of `bad_query` is not proof of full jailbreak capability. No exact-build reproduction on iPhone 16 Plus / `23G83` is documented in the sources reviewed here.

### EscapeOS
The [upstream EscapeOS README](https://github.com/pwnapplehat/EscapeOS) describes selected app-data browsing/backup rather than a complete jailbreak. The reviewed setup requires a Windows host for pairing preparation, so it is not a documented iPhone-only workflow.

## Result
No public source reviewed establishes a complete jailbreak for iPhone 16 Plus / iOS 26.6.1 / build `23G83`. Keep Freedom27's status as research-only/blocked and the verified-jailbreak flag false.

## Next actions
1. Inspect the latest GitHub Actions run at https://github.com/mirkolanvojov-collab/Freedom27/actions. The combined-status query returned an empty status list for a previous commit, which is inconclusive.
2. Continue read-only review only when primary upstream documentation, a release, or a new exact-build report appears.
3. Do not install unknown profiles/apps, run proof-of-concept code, or restore/downgrade the daily-use phone as a substitute for evidence.
4. Use supported iOS settings and customization options if the immediate goal is visual customization while waiting for verified jailbreak support.

This is a public-source review, not a physical-device test or proof that no private exploit exists.
