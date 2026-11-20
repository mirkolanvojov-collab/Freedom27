# Coordinate narrowing and downstream edge arithmetic audit — 2026-10-26

## Evidence provenance

- Source comparison: [workflow run 40289913764](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40289913764), commit `194c59aa27d3caff5990db2d6e93ca772ea85692`.
- Artifact: `coregraphics-build-comparison`, artifact ID `12636176710`; `coregraphics-function-diff.json` and `coregraphics-conversion-cfg-audit.json`.
- Target: iOS 26.6.1 / build 23G83; reference: iOS 26.7.1 / build 23H30.
- This is a static disassembly audit only. No binary execution, crafted font/PDF, or device interaction was performed.

## Key finding: vector 64-bit conversion followed by 32-bit narrowing

In target `_aa_lineto`, the unclipped path at these addresses computes two double-precision coordinate values, then converts and narrows them:

| Address | Instruction |
|---|---|
| `0x18430acb8` | `ld1r {v0.2d}, [x8]` |
| `0x18430acbc` | `ldr q1, [x19, #0x80]` |
| `0x18430acc0` | `str q17, [sp, #0x20]` |
| `0x18430acc4` | `fmla v0.2d, v17.2d, v1.2d` |
| `0x18430acc8` | `fcvtzs v0.2d, v0.2d` |
| `0x18430accc` | `xtn v0.2s, v0.2d` |
| `0x18430acd0` | `str d0, [sp, #0x38]` |
| `0x18430ace0` | `bl _aa_add_edges` |

`FCVTZS Vd.2D, Vn.2D` produces signed 64-bit integer lanes from the double lanes. `XTN Vd.2S, Vn.2D` then narrows each 64-bit lane to its low 32 bits; it does not perform a signed-range clamp to the 32-bit interval. Therefore, for finite converted values whose integer magnitude exceeds the signed 32-bit range but remains representable in signed 64 bits, the narrowing step can yield a different signed 32-bit coordinate than a range-clamped conversion. This is an instruction-semantics observation, not proof that arbitrary values can reach this path from a public API.

The target path has no clamp loads or self-compare NaN guard dominating the vector conversion in the current CFG audit. The fixed reference instead has scalar coordinate conversion paths that compare against constants at `__TEXT,__const` offsets `0x5a78` and `0x5a80`, handle unordered/NaN cases, and clamp before `fcvtzs wN, dN` (32-bit conversion). The constant-validation artifact confirms these are `-1073737729.0` and `+1073737729.0`.

## Why the clamp bound is relevant downstream

In `_aa_add_edges`, the candidate coordinate pairs are subtracted using 32-bit operations before the results are sign-extended and used in division/edge interpolation. For example:

- `sub w8, w27, w21` at target `0x18430a9a0`;
- `subs w12, w28, w22` at target `0x18430a974`;
- `sbfiz x10, x8, #0xc, #0x20` at target `0x18430a9dc`;
- `sxtw x9, w12` and `sdiv x25, x10, x9` at `0x18430a9e0`–`0x18430a9e8`.

The reference build has the same normalized `_aa_add_edges` stream and the same `_aa_new_edge` stream. `_aa_new_edge` computes allocation bytes from a capacity multiplied by the 96-byte record stride, plus a 24-byte header; it checks the allocator return before updating the list and returning a record. The observed edge-record writes are within offsets `0x10` through `0x2f) of that inferred 96-byte record.

The reference clamp magnitude is just below (2^{30}), so a difference between two clamped endpoints stays within signed 32-bit range. Without a corresponding pre-narrowing range restriction, the target's narrowing can map a large converted coordinate to a different 32-bit value, and 32-bit subtraction may also overflow for some coordinate pairs. The downstream arithmetic is therefore a plausible corruption point to analyze, but the static evidence does not establish that it reaches an invalid allocation, writes out of bounds, or is attacker-controllable.

## What this establishes — and what it does not

Established from the current artifact:
1. The target path uses vector FP64-to-signed-64 conversion followed by low-32-bit narrowing.
2. The compared reference paths include NaN/range handling and 32-bit conversion after clamping.
3. Edge allocation and edge-record construction have identical normalized streams in these two builds.
4. The downstream edge arithmetic performs 32-bit coordinate subtraction and derives interpolation values from those differences.

Not established:
- Exact reachability from any particular public CoreGraphics API and input encoding.
- Complete register/dataflow semantics for both vector lanes through clipping, coordinate transforms, and the caller.
- A confirmed divide-by-zero, invalid record count, undersized allocation, or out-of-bounds write.
- That these differences were introduced specifically by CVE-2026-86950; the compared builds are 26.6.1 and 26.7.1, while the public lead describes the 26.7 to 26.7.1 patch.

## Next work

1. Extend the static analyzer to explicitly report FP64-to-int64 vector conversions followed by narrowing, and add regression tests for this instruction pattern.
2. Trace the two lanes from the coordinate calculation into `_aa_add_edges`, including path conditions and all writes, while marking unresolved dataflow rather than guessing.
3. Seek a verifiable iOS 26.7 CoreGraphics artifact to compare against 26.7.1 for patch attribution.
4. Keep any runtime testing outside this audit unless there is an authorized, isolated test plan; do not treat the static candidate as a proven exploit.
