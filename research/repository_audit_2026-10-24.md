# Repository audit — 2026-10-24

## Scope

Audited the current `main` tree (170 tracked files at the time of review): 67 Python files, 80 Markdown files, 19 JSON files, and 4 GitHub Actions workflow files. All Python source/tests and workflow definitions were reviewed with static-pattern checks; all JSON files were parsed; Markdown files were scanned for stale component-hash status and unsafe overclaim patterns; core download, IPSW inventory/comparison, device-safety, evidence-gate, and test paths received focused review.

This is a repository/tooling audit. It is not a binary audit of Apple firmware and not a test of the physical iPhone. The repository remains a research scaffold and does not contain a working jailbreak implementation. No device was accessed or modified, and no exploit was executed.

## Issues fixed

1. **Stream range parser and response-boundary checks.** Tightened resumed streaming to validate HTTP `Content-Range` start/total/bounds, constrain reads to the declared range, validate numeric `Content-Length` when present, reject excess bytes, and reject invalid size/retry arguments. Added regression tests for wrong range totals, malformed/mismatched lengths, overlong responses, and interrupted reads. An intermediate regression from incorrectly escaped regex text was caught by CI, corrected, and the full test workflow subsequently passed.
2. **Pinned fixed-build size.** The iOS 27.0 comparison IPSW now has its observed expected byte count pinned at 12,313,212,859 bytes, so the workflow no longer relies on a HEAD response to determine the expected size.
3. **Fail-closed inventory comparison.** The comparison loader now rejects malformed JSON roots, invalid SHA-256 values, missing device class, malformed identity/component structures, and ambiguous duplicate variant/component entries rather than silently overwriting a record.
4. **Stale research report.** Updated the 23G83 vs 24A437 manifest comparison report to reflect that both builds' raw AVE and KernelCache member hashes are now available. Raw-byte differences are documented without attributing them to a specific CVE.

## Validation

- Full GitHub Actions test workflow passed after the final stream-verifier changes: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40049498513
- Full GitHub Actions test workflow passed after the fail-closed inventory-comparison changes: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40049362690
- The workflow compiles Python files, runs the unit-test suite, validates advisory/source metadata, checks exact-target claims and project metadata, verifies safety preflight fails closed, and validates generated research reports.
- Static scans found no use of dynamic `eval/exec`, `shell=True`, `os.system`, unsafe temporary-name generation, or pickle loading in the reviewed Python source/tests. The one broad exception in the advisory source audit is used to record failed external-source fetches as audit errors, not to continue a security-sensitive operation.

## Remaining limits / no crash guarantee

- **No crash-free claim is possible.** The project does not yet contain a verified exploit chain or runnable jailbreak to exercise. A passing unit-test suite validates repository logic, not kernel exploit stability or behavior on an iPhone.
- Exact-build entry, sandbox escape, kernel primitive, privilege escalation, mitigation handling, bootstrap/package-manager compatibility, and independent reproduction remain unverified.
- Raw IPSW member hashes are not decrypted code hashes and do not prove CVE patch attribution.
- The safety preflight intentionally keeps `device_execution_authorized=false` and `guarantees_no_crash=false`.

## Follow-up

Continue with non-invasive evidence review and tests only. Before any future device-testing phase, require a source-pinned implementation review, a dedicated recoverable test device, independently checked backup/recovery procedure, and a narrowly scoped test plan. Do not run an unverified payload on the daily-use phone.

## Follow-up audit — research branch (2026-10-24)

Rechecked the current branch against `main` after the CoreGraphics comparison work. The branch contains 184 tracked files: 73 Python files, 86 Markdown files, 19 JSON files, and 6 GitHub Actions workflow files. All 19 JSON files were parsed successfully and their fetched blob SHAs matched the Git tree. The new CoreGraphics scripts, synthetic bounds model, related tests, workflow definitions, changed evidence-gate code, and changed verification scripts received focused review.

Additional issues fixed in this follow-up:

1. **Chain evidence scope:** `Framework/chain_readiness.py` now requires `scope_confirmed=true` in addition to a source-pinned exact-target record and independent reproduction. Regression tests cover missing scope confirmation.
2. **Exact-target identity and malformed fields:** `Framework/compatibility_status.py` now matches the device marketing name as well as identifier/version/build, rejects malformed or credentialed HTTPS evidence URLs, and treats JSON `null` as missing rather than converting it to the string `None`. The compatibility matrix mapper has the same null-handling fix.
3. **Firmware stream source validation:** `research/scripts/verify_ipsw_stream.py` now rejects non-HTTPS URLs, embedded credentials, and malformed ports before opening a connection; regression tests verify the opener is not called.
4. **NVD capture input validation:** `research/scripts/capture_nvd_configurations.py` now validates the complete CVE identifier format instead of accepting any string with a `CVE-` prefix.
5. **Fixed OTA digest enforcement:** `.github/workflows/resolve-fixed-ota-metadata.yml` now compares the downloaded OTA SHA-256 with the pinned expected digest, rather than merely printing the computed digest after checking the size.
6. **Research-document consistency:** updated the CoreGraphics evidence assessment and Priority 2 reports to reflect the completed 25-symbol static comparison and seven-function patch-pattern correlation, while keeping runtime reachability and jailbreak status unverified.
7. **Empty comparison results:** the CoreGraphics function comparer now exits non-zero when there are no shared executable `aa_*` symbols, rather than returning a misleading success with zero coverage.
8. **Malformed inventory/evidence inputs:** the IPSW manifest inventory rejects invalid argument types and non-dictionary plist roots; evidence checks no longer crash on unhashable registry IDs and reject malformed HTTPS ports. Compatibility URL validators also reject malformed ports and null fields instead of stringifying them.
9. **Synthetic coordinate model:** finite values whose scaling overflows now saturate to the safe bound; non-finite inputs return the defined safe fallback, and booleans/non-numeric inputs are rejected. Regression tests cover these boundaries.
10. **CI resource control:** the OTA download, CoreGraphics comparison, and unit-test workflows now cancel superseded runs for the same PR/ref, preventing each successive commit from starting another redundant multi-gigabyte firmware download.

Validation after the code fixes: GitHub Actions test run https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40116859478 completed successfully on commit `0f87efa3df8bb1848e3507c5612f8552be28a24b`, including the new regression tests for malformed evidence/inventory input, empty CoreGraphics comparisons, and coordinate bounds. The fixed-OTA digest workflow passed on commit `6a78d9811e53aecfeebea8fa82a1dfca22a43eb0`; the latest workflow revisions add concurrency controls without changing the pinned digest check. The final audit-document update is documentation-only and will trigger a fresh PR check.

Remaining audit boundary: repository-level static review and tests do not prove Apple firmware behavior, exact-build exploitability, or a working jailbreak. The CoreGraphics comparison remains static, relocation-sensitive references are not fully resolved, and runtime reachability, privilege escalation, persistence, and independent reproduction remain open.


## Follow-up audit — compatibility metadata edge cases (2026-10-24)

A further pass over the compatibility claim helpers found two edge cases that could obscure conflicting or malformed evidence:

1. **Conflicting rows for the same exact target:** the compatibility matrix duplicate key included the claim status, so the same model/version/build could appear once as `researching` and again as `verified` without a duplicate warning. The key now identifies the target tuple independent of status, and a regression test covers conflicting statuses.
2. **Whitespace-normalized status leakage:** the exact-target status reader validated a trimmed status but returned the original untrimmed value, allowing padded status text to leak into output and conflict handling. Validated claims now store the normalized status; a regression test covers it.

Validation: GitHub Actions test run https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40119295737 passed on commit `84ee2e969ccd2662297316a980073f12b19347c4`, including compilation, unit tests, advisory-source checks, evidence metadata checks, fail-closed safety preflight, and generated report validation. This follow-up did not test or modify a device and does not change the project's unverified jailbreak status.
