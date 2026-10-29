# CoreGraphics render-dispatch follow-up — 2026-10-28

## Verified comparison results

Workflow [40755743262](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40755743262) completed successfully after its retry. The earlier attempt failed during artifact upload; the retry uploaded both output bundles. The paired tests [40755743341](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40755743341) passed.

- iOS 26.6.1 build 23G83 versus iOS 26.7.1 build 23H30: 25 common `aa_*` symbols compared, 15 normalized streams differ, zero disassembly failures.
- iOS 26.7 build 23H24 versus 23H30: 25 common symbols compared, 15 normalized streams differ, zero disassembly failures.
- The two expected clamp constants in the fixed reference matched.
- Bounded disassembly succeeded for the listed public path APIs, helpers, callbacks, decoders, and internal add-line method in both builds.

Artifacts: [comparison JSON bundle](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40755743262/artifacts/12851476233) · [diagnostic disassembly bundle](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40755743262/artifacts/12850682594).

## Observed control-flow edges

The captured `_CGContextDrawPath` body calls `_path_coordinates_are_safe` and, on the accepted branch, `_draw_path`. The captured `_draw_path` body calls `_CGPathApplyWithBlock2` to process path elements.

Separately, the captured `_ripc_DrawPath` body calls `_RIPRenderPath` in two render-mode branches. The captured `_ripr_path_fill` body branches to `_aa_lineto`, `_aa_quadto`, `_aa_cubeto`, `_aa_moveto`, and `_aa_close` for path-element cases. These observations establish direct branches in the captured function bodies. They do not yet establish which concrete renderer implementation is selected by `_RIPRenderPath` for the path being reviewed.

The workflow log continues to mark `caller_xref_status=deferred_experimental_shared_cache_scan`; a full shared-cache reference scan is still outstanding.

## Next capture

The comparison workflow now includes bounded captures for `_RIPRenderPath` and `_ripc_Render` in both builds. The purpose is to inspect the intermediate renderer dispatch and identify which edges are direct versus indirect. Symbol capture alone does not establish runtime behavior.
