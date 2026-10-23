# Public patch evidence and safe regression specifications — 2026-10-24

## Scope and source quality

This pass covers all 12 candidates from the existing Freedom27 ledger. Public-source checks were performed against Apple's iOS 26.7 / iPadOS 26.7 security bulletin and the NVD records. Apple's bulletin is the primary source for the issue summary and fix wording; the NVD record is a secondary index. Public source code diffs, function names, and reproducer details were not found in the checked public material. The absence of a public diff is not evidence that no private or unpublished diff exists.

Primary source: https://support.apple.com/en-us/149041
NVD example: https://nvd.nist.gov/vuln/detail/CVE-2026-84607

## Per-candidate evidence and safe regression specification

The following specifications define a security property to test in a vendor-controlled harness or abstract model. They intentionally omit exploit triggers, payloads, race choreography, memory-corruption instructions, and device-specific attack steps.

| CVE | Public fix wording / impact | Safe regression property | Evidence still missing |
|---|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder race; improved state management; sandboxed app may execute code with kernel privileges | State transitions must be serialized or validated so concurrent lifecycle changes cannot violate authorization or object-state invariants | Affected state machine/function, patch diff, build-specific reachability, reproduction evidence |
| CVE-2026-43689 | Kernel permissions; additional restrictions; malicious app may gain root privileges | Privileged operations must reject callers lacking the documented entitlement/authorization context on every entry path | Exact authorization check, caller context, patched code path, build-specific verification |
| CVE-2026-84523 | APFS out-of-bounds write; improved bounds checking; system termination or kernel-memory write possible | Every length/offset pair must be validated against the actual destination capacity before write; boundary and integer-overflow cases must reject safely | Exact APFS operation and field, patch diff, controlled regression fixture |
| CVE-2026-86876 | CoreMedia out-of-bounds write; sandbox restriction bypass reported in candidate ledger | Media processing must preserve process sandbox policy and validate buffer bounds on all parsing branches | Public wording/function mapping needs reconciliation against primary bulletin; patch diff and path details |
| CVE-2026-86886 | TCC path traversal; improved path validation; protected-file modification reported in candidate ledger | Authorization must apply to the canonical resolved target, not only the unnormalized input path; traversal must not cross protected roots | Exact path-handling function, primary advisory wording, patch diff, supported test fixture |
| CVE-2026-84566 | Kernel memory handling; improved memory handling; termination or kernel-memory corruption | Object lifetime and ownership invariants must hold across cleanup and error paths; invalid state must fail closed | Exact object/type and patch diff; whether impact exceeds denial of service |
| CVE-2026-43687 | Kernel/NFS; malicious NFS server may disclose kernel memory; improved memory handling | Network-derived response data must not expose uninitialized or out-of-scope kernel data; all output fields must be initialized and bounded | Exact NFS path, data source, patch diff; impact remains disclosure, not execution |
| CVE-2026-43684 | Kernel use-after-free; improved memory management; termination or kernel-memory corruption | References must remain valid for the entire operation; cleanup must not free an object while an outstanding reference is in use | Exact object/lifetime invariant, patch diff, reachable caller path |
| CVE-2026-43686 | Kernel/NFS use-after-free; improved memory management; NFS-triggered kernel-memory corruption | NFS request teardown and asynchronous completion must preserve ownership and lifetime invariants | Exact NFS object and lifecycle, patch diff, supported regression fixture |
| CVE-2026-65405 | Kernel memory initialization; app may determine kernel memory layout; improved memory handling | All user-visible outputs must be initialized and must not disclose addresses or bytes outside the authorized output structure | Exact disclosed field/source, patch diff, evidence of practical information content |
| CVE-2026-84622 | Root-privileged app may read uninitialized kernel memory; improved memory handling | Root-context interfaces must initialize all returned bytes before copyout; access checks must remain explicit | Exact interface and returned structure; root prerequisite means not established as an initial privilege-escalation path |
| CVE-2026-28968 | Kernel out-of-bounds write; improved bounds checking; termination or kernel-memory corruption | Validate indices, lengths, and arithmetic before access; out-of-range input must be rejected without modifying adjacent state | Exact data structure/path, patch diff, controlled regression fixture |

## Findings

1. The public Apple bulletin supplies concise fix summaries, not enough implementation detail to name affected functions or reconstruct a patch.
2. A safe test specification can be drafted from each issue class, but it is a proposed invariant—not proof that it reproduces the original flaw or matches Apple's private fix.
3. The previous candidate ledger's descriptions for CVE-2026-86876 and CVE-2026-86886 should be treated as provisional until reconciled line-by-line against the primary Apple entry; this report deliberately calls out that evidence gap rather than elevating the ledger text to confirmed fact.
4. Version-range matching for iOS 26.6.1 is not exact build verification for build 23G83 and is not evidence of exploitability.
5. No public patch diff or independently verifiable reproduction details were established by this pass.

## Priority order for further non-exploitative research

- First: CVE-2026-84607 (race/state-management issue with published kernel-privilege impact) and CVE-2026-43689 (authorization/root impact). Search for a public patch or author write-up; do not attempt to weaponize the bug from advisory text alone.
- Second: CVE-2026-84523, CVE-2026-84566, CVE-2026-43684, CVE-2026-43686, CVE-2026-28968 for memory-safety invariants.
- Third: CVE-2026-86876 and CVE-2026-86886 after the primary advisory mapping is reconciled.
- Fourth: CVE-2026-43687, CVE-2026-65405, CVE-2026-84622, where public impact is information disclosure or a prerequisite makes the issue unsuitable as an initial entry point.

## Safety and verification

Read-only public-source review. No exploit code was run or added. No device was accessed or modified. These specifications are suitable only as a starting point for vendor-controlled unit tests or abstract model checks; they do not establish a working jailbreak chain.
