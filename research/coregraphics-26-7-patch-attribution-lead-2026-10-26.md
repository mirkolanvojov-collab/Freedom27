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

The latest comparison workflow run for PR #37 (run 40338497619, commit `6cb43f37fbf0a33670e6301e5e9ffc5a8fe4dd1c`) was still `pending` with no jobs returned by the jobs endpoint when checked at 2026-10-26 14:21 UTC. Previous comparison runs for older commits were cancelled while a newer run was created; this status is consistent with a runner/queue or orchestration issue but does not establish the cause. The unit-test workflow for commit `6cb43f37fbf0a33670e6301e5e9ffc5a8fe4dd1c` completed successfully. The documentation commit that adds this note does not modify the comparison workflow or its inputs.
