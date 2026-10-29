# Firmware release matrix — 2026-10-29

Target device: iPhone 16 Plus (`iPhone17,4`, board `D48AP`). This is a release inventory, not a compatibility or vulnerability conclusion.

| Priority | Release | Build | Target-device applicability / provenance | Current static CoreGraphics evidence |
|---:|---|---|---|---|
| Baseline | iOS 26.6.1 | 23G83 | Target-device restore image; baseline | Compared against 23H30; 25 shared `aa_*` symbols, 15 normalized streams differ |
| 4 | iOS 26.6.2 | 23G90 | Target-device restore image listed; currently unsigned in the catalog checked 2026-10-29 | Not yet extracted or compared |
| Historical | iOS 26.7 | 23H24 | Target-device image listed | Compared against 23H30; 25 shared `aa_*` symbols, 15 normalized streams differ |
| Reference | iOS 26.7.1 | 23H30 | Fixed-reference build | Reference CoreGraphics hash/UUID recorded; antialiasing clamp constants validated |
| Excluded pending compatible firmware | iOS 26.7.2 | 23H128 | The matrix workflow's device/build filter returned zero iPhone17,4 IPSWs for this build; the previous attempt failed before extraction. Treat the advisory as release-level context only unless a compatible target-device image is independently verified. | Not analyzed; no binary-comparison evidence |
| 5 | iOS 27.0 | 24A437 | Target-device restore image listed; unsigned in the catalog checked 2026-10-29 | Not yet extracted or compared |
| 3 | iOS 27.0.1 | 24A446 | Target-device restore image listed; signed in the catalog checked 2026-10-29 | Not yet extracted or compared |
| Excluded | iOS 27.1 | 24A94425 | Previously identified as iPhone Duo-only; not a target-device build for `iPhone17,4` | Excluded from the device-specific matrix |
| **Completed** | **iOS 27.2** | **24B119** | Apple release dated 2026-10-26; device-specific `iPhone17,4` image resolved and extracted successfully | Compared against 23H30 in [run 40904316027](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40904316027). Target CoreGraphics SHA-256 `0e9eedce7a9f09448dbd1deb19b94c95b1440e15fadfcbbb953e710a31b153d3`, UUID `314A6344-864D-33EB-8A8C-F8279D3014C8`; 12 shared `aa_*` symbols compared, all 12 streams differ. Semantic `_path_coordinates_are_safe` limit matches 23H30 at `1,000,000,000.0` (see assessment and run artifacts).

## Next analysis order

1. **24A446 (27.0.1)** — next target-device comparison; device-specific image was listed as signed in the 2026-10-29 catalog snapshot.
2. **23G90 (26.6.2)** — near-baseline comparison; verify signing and image availability again before extraction.
3. **24A437 (27.0)** — historical pre-27.0.1 comparison.
4. **23H128 (26.7.2)** — excluded from the executable matrix unless a valid iPhone17,4 restore image can be verified; the prior filter returned zero IPSWs. The advisory's Accelerate fix must not be conflated with a CoreGraphics change.

## Source references

- Apple security releases: https://support.apple.com/en-us/100100
- Apple Developer release feed: https://developer.apple.com/news/releases/
- iPhone 16 Plus device firmware catalog: https://www.ipsw.dev/iPhone17%2C4
- iOS 26.7.2 Apple security advisory (released 2026-10-26): https://support.apple.com/en-us/149227
- iOS 27.2 Apple security advisory (released 2026-10-26): https://support.apple.com/en-us/149230
- Device-specific iOS 27.2 restore image listing: https://ipsw.me/install/iPhone17%2C4/24B119/

## Evidence rules

- A published build number or supported-device list does not mean its CoreGraphics binary has been analyzed.
- The 23G83/23H30, 23H24/23H30, and 24B119/23H30 comparisons are static evidence only. The 24B119 run also confirms that `_path_coordinates_are_safe` loads the same `1,000,000,000.0` value as 23H30, despite the section-relative address differing.
- Every new row must remain “not analyzed” until the exact device-specific firmware is verified, extracted, and checked for CoreGraphics SHA-256 and Mach-O UUID; the function comparison and relevant constant checks must complete; and test/artifact references are recorded.
- See [the 2026-10-29 callback and coordinate-safety trace](coregraphics-callback-coordinate-safety-2026-10-29.md) for the resolved renderer callback addresses, coordinate-check findings, and unresolved shared-cache references.
- iOS 27.1 is excluded from target-device binary analysis because the listed build is not applicable to `iPhone17,4`.
