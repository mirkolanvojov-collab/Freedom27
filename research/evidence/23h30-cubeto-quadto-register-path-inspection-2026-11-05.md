# 23H30 cubeto/qu adto register-path inspection (2026-11-05)

Read-only inspection of the addressed instructions in GitHub Actions artifact 13362383025 (`coregraphics-26-7-function-diff.json`). This is an instruction-level observation, not a full register/flag provenance proof.

## `_aa_cubeto`

- First coordinate: `0x184332254 fcmp d1,d1`; `0x184332258 b.vs 0x184332334`. NaN target `0x184332334 mov w8,#0`; `0x184332338 b 0x184332288`, which is **after** `0x184332278 fcvtzs w8,d1`. Thus this direct NaN branch bypasses the first conversion.
- Second coordinate: `0x184332294 fcmp d0,d0`; `0x184332298 str q6,[sp,#0x90]`; `0x18433229c b.vs 0x18433233c`. Target `0x18433233c mov w8,#0`; `0x184332340 b 0x1843322c4`, **after** `0x1843322c0 fcvtzs w8,d0`. The intervening `str` means this pair fails the analyzer's *immediate adjacency* candidate rule, even though the branch target bypasses conversion. Determining whether the `str` preserves NZCV is a separate architecture-semantics check.

## `_aa_quadto`

- First coordinate: `0x18433b9cc fcmp d1,d1`; `0x18433b9d0 b.vs 0x18433baac`. Target `0x18433baac mov w8,#0`; `0x18433bab0 b 0x18433b9f8`, **after** `0x18433b9e8 fcvtzs w8,d1`.
- Second coordinate: `0x18433ba04 fcmp d0,d0`; `0x18433ba08 str q6,[sp,#0x30]`; `0x18433ba0c b.vs 0x18433bab4`. Target `0x18433bab4 mov w8,#0`; `0x18433bab8 b 0x18433ba34`, **after** `0x18433ba30 fcvtzs w8,d0`. Again, the `str` breaks the analyzer's adjacency heuristic.

## Important interpretation

The previously reported zero accepted candidate count for both conversions in each function does **not** establish that the NaN branches lead to conversion. The first-coordinate NaN successors visibly skip their corresponding conversion, but a later second-coordinate conversion remains reachable. The analyzer's candidate logic tests reachability to each conversion from *every* NaN successor and does not track which floating-point register is guarded. This can reject a legitimate first-coordinate guard because a path later reaches the distinct second-coordinate conversion. The second-coordinate branches have an intervening store and are omitted by the strict adjacency heuristic.

This explains specific conservative-analysis false-negative mechanisms in the four cases, but is not a formal proof of protection or exploitability. Further work: add per-register, flag-clobber-aware diagnostics with tests before changing coverage semantics. No device was accessed.
