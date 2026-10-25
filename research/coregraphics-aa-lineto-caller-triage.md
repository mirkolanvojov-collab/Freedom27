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
