# Caller coordinate-clamping review for `_aa_lineto` — 2026-10-26

## Scope and evidence

This review re-examines the preserved target-side caller disassembly from comparison run [40289913764](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40289913764), specifically `target-caller-aa_path_iterate.txt`, `target-caller-ripr_path_fill.txt`, `target-caller-ripr_stroke_iterate.txt`, and `target-caller-RIPRenderRectangles.txt` in the diagnostics artifact. It is a static instruction/dataflow review only. No binary was executed and no crafted input or device was used.

## New observation: one caller appears to clamp transformed coordinates

In `_aa_path_iterate`, the call-site sequence around `0x184694ee4–0x184694f08` is:

- `fmul v1.2d, v3.2d, v1.d[0]`
- `fmla v1.2d, v2.2d, v0.d[0]`
- `fadd v0.2d, v4.2d, v1.2d`
- load scalar bounds into both lanes of `v1` and `v2`
- `fcmgt v3.2d, v1.2d, v0.2d`
- `fcmgt v4.2d, v0.2d, v2.2d`
- `bit v0.16b, v2.16b, v4.16b`
- `bit v0.16b, v1.16b, v3.16b`
- optionally call `_CGFontAutohintTransformApply`
- convert `d0,d1` to floats and branch to `_aa_lineto`

The compare-and-select sequence is consistent with clamping the transformed coordinate lanes to a lower and upper bound before the call. This materially weakens any claim that this particular caller necessarily forwards extreme coordinates unchanged. The saved disassembly alone does not identify the bound values' provenance, establish their ordering, or prove the clamp is applied to every route into `_aa_lineto`; the optional autohint transform also occurs after the select and needs its own range analysis.

## Other observed callers do not show the same clamp in the captured call-site window

- `_ripr_path_fill` loads doubles from the path-element pointer, converts them to floats, then branches to `_aa_lineto` at `0x1843171b0`. Its captured function is a path-element dispatcher; no range clamp is visible in that short function.
- `_ripr_stroke_iterate` loads a pair of doubles from `[x2]`, converts to floats, then branches to `_aa_lineto` at `0x18433d95c`. The bounded function listing does not show a coordinate range clamp before this branch.
- `_RIPRenderRectangles` computes transformed rectangle corners using floating-point multiply-adds, converts to floats, and calls `_aa_lineto` at `0x1842fc91c`, `0x1842fc934`, and `0x1842fc950`. No explicit range clamp is visible in the captured corner-generation loop; upstream rectangle validation and the state passed to the antialiasing routines remain untraced.

Absence from these captured windows is not proof that no upstream validation exists.

## Updated assessment

1. The target/reference conversion mismatch remains real in the compared binaries: the target has vector FP64-to-signed-64 conversion followed by low-32-bit narrowing, while the reference contains scalar range/NaN handling and 32-bit conversion after clamping.
2. A plausible clamp sequence is visible in one internal path caller, so reachability must be evaluated separately for each call route rather than generalized from `_aa_lineto` alone.
3. The static evidence still does not prove attacker-controlled out-of-range values reach the conversion, cause an invalid edge denominator or allocation, or produce an out-of-bounds access.
4. Patch attribution to CVE-2026-86950 remains unresolved because the comparison is iOS 26.6.1 versus 26.7.1, not 26.7 versus 26.7.1.

## Next bounded validation

- Resolve the source and exact values of the two bounds used by `_aa_path_iterate`, then inspect whether `_CGFontAutohintTransformApply` can move coordinates outside them.
- Trace the input/state setup for `_ripr_path_fill`, `_ripr_stroke_iterate`, and `_RIPRenderRectangles` to determine whether they inherit equivalent bounds.
- Preserve the per-caller uncertainty until a complete dataflow and guard analysis is available.
