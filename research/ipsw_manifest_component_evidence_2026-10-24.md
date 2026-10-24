# Exact IPSW inventory and selected component evidence — 2026-10-24

## Scope

Read-only inventory of the iPhone 16 Plus (`iPhone17,4`, board configuration `D48AP`) target IPSW iOS 26.6.1 build `23G83`. The full firmware was downloaded only to an ephemeral GitHub Actions runner, verified against pinned whole-file SHA-256 and exact size, inventoried, and removed from the runner. The report stores only metadata and hashes, not firmware payloads.

## Whole-image verification

| Field | Target |
|---|---|
| Build | iOS 26.6.1 (`23G83`) |
| Product type / board config | `iPhone17,4` / `D48AP` |
| Whole IPSW SHA-256 | `101aed9c3d5513b598a2b22da7bda5843a051adbe0430f23faed546c1613bd0f` |
| Whole IPSW size | `11225458130` bytes |
| Inventory workflow | https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40048409001 |
| Target inventory job | Passed |
| Firmware persisted in repository | No |
| Device modified / exploit executed | No / No |

## Selected raw IPSW member hashes

After whole-file verification, the inventory script streamed the exact ZIP member bytes for the selected components and computed an independent SHA-256 without extracting them to disk.

| Manifest component | Member path | Raw member size | Raw member SHA-256 | Manifest-provided digest hex |
|---|---|---:|---|---|
| `AVE` | `Firmware/ave/AppleAVE2FW_H17.im4p` | 2,711,801 bytes | `711087234143f97da3c7d60f4dc2b032ee226632f332b81cd4af6abadc25e37d` | `3d4c0dd4094938e36c34f92a7d4709b2888a7248d6983542b071d9b2ade63b57ecde7f832d13f3a11599f5c5f5b2b32d` |
| `KernelCache` | `kernelcache.release.iphone17` | 22,077,586 bytes | `34d04f40e60955ed23ffadc5be6bc79a08fb08cd15d4a67485b0dcab34671113` | `61e6d1ee40452927e7e155b6d2b5501c13a0e652c757d653ab39647cda2dfa945a5c0fc7d8329fe66d26a69078743e2e` |

The manifest-provided digest values are recorded as opaque hex. Their length is 48 bytes in these entries; the independent raw ZIP member hash is explicitly SHA-256 and must not be confused with the manifest digest. The raw member hash is a hash of the exact IPSW member bytes, not a hash of decrypted or unpacked code.

## Identity inventory

The target BuildManifest has three matching `D48AP` build identities:
- Customer Erase Install (IPSW), build 23G83, 103 manifest components.
- Customer Upgrade Install (IPSW), build 23G83, 103 manifest components.
- Recovery Customer Install, build 23G83, 30 manifest components.

The erase and upgrade identities share the selected AVE and KernelCache paths and hashes.

## Fixed-build comparison

The pinned iOS 27.0 build `24A437` full IPSW also passed whole-file verification and BuildManifest inventory in the earlier CI run https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40048100602. Its pinned whole-image SHA-256 is `a8bed747c08709a63e5b9d55fa87bfca2839245f91a82082a8c30b8833fae149`; its observed size is `12313212859` bytes. The selected raw-member SHA-256 comparison for the fixed build is running in workflow https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40048409001 and will be added after the fixed-build artifact is available.

## Interpretation limits

- Different manifest digests or raw ZIP member hashes establish byte differences only.
- iOS 27.0 is a broad version-gap comparison, not a minimal patch release; changes cannot be attributed to a particular CVE based on hash differences alone.
- The Apple iOS 26.7 advisory identifies CVE-2026-84607 as an AVEVideoEncoder race condition fixed with improved state management, but the exact vulnerable code path and its presence/reachability in build 23G83 are not established by this inventory.
- The KernelCache member is a complete kernel cache, not a symbol-level or source-level patch diff. No component was decrypted, disassembled, or executed by this workflow.
- No exploit was built or run, no device was accessed or modified, and no end-to-end jailbreak is verified.
