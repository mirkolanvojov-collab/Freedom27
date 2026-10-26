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
| `_aa_cache_render` | 664 / 664 | 9 | Same length; all nine position mismatches need operand/data-layout reconciliation before attributing a logic change. |
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
- `_aa_new_edge` is present in the comparison artifact with 37 instructions in each build and matching normalized instruction hashes. Its stream is available only as a hash/count in this artifact, so this record alone cannot be used to audit its allocation-size or write-width details.
- `_aa_path_iterate` has 221 instructions in each build and its normalized streams match. That alone does not establish identical runtime behavior for every caller or context.
- The fixed-reference constant verifier confirms the expected clamp constants at the audited section-relative locations, but constant identity alone does not establish reachability or effective guard coverage.

## Detailed `_aa_cache_render` mismatch triage

The preserved artifact records the following nine position-wise differences (instruction indices are zero-based in the normalized arrays):

| Index | Target instruction | Fixed-reference instruction | Initial interpretation |
|---:|---|---|---|
| 11 | `ldr x8, [x8, #0xc30]` | `ldr x8, [x8, #0xc58]` | Loads through an address outside the artifact's listed Mach-O sections; likely requires symbol/cache metadata to resolve. Do not assume equivalent. |
| 53, 79 | `add x17, x17, #0xfe8` | `add x17, x17, #0x118` | Followed by `ldr x16, [x17]` and `blraa x16, x17`; indirect-call dispatch slot differs. Determine resolved target and pointer-authentication context before judging behavior. |
| 122 | `ldr q1, [x8, #0x740]` | `ldr q1, [x8, #0xd00]` | The artifact maps both derived references to `__TEXT,__const` section offset `0x5080`; that is evidence for a likely same section-relative constant, but confirm the section bytes/relocation before asserting equivalence. |
| 247, 279 | `add x23, x23, #0x591` / `#0x57b` | `add x23, x23, #0xb51` / `#0xb3b` | Relative addresses into a different mapped region; investigate the table/object layout. |
| 249, 281 | `add x26, x26, #0x550` | `add x26, x26, #0xb10` | Same repeated base-relative target pattern as above; likely data-layout sensitive, not enough evidence to classify as harmless. |
| 633 | `ldr x9, [x9, #0xc30]` | `ldr x9, [x9, #0xc58]` | Repeats the earlier out-of-listed-sections load and should be resolved together with index 11. |

This narrows the next check: resolve the two indirect-call slots and the two repeated `0xc30`/`0xc58` loads against the exact shared-cache metadata, then compare the bytes behind the `__const` reference. Until that is done, the safest conclusion is **same function length, nine normalized differences of unresolved semantic significance**—not “relocation-only” and not “changed allocation logic.”

## Recommended order

1. Reconcile `_aa_lineto` and `_aa_moveto` conversion behavior with the public analysis at the instruction level.
2. Trace `_aa_cubeto`, `_aa_quadto`, and `_aa_rectat` coordinate values into edge insertion, retaining clipping/non-clipping distinctions.
3. Trace how `_aa_clipping` establishes context flags and determine which path reaches the conversion helper without clamping.
4. Inspect `_aa_cache_render` mismatches using surrounding raw instructions and data-reference provenance. Do not label the differences as only relocation noise without resolving them.
5. When possible, obtain a same-scope 26.7 versus 26.7.1 comparison to separate the CVE patch from intervening 26.6.1-to-26.7 changes.

## Evidence boundary

This triage is static, read-only, and does not execute CoreGraphics or construct a trigger. It supports prioritization, not a claim of exploitability, CVE attribution for each changed symbol, or code execution.
