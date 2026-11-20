# CoreGraphics `_aa_lineto` caller-triage note

**Status:** partial static evidence; caller tracing is not complete.  
**Target:** iPhone17,4 / iOS 26.6.1 / build 23G83.  
**Reference:** iPhone17,4 / iOS 26.7.1 / build 23H30.  
**Evidence run:** [GitHub Actions run 160](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40236984299).  
**Archived diagnostic artifact SHA-256:** `9f19ffda77bd767eb5bfb0749c9b0f5f4d463cf542a1c04eb15573dc62909c25`.

## What the captured log says

The target-side diagnostic `target-xref-aa_lineto.txt` records five xref locations for the CoreGraphics symbol `_aa_lineto`:

| Xref address | Reported containing symbol | Reported offset |
| --- | --- | ---: |
| `0x1846952e4` | `_process_path_element.15286` | +244 |
| `0x1842fc91c` | `_RIPRenderRectangles` | +1508 |
| `0x1843171b0` | `_ripr_path_fill` | +68 |
| `0x18433d95c` | `_ripr_stroke_iterate` | +52 |
| `0x184694f4c` | `_aa_path_iterate` | +236 |

The same diagnostic identifies the queried target symbol address as `0x18430ab5c`. The recorded command used `ipsw dyld xref <cache> <address> --all` and returned exit status 0.

The separate `target-xref-aa_path_iterate.txt` run completed with exit status 0 but produced no caller rows in the captured output. That absence is **not** evidence that the function has no callers. The experimental xref command scans shared-cache symbol metadata and has previously been slow or incomplete in this runner environment.

## What can and cannot be inferred

- The log is a lead that `_aa_path_iterate` has a call/reference site at `0x184694f4c` associated with `_aa_lineto`; the offset is consistent with the target `_aa_path_iterate` entry address `0x184694e60` reported by the symbol listing.
- The other four reported locations are candidate upstream call paths to review.
- An xref listing alone does not establish a complete call graph, runtime reachability, argument provenance, bounds invariants, attacker control, or a vulnerability.
- The target and fixed `_aa_path_iterate` normalized instruction streams were previously reported as matching. This is a useful narrowing result, not proof that all caller behavior or referenced data is equivalent across builds.

## Next bounded static checks

1. Resolve each candidate address against the target CoreGraphics disassembly and confirm whether the instruction is a direct branch/call or another kind of reference.
2. Recover the enclosing function boundaries for `_process_path_element.15286`, `_RIPRenderRectangles`, `_ripr_path_fill`, and `_ripr_stroke_iterate` using Mach-O function metadata where available; do not assume a local/private name is exported.
3. For each confirmed call site, trace the argument registers and the source of point coordinates, transform context, and bounds into `_aa_path_iterate`. Mark unresolved data flow explicitly.
4. Compare the same caller sites and relevant instructions in build 23H30 before drawing any patch-attribution conclusion.

This note records evidence and limitations only. It does not execute either binary, interact with a device, or claim exploitability or a jailbreak.


## Follow-up: conversion-path evidence from the preserved comparison artifact

The successful read-only comparison artifact from [workflow run 160](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40236984299) provides a stronger, function-scoped lead than the xref list alone. Its recorded CoreGraphics hashes are target `0dc5ef74a54e7040857af5cafe796fa647f6dd552b4688fece7d5d84d2fb08ba` and fixed reference `ce59778ac827c624d005a8c0c96fba62a50d8a366b490bfb284a703d38967617`.

### Observed differences

- `_aa_path_iterate` has 221 instructions on each side and its normalized instruction stream matches.
- `_aa_lineto` differs substantially: the target stream has 113 instructions, while the fixed-reference stream has 163.
- The target `_aa_lineto` contains a vector conversion sequence including `fcvtzs v0.2d, v0.2d` followed by `xtn v0.2s, v0.2d`; the CFG audit reports no dominating self-compare/NaN branch and no dominating clamp-constant load for that conversion.
- The fixed-reference `_aa_lineto` has three scalar `fcvtzs` sites. The audit identifies explicit `fcmp d1, d1` / `b.vs` NaN-check patterns and loads corresponding to the two verified clamp constants at offsets `0x6f8` and `0x700` on two of those paths. The constants are recorded as `-1073737729.0` and `1073737729.0`; the constant-validation report says both match the expected values.
- The audit reports a third fixed-reference conversion with clamp loads and structural cutset coverage but without a dominating self-compare. This is why the report is treated as a triage signal rather than a proof of complete guard correctness.

### Interpretation and remaining checks

This is a concrete static difference consistent with additional non-finite-value handling and clamping in the fixed reference's `_aa_lineto`. It is not, by itself, proof that this change is the fix for CVE-2026-86950, nor that the target path is reachable with attacker-controlled NaN or out-of-range coordinates. The CFG tool does not establish register/flag data flow, loop invariants, pointer validity, allocation bounds, or semantic equivalence of the constants after relocation.

Next checks should establish (1) how `_aa_lineto` obtains its coordinate values and context, (2) whether those values can be influenced by an untrusted document or image through a supported parser/API path, (3) how the conversion results flow into `_aa_add_edges` and its count/index/allocation invariants, and (4) whether the changed fixed-reference instructions are attributable to the cited CVE using a primary Apple advisory or patch source. Until those are established, record this as a high-priority static lead, not a confirmed vulnerability or exploit chain.


## Follow-up: bounded caller disassembly from workflow run 169

The newer successful comparison run [169](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40240737732) captured symbol-scoped disassembly for `_aa_path_iterate`, `_RIPRenderRectangles`, `_ripr_path_fill`, and `_ripr_stroke_iterate` in both builds, plus a small target-side window at the recorded private call site. All eight symbol captures reported success, and the local window was captured. The absolute address `0x1846952c4` did resolve in this extracted target Mach-O: the window shows the epilogue guard followed by a branch at `0x1846952e4` to `_aa_lineto`. This validates that particular capture, but the address remains build-specific and must not be reused for another binary without resolving its image mapping.

### Confirmed call-site patterns

- Target `_ripr_path_fill` at `0x1843171a4` loads two doubles from the path-data pointer (`ldp d0, d1, [x8]`), narrows them to single precision (`fcvt s0, d0`, `fcvt s1, d1`), then tail-branches to `_aa_lineto` at `0x1843171b0`. The fixed reference shows the same instruction pattern at relocated addresses `0x18433e678`–`0x18433e684`.
- Target `_ripr_stroke_iterate` similarly loads two doubles from `[x2]`, narrows them to single precision, and branches to `_aa_lineto` at `0x18433d95c`; the fixed reference has the same pattern at `0x184364e24`–`0x184364e3c`.
- Target `_RIPRenderRectangles` has direct calls to `_aa_lineto`, including `0x1842fc91c`, after arithmetic on coordinates and float narrowing. The fixed reference contains corresponding call sites at `0x18432391c` and nearby offsets.
- In target `_aa_path_iterate`, the confirmed tail branch at `0x184694f4c` follows transform and ordered SIMD bound comparisons/selects; the fixed reference has the corresponding branch at `0x1846bc514`. This is consistent with the previously observed matching normalized `_aa_path_iterate` body.

### What this narrows—and what it does not

The captured call sites support that multiple internal path/rendering routes pass coordinates into `_aa_lineto`, and the sampled caller instruction patterns are substantially alike across the target and fixed builds. The strongest observed target/fixed difference remains inside `_aa_lineto` itself, where the conversion/clamp logic differs. The caller excerpts do not establish that any particular input is untrusted, that NaN or extreme values survive all upstream processing, or that the downstream edge builder violates a memory-safety invariant.

Next, trace the path-data pointer and command-count/length validation back to the public document or image parsing entry points, then inspect the complete `_aa_add_edges` implementation and its allocation/count checks. Keep all conclusions static and evidence-scoped until those links are established.


## Follow-up: `_aa_add_edges` contract and target/reference parity

The same run 169 comparison reports `_aa_add_edges` as 138 instructions in both binaries with identical normalized instruction streams. Its captured instruction flow provides several useful checks:

- It returns early when the supplied count in `x2` is zero.
- For a nonzero count, it loads the pair of 32-bit values at the supplied coordinate pointer, advances that pointer by eight bytes per iteration, and decrements the remaining count until zero.
- It calls `_aa_new_edge` and checks the returned pointer for null before writing edge fields. This is evidence of an allocation-failure check, not a complete proof of all allocation invariants.
- In the target `_aa_lineto` conversion path, the shown sequence stores the packed converted coordinate pair to a stack slot, sets `x2 = 1`, passes that stack address as `x1`, and calls `_aa_add_edges`. At the instruction level, this is consistent with one two-coordinate record being supplied to a one-item loop.

No immediate target/reference divergence was found in `_aa_add_edges`, and the visible count/pointer sequence does not by itself establish an out-of-bounds condition. Remaining uncertainty is concentrated upstream: whether the floating-point values can reach the differing `_aa_lineto` conversion with non-finite or extreme values, and what upstream API/parser constraints apply. A full proof would still require validating the relevant structure layout, count provenance, all `_aa_new_edge` allocation paths, and the source of the path records.


## Follow-up: input transformation and public API leads (run 169 evidence)

A second pass over the addressed instruction records clarifies the conversion context:

- At target `_aa_lineto` entry (`0x18430ab5c`), the first argument is retained as the context/state pointer in `x19`. The coordinate input arrives in SIMD registers: the code combines the low 32-bit lanes of `v0` and `v1`, widens the two single-precision values to doubles, and applies a context scalar at offset `0xa8` when its comparison indicates it is nonzero. The resulting pair is held in `v17` and used by later clipping/bounds logic.
- On the target's direct conversion path (`0x18430acb8`–`0x18430ace0`), the code loads transform data from context offsets `0xa0` and `0x80`, performs vector fused multiply-add, converts both lanes with `fcvtzs v0.2d, v0.2d`, narrows with `xtn`, stores the packed pair, and calls `_aa_add_edges` with count one.
- The fixed-reference function has scalar conversion paths instead. In the non-clipping path around `0x184331d14`–`0x184331e18`, it calculates transformed coordinates separately, checks each computed double against itself (`fcmp dN, dN`) to detect NaN, and compares against clamp constants before integer conversion or selects sentinel values. The clipping path is different and calls `_aa_clip_edge`; therefore this is not evidence that every possible path has identical guard coverage.
- `_aa_add_edges` itself is byte-for-byte normalized-equivalent across the two extracted builds (138 instructions each). It consumes `x2` coordinate records from `x1` in eight-byte steps, updates context bounds/state, computes edge parameters, and calls `_aa_new_edge`; the allocation result is null-checked. This narrows the visible difference to coordinate preparation and conversion, but does not prove an out-of-bounds write in this path.

The target symbol table also contains public CoreGraphics entry points that are useful upstream trace candidates, including `_CGPathAddLineToPoint`, `_CGPathAddCurveToPoint`, `_CGPathAddQuadCurveToPoint`, `_CGPathCreateWithData`, `_CGPathApply`, `_CGContextAddLineToPoint`, `_CGContextStrokePath`, and `_CGContextFillPath`. The symbol listing alone does not show their validation behavior or prove that any of them reaches this exact rasterization path. The next pass should inspect these function bodies and follow the path-data pointer/element count to the render callbacks, then compare corresponding fixed-build logic. No parser-to-rasterizer input provenance is claimed yet.

## CVE attribution guardrail

Public advisory records identify CVE-2026-86950 as a CoreGraphics out-of-bounds write addressed by improved bounds checking, with malicious-file processing described as a possible route. That high-level description is consistent with investigating bounds and coordinate conversion, but it does not identify `_aa_lineto` as the vulnerable function. The binary-level change remains a candidate correlation until a primary Apple patch/advisory detail or a defensible end-to-end bounds invariant links it to the CVE.
