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
