# 23H24 Google Drive transfer — observed evidence (2026-11-04)

## Successful transport and digest observation

- GitHub Actions run: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41904780241
- Workflow: `.github/workflows/verify-23h24-drive.yml`
- Job: `verify` (126836400598), completed successfully.
- Source: user-provided publicly shared Google Drive file, **not** independently authenticated as an Apple download.
- Downloaded bytes: **8,724,152,320**
- Observed SHA-256: `4d26644c2e7876c022f40a6e2459b1e3ae32027fedbd297bab82379bb40c6a4a`
- Integrity report artifact: `23H24-drive-integrity`, artifact ID `13358559039`.
- Log shows gdown transfer reached 100%, then `stat` and `sha256sum` completed. The workflow removed the downloaded `.aea` from the runner after hashing.

## Interpretation and remaining blockers

This verifies a successful cloud-to-runner transfer and records the digest of the received bytes. It **does not** verify an independently trusted Apple digest, a signed firmware manifest, exact build 23H24, device compatibility, or decryptability of the AEA archive. The Google Drive file is not equivalent to verified Apple CDN provenance.

Before treating this as a trusted 23H24 CoreGraphics source:
1. Establish authoritative archive identity and build/device metadata from a trusted independent source, and compare with the observed archive.
2. Determine whether the AEA container can be decrypted/extracted using legitimate available keys/tools. Do not infer CoreGraphics availability from successful download alone.
3. Only after extraction, record CoreGraphics binary identity and perform reproducible comparisons to 23H30 and 23G83, keeping patch attribution tentative until corroborated.

No jailbreak, exploit, firmware installation, or device modification is established by this evidence. Keep PR #37 in draft.

## Authentication checkpoint (2026-11-05)

The successful transfer was independently rechecked against GitHub Actions run 41904780241, job 126836400598. Its log confirms the full 8,724,152,320-byte transfer, SHA-256 `4d26644c2e7876c022f40a6e2459b1e3ae32027fedbd297bab82379bb40c6a4a`, and artifact 13358559039 (383-byte integrity report, not the firmware). The workflow explicitly deleted the temporary `23H24.aea` after hashing. Therefore no retained firmware bytes are available in that artifact for inspecting the AEA prologue, decrypting, or extracting CoreGraphics.

The subsequent live `ipsw download ota --platform ios --device iPhone17,4 --build 23H24 --json` query in run 42101677930 returned schema version 1 with an empty `otas` array. This establishes only that this query did not return a matching OTA at that time; it does not establish that the Google Drive archive is authentic or inauthentic.

### Authentication gates (do not infer success)

| Gate | Evidence | Status |
| --- | --- | --- |
| Transfer and local digest observation | GitHub run 41904780241, artifact 13358559039 | Verified |
| AEA magic/header/profile | Requires access to original archive bytes; expect `AEA1` magic, then inspect profile and authenticated metadata | Unverified |
| Independent Apple CDN URL, metadata, size, published hash | Must obtain Apple-served asset record matching exact archive; live OTA discovery returned no match | Blocked |
| Build 23H24 and device iPhone17,4 identity | Requires independent Apple asset metadata and/or authenticated extracted firmware metadata | Unverified |
| Decryption and CoreGraphics extraction | Requires legitimate key/tooling and archive bytes; successful transfer alone is insufficient | Unverified |

Do not compare the GitHub artifact ZIP digest with the firmware SHA-256: these identify different objects. Do not claim a cryptographic signature from an AEA magic check; some AEA encryption profiles are unsigned. The next meaningful archive-side operation is to inspect the first bytes and authenticated metadata of the *existing* Drive file without treating the filename or uploader's label as proof of origin. Keep PR #37 draft and avoid repeated multi-gigabyte transfers solely to re-establish the same observed hash.
