# 23H30 cutset-negative sites: source-register adjacent-pair inventory (2026-11-05)

Input: saved GitHub Actions artifact `13362383025`, files `coregraphics-26-7-function-diff.json` and `coregraphics-26-7-conversion-cfg-audit.json`. Independent read-only inventory, not a full rerun of the updated analyzer.

For each of the 11 fixed-build conversions whose saved audit has `cfg_nan_guard_cutset_coverage=false`, match `fcvtzs wN, dM` source register against an immediately adjacent `fcmp dM,dM` followed by `b.vs` or `b.vc`, restricting to branch instruction addresses **earlier** than the conversion address.

| Function | Conversion | Earlier source-matched adjacent NaN branch addresses |
|---|---|---|
| `_aa_moveto` | `0x18433172c` | none |
| `_aa_lineto` | `0x184331db8` | `0x184331d24` |
| `_aa_clip_edge` | `0x184335474` | `0x184335450` |
| `_aa_clip_edge` | `0x1843354c0` | `0x184335450`, `0x184335490` |
| `_aa_clip_edge` | `0x1843357c0` | `0x184335450`, `0x184335490`, `0x1843355ec`, `0x184335644` |
| `_aa_clipping` | `0x18433e538` | none |
| `_aa_cubeto` | `0x184332278` | `0x184332258` |
| `_aa_cubeto` | `0x1843322c0` | none (store-separated match `0x18433229c`) |
| `_aa_quadto` | `0x18433b9e8` | `0x18433b9d0` |
| `_aa_quadto` | `0x18433ba30` | none (store-separated match `0x18433ba0c`) |
| `_aa_rectat` | `0x1846bad80` | none |

**Interpretation:** Six of 11 have at least one earlier source-matched adjacent pair, two additional sites have earlier source-matched store-separated branches, and three have neither pattern in this narrow inventory (`_aa_moveto`, `_aa_clipping`, `_aa_rectat`). These are *lexical/address-order* observations only; they do not establish dominance, CFG reachability, NZCV provenance, or whether the guarded value is the value eventually converted. A matching branch can be on a path irrelevant to the conversion. Conversely, missing patterns do not establish missing protection.

The full updated analyzer must still be rerun on the saved function-diff JSON for a canonical refreshed report. Do not alter existing cutset coverage based on this inventory alone.
