# Fixed-build CFG cutset negatives: evidence classification (2026-11-05)

Source: direct inspection of `coregraphics-26-7-conversion-cfg-audit.json` from [run 41905970197, artifact 13362383025](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362383025).

The fixed-side audit reports 24 conversion sites in seven functions. Of these, 11 have `cfg_nan_guard_cutset_coverage=false`. **All 11 nevertheless report at least one dominating self-compare, at least one dominating NaN branch, and two dominating clamp loads.** This makes it incorrect to equate a cutset-negative flag with an absent structural guard.

| Function | Conversion address | Candidate CFG guard branches |
|---|---|---:|
| `_aa_moveto` | `0x18433172c` | 1 |
| `_aa_lineto` | `0x184331db8` | 3 |
| `_aa_clip_edge` | `0x184335474` | 5 |
| `_aa_clip_edge` | `0x1843354c0` | 5 |
| `_aa_clip_edge` | `0x1843357c0` | 5 |
| `_aa_clipping` | `0x18433e538` | 3 |
| `_aa_cubeto` | `0x184332278` | 0 |
| `_aa_cubeto` | `0x1843322c0` | 0 |
| `_aa_quadto` | `0x18433b9e8` | 0 |
| `_aa_quadto` | `0x18433ba30` | 0 |
| `_aa_rectat` | `0x1846bad80` | 3 |

## Classification

- **Seven cutset-negative sites with candidate branches:** the algorithm records possible CFG guards but cannot establish its particular cutset criterion. Loop-back paths, branch semantics, and register/flag provenance require examination before interpreting this result.
- **Four cutset-negative sites with zero candidate branches:** the audit still records dominating self-comparisons, NaN branches, and clamp loads. This mismatch between candidate enumeration and structural dominator fields warrants inspecting the candidate-selection logic, not declaring an unguarded conversion.

The audit itself says branch structure comes from disassembler text and direct labels, structural dominance does not prove operand identity, and its cutset test does not prove flag/register dataflow or sentinel correctness. A false flag is not proof of a missing guard; a true flag is not proof of safety.

## Next verifiable tasks

1. Inspect the cutset candidate-selection implementation and explain why `_aa_cubeto` and `_aa_quadto` have zero listed candidates despite dominating branch records.
2. Determine whether the seven other negative sites are reachable through loop-back paths after candidate-node removal.
3. Only after these checks, consider a more precise value-sensitive CFG test. Do not infer exploitability or device compromise from these static metrics.

No binary was executed, and no device was modified. Keep PR #37 draft.
