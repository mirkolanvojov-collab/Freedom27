# CoreGraphics callback and coordinate-safety trace — 2026-10-29

Target: iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1 build `23G83`.
Reference: iOS 26.7.1 build `23H30`.
Method: read-only comparison of the preserved `ipsw macho disass` output and Mach-O section metadata. No binary execution, device interaction, or crafted input.

## Findings

### 1. Render callback dispatch is resolved for the captured branches

In both builds, `_RIPRenderPath` checks its renderer/context inputs, acquires the renderer, and selects one of two path-iteration callbacks:

- Stroke branch: constructs a pointer to `_ripr_path_stroke` and passes it as the callback argument to `_CGPathApply`.
- Fill branch: constructs a pointer to `_ripr_path_fill` and passes it as the callback argument to `_CGPathApply`.

The address-immediate differences are explained by code placement, not by a changed destination:

| Callback | 23G83 calculation | 23H30 calculation | Resolved symbol entry |
|---|---|---|---|
| `_ripr_path_stroke` | `0x184339000 + 0xa20 = 0x184339a20` | `0x184360000 + 0xf00 = 0x184360f00` | Matches captured callback entry in each binary |
| `_ripr_path_fill` | `0x184317000 + 0x16c = 0x18431716c` | `0x18433e000 + 0x640 = 0x18433e640` | Matches captured callback entry in each binary |

The fill callback directly branches on path-element type to `_aa_lineto`, `_aa_quadto`, `_aa_cubeto`, `_aa_moveto`, and `_aa_close` in both builds. This resolves the previously uncertain callback target for the captured fill branch. It does not prove that every public drawing operation reaches this branch.

### 2. Coordinate safety: direct caller and check sequence

Both captured `_CGContextDrawPath` bodies call `_path_coordinates_are_safe` after checking that the path exists and is not empty. The caller tests bit 0 of the return value: a clear bit branches to cleanup/early exit; a set bit proceeds toward the drawing path, including `_draw_path`.

The captured `_path_coordinates_are_safe` bodies have the same instruction sequence in both builds:

1. Call `_CGPathGetBoundingBox`.
2. Take absolute values of the two origin components.
3. Compare both origins against a shared floating-point limit.
4. Reject negative width/height and dimensions greater than the limit.
5. Add origin and extent, take absolute values, compute `fmaxnm` of the two results, and compare that maximum against the limit.
6. Return the comparison result.

The apparent limit-address change is resolved as a section-relative layout difference. In 23G83, `ADRP 0x1847c2000 + 0xe8 = 0x1847c20e8`; in 23H30, `ADRP 0x1847e9000 + 0x6a8 = 0x1847e96a8`. Each address is at offset `0x5a28` from that binary's `__TEXT,__const` section base. Thus the instruction operand changed while the section-relative constant location stayed the same. The current artifact set independently validates the two clamp constants used by the antialiasing code in 23H30; it does **not** include a byte-level validation of this particular safety-limit constant in both binaries.

### 3. Floating-point edge case to investigate, not a vulnerability finding

The safety-check disassembly uses `FCMP` followed by ordered conditions such as `B.GT` and `B.MI`, and the final comparison result is materialized with `CSET LE`. The captured function does not show an explicit unordered/NaN branch (for example, `B.VS`) at these checks. ARM floating-point comparisons have distinct unordered flags, so NaN behavior should be checked against the exact path-bounds semantics and the final `FMAXNM` behavior.

This is a static review lead only. The available disassembly does not establish that a NaN-containing path can produce a bounding box that passes the check, that such a path reaches this function with attacker-controlled values, or that any downstream memory-safety consequence exists. Do not describe it as a confirmed bypass or CVE match without additional evidence.

### 4. Remaining unresolved address differences

`_draw_path` has matching high-level setup and calls `_CGPathApplyWithBlock2` in both captures, but some global/shared-cache load offsets differ. These cannot yet be classified as mere relocation/layout changes because the workflow did not preserve a resolved shared-cache symbol/xref map for those data references. The previous workflow explicitly marks the experimental shared-cache xref scan as deferred. Resolving those references requires a bounded shared-cache mapping/symbol pass; do not infer object identity from raw offsets alone.

The captured `_ripc_Render` and `_ripr_path_fill` instruction streams are otherwise consistent across the two builds after normalization. No semantic difference is established for those bodies by the current artifacts.

## Build-matrix extension and priority

The device-specific firmware catalogs identify `iPhone17,4` images for `23G90`, `23H128`, `24A437`, `24A446`, and `24B119`. Apple’s release/security pages confirm iOS 26.7.2 (`23H128`) and iOS 27.2 (`24B119`) were released on 2026-10-26; device catalogs list the iPhone 16 Plus image for 27.2. The release matrix should prioritize:

1. **23H128 (iOS 26.7.2)** — newly released branch relative to the 23H30 reference; analyze for current code state.
2. **24B119 (iOS 27.2)** — newest public release in this snapshot and a device-specific image is listed.
3. **24A446 (iOS 27.0.1)** — current signed iOS 27 image for the target device.
4. **23G90 (iOS 26.6.2)** — useful near-baseline comparison; catalog lists the target-device restore image.
5. **24A437 (iOS 27.0)** — historical pre-27.0.1 comparison.

These are availability/provenance leads, not analyzed binaries. Each remains “not analyzed” until the exact target-device image is obtained, extraction is verified, CoreGraphics SHA-256/UUID are recorded, comparison and safety-constant checks pass, and artifacts/tests are linked. The 26.7.2 release advisory discusses an Accelerate out-of-bounds-write fix; that fact alone does not attribute the change to CoreGraphics or CVE-2026-86950.

## Reproducibility references

- Prior comparison workflow: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40782061277
- Comparison JSON artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40782061277/artifacts/12858829605
- Diagnostic disassembly artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40782061277/artifacts/12859596888
- Apple iOS 26.7.2 security advisory: https://support.apple.com/en-us/149227
- Apple iOS 27.2 security advisory: https://support.apple.com/en-us/149230
- Device-specific 27.2 image listing: https://ipsw.me/install/iPhone17%2C4/24B119/

## Evidence boundaries

This is static analysis of preserved disassembly and section metadata. It does not prove runtime reachability, exploitability, a working jailbreak, or behavior on builds not yet extracted and compared.
