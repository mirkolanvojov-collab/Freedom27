# CoreGraphics next-stage validation review

**Review date:** 2026-10-26  
**Target:** iPhone17,4 / iOS 26.6.1 / build 23G83  
**Fixed reference:** iPhone17,4 / iOS 26.7.1 / build 23H30  
**Scope:** read-only static evidence review; no device execution, crafted trigger, or exploit validation.

## Current evidence baseline

The preserved run 169 comparison reports 25 shared `aa_*` symbols compared successfully, 15 normalized instruction streams changed, and zero disassembly failures. The target and reference CoreGraphics file hashes differ. These results establish a reproducible binary difference, not CVE attribution. Note that this comparison spans iOS 26.6.1 to 26.7.1, while the cited public patch analysis focuses on 26.7 to 26.7.1; unrelated intervening changes are possible.

Within the reviewed subset:

- `_aa_lineto` is 113 instructions in the target and 163 in the fixed reference.
- The target has a vector float-to-integer conversion and narrowing sequence without a structurally dominating NaN self-compare or the audited clamp-constant load.
- The fixed reference has scalar conversion paths with NaN/range-handling patterns on some non-clipping paths. The clipping path differs, and the existing CFG audit is structural rather than a register/flags data-flow proof.
- `_aa_add_edges` has matching normalized streams (138 instructions each); the reviewed path supplies one coordinate record. This does not prove all allocation, count, pointer, or bounds invariants.
- **Correction from artifact reinspection:** `_aa_cache_render` is 664 instructions in each build, but its normalized streams are *not* identical. The saved JSON marks `instruction_stream_identical: false` and contains 9 differing normalized instruction positions. Some are immediate offsets or memory operands that may reflect data-layout changes; their semantic impact is not established. Earlier wording that called this stream identical was inaccurate.
- Captured caller excerpts show path-data loads and float narrowing before some `_aa_lineto` branches. They do not establish untrusted-input provenance or the validity of the source buffer/element count.

## Highest-value next checks

1. **Expand comparison beyond the first interesting function.** Review every changed `aa_*` symbol in the preserved `coregraphics-function-diff.json` and rank changes by direct bounds-checking, index/count arithmetic, allocation sizing, and stores. Treat function names and instruction-count changes as triage signals only.
2. **Validate conversion semantics.** For each candidate conversion path, track input registers, floating-point flags, branch conditions, constants, and the converted integer through all subsequent stores. The current dominator report alone cannot prove that a guard is semantically effective.
3. **Resolve structure and allocation invariants.** Trace the count passed into `_aa_add_edges`, the size/capacity calculations in `_aa_new_edge`, and every write to the allocated edge record. Record offsets and widths from disassembly; do not infer structure layouts from names alone.
4. **Trace path-data provenance.** Inspect the public API and parsing entry points as separate hypotheses. For each path, require evidence of command-length validation, element-count derivation, pointer advancement, and the call chain into the captured rendering callbacks. A public symbol's presence in the symbol table is not proof that it reaches this path.
5. **Compare paired paths in both builds.** Match functions by symbol and instruction context, not by reusing absolute shared-cache addresses. Preserve raw addresses and section-relative annotations separately.
6. **Keep the CVE claim gated.** Apple's advisory identifies CVE-2026-86950 as a CoreGraphics out-of-bounds write addressed by improved bounds checking and warns of possible targeted exploitation. It does not identify `_aa_lineto` as the vulnerable routine. Function-level attribution remains open until primary-source or end-to-end invariant evidence connects the patch to this exact path.

## Acceptance criteria for stronger conclusions

Do not mark a candidate as confirmed until the evidence set shows all of the following:

- the relevant target/fixed instruction difference is reproducible and tied to verified build provenance;
- the compared instructions are in the same semantic path, including clipping/non-clipping distinctions;
- the input's origin and validation boundary are documented;
- the value/count/pointer flow reaches the relevant operation without an intervening proven invariant;
- the specific write and its destination extent are identified, and the violated bound is demonstrated from static evidence or a safe, authorized test harness;
- the attribution to CVE-2026-86950 is supported independently of the mere presence of a patch-version difference.

## Sources and artifacts

- [CoreGraphics comparison workflow run 169](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40240737732)
- [Apple security advisory for CVE-2026-86950](https://support.apple.com/en-us/149226)
- [Apple security releases index](https://support.apple.com/en-us/100100)

This note is a review checklist and evidence boundary, not a claim that the vulnerability, exploitability, or a jailbreak has been reproduced.
