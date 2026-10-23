# All-priority public advisory reconciliation — 2026-10-24

## Primary-source correction

The current Apple iOS 26.7 / iPadOS 26.7 bulletin is available at https://support.apple.com/en-us/149041. It confirms these entries directly:

- CVE-2026-84607 — AVEVideoEncoder race condition; sandboxed app may execute arbitrary code with kernel privileges; improved state management.
- CVE-2026-43689 — Kernel permissions issue; malicious app may gain root privileges; additional restrictions.
- CVE-2026-84523 — APFS out-of-bounds write; unexpected system termination or kernel-memory write; improved bounds checking.
- CVE-2026-86876 — CoreMedia out-of-bounds write; sandboxed process may circumvent sandbox restrictions; improved bounds checking.
- CVE-2026-86886 — TCC path traversal; app may modify protected system files; improved input validation.
- CVE-2026-84566 — Kernel memory handling; local attacker may cause termination or corrupt kernel memory; improved memory handling.

This resolves the previous uncertainty for CVE-2026-86876 and CVE-2026-86886: their component and high-level impact are explicitly present in Apple's primary bulletin. It does not reveal the exact code path, patch diff, or reproduction conditions.

## Priority work status across all 12 candidates

The following are public-source triage states, not exploitability determinations.

| Priority | CVE(s) | Publicly established | Still not publicly established in this review | Safe validation target |
|---|---|---|---|---|
| P1 | CVE-2026-84607 | AVEVideoEncoder race; kernel-privilege code execution impact; improved state management | Specific state transition, source diff, reproducible affected-build condition | Abstract state-machine regression: invalid or concurrent lifecycle transitions must not violate authorization/state invariants |
| P1 | CVE-2026-43689 | Kernel permission issue; root-privilege impact; additional restrictions | Exact check, caller/entitlement conditions, patch diff | Authorization model test: unauthorized callers remain denied on every entry path |
| P2 | CVE-2026-84523 | APFS out-of-bounds write; bounds-checking fix | Exact APFS operation, size/offset invariant, patch diff | Boundary-value and overflow tests in a vendor-controlled parser/model |
| P2 | CVE-2026-84566 | Kernel memory handling; termination or kernel-memory corruption; improved memory handling | Object/type, lifetime invariant, patch diff | Ownership and error-path tests in a model/unit-test harness |
| P2 | CVE-2026-43684 | Kernel use-after-free as recorded in candidate ledger | Exact object, public patch/source evidence, reachability | Reference lifetime and cleanup-order model tests |
| P2 | CVE-2026-43686 | Kernel/NFS use-after-free/corruption as recorded; NFS context noted in public description | Exact object/path and patch diff | NFS request ownership/lifecycle model tests; no malicious server against a real device |
| P2 | CVE-2026-28968 | Kernel out-of-bounds write as recorded in candidate ledger | Exact structure, invariant, patch diff | Bounds and arithmetic validation model tests |
| P3 | CVE-2026-86876 | CoreMedia out-of-bounds write; sandbox restriction bypass impact | Exact affected parsing path and patch diff | Sandbox policy must remain enforced for media-processing work; bounds tests in a model |
| P3 | CVE-2026-86886 | TCC path traversal; protected-system-file modification impact | Exact path-handling function and patch diff | Authorization against canonical resolved path; traversal tests in a mock filesystem |
| P4 | CVE-2026-43687 | Kernel/NFS memory-disclosure impact as recorded | Exact disclosure source, data structure, patch diff | All output bytes initialized and limited to authorized response fields |
| P4 | CVE-2026-65405 | Kernel memory-layout disclosure impact as recorded | Exact disclosed data and practical utility, patch diff | User-visible outputs do not expose unauthorized kernel addresses/data |
| P4 | CVE-2026-84622 | Root-privileged app may read uninitialized kernel memory as recorded | Exact interface/structure and patch diff | All copyout fields initialized; access checks explicit; root prerequisite means not established as initial entry point |

**Important evidence limit:** The table preserves the existing candidate ledger's summaries for the CVEs where this pass did not independently retrieve a complete Apple advisory entry. Those rows must remain provisional until their specific Apple entries are located and cross-checked. Do not infer a component, impact, or patch detail from a CVE ID alone.

## What was accomplished

1. Checked the primary Apple bulletin and reconciled the two previously flagged mappings (86876 and 86886).
2. Ranked all 12 candidates by public impact and prerequisite considerations for research planning.
3. Converted each candidate into a safe regression-property target without adding exploit triggers, payloads, race choreography, or memory-corruption instructions.
4. Kept the distinction between public impact, version-range match, exact build applicability, and exploitability explicit.

## Next evidence requirement

For each provisional row, locate the exact entry in Apple's primary bulletin or an authoritative CVE Program record and quote/record only the minimum component, impact, fix summary, and publication timestamp needed for traceability. Search for public source diffs or author write-ups only when they are explicitly published. If no public patch-level evidence is available, record `not_publicly_available_in_review` and stop there rather than reverse-engineering a weaponized chain from impact text.

## Safety

This is read-only advisory analysis and abstract regression planning. No exploit was executed, no device was accessed or modified, and no jailbreak functionality is claimed.
