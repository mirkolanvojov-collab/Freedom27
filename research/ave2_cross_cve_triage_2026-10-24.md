# AppleAVE2 cross-CVE triage and firmware hash provenance — 2026-10-24

## Summary

1. **Exact IPSW streaming verification succeeded.** GitHub Actions run https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40046497529 streamed the complete Apple CDN response and reported SHA-256 `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`, exactly matching the pinned digest, and `11225458130` bytes, exactly matching the pinned size. The IPSW was streamed without being written to disk. This closes the checksum-verification process gap, but it does not supply a local IPSW file for component extraction or establish exploitability.
2. A separate public AppleAVE2 research repository was found for **CVE-2026-64747**, describing a macOS AppleAVE2 buffer-overflow hypothesis. It must not be conflated with the project's iOS CVE-2026-84607 candidate.

## Firmware metadata and verification provenance

- Apple security-content advisory for iOS 26.6.1: https://support.apple.com/en-us/148282
- IPSW Downloads exact build page: https://ipsw.me/download/iPhone17%2C4/23G83/
- AppleSN.info exact build page: https://applesn.info/firmware/ipsw/iPhone17%2C4/23G83/
- Apple CDN URL: https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw
- Verification workflow: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40046497529
- Expected and computed SHA-256: `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`
- Expected and computed size: `11225458130` bytes
- File written to disk: no; device modified: no.

The stream's byte-for-byte digest and length match establish integrity relative to the pinned digest and byte count. The digest was previously listed by secondary firmware catalogues; the computation itself was performed by the project's read-only CI job. This does not establish that the digest is an Apple-signed attestation, and it does not provide a persistent local image for binary analysis.

## Cross-CVE triage: CVE-2026-64747

- Public repository: https://github.com/eddinos2/CVE-2026-64747
- README: https://github.com/eddinos2/CVE-2026-64747/blob/main/README.md
- Detailed limitations/validation notes: https://github.com/eddinos2/CVE-2026-64747/blob/main/FIRE_READY.md
- Apple advisory for the current target release: https://support.apple.com/en-us/148282

The public repository describes its work as AppleAVE2 analysis for **CVE-2026-64747**, fixed in macOS 26.6 with an AppleAVE2 kext version transition. Its own README describes its evidence tier as reachability/protocol analysis and analytically argued overflow, not remote code execution; its notes also identify an unresolved hardware-capability gate and say no live overflow was demonstrated in that lab.

### Relevance decision

- This is a separate CVE identifier and a macOS-focused report, not independent validation of iOS CVE-2026-84607.
- Similar component naming (AppleAVE2 / AVEVideoEncoder) is not enough to infer a shared root cause, patch, or exploit primitive.
- The report's detailed trigger and exploitation instructions are not adopted into Freedom27's execution plan; this checkpoint records provenance and scope only.
- It does not establish applicability to iPhone 16 Plus build `23G83`, and it does not justify running the PoC on the user's phone.
- CVE-2026-84607 remains a separate, unverified third-party hypothesis; exact-build applicability, authoritative patch diff, and Freedom27 reproduction remain unestablished.

## Next evidence gate

The transfer/checksum gap is closed. The remaining non-invasive step is a reproducible read-only component inventory/comparison using pinned firmware builds, recording component paths, build identifiers, hashes, extraction-tool versions, and limitations. A successful hash stream does not create a local file to extract. Any comparison must avoid treating symbol/string similarities alone as proof of CVE attribution. If the image is later downloaded to a controlled analysis environment, verify the file hash again before extracting any component.

## Method limits

- Public-source read-only research and streaming integrity verification.
- No firmware image persisted to disk by the verification job.
- No exploit code built or run.
- No device accessed, installed on, downgraded, restored, or modified.
- No exact-build vulnerable code path, jailbreak chain, or crash-safety guarantee established.
