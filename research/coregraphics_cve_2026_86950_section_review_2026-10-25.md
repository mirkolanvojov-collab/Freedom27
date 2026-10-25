# CoreGraphics / CVE-2026-86950 — section-resolution review (2026-10-25)

## Scope and provenance

This note records the read-only comparison produced by GitHub Actions workflow run [40195214425](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40195214425), on merge commit `6a0c22f131031b73a882a5234fb4d65aa827ca78`. The section-resolution annotations were added by PR #49.

- Target: iPhone17,4 / iOS 26.6.1 build 23G83
- Fixed reference: iPhone17,4 / iOS 26.7.1 build 23H30
- Target CoreGraphics SHA-256: `0dc5ef74a54e7040857af5cafe796fa647f6dd552b4688fece7d5d84d2fb08ba`
- Fixed-reference CoreGraphics SHA-256: `ce59778ac827c624d005a8c0c96fba62a50d8a366b490bfb284a703d38967617`
- Both files are 9,294,920 bytes; their Mach-O UUIDs differ.
- Comparison mode: read-only binary metadata and symbol-scoped disassembly. No exploit was run and no device was accessed or modified.

## Automated result

The workflow completed successfully. The function-diff artifact reports:

- 25 target `aa_*` symbols and 25 fixed-reference `aa_*` symbols.
- 25 common symbols; all 25 were successfully compared.
- 15 normalized instruction streams differ.
- The changed set is `_aa_cache_render`, `_aa_clip_edge`, `_aa_clipping`, `_aa_close`, `_aa_create`, `_aa_cubeto`, `_aa_free_edges`, `_aa_line_render`, `_aa_line_render_shape`, `_aa_lineto`, `_aa_moveto`, `_aa_quadto`, `_aa_rectat`, `_aa_render`, and `_aa_render_shape`.

Section-resolution annotations were present in the fresh artifact. Across derived references, the target side classified 13 addresses inside listed sections and 16 outside the listed section ranges; the fixed-reference side classified 51 inside and 16 outside. These totals arise from different numbers of derived references in the two disassemblies (29 versus 67), so they must not be read as a direct measure of vulnerability severity or as a one-to-one comparison. “Outside listed sections” can mean an address in another image or an unresolved shared-cache mapping; it is not automatically an invalid address. An inside-section classification proves only range membership, not the meaning of the data or a vulnerability.

## Primary-source reconciliation

Apple's [iOS 26.7.1 and iPadOS 26.7.1 security-content advisory](https://support.apple.com/en-us/149226) identifies CVE-2026-86950 in CoreGraphics. Apple describes an out-of-bounds write addressed with improved bounds checking; processing a maliciously crafted file may lead to arbitrary code execution. Apple also states that it is aware of a report of exploitation in a highly sophisticated attack against specific targeted individuals on versions before iOS 27.

The target release, iOS 26.6.1, precedes the published fix in iOS 26.7.1, and the advisory's device scope includes iPhone 11 and later. This supports release-level applicability to the target profile. It does **not** establish that any particular changed `aa_*` function is the vulnerable code, identify the exact bounds check added by the fix, or demonstrate a reachable exploit path on build 23G83.

## Next evidence gates

1. Inspect changed functions' target-versus-fixed instruction windows and section-relative references, separating genuine control/data-flow changes from relocation and image-layout effects.
2. Verify all relevant section/load-command inputs and extraction provenance before interpreting an address classified outside listed sections.
3. Correlate any candidate bounds-check change with Apple's stated fix class and an independently sourced technical disclosure, if available.
4. Add only non-weaponized regression assertions for bounds and error handling; do not infer a reproduction from binary differences alone.

## Conclusion

The pipeline and section annotation pass. The result narrows static-review leads but does not yet attribute CVE-2026-86950 to a specific function in these binaries. Preserve that distinction in future reports.
