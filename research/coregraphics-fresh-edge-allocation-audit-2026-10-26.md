# Fresh CoreGraphics edge-allocation audit — 2026-10-26

## Evidence provenance

- Comparison workflow run: [40289913764](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40289913764)
- Workflow head commit: `194c59aa27d3caff5990db2d6e93ca772ea85692`
- Comparison artifact: `coregraphics-build-comparison` (artifact ID `12636176710`)
- Diagnostic artifact: `coregraphics-comparison-diagnostics` (artifact ID `12636695003`)
- Target: iOS 26.6.1 / 23G83; reference: iOS 26.7.1 / 23H30
- Workflow result: success; 25 shared `aa_*` symbols compared; 15 normalized streams differ; zero disassembly failures.
- The artifact now contains addressed instruction arrays for both target and reference `_aa_new_edge` (37 instructions each). This is the first run after the preservation regression test and workflow refresh change.

## Direct observations

### `_aa_new_edge`

The normalized target and reference instruction streams are identical (37 instructions each). In the target build, the relevant sequence is:

- Loads a state pointer from `[x0, #0xc0]`; reads two 32-bit fields at offsets `+0x8` and `+0xc`.
- Computes a required count and compares it with the stored capacity.
- On growth, doubles the capacity and computes a byte count using a `0x60` stride, then calls an allocator-like routine at `0x186bef3f0`.
- If that call returns null, branches to the common epilogue and returns null.
- On success, links the new allocation into state, stores the capacity/count metadata, and computes a record address using `base + (count - 1) * 0x60`.
- Initializes fields beginning at record offset `0x18`; returns the record pointer.

This supports a record stride of 96 bytes and a null-return failure path. It does **not** identify the allocator's contract, prove the actual allocation size after allocator-specific rounding, or establish that any write exceeds the allocated object.

### `_aa_add_edges`

The target and reference normalized instruction streams are identical (138 instructions each). The function calls `_aa_new_edge` and checks the returned pointer for null before writing. On the successful path, observed writes include:

- `stp w23, w25, [x0, #0x20]`
- `strb w8, [x0, #0x2f]`
- `strh w8, [x0, #0x2c]`
- `stp w21, w26, [x0, #0x10]` or the reversed-endpoint variant
- `stp w22, w28, [x0, #0x18]` or the reversed-endpoint variant

The highest directly observed byte written here is offset `0x2f), within a `0x60)-byte stride if the record pointer and allocation layout are as inferred. The instruction stream alone does not prove the backing allocation remains valid in all states.

### `_aa_lineto` conversion path

The target build contains a reachable vector conversion at `0x18430acc8`:
`fcvtzs v0.2d, v0.2d`, followed by `xtn v0.2s, v0.2d` at `0x18430accc`. The CFG audit found no dominating self-compare/NaN guard or clamp-constant reference for that conversion. The reference build has scalar conversions in a longer path with NaN branches and references to the constants at `__TEXT,__const` section offset `0x5a78` and its companion at `0x5a80`; the constant-validation artifact confirms the referenced clamp value `-1073737729.0` matches expected bytes.

The CFG audit is a structural approximation based on disassembly and direct branch labels; it does not prove semantic equivalence or execution reachability from a public API input.

## Interpretation

The new evidence narrows the hypothesis: the candidate discrepancy is upstream in coordinate conversion/validation, not a demonstrated difference in the `_aa_new_edge` allocation routine or the `_aa_add_edges` record writes. Both edge-management functions have identical normalized streams across these two builds, and the observed writes fit within the inferred record stride. A malformed or out-of-range coordinate could still influence arithmetic that feeds edge construction, but this audit does not establish an out-of-bounds write, a reachable crash, or a complete exploit chain.

Also, the target/reference comparison spans iOS 26.6.1 to 26.7.1, while the public research lead describes the 26.7 to 26.7.1 fix. Differences may include unrelated changes between those builds. Do not attribute the entire diff to CVE-2026-86950.

## Next evidence needed

1. Resolve the allocator call contract and the object layout behind the state pointer at offset `0xc0`, using available symbols/metadata and call-site context.
2. Trace the converted coordinates into the exact arithmetic used by `_aa_add_edges` (including signed overflow, divide-by-zero, and count/capacity invariants) without executing a crafted input.
3. Validate whether every relevant conversion path in the reference build is guarded, especially vector lanes and branch joins; refine CFG handling where cut-set coverage is incomplete.
4. Establish the exact 26.7 versus 26.7.1 function delta, if matching firmware artifacts can be sourced, before attributing the patch to this candidate.
5. Keep runtime exploitation and device-facing tests out of this evidence-only audit until the static chain is independently demonstrated and an authorized safe test plan exists.
