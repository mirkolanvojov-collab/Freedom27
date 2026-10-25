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
