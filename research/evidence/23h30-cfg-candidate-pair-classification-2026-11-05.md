# 23H30 CFG cutset exception: candidate-pair classification (2026-11-05)

Source: saved GitHub Actions artifact 13362383025, `coregraphics-26-7-function-diff.json` and `coregraphics-26-7-conversion-cfg-audit.json`; checked against analyzer branch-pair rule following fix `d4bf062`. No binaries executed.

Among 11 fixed-build conversion sites with `cfg_nan_guard_cutset_coverage=false`, seven have at least one accepted candidate NaN guard, while four have zero accepted candidates despite a recognized adjacent `fcmp d1,d1` / `b.vs` pair. No unresolved control transfers are reported in these seven functions. This does **not** imply complete CFG modeling or any exploitability.

| Symbol | Conversion address(es) | Adjacent candidate pair | Branch target | Accepted candidates |
|---|---|---|---|---|
| `_aa_cubeto` | `0x184332278`, `0x1843322c0` | `0x184332254 fcmp d1,d1`; `0x184332258 b.vs` | `0x184332334` | 0 |
| `_aa_quadto` | `0x18433b9e8`, `0x18433ba30` | `0x18433b9cc fcmp d1,d1`; `0x18433b9d0 b.vs` | `0x18433baac` | 0 |

At `_aa_cubeto:0x184332334`, the NaN branch target initializes `w8=0`, then branches to `0x184332288`; at `_aa_quadto:0x18433baac`, it initializes `w8=0`, then branches to `0x18433b9f8`. The analyzer rejects the candidate for both conversions in each function because the selected NaN successor still has a CFG path to the conversion (consistent with the stored zero-candidate reports). This may represent intentional reuse of a later conversion path, but the current analysis does not track whether the original NaN operand can reach that conversion unchanged.

For the other seven cutset-negative sites, accepted guard counts are: `_aa_moveto:0x18433172c` 1, `_aa_lineto:0x184331db8` 3, `_aa_clip_edge:0x184335474` 5, `0x1843354c0` 5, `0x1843357c0` 5, `_aa_clipping:0x18433e538` 3, and `_aa_rectat:0x1846bad80` 3. Their negative cutset coverage indicates entry-to-conversion reachability after candidate-node removal, not a proven NaN dataflow bypass.

Next: separately classify paths from NaN branch successors to each conversion, record whether the relevant source register is overwritten, and validate NZCV provenance. Until then, these are **structural-analysis exceptions**, not vulnerability confirmations.
