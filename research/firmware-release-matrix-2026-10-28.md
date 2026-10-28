# Firmware release matrix — 2026-10-29

Target device: iPhone 16 Plus (`iPhone17,4`, board `D48AP`). This is a release inventory, not a compatibility or vulnerability conclusion.

| Priority | Release | Build | Target-device applicability / provenance | Current static CoreGraphics evidence |
|---:|---|---|---|---|
| Baseline | iOS 26.6.1 | 23G83 | Target-device restore image; baseline | Compared against 23H30; 25 shared `aa_*` symbols, 15 normalized streams differ |
| 4 | iOS 26.6.2 | 23G90 | Target-device restore image listed; currently unsigned in the catalog checked 2026-10-29 | Not yet extracted or compared |
| Historical | iOS 26.7 | 23H24 | Target-device image listed | Compared against 23H30; 25 shared `aa_*` symbols, 15 normalized streams differ |
| Reference | iOS 26.7.1 | 23H30 | Fixed-reference build | Reference CoreGraphics hash/UUID recorded; antialiasing clamp constants validated |
| **1** | **iOS 26.7.2** | **23H128** | Apple advisory published 2026-10-26; target device is within the supported iPhone 11-and-later family. Verify exact `iPhone17,4` image and provenance before extraction. | Not yet extracted or compared |
| 5 | iOS 27.0 | 24A437 | Target-device restore image listed; unsigned in the catalog checked 2026-10-29 | Not yet extracted or compared |
| 3 | iOS 27.0.1 | 24A446 | Target-device restore image listed; signed in the catalog checked 2026-10-29 | Not yet extracted or compared |
| Excluded | iOS 27.1 | 24A94425 | Previously identified as iPhone Duo-only; not a target-device build for `iPhone17,4` | Excluded from the device-specific matrix |
| **2** | **iOS 27.2** | **24B119** | Apple release dated 2026-10-26; device-specific `iPhone17,4` image listed and signed in the catalog checked 2026-10-29 | Not yet extracted or compared |

## Next analysis order

1. **23H128 (26.7.2)** — most recent 26.x build; the release advisory reports an Accelerate bounds-checking fix, which must not be conflated with a CoreGraphics change.
2. **24B119 (27.2)** — newest public build in this snapshot and device-specific firmware is listed.
3. **24A446 (27.0.1)** — current signed 27.x image for the target device.
4. **23G90 (26.6.2)** — near-baseline comparison.
5. **24A437 (27.0)** — historical pre-27.0.1 comparison.

## Source references

- Apple security releases: https://support.apple.com/en-us/100100
- Apple Developer release feed: https://developer.apple.com/news/releases/
- iPhone 16 Plus device firmware catalog: https://www.ipsw.dev/iPhone17%2C4
- iOS 26.7.2 Apple security advisory (released 2026-10-26): https://support.apple.com/en-us/149227
- iOS 27.2 Apple security advisory (released 2026-10-26): https://support.apple.com/en-us/149230
- Device-specific iOS 27.2 restore image listing: https://ipsw.me/install/iPhone17%2C4/24B119/

## Evidence rules

- A published build number or supported-device list does not mean its CoreGraphics binary has been analyzed.
- The existing 23G83/23H30 and 23H24/23H30 comparisons are static evidence only.
- Every new row must remain “not analyzed” until the exact device-specific firmware is verified, extracted, and checked for CoreGraphics SHA-256 and Mach-O UUID; the function comparison and relevant constant checks must complete; and test/artifact references are recorded.
- See [the 2026-10-29 callback and coordinate-safety trace](coregraphics-callback-coordinate-safety-2026-10-29.md) for the resolved renderer callback addresses, coordinate-check findings, and unresolved shared-cache references.
- iOS 27.1 is excluded from target-device binary analysis because the listed build is not applicable to `iPhone17,4`.
