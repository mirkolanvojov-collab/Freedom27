# Line-render conversion and instruction-delta review (2026-11-05)

Source: `coregraphics-26-7-function-diff.json` from successful [run 41905970197](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197), [artifact 13362383025](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362383025). Compared each target/fixed normalized instruction array with an exact sequence diff (`SequenceMatcher(autojunk=False)`); instruction indexes below are zero-based. This is textual comparison, not dataflow verification.

## `_aa_line_render`
217 instructions in each build; one changed instruction at index 37:
- 23H24: `ldr d8, [x8, #0x130]`
- 23H30: `ldr d8, [x8, #0x6f0]`

The sole `fcvtzs` is at index 25 in both arrays, and its immediate surrounding sequence is identical:
`ldr s0, [x20, #0x94]`; `mov w8, #0x47800000`; `fmov s1, w8`; `fmul s0, s0, s1`; `fabs s0, s0`; `fcvtzs w8, s0`; `cmp w8, #0x10, lsl #0xc`; `mov w9, #0x10000`; `csel w8, w8, w9, cc`; `str w8, [x20, #0x68]`.

## `_aa_line_render_shape`
509 instructions in each build; seven changed single instructions, at indexes 75, 94, 311, 340, 468, 483, 487. Changes are immediate/displacement operands only:
- 75: `add x0, x0, #0xb7a` → `add x0, x0, #0x13a`
- 94: `ldr d11, [x8, #0x130]` → `ldr d11, [x8, #0x6f0]`
- 311: `add x0, x0, #0xb5a` → `add x0, x0, #0x11a`
- 340: `ldr d1, [x8, #0xc00]` → `ldr d1, [x8, #0x1c0]`
- 468: `add x0, x0, #0xb52` → `add x0, x0, #0x112`
- 483 and 487: `add x0, x0, #0xb5a` → `add x0, x0, #0x11a`

The sole `fcvtzs` is at index 39 on both sides, with an identical surrounding sequence: `mov w8, #0x47800000`; `fmov s0, w8`; `fmul s0, s10, s0`; `fabs s0, s0`; `fcvtzs w8, s0`; `cmp w8, #0x10, lsl #0xc`; `mov w9, #0x10000`; `csel w8, w8, w9, cc`; `str w8, [x20, #0xc0]`.

## Assessment
Both conversion sequences are unchanged in these two functions between 23H24 and 23H30. The changed load offsets and address immediates may reflect changed constant-pool or code layout; their referents were not resolved, so do **not** label them definitively layout-only or semantically equivalent. The presence of `fcvtzs` is not proof of an unpatched vulnerability, and this review does not certify full safety. Neither function currently provides direct evidence of a newly inserted coordinate clamp at its conversion site. The seven-function CFG audit remains the stronger static patch evidence.

No exploit execution, runtime input testing, or device modification was performed.
