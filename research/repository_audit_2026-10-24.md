# Repository audit — 2026-10-24

## Scope

Audited the current `main` tree (170 tracked files at the time of review): 67 Python files, 80 Markdown files, 19 JSON files, and 4 GitHub Actions workflow files. All Python source/tests and workflow definitions were reviewed with static-pattern checks; all JSON files were parsed; Markdown files were scanned for stale component-hash status and unsafe overclaim patterns; core download, IPSW inventory/comparison, device-safety, evidence-gate, and test paths received focused review.

This is a repository/tooling audit. It is not a binary audit of Apple firmware and not a test of the physical iPhone. The repository remains a research scaffold and does not contain a working jailbreak implementation. No device was accessed or modified, and no exploit was executed.

## Issues fixed

1. **Stream range parser and response-boundary checks.** Tightened resumed streaming to validate HTTP `Content-Range` start/total/bounds, constrain reads to the declared range, validate `Content-Length` when present, reject excess bytes, and reject invalid size/retry arguments. Added regression tests for wrong range totals, mismatched lengths, overlong responses, and interrupted reads. An intermediate regression from incorrectly escaped regex text was caught by CI, corrected, and the full test workflow subsequently passed.
2. **Pinned fixed-build size.** The iOS 27.0 comparison IPSW now has its observed expected byte count pinned at 12,313,212,859 bytes, so the workflow no longer relies on a HEAD response to determine the expected size.
3. **Fail-closed inventory comparison.** The comparison loader now rejects malformed JSON roots, invalid SHA-256 values, missing device class, malformed identity/component structures, and ambiguous duplicate variant/component entries rather than silently overwriting a record.
4. **Stale research report.** Updated the 23G83 vs 24A437 manifest comparison report to reflect that both builds' raw AVE and KernelCache member hashes are now available. Raw-byte differences are documented without attributing them to a specific CVE.

## Validation

- Full GitHub Actions test workflow passed after the stream-verifier fixes: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40049362690
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
