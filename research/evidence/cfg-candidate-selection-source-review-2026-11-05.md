# CFG candidate-selection implementation review (2026-11-05)

Inspected `research/scripts/analyze_coregraphics_conversion_cfg.py` on branch `research/cve-source-reconciliation-2026-10-24`.

## Confirmed implementation behavior

`_path_nan_guard_nodes` recognizes a candidate only if a `b.vs` or `b.vc` is immediately preceded in the instruction list by a self-compare matching `fcmp sN, sN` or `fcmp dN, dN`. It chooses the NaN successor as the branch target for `b.vs`, or fallthrough for `b.vc`, then requires that successor to have no CFG path to the conversion. If these conditions are not met, the branch is omitted from `cfg_nan_guard_branches`.

`analyze_function` separately gathers **all** dominating self-compares and **all** dominating `b.vs` branches, without requiring adjacency, same register, or a direct relationship. Consequently, `structural_nan_guard_in_dominators=true` and `cfg_nan_guard_branches=[]` are compatible: the two fields answer different questions. This is sufficient to explain how the four zero-candidate records can arise, **but not sufficient to determine which exact predicate failed for each site** without tracing the addressed instruction records.

The coverage check removes all candidate branch nodes and tests whether entry can still reach the conversion. This is a deliberately conservative graph criterion; a negative result does not demonstrate that NaN reaches an unsafe conversion. The script's own limitations warn about loop-back paths, missing value/flag provenance, and branch semantics.

## Engineering recommendation

Before changing the recognition logic, add per-conversion diagnostic counts and reasons: adjacent compare/branch pairs; missing/invalid NaN successor; NaN successor that can reach conversion; and candidate nodes excluded by the cutset. Preserve existing boolean fields for compatibility, add tests for separated compares and loop paths, and ensure no diagnostic is reported as proof of safety. Only then consider broader predicate recognition with explicit NZCV clobber tracking.

This review is source-level and does not claim to have reproduced the four exact exception paths or to have fixed the analyzer. No device was accessed.
