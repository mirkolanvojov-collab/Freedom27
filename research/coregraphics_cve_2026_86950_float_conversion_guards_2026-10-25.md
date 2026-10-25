# CVE-2026-86950: candidate floating-point conversion guard changes

Date: 2026-10-25

## Evidence source

Read-only review of the CoreGraphics comparison artifact from [workflow run 40195214425](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40195214425), using target iOS 26.6.1 build 23G83 and fixed reference iOS 26.7.1 build 23H30. The report compares 25 shared `aa_*` symbols; 15 normalized instruction streams differ. This note records a more specific static lead, not an exploitability conclusion.

Apple's [iOS 26.7.1 security advisory](https://support.apple.com/en-us/149226) identifies CVE-2026-86950 in CoreGraphics as an out-of-bounds write addressed with improved bounds checking. Apple says processing a maliciously crafted file may lead to arbitrary code execution and that a report of exploitation against targeted individuals existed on earlier iOS versions.

## Strongest current static lead

The fixed-reference disassembly contains repeated guard sequences around floating-point calculations and conversion to integer coordinates that are absent from the corresponding target instruction stream in several changed functions:

- A self-compare such as `fcmp d0, d0`, followed by a conditional branch on the floating-point unordered/NaN condition (commonly `b.vs`).
- Loads of constants through fixed-reference `__TEXT,__const` references, then floating-point comparisons and conditional branches.
- `fcvtzs` conversions to integer coordinates occur after these checks in the fixed-reference code.

The clearest examples are:

| Function | Target instructions | Fixed-reference instructions | Observed delta |
|---|---:|---:|---|
| `_aa_moveto` | 86 | 122 | Fixed adds NaN/range-check branches around both coordinate conversions; target converts the calculated doubles directly with `fcvtzs`. |
| `_aa_lineto` | 113 | 163 | Fixed adds floating-point range handling and additional conversion paths; target has a much shorter conversion path. |
| `_aa_clip_edge` | 162 | 280 | Fixed adds repeated checks around calculated edge coordinates before integer conversion and storage. |
| `_aa_clipping` | 120 | 178 | Fixed adds floating-point self-comparisons and range checks in coordinate-related logic. |
| `_aa_rectat` | 164 | 221 | Fixed adds repeated floating-point checks in coordinate handling. |
| `_aa_cubeto` | 313 | 336 | Fixed adds floating-point checks in a coordinate-related path. |
| `_aa_quadto` | 242 | 269 | Fixed adds floating-point checks in a coordinate-related path. |

These counts are raw instruction counts from the report, not semantic equivalence scores. Register allocation, function layout, compiler transformations, and changed call conventions can account for some differences. The specific guard patterns are more informative than function-size deltas, but still need corroboration.

## Interpretation

This is a credible lead for review because it is consistent with Apple's broad description of an out-of-bounds write fixed by improved bounds checking: the fixed binary appears to validate computed floating-point coordinates before narrowing them to integer values, while the target binary has direct conversion sequences in corresponding paths.

It is **not yet proven** that these instructions implement CVE-2026-86950. The public Apple advisory does not name the affected function or disclose the exact bounds invariant. The `aa_*` symbol names and instruction differences alone cannot establish a vulnerable write, input reachability, exploitability, or a complete chain.

## Next validation steps

1. Independently verify the constants loaded from the fixed binary's `__TEXT,__const` section and their numeric values; do not infer their meaning from offsets alone.
2. Compare control-flow paths from each check to the associated `fcvtzs` and subsequent stores, accounting for ARM64 condition-code semantics.
3. Check whether the guard cluster is consistently added across all coordinate-producing entry points and whether the same invariant is applied in the target's shared helper paths.
4. Seek a primary technical disclosure or reproducible non-weaponized analysis tying these exact checks to CVE-2026-86950.
5. Preserve the conclusion as “candidate patch pattern” until these checks are completed.

No crafted input was used, no binary was executed, and no device was accessed or modified.
