# Freedom27 source-pinned compatibility research — 2026-10-23

## Scope and method

Target: iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`. Development constraint: iPhone only.

This is a read-only review of public primary sources and release metadata. No IPA was downloaded or installed, no proof-of-concept was executed, and the physical iPhone was not tested. GitHub commit IDs below pin the reviewed source revisions; README claims are not treated as independent reproduction.

## Findings

### 1. Public jailbreak status

The community-maintained [Apple Wiki iOS 26.x tracker](https://theapplewiki.com/wiki/Jailbreak/26.x), reviewed on 2026-10-23, lists “No Tool Available” for iOS 26.6.1 and also for 26.6.2. The tracker does not list a working tool for the target row. This is evidence about public status, not proof that private research does not exist.

### 2. bad_query upstream claim

- Repository: https://github.com/forcequitOS/bad_query
- Reviewed README revision: `3563002bfaa6fc4be1eb2e0e33d6fc9076f7b67e` (the README blob previously reviewed; repository head reported separately as `73ef6da1adabef0982fd00e36cb85f21b8f8194a` on 2026-10-23).
- The README says iOS 26.0–26.6.1 / iOS 27.0 beta 4, but explicitly describes itself as a developer proof-of-concept “not anything meaningfully usable.”
- The listed behavior is access to selected container/data paths, with some paths marked iOS-27-only and App Group access requiring an App Group sacrifice on iOS 26.
- The claim does not establish a kernel exploit primitive, privilege escalation, root access, persistence, a tweak-injection framework, package-manager support, or a complete jailbreak.
- It does not provide exact-device reproduction evidence for iPhone 16 Plus (`iPhone17,4`) on build `23G83`.

**Assessment:** Relevant research lead only. Exact-target compatibility remains unverified.

### 3. Erosion source and release check

- Repository: https://github.com/jailbreakdotparty/Erosion
- README blob reviewed: `71069b7313bf7aa5130392034856aa147b9a4bc2`
- Repository head observed: `d16f7f12470458c7028dc274b343a80b85b408be` (2026-09-27).
- Latest public release observed: [v0.2.1](https://github.com/jailbreakdotparty/Erosion/releases/tag/0.2.1), published 2026-09-18.
- Release asset metadata: `Erosion_v0.2.1.ipa`, SHA-256 `8c1276ce6125052333d04200a1bc568fd6e59087eaacb054f3e5edc854f0e18c`. This is metadata reported by GitHub for the release asset; the file was not downloaded or independently hashed.
- README claims iOS/iPadOS 26.0–26.6.2 with limited functionality, specifically noting that MobileGestalt tweaks are unavailable. The README says Erosion uses bad_query.
- Erosion's version-range claim includes 26.6.1 but does not provide independently reproduced results for the exact iPhone 16 Plus / `23G83` target.
- Its own warning notes potential data loss and asks users to back up. This research does not recommend installing it on the daily-use device.

**Assessment:** Erosion may offer limited customization on some supported builds, but its documentation does not establish a complete jailbreak or prove exact-target operation. It does not provide evidence of Cydia/package-manager support or a persistent rootful/rootless jailbreak chain.

### 4. Apple security advisory cross-check

Apple's [iOS 26.6.1 security-content advisory](https://support.apple.com/en-us/148282) lists CVE-2026-65343 as a Kernel use-after-free issue addressed with improved memory management, with impact described as possible unexpected system termination. It lists CVE-2026-65349 as a Kernel out-of-bounds read addressed with improved input validation, with impact described as possible system termination or kernel-memory read.

The advisory does not identify either issue as a working jailbreak, does not document privilege escalation or persistence, and does not validate a third-party exploit attribution beyond the descriptions Apple publishes. Do not infer a usable exploit chain from the CVE numbers alone.

### 5. Installation and workflow verification

The public Erosion release includes an IPA asset, but this review did not verify its signature, installation prerequisites, device-specific behavior, or whether it can be installed and used entirely from an iPhone. The existence of an IPA download is not evidence that installation is safe, that the app works on the target, or that it creates a jailbreak.

No installation guide or sideloading step should be presented as verified for this target unless it is traced to current upstream instructions and exact-target evidence. Do not install configuration profiles or certificates from third-party “online jailbreak” pages, and do not downgrade/restore as an exploratory step.

## Decision for Freedom27

- `verified_complete_jailbreak`: **false**
- Exact target: **unverified / blocked**
- Public complete jailbreak chain demonstrated for iPhone 16 Plus / iOS 26.6.1 / build `23G83`: **no evidence found in sources reviewed**
- Entry point, sandbox escape reproduction on exact target, kernel primitive, privilege escalation, mitigation handling, persistence/bootstrap, package manager, and independent reproduction: remain separate gates; none should be marked complete from these sources.
- Project classification: research scaffold only; not an installable jailbreak.

## Next research actions

1. Keep source URLs and full immutable revisions in the research manifest.
2. Correct any previous installation-guide citation that cannot be traced to an official upstream source; do not replace it with an unverified third-party guide.
3. Revisit only if upstream publishes a materially new release or exact-device/build reproduction evidence appears.
4. Keep all testing read-only until an appropriate authorized test environment exists. Do not execute the PoC or install Erosion on the daily-use phone merely to resolve uncertainty.

## Sources

- Apple Wiki tracker: https://theapplewiki.com/wiki/Jailbreak/26.x
- bad_query README: https://github.com/forcequitOS/bad_query/blob/3563002bfaa6fc4be1eb2e0e33d6fc9076f7b67e/README.md
- Erosion README: https://github.com/jailbreakdotparty/Erosion/blob/71069b7313bf7aa5130392034856aa147b9a4bc2/README.md
- Erosion release v0.2.1: https://github.com/jailbreakdotparty/Erosion/releases/tag/0.2.1
- Apple security advisory: https://support.apple.com/en-us/148282
