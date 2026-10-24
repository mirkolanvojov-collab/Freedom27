# Exact-target IPSW manifest comparison: 23G83 vs 24A437 — 2026-10-24

## Result

The project completed a hash-gated download and metadata inventory for both full IPSWs on the same device family and board configuration, then compared their BuildManifest metadata. The successful workflow is https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40048290511.

| Property | Target | Fixed comparison baseline |
|---|---|---|
| Product type | `iPhone17,4` | `iPhone17,4` |
| Board / BuildManifest device class | `D48AP` / `d48ap` | `D48AP` / `d48ap` |
| Build | iOS 26.6.1 / `23G83` | iOS 27.0 / `24A437` |
| Build train | `LuckG` | `Rave` |
| Whole-file SHA-256 | `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f` | `a8bed747c08709a63e5b9d55fa87bfca2839245f91a82082a8c30b8833fae149` |
| Whole-file size | `11225458130` bytes | `12313212859` bytes |
| Manifest identities | 3 | 3 |

The target image's SHA-256 and exact size match the previously pinned values. The comparison IPSW's SHA-256 matches the pinned catalogue digest; its observed byte count is recorded above. Catalogue hashes are not Apple-signed attestations.

## Artifact provenance

- Successful inventory workflow: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40048290511
- Target manifest artifact: [ipsw-manifest-target-23G83](https://api.github.com/repos/mirkolanvojov-collab/Freedom27/actions/artifacts/12542162700) (artifact ZIP SHA-256 `4ee25bf107a63be54ffafcc152a499fb9bff8f2148e7af3c7eed671b8cf3af85`)
- Fixed-build manifest artifact: [ipsw-manifest-fixed-24A437](https://api.github.com/repos/mirkolanvojov-collab/Freedom27/actions/artifacts/12542436352) (artifact ZIP SHA-256 `3b77b73b026735cafbc36c859292ec7c7a178b469548dc695aef597d931f230d`)
- Target IPSW source: https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-75160/D83A8969-3179-4D59-9F72-37FFC825CD9A/iPhone17,4_26.6.1_23G83_Restore.ipsw
- Fixed-build IPSW source: https://updates.cdn-apple.com/2026FallFCS/601712cb-7aa9-4914-b421-91d45da959e6/iPhone17%2C4_27.0_24A437_Restore.ipsw

The workflow downloaded each image to a separate ephemeral runner, verified the whole-file digest before reading the manifest, and uploaded only the small JSON inventory. The firmware files were not committed to the repository or retained as workflow artifacts.

## Manifest comparison

The comparison keys entries by both install variant and component name, avoiding collisions where a component name appears in multiple BuildIdentity variants.

| Variant | Target entries | Fixed entries | Shared | Metadata-changed shared entries | Added in fixed | Absent in fixed |
|---|---:|---:|---:|---:|---:|---:|
| Customer Erase Install (IPSW) | 103 | 103 | 102 | 81 | 1 | 1 |
| Customer Upgrade Install (IPSW) | 103 | 103 | 102 | 81 | 1 | 1 |
| Recovery Customer Install | 30 | 30 | 30 | 30 | 0 | 0 |
| **Total variant/component entries** | **236** | **236** | **234** | **192** | **2** | **2** |

Across shared entries, the manifest-declared digest field differed for 158 variant/component entries and the path field differed for 72. These field counts overlap; they are not a count of unique affected components.

The two added entries are `Yonkers,SepObject` (path `Firmware/all_flash/sep-firmware.d48.RELEASE.im4p`) in the erase and upgrade variants. The two absent entries are `Ap,HapticAssets` (path `Firmware/D48_HapticAssets.im4p`) in those same variants.

## Priority technical lead: AVE firmware metadata changed

In both customer install variants, the `AVE` manifest entry points to `Firmware/ave/AppleAVE2FW_H17.im4p`, and its manifest-declared digest changes:

- Target `23G83`: `3d4c0dd4094938e36c34f92a7d4709b2888a7248d6983542b071d9b2ade63b57ecde7f832d13f3a11599f5c5f5b2b32d`
- Comparison `24A437`: `c19bac2179d9cd3938156aa6ffc1fbdd707d4db55873922d7e0ec45c096cdb21bf54ff4b8077ff96e704f7130caf1d64`

The `KernelCache` manifest-declared digest also changes while the path remains `kernelcache.release.iphone17`.

**Interpretation:** this is a concrete, reproducible metadata delta on the exact product type and board configuration, and it prioritizes the AVE firmware component for further static analysis. It is **not** proof that the change fixes CVE-2026-84607. The advisory describes an AVEVideoEncoder race condition; the `AVE` entry here is a firmware component, not a source-level mapping to the vulnerable driver or function. The initial metadata comparison did not hash component payloads. A later selected-component CI run completed raw ZIP-member SHA-256 hashing for both builds (see `research/raw_component_hash_evidence_2026-10-24.md`). The AVE member grew by 36,584 bytes and the KernelCache member by 1,328,551 bytes; both raw hashes differ. These results establish byte-level differences only. Neither workflow decrypts or inspects the kernel extension inside the system volume, identifies a patch hunk, or demonstrates vulnerable-code reachability on build `23G83`.

The broad change count is expected when comparing iOS 26.6.1 with iOS 27.0. This is a fixed-release baseline with a larger version gap, not a minimal patch diff. No individual metadata difference should be attributed to one CVE without additional evidence.

## What this resolves and what remains

Resolved:
- Independently verified full-file SHA-256 and size for the target IPSW.
- Downloaded and hash-verified a same-product fixed-release comparison IPSW.
- Captured both BuildManifest inventories and compared entries by install variant and component name.
- Identified the AVE firmware manifest digest delta as a concrete next static-analysis lead.

Still unresolved:
- Raw AVE and KernelCache ZIP-member hashes and sizes are recorded for both builds. These are hashes of uncompressed archive-member bytes, not decrypted executable-code hashes.
- No source-level or binary patch diff tying the AVE firmware or kernel code changes to CVE-2026-84607.
- No exact-build vulnerable-code reachability proof for `23G83`.
- No candidate CVE reproduced by Freedom27 and no verified end-to-end jailbreak.

No device was accessed or modified. No payload or exploit was run.
