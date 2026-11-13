# Direct 23H24 → 23H30 CoreGraphics JSON audit (2026-11-05)

## Artifact and identity
Downloaded and inspected [comparison artifact 13362383025](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362383025) from successful [run 41905970197](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197).

`coregraphics-26-7-patch-comparison.json` identifies:
- 23H24 / iPhone17,4 CoreGraphics: 9,294,928 bytes, SHA-256 `c2148f5b9ddfd03ba2989f4410ef5421c55814a5f2d2891c1b548d09234288ee`, Mach-O UUID `4C04F0CB-7A29-3BE8-9B93-4E86FE0DEC4E`.
- 23H30 / iPhone17,4 CoreGraphics: 9,294,928 bytes, SHA-256 `c5ebb5405dcd271fcab53cd4de0f59b9106672f86f790b7842a4702838275285`, Mach-O UUID `4D24CA95-6D98-3968-BA43-D63976262D3D`.
- `byte_identical: false`.

## Function comparison
`coregraphics-26-7-function-diff.json` (schema 3) reports 25 common `aa_*` symbols, 25 successfully compared, **15 changed**, zero disassembly failures. Changed symbols:

`_aa_cache_render`, `_aa_clip_edge`, `_aa_clipping`, `_aa_close`, `_aa_create`, `_aa_cubeto`, `_aa_free_edges`, `_aa_line_render`, `_aa_line_render_shape`, `_aa_lineto`, `_aa_moveto`, `_aa_quadto`, `_aa_rectat`, `_aa_render`, `_aa_render_shape`.

**Do not confuse 15 changed normalized function streams with 15 independent security fixes.** Relocations, layout changes, and unrelated modifications may contribute.

## Fixed constants
`coregraphics-26-7-constant-validation.json` reports 36 references, 2 unique constants checked, `all_constants_match_expected: true`: -1073737729.0 and +1073737729.0 in the fixed binary.

## Static control-flow audit
`coregraphics-26-7-conversion-cfg-audit.json` contains 14 analyzed function-side records (7 symbols × 2 builds): `_aa_clip_edge`, `_aa_clipping`, `_aa_cubeto`, `_aa_lineto`, `_aa_moveto`, `_aa_quadto`, `_aa_rectat`. There are zero unresolved control transfers reported.

- 23H24 target: 21 conversion records; 0 with `structural_nan_guard_in_dominators`, 0 with `structural_clamp_reference_in_dominators`, 0 with `cfg_nan_guard_cutset_coverage`.
- 23H30 fixed: 24 conversion records; 22 with `structural_nan_guard_in_dominators`, 24 with `structural_clamp_reference_in_dominators`, 13 with `cfg_nan_guard_cutset_coverage`.

These are distinct structural metrics, **not** a proof that all paths are guarded. In particular, 13/24 CFG cutset-coverage flags and 22/24 structural NaN-dominator flags do not establish complete NaN handling. Review the exceptions and the audit's documented limitations before concluding comprehensive coverage.

## Interpretation
The fixed build's clamp constants and conversion-site structural differences are consistent with [Calif's public root-cause analysis](https://calif.io/research/the-great-glyph-grift) for CVE-2026-86950. Static analysis does not establish exploitability, runtime reachability, or an untethered jailbreak. No exploit was executed and no device was modified.

## Follow-up
1. Audit the two fixed-side conversion records lacking structural NaN dominators and the 11 lacking CFG cutset coverage; distinguish analysis conservatism from a genuine guard gap.
2. Inspect the eight other changed functions for layout-only changes vs relevant code changes.
3. Keep PR #37 in draft until claims are fully grounded.
