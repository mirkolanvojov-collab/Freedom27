# 23H24-to-23H30 changed-function instruction-count crosscheck (2026-11-05)

Re-read the original `coregraphics-26-7-function-diff.json` from [run 41905970197, artifact 13362383025](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362383025). The table below reports the stored normalized instruction-array lengths; it is not a semantic diff.

| Changed function | 23H24 | 23H30 | Difference |
|---|---:|---:|---:|
| `_aa_cache_render` | 664 | 664 | 0 |
| `_aa_clip_edge` | 162 | 280 | +118 |
| `_aa_clipping` | 120 | 178 | +58 |
| `_aa_close` | 69 | 66 | -3 |
| `_aa_create` | 57 | 57 | 0 |
| `_aa_cubeto` | 313 | 336 | +23 |
| `_aa_free_edges` | 30 | 30 | 0 |
| `_aa_line_render` | 217 | 217 | 0 |
| `_aa_line_render_shape` | 509 | 509 | 0 |
| `_aa_lineto` | 113 | 163 | +50 |
| `_aa_moveto` | 86 | 122 | +36 |
| `_aa_quadto` | 242 | 269 | +27 |
| `_aa_rectat` | 164 | 221 | +57 |
| `_aa_render` | 1086 | 1086 | 0 |
| `_aa_render_shape` | 838 | 838 | 0 |

The large positive deltas in six of the seven CFG-audited functions provide independent prioritization for examining added clamp/guard logic. Equal instruction counts in other functions do not imply semantic identity. The exact meaning of line-render changed load/address operands remains unresolved because the saved function-diff JSON does not include fully resolved constant-pool referents; a relocation-sensitive site record alone is insufficient to establish the referenced data value. Do not label those differences as harmless or patch-related without referent resolution.

The previously documented CFG cutset negatives remain analysis limitations, not confirmed unguarded conversions. No dynamic testing or jailbreak demonstration was performed.
