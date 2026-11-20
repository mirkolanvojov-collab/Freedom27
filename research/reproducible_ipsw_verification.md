# Reproducible IPSW checksum verification

## Result: target firmware integrity verified

The exact target IPSW was downloaded to an ephemeral GitHub Actions runner and passed the repository's full-file SHA-256, exact byte-count, and BuildManifest identity checks in [workflow run 40048409001](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40048409001). The run's **Target iOS 26.6.1 build 23G83** job and all seven substantive steps completed successfully. It produced the manifest-only artifact `ipsw-manifest-target-23G83`.

Target: iPhone 16 Plus (`iPhone17,4`), board class `D48AP`, iOS 26.6.1, build `23G83`.

- Official Apple CDN URL: https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw
- Expected and verified SHA-256: `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f`
- Expected and verified size: `11225458130` bytes
- Device-class check: `D48AP`
- Product type check: `iPhone17,4`
- Evidence artifact: `ipsw-manifest-target-23G83` (manifest metadata only; no firmware component extraction or decryption)

## Ten verification checks

1. **Target identity pinned:** model identifier, OS version, and build match `iPhone17,4 / 26.6.1 / 23G83`.
2. **Source pinned:** the input URL is the specific Apple CDN IPSW URL, not a third-party mirror.
3. **Reference digest pinned:** SHA-256 is recorded from independent public firmware catalogues.
4. **Expected size pinned:** the workflow requires exactly 11,225,458,130 bytes.
5. **Full image acquired:** the CI job downloaded the complete IPSW to ephemeral runner storage.
6. **Whole-file SHA-256 checked:** the hash-gated inventory tool exits unsuccessfully if any byte differs from the pinned digest; the target job passed.
7. **Exact byte count checked:** the workflow compares the actual file size against the pinned expected size; the target job passed.
8. **BuildManifest parsed safely:** only the root `BuildManifest.plist` was read after the whole-file checks passed.
9. **Device compatibility checked:** the manifest lists product type `iPhone17,4` and a matching `D48AP` BuildIdentity; the target job passed.
10. **Evidence retained and scope bounded:** the workflow uploaded a manifest-only artifact, removed the downloaded IPSW from runner storage, and did not access or modify a physical device or execute an exploit.

## Provenance and limits

The checksum is corroborated by public firmware catalogues, including [IPSW Downloads](https://ipsw.me/download/iPhone17%2C4/23G83/), [AppleSN](https://applesn.info/firmware/ipsw/iPhone17%2C4/23G83/), and [BetaProfiles](https://betaprofiles.dev/ipsw/ios/26-6-1-23g83/). The file itself was served from Apple's CDN. Matching a catalogue-pinned digest proves that the downloaded bytes match that digest; it is **not by itself an Apple-signed attestation**.

This completes Priority 1's firmware-integrity verification gate. It does not establish that a CVE is exploitable on build 23G83, that a jailbreak chain exists, or that a jailbreak is complete or crash-free.

## Reproducibility

The read-only stream verifier is `research/scripts/verify_ipsw_stream.py`; the hash-gated manifest inventory is `research/scripts/inventory_ipsw_manifest.py`. The successful run and job summaries are available at https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40048409001.
