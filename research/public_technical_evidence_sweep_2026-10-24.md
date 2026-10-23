# Public technical-evidence sweep for all 12 candidates — 2026-10-24

## Outcome

Reviewed the public Apple iOS 26.7/iPadOS 26.7 bulletin and accessible NVD/vendor summaries for the 12-candidate set. The sources establish impact statements and broad fix classes, but the reviewed public material does not supply source diffs, affected function names, a reproducer, or sufficient patch detail to establish a working exploit chain. This report records the best supported next step for each candidate without inferring hidden internals.

Primary sources:
- Apple iOS/iPadOS 26.7 security content: https://support.apple.com/en-us/149041
- NVD CVE-2026-84607: https://nvd.nist.gov/vuln/detail/CVE-2026-84607
- CVE-2026-43689 summary: https://www.tenable.com/cve/CVE-2026-43689

## Candidate-by-candidate public evidence and safe regression target

| CVE | Public evidence currently established | Safe regression specification to write next | Status |
|---|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder race; Apple says improved state management; advisory impact says sandboxed app may execute code with kernel privileges. NVD shows high complexity and local access in CISA-ADP vector. | State-machine invariant: concurrent operations must not observe or use stale/inconsistent encoder state. Test only against a mock/model with deterministic scheduling; no device trigger. | Public impact confirmed; exact invariant and build applicability unresolved. |
| CVE-2026-43689 | Kernel permissions issue; additional restrictions; malicious app may gain root privileges. | Authorization invariant: every privileged operation must enforce the intended caller/entitlement/credential check on every path. Model tests only; no privilege attempt. | Impact summary confirmed; changed check/path unresolved. |
| CVE-2026-84523 | APFS out-of-bounds write; bulletin describes bounds-checking class of fix. | Bounds invariant: lengths and offsets are validated before indexing/writing; negative/overflow/edge cases rejected in a standalone model. | Exact affected APFS path and controllability unresolved. |
| CVE-2026-86876 | CoreMedia out-of-bounds write; reported sandbox restriction bypass. | Media parser must validate sizes and preserve sandbox policy; use benign malformed-input unit cases against a mock parser, not a crafted exploit. | Trigger and patch invariant unresolved. |
| CVE-2026-86886 | TCC path traversal; improved input validation; impact may permit protected system-file modification. | Canonical-path and authorization invariant: path normalization cannot escape approved roots, and authorization applies to the final resolved object. Use a temporary test directory only. | Exact path and file boundary unresolved. |
| CVE-2026-84566 | Kernel memory handling; possible termination or kernel-memory corruption; improved memory handling. | Object lifetime/ownership model must reject invalid transitions and double use. Unit-test a mock allocator/state model only. | Exact memory invariant unresolved. |
| CVE-2026-43687 | Malicious NFS server may disclose kernel memory; improved memory handling. | Protocol response data must not expose uninitialized bytes; model test verifies output buffers are initialized before serialization. No malicious NFS server or target-device test. | NFS precondition and disclosure impact established; exact source unresolved. |
| CVE-2026-43684 | Kernel use-after-free; possible termination or kernel-memory corruption; improved memory management. | Lifetime invariant: freed objects cannot be dereferenced and references are invalidated before reclamation. Mock ownership model only. | Object type and trigger unresolved. |
| CVE-2026-43686 | NFS use-after-free; malicious NFS server can lead to kernel-memory corruption; improved memory management. | NFS state machine must not retain references past object lifetime. Test a model with synthetic state transitions, not a live hostile server. | NFS precondition established; object and trigger unresolved. |
| CVE-2026-65405 | Kernel memory initialization issue; app may determine kernel memory layout. | Information-flow invariant: uninitialized/pointer-bearing kernel data must not cross a user-visible boundary. Unit-test serialization with sentinel bytes. | Exact leak source and usefulness unresolved. |
| CVE-2026-84622 | Root-privileged app may read uninitialized kernel memory; improved memory handling. | Initialization invariant: data returned from a kernel-facing API must be fully initialized before readout. Model tests only. Root is already a stated prerequisite, so not established as an initial entry point. | Root prerequisite and disclosure impact established; source unresolved. |
| CVE-2026-28968 | Kernel out-of-bounds write; possible termination or kernel-memory corruption; improved bounds checking. | Bounds invariant: write range must fit the allocated object after checked arithmetic; test boundary cases in a standalone model. | Exact object/path and controllability unresolved. |

## What this does and does not establish

- The public advisory supports the impact and broad fix-class descriptions above.
- It does not reveal enough patch-level detail to name the changed function or prove a particular invariant was the original defect. The regression targets above are defensive specifications derived from the stated bug class, not claims about Apple's actual source patch.
- Version-range data says 26.6.1 falls below NVD's upper bound excluding 26.7. It does not independently prove exact build 23G83 is vulnerable.
- No candidate has been demonstrated to be reproducible or composable into a jailbreak.
- No exploit was run; no device was accessed or modified.

## Next deliverable

Implement a small, platform-independent regression-specification suite for these classes using mock objects and synthetic inputs (state transitions, bounds arithmetic, path normalization, initialization, and lifetime checks). It should not contain iOS exploit triggers, kernel primitives, payloads, or privilege-bypass logic. If public patch diffs or researcher write-ups appear later, update a candidate only with a direct citation and precise claim.
