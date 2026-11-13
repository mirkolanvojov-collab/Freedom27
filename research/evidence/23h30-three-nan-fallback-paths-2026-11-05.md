# 23H30 three remaining NaN guard paths: instruction-level triage (2026-11-05)

Source: saved GitHub Actions artifact 13362383025, `coregraphics-26-7-function-diff.json`, fixed 23H30 addressed instruction records. This is an independent instruction-level check, **not** a canonical full CFG analyzer rerun.

All three sites previously classified as lacking earlier source-matched adjacent or store-separated pairs instead have `fcmp source,source` → `adrp` → `b.vs`. The intervening `adrp` computes a page-relative address and does not update NZCV. Their NaN-branch targets assign a zero integer fallback and branch beyond the relevant conversion:

| Function | Conversion | Comparison | NaN branch | NaN target and join |
|---|---|---|---|---|
| `_aa_moveto` | `0x18433172c fcvtzs w9,d0` | `0x1843316f0 fcmp d0,d0` | `0x1843316f8 b.vs` | `0x184331794 mov w9,#0`; `0x184331798 b 0x184331730` |
| `_aa_clipping` | `0x18433e538 fcvtzs w2,d4` | `0x18433e50c fcmp d4,d4` | `0x18433e514 b.vs` | `0x18433e620 mov w2,#0`; `0x18433e624 b 0x18433e540` |
| `_aa_rectat` | `0x1846bad80 fcvtzs w11,d2` | `0x1846bad54 fcmp d2,d2` | `0x1846bad5c b.vs` | `0x1846baea0 mov w11,#0`; `0x1846baea4 b 0x1846bad88` |

In each case, the observed branch-to-zero path skips the listed `fcvtzs` and rejoins after it. The earlier inventory missed this pattern because it recognized only adjacent comparisons or comparisons separated by `str`. The instruction ordering and destinations are evidence of a local NaN fallback, but are not a formal proof of complete path coverage, absence of flag clobbers on every path, or safety for all inputs. The `_aa_clipping` and `_aa_rectat` conversion sites also use `csel` after conversion; this warrants separate dataflow analysis.

**Recommended engineering follow-up:** extend diagnostic-only matching to a whitelist of one NZCV-preserving instruction (`adrp` or `str`) and record whether the branch's NaN successor can reach the *same* conversion. Keep the conservative `cfg_nan_guard_cutset_coverage` flag unchanged pending path-sensitive validation.

The full updated analyzer has not yet been rerun on this artifact. No device access, exploit, or jailbreak is implied.
