# Public 26.7-to-26.7.1 comparison lead — 2026-10-26

## What was found

The public `blacktop/ipsw-diffs` repository now lists a direct comparison titled **26.7 (23H24) vs 26.7.1 (23H30)** and identifies `/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics` as the only updated dylib in that comparison. It links Apple's iOS 26.7.1 security advisory.

- Public comparison: https://github.com/blacktop/ipsw-diffs/blob/main/iOS/26_7_23H24_vs_26_7_1_23H30/README.md
- Apple advisory: https://support.apple.com/en-us/149226
- The comparison inputs named by that public report are for `iPhone18,1`, not the project target `iPhone17,4`.

## Why this helps, and what it does not prove

This is a better patch-attribution lead than comparing 26.6.1 directly with 26.7.1: the public diff independently identifies CoreGraphics as updated between the two release builds associated with the CVE advisory. However, the published binary pair is for a different device profile, so its exact instructions and hashes cannot be substituted for the iPhone 16 Plus target. It does not establish that the candidate `_aa_lineto` conversion change is the fix; that still requires a same-device, same-architecture 23H24-to-23H30 comparison.

## Next step for the target profile

Obtain or verify the iPhone17,4 build 23H24 restore/OTA metadata and cryptographic hashes from Apple's update catalog or a trustworthy IPSW index. Then extract the 23H24 CoreGraphics binary with the existing read-only workflow and compare it directly to 23H30. Do not hard-code an unverified download URL, size, hash, or OTA decryption key into CI.

## Current workflow note

As of 2026-10-26 14:26 UTC, the comparison workflow configuration has been adjusted to cancel superseded runs (`cancel-in-progress: true`) and to avoid duplicate branch-push plus pull-request triggers; it now runs on `workflow_dispatch` and relevant pull-request changes. The latest PR #37 comparison run is **40339513445** for commit `702e53e6e7da214b2f90b91ff297f298d6c7d790`. GitHub now returns a `compare` job (job ID `121630054731`), but both the run and job remain `queued`, with no runner name or start time assigned. This is different from the earlier zero-job pending state, and confirms that workflow configuration is registering a job; it does not prove whether the remaining delay is runner capacity, account/repository limits, or GitHub orchestration. The unit-test workflow for the same commit completed successfully in run **40339512471**. Comparison run: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40339513445. Tests: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40339512471.

The research blocker remains separate from CI. A new provenance lead now identifies the iPhone17,4 iOS 26.7 / 23H24 OTA candidate, its published size, and extraction key; see [the target OTA provenance note](coregraphics-26-7-target-ota-provenance-lead-2026-10-26.md). The direct Apple CDN URL and locally computed full-file SHA-256 still need verification, followed by a same-device 23H24-to-23H30 CoreGraphics comparison. The public comparison remains a useful cross-check but is for `iPhone18,1`. Do not substitute a different device profile or guess a URL, hash, file size, or decryption key.
