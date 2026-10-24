# Read-only IPSW manifest inventory — research method

**Target:** iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`  
**Current verified target IPSW SHA-256:** `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`  
**Current verified target IPSW size:** `11225458130` bytes  
**Fixed-build comparison candidate:** iOS 27.0 (24A437), `iPhone17,4`; catalogue SHA-256 `a8bed747c08709a63e5b9d55fa87bfca2839245f91a82082a8c30b8833fae149`  
**Primary patch bulletin:** https://support.apple.com/en-us/149041  
**Firmware catalogue references:** https://ipsw.me/download/iPhone17%2C4/23G83/ and https://ipsw.me/install/iPhone17%2C4/24A437/

## Why this is the next gate

The target image's whole-file digest has been independently computed by the project's CI stream verifier and matched the pinned digest and byte count. That operation did not persist the image. A fixed-release comparison therefore still needs a controlled environment with enough temporary storage for one IPSW at a time.

The 26.7 advisory is the closest named fixed release for the tracked CVEs, but a full IPSW for this device was not established in the prior catalogue check. iOS 27.0 has a device-specific full IPSW and a published SHA-256, but it is a larger version gap and includes additional changes. Treat it as a fallback fixed-build comparison baseline, not a minimal patch diff.

## Inventory tool

`research/scripts/inventory_ipsw_manifest.py`:
1. Hashes the complete local IPSW in 1 MiB chunks.
2. Requires a pinned SHA-256 and exact byte count before opening the ZIP.
3. Reads only root `BuildManifest.plist`, with a 64 MiB manifest-size ceiling.
4. Requires root `SupportedProductTypes` to include `iPhone17,4`, then selects BuildIdentity entries whose `Info.DeviceClass` matches board configuration `D48AP`. Product type and board configuration are distinct identifiers.
5. Writes component names, paths and flags (including fields nested under each component's `Info` dictionary), raw manifest digest bytes as hex, and build metadata to JSON without assuming the digest algorithm.
6. Does not extract component payloads, decrypt binaries, contact a device, or execute code.

Example for the already verified target image:

```sh
python research/scripts/inventory_ipsw_manifest.py /path/to/iPhone17,4_26.6.1_23G83_Restore.ipsw \
  --sha256 101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f \
  --size 11225458130 \
  --product-type iPhone17,4 \\
  --device-class D48AP \\
  --output target-23G83-manifest.json
```

For the iOS 27.0 comparison image, use the catalogue-published SHA-256 above and obtain the exact byte count from the verified local file's size after download. The SHA-256 gate remains the primary integrity control; do not treat catalogue-provided metadata as an Apple-signed attestation.

## Interpretation boundary

- A matching whole-file hash confirms agreement with the pinned digest, not authenticity by itself.
- BuildManifest component digests are metadata values, not independent hashes of the component bytes.
- Different component digests across builds establish only that bytes differ, not that a difference implements a particular CVE fix.
- This inventory is a provenance and component-selection aid, not a patch diff, vulnerability reproduction, exploit, or jailbreak.
- The next evidence tier requires a reproducible extraction of only relevant components in a controlled analysis environment, independent component hashes, tool versions, and a reviewed comparison. Any inferred fix must be tied to public source evidence or a verifiable behavioral invariant; symbol/string differences alone are insufficient.

## Safety status

No exploit executed; no device accessed or modified; no firmware installed, restored, or downgraded. The target IPSW was streamed by CI but not persisted there. The fixed-build component comparison remains pending until locally available verified inputs are analyzed.
