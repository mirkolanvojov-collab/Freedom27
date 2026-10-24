# Reproducible IPSW checksum verification

This resolves the *process gap* in exact-firmware provenance; it does not claim the firmware has already been downloaded or verified.

Target: iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`.

The pinned SHA-256 currently published by two secondary firmware catalogues is:

`101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`

Apple CDN URL listed in the catalogue:
https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw

## Procedure

1. Obtain the IPSW only from the pinned Apple CDN URL or Apple's supported restore workflow.
2. Keep the original file unchanged and note where and when it was obtained.
3. Run `python research/scripts/verify_ipsw_sha256.py /path/to/iPhone17,4_26.6.1_23G83_Restore.ipsw`.
4. Require `verified: true`, and retain the JSON output alongside acquisition date, file size, and source URL.
5. On mismatch, stop. Do not unpack, inspect, install, or use the file as target evidence until the discrepancy is resolved.

The script streams the file in 1 MiB chunks, so it does not load the full IPSW into memory. It does not download files, alter firmware, contact a device, or execute exploit code. The hash is a pinned secondary-source value, not an Apple-signed attestation; independently computed agreement proves file-byte consistency with that pinned value, not authenticity by itself.

## Next boundary

After the hash check succeeds, record the output and compare the minimum relevant components against a known fixed release using reproducible read-only tooling. Component/string/symbol similarity alone is not enough to attribute a CVE or establish exploitability. No CVE should be promoted to exact-build-confirmed without a defensible affected/fixed code comparison and independently reviewed evidence.
