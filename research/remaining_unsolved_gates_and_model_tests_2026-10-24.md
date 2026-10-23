# Remaining unsolved work — evidence gates and safe model tests (2026-10-24)

## What this change accomplishes

Adds benign, executable abstract regression models for authorization, range validation,
object lifetime, explicit state transitions, complete output initialization, and
synthetic POSIX path containment. The tests run offline and do not access iOS, invoke
Apple components, reproduce a CVE, or contain exploit triggers.

- Implementation: `Framework/security_invariant_models.py`
- Tests: `tests/test_security_invariant_models.py`
- Automated discovery: the existing workflow runs `python -m unittest discover -s tests -v`,
  so the new tests are included without a separate workflow path.

## What remains unsolved

| Gate | Current state | Evidence required to close it |
|---|---|---|
| Exact build 23G83 applicability | **Open** for all 12 candidates | Build-specific vendor/research evidence or independently reproducible, non-invasive confirmation |
| Public patch invariant | **Unavailable publicly** in the sources reviewed for most candidates | Stable primary-source patch/commit, technical write-up, or vendor clarification |
| CVE metadata reconciliation | **Partially open** | Per-CVE matching of Apple advisory wording to official CVE Program records and NVD capture, with discrepancies retained |
| Exploitability / chain role | **Not established** for all 12 | Credible independently reproduced evidence; advisory impact alone is insufficient |
| Safe physical-device validation | **Not performed** | Dedicated test hardware, reviewed test protocol, logs, and documented recovery path; repository CI is not device validation |
| Full jailbreak implementation | **Absent** | A legitimate, documented platform path and reviewed implementation; package manager, tweak support, and persistence are not established |

## Model coverage and limitations

- Authorization decision model: a false or malformed mock authorization result fails closed.
- Range model: zero length, exact end, one-past-end, negative values, boolean-as-integer, and very large lengths are checked.
- Lifetime model: terminal release cannot be retained, released again, or used.
- State-transition model: only declared transitions are accepted.
- Output model: required fields must all be present and initialized.
- Path model: lexical containment is checked for synthetic absolute POSIX paths.

These are general defensive properties, not reconstructed Apple patch invariants. In particular,
lexical path containment is not a filesystem security boundary; real systems require platform-
appropriate canonicalization and race-resistant file-handle checks. Passing these tests cannot
establish that any CVE is present, reachable, exploitable, or useful for a jailbreak.

## Provenance and validation contract

Target metadata remains the reported iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build
`23G83`. Existing NVD capture provenance remains workflow
[40041118442](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40041118442),
artifact SHA-256
`e21723d4911c67ca86efbfa74b845c595070ca39ca80856bf1d8e4af3fd9f236`.
The existing advisory assessment records 12/12 version-range matches but 0/12 exact-build
reachability confirmations and no reproduced exploit. Those values are not upgraded by these
model tests.

Required checks for this change:
1. Python compile check for all source and test modules.
2. Full `unittest discover` suite.
3. Existing advisory, source, evidence, compatibility, blocker, and safety metadata checks.
4. Review the PR diff and CI result before merge.
