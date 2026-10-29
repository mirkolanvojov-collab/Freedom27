# CVE-2026-86950: floating-point conversion guard analysis

Date: 2026-10-25

## Evidence sources

This is a read-only review of the CoreGraphics comparison artifact from [workflow run 40195214425](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40195214425), comparing target iOS 26.6.1 build 23G83 against fixed reference iOS 26.7.1 build 23H30. The report compares 25 shared `aa_*` symbols; 15 normalized instruction streams differ.

Apple's [iOS 26.7.1 security advisory](https://support.apple.com/en-us/149226) identifies CVE-2026-86950 in CoreGraphics as an out-of-bounds write addressed with improved bounds checking. It says processing a maliciously crafted file may lead to arbitrary code execution and notes a report of exploitation against targeted individuals on earlier iOS versions.

A public technical analysis, [“CVE-2026-86950: The Great Glyph Grift” by Calif](https://calif.io/research/the-great-glyph-grift) (30 September 2026), independently reports that patch analysis found a floating-point-to-fixed-point coordinate conversion error in CoreGraphics path scan conversion, with a compiler-optimization-related unit conversion issue that can cause an undersized allocation followed by out-of-bounds drawing writes. The article describes a malicious PDF/font rendering path. This substantially strengthens the relevance of the conversion-guard pattern below, but does not by itself prove that every observed change in this specific target/reference pair has the same cause.

## Static comparison lead

The fixed-reference disassembly contains repeated guard sequences around floating-point calculations and conversion to integer coordinates that are absent from the corresponding target instruction stream in several changed functions:

- A self-compare such as `fcmp d0, d0`, followed by a conditional branch on the floating-point unordered/NaN condition (commonly `b.vs`).
- Loads of constants through fixed-reference `__TEXT,__const` references, then floating-point comparisons and conditional branches.
- `fcvtzs` conversions to integer coordinates occur after these checks in the fixed-reference code.

The clearest examples are:

| Function | Target instructions | Fixed-reference instructions | Observed delta |
|---|---:|---:|---|
| `_aa_moveto` | 86 | 122 | Fixed adds NaN/range-check branches around both coordinate conversions; target converts calculated doubles directly with `fcvtzs`. |
| `_aa_lineto` | 113 | 163 | Fixed adds floating-point range handling and additional conversion paths; target has a shorter conversion path. |
| `_aa_clip_edge` | 162 | 280 | Fixed adds repeated checks around calculated edge coordinates before integer conversion and storage. |
| `_aa_clipping` | 120 | 178 | Fixed adds floating-point self-comparisons and range checks in coordinate-related logic. |
| `_aa_rectat` | 164 | 221 | Fixed adds repeated floating-point checks in coordinate handling. |
| `_aa_cubeto` | 313 | 336 | Fixed adds floating-point checks in a coordinate-related path. |
| `_aa_quadto` | 242 | 269 | Fixed adds floating-point checks in a coordinate-related path. |

These are raw instruction counts from the report, not semantic equivalence scores. Register allocation, function layout, compiler transformations, and changed call conventions can account for some differences. The guard pattern and independent technical write-up are more informative than function-size deltas.

## Interpretation and confidence

The new public technical analysis corroborates the general hypothesis that the relevant patch concerns floating-point coordinate conversion in CoreGraphics path scan conversion. The added checks in the fixed-reference disassembly are consistent with guarding invalid or out-of-range coordinates before narrowing them to integers. The target disassembly's shorter conversion paths are a focused candidate for the same class of defect.

Still, this comparison is not a complete reproduction or a proof that each changed function is vulnerable. The public write-up's analysis and the binaries in this repository are separate evidence streams; exact function correspondence, constant values, and the affected bounds invariant must be verified before asserting an exact instruction-level mapping. Static differences alone do not establish input reachability or exploitability.

## Next validation steps

1. Extract and verify the numeric values of constants loaded from the fixed binary's `__TEXT,__const` section; do not infer their meaning from offsets alone.
2. Trace each check's ARM64 condition-code/control-flow path to the associated `fcvtzs` and subsequent stores.
3. Compare the conversion sequence and bounds invariant across all coordinate-producing entry points and any shared helper paths.
4. Reconcile this target/reference pair against the public technical analysis while preserving exact build provenance and hash checks.
5. Keep the conclusion at “strongly corroborated static patch lead” until the constants and control flow are independently verified.

No crafted input was used, no binary was executed, and no device was accessed or modified.
