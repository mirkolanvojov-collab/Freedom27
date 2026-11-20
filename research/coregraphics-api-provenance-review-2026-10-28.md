# CoreGraphics public-API provenance review — 2026-10-28

## Scope and provenance

This is a static review of the read-only disassembly artifacts produced by comparison workflow [40725977368](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40725977368) on branch `research/cve-source-reconciliation-2026-10-24`, commit `16927dda1480b8f23926f1f599532703177e1795`. The workflow completed successfully on 2026-10-28. Its test workflow [40725977461](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40725977461) also passed.

The workflow captured bounded disassembly for six public CoreGraphics API candidates in both target iOS 26.6.1 build 23G83 and reference iOS 26.7.1 build 23H30:
`_CGPathAddLineToPoint`, `_CGPathCreateWithData`, `_CGPathApply`, `_CGContextAddLineToPoint`, `_CGContextStrokePath`, and `_CGContextFillPath`. All twelve symbol-scoped disassembly commands reported success. This means disassembly was captured, not that each symbol was proven to reach `_aa_lineto`.

## Observations from candidate function bodies

### Direct path-point API

In both builds, `_CGPathAddLineToPoint` checks the path pointer, consults `_CGPathDisableTypeValidation`, and—when validation is enabled—checks the object type using `_CGPathGetTypeID`. Before dispatching to `CG::Path::add_line_to_point`, the visible path masks the sign bit from each double coordinate, compares the resulting bit patterns against the positive-infinity encoding, and branches to an error path for values at or above that threshold. It also calls `transform_is_valid` and rejects an invalid transform before the internal call.

This is evidence that the direct public line-to-point API has non-finite-coordinate and transform-validation gates in the captured path. It weakens any claim that arbitrary NaN/infinity values trivially pass through this specific API. It does not prove that every path-construction route applies the same checks, or that finite but extreme transformed coordinates are constrained to the fixed-reference clamp interval.

The target and reference bodies have the same instruction counts and the same apparent validation/control-flow sequence in this bounded capture. Absolute branch destinations and some image addresses differ, so raw textual equality is not used as a semantic equivalence proof.

### Serialized path decoding candidate

`_CGPathCreateWithData` is a candidate for tracing serialized path data, but the captured function is a decoder for several encoded object variants, not a simple untyped byte copy. The observed path obtains a data pointer and length through helper calls, rejects too-short input (including a minimum-length check against four bytes), validates encoded type tags, and performs repeated offset-plus-field-width comparisons against the available length before loading fields. In the shown multi-field branch, checks of the form `offset + 8 <= length`, `offset + 16 <= length`, and subsequent bounds checks precede the corresponding loads.

These checks are evidence of length-aware parsing on the observed branches. This pass did not fully audit every encoded variant, the helpers that return the byte pointer and length, integer-overflow behavior in every offset calculation, or whether decoded point values are checked for finiteness/range before they can reach rendering. Therefore this is not a finding of either a parser bug or complete parser safety.

### Context drawing and path application

`_CGContextAddLineToPoint` checks for a non-null context and a context type marker, examines the current path/current-point state, and branches to an error path when there is no current point; its normal branch forwards to `_CGPathAddLineToPoint`.

`_CGContextFillPath` and `_CGContextStrokePath` are small dispatch stubs that set the draw mode and branch to `_CGContextDrawPath`. Their presence identifies a next function to inspect, but these stubs alone do not show how path elements reach the rasterizer.

`_CGPathApply` validates the path object when type validation is enabled and forwards through the internal `CG::Path::apply` callback mechanism. The captured body does not establish that a caller-supplied callback is a rasterization callback, nor does it provide an end-to-end edge into `_aa_path_iterate`.

## Comparison results retained with the same workflow

- Primary comparison: target 23G83 versus fixed reference 23H30; 25 common `aa_*` symbols, 25 compared, 15 differing normalized instruction streams, zero disassembly failures.
- Direct patch-attribution comparison: 23H24 versus 23H30; the same 25-symbol scope completed, with 15 differing streams and zero disassembly failures.
- In both comparisons, `_aa_lineto` differs (113 target instructions versus 163 reference instructions); `_aa_path_iterate` is normalized-stream-identical (221 instructions); `_aa_add_edges` is identical (138 instructions); and `_aa_new_edge` is identical (37 instructions).
- The workflow log explicitly reports `caller_xref_status=deferred_experimental_shared_cache_scan`. It did not produce full shared-cache cross-reference results. Caller provenance is still unresolved.

## Assessment and next gate

The best-supported static conclusion is now narrower: a direct public line-to-point route contains non-finite coordinate and transform checks, while the serialized-data candidate contains visible length/offset checks on multiple decode branches. The current evidence does not establish whether all decoded coordinates inherit equivalent numeric constraints, whether finite extreme values can reach the differing `_aa_lineto` conversion on a renderable path, or whether any such path violates an allocation or write bound.

Next, inspect `_CGContextDrawPath`, the relevant `CG::Path::apply`/element callback implementations, and the point-decoding helper with the same-build address/section mapping. Establish a supported call/data-flow chain into the saved `_ripr_path_fill` or `_aa_path_iterate` call sites, and compare numeric checks on that exact path. Do not infer a call graph from symbol names alone.

The CVE-2026-86950 attribution remains unconfirmed at function level. No binary or crafted file was executed, no device was accessed or modified, and this review is not evidence of a reproduced out-of-bounds write or exploit.


## Draw-path safety gate and internal path mutation (workflow run 40730463450)

The expanded comparison workflow [40730463450](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40730463450) completed successfully on commit `1c5615160c6279504d8f325890b17af7138a185c`; the corresponding test workflow [40730463431](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40730463431) also passed.

The new bounded disassembly provides two concrete control-flow observations:

- In both target 23G83 and fixed 23H30, `_CGContextDrawPath` rejects a null context and validates a context type marker, checks whether the current path is empty, and then calls `_path_coordinates_are_safe` on the current path before proceeding to `_draw_path`. The return value controls whether drawing is skipped/cleaned up or continues. The helper is therefore a real pre-draw gate on this public context-drawing path, not merely a symbol inferred from its name.
- The captured internal `CG::Path::add_line_to_point` body clamps a pair of coordinates against stored bounds using SIMD greater-than comparisons and bit-select operations before reserving path storage and writing the point pair. This supports a bounded internal path-mutation route for the observed direct API implementation. It does not prove that serialized decoding, every other path-construction route, or rasterizer inputs obey the same invariant.

The draw-path dispatcher’s block setup and `_draw_path` call are visible, but this artifact does not include the body of `_path_coordinates_are_safe` or the block-invoke implementation. The `CG::Path::apply` implementation also uses an indirect block callback, so symbol presence alone does not establish a callback edge into `_ripr_path_fill` or `_aa_path_iterate`. Thus this run narrows the next audit to the safety helper and draw callback, but does not yet close the end-to-end data-flow question.

**Next capture added:** the workflow will now attempt bounded disassembly of `_path_coordinates_are_safe`, `_draw_path`, and `___CGContextDrawPath_block_invoke` in both builds. Successful capture will be treated as evidence only; call relationships and guard semantics must be read from the instructions. The caller-xref scan remains deferred, as recorded in the workflow log.

**Assessment:** a concrete pre-draw safety gate exists in both versions, and direct path-point insertion has bounds-selection logic. The unresolved questions are what coordinate classes the helper accepts, whether decoded points pass through equivalent validation, and which callback path feeds the changed rasterization conversion. No binary or crafted file was executed, and no device was accessed or modified.


## Safety-helper and callback captures (workflow run 40740516479)

The updated read-only workflow [40740516479](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40740516479) completed successfully on commit `a040f0d807c5acfa115866dca1101a6d8c86012c`; the associated test workflow [40740517208](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40740517208) passed. The diagnostic artifact now contains bounded disassembly for `_path_coordinates_are_safe`, `_draw_path`, `___CGContextDrawPath_block_invoke`, both `___draw_path_block_invoke` callbacks, and the adaptive/automatic context draw-path functions in both builds. The internal add-line C++ symbol candidate was unavailable under the exact mangled spelling used by the capture loop; that individual capture needs its symbol spelling corrected or its alternate symbol name resolved.

### What the safety helper checks

In both 23G83 and 23H30, `_path_coordinates_are_safe` calls `_CGPathGetBoundingBox`, takes absolute values of the returned rectangle's origin coordinates, compares them with a loaded threshold, rejects negative width/height, checks width/height against the same threshold, then checks the absolute values of the two far-edge sums. The helper returns a boolean-like result. The target and fixed bodies have the same observed instruction-level control-flow structure, with relocated addresses and different constant-pool locations. This is a real bounding-box gate in both builds, but this comparison does not show a new guard added to this helper in 23H30.

A numeric caveat remains: the observed floating-point branches use ordered-condition tests such as `b.gt` and `b.mi`, rather than an explicit unordered/NaN rejection branch. On ARM64, an unordered `FCMP` does not satisfy those conditions. The final `fmaxnm` ignores one NaN operand when the other operand is numeric, so the instruction sequence alone does not prove that every rectangle containing a NaN is rejected. This is a static semantic observation, not a demonstrated reachable bypass: the behavior of `_CGPathGetBoundingBox`, path invariants, and all construction routes must be established before concluding that a NaN rectangle can reach this helper.

### Callback/data-flow status

`_draw_path` calls `_CGPathApplyWithBlock2` with a block whose implementation is captured as `___draw_path_block_invoke`; a second callback, `___draw_path_block_invoke_2`, handles a path-element case that reads a point pair and appends it to temporary path storage, with batching into `_CGPathAddLines` once the stored point count reaches its threshold. The corresponding target and fixed callback bodies have highly similar visible control flow. These captures strengthen the evidence that draw-path callback logic iterates and copies path elements, but do not by themselves prove the callback ultimately reaches `_ripr_path_fill` or the differing `_aa_lineto` conversion.

The new artifact confirms successful disassembly for the safety helper and callback candidates in both builds. Shared-cache cross-reference analysis remains deferred (`caller_xref_status=deferred_experimental_shared_cache_scan`), so the end-to-end caller chain remains unresolved. The comparison and tests passing validate the research workflow, not a vulnerability.

### Next technical gate

1. Resolve the correct mangled symbol (or alternate symbol-table entry) for `CG::Path::add_line_to_point` and capture it in both builds.
2. Trace the captured callback into the context draw-path backend and establish whether it reaches `_ripr_path_fill` / `_aa_path_iterate`, using bounded caller/xref analysis rather than symbol-name inference.
3. Verify how `_CGPathGetBoundingBox` handles non-finite coordinates and whether all decoded/constructed points are constrained before this gate.

No binaries or crafted inputs were executed, no device was accessed or modified, and CVE-2026-86950 remains unconfirmed by this static review.


## Corrected internal add-line capture verified (workflow run 40750705815)

The corrected workflow run [40750705815](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40750705815) completed successfully on commit `9109310453cafc33ec58fb3abb770472d7dbb953`; the associated test workflow [40750706065](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40750706065) also passed. The diagnostic artifact reports successful disassembly of the corrected `__ZN2CG4Path17add_line_to_pointERK7CGPointPK17CGAffineTransform` symbol in both target 23G83 and fixed 23H30. This resolves the prior symbol-spelling/capture blocker.

### Comparison of the captured internal method

Both captured bodies are 3,459 characters in the diagnostic text and show the same instruction sequence after accounting for relocated addresses. The method optionally applies an affine transform to the input point, stores the point temporarily, handles path storage modes/capacity, uses SIMD greater-than comparisons and bit-selects against bounds stored in the path object, reserves storage, and writes the point pair. The target and fixed captures show no obvious new clamp/control-flow guard in this method in 23H30.

This finding narrows the patch-localization lead: the visible internal add-line method does not, by itself, explain the changed `_aa_lineto` stream. It does not establish that all construction routes share this method or that every point reaching rasterization has these bounds. In particular, the current artifact does not prove the serialized decoder's points pass through this exact method, nor does it establish the callback-to-rasterizer edge.

### Run verification details and remaining limits

- The comparison job and all listed steps completed successfully, including extraction of target 23G83, fixed 23H30, and intermediate 23H24 caches; primary and direct 23H24-to-23H30 comparisons; and diagnostic/evidence artifact upload.
- The comparison still reports 25 common `aa_*` symbols, 15 normalized instruction streams differing, and zero disassembly failures. The fixed-reference constant validation still reports both expected clamp constants matching.
- All 18 API/helper/callback candidate disassembly attempts in each build report success in the workflow log, including the corrected internal add-line method.
- `caller_xref_status=deferred_experimental_shared_cache_scan` remains in the log. End-to-end callback/caller provenance is still unresolved.

**Assessment:** the corrected symbol-capture blocker is fixed and verified. The static evidence still does not confirm CVE-2026-86950 or demonstrate a reachable out-of-bounds write. The next research gate is to establish the actual draw-callback-to-rasterizer path and reconcile the coordinate invariants on that path. No binary or crafted input was executed, and no device was accessed or modified.
