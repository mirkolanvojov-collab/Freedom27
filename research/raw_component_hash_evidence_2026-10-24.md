# Raw IPSW member hash evidence — 23G83 vs 24A437

Date: 2026-10-24  
Target: iPhone 16 Plus (`iPhone17,4`), board class `D48AP`  
Mode: read-only archive-member hashing; no device interaction or payload execution

## Target build raw-member hashes

The selected-component inventory workflow verified the full target IPSW SHA-256 and size before opening the archive, then streamed the exact uncompressed ZIP member bytes for two selected entries into SHA-256. Evidence artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40048409001 (target job succeeded). The artifact ZIP was retrieved and its JSON contents independently inspected.

| Component | Archive member path | Raw member size | Raw member SHA-256 |
|---|---|---:|---|
| AVE | `Firmware/ave/AppleAVE2FW_H17.im4p` | 2,711,801 bytes | `711087234143f97da3c7d60f4dc2b032ee226632f332b81cd4af6abadc25e37d` |
| KernelCache | `kernelcache.release.iphone17` | 22,077,586 bytes | `34d04f40e60955ed23ffadc5be6bc79a08fb08cd15d4a67485b0dcab34671113` |

Both the Customer Erase Install and Customer Upgrade Install identities point to the same raw member path and produce the same hashes. Recovery Customer Install contains the KernelCache member and the same hash.

## Fixed-build manifest metadata already available

A separately successful hash-gated inventory for iOS 27.0 build `24A437` recorded these manifest-declared digests:

| Component | Manifest path | Manifest-declared digest |
|---|---|---|
| AVE | `Firmware/ave/AppleAVE2FW_H17.im4p` | `c19bac2179d9cd3938156aa6ffc1fbdd707d4db55873922d7e0ec45c096cdb21bf54ff4b8077ff96e704f7130caf1d64` |
| KernelCache | `kernelcache.release.iphone17` | `ea6a41b73ccbcfcae7cb11a558ad4852f04ba427a91bdd560f7274debf3b176b730fde0d2b5448b0b99363b8d10ceb69` |

These manifest digest values differ from the target's corresponding manifest values. This establishes a metadata-level delta only; the values are not raw member SHA-256 values and must not be compared as if they used the same hash algorithm or data representation.

## Fixed-build raw member hashes

The selected-component workflow completed successfully for both builds in run https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40048801314. The fixed-build artifact was retrieved and inspected. Its whole IPSW SHA-256 matched the pinned value `a8bed747c08709a63e5b9d55fa87bfca2839245f91a82082a8c30b8833fae149`; the verified size was 12,313,212,859 bytes.

| Component | Archive member path | Raw member size | Raw member SHA-256 |
|---|---|---:|---|
| AVE | `Firmware/ave/AppleAVE2FW_H17.im4p` | 2,748,385 bytes | `0f054362656bb9e00298692b711f1f007569628cd376ce861a06fa9be275f7a3` |
| KernelCache | `kernelcache.release.iphone17` | 23,406,137 bytes | `a1844ca958421bb8b878ed38c4f3033293baef6302c7bc4cf7b88266e5d7e5af` |

The fixed build's raw AVE and KernelCache member hashes and sizes are now available for direct comparison.

## Interpretation

- Whole IPSW integrity is checked against a pinned SHA-256 and exact size before manifest processing.
- Selected member SHA-256 values hash raw, uncompressed ZIP-member bytes. They do not hash decrypted code.
- AVE is a firmware payload; the public CVE-2026-84607 advisory names AVEVideoEncoder and describes a race condition fixed by improved state management. Similar component names and changed firmware bytes do not prove a direct mapping between that CVE and this firmware payload.
- KernelCache raw bytes differ across OS builds for many reasons. A raw hash difference does not identify the changed code or tie it to CVE-2026-43689.
- The 26.6.1 to 27.0 version gap is broad. Even after raw hashes are compared, attributing a change to one CVE requires source-level evidence, a defensible binary-level mapping, or an independently verified behavioral invariant.

## Next evidence gate

Compare the completed raw SHA-256 values and member sizes across both builds, then determine whether public, non-invasive static analysis can map a specific changed code region to an Apple advisory claim. If the payload is encrypted or otherwise not inspectable without unavailable keys, record that as a hard evidence boundary rather than infer a patch. No exploit or device test is authorized by this research record.

No device was accessed, modified, restored, or downgraded. No exploit code or payload was executed.
