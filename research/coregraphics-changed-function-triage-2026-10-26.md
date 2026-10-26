# CoreGraphics changed-function triage from preserved run 169

**Date:** 2026-10-26  
**Artifact:** `coregraphics-function-diff.json` from [workflow run 40240737732](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40240737732)  
**Builds compared:** iOS 26.6.1 (23G83) versus iOS 26.7.1 (23H30)  
**Method:** read-only analysis of the saved normalized instruction streams.

## Scope and interpretation

The artifact contains 25 common `aa_*` symbols, all successfully compared, with 15 streams marked changed and zero disassembly failures. The public Calif patch analysis compares 26.7 to 26.7.1; this project's 26.6.1-to-26.7.1 comparison spans a wider interval and can include unrelated changes. Do not equate all 15 local differences with the CVE patch.

The “position mismatches” column counts unequal normalized instruction strings at the same array index over the shorter of the two streams. It is a quick triage metric, **not** an edit distance, semantic diff, or count of changed machine-code instructions; insertions and deletions shift subsequent indices. The saved JSON preserves full streams and should be used for detailed review.

## Changed-stream inventory

| Symbol | Target / fixed instructions | Position mismatches | Initial triage |
|---|---:|---:|---|
| `_aa_cache_render` | 664 / 664 | 9 | Same length; changes are primarily memory operands/immediates. Resolve data-layout/relocation effects before attributing a logic change. |
| `_aa_clip_edge` | 162 / 280 | 154 | Major control-flow and conversion changes; split clipping and non-clipping paths. |
| `_aa_clipping` | 120 / 178 | 69 | Context flag and clipping-state initialization candidate. |
| `_aa_close` | 69 / 66 | 49 | Length and stack-frame differences; trace end-of-path edge finalization. |
| `_aa_create` | 57 / 57 | 3 | Small number of memory-operand differences; likely requires address/layout resolution before semantic interpretation. |
| `_aa_cubeto` | 313 / 336 | 234 | Large stream changes; inspect coordinate conversions and propagation to edge insertion. |
| `_aa_free_edges` | 30 / 30 | 1 | Single memory-operand difference; low priority until its base object is resolved. |
| `_aa_line_render` | 217 / 217 | 1 | Single memory-operand difference; resolve data reference before treating as a behavior change. |
| `_aa_line_render_shape` | 509 / 509 | 7 | Small number of memory/immediate differences; compare data references and call targets. |
| `_aa_lineto` | 113 / 163 | 107 | Highest-priority coordinate-conversion candidate; vector conversion/narrowing differs from fixed-reference scalar guarded paths. |
| `_aa_moveto` | 86 / 122 | 16 | High-priority related conversion path; compare the actual conversion sites and guard branches. |
| `_aa_quadto` | 242 / 269 | 238 | Large stream changes; inspect coordinate conversion and edge propagation. |
| `_aa_rectat` | 164 / 221 | 129 | Large stream changes; inspect coordinate conversion and clipping behavior. |
| `_aa_render` | 1086 / 1086 | 6 | Same length; changes are largely memory/immediate operands, likely requiring data-layout resolution. |
| `_aa_render_shape` | 838 / 838 | 6 | Same length; memory-operand changes require section/data-reference context. |

## Corrections and confirmed invariants

- `_aa_cache_render` is **not** an identical normalized stream. Its artifact record has `instruction_stream_identical: false` and nine position-wise mismatches despite equal instruction counts. Earlier research-note wording that called it identical was corrected in commit `746c588` and the validation checklist was corrected in commit `349c8be`.
- `_aa_add_edges` has 138 instructions in each build and its normalized streams match. This does not rule out the documented signed-delta/bounds failure when upstream values differ.
- `_aa_path_iterate` has 221 instructions in each build and its normalized streams match. That alone does not establish identical runtime behavior for every caller or context.
- The fixed-reference constant verifier confirms the expected clamp constants at the audited section-relative locations, but constant identity alone does not establish reachability or effective guard coverage.

## Recommended order

1. Reconcile `_aa_lineto` and `_aa_moveto` conversion behavior with the public analysis at the instruction level.
2. Trace `_aa_cubeto`, `_aa_quadto`, and `_aa_rectat` coordinate values into edge insertion, retaining clipping/non-clipping distinctions.
3. Trace how `_aa_clipping` establishes context flags and determine which path reaches the conversion helper without clamping.
4. Inspect `_aa_cache_render` mismatches using surrounding raw instructions and data-reference provenance. Do not label the differences as only relocation noise without resolving them.
5. When possible, obtain a same-scope 26.7 versus 26.7.1 comparison to separate the CVE patch from intervening 26.6.1-to-26.7 changes.

## Evidence boundary

This triage is static, read-only, and does not execute CoreGraphics or construct a trigger. It supports prioritization, not a claim of exploitability, CVE attribution for each changed symbol, or code execution.
