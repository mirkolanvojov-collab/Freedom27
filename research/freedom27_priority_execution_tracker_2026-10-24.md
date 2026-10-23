# Freedom27 research priorities — execution tracker (2026-10-24)

## Scope and constraints

This tracker executes the four priorities in `public_patch_evidence_and_regression_specs_2026-10-24.md` as a coordinated, read-only research pass. It does not attempt to obtain kernel execution, bypass iOS protections, weaponize a vulnerability, or modify a device. Public advisory text and version metadata are evidence of vendor-reported impact and affected ranges, not proof that a specific device build is exploitable.

Target noted in the existing ledger: iPhone17,4 / iOS 26.6.1 / build 23G83. The exact build remains **unverified** by the public records reviewed so far.

## Execution matrix

| Priority | Candidates | Work item | Acceptance criteria | Current status |
|---|---|---|---|---|
| P0 — source integrity | All 12 | Reconcile each CVE ID, component, impact and fix wording against Apple's primary advisory and the official CVE Program (Apple CNA) JSON | Every summary cites a primary URL; mismatches are marked unresolved rather than guessed | Partial: public summaries captured; repeatable automated comparison still needed |
| P0 — version evidence | All 12 | Re-run the existing read-only NVD CVE 2.0 + CPE Match 2.0 capture and retain raw responses with timestamps and hashes | Every candidate has raw JSON or a clearly recorded retrieval failure; iOS/iPadOS CPE matches are distinguished from other Apple platforms | Prior run reported 12/12 HTTP 200; repeat capture not yet run in this tracker |
| P0 — high-impact public evidence | CVE-2026-84607, CVE-2026-43689 | Search vendor bulletins, official CVE records, public vendor/maintainer notes and public source-control history for implementation-level patch evidence | Evidence is a stable public URL or commit; otherwise explicitly record “no public patch found in checked sources” | Open; advisory-only wording is not sufficient to reconstruct an exploit |
| P1 — mapping correction | CVE-2026-86876, CVE-2026-86886 | Reconcile the existing ledger's CoreMedia / TCC descriptions line-by-line against Apple's advisory and official CVE JSON | No component or impact remains marked confirmed without matching source text | Open; existing descriptions are provisional until checked |
| P1 — memory-safety properties | CVE-2026-84523, CVE-2026-84566, CVE-2026-43684, CVE-2026-43686, CVE-2026-28968 | Define vendor-harness regression properties for bounds, ownership and lifetime without a device trigger or exploit primitive | Each test is a benign invariant/model test and records what it cannot establish | Specification drafted; executable abstract-model tests are the next safe artifact |
| P2 — information disclosure/prerequisite | CVE-2026-43687, CVE-2026-65405, CVE-2026-84622 | Confirm advisory impact and prerequisites; preserve the distinction between disclosure and initial privilege escalation | Any root prerequisite is explicit; disclosure-only issues are not promoted to an initial-entry claim | Advisory-level classification drafted; source-level details remain open |
| P2 — exact target identity | All 12 | Separate product identifier, marketing OS version, build number and vendor affected-range metadata | Report labels version-range matches separately from exact-build proof and device testing | Open: no local device verification performed |

## Per-CVE status ledger

| CVE | Working issue class from current public summary | Safe next check | Do not infer |
|---|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder race / state management | Public patch/commit or vendor technical note; abstract state-machine invariant | Race controllability or kernel execution |
| CVE-2026-43689 | Kernel authorization / permissions | Public patch reference; authorization matrix in a mock interface | Root access or an entry primitive |
| CVE-2026-84523 | APFS out-of-bounds write | Bounds-validation model with overflow/boundary cases | Controllable kernel-memory write |
| CVE-2026-86876 | Provisional CoreMedia mapping | Primary advisory and official CVE JSON reconciliation | Confirmed component/path until sources agree |
| CVE-2026-86886 | Provisional TCC/path-validation mapping | Primary advisory and official CVE JSON reconciliation | Confirmed path traversal until sources agree |
| CVE-2026-84566 | Kernel memory handling | Verify exact impact wording; abstract lifetime/error-path invariant | Kernel execution from memory-corruption wording |
| CVE-2026-43687 | NFS-related information disclosure | Verify scope and disclosure source in official records | Code execution from disclosure alone |
| CVE-2026-43684 | Kernel use-after-free | Ownership/lifetime model; public patch evidence search | Exploitability from CWE or impact statement |
| CVE-2026-43686 | NFS-related use-after-free | Ownership/lifetime model; verify NFS association against primary record | Reachability from a malicious server alone |
| CVE-2026-65405 | Kernel memory-layout disclosure | Identify what official advisory actually confirms | A complete bypass from layout disclosure alone |
| CVE-2026-84622 | Uninitialized kernel memory with root prerequisite | Confirm prerequisite and exact affected range | Initial privilege escalation without evidence of root acquisition |
| CVE-2026-28968 | Kernel out-of-bounds write | Bounds/arithmetic model; public patch evidence search | A reliable corruption primitive |

## Safe model-test plan

These are abstract tests for a vendor-controlled harness, not reproductions of Apple's bugs:

1. **Authorization model (CVE-2026-43689):** enumerate allowed and denied caller contexts; every privileged operation must fail closed when the mock authorization predicate is false, including alternate entry points.
2. **Bounds model (CVE-2026-84523, CVE-2026-28968):** test zero length, exact capacity, one-past-capacity, negative/signed conversion, and arithmetic-overflow inputs against a synthetic buffer. Assert rejection and unchanged adjacent sentinel values.
3. **Lifetime model (CVE-2026-84566, CVE-2026-43684, CVE-2026-43686):** model object states and references; reject use after terminal release and ensure cleanup/error transitions do not leave stale references.
4. **State-machine model (CVE-2026-84607):** enumerate legal state transitions and conflicting abstract events; assert that each operation observes a valid state and authorization decision. Do not reproduce timing or scheduling against Apple's component.
5. **Output-initialization model (CVE-2026-43687, CVE-2026-65405, CVE-2026-84622):** initialize mock output structures to a sentinel; assert all returned bytes are explicitly assigned and only authorized fields are emitted.
6. **Canonical-path model (only if the CVE-2026-86886 mapping is confirmed):** test normalization and authorization decisions on synthetic paths, asserting that access checks apply to the canonical target and protected roots cannot be crossed.
7. **Sandbox-policy model (only if the CVE-2026-86876 mapping is confirmed):** test that a mock media parser cannot change its declared privilege boundary; keep parser input synthetic and non-exploitative.

## Source and evidence rules

- Primary sources: Apple's security bulletin and the official CVE Program repository (`CVEProject/cvelistV5`, Apple CNA record).
- NVD is used for structured affected-software configurations; preserve raw JSON, timestamps, HTTP status and hashes.
- Secondary mirrors may help discover a source but are not the final authority when the primary record is available.
- Do not treat a version upper bound such as “below 26.7” as proof for build 23G83, a working exploit, or a jailbreak chain.
- Apple lists later updates in its security release index. Re-check the currently applicable release record when refreshing evidence; do not assume a previous bulletin is the newest release.
- A search that finds no public diff should be reported as “not found in sources checked,” not “does not exist.”

## Definition of done for this pass

- [ ] Capture a fresh NVD API artifact for all 12 candidates.
- [ ] Save a per-CVE source reconciliation result, including mismatches and unknowns.
- [ ] Record any public patch/commit references for P0 candidates or mark them not found in sources checked.
- [ ] Add synthetic model tests for bounds, authorization, state transitions, lifetime and output initialization.
- [ ] Keep exact-build verification and exploitability as false/unverified unless independent evidence changes that status.

## Sources

- Apple iOS 26.7 / iPadOS 26.7 security bulletin: https://support.apple.com/en-us/149041
- Apple security releases index (for later releases): https://support.apple.com/en-us/100100
- NVD CVE 2.0 API: https://services.nvd.nist.gov/rest/json/cves/2.0
- NVD CPE Match 2.0 API: https://services.nvd.nist.gov/rest/json/cpematch/2.0
- Official CVE Program records: https://github.com/CVEProject/cvelistV5

Last updated: 2026-10-24. This is a research tracker, not an exploitability assessment.
