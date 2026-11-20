# Static caller-context review for _aa_lineto — 2026-10-26

## Evidence source

This review uses the preserved caller disassembly in the CoreGraphics diagnostics artifact from [comparison run 40289913764](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40289913764). It is a static call-site review; no binary or crafted document was executed.

## Direct call-site observations

- `_ripr_path_fill` at target address `0x1843171b0` branches to `_aa_lineto` after loading a pair of doubles and converting them to single-precision floats with `fcvt s0, d0` and `fcvt s1, d1`.
- `_ripr_stroke_iterate` at `0x18433d95c` similarly loads a pair of doubles, converts them to floats, and branches to `_aa_lineto`.
- `_RIPRenderRectangles` calls `_aa_lineto` at `0x1842fc91c`, `0x1842fc934`, and `0x1842fc950`; each shown call site computes coordinates with floating-point fused multiply-add instructions and converts them to single-precision values before the call.
- `_aa_path_iterate` has a branch to `_aa_lineto` at `0x184694f4c`. The saved bounded disassembly does not by itself identify the public API entry that reaches this specific branch.
- A saved local call-site window around `0x1846952e4` also branches to `_aa_lineto`, but a 16-instruction window is not enough to reconstruct its complete caller or input validation.

## Interpretation

These call sites support that `_aa_lineto` is used by multiple rendering paths, including path fill, stroke iteration, and rectangle rendering. They do **not** establish that untrusted coordinates reach the vector conversion unchanged: callers perform conversions and transforms, and the full function prologues, state setup, clipping predicates, and input-source chain must be traced before drawing a reachability conclusion.

The key unresolved dataflow question is whether the double-precision vector values converted inside `_aa_lineto` can exceed the reference clamp bounds on a path reachable from an externally supplied path, and which guards dominate that path.

## Next validation

1. Recover complete bounded disassembly around each call site and its preceding branch predicates.
2. Trace the coordinate registers and state pointer into `_aa_lineto`, including clipping and transforms.
3. Link the rendering paths to public CoreGraphics path APIs using symbols and call edges supported by the artifact; do not infer a complete call graph from isolated xrefs.
4. Compare iOS 26.7 with 26.7.1 to distinguish the candidate patch from unrelated changes between 26.6.1 and 26.7.1.
