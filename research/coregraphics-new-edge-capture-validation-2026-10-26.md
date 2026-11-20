# Validation status for addressed `_aa_new_edge` capture

**Date:** 2026-10-26  
**Branch:** `research/cve-source-reconciliation-2026-10-24`  
**Tooling change:** [`85a6aa1`](https://github.com/mirkolanvojov-collab/Freedom27/commit/85a6aa1a50d7199252ee79b4fab0c39915a7cd0b)

## Status

The comparison script now includes `_aa_new_edge` in `ADDRESS_PRESERVED_SYMBOLS`, so a *new run* should retain its target and fixed addressed instruction records even when the normalized streams match.

The currently available run-169 artifact is older than that change. In that artifact, `_aa_new_edge` has 37 instructions in each build and matching normalized hashes, but contains neither `target_addressed_instructions` nor `fixed_addressed_instructions`. Therefore it cannot answer the allocation-size questions from the prior stage. Do not treat the old artifact as validation of the new capture behavior.

## Required verification on the next comparison run

1. Run the existing CoreGraphics comparison workflow on the same pinned target/reference inputs and branch revision containing commit `85a6aa1`.
2. Confirm the JSON record for `_aa_new_edge` contains `target_addressed_instructions` and `fixed_addressed_instructions`, each with 37 parsed instruction records (or document any count change and inspect function-boundary metadata).
3. Confirm the artifact records both binary hashes and the script revision used to produce it. If it does not record the script revision, add that provenance before using the artifact as a reproducible result.
4. Inspect the actual allocation call and its argument data flow in each build. Record call target, size argument, alignment/rounding, null/error handling, and subsequent stores. Do not infer allocation size from function name or the caller's record stride.
5. Re-run the relevant unit tests and comparison workflow; record actual workflow URLs and results. The tooling commit currently has no reported status checks, which is **unverified**, not a pass.

## Interpretation boundary

Matching 37-instruction normalized streams would show only that the captured instruction strings match under this normalizer. It would not establish equivalent indirect-call targets, equivalent global objects, runtime reachability, or memory-safety. Resolve any indirect calls and memory references against exact-build metadata before concluding that allocation semantics are unchanged.

No binary execution, crafted input, or device test is part of this step.
