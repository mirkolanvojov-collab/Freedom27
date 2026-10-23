# Exact-target public compatibility status

Reviewed: 2026-10-23

## Target

- Device: iPhone 16 Plus
- Identifier: iPhone17,4
- OS/build: iOS 26.6.1 (23G83)

## Findings

0. Apple's official [iOS 26.6.1 security-content advisory](https://support.apple.com/en-us/148282) states that the release was published on 2026-08-17 and lists security issues addressed in that release, including kernel and WebKit issues. An advisory describing fixes shipped in build `23G83` is not evidence that those same issues remain exploitable on `23G83`, nor that any one issue provides the primitives required for a jailbreak. Each claim must be evaluated against the advisory's affected scope and patch state.

1. The Apple Wiki's public iOS 26.x jailbreak tracker lists no tool for iOS 26.6.1 across the listed iPhone generations, including iPhone 16 Plus:
   https://theapplewiki.com/wiki/Jailbreak/26.x

2. The public firmware listing identifies iOS 26.6.1 build 23G83 as the iPhone 16 Plus firmware:
   https://ipsw.me/iPhone17,4/

3. The upstream bad_query README claims iOS 26.0–26.6.1 support, but explicitly calls itself a developer proof of concept that is not meaningfully usable. It documents sandbox/container paths and does not claim a complete jailbreak:
   https://github.com/forcequitOS/bad_query

4. The registry now tracks bad_query as an unverified research lead. Its OS-version claim overlaps the target version, but the upstream README does not specifically verify iPhone 16 Plus / iPhone17,4 / 23G83.

5. A separate website makes broad claims that an online jailbreak works on iOS 26.6.1. Those claims conflict with the more cautious public tracker and are not supported here by a primary-source release or independently reproducible evidence. Do not install profiles, apps, certificates, or pay/complete surveys based on such claims.

## Decision

**No verified public jailbreak established for this exact target.** The bad_query lead is version-overlapping but not proven to work on this device/build and is not a usable jailbreak according to its own README.

Freedom27 remains research-only. Do not downgrade/restore the device, install unknown profiles, or run unverified payloads as a result of this review.

## Evidence required to change this status

- Primary-source support naming iPhone17,4 and build 23G83, or reproducible independent testing on that exact target.
- Clear documentation of the capability demonstrated; sandbox access must not be described as kernel control or a full jailbreak.
- For any claimed jailbreak release, a public source/release, reproducible instructions, and independent confirmation of device/build support.
