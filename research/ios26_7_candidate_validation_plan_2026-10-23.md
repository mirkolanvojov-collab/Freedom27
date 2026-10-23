# Freedom27 — candidate validation plan (read-only, no exploit execution)

**Date:** 2026-10-23  
**Target reported by user:** iPhone 16 Plus, `iPhone17,4`, iOS 26.6.1, build `23G83`  
**Primary source:** Apple, *About the security content of iOS 26.7 and iPadOS 26.7*: https://support.apple.com/en-us/149041  
**Baseline source:** Apple, *About the security content of iOS 26.6.1 and iPadOS 26.6.1*: https://support.apple.com/en-us/148282  
**Execution status:** no CVE cracked, no exploit executed, no device accessed or modified.

## Scope and limits

This plan turns the public advisory leads into a repeatable evidence workflow. It does not contain an exploit, payload, kernel write primitive, sandbox escape procedure, or instructions to bypass iOS protections. A CVE appearing in a later advisory is not proof that the earlier target build is vulnerable; it is only a reason to investigate public patch evidence.

Apple's 26.7 advisory is dated September 14, 2026, and lists iPhone 11 and later for the cited components, which includes the reported device family. That hardware support statement is not a vulnerable-version statement. Each candidate needs separate evidence for affected versions and exact build applicability.

## Candidate-by-candidate work queue

| Candidate | Publicly stated impact | Safe next action | Do not infer |
|---|---|---|---|
| CVE-2026-84607 — AVEVideoEncoder | Sandboxed app may execute arbitrary code with kernel privileges; race condition fixed by improved state management | Search for a public bug reference or patch artifact; capture source URL and affected/fixed versions; design a synthetic state-machine regression test if the behavior can be modeled without platform exploitation | That the 26.6.1 build is affected, that the race is controllable, or that kernel code execution is reproducible |
| CVE-2026-43689 — Kernel | App may gain root privileges; additional restrictions added | Record exact Apple advisory section and search public patch/bug references; map the privilege boundary and prerequisites from source evidence | That root implies kernel privilege or a jailbreak |
| CVE-2026-84523 — APFS | App may cause termination or write kernel memory | Search public patch references; distinguish impact wording from demonstrated attacker control; use only synthetic filesystem test cases | That a controllable kernel-write primitive exists |
| CVE-2026-86876 — CoreMedia | Sandbox restrictions may be circumvented | Find exact advisory entry, public fix references, and version boundary; consider parser regression tests using benign synthetic inputs | That a sandbox escape has been reproduced |
| CVE-2026-86886 — TCC | App may modify protected system files; path traversal fixed with input validation | Identify the documented path-validation boundary and required permissions; write ordinary path-validation unit tests against a toy model | That protected-file writes are possible on the target |
| CVE-2026-84566 — Kernel | System termination or kernel-memory corruption; improved memory handling | Search for public technical detail; record preconditions and safe static evidence | That memory corruption gives reliable code execution |
| CVE-2026-43687 — Kernel/NFS | Malicious NFS server may disclose kernel memory | Record network/server prerequisites and whether the target configuration exposes the path; prioritize static documentation over live testing | That a remote or local path is reachable on this device |
| CVE-2026-43684 — Kernel | Termination or kernel-memory corruption; use-after-free fixed | Search public fix references and determine if a non-destructive model-based regression test is possible | That a use-after-free is exploitable |
| CVE-2026-43686 — Kernel/NFS | Malicious NFS server may cause kernel memory corruption; use-after-free fixed | Document NFS prerequisites and affected/fixed version evidence | That this is reachable from an ordinary app |
| CVE-2026-65405 — Kernel | App may determine kernel memory layout; memory initialization fixed | Assess public description and whether it documents a measurable disclosure; build a toy model test only if useful | That a leak bypasses mitigations in the target build |
| CVE-2026-84622 — Kernel | An app with root privileges may read uninitialized kernel memory | Mark as post-root-only; do not rank as initial entry without independent privilege-escalation evidence | That it can obtain root itself |
| CVE-2026-28968 — Kernel | System termination or kernel-memory corruption (per current candidate ledger) | Reconcile the exact advisory section and wording against the Apple page before further assessment | That the current short summary is sufficient technical evidence |

## Evidence record required for each candidate

Create or update a record only when the following fields can be supported:

- `cve_id`
- `apple_advisory_url` and exact section/component
- `advisory_checked_on`
- `published_impact` and `fix_summary` copied or carefully paraphrased from the primary source
- `public_bug_or_patch_url` (null if none found; never guess)
- `affected_version_evidence` and `fixed_version_evidence`
- `target_build_applicability`: one of `supported`, `ruled_out`, or `not_established`, with a source
- `preconditions`: only what public evidence states
- `safe_validation`: static or synthetic test proposal
- `reproduction_status`: `not_attempted`, `safe_model_test_passed`, or `not_reproducible_from_public_evidence`
- `limitations` and evidence gaps

## Validation gates

1. **Source gate:** confirm CVE, component, impact, and fix from Apple's page.
2. **Version gate:** require independent evidence for vulnerable/fixed range; otherwise target applicability stays `not_established`.
3. **Patch gate:** attach a public patch, bug tracker, or source artifact; absence is recorded as an evidence gap.
4. **Precondition gate:** establish required attacker position, process privileges, entitlement, user interaction, and service exposure where documented.
5. **Safe-test gate:** test only benign models or static properties. Do not corrupt kernel memory, modify protected files, escape a sandbox, or run exploit code on the daily-use phone.
6. **Claim gate:** never call a candidate “cracked,” “working,” or “reproduced” without reproducible evidence and logs.

## Current conclusion

The work completed so far is advisory triage, not an exploit. Public advisory summaries identify research leads but do not supply a verified path for the reported build. The next meaningful milestone is a source-backed version/patch record for at least one candidate, followed by a non-destructive regression test where feasible. If no public patch artifact exists, that candidate remains unresolved rather than being filled in by guesswork.
