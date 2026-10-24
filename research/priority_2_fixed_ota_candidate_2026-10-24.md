# Priority 2: fixed-build OTA candidate (2026-10-24)

## Blocker update

The earlier blocker was phrased too narrowly as “no iPhone17,4 iOS 26.7.1 restore IPSW found.” A same-device **OTA update** entry is listed for iPhone 16 Plus by The Apple Wiki's iOS 26.7.1 OTA catalogue:

- Device: iPhone 16 Plus (target identifier iPhone17,4)
- Fixed OS version/build: iOS 26.7.1 / 23H30
- Release date: 2026-09-28
- OTA package identifier shown by the catalogue: `818080afd3f2204f9cf3c8da075752ee6e05c420554a0b076e7c9f5d2378d203.aea`
- Listed package size: 8,724,152,320 bytes
- Listed extraction key: `YSWzwfZFdAFfs7gP222NfRfnN9lb1riyeL3bzwMlkEs=`
- Source catalogue: https://theapplewiki.com/wiki/OTA_Updates/iPhone/26.7.1 (iPhone 16 Plus section)
- Apple security bulletin: https://support.apple.com/en-us/149226
- Public patch analysis: https://calif.io/research/the-great-glyph-grift

The exact download URL was subsequently resolved from Apple's live OTA metadata using the open-source `ipsw` utility in GitHub Actions (run 40053023805): https://updates.cdn-apple.com/2026FallFCS/5ef51a7b-0f58-4585-8cdf-14afa18e9622/com_apple_MobileAsset_SoftwareUpdate/818080afd3f2204f9cf3c8da075752ee6e05c420554a0b076e7c9f5d2378d203.aea

The CI step verified that the returned URL's hostname is exactly `updates.cdn-apple.com`. The package was then downloaded from that URL in CI run https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40053079976. The job verified the exact 8,724,152,320-byte size and computed SHA-256:

```
SHA-256: 0078dc02b647fbc5c6efb8fd4e3fe0fc79d02af5f798f2e7981e069bd6987d92
Size:    8724152320 bytes
```

The 64-hex filename identifier differs from the whole-file SHA-256, so it must not be treated as the file digest. The workflow removed the 8.7 GB package after hashing and uploaded a small verification-record artifact. This establishes a reproducible digest for the downloaded package and exact size; it is not an Apple-published checksum or cryptographic signature by itself.

## Safe validation sequence

1. **Completed:** resolve the exact Apple CDN URL through Apple's live OTA metadata; URL host checked in CI run https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40053023805.
2. **Completed:** download from that Apple CDN URL; validate exact length and compute SHA-256 in CI run https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40053079976.
3. Next: validate package internals and device/build identity, then determine whether CoreGraphics can be extracted and compared with target 23G83. Treat the published extraction key as untrusted until cross-checked against an independent firmware metadata source.
4. If the package can be lawfully and reproducibly extracted, identify the CoreGraphics binary and record its cryptographic hash, architecture, UUID/build metadata, and provenance.
5. Compare only corresponding code with the target 23G83 component. If target or fixed binary is encrypted, incomparable, or lacks sufficient symbols/metadata, record that limitation rather than inferring a patch.
6. Use static, read-only comparison and synthetic defensive-model tests only. Do not run the published exploit/PoC, craft a trigger file, modify a device, or claim exploitability from a version-range match alone.

## Current evidence state

- Target IPSW 23G83 integrity: verified in CI previously (SHA-256 `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`; 11,225,458,130 bytes).
- CVE-2026-86950: Apple says fixed in iOS 26.7.1 and describes an out-of-bounds write addressed by improved bounds checking.
- Public patch analysis: reports changes in CoreGraphics anti-aliased path-rasterization coordinate conversion.
- Exact target vulnerable code path: not established.
- Same-device fixed OTA: downloaded from the resolved Apple CDN; exact byte count and computed SHA-256 recorded by CI; internal extraction and component comparison remain outstanding.
- Reproduction and jailbreak chain: not established.

This is a research evidence update, not a claim that the blocker is fully cleared or that a jailbreak works.
