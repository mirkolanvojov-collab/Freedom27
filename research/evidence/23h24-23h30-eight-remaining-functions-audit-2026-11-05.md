# 23H24 → 23H30: eight changed functions outside the CFG audit (2026-11-05)

## Method
Read `coregraphics-26-7-function-diff.json` from successful run [41905970197](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197), artifact [13362383025](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362383025). Compared the reported normalized instruction counts and counted literal `fcvtzs` mnemonics in each function's saved `target_instructions` and `fixed_instructions` arrays. These are static textual counts, not full semantic equivalence checks.

| Function | 23H24 instructions | 23H30 instructions | `fcvtzs` target / fixed |
|---|---:|---:|---:|
| `_aa_cache_render` | 664 | 664 | 0 / 0 |
| `_aa_close` | 69 | 66 | 0 / 0 |
| `_aa_create` | 57 | 57 | 0 / 0 |
| `_aa_free_edges` | 30 | 30 | 0 / 0 |
| `_aa_line_render` | 217 | 217 | 1 / 1 |
| `_aa_line_render_shape` | 509 | 509 | 1 / 1 |
| `_aa_render` | 1086 | 1086 | 0 / 0 |
| `_aa_render_shape` | 838 | 838 | 0 / 0 |

All eight have nonidentical normalized instruction hashes in the comparison report. Seven retain equal instruction counts; `_aa_close` has three fewer instructions in 23H30. Both `_aa_line_render` and `_aa_line_render_shape` contain a literal `fcvtzs` on each side, but are not covered by the seven-function CFG guard audit.

## Interpretation
These observations do **not** establish that the differences are merely layout changes or security fixes. A matching instruction count can conceal substantial behavioral changes; `fcvtzs` presence alone does not establish vulnerable coordinate conversion. These two line-render functions are candidates for a separate guard/dataflow review. Other changed functions should be classified by normalized instruction-level edits and callsite changes before attribution.

No execution, exploit, or device modification occurred. Preserve PR #37 as draft.
