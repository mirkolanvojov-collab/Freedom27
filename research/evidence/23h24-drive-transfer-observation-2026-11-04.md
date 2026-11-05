# 23H24 Google Drive transfer — observed evidence (2026-11-04)

## Successful transport and digest observation

- GitHub Actions run: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41904780241
- Workflow: `.github/workflows/verify-23h24-drive.yml`
- Job: `verify` (126836400598), completed successfully.
- Source: user-provided publicly shared Google Drive file, **not** independently authenticated as an Apple download.
- Downloaded bytes: **8,724,152,320**
- Observed SHA-256: `4d26644c2e7876c022f40a6e2459b1e3ae32027fedbd297bab82379bb40c6a4a`
- Integrity report artifact: `23H24-drive-integrity`, artifact ID `13358559039`.
- Log shows gdown transfer reached 100%, then `stat` and `sha256sum` completed. The workflow removed the downloaded `.aea` from the runner after hashing.

## Interpretation and remaining blockers

This verifies a successful cloud-to-runner transfer and records the digest of the received bytes. It **does not** verify an independently trusted Apple digest, a signed firmware manifest, exact build 23H24, device compatibility, or decryptability of the AEA archive. The Google Drive file is not equivalent to verified Apple CDN provenance.

Before treating this as a trusted 23H24 CoreGraphics source:
1. Establish authoritative archive identity and build/device metadata from a trusted independent source, and compare with the observed archive.
2. Determine whether the AEA container can be decrypted/extracted using legitimate available keys/tools. Do not infer CoreGraphics availability from successful download alone.
3. Only after extraction, record CoreGraphics binary identity and perform reproducible comparisons to 23H30 and 23G83, keeping patch attribution tentative until corroborated.

No jailbreak, exploit, firmware installation, or device modification is established by this evidence. Keep PR #37 in draft.

## Authentication checkpoint (2026-11-05)

The successful transfer was independently rechecked against GitHub Actions run 41904780241, job 126836400598. Its log confirms the full 8,724,152,320-byte transfer, SHA-256 `4d26644c2e7876c022f40a6e2459b1e3ae32027fedbd297bab82379bb40c6a4a`, and artifact 13358559039 (383-byte integrity report, not the firmware). The workflow explicitly deleted the temporary `23H24.aea` after hashing. Therefore no retained firmware bytes are available in that artifact for inspecting the AEA prologue, decrypting, or extracting CoreGraphics.

The subsequent live `ipsw download ota --platform ios --device iPhone17,4 --build 23H24 --json` query in run 42101677930 returned schema version 1 with an empty `otas` array. This establishes only that this query did not return a matching OTA at that time; it does not establish that the Google Drive archive is authentic or inauthentic.

### Authentication gates (do not infer success)

| Gate | Evidence | Status |
| --- | --- | --- |
| Transfer and local digest observation | GitHub run 41904780241, artifact 13358559039 | Verified |
| AEA magic/header/profile | Requires access to original archive bytes; expect `AEA1` magic, then inspect profile and authenticated metadata | Unverified |
| Independent Apple CDN URL, metadata, size, published hash | Must obtain Apple-served asset record matching exact archive; live OTA discovery returned no match | Blocked |
| Build 23H24 and device iPhone17,4 identity | Requires independent Apple asset metadata and/or authenticated extracted firmware metadata | Unverified |
| Decryption and CoreGraphics extraction | Requires legitimate key/tooling and archive bytes; successful transfer alone is insufficient | Unverified |

Do not compare the GitHub artifact ZIP digest with the firmware SHA-256: these identify different objects. Do not claim a cryptographic signature from an AEA magic check; some AEA encryption profiles are unsigned. The next meaningful archive-side operation is to inspect the first bytes and authenticated metadata of the *existing* Drive file without treating the filename or uploader's label as proof of origin. Keep PR #37 draft and avoid repeated multi-gigabyte transfers solely to re-establish the same observed hash.

## Independent Apple CDN comparison (2026-11-05)

GitHub Actions run [42102662794](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/42102662794), job 127509224136, completed successfully using the live-then-AppleDB metadata discovery workflow. Its source validation required build `23H24`, device `iPhone17,4` (for historical metadata), Apple CDN host `updates.cdn-apple.com`, and exact filename `9fa3dca87b9d18a7329eada91fcd038086f20c37e1aed47f8735f0970b27cd14.aea`.

The Apple CDN transfer completed and reported **8,724,152,320 bytes** and SHA-256 **`4d26644c2e7876c022f40a6e2459b1e3ae32027fedbd297bab82379bb40c6a4a`**. These independently observed values exactly match the prior Google Drive transfer in run 41904780241. Integrity artifact `ota-23H24-observed-integrity`, ID **13450657001**, contains the source-discovery and transport reports (not the firmware bytes).

**Revised assessment:** The Google Drive archive's byte identity with the independently downloaded Apple CDN archive is strongly corroborated by matching full-file SHA-256 digests. The prior live-only OTA lookup failure is resolved through historical metadata discovery. This is evidence of Apple CDN provenance for those bytes, but is **not** an independent published Apple SHA-256, signed firmware-manifest verification, decryption, extracted build metadata verification, or CoreGraphics binary comparison. The source and transport gates are resolved; AEA header/cryptographic content gates remain open. Preserve PR #37 as draft.

## Successful cross-build extraction checkpoint (2026-11-05)

Workflow [42106199925](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/42106199925) completed successfully at commit `bec478d994b5f818f796897e4fa6aca38d6df959`. Its artifact upload steps confirm comparison reports (`coregraphics-build-comparison`, ID **13455461822**), extracted CoreGraphics binary pairs `23G83/23H30` (ID **13453628648**) and `23H24/23H30` (ID **13453438792**), and diagnostics (ID **13453513652**). This establishes that the CI pipeline reached extraction, comparison, and evidence export; interpretation of individual JSON findings still requires review. The 23H24/23H30 binaries are available through the workflow artifact, not committed to Git. This is not evidence of an exploitable vulnerability or untethered jailbreak.

## Review of uploaded comparison JSON (2026-11-05)

Downloaded and inspected `coregraphics-build-comparison` artifact **13455461822** from run **42106199925**. Both `coregraphics-function-diff.json` (23G83 versus 23H30) and `coregraphics-26-7-function-diff.json` (23H24 versus 23H30) report **25 shared and successfully compared `aa_*` symbols**, with **15 normalized instruction-stream differences**. The two `coregraphics-*-conversion-cfg-audit.json` reports each contain **14 analyzed function-side records**, **45 conversion records**, **13 with** and **32 without** `cfg_nan_guard_cutset_coverage` flagged true. The checker explicitly states that structural diagnostics are not a register/flag dataflow or safety proof. Counts should not be interpreted as independent vulnerabilities, confirmed exploit paths, or proof of CVE attribution. The two build comparisons must still be reviewed at the individual changed-instruction and dataflow level. The binary metadata reports establish distinct Mach-O SHA-256 values across compared builds; this alone does not establish which changes are security fixes.

## Three-build symbol-fingerprint triage (2026-11-05)

Compared `coregraphics-function-diff.json` (23G83 versus 23H30) and `coregraphics-26-7-function-diff.json` (23H24 versus 23H30) from artifact **13455461822**, matching by symbol name. The fixed 23H30 normalized instruction SHA-256 fingerprints agree for **all 25 shared `aa_*` symbols** across the two reports. The target fingerprints differ between 23G83 and 23H24 for **eight symbols**: `_aa_cache_render`, `_aa_close`, `_aa_cubeto`, `_aa_lineto`, `_aa_quadto`, `_aa_rectat`, `_aa_render`, and `_aa_render_shape`. The other **17** target fingerprints agree across those two builds. Target-side instruction counts for the eight changed symbols remain equal across 23G83 and 23H24, so this fingerprint comparison alone does not establish control-flow changes or semantics. The 23H30 reference differs from both earlier builds in 15 symbols; the overlap is not proof of security patch attribution. Next: inspect precise instruction edits and resolve relocation, compiler, and dataflow explanations before claiming a vulnerability or fix.

## Instruction-level triage of eight 23G83-to-23H24 fingerprint changes (2026-11-05)

Read both normalized per-symbol instruction arrays in comparison artifact **13455461822**, aligned by symbol and instruction index. All eight fingerprint-changing `aa_*` symbols have equal target-side instruction counts between 23G83 and 23H24. Exactly **21 positions** differ: **16** `ldr` immediate-offset changes `#0xc30` to `#0xc58` (two per function), and **5** `add x17, x17` immediate-offset changes `#0xfe8` to `#0x118` (two in `_aa_cache_render`, two in `_aa_render`, one in `_aa_render_shape`). All five changed `add` instructions occur in an `adrp x17` / `add x17` / `ldr x16, [x17]` / `blraa x16, x17` sequence, consistent with a relocated authenticated indirect-call target or stub. The 16 `ldr` offset changes likewise suggest moved data references. No inserted/deleted instructions, changed branch opcodes, or modified arithmetic/validation operations were observed **within these eight target-side instruction arrays**. These findings favor layout/linkage differences over a demonstrated functional patch for 23G83 versus 23H24, but do not prove semantic equivalence: effective address, relocation target, section and imported-symbol identities remain unverified. They also do not explain the 15 differences between each target and 23H30. Continue with relocation-target resolution and 23H24-to-23H30 dataflow review before attributing a security fix.

## Direct 23H24-to-23H30 instruction-count triage (2026-11-05)

Reopened the actual `coregraphics-26-7-function-diff.json` from artifact **13455461822** and compared per-symbol normalized instruction arrays. Of the **15** symbols with different instruction fingerprints, **eight** have different instruction counts, making them higher-priority leads for semantic review: `_aa_clip_edge` **162→280**, `_aa_clipping` **120→178**, `_aa_close` **69→66**, `_aa_cubeto` **313→336**, `_aa_lineto` **113→163**, `_aa_moveto` **86→122**, `_aa_quadto` **242→269**, and `_aa_rectat` **164→221** (23H24→23H30). The other seven changed symbols retain equal instruction counts: `_aa_cache_render`, `_aa_create`, `_aa_free_edges`, `_aa_line_render`, `_aa_line_render_shape`, `_aa_render`, and `_aa_render_shape`. Equal instruction counts do not prove equivalent behavior, and changed counts may reflect optimization or build configuration. A preliminary sequence alignment reveals multi-instruction replacements in the eight priority functions; they must be analyzed for control/dataflow and relocation targets before attributing any fix to CVE-2026-86950. No vulnerability or exploit has been demonstrated.

## Opcode-frequency triage of 23H24-to-23H30 structural changes (2026-11-05)

Read `coregraphics-26-7-function-diff.json` from artifact **13455461822** and counted opcode mnemonics in each of the eight previously shortlisted functions (normalized symbol-scoped instruction arrays). The `fcmp` counts (23H24→23H30) are `_aa_clip_edge` **8→30**, `_aa_clipping` **18→30**, `_aa_close` **1→1**, `_aa_cubeto` **11→17**, `_aa_lineto` **5→19**, `_aa_moveto` **7→13**, `_aa_quadto` **16→22**, and `_aa_rectat` **25→37**. New `b.vs` instructions in the fixed-reference stream are counted as +7, +4, +0, +2, +4, +2, +2, +4 respectively. The `fcvtzs` count is unchanged except `_aa_clip_edge` **6→7** and `_aa_lineto` **1→3**. These opcode deltas suggest additional floating-point comparisons and conditional handling in the reference build, but do **not** demonstrate a security patch, prove NaN guard dominance, identify branch predicates or compare operands, or establish CVE attribution. The immediate next test is address-aware CFG/dataflow review of `fcmp` / `b.vs` pairs and their paths to floating-point-to-integer conversions, especially `_aa_clip_edge` and `_aa_lineto`.

## Conversion-site CFG coverage review for two priority symbols (2026-11-05)

Read `coregraphics-26-7-conversion-cfg-audit.json` from comparison artifact **13455461822** and counted per-conversion `cfg_nan_guard_cutset_coverage` values, rather than inferring coverage from opcode counts. For `_aa_clip_edge`, **0/6** target 23H24 conversion sites are structurally covered versus **4/7** fixed 23H30 sites; for `_aa_lineto`, **0/1** versus **2/3**. All records in these two symbols report zero unresolved control transfers, but the audit itself explicitly lacks full register/flag dataflow and cannot establish safety. In the fixed `_aa_lineto` records, the conversion at `0x184331d80` is covered and has a dominating `b.vs` at `0x184331d24`, while `0x184331db8` is not covered despite a dominating `b.vs` at `0x184331d54`, illustrating why a nearby NaN branch alone is insufficient. In fixed `_aa_clip_edge`, four sites are structurally covered and three are not. **Interpretation:** meaningful differences in static guard coverage are observable; neither uncovered conversions nor added guards prove an exploitable bug, a complete fix, or CVE-2026-86950 attribution. Next: inspect operand provenance, branch conditions, and dominating paths before asserting semantic security impact.
