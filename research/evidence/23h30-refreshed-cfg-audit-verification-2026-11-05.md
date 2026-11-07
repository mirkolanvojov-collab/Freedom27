# Refreshed 23H30 CFG audit verification (2026-11-05)

**Provenance:** GitHub Actions comparison run [41960951965](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41960951965) completed successfully, artifact `13386158235` (`coregraphics-build-comparison`). Inspected `coregraphics-26-7-conversion-cfg-audit.json` and `coregraphics-conversion-cfg-audit.json`; both contain 24 fixed-build conversion records and 11 fixed-build `cfg_nan_guard_cutset_coverage=false` records. These reports were generated after the diagnostic-only analyzer changes through commit `c456334`.

| Symbol | Fixed conversion | Source-matched branch separated by ADRP | Source-matched branch separated by STR | Adjacent pairs / accepted |
|---|---|---|---|---|
| `_aa_moveto` | `0x18433172c` | `0x1843316f8` | — | 1 / 1 |
| `_aa_lineto` | `0x184331db8` | `0x184331d54` | — | 3 / 3 |
| `_aa_clip_edge` | `0x184335474` | `0x18433579c` | — | 7 / 5 |
| `_aa_clip_edge` | `0x1843354c0` | `0x18433579c` | — | 7 / 5 |
| `_aa_clip_edge` | `0x1843357c0` | `0x18433579c` | — | 7 / 5 |
| `_aa_clipping` | `0x18433e538` | `0x18433e514` | — | 3 / 3 |
| `_aa_cubeto` | `0x184332278` | — | — | 1 / 0 |
| `_aa_cubeto` | `0x1843322c0` | — | `0x18433229c` | 1 / 0 |
| `_aa_quadto` | `0x18433b9e8` | — | — | 1 / 0 |
| `_aa_quadto` | `0x18433ba30` | — | `0x18433ba0c` | 1 / 0 |
| `_aa_rectat` | `0x1846bad80` | `0x1846bad5c` | — | 3 / 3 |

**Summary:** 7/11 cutset-negative conversions have at least one ADRP-separated source-match, 2/11 have an STR-separated source-match, and 2/11 have neither. The latter two are the first conversions in `_aa_cubeto` and `_aa_quadto`, which have adjacent self-compare branches already documented in the earlier instruction-path report. Thus every exception has at least one candidate pattern to investigate, but this is not a formal path-coverage claim.

**Critical caveat:** The current diagnostics scan the entire function; an ADRP-separated branch may occur after a conversion or on a path irrelevant to that conversion. The `_aa_clip_edge` branch `0x18433579c` is after all three listed conversions. Its inclusion illustrates that diagnostic matches must not be interpreted as preceding or protecting the conversion. The existing cutset coverage remains unchanged and conservative. Next: require address/path relevance and confirm NaN successor exclusion of the **same** conversion, plus NZCV provenance. No exploitability or jailbreak conclusion follows.
