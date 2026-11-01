# Firmware release matrix — 2026-10-29

Target device: iPhone 16 Plus (`iPhone17,4`, board `D48AP`). This is a release inventory, not a compatibility or vulnerability conclusion.

| Priority | Release | Build | Target-device applicability / provenance | Current static CoreGraphics evidence |
|---:|---|---|---|---|
| **Baseline — provenance review required** | **iOS 26.6.1** | **23G83** | Target-device restore image; baseline. The 2026-11-01 rerun (workflow 41332951724) labels the target 23G83 but extracts CoreGraphics SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`, identical to the independently recorded 23G90 hash. This conflicts with earlier 23G83 SHA-256 `0dc5ef74a54e7040857af5cafe796fa647f6dd552b4688fece7d5d84d2fb08ba`. Do not use the latest run as independent 23G83 evidence until firmware provenance is reconciled. | Earlier 23G83 evidence remains historical; latest rerun is quarantined pending provenance verification. |
| **Completed** | **iOS 26.6.2** | **23G90** | Exact `iPhone17,4` restore image resolved to an Apple CDN URL and extracted successfully in workflow run [41330882278](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41330882278). Catalog signing reports remain conflicting (IPSW.me marks unsigned; AppleSN lists signed for 31 devices, checked 2026-11-01); successful offline download/extraction does not establish restore authorization. | Compared against 23H30; 25 shared `aa_*` symbols, all 25 compared, 15 normalized streams differ, zero disassembly failures. Target CoreGraphics SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`, size 9,294,928 bytes, UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`. Semantic `_path_coordinates_are_safe` load and fixed reference both contain `0000000065cdcd41` (`1,000,000,000.0`). CFG audit: 21 target conversions with no detected dominating self-compare/NaN-branch or clamp-reference pattern; fixed reference 24 conversions, 22 with the structural NaN-guard pattern and all 24 with clamp-reference loads. Heuristic only; see assessment and run artifacts. |
| Historical | iOS 26.7 | 23H24 | Target-device image listed | Compared against 23H30; 25 shared `aa_*` symbols, 15 normalized streams differ |
| Reference | iOS 26.7.1 | 23H30 | Fixed-reference build | Reference CoreGraphics hash/UUID recorded; antialiasing clamp constants validated |
| Excluded pending compatible firmware | iOS 26.7.2 | 23H128 | The matrix workflow's device/build filter returned zero iPhone17,4 IPSWs for this build; the previous attempt failed before extraction. Treat the advisory as release-level context only unless a compatible target-device image is independently verified. | Not analyzed; no binary-comparison evidence |
| 5 | iOS 27.0 | 24A437 | Target-device restore image listed; unsigned in the catalog checked 2026-10-29 | Not yet extracted or compared |
| **Completed** | **iOS 27.0.1** | **24A446** | Target-device `iPhone17,4` restore image resolved and extracted successfully in workflow run 40940524899 | Compared against 23H30; 12 shared `aa_*` symbols, all 12 normalized streams differ; zero disassembly failures. Target CoreGraphics SHA-256 `1a0143dc707a9f85296621dd184705f6ce90ae0e6fa3b91ad6b4ea41b6355f33`, UUID `CF583D9C-9E49-3959-8C09-1E7141C57781`. Semantic safety-limit load matches reference at `1,000,000,000.0`; see artifacts and assessment. |
| Excluded | iOS 27.1 | 24A94425 | Previously identified as iPhone Duo-only; not a target-device build for `iPhone17,4` | Excluded from the device-specific matrix |
| **Completed** | **iOS 27.2** | **24B119** | Apple release dated 2026-10-26; device-specific `iPhone17,4` image resolved and extracted successfully | Compared against 23H30 in [run 40904316027](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40904316027). Target CoreGraphics SHA-256 `0e9eedce7a9f09448dbd1deb19b94c95b1440e15fadfcbbb953e710a31b153d3`, UUID `314A6344-864D-33EB-8A8C-F8279D3014C8`; 12 shared `aa_*` symbols compared, all 12 streams differ. Semantic `_path_coordinates_are_safe` limit matches 23H30 at `1,000,000,000.0` (see assessment and run artifacts).

## Next analysis order

1. **24A437 (27.0)** — next historical pre-27.0.1 comparison; verify the exact iPhone17,4 image before extraction.
2. **23H128 (26.7.2)** — excluded from the executable matrix unless a valid iPhone17,4 restore image can be independently verified; the prior filter returned zero IPSWs. The advisory's Accelerate fix must not be conflated with a CoreGraphics change.

## Source references

- Apple security releases: https://support.apple.com/en-us/100100
- Apple Developer release feed: https://developer.apple.com/news/releases/
- iPhone 16 Plus device firmware catalog: https://www.ipsw.dev/iPhone17%2C4
- Exact iPhone17,4 / 23G90 image and signing status (IPSW.me): https://ipsw.me/download/iPhone17%2C4/23G90/
- Cross-catalog 23G90 signing status (AppleSN): https://applesn.info/firmware/ios/
- iOS 26.7.2 Apple security advisory (released 2026-10-26): https://support.apple.com/en-us/149227
- iOS 27.2 Apple security advisory (released 2026-10-26): https://support.apple.com/en-us/149230
- Device-specific iOS 27.2 restore image listing: https://ipsw.me/install/iPhone17%2C4/24B119/

## Evidence rules

- A published build number or supported-device list does not mean its CoreGraphics binary has been analyzed.
- The 23G83/23H30, 23H24/23H30, and 24B119/23H30 comparisons are static evidence only. The 24B119 run also confirms that `_path_coordinates_are_safe` loads the same `1,000,000,000.0` value as 23H30, despite the section-relative address differing.
- Every new row must remain “not analyzed” until the exact device-specific firmware is verified, extracted, and checked for CoreGraphics SHA-256 and Mach-O UUID; the function comparison and relevant constant checks must complete; and test/artifact references are recorded.
- See [the 2026-10-29 callback and coordinate-safety trace](coregraphics-callback-coordinate-safety-2026-10-29.md) for the resolved renderer callback addresses, coordinate-check findings, and unresolved shared-cache references.
- iOS 27.1 is excluded from target-device binary analysis because the listed build is not applicable to `iPhone17,4`.


## 24A446 comparison result (workflow run 40940524899, 2026-10-29)

The additional-build workflow completed successfully for iPhone 16 Plus (`iPhone17,4`), target build `24A446` versus fixed reference `23H30`. The target CoreGraphics binary is 9,949,872 bytes, SHA-256 `1a0143dc707a9f85296621dd184705f6ce90ae0e6fa3b91ad6b4ea41b6355f33`, Mach-O UUID `CF583D9C-9E49-3959-8C09-1E7141C57781`. Twelve common `aa_*` symbols were compared; all twelve normalized instruction streams differ and there were zero disassembly failures. These differences are comparison leads only, not CVE attribution.

The address-resolving `_path_coordinates_are_safe` checker confirms the target's actual `d4` load resolves to virtual address `0x1843795b0`, `__TEXT,__const` section offset `0x1deab0`, file offset `0x74c5b0`. The reference load resolves to `0x1847e96a8`, section offset `0x5a28`, file offset `0x4fe6a8`. Both contain `0000000065cdcd41`, float64 `1,000,000,000.0`.

The static conversion-CFG audit examined six functions (`_aa_moveto`, `_aa_lineto`, `_aa_clipping`, `_aa_cubeto`, `_aa_quadto`, `_aa_rectat`). In the target, it identified 15 conversion sites and no dominating self-compare/NaN-branch pattern or clamp-reference load for those sites. In the fixed reference, it identified 17 conversion sites; 16 had a detected dominating self-compare/NaN branch and all 17 had a detected dominating clamp-reference load. The target `_aa_moveto` function also contains one unresolved indirect control transfer. These are structural CFG heuristics, not register/value dataflow proofs: absence of a detected pattern is not proof that no equivalent guard exists, and presence does not prove the loaded clamp is applied to the converted value. The artifact explicitly records the limitations.

Artifacts: [workflow run 40940524899](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40940524899), [comparison evidence ZIP](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40940524899/artifacts/12927227806), [diagnostic disassembly ZIP](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40940524899/artifacts/12927412459). The workflow's extraction, comparison, artifact upload, and cleanup steps all succeeded.


## 23G90 (iOS 26.6.2) comparison result — workflow run 41330882278 (2026-11-01)

The additional-build workflow [41330882278](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41330882278) completed successfully on branch head `055328cb0f000a59d7f6c5c3e774a38fc518b38e`, for target device `iPhone17,4`, target build `23G90`, and fixed reference `23H30`. All 11 job steps succeeded, including exact-device restore-image resolution, target dyld-cache extraction, fixed-reference OTA download and extraction, comparison, artifact upload, and cleanup.

- **Firmware resolution:** the target metadata resolved to Apple CDN URL `https://updates.cdn-apple.com/2026SummerFCS/911faed2-7d37-4532-8a4a-bd60530e1b11/iPhone17,4_26.6.2_23G90_Restore.ipsw`. The workflow downloaded/extracted the target cache successfully. This confirms image availability and offline analyzability at run time, not that Apple currently authorizes device restoration. The catalog signing discrepancy remains open.
- **Target CoreGraphics:** 9,294,928 bytes; SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`; arm64e Mach-O UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`.
- **Fixed reference CoreGraphics:** 9,294,928 bytes; SHA-256 `c5ebb5405dcd271fcab53cd4de0f59b9106672f86f790b7842a4702838275285`; UUID `4D24CA95-6D98-3968-BA43-D63976262D3D`.
- **Function comparison:** 25 target and 25 reference `aa_*` symbols; 25 common; all 25 successfully compared; 15 normalized instruction streams differ; zero disassembly failures. The changed-symbol list is `_aa_cache_render`, `_aa_clip_edge`, `_aa_clipping`, `_aa_close`, `_aa_create`, `_aa_cubeto`, `_aa_free_edges`, `_aa_line_render`, `_aa_line_render_shape`, `_aa_lineto`, `_aa_moveto`, `_aa_quadto`, `_aa_rectat`, `_aa_render`, and `_aa_render_shape`.
- **Semantic coordinate-safety limit:** the checker resolved the actual `ADRP` + `LDR d4` load in `_path_coordinates_are_safe`, rather than relying on a fixed section-relative offset. Target effective address `0x1847c20e8`, `__TEXT,__const` section offset `0x5a28`, file offset `0x4fe0e8`; fixed reference effective address `0x1847e96a8`, section offset `0x5a28`, file offset `0x4fe6a8`. Both contain `0000000065cdcd41`, little-endian float64 `1,000,000,000.0`.
- **Antialiasing constants:** the fixed-reference validation found 36 references and verified both expected constants, `-1073737729.0` and `+1073737729.0`, at their mapped `__TEXT,__const` offsets.
- **Conversion CFG audit (heuristic):** seven functions were analyzed on each side: `_aa_moveto`, `_aa_lineto`, `_aa_clip_edge`, `_aa_clipping`, `_aa_cubeto`, `_aa_quadto`, and `_aa_rectat`. Target: 21 conversion sites, zero with a detected dominating self-compare, NaN branch, or clamp-reference load. Fixed reference: 24 conversion sites; 22 with the detected dominating self-compare/NaN-branch structure and all 24 with a detected dominating clamp-reference load. No unresolved control transfers were reported in these audited functions.
- **Important binary-identity note:** the 23G90 target reports the same Mach-O UUID as the earlier 23G83 target, but its SHA-256 and file size differ. UUID equality is not byte identity and should not be treated as proof that the builds contain identical CoreGraphics code.

The CFG result is a structural heuristic, not exact floating-point value tracking or a proof of branch/value dominance for the converted operand. Detected patterns do not prove a clamp is applied to the exact value; absent patterns do not exclude equivalent guards implemented differently. The normalized function differences are triage leads, not CVE attribution. No binary was executed and no device was accessed or modified.

Artifacts: [workflow run 41330882278](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41330882278), evidence ZIP artifact ID `13093434027`, diagnostics ZIP artifact ID `13093618642`.


## 23G83 provenance discrepancy — latest rerun quarantined (2026-11-01)

The branch-head comparison workflow [41332951724](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41332951724) completed successfully on commit `1c1aa345b97a535a7ee20724b81ec2988431857e`. Unit-test workflows [41332951645](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41332951645) and [41332948667](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41332948667) also passed. However, artifact inspection found a source-identity inconsistency that prevents treating this run as validated 23G83 evidence.

- Workflow configuration names the target step as iOS 26.6.1 / build `23G83` and uses the hard-coded Apple CDN URL ending `iPhone17,4_26.6.1_23G83_Restore.ipsw`.
- The extracted target CoreGraphics metadata in the comparison JSON labels it `23G83`, but reports SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`, size 9,294,928 bytes, UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`.
- That SHA-256/size/UUID tuple exactly matches the separately run and independently catalog-resolved 23G90 workflow [41330882278](https://github.com/mirkolanvojov-collab/Freedom27).
- It conflicts with the earlier preserved 23G83 result from workflow [40884242887](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40884242887): SHA-256 `0dc5ef74a54e7040857af5cafe796fa647f6dd552b4688fece7d5d84d2fb08ba`, UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`. The UUID matches but the binary hash differs.
- The current workflow's target extraction log records a remote dyld-cache extraction path under `23G83__iPhone17,4`, but does not preserve the resolved target restore-image metadata/manifest or a cryptographic identity for the remote source image. The comparison JSON's build label is supplied by the workflow and is not independent proof of the image build.

**Disposition:** quarantine the latest 23G83 comparison output (artifact IDs `13094269122` and `13095321180`) from substantive build-specific conclusions. Do not overwrite the historical 23G83 baseline with this run. This is a provenance/chain-of-custody discrepancy, not evidence of a CoreGraphics vulnerability or of malicious substitution.

**Required correction:** make the baseline workflow resolve the target URL from current exact-device/build metadata at run time, preserve that metadata and URL in diagnostics, verify the selected device/build identity from the downloaded restore image's manifest before remote extraction, and fail closed if the manifest does not identify `iPhone17,4` / `23G83`. Record the source image digest when the complete image is downloaded; if remote extraction remains used, capture and validate the manifest metadata before invoking it. Re-run only after those checks are implemented. Then compare the resulting CoreGraphics SHA-256 to the historical 23G83 record and investigate any difference rather than assuming it is harmless.

The latest workflow's 25-symbol comparison and conversion-CFG output may be retained as diagnostic material, but must not be attributed to 23G83 until the source identity issue is resolved. The reported 15 changed symbols and heuristic conversion counts are therefore not accepted as new 23G83 evidence.

Artifacts: [comparison evidence ZIP](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41332951724/artifacts/13094269122), [diagnostics ZIP](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41332951724/artifacts/13095321180).
