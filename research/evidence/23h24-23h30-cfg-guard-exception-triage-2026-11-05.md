# 23H24-to-23H30 CFG guard exceptions — record-level triage (2026-11-05)

Source: `coregraphics-26-7-conversion-cfg-audit.json` in [artifact 13362383025](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362383025), from successful run [41905970197](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197).

## Exact exception records

Of 24 conversion sites in the 23H30 (fixed) binary across seven audited `aa_*` functions, **24/24** have structural clamp references in dominators, **22/24** have structural NaN-guard dominators, and **13/24** have CFG NaN-guard cutset coverage.

The two sites with `structural_nan_guard_in_dominators=false` are:
- `_aa_lineto` at `0x184331e04`, `fcvtzs w8, d0`: `cfg_nan_guard_cutset_coverage=true`; `structural_clamp_reference_in_dominators=true`.
- `_aa_clip_edge` at `0x184335678`, `fcvtzs w10, d4`: `cfg_nan_guard_cutset_coverage=true`; `structural_clamp_reference_in_dominators=true`.

The 11 sites with `cfg_nan_guard_cutset_coverage=false` are:
- `_aa_moveto`: `0x18433172c`
- `_aa_lineto`: `0x184331db8`
- `_aa_clip_edge`: `0x184335474`, `0x1843354c0`, `0x1843357c0`
- `_aa_clipping`: `0x18433e538`
- `_aa_cubeto`: `0x184332278`, `0x1843322c0`
- `_aa_quadto`: `0x18433b9e8`, `0x18433ba30`
- `_aa_rectat`: `0x1846bad80`

All 11 cutset-negative sites nevertheless have `structural_nan_guard_in_dominators=true` and `structural_clamp_reference_in_dominators=true`.

## Interpretation and limits

These two metrics are **not interchangeable**. A structural dominator flag does not prove that the compared register value equals the value being converted; a cutset-coverage flag does not prove correct dataflow or sentinel semantics. The report explicitly warns that loop-back edges can make a negative cutset result inconclusive, and that even a positive result is not proof of safety. No full register/flag dataflow, alias analysis, or symbolic execution was performed. No binary was executed.

The observed fixed-side clamp pattern is consistent with [Calif's published research](https://calif.io/research/the-great-glyph-grift) describing saturation and NaN handling in the fixed-point coordinate conversion. **No unpatched conversion or new vulnerability is established by these exception flags.**

## Research next steps
1. Independently validate dataflow and branch semantics for these exception sites using the saved disassembly evidence; distinguish loops from genuinely unguarded paths.
2. Crosscheck the remaining eight changed functions outside the seven-function CFG audit for patch relevance.
3. Keep vulnerability attribution and exploitability claims on evidence hold; PR #37 remains draft.
