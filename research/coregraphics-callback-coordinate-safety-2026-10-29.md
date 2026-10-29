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

The 23G83/23H30 pair resolves to the same section-relative limit location (`0x5a28`) in both binaries: 23G83 loads from `0x1847c20e8` (`ADRP 0x1847c2000 + 0xe8`) and 23H30 from `0x1847e96a8` (`ADRP 0x1847e9000 + 0x6a8`). A later matrix run added build 24B119, where the semantic load resolves instead to `0x184266070`, section-relative offset `0x1deb30`, file offset `0x750070`. The corrected checker reads the actual address referenced by `_path_coordinates_are_safe` rather than assuming the same section offset across builds. In 24B119 and 23H30, the loaded bytes are both `0000000065cdcd41`, decoding to `1,000,000,000.0`; the earlier 23G83/23H30 check also recorded these bytes at offset `0x5a28`. This validates the value for these analyzed binaries, but does not by itself prove the entire safety-check logic is equivalent.

### 3. Floating-point edge case to investigate, not a vulnerability finding

The safety-check disassembly uses `FCMP` followed by ordered conditions such as `B.GT` and `B.MI`, and the final comparison result is materialized with `CSET LE`. The captured function does not show an explicit unordered/NaN branch (for example, `B.VS`) at these checks. ARM floating-point comparisons have distinct unordered flags, so NaN behavior should be checked against the exact path-bounds semantics and the final `FMAXNM` behavior.

This is a static review lead only. The available disassembly does not establish that a NaN-containing path can produce a bounding box that passes the check, that such a path reaches this function with attacker-controlled values, or that any downstream memory-safety consequence exists. Do not describe it as a confirmed bypass or CVE match without additional evidence.

### 4. Remaining unresolved address differences

`_draw_path` has matching high-level setup and calls `_CGPathApplyWithBlock2` in both captures, but some global/shared-cache load offsets differ. These cannot yet be classified as mere relocation/layout changes because the workflow did not preserve a resolved shared-cache symbol/xref map for those data references. The previous workflow explicitly marks the experimental shared-cache xref scan as deferred. Resolving those references requires a bounded shared-cache mapping/symbol pass; do not infer object identity from raw offsets alone.

The captured `_ripc_Render` and `_ripr_path_fill` instruction streams are otherwise consistent across the two builds after normalization. No semantic difference is established for those bodies by the current artifacts.

## Build-matrix extension and priority

The device-specific firmware matrix has now completed a static CoreGraphics comparison for `24B119` vs `23H30` in [run 40904316027](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40904316027). That run compared 12 shared `aa_*` symbols, with all 12 normalized streams differing and zero disassembly failures; these differences are triage evidence only. The corrected safety-limit checker resolves the load address from each build's `_path_coordinates_are_safe` disassembly and confirms the loaded value matches `23H30` at `1,000,000,000.0`.

The next planned device-specific comparison is **24A446 (iOS 27.0.1)**, followed by `23G90` (26.6.2, subject to image availability/signing), then `24A437` (27.0). Build `23H128` (26.7.2) is currently excluded from executable matrix runs because the workflow's device/build filter returned zero `iPhone17,4` IPSWs; do not mark it analyzed unless a compatible image is independently verified. The 26.7.2 release advisory discusses an Accelerate out-of-bounds-write fix; that fact alone does not attribute the change to CoreGraphics or CVE-2026-86950.

## Reproducibility references

- Latest successful target/reference comparison workflow (run 40787926888, completed 2026-10-28): https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40787926888
- Latest comparison JSON artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40787926888/artifacts/12861297410
- Latest diagnostic disassembly artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40787926888/artifacts/12860928451
- Earlier comparison workflow and artifacts: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40782061277
- The successful run confirms target and reference dyld-cache extraction, both symbol-scoped comparisons, diagnostic upload, and cleanup completed. It did **not** run the additional-build matrix workflow.
- The semantic-address checker and regression test are now wired into the additional-build workflow. Run [40904316027](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40904316027) confirms the checker resolves the actual `d4` load and validates the `24B119` limit against `23H30`; this supersedes the earlier note that the safety-limit bytes were not yet validated for that build.
- Apple iOS 26.7.2 security advisory: https://support.apple.com/en-us/149227
- Apple iOS 27.2 security advisory: https://support.apple.com/en-us/149230
- Device-specific 27.2 image listing: https://ipsw.me/install/iPhone17%2C4/24B119/

## Evidence boundaries

This is static analysis of preserved disassembly and section metadata. It does not prove runtime reachability, exploitability, a working jailbreak, or behavior on builds not yet extracted and compared.


## Follow-up update: semantic safety-limit verification (2026-10-29)

The additional-build matrix run [40904316027](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40904316027) completed successfully for target build 24B119 against fixed reference 23H30. The target CoreGraphics SHA-256 is `0e9eedce7a9f09448dbd1deb19b94c95b1440e15fadfcbbb953e710a31b153d3`, Mach-O UUID `314A6344-864D-33EB-8A8C-F8279D3014C8`. Twelve common `aa_*` symbols were compared; all twelve normalized instruction streams differ, with zero disassembly failures.

The safety-limit checker now receives the `_path_coordinates_are_safe` disassembly for each binary and resolves the actual `adrp`/ `ldr d4` address pair. For 24B119 the resolved address is `0x184266070` (section offset `0x1deb30`, file offset `0x750070`); for 23H30 it is `0x1847e96a8` (section offset `0x5a28`, file offset `0x4fe6a8`). Both locations contain `0000000065cdcd41`, float64 `1,000,000,000.0`. The earlier 24B119 lookup at offset `0x5a28` was not the operand used by the target function and is not evidence of a changed or missing limit.

This closes the specific address-selection/value-validation blocker. It does not resolve the NaN/dataflow question, prove downstream guard semantics, attribute every changed `aa_*` stream to the CVE, or establish runtime reachability/exploitability. See [the target assessment](evidence/CVE-2026-86950-target-assessment.md) and the matrix evidence/diagnostics linked from the successful run.
