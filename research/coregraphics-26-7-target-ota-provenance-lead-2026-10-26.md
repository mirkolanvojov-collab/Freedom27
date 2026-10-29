# iPhone17,4 iOS 26.7 (23H24) OTA provenance lead — 2026-10-26

## Verified public metadata

The Apple Wiki's iOS 26.7 OTA catalogue has a row specifically for **iPhone 16 Plus / iPhone17,4**:

- OS/build: iOS 26.7 / 23H24
- Release date: 2026-09-14
- OTA package identifier: `9fa3dca87b9d18a7329eada91fcd038086f20c37e1aed47f8735f0970b27cd14.aea`
- Published package size: 8,724,152,320 bytes
- Published extraction key: `Nsc4CePIkIJyP8wCRmF/FllWT3yZDH9NWM9MNor1IVE=`
- Source: https://theapplewiki.com/wiki/OTA_Updates/iPhone/26.7 (iPhone 16 Plus section)
- The same catalogue separately lists the iPhone 16 Plus 26.7.1 / 23H30 OTA in its 26.7.1 page; existing repository evidence records that package's successful download and hash verification.

The package identifier is not the full-file SHA-256. A direct Apple CDN URL and full-file digest for this 23H24 package have **not yet been independently verified in this workstream**. Resolve the URL from Apple's live OTA metadata (for example, using the repository's existing `ipsw download ota --platform ios --device iPhone17,4 --build <build> --urls` workflow pattern), require the exact Apple CDN hostname, then download and hash the package before extracting it. Do not infer the CDN path from the package identifier.

## Why this closes part of the blocker

The prior research note said the target-device 23H24 image/OTA was still unverified. This catalogue entry now provides a concrete same-device OTA candidate with a published size and extraction key. It does **not** yet establish the direct 23H24-to-23H30 binary comparison: the URL still needs live resolution, the downloaded package needs size and digest recording, and extraction must confirm that it contains the expected iPhone17,4 dyld cache.

## Required next steps

1. Resolve the direct Apple CDN URL from live metadata for iPhone17,4 build 23H24; record the exact URL and timestamped command output.
2. Download from that URL; require 8,724,152,320 bytes and record the computed SHA-256 (clearly label it as locally computed, not an Apple-published digest).
3. Extract the 23H24 dyld cache using the published key and verify the resulting cache and CoreGraphics architecture/device provenance.
4. Compare CoreGraphics from 23H24 against the already verified iPhone17,4 23H30 OTA. Keep the 23G83-to-23H30 comparison as a separate baseline.
5. Attribute the CVE fix only if the same-device comparison and code-level evidence support it; instruction differences alone do not prove attacker control or exploitability.

## Safety and interpretation

All planned analysis is static and read-only. Do not execute exploit code or modify a device. A valid firmware match and changed instructions are evidence leads, not proof of exploitability.

## Repository automation update — 2026-10-26

The CoreGraphics comparison workflow now has a separate direct 23H24-to-23H30 lane while retaining the existing 23G83-to-23H30 baseline. It resolves the 23H24 OTA URL from live `ipsw` metadata, rejects URLs whose hostname is not exactly `updates.cdn-apple.com`, verifies the published package size, computes and logs the downloaded file's SHA-256, extracts the 23H24 dyld cache with the published key, and emits separate binary/function/constant/CFG artifacts. The binary comparison helper now accepts explicit build/device labels so the report cannot silently label the 23H24 cache as 23G83.

- Workflow change commit: `5f1258ac569efe8bd7b7b6b39e431e83a62a3606`
- Comparison run for that commit: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40340793267
- Build-label parameterization fix: `f03d9c5170e4ebae374dab5b4219c979850673da`
- Tests for the latest script fix: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40340852177

The first test attempt exposed a syntax error in the new helper edit; it was corrected in `f03d9c5`. The new test run was still in progress at the time of this note, and the macOS comparison run remained queued. Therefore, the workflow design is committed but the new end-to-end comparison is **not yet verified successful**.
