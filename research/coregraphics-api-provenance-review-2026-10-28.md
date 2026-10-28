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
