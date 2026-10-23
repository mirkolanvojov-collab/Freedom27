# iPhone 16 Plus exact-target evidence record

**Record date:** 2026-10-23  
**Project:** Freedom27  
**Target under review:** iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`  
**Evidence type:** Public-source review only — not a test performed on the physical device  
**Status:** `source_supported`; exact-target exploit verification remains **unproven**

## Evidence gathered

### E1 — Device/build identity

A public firmware catalog maps iOS 26.6.1 build `23G83` to iPhone 16 Plus identifier `iPhone17,4`. This corroborates the target tuple used by this research record; it does not establish exploitability.

- Source: https://www.applefirmwares.com/firmware/iPhone17%2C4/26.6.1
- Cross-check: https://ipsw.me/iOS/26.6.1/

### E2 — Upstream `bad_query` claim

The upstream README claims a sandbox escape PoC for iOS 26.0–26.6.1 and iOS 27.0 beta 4. It explicitly describes the project as a developer PoC that is not meaningfully usable yet, and lists selected container/data paths.

- Source: https://github.com/forcequitOS/bad_query
- Reviewed README blob: `3563002bfaa6fc4be1eb2e0e33d6fc9076f7b67e`
- Reviewed C source blob: `dce2c4db47152efd4f84826c99e4348016126416`

The README's version range overlaps the target's OS version, but it does not provide a reproducible test record for the exact combination of iPhone 16 Plus, identifier `iPhone17,4`, and build `23G83`. A broad version claim is not exact-device proof.

### E3 — Scope limitation from static source review

The reviewed C source dynamically resolves private container-management and sandbox-extension APIs, forms a container query, requests a sandbox token, and attempts to consume the extension. The code includes failure paths. This static observation describes the implementation; it is not evidence that the operation succeeded on any particular device.

- Source: https://github.com/forcequitOS/bad_query/blob/main/bad_query/bad_query.c

## Evidence classification

| Claim | Current assessment | Why |
|---|---|---|
| Target identity is `iPhone17,4 / iOS 26.6.1 / 23G83` | Public-source corroborated | Firmware catalogs map the model identifier and build |
| Upstream claims an overlapping OS range | Source-supported | README states iOS 26.0–26.6.1 |
| PoC works on this exact device/build | **Not verified** | No exact-target reproducible artifact or result found in the reviewed sources |
| Kernel privilege escalation exists | **No evidence recorded** | The reviewed README/source review does not establish it |
| Persistence, package manager, or complete jailbreak works | **No evidence recorded** | These capabilities are not demonstrated by the cited material |

## What would count as real exact-target evidence

Do not fill these fields with estimates or invented values. An exact-target verification record needs:

1. The device identifier and OS/build read directly from the tested iPhone.
2. The precise upstream revision and documented prerequisites used.
3. A timestamp in ISO-8601 UTC format.
4. A test artifact reference, such as a sanitized log or screen recording, with private data removed.
5. The actual observed result, including failure output if it failed.
6. Independent review or reproduction before claiming independent verification.

## Safety and conclusion

No exploit was run, no payload was installed, and no device state was changed during this review. Do not downgrade or restore the daily-use iPhone to chase this lead; the listed iOS 26.6.1 firmware may no longer be signed.

**Conclusion:** The public sources support investigating `bad_query` as a research lead, but they do not establish a working jailbreak on the exact iPhone 16 Plus target. Keep `exact_target_verified = false` until reproducible, exact-build evidence is collected.


## Follow-up upstream status check — 2026-10-23

A public upstream pull request remains open and unmerged: [bad_query hardening PR #1](https://github.com/forcequitOS/bad_query/pull/1). It proposes a NULL guard, a bound on an inode parameter, and cleanup of a security-scoped resource handle. Its own checklist marks Xcode compilation and the listed regression checks as not yet completed in the PR description.

This is additional evidence that the public project still has unresolved engineering/testing work; it is **not** proof the core approach fails. It also provides no exact-target result for iPhone17,4 / build 23G83. Keep the exact-target gate blocked and do not use an unreviewed build on the daily-use phone.


## Follow-up lead review — Veilpath — 2026-10-23

A newer downstream project, [everettjf/veilpath](https://github.com/everettjf/veilpath), describes itself as a native iPhone/iPad container explorer built around `bad_query`. Its README states that the complete access path was validated on a physical iPad Air running iPadOS 27 beta 3 (build `24A5380l`), and explicitly warns that the upstream PoC's additional claimed versions have not all been validated in Veilpath.

This is a more concrete public validation report than the upstream version-range claim, but it is **not** validation for the target iPhone 16 Plus / iOS 26.6.1 / build 23G83. The hardware and OS build differ. The downstream app also describes itself as experimental and dependent on private APIs. Treat it as a lead for further source/evidence review, not as a ready-to-install jailbreak or proof of kernel privilege escalation.

- Project: https://github.com/everettjf/veilpath
- Public description reviewed: README and repository metadata
- Repository last updated (API metadata): 2026-10-06T19:27:04Z
- No build, install, or device test was performed by Freedom27 during this review.

### Updated lead assessment

| Lead | Evidence strength for the exact target | Next check |
|---|---|---|
| `bad_query` upstream PoC | OS-range claim only; exact target unverified | Review implementation and validation caveats |
| Veilpath downstream app | Physical iPad Air / iPadOS 27 beta 3 validation reported; not the target | Inspect diagnostics and compatibility claims; do not extrapolate across device/build |
| Full jailbreak / Cydia bootstrap | No supporting evidence found in these sources | Keep blocked until independently reproducible evidence exists |

**Decision:** Keep `bad_query` as a research lead, but do not mark it target-verified or promote it to a full-jailbreak solution. The next research task is to inspect Veilpath's public diagnostics and compatibility notes for evidence that can be responsibly compared with the exact target. Do not install or run experimental private-API software on the daily-use iPhone based on this report alone.


### Compatibility table detail checked in Veilpath README

The README's compatibility table also reports physical-device testing on an **iPhone 17 Pro (`iPhone18,1`) running iOS 27 beta 3 (`24A5390f`)**. It lists iOS/iPadOS 26.x as a deployment-target/App Group compatibility path, not as full physical-device validation of every 26.x build. It explicitly says versions outside the documented tested range remain unsupported until physical-device testing confirms them.

This improves confidence that the approach has been exercised on at least one physical iPhone model, but it still does not validate the different iPhone 16 Plus / iOS 26.6.1 / 23G83 target. The README describes a container-exploration/file-workspace app, not a full jailbreak, kernel privilege escalation, or Cydia bootstrap.

- Compatibility source: https://github.com/everettjf/veilpath#compatibility
- Build requirements include Xcode 27 beta and a physical device for sandbox-access testing; this is not a build path available on the user's iPhone alone.


## Alternative path found: Erosion partial customization — 2026-10-23

A direct alternative to waiting for a full jailbreak is the public [Erosion](https://github.com/jailbreakdotparty/Erosion) customization toolbox. Its README states support for iOS/iPadOS 26.0–26.6.2, with **limited functionality on iOS 26** and explicitly no MobileGestalt tweaks on iOS 26 because its underlying `bad_query` approach cannot write MobileGestalt. The latest listed release reviewed here is v0.2.1 and publishes an IPA asset with SHA-256 `8c1276ce612505233d04200a1bc568fd6e59087eaacb054f3e5edc854f0e18c`.

The target OS version 26.6.1 is inside Erosion's declared range. This is a plausible partial-customization path, **not a full jailbreak** and not proof that every Erosion feature works on this specific iPhone 16 Plus/build. Its README asks users to back up first and warns that functionality is limited and tweak behavior can vary. No IPA was downloaded, installed, or executed during this review.

- Compatibility statement: https://github.com/jailbreakdotparty/Erosion#supported-versions
- Release: https://github.com/jailbreakdotparty/Erosion/releases/tag/0.2.1
- Published IPA SHA-256 from GitHub release metadata: `8c1276ce612505233d04200a1bc568fd6e59087eaacb054f3e5edc854f0e18c`

### Decision update

To make progress without falsely clearing the full-jailbreak gate, split the goal into two tracks:
1. **Partial customization track:** assess Erosion's release provenance, supported features on iOS 26, and whether it can be installed safely using only the user's available iPhone.
2. **Full jailbreak track:** remain blocked until there is exact-target evidence for kernel privilege escalation, bootstrap/package manager, and independent reproduction.

Do not label Erosion as Freedom27 or as a jailbreak. Do not claim iPhone-only installation is solved until its install/signing requirements are verified.
