# Firmware release matrix — 2026-10-28

Target device: iPhone 16 Plus (`iPhone17,4`, board `D48AP`). This is a release inventory, not a compatibility or vulnerability conclusion.

| Release | Build | Target-device applicability | Current static CoreGraphics evidence |
|---|---|---|---|
| iOS 26.6.1 | 23G83 | Target baseline | Compared against 23H30; 25 shared `aa_*` symbols, 15 normalized streams differ |
| iOS 26.6.2 | 23G90 | Target model listed in firmware catalog | Not yet extracted or compared in this workflow |
| iOS 26.7 | 23H24 | Target model listed in firmware catalog | Compared against 23H30; 25 shared `aa_*` symbols, 15 normalized streams differ |
| iOS 26.7.1 | 23H30 | Fixed-reference build | Reference binary and constants validated |
| iOS 26.7.2 | 23H128 | Target model included in the iOS 26.7.2 supported device family; verify the exact restore image before extraction | Not yet extracted or compared |
| iOS 27.0 | 24A437 | Target model supported | Not yet extracted or compared |
| iOS 27.0.1 | 24A446 | Target model supported | Not yet extracted or compared |
| iOS 27.1 | 24A94425 | Published for iPhone Duo only; not applicable to iPhone17,4 | Excluded from this device-specific matrix |
| iOS 27.2 | 24B119 | Target model supported; newest public release as of 2026-10-28 | Not yet extracted or compared |

## Source references

- Apple security releases (latest versions and dates): https://support.apple.com/en-us/100100
- Apple Developer release feed (build numbers): https://developer.apple.com/news/releases/
- iPhone 16 Plus firmware catalog and per-device build list: https://www.ipsw.dev/iPhone17%2C4
- iOS 26.7.2 Apple security advisory: https://support.apple.com/en-us/149227
- iOS 27.2 Apple security advisory: https://support.apple.com/en-us/149230

## Evidence rules

- A published build number or supported-device list does not mean the binary has been analyzed.
- The existing 23G83/23H30 and 23H24/23H30 comparisons are static evidence only.
- Each new row needs device-specific firmware provenance, verified extraction, CoreGraphics hash, comparison output, and test/artifact references before it can be marked analyzed.
- iOS 27.1 is listed for completeness but is not a target-device build for iPhone17,4.
