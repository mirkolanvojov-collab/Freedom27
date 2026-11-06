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

## Initial operand and conditional-selection trace (2026-11-05)

Inspected address-preserving instructions in `coregraphics-26-7-function-diff.json` from artifact **13455461822**, focused on `_aa_lineto` and `_aa_clip_edge`.

- **23H24 `_aa_lineto` at 0x184331cc4–0x184331cd0:** `fmla v0.2d, v17.2d, v1.2d`; `fcvtzs v0.2d, v0.2d`; `xtn v0.2s, v0.2d`; then stores the packed result. This is a vector multiply-add followed by floating-point-to-integer conversion and narrowing; no guard is evident in this local instruction window.
- **23H30 `_aa_lineto` at 0x184331d74–0x184331d88:** loads a floating-point comparison constant through `adrp/ldr d2`, executes `fcmp d1, d2`, then `fcvtzs w9, d1`, `csel w8, w8, w9, gt`, and stores `w8`. At 0x184331db4–0x184331dc0 a similar `fcmp`/`fcvtzs`/`csel gt` sequence appears; at 0x184331dec–0x184331e08 a `fcmp` and `b.le` control whether `fcvtzs w8, d0` executes or a preloaded fallback is stored. These demonstrate *conditional use* of converted results, not that every conversion is guarded from execution.
- **23H24 `_aa_clip_edge` at 0x1843353e8–0x1843353f8:** `fmadd d0, d4, d0, d6`; `fcvtzs w9, d0`; `fmadd d0, d5, d1, d6`; `fcvtzs w10, d0`; then stores both integers.
- **23H30 `_aa_clip_edge` at 0x1843356c8–0x1843356dc:** loads a floating-point constant into `d3`, compares `d2` with `d3`, executes `fcvtzs w10, d2`, then `csel w10, w9, w10, gt` and stores. Similar sequences occur at 0x184335628 and 0x1843357bc. These establish added compare-and-select logic, but not the values of loaded constants or full input provenance.

**Caveats:** ARM64 `fcmp` sets flags including an unordered case; `csel ... gt` chooses the conversion result only when the ordered greater-than condition holds, but this local observation does not prove complete NaN/infinity or range handling. Branch destinations, loaded constants, and register definitions must be resolved before asserting a security fix or CVE attribution. The static CFG audit is not a full dataflow proof. No exploit has been demonstrated.

## Address-aware branch and register-def tracing (2026-11-05)

Re-inspected the address-preserving 23H30 instructions in `coregraphics-26-7-function-diff.json` from artifact **13455461822** (not a live-device test). In `_aa_lineto`, `ldr d1,[x19,#0x80]` at **0x184331d14** and `ldr d0,[x19,#0xa0]` at **0x184331d18** feed `fmadd d1,d1,d9,d0` at **0x184331d1c**. The self-compare `fcmp d1,d1` at **0x184331d20** and `b.vs` at **0x184331d24** explicitly branch on unordered/NaN before the subsequent integer-conversion path. The next `fcmp d1,d2` uses a floating constant loaded from **0x1847e96f8** (`adrp`/`ldr` at 0x184331d28–d2c); `b.pl` at 0x184331d34 selects an alternate saturation path. The upper comparison constant is loaded from **0x1847e9700** at 0x184331d74–d78, and `csel` at 0x184331d84 chooses a fallback integer or converted value according to flags. A parallel branch at **0x184331d4c–d54** checks another `fmadd` result for NaN. A second coordinate is calculated at **0x184331d8c–d94** and checked by `b.vs` at **0x184331d98**, then range-tested at **0x184331dd4–e04** before the value is stored and passed to `_aa_add_edges` at **0x184331e18**.

In fixed `_aa_clip_edge`, `ldr d19,[x1,#0x80]` and `ldr d18,[x1,#0xa0]` at **0x184335440–444** feed `fmadd d4,d19,d4,d18` at **0x184335448**. `fcmp d4,d4; b.vs` at **0x18433544c–450** explicitly detects unordered/NaN and skips the subsequent conversion. Comparisons against the same `__TEXT,__const` addresses **0x1847e96f8** and **0x1847e9700** control fallback/selection at **0x184335460–478**. A second `fmadd` at **0x184335488** is followed by `fcmp d4,d4; b.vs` at **0x18433548c–490** and lower/upper comparisons at **0x1843354a0–4bc** before `fcvtzs` at **0x1843354c0**.

**New verified insight:** self-comparisons followed by `b.vs` explicitly handle unordered/NaN in these local 23H30 paths, and shared floating-point constant addresses act as apparent bounds. The bytes and numeric values at those two addresses have **not** been extracted; they must not be labeled as particular thresholds. Register-provenance and local branch observations do not establish complete-path coverage, behavior for infinity, or exploitability. Next: extract exact eight-byte values at the two constant addresses from the verified 23H30 Mach-O and perform fuller CFG/dataflow checks.

## _aa_lineto predecessor trace (2026-11-05)

In the 23H30 address-preserving disassembly from comparison artifact 13455461822, the path to the conversion at `0x184331db8` comes through `fmadd d1,d1,d9,d0` (`0x184331d48`), `fcmp d1,d1` (`0x184331d4c`), and `b.vs` (`0x184331d54`), then a lower-bound comparison and `b.pl` (`0x184331d60`) to `0x184331da4`. At `0x184331db4`, `d1` is compared to the upper-bound constant; `fcvtzs w10,d1` at `0x184331db8` is followed by `csel w9,w9,w10,gt` and a store. No instruction on this inspected path overwrites `d1` after its self-comparison. The conversion still executes even if the conditional selection subsequently chooses a fallback. This is a local register-provenance and output-selection finding, not a proof of complete safety, exploitability, or CVE attribution.

## 23H24 versus 23H30 numeric-handling milestone (2026-11-05)

Compared the address-preserving instructions in `coregraphics-26-7-function-diff.json` from comparison artifact 13455461822. In 23H24 `_aa_lineto`, `fmla v0.2d,v17.2d,v1.2d` at `0x184331cc4` is followed by `fcvtzs v0.2d,v0.2d`, `xtn v0.2s,v0.2d`, and `str d0,[sp,#0x38]` at `0x184331cc8–cd0`. In 23H30, a scalar path at `0x184331d14–d88` calculates `d1`, checks `fcmp d1,d1` and `b.vs`, compares against lower and upper float64 bounds, converts with `fcvtzs w9,d1`, and conditionally selects an integer before storing. A second scalar path at `0x184331d40–dc0` has analogous checks and a conditional selection. The newer implementation is not merely an address-relocation of the older vector conversion.

In 23H24 `_aa_clip_edge`, one path at `0x184335298–2a8` performs `fmadd`, `fcvtzs`, `fmadd`, `fcvtzs`, then paired integer store, with a similar path at `0x1843353e8–3f8`. In 23H30, a path at `0x184335448–480` computes a coordinate, self-compares for NaN, branches on `b.vs`, compares against float64 lower/upper bounds, executes `fcvtzs` and conditionally selects an integer before storing. Another path at `0x184335488–4c4` branches around conversion for NaN and out-of-range values. These differences support a changed numeric-handling implementation but are not proof of an exploitable older-build vulnerability, complete new-build safety, or attribution to CVE-2026-86950. Other paths in both functions still require review.

## Public-source security attribution review (2026-11-05)

Apple's iOS 26.7.1 security advisory (https://support.apple.com/en-us/149226; released September 28, 2026) attributes CVE-2026-86950 to a CoreGraphics out-of-bounds write addressed by improved bounds checking and warns of possible targeted exploitation. Independent Calif research (https://calif.io/research/the-great-glyph-grift; September 30, 2026) describes a compiler-optimization-related floating-point/fixed-point conversion problem in the anti-aliased path rasterizer, with patched patterns across eight `aa_*` functions, and an undersized-allocation/out-of-bounds-write consequence when rendering crafted font data in a PDF. This public explanation is consistent with our observed 23H24-to-23H30 `aa_*` conversion, NaN-branch, clamp-bound and fallback differences, but matching high-level patterns is corroboration rather than independent reproduction of the vulnerability. A separate ipsw-diffs comparison (https://github.com/blacktop/ipsw-diffs/tree/main/iOS/26_7_23H24_vs_26_7_1_23H30) lists CoreGraphics as the updated shared-cache dylib. No controlled proof of an out-of-bounds write on iPhone17,4 / 23G83, privilege escalation, persistence, or jailbreak has been obtained. Keep security attribution supported by Apple and third-party research, while target-specific exploitability remains unresolved.

## Target-build CVE attribution evidence matrix (2026-11-05)

**Authoritative disclosure:** Apple's iOS 26.7.1 advisory (https://support.apple.com/en-us/149226, September 28, 2026) lists CVE-2026-86950 as a CoreGraphics out-of-bounds write addressed with improved bounds checking, potentially resulting in arbitrary code execution from a maliciously crafted file. This establishes the vulnerability class and fixed release, not an exploit on our particular target.

**Independent mechanism:** Calif's published analysis (https://calif.io/research/the-great-glyph-grift, September 30, 2026) attributes the fault to inconsistent floating-point-to-fixed-point conversion behavior among anti-aliased rasterizer functions and a consequent incorrect bounding box and undersized buffer. The authors report a reproducible crash on their test environments. This is third-party evidence, not a Freedom27 device test.

**Local cross-build evidence:** Comparison artifact 13455461822 contains symbol-normalized CoreGraphics instruction records for 23G83→23H30 and 23H24→23H30. Our prior fingerprint reconciliation found 17 of 25 shared target-side `aa_*` fingerprints identical between 23G83 and 23H24, including `_aa_moveto` and `_aa_lineto`; eight other functions had 21 offset-only instruction differences in their target-side streams. The local 23H24 `_aa_lineto` record contains a vector `fcvtzs` followed by `xtn`, and the 23H30 record adds explicit NaN checks, numerical bounds and fallback selection. This independently corroborates the **code-pattern relationship** across builds, not identical device runtime behavior.

**Assessment:** The combination of Apple's advisory, independent mechanism research, and our local binary comparison supports **high-confidence association of the observed rasterizer numerical-handling changes with the published CVE fix**. It does not verify exploitability, actual device reachability, memory corruption, code execution, privilege escalation, or persistence on iPhone17,4 running 23G83. Keep the distinction between published third-party reproduction and our own verified artifacts explicit. No jailbreak is demonstrated.

## Published affected-version applicability checkpoint (2026-11-05)

Apple's iOS 26.7.1 security advisory (https://support.apple.com/en-us/149226) confirms CVE-2026-86950 is a CoreGraphics out-of-bounds write addressed by improved bounds checking and applies to iPhone 11 and later. The NVD record (https://nvd.nist.gov/vuln/detail/CVE-2026-86950, last modified October 27, 2026) lists Apple iOS 26.0 up to but excluding 26.7.1 as affected, which includes our iPhone17,4 target's iOS 26.6.1 (23G83). NVD also records the CVE in CISA's Known Exploited Vulnerabilities catalog (added September 29, 2026). This **resolves published version applicability**, not target-device exploitability. Previous local symbol fingerprint and instruction comparisons corroborate similar CoreGraphics code patterns in 23G83 and 23H24; they do not demonstrate a device crash, an out-of-bounds write, arbitrary code execution, privilege escalation, or persistence. Next research checkpoint is an evidence matrix separating documented software exposure from independently reproduced runtime behavior, without conflating a published CVE with a jailbreak capability.

## Evidence provenance and unresolved target validation (2026-11-05)

| Claim | Evidence class | Status / limitation |
| --- | --- | --- |
| iOS 26.6.1 on iPhone17,4 falls within the published affected range for CVE-2026-86950 | Apple advisory and public vulnerability catalogs | **Published applicability**, not a local runtime test |
| CVE-2026-86950 is a CoreGraphics out-of-bounds write addressed with improved bounds checking in iOS 26.7.1 | Apple advisory, https://support.apple.com/en-us/149226 | **Vendor-confirmed** vulnerability class and fixed release |
| 23G83 and 23H24 have matching normalized target-side instruction fingerprints for `_aa_moveto` and `_aa_lineto` | Our archived comparison artifact 13455461822 | **Locally verified static binary observation**, not proof of runtime reachability |
| 23H24 `_aa_lineto` uses vector `fcvtzs` followed by `xtn`, while 23H30 adds scalar comparisons, NaN handling, bounds and fallback logic | Our archived address-preserving disassembly | **Locally verified code-pattern difference**, not independently demonstrated memory corruption |
| A crafted input causes an out-of-bounds write on the user's exact 23G83 device | No Freedom27 target-device execution or controlled crash evidence | **Unverified** |
| This vulnerability enables privilege escalation, persistence, or an untethered jailbreak on iPhone17,4 | No chain, entitlement, kernel, or reboot-persistence demonstration | **Unverified / not achieved** |

**Decision:** Public affected-version applicability and local binary patch-pattern reconciliation can be marked complete as *research evidence*. Target-device exploitability and the downstream jailbreak prerequisites must remain separate, open gates. Avoid upgrading static comparison results or third-party demonstrations into claims of a Freedom27 runtime exploit. For personal device safety, Apple's recommended mitigation is to install a patched iOS release; do not treat continued exposure as evidence of jailbreak progress.

## Jailbreak-capability evidence gates (2026-11-05)

This checkpoint deliberately separates the documented CoreGraphics vulnerability from capabilities needed for a device jailbreak.

| Capability gate | Evidence available | Conclusion |
| --- | --- | --- |
| Published affected-version applicability for iPhone17,4 on 23G83 | Apple's iOS 26.7.1 advisory (https://support.apple.com/en-us/149226) and prior version-reconciliation notes | Supported by vendor disclosure and version mapping |
| Vulnerable-code-family and patch-pattern identification | Locally archived normalized instruction and address-preserving CoreGraphics comparisons, artifact 13455461822 | Static binary pattern relationship supported |
| Controlled code execution on the exact iPhone17,4 / 23G83 target | No Freedom27 device execution evidence | **Not demonstrated** |
| Escape from a renderer or application sandbox | No target-specific capability evidence | **Not demonstrated** |
| Kernel privileges or protected-system modifications | No target-specific capability evidence | **Not demonstrated** |
| Untethered persistence after reboot | No target-specific capability evidence | **Not demonstrated** |

Apple describes CVE-2026-86950 as an out-of-bounds write whose impact **may** include arbitrary code execution from processing a crafted file; this statement does not imply a demonstrated Freedom27 exploit or downstream jailbreak privileges. No device test, proof of kernel access, persistence test, or exploit chain is part of the available evidence. The research result is a documented entry-point candidate, **not** a completed jailbreak primitive. For user-device security, installing an Apple-patched release mitigates the published vulnerability.

## CoreGraphics execution-context and sandbox-boundary assessment (2026-11-05)

**Public platform constraints:** Apple's runtime-process security guide (https://support.apple.com/guide/security/security-of-runtime-process-sec15bfe098e/web) documents app sandboxing, signed entitlements, ASLR and executable-memory restrictions. Apple's Quick Look developer documentation (https://developer.apple.com/documentation/QuickLook) documents PDF preview support, and WebKit's GPU-process architecture (https://webkit.org/blog/14445/webkit-features-in-safari-17-0/) illustrates that drawing can occur in a separate process. These are platform-level descriptions, **not** proof of the precise process handling the affected CoreGraphics rasterization path on iPhone17,4 / iOS 26.6.1.

| Context claim | Evidence | Assessment |
| --- | --- | --- |
| CoreGraphics functionality may be reached through document or graphics rendering | Public framework descriptions and published CVE context | Plausible entry surfaces, not route-specific confirmation |
| Specific vulnerable path's hosting process on 23G83 | No target-process trace or process identity record | **Unknown** |
| Sandbox profile, effective privileges, and signed entitlements of that process | No verified target-process metadata | **Unknown** |
| Exploitation would escape its sandbox or modify protected system resources | No Freedom27 execution or privilege evidence | **Not demonstrated** |
| Persistence across device reboot | No persistence or reboot evidence | **Not demonstrated** |

**Decision:** Do not infer the vulnerable function's privilege level from the CoreGraphics library name, a PDF preview feature, or a generic WebKit process diagram. Treat process identity, sandbox, and entitlements as distinct unresolved questions. Continue evidence-based static research without claiming device-level code execution or an untethered jailbreak.

## Static library linkage versus runtime process identity (2026-11-05)

Reviewed Apple's dynamic-loader documentation (https://developer.apple.com/documentation/xcode/reducing-your-app-s-launch-time), dyld shared-cache layout documentation (https://github.com/apple-oss-distributions/dyld/blob/main/doc/CacheLayout.md), and Apple's runtime-process security guidance (https://support.apple.com/en-gb/guide/security/sec15bfe098e/web). A Mach-O load command or framework dependency can show that a process binary **declares a dependency** on CoreGraphics; a dyld shared-cache membership entry shows the framework is **available in the shared cache**. Neither observation establishes that a particular process executes the vulnerable `aa_*` rasterizer code with attacker-controlled input, or identifies its effective sandbox and entitlements. Conversely, indirect or runtime-loaded framework use may be missed by a direct-linkage inventory.

**Local artifact availability:** Existing Freedom27 comparison artifact 13455461822 contains CoreGraphics symbol disassembly, CFG audits, constants, and binary metadata; these are library-side observations and do not constitute a process-level dependency inventory or runtime stack trace. Therefore **no hosting process can be identified from the current evidence**. Treat any candidate process named from generic PDF/graphics APIs as hypothetical until supported by build-specific executable linkage and runtime evidence. Even verified linkage would not by itself demonstrate a vulnerable path's reachability or privileges.

**Evidence gate:** To close execution-context attribution, require (1) build-specific process executable identity and provenance, (2) verified linkage or loaded-image observation, (3) evidence the affected rasterizer path is actually invoked by that process, and (4) independent sandbox/entitlement evidence. None of these four is established by the current comparison JSON alone. No privilege escalation or untethered persistence is demonstrated.

## Direct inventory of archived comparison artifact (2026-11-05)

Inspected the **actual downloaded ZIP** for GitHub Actions artifact **13455461822** (`coregraphics-build-comparison`), rather than inferring its contents from the workflow description. It contains **nine JSON files**: `coregraphics-comparison.json`, `coregraphics-function-diff.json`, `coregraphics-constant-validation.json`, `coordinate-safety-limit-validation.json`, `coregraphics-conversion-cfg-audit.json`, `coregraphics-26-7-patch-comparison.json`, `coregraphics-26-7-function-diff.json`, `coregraphics-26-7-constant-validation.json`, and `coregraphics-26-7-conversion-cfg-audit.json`. Inspected top-level report schemas: these cover library-side binary identity, function disassembly, constants and CFG conversion checks, **not** an executable inventory, Mach-O dependency graph for host processes, process entitlements, or runtime stacks. Therefore this artifact alone cannot name a host process or its privilege context.

Apple's dyld4 architecture (https://github.com/apple-oss-distributions/dyld/blob/main/doc/dyld4.md) describes prebuilt process loader graphs, and the shared-cache format (https://github.com/apple-oss-distributions/dyld/blob/main/include/mach-o/dyld_cache_format.h) documents image entries and dependency-related structures. Such data may support **static linkage** attribution if obtained from the correct build, but does not independently establish invocation of the vulnerable `aa_*` path. This inventory closes the question of whether artifact 13455461822 already contains process-attribution evidence: **it does not**. Next evidence source would need to be a separately verified build-specific executable/cache inventory; no runtime reachability, sandbox escape, or jailbreak is demonstrated.

## Dyld loader-graph evidence source decision (2026-11-05)

Re-inspected the downloaded GitHub Actions comparison artifact **13455461822** directly. Its nine JSON reports have top-level schemas for CoreGraphics binary comparison, function instruction differences, constants, coordinate-safety limits, and CFG audits. **None includes a build-specific main-executable inventory, dyld program-loader graph, or process-entitlement records.** This is a verified artifact-content limitation, not a failed inference from filenames.

Apple's dyld4 design documentation (https://github.com/apple-oss-distributions/dyld/blob/main/doc/dyld4.md) describes `PrebuiltLoaderSet` entries for OS main executables and shared `PrebuiltLoader` dependency nodes stored in the dyld cache, with a trie mapping program paths to their loader sets. The shared-cache layout documentation (https://github.com/apple-oss-distributions/dyld/blob/main/doc/CacheLayout.md) describes cached dylib mappings. The `ipsw dyld image` guide (https://blacktop.github.io/ipsw/docs/guides/dyld/) documents tooling to inspect cache image metadata and dependents. These sources justify a **future build-specific static executable dependency inventory** as a distinct input, not a claim that such an inventory has been acquired or parsed.

**Decision and verification gate:** No hosting process is identified by artifact 13455461822. A next analysis would require a provenance-verified dyld cache / executable-loader set from the precise target build 23G83, then a distinction between direct/transitive dependencies and runtime invocation. Executable name, loaded-image evidence, and process entitlements remain unverified. Even a proven dependency would not establish vulnerable-path reachability, elevated privileges, or jailbreak persistence. Do not treat the existing 23H24 OTA or 23H30 CoreGraphics-only binary as a substitute for a 23G83 program-loader inventory.

## 23G83 target restore source identified (2026-11-05)

Located a public Apple-CDN restore-image source for **iPhone17,4 / iOS 26.6.1 / 23G83**. IPSW Downloads (https://ipsw.me/download/iPhone17%2C4/23G83/) and BetaProfiles (https://www.betaprofile.dev/ipsw/ios-26-6-1/) agree on filename `iPhone17,4_26.6.1_23G83_Restore.ipsw`, SHA-256 `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`, and approximate 10.45 GiB size. BetaProfiles specifies **11,225,458,130 bytes** and Apple CDN URL `https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw`. This is **third-party catalog metadata pointing to an Apple host**, not a completed download or independently verified checksum. The archive is marked unsigned for restoring, which does not prevent offline static inspection. Next gate: acquire archive in a suitable execution environment, verify complete SHA-256, inspect its BuildManifest and relevant cache payloads, and only then attempt a provenance-grounded process/dependency inventory. Do not infer that an available full restore contains a readily accessible dyld loader graph or that a CoreGraphics dependency establishes vulnerable-path execution.

## Successful 23G83 extraction CI and artifact boundary (2026-11-06)

GitHub Actions run [42121287345](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/42121287345), at commit `642a77ae411fce61606eccdcd884cd6cf5957d05`, **completed successfully**. Job steps explicitly succeeded for target iPhone17,4 iOS 26.6.1 (23G83) restore BuildManifest verification, target dyld-cache extraction, 23H30 and 23H24 reference-cache extraction, and CoreGraphics comparisons. Four artifacts were published: comparison JSON `13460696130` (197,517 bytes), diagnostics `13460676146` (1,208,067 bytes), 23H24/23H30 CoreGraphics raw binaries `13460481487` (8,558,906 bytes), and 23G83/23H30 CoreGraphics raw binaries `13459994467` (8,468,850 bytes). These artifact sizes are ZIP archive sizes, not extracted firmware sizes. **The workflow did not publish the complete extracted dyld cache or a host-process dependency inventory**; the successful cache extraction step alone does not establish which executable loads CoreGraphics. Follow-on evidence must be derived from the cache in a new CI job or a separate authenticated artifact, with process identity, dependencies, and runtime invocation clearly distinguished. The source-probe workflow remains unconfirmed separately and is not a prerequisite to accepting this completed extraction job's reported success. No exploit, privileges, or untethered persistence have been demonstrated.

## Target cache header report retrieved (2026-11-06)

Downloaded and inspected the diagnostics ZIP **13462738307** from successful CI run **42127758272**. Its `target-dyld-cache-provenance.txt` reports `build=23G83`, `device=iPhone17,4`, `cache_filename=dyld_shared_cache_arm64e`, `cache_size_bytes=622592`, `cache_sha256=d8e44d7473e546b64a0f21ff7648c28fe2166784cad9d47522592a9c7f7751b7`, and `cache_file_type=Dyld shared cache version 1 arm64e`. **This SHA-256 covers only the named 622,592-byte file, not the complete split cache set.** A modern dyld cache can have multiple subcache files, and the unexpectedly small size requires subcache enumeration before any comprehensive dependency inference. The archived `ipsw-dyld-inspection-help.txt` explicitly lists `ipsw dyld imports` as “List all dylibs that load a given dylib”; the command is available but has **not** been executed against the target cache. Next step: inventory all cache/subcache files and validate the command's exact arguments before any dependency report. Neither runtime invocation nor process privilege is established.

## Verified complete target dyld component inventory (2026-11-06)

Downloaded and directly parsed `coregraphics-comparison-diagnostics` artifact **13465993399** from successful run **42132581759**. The `target-dyld-cache-components.json` contains **86** enumerated files totaling **6,277,272,443 bytes (5.846 GiB)**, with a separate SHA-256 for each. Entries include numbered `dyld_shared_cache_arm64e.*` components, `.atlas`, and `.symbols`. The main `dyld_shared_cache_arm64e` component is **622,592 bytes**, hash `d8e44d7473e546b64a0f21ff7648c28fe2166784cad9d47522592a9c7f7751b7`, so that digest is not a whole-cache digest. The archive's `ipsw-dyld-imports-help.txt` documents syntax `ipsw dyld imports <DSC> [DYLIB]` and an optional `--filter` flag. This is verified tool capability, **not a completed dependency analysis**. The 86 recorded per-component hashes are provenance observations for this CI extraction, not proof of host process invocation or entitlements. Next CI step can run read-only imports against the target cache while retaining all its subcache files together and clearly distinguish dylib importers from executable process hosts.

## Reverse dependency interpretation and evidence gates (2026-11-06)

The read-only `ipsw dyld imports <DSC> CoreGraphics` query was introduced in commit `f00862b7ccb0c99c2bb8f7933017b96c888e75aa`, with explicit exit-status diagnostics in `2760fba31702c3a0c1c9c39b9e7b8d68ae48d7f0`. At this checkpoint run **42150575657** was in progress and its import query had not completed; **no importer names are yet verified**.

Interpretation protocol for the forthcoming artifact:

1. Check `target-coregraphics-imports-status.txt` first. A nonzero status means the query failed; empty stdout is not evidence of zero dependencies.
2. Preserve stdout and stderr verbatim, noting whether `CoreGraphics` resolves to a concrete cache dylib or whether the command requires a full install name such as `/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics`.
3. Classify reported entries as **static dylib reverse dependencies** only. A dylib listed as an importer does not establish a running executable, invocation of a vulnerable rasterization path, or sandbox identity.
4. For process attribution, obtain separately verified executable linkage, runtime loading/trace evidence, and process identity. None is presently available from the static dyld import query alone.
5. Do not infer exploitation, kernel privileges, untethered persistence, or a working jailbreak from the importer list. Those are independent unverified capability gates.

A successful query with zero matches is also scope-limited: dyld import metadata cannot rule out indirect, dynamic, or runtime calls.

## Verified CoreGraphics reverse import report (2026-11-06)

Successful comparison workflow **42150658901** uploaded diagnostics artifact **13474002553** (`coregraphics-comparison-diagnostics`). Direct inspection of `target-coregraphics-imports-status.txt` showed `query_exit_status=0`; `target-coregraphics-imports-stderr.txt` was empty. The output file `target-coregraphics-imports.txt` was **197,046 bytes** and listed **1,268** paths under `In DSC (Dylibs)` and **905** paths under `In FileSystem DMG (Apps)`. The latter includes application binaries, app extensions, and system executable paths, but is a static firmware-image import inventory, not a record of executing processes. Example dylib importers: `/System/Library/Frameworks/QuartzCore.framework/QuartzCore`, `/System/Library/Frameworks/CoreText.framework/CoreText`, `/System/Library/Frameworks/ImageIO.framework/ImageIO`, `/System/Library/PrivateFrameworks/UIKitCore.framework/UIKitCore`, and `/System/Library/Frameworks/WebKit.framework/WebKit`. The filesystem section includes `/usr/libexec/backboardd`, `/usr/libexec/mediaparserd`, and `/private/var/staged_system_apps/Weather.app/Weather`. Counts are the number of absolute-path lines in each report section; they are **not** distinct verified runtime processes, nor proof that any importer reaches the vulnerable anti-aliasing rasterization routine.

This closes the static CoreGraphics reverse-import **inventory milestone**, but not the execution-context, exploitability, privilege escalation, or untethered-persistence gates. Follow-up should distinguish direct importers from transitive dependencies and require runtime traces or other independent evidence before attributing a vulnerable call to any process.

## Reverse-import uniqueness and path taxonomy audit (2026-11-06)

Reparsed the raw `target-coregraphics-imports.txt` inside run **42150658901**, artifact **13474002553**. The `In DSC (Dylibs)` section contains **1,268 paths, all unique**; the `In FileSystem DMG (Apps)` section contains **905 paths, all unique**. The combined **2,173 paths** have no repeated paths within either section. Within the filesystem section, **355** paths contain `.appex/`, **568** contain `.app/`, and **26** start with `/usr/libexec/`. These are overlapping lexical path categories, not mutually exclusive execution roles.

The CLI's `imports` help explicitly describes reverse importers and provides an `--image` option for imported bind symbols of a specified image. The existing reverse-import report does **not** prove direct symbol-level call sites, runtime loading, or vulnerable rasterization invocation. Next discriminating evidence should inspect imported bind symbols for selected candidate images, check exact dylib install-name matches, and keep static linkage separate from observed process execution. No runtime or jailbreak capability gate is resolved by this audit.

## Selected framework imported-bind symbol results (2026-11-06)

Directly inspected `coregraphics-comparison-diagnostics` artifact **13495045001** from successful run **42197369523**. All five `ipsw dyld imports <DSC> --image <framework-path>` queries recorded `success` and had empty stderr. Each output is a list of imported symbol names, **not** a mapping from symbols to providing dylibs or proof of direct CoreGraphics imports.

| Selected image | Nonempty symbol lines | Lines containing literal `CoreGraphics` |
| --- | ---: | ---: |
| QuartzCore | 1,373 | 0 |
| CoreText | 739 | 0 |
| ImageIO | 1,061 | 0 |
| UIKitCore | 3,506 | 73 |
| WebKit | 6,640 | 1 |

UIKitCore examples include Swift mangled `CoreGraphics` namespace symbols such as `_$s12CoreGraphics14CGPathFillRuleOMa`; the WebKit example is a SwiftUI symbol whose signature includes `CoreGraphics7CGFloat`. These string matches **do not prove** a direct import from the CoreGraphics dylib, a call to an affected `aa_*` function, or execution of the vulnerable code path. Absence of the literal namespace in the other three lists does not disprove a CoreGraphics dependency: C symbols and indirect dependencies need not contain that string. The 5 reports are symbol inventories, and provider resolution / bind-target attribution remains unresolved.
