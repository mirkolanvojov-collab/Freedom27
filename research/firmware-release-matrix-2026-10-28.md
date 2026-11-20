# Firmware release matrix — 2026-10-29

Target device: iPhone 16 Plus (`iPhone17,4`, board `D48AP`). This is a release inventory, not a compatibility or vulnerability conclusion.

| Priority | Release | Build | Target-device applicability / provenance | Current static CoreGraphics evidence |
|---:|---|---|---|---|
| **Locally verified; CoreGraphics byte-identical to 23G90** | **iOS 26.6.1** | **23G83** | Paired full-restore workflow [41351395468](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41351395468) downloaded and SHA-256 checked the complete `iPhone17,4` IPSW (11,225,458,130 bytes; `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`), verified the embedded BuildManifest byte-for-byte against the separately extracted manifest, and confirmed `iPhone17,4` / 26.6.1 / 23G83. | Local CoreGraphics is 9,294,928 bytes, UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`, SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`; byte-identical to the locally extracted 23G90 component. The older remote-extraction hash `0dc5ef74...` remains quarantined as a lower-provenance historical observation; no malicious substitution is inferred. |
| **Completed** | **iOS 26.6.2** | **23G90** | Exact `iPhone17,4` restore image resolved to an Apple CDN URL and extracted successfully in workflow run [41330882278](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41330882278). Catalog signing reports remain conflicting (IPSW.me marks unsigned; AppleSN lists signed for 31 devices, checked 2026-11-01); successful offline download/extraction does not establish restore authorization. | Compared against 23H30; 25 shared `aa_*` symbols, all 25 compared, 15 normalized streams differ, zero disassembly failures. Target CoreGraphics SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`, size 9,294,928 bytes, UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`. Semantic `_path_coordinates_are_safe` load and fixed reference both contain `0000000065cdcd41` (`1,000,000,000.0`). CFG audit: 21 target conversions with no detected dominating self-compare/NaN-branch or clamp-reference pattern; fixed reference 24 conversions, 22 with the structural NaN-guard pattern and all 24 with clamp-reference loads. Heuristic only; see assessment and run artifacts. |
| **Completed** | **iOS 26.7** | **23H24** | Exact iPhone17,4 OTA resolved from live metadata/catalog fallback, downloaded and extracted in workflow run [41332951724](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41332951724) | Direct comparison against 23H30: CoreGraphics SHA-256 `c2148f5b9ddfd03ba2989f4410ef5421c55814a5f2d2891c1b548d09234288ee`, UUID `4C04F0CB-7A29-3BE8-9B93-4E86FE0DEC4E`; 25 common `aa_*` symbols, 15 normalized streams differ, zero disassembly failures. CFG audit: 21 target conversions (0 detected dominating NaN patterns / 0 clamp-reference loads); fixed 24 (22 NaN patterns / 24 clamp loads). Heuristic only. |
| Reference | iOS 26.7.1 | 23H30 | Fixed-reference build | Reference CoreGraphics hash/UUID recorded; antialiasing clamp constants validated |
| Excluded pending compatible firmware | iOS 26.7.2 | 23H128 | The matrix workflow's device/build filter returned zero iPhone17,4 IPSWs for this build; the previous attempt failed before extraction. Treat the advisory as release-level context only unless a compatible target-device image is independently verified. | Not analyzed; no binary-comparison evidence |
| **Locally verified; comparison queued** | **iOS 27.0** | **24A437** | Exact `iPhone17,4` full restore verified in [workflow 41369824538](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41369824538): 12,313,212,859 bytes; SHA-256 `a8bed747c08709a63e5b9d55fa87bfca2839245f91a82082a8c30b8833fae149`; embedded BuildManifest confirms iPhone17,4 / 27.0 / 24A437. Manifest SHA-256 `cba7917c25f78173e291a3939ad66748fe629f74e1598c82f3ec42c44eeba8b3`. Catalog signing status conflicts; offline provenance does not establish restore authorization. | CoreGraphics locally extracted from the verified image: 9,949,872 bytes; SHA-256 `5e87f6baa2c5f2d83d7e92cddd7d7c02ee852e8db8acab3887c4e7b5a81a0868`. Symbol/function comparison against 23H30 has been queued via [workflow trigger commit c18597c](https://github.com/mirkolanvojov-collab/Freedom27/commit/c18597c885e710ad4958e7b5a590f47e675ddd4e); the workflow will require the comparison extraction hash to match this locally verified binary before analysis. |
| **Completed** | **iOS 27.0.1** | **24A446** | Target-device `iPhone17,4` restore image resolved and extracted successfully in workflow run 40940524899 | Compared against 23H30; 12 shared `aa_*` symbols, all 12 normalized streams differ; zero disassembly failures. Target CoreGraphics SHA-256 `1a0143dc707a9f85296621dd184705f6ce90ae0e6fa3b91ad6b4ea41b6355f33`, UUID `CF583D9C-9E49-3959-8C09-1E7141C57781`. Semantic safety-limit load matches reference at `1,000,000,000.0`; see artifacts and assessment. |
| Excluded | iOS 27.1 | 24A94425 | Previously identified as iPhone Duo-only; not a target-device build for `iPhone17,4` | Excluded from the device-specific matrix |
| **Completed** | **iOS 27.2** | **24B119** | Apple release dated 2026-10-26; device-specific `iPhone17,4` image resolved and extracted successfully | Compared against 23H30 in [run 40904316027](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40904316027). Target CoreGraphics SHA-256 `0e9eedce7a9f09448dbd1deb19b94c95b1440e15fadfcbbb953e710a31b153d3`, UUID `314A6344-864D-33EB-8A8C-F8279D3014C8`; 12 shared `aa_*` symbols compared, all 12 streams differ. Semantic `_path_coordinates_are_safe` limit matches 23H30 at `1,000,000,000.0` (see assessment and run artifacts).

## Next analysis order

1. **24A437 (27.0)** — next historical pre-27.0.1 comparison. The exact-device image and independent catalog SHA-256 are now identified; next step is full-image download, local SHA-256 verification, embedded BuildManifest/device-build verification, then local dyld extraction. The build is reported unsigned, which does not prevent offline static analysis.
2. **23H128 (26.7.2)** — excluded from the executable matrix unless a valid iPhone17,4 restore image can be independently verified; the prior filter returned zero IPSWs. The advisory's Accelerate fix must not be conflated with a CoreGraphics change.

## Source references

- Apple security releases: https://support.apple.com/en-us/100100
- Apple Developer release feed: https://developer.apple.com/news/releases/
- iPhone 16 Plus device firmware catalog: https://www.ipsw.dev/iPhone17%2C4
- Exact iPhone17,4 / 24A437 restore image, SHA-256, and signing status: https://www.applefirmwares.com/firmware/iPhone17%2C4/27.0
- Independent iPhone17,4 / 24A437 checksum listing: https://applesn.info/firmware/ipsw/iPhone17%2C4/24A437/
- iPhone17,4 / 24A437 release/device listing and file size: https://theapplewiki.com/wiki/Firmware/iPhone/27.x
- Exact iPhone17,4 / 23G90 image and signing status (IPSW.me): https://ipsw.me/download/iPhone17%2C4/23G90/
- Cross-catalog 23G90 signing status (AppleSN): https://applesn.info/firmware/ios/
- iOS 26.7.2 Apple security advisory (released 2026-10-26): https://support.apple.com/en-us/149227
- iOS 27.2 Apple security advisory (released 2026-10-26): https://support.apple.com/en-us/149230
- Device-specific iOS 27.2 restore image listing: https://ipsw.me/install/iPhone17%2C4/24B119/

## Evidence rules

- A published build number or supported-device list does not mean its CoreGraphics binary has been analyzed.
- The paired 23G83/23G90 local restore reconciliation establishes byte identity of their CoreGraphics components; the historical remote-extraction 23G83 hash remains quarantined. The 23G83/23H30, 23H24/23H30, and 24B119/23H30 comparisons are static evidence only. The 24B119 run also confirms that `_path_coordinates_are_safe` loads the same `1,000,000,000.0` value as 23H30, despite the section-relative address differing.
- Every new row must remain “not analyzed” until the exact device-specific firmware is verified, extracted, and checked for CoreGraphics SHA-256 and Mach-O UUID; the function comparison and relevant constant checks must complete; and test/artifact references are recorded.
- See [the 2026-10-29 callback and coordinate-safety trace](coregraphics-callback-coordinate-safety-2026-10-29.md) for the resolved renderer callback addresses, coordinate-check findings, and unresolved shared-cache references.
- iOS 27.1 is excluded from target-device binary analysis because the listed build is not applicable to `iPhone17,4`.


## 24A437 local restore provenance — workflow run 41369824538 (2026-11-02)

The dedicated local-restore workflow [41369824538](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41369824538) completed successfully for iPhone 16 Plus (`iPhone17,4`), iOS 27.0 build `24A437`. It downloaded the full restore IPSW, verified its complete-file SHA-256 against the independent catalog checksum, confirmed the embedded BuildManifest identifies the expected product type/version/build, extracted the arm64e dyld cache locally, extracted CoreGraphics, and uploaded the evidence before deleting the large restore image and cache from the runner.

- Restore image: `iPhone17,4_27.0_24A437_Restore.ipsw`; 12,313,212,859 bytes; SHA-256 `a8bed747c08709a63e5b9d55fa87bfca2839245f91a82082a8c30b8833fae149`.
- BuildManifest: 468,627 bytes; SHA-256 `cba7917c25f78173e291a3939ad66748fe629f74e1598c82f3ec42c44eeba8b3`; supported product type includes `iPhone17,4`; manifest reports product version `27.0`, build `24A437`.
- CoreGraphics: 9,949,872 bytes; SHA-256 `5e87f6baa2c5f2d83d7e92cddd7d7c02ee852e8db8acab3887c4e7b5a81a0868`.
- Evidence artifact: [24A437-iPhone17,4-local-restore-provenance](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41369824538/artifacts/13109037449).

This verifies local file-byte integrity against the catalog checksum and the embedded device/build identity. It does not verify Apple's cryptographic restore authorization; signing catalogs remain inconsistent. No device was accessed or restored.

Commit `c18597c885e710ad4958e7b5a590f47e675ddd4e` enables the matrix comparison workflow on branch updates and makes 24A437 the push-trigger default. It adds a hard assertion that the comparison workflow's extracted target CoreGraphics SHA-256 must equal the locally verified value above before symbol-level analysis proceeds. The comparison run has not yet completed; until it does, no function-difference or coordinate-safety conclusions are recorded for 24A437.

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
- **Important binary-identity note:** the paired local restore reconciliation subsequently verified that the extracted 23G83 and 23G90 CoreGraphics files are byte-identical, with matching size, SHA-256, and UUID. The older 23G83 remote-extraction hash remains a separate quarantined historical observation.

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


## 23H24 (iOS 26.7) direct patch-comparison result — workflow run 41332951724 (2026-11-01)

The workflow [41332951724](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41332951724) completed successfully. It resolved and downloaded the iPhone17,4 23H24 OTA, extracted its dyld cache, and compared CoreGraphics directly with fixed reference 23H30. The 23H24-specific output is `coregraphics-26-7-patch-comparison.json` in evidence artifact ZIP ID `13094269122`; diagnostics are ZIP ID `13095321180`.

- Target CoreGraphics: 9,294,928 bytes; SHA-256 `c2148f5b9ddfd03ba2989f4410ef5421c55814a5f2d2891c1b548d09234288ee`; Mach-O UUID `4C04F0CB-7A29-3BE8-9B93-4E86FE0DEC4E`.
- Fixed 23H30 CoreGraphics: 9,294,928 bytes; SHA-256 `c5ebb5405dcd271fcab53cd4de0f59b9106672f86f790b7842a4702838275285`; UUID `4D24CA95-6D98-3968-BA43-D63976262D3D`.
- 25/25 common `aa_*` symbols compared; 15 normalized instruction streams differ; zero disassembly failures.
- Seven-function conversion CFG audit: 21 target conversion sites, zero with detected dominating self-compare/NaN-branch patterns and zero with detected clamp-reference loads; 24 fixed-reference sites, 22 with the structural NaN-guard pattern and all 24 with clamp-reference loads. No unresolved control transfers. This is a structural heuristic, not exact value/register dataflow.
- The fixed-reference constant check found 36 references and verified `-1073737729.0` and `+1073737729.0`.

### 23G83 provenance discrepancy found in the same workflow

The same workflow's primary 23G83-labeled comparison output reports target SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`, size 9,294,928 bytes, and UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`. That SHA is already recorded for the separately downloaded 23G90 build. The 23G83 extraction log shows the expected `23G83__iPhone17,4` output directory, but the artifact does not preserve a signed BuildManifest/build-identity record that explains the hash collision with 23G90. Earlier baseline evidence records a different 23G83 CoreGraphics SHA-256 (`0dc5ef74a54e7040857af5cafe796fa647f6dd552b4688fece7d5d84d2fb08ba`). Therefore, do not treat the primary comparison's 23G83 label or its conversion audit as verified 23G83 evidence until the exact IPSW BuildManifest and extracted cache provenance are independently bound to the binary. The separate 23H24-to-23H30 result above is independently labeled in its own comparison JSON and is not affected by this 23G83 discrepancy.

No binary was executed and no device was accessed or modified.


## Resolver repair and rerun — workflow 41338740145 (2026-11-01)

The target IPSW resolver failed in the prior run because the Python candidate-parsing statement was not indented inside its nested token loop. Commit `1f24e4c5606eb3089dd4a756f19a1e76877b890e` corrects that indentation. The rerun [41338740145](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41338740145) completed successfully: exact-device 23G83 catalog resolution, target remote dyld extraction, fixed 23H30 OTA verification/extraction, optional 23H24 OTA resolution/extraction, both CoreGraphics comparison stages, diagnostics/evidence upload, and cleanup all passed. Tests run [41338740153](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41338740153) and [41338735971](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41338735971) passed.

The 23G83-labeled comparison JSON still reports CoreGraphics SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`, size 9,294,928 bytes, UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`—the same binary tuple previously associated with 23G90. The earlier 23G83 record remains `0dc5ef74a54e7040857af5cafe796fa647f6dd552b4688fece7d5d84d2fb08ba`. Thus the resolver syntax/indentation failure is fixed, but the exact-build source-identity hold is **not** resolved. This run still uses remote extraction and does not preserve a verified IPSW BuildManifest or full-image digest; do not accept its 23G83-labeled binary/CFG output as exact-build evidence.

The separate 23H24-to-23H30 stage completed successfully. Its 23H24 CoreGraphics is 9,294,928 bytes, SHA-256 `c2148f5b9ddfd03ba2989f4410ef5421c55814a5f2d2891c1b548d09234288ee`, UUID `4C04F0CB-7A29-3BE8-9B93-4E86FE0DEC4E`. It compared 25/25 common `aa_*` symbols, found 15 normalized instruction-stream differences, and had zero disassembly failures. Its conversion CFG audit reports 21 target conversion sites versus 24 in fixed 23H30; structural guard/clamp observations remain heuristic and are not proof of operand-level guarding or vulnerability.

Artifacts: diagnostics ZIP [13096103717](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41338740145/artifacts/13096103717); comparison evidence ZIP [13096018844](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41338740145/artifacts/13096018844).


## 23G83 BuildManifest verification — workflow run 41340835900 (2026-11-01)

The workflow [41340835900](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41340835900) successfully resolved the live catalog URL for iPhone17,4 / 23G83, retrieved BuildManifest.plist from that exact catalog selection, and passed the new fail-closed verifier before remote dyld extraction.

- Manifest size: 471,784 bytes.
- Manifest SHA-256: 0a1253579fffc40fb3353b9618fb8299190c48857b3af26734db2dbf63f3dfd6.
- ProductVersion=26.6.1, ProductBuildVersion=23G83.
- SupportedProductTypes=[iPhone17,4].
- Three BuildIdentities; each reports DeviceClass=d48ap, ApChipID=0x8140, ApBoardID=0x0A, with erase, update, and recovery variants.
- Remote dyld extraction for the resolved Apple CDN URL completed successfully.

This strengthens catalog-to-manifest identity evidence, but does not close the full chain-of-custody issue: the workflow retrieves the manifest via a selective remote IPSW member request, then separately performs remote dyld extraction. It does not download and hash the complete IPSW or cryptographically bind the retrieved manifest bytes to the exact source bytes used by remote extraction. The historical CoreGraphics hash conflict is therefore still unresolved, and the new target binary remains quarantined from exact-build conclusions.

The same run failed later in the optional 23H24 OTA-resolution step because ipsw download ota could not resolve gdmf.apple.com (DNS failure). The fixed 23H30 OTA had already downloaded and extracted successfully. No 23H24 or CoreGraphics comparison ran in this attempt. This is an external metadata-service availability failure, not a failure of the 23G83 manifest check.

Diagnostics artifact: [13098420071](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41340835900/artifacts/13098420071).


## 23G83 full restore-image provenance rerun — workflow 41347052092 (2026-11-01)

The full target restore pipeline now succeeds end-to-end. It downloads the complete exact-device Apple-CDN IPSW, calculates its SHA-256, compares the embedded BuildManifest.plist byte-for-byte with the separately extracted manifest, and extracts dyld from that same local IPSW before deleting it.

- Restore image: 11,225,458,130 bytes; SHA-256 101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f.
- Embedded/separate manifest match: true. Manifest SHA-256 0a1253579fffc40fb3353b9618fb8299190c48857b3af26734db2dbf63f3dfd6; identity iPhone17,4 / 26.6.1 / 23G83.
- Local dyld extraction: succeeded.
- Extracted CoreGraphics: 9,294,928 bytes; SHA-256 9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77; UUID 1EB92A97-21BD-3DB6-B285-714563E0C116.
- This CoreGraphics identity exactly matches the separately analyzed 23G90 image. It conflicts with historical 23G83 hash 0dc5ef74a54e7040857af5cafe796fa647f6dd552b4688fece7d5d84d2fb08ba (historical reported size 9,294,920 bytes; same UUID).
- The 23G83-labelled comparison against 23H30 completed with 25 shared aa_* symbols, 15 normalized streams changed, and zero disassembly failures. Because the extracted target component identity conflicts with historical evidence, do not treat this comparison as exact-23G83 CVE evidence yet.

This confirms the component came from the downloaded restore archive and the archive's manifest matches the expected device/build identity. It does not independently authenticate Apple's restore signature or explain why the CoreGraphics bytes match 23G90. Keep the target row quarantined pending comparison with an independent catalog checksum, manifest component metadata, and the historical 23G83 extraction chain.


## Independent restore checksum and local-image reconciliation (2026-11-01)

The 23G83 full IPSW SHA-256 computed in workflow 41347052092 matches the values independently published by [IPSW Downloads](https://ipsw.me/download/iPhone17%2C4/23G83/) and [Apple Firmwares](https://www.applefirmwares.com/firmware/iPhone17%2C4/26.6.1): `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`, size 11,225,458,130 bytes. The archive's embedded manifest also matches the separately extracted manifest byte-for-byte and identifies iPhone17,4 / 26.6.1 / 23G83.

The earlier historical 23G83 CoreGraphics hash (`0dc5ef74...`) was produced by remote dyld extraction in workflow 40193027374 using IPSW 3.1.739; no full restore image was downloaded or hashed in that run. The 2026-11-01 local restore extraction uses IPSW 3.1.741 and produces the 23G90-matching CoreGraphics hash (`9c2003a7...`). This points to an extraction provenance/tool-version difference as a possible explanation, not a firmware substitution finding. The paired local restore workflow [41351317547](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41351317547) will independently checksum both the 23G83 and 23G90 full restore images, extract both local dyld caches, and directly compare their CoreGraphics binaries. Its syntax check passed in [41351317558](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41351317558). Keep the historical 23G83 hash quarantined pending this result.


## Paired local restore reconciliation — 23G83 / 23G90 (2026-11-01)

Workflow [41351395468](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41351395468) completed successfully. Both full iPhone17,4 restore IPSWs matched their independent catalog SHA-256 values, both embedded BuildManifests identified the expected product/build, and both dyld caches were extracted from the local verified IPSWs.

- 23G83 restore: 11,225,458,130 bytes; SHA-256 `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`; manifest SHA-256 `0a1253579fffc40fb3353b9618fb8299190c48857b3af26734db2dbf63f3dfd6`.
- 23G90 restore: 11,225,388,519 bytes; SHA-256 `3c8d4bb6bfe6273ea297c2571e0108e196ef0e1da28c6c98dd268d35a4527480`; manifest SHA-256 `c4f63ee6e420f6c2056106fef31f47c4081462895c0d23cf6d86b08afd9914d8`.
- Extracted CoreGraphics from each: 9,294,928 bytes; SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`; UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`.
- Reconciliation output: `byte_identical: true`.

**Disposition:** the local-restore CoreGraphics bytes for 23G83 and 23G90 are identical. The historical 23G83 hash `0dc5ef74...` from the earlier remote extraction remains in the record as a quarantined, lower-provenance observation; it is not used as the current exact-source binary. The extraction-method/tool-version difference is a plausible but unproven explanation. This result clears the local component identity conflict, but does not verify Apple's restore authorization/signature or establish CVE attribution/reachability.

Evidence artifact: [13101825959](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41351395468).


## Superseding disposition — paired 23G83 / 23G90 local restore reconciliation (2026-11-01)

This section supersedes the earlier provisional 23G83 provenance-hold wording above wherever it says the local restore identity conflict remains unresolved or that the 23G83/23G90 component comparison is still pending.

The paired local restore workflow [41351395468](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41351395468) downloaded both exact-device full restore IPSWs, verified their complete-image SHA-256 values against independent catalog listings, checked each embedded BuildManifest against the separately extracted manifest, verified the expected iPhone17,4 product/build identity, extracted each dyld cache locally, and compared the CoreGraphics components. Both CoreGraphics files are byte-identical: 9,294,928 bytes, SHA-256 `9c2003a7123c0f6bb7f21b91b7d78847ba9c5a9fde678811b9a01b7fa1772b77`, UUID `1EB92A97-21BD-3DB6-B285-714563E0C116`.

The historical 23G83 hash `0dc5ef74a54e7040857af5cafe796fa647f6dd552b4688fece7d5d84d2fb08ba` remains quarantined because it came from an earlier remote extraction without full-image hashing and manifest binding. It is not the accepted local-restore identity. The difference is consistent with an extraction-path/tool-version discrepancy, but that explanation is not proven; no malicious substitution is inferred. Apple's restore authorization/signature has not been independently verified.

For 24A437, the published SHA-256 is now a useful fail-closed verification target, but no full-image download, local checksum, manifest verification, or CoreGraphics extraction has yet been performed. Catalog signing labels conflict; offline static analysis remains possible regardless of restore-signing status.
