# AppleAVE2 cross-CVE triage and firmware hash provenance — 2026-10-24

## Summary

Two useful checks were completed in this pass:

1. The exact IPSW SHA-256 published by IPSW Downloads and AppleSN.info matches: `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`. Both list iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`. The catalogues point to an Apple CDN URL. This is cross-catalogue agreement, **not** an independently recalculated checksum: the 11+ GiB firmware image was not downloaded in this pass.
2. A separate public AppleAVE2 research repository was found for **CVE-2026-64747**, describing a macOS AppleAVE2 buffer-overflow hypothesis. It must not be conflated with the project's iOS CVE-2026-84607 candidate.

## Firmware metadata provenance

- Apple security-content advisory for iOS 26.6.1: https://support.apple.com/en-us/148282
- IPSW Downloads exact build page: https://ipsw.me/download/iPhone17%2C4/23G83/
- AppleSN.info exact build page: https://applesn.info/firmware/ipsw/iPhone17%2C4/23G83/
- Apple CDN URL listed by AppleSN.info: https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw

Both secondary catalogues list the same SHA-256, SHA-1, and MD5 values for the same filename/build. Matching values strengthen metadata consistency but do not substitute for hashing a downloaded file or cryptographically verifying its contents. Apple’s advisory says the release was published on 2026-08-17 and that it delivers security fixes first made available in iOS 27 betas.

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

To advance exact-build confidence without touching the device, the next gate is to obtain a lawful, authenticated copy of the matching firmware, independently calculate its SHA-256, record download and tool provenance, and inspect only the minimum relevant binaries using a reproducible, read-only workflow. Any comparison against a fixed build must pin both builds and avoid treating symbol/string similarities alone as proof of CVE attribution. If the firmware cannot be obtained and verified, record that blocker rather than infer the result.

## Method limits

- Public-source read-only research.
- No firmware image downloaded or independently hashed in this pass.
- No exploit code built or run.
- No device accessed, installed on, downgraded, restored, or modified.
- No exact-build vulnerable code path, jailbreak chain, or crash-safety guarantee established.
