# All-priority public evidence triage — 2026-10-24

## Primary-source check

Primary Apple bulletin: https://support.apple.com/en-us/149041
NVD CVE-2026-84607: https://nvd.nist.gov/vuln/detail/CVE-2026-84607

The Apple bulletin does publicly confirm CVE-2026-84607: AVEVideoEncoder race condition, impact potentially allowing a sandboxed app to execute arbitrary code with kernel privileges, fixed through improved state management. The public summary does not identify the affected function or expose a patch diff. NVD independently shows the iPhone OS/iPadOS affected range as below 26.7. This remains version-range evidence, not a build-specific proof or an exploit demonstration.

A targeted public-source search was also made for the other prioritized candidate IDs and patch details. The checked results did not yield a verifiable source diff, affected function, or researcher reproduction for them. Apple explicitly notes that it does not disclose, discuss, or confirm security issues until an investigation has occurred and patches or releases are available; public advisory summaries may therefore be all that is available.

## Priority-by-priority results

| Priority | Candidate(s) | Public evidence found in this pass | Status / next evidence needed |
|---|---|---|---|
| P1 | CVE-2026-84607 | Apple and NVD confirm AVEVideoEncoder race, kernel-privilege impact, fix in 26.7; NVD marks iOS/iPadOS affected below 26.7 | Advisory-confirmed; patch-level invariant, affected function and build-specific reachability unavailable publicly |
| P1 | CVE-2026-43689 | No verifiable patch diff or independent technical write-up found in checked results | Advisory-only; exact permission check and code path unresolved |
| P2 | CVE-2026-84523, CVE-2026-84566, CVE-2026-43684, CVE-2026-43686, CVE-2026-28968 | No verifiable source diff or reproducer found in checked results | Keep proposed bounds/lifetime invariants as test hypotheses, not confirmed reconstructions of Apple's patches |
| P3 | CVE-2026-86876, CVE-2026-86886 | Search did not yield source-level evidence that reconciles the candidate-ledger summaries with a concrete public patch | Mapping remains provisional; do not treat the ledger wording as independently confirmed until primary record is matched exactly |
| P4 | CVE-2026-43687, CVE-2026-65405, CVE-2026-84622 | No public technical patch evidence found in this pass; prior advisory summaries indicate information-disclosure outcomes, with CVE-2026-84622 requiring root | Low priority as standalone entry points; exact disclosure details remain unavailable |

## Safe regression specifications retained

These are proposed security properties for a vendor-controlled test harness or abstract model, not claims about Apple's exact implementation:
- State/race: concurrent state changes must not allow an operation to proceed against stale or unauthorized state.
- Authorization: privileged actions must validate the caller context on every entry path.
- Bounds: offsets, lengths, and arithmetic must be checked against actual object capacity before memory access.
- Object lifetime: ownership/reference rules must prevent use after release and double release.
- Path authorization: checks must apply to the canonical target path and remain confined to authorized roots.
- Memory disclosure: all returned bytes must be initialized and limited to the authorized output structure.

## What this does and does not establish

- Public-source triage has been performed across all listed priority groups.
- Only CVE-2026-84607 was directly reconfirmed against both the Apple bulletin and its NVD detail page in this pass.
- No public patch diff or reproducible exploit was established for any candidate.
- iOS 26.6.1 lies within the published NVD version range for CVE-2026-84607, but exact build 23G83 and device-specific applicability have not been verified.
- No exploit was run, no payload was developed, and no device was accessed or modified.

## Sources

- Apple iOS 26.7 / iPadOS 26.7 security content: https://support.apple.com/en-us/149041
- NVD CVE-2026-84607: https://nvd.nist.gov/vuln/detail/CVE-2026-84607
- Existing Freedom27 NVD capture and candidate ledger:
  - https://github.com/mirkolanvojov-collab/Freedom27/blob/main/research/nvd_affected_configuration_capture_2026-10-23.md
  - https://github.com/mirkolanvojov-collab/Freedom27/blob/main/research/ios26_7_candidate_validation_results_2026-10-23.json
