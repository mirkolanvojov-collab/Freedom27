# Exact-target IPSW integrity verification procedure

## Pinned target

- Device: iPhone 16 Plus (iPhone17,4)
- OS/build: iOS 26.6.1 (23G83)
- Expected filename: iPhone17,4_26.6.1_23G83_Restore.ipsw
- Published size: 11,225,458,130 bytes
- Published SHA-256: 101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f
- Apple CDN URL: https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw
- Independent catalogue references: https://ipsw.me/download/iPhone17%2C4/23G83/ and https://applesn.info/firmware/ipsw/iPhone17%2C4/23G83/

The two catalogues agree on the SHA-256, but that is not an independent file hash. The verifier in research/scripts/verify_ipsw.py hashes a local file in bounded-memory chunks, checks the exact filename and published size, and optionally validates the ZIP CRCs. It performs no download and cannot modify a device.

## Run after downloading from the Apple CDN

From the repository root:

```sh
python research/scripts/verify_ipsw.py "/path/to/iPhone17,4_26.6.1_23G83_Restore.ipsw"
```

For a full archive CRC check (reads every member and may take considerable time):

```sh
python research/scripts/verify_ipsw.py "/path/to/iPhone17,4_26.6.1_23G83_Restore.ipsw" --check-zip
```

Only a JSON result with "verified": true passes the pinned identity/size/hash checks. Save the JSON output alongside the file's acquisition date and source URL. Do not restore or mount the image as part of this integrity check.

## What this does and does not resolve

- It provides a reproducible path to independently verify the firmware file once the 11.23 GB IPSW is available on a trusted host.
- No IPSW was downloaded in this research session, so no independent hash result is claimed.
- Hash integrity authenticates correspondence to the published digest, not that a CVE is exploitable.
- The 12 CVE records are version-range candidates: NVD's versionEndExcluding: 26.7 and Apple's iOS 26.7 advisory do not prove vulnerable code is present or reachable in build 23G83.
- To narrow CVE applicability, the next required evidence is a source-backed, version-matched comparison of the relevant component in the target and fixed firmware, with exact source/build provenance and a human-reviewed change attribution. A symbol/string match alone is insufficient. No exploit reproduction or device execution is required or authorized by this procedure.

## Primary security-source anchor

Apple's iOS 26.7 advisory identifies CVE-2026-84607 as an AVEVideoEncoder race condition addressed with improved state management, with an impact described as a sandboxed app potentially executing code with kernel privileges. This is authoritative issue context, not a public proof-of-concept or target-build reproduction:
https://support.apple.com/en-us/149041
