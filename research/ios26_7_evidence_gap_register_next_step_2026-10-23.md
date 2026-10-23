# Freedom27 — next research step: evidence-gap register and candidate gates

**Reviewed:** 2026-10-23  
**Target context:** user-reported iPhone17,4 / iOS 26.6.1 / build 23G83  
**Mode:** public-source, read-only research. No exploit execution, device access, or device modification.

## Why this is the next step

The candidate list is an advisory-derived lead list, not a validated exploit list. The highest-value next action is to resolve evidence gaps in a consistent order before implementation: (1) exact affected-version evidence, (2) public technical/patch evidence, (3) documented prerequisites and trust boundary, and (4) a harmless regression model only where the documented fix can be expressed without reproducing the vulnerability.

Apple's iOS 26.7 advisory is the source for reported impacts and fixes: https://support.apple.com/en-us/149041. The iOS 26.6.1 baseline advisory is https://support.apple.com/en-us/148282. A fixed-release date or device support list alone does not establish that a specific earlier build is affected.

## Ranked evidence queue

Priority means **research value / evidence resolution**, not exploitability.

| Queue | Candidate(s) | Why it is here | Required evidence | Safe next action |
|---|---|---|---|---|
| P0 — resolve version range | CVE-2026-43689, CVE-2026-86876, CVE-2026-86886, CVE-2026-84566, CVE-2026-43687, CVE-2026-43684, CVE-2026-43686, CVE-2026-65405, CVE-2026-84622, CVE-2026-28968 | Current ledger lacks a captured exact affected CPE range | Canonical CVE/NVD record, affected product and bounds, whether 26.6.1 is inside the range | Retrieve exact records individually; mark unavailable/unknown rather than infer from “fixed in 26.7” |
| P0 — reconcile current version claim | CVE-2026-84523 | Ledger records below 26.7 from an earlier NVD review; needs canonical source capture | Exact CPE range and confirmation it applies to iPhone OS rather than a related platform | Re-open canonical NVD record; keep target applicability provisional until source wording is captured |
| P1 — strongest current version evidence | CVE-2026-84607 | NVD range below 26.7 includes version 26.6.1, but exact build and exploitability remain unknown | Preserve canonical NVD configuration; look for public bug/patch references | Model the corrected synchronization invariant only if public documentation grounds the invariant |
| P2 — prerequisites / chain relevance | CVE-2026-84622 | Public impact requires root privileges, so it is not an initial-entry candidate on current evidence | Exact affected range and source-grounded prerequisite wording | Keep out of initial-entry ranking unless separate evidence establishes root acquisition |
| P2 — reachability / threat model | CVE-2026-43687, CVE-2026-43686 | NFS-related impact depends on connecting to a malicious NFS server per advisory wording | Documented prerequisites, availability/configuration requirements, affected range | Static research only; do not use a malicious server against the daily-use device |
| P3 — modelable validation candidates | CVE-2026-86886, CVE-2026-86876, CVE-2026-84607 | Fix summaries suggest input-validation, bounds-checking, or synchronization invariants, but exact internals may not be public | A specific public invariant that can be expressed independently of the vulnerable implementation | Create toy path-normalization/parser/state-machine regression tests; no iOS internals or CVE reproduction |

## Evidence record required for every candidate

Each candidate should record these fields, or explicitly mark them unknown:

- canonical record URL
- Apple advisory URL
- affected product
- affected version range
- whether target version is in range: true, false, or unknown
- exact build verified (currently false for all candidates)
- public patch/bug reference (URL or not found in review)
- prerequisites (source-grounded or unknown)
- trust boundary (source-grounded or unknown)
- safe validation method
- validation status
- what is not proven

Do not mark a candidate as applicable just because it appears in the iOS 26.7 advisory. Missing evidence should remain unknown, not become a positive claim.

## Exit criteria

A candidate moves from **advisory lead** to **version-supported** only when a canonical source supplies an affected range including 26.6.1. Exact build applicability remains unverified unless a source specifically supports it. It moves to **public-fix-understood** only when a patch or reliable public technical reference supports the claimed invariant. A harmless model test validates the model property, not the iOS bug or exploitability.

No candidate should be labeled exploitable, cracked, or a working jailbreak without independent evidence directly supporting that claim. No live exploit testing is part of this plan.

## Current evidence summary

- CVE-2026-84607: version-range evidence below 26.7 is recorded; exact build 23G83, race controllability, and exploitability are not established.
- CVE-2026-84523: below-26.7 range was previously recorded, but the canonical record should be rechecked before relying on it.
- CVE-2026-43689: secondary source says affected versions unknown; do not infer a precise range from fixed-release wording.
- CVE-2026-86876 and CVE-2026-86886: impact/fix summaries are recorded, but precise CPE ranges are not established in the current review.
- Other candidates: precise affected-version ranges and patch-level detail remain evidence gaps.

## Sources

- Apple iOS 26.7 security content: https://support.apple.com/en-us/149041
- Apple iOS 26.6.1 security content: https://support.apple.com/en-us/148282
- NVD CVE-2026-84607: https://nvd.nist.gov/vuln/detail/CVE-2026-84607
- NVD CVE-2026-84523: https://nvd.nist.gov/vuln/detail/CVE-2026-84523
- Existing candidate results ledger: https://github.com/mirkolanvojov-collab/Freedom27/blob/main/research/ios26_7_candidate_validation_results_2026-10-23.json
