# 23H30 source-matched store-separated branch diagnostics (2026-11-05)

Input: previously downloaded GitHub Actions artifact 13362383025, `coregraphics-26-7-function-diff.json` and `coregraphics-26-7-conversion-cfg-audit.json`. Applied the corrected source-register and one-intervening-`str` matching rule from analyzer commit `3f353f0` to the 11 fixed-build cutset-negative conversions. This is a targeted offline re-evaluation, **not** a full regenerated analyzer output.

| Symbol | Conversion | Conversion source | Matching branch after one store |
|---|---|---|---|
| `_aa_moveto` | `0x18433172c` | d0 | none |
| `_aa_lineto` | `0x184331db8` | d1 | none |
| `_aa_clip_edge` | `0x184335474` | d4 | none |
| `_aa_clip_edge` | `0x1843354c0` | d4 | none |
| `_aa_clip_edge` | `0x1843357c0` | d4 | none |
| `_aa_clipping` | `0x18433e538` | d4 | none |
| `_aa_cubeto` | `0x184332278` | d1 | none |
| `_aa_cubeto` | `0x1843322c0` | d0 | `0x18433229c` |
| `_aa_quadto` | `0x18433b9e8` | d1 | none |
| `_aa_quadto` | `0x18433ba30` | d0 | `0x18433ba0c` |
| `_aa_rectat` | `0x1846bad80` | d2 | none |

**Result:** exactly 2/11 sites have source-matched self-comparison / `str` / NaN branch triples. The other 9 do not match this narrow pattern; absence of a match is not evidence of a missing protection. In particular, the first conversions in `_aa_cubeto` and `_aa_quadto` use immediately adjacent NaN branches and are outside this new diagnostic's scope.

This analysis does not alter the previously computed cutset flags, prove NZCV/register dataflow for arbitrary paths, or establish exploitability. Follow-up: run the entire updated analyzer on the same comparison JSON and check output consistency, then investigate the seven other cutset-negative sites using path-specific provenance.
