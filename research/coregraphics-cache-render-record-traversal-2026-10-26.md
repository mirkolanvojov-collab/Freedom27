# CoreGraphics `_aa_cache_render` record-traversal audit

**Date:** 2026-10-26  
**Evidence:** preserved run-169 artifact `coregraphics-function-diff.json`  
**Target:** iOS 26.6.1 (23G83); **reference:** iOS 26.7.1 (23H30)  
**Method:** read-only review of normalized and addressed instruction records. No binary execution or crafted-input testing.

## Result

The two `_aa_cache_render` streams each contain 664 instructions, but are not identical: the artifact records nine position-wise mismatches. The loop reviewed at normalized indices 242–309 is instruction-for-instruction the same after layout normalization, including both uses of a `0x60` stride. Its visible operations are more consistent with traversal and link maintenance over fixed-size records than with a direct coverage-buffer sizing calculation.

### First traversal

At indices 242–260, the code loads a pointer from `[x19, #0xc0]`, checks it for null, loads a count-like field from `[x25, #0xc]`, subtracts one, multiplies by `0x60` using `umull`, and adds the product to `x25`. It reads a field at record offset `0x30`, shifts it right by 12, compares the derived value against `w28`, then accesses an index table through `[x20, w8, sxtw #3]`. The subsequent stores update a pointer at offset `0x18` and the corresponding table slot.

### Second traversal

At indices 282–297, the same count-minus-one and `0x60` multiplication pattern is used. The code computes an address with an additional `0x78` offset, reads a field at `-0x48`, derives and checks an index, updates a pointer link, and adjusts a double-width value at `-0x50`. The loop then steps by `0x60` and follows a pointer loaded from the record.

These instruction patterns support a cautious interpretation of fixed-stride record traversal and index/link updates. They do **not** establish the exact record type, count origin, allocation extent, or index-table bounds. They also do not connect this count to the coverage buffer described in public CVE analysis.

## Cross-build comparison

The normalized instructions in the two loop windows are identical. Nearby differences include:
- the `add x23` immediates at indices 247, 279;
- the `add x26` immediate at indices 249, 281;
- the entry/epilogue global-reference offsets `0xc30` versus `0xc58`;
- other differences elsewhere in the function, including indirect-call slots and a vector-data load.

The `x23`/ `x26` address differences are unresolved references, not proven relocations. They should not be classified as harmless until exact-build symbol/relocation data is available. The vector-data load resolves to the same section-relative offset in the current audit, but its bytes have not been compared.

## Related invariant

The paired `_aa_add_edges` streams are identical at 138 normalized instructions. Its inspected instructions allocate an edge through `_aa_new_edge`, check the returned pointer for null, and write fields at offsets such as `0x10`, `0x18`, `0x20`, `0x2c`, and `0x2f`. This shows record-field writes after a successful allocation call, but the saved artifact does not establish allocation size, the complete record layout, or the caller's capacity invariants. The `_aa_new_edge` record contains counts and hashes only, not its instruction body, so allocator semantics cannot be reconstructed from this artifact alone.

## Next evidence required

1. Capture the exact-build `_aa_new_edge` disassembly and its allocation call arguments/return behavior.
2. Resolve the owner and extent of the `[x19, #0xc0]` object and the index table based at `x20`.
3. Trace the count at `[x25, #0xc]` back to its initialization and validation; establish the allocated extent of the `0x60`-stride records.
4. Separately identify the coverage-buffer allocation and writes, then determine whether a proven data-flow link connects the record traversal or edge bounds to that buffer.
5. Resolve exact-build global/constant references before assigning semantics to the remaining nine stream differences.

## Conclusion

This audit narrows the interpretation of the repeated `0x60` arithmetic: it is a credible record-traversal lead, not proof of the coverage-buffer allocation path or an out-of-bounds write. The local comparison remains a 26.6.1-to-26.7.1 binary comparison and does not by itself attribute every change to CVE-2026-86950.
