# Public component-diff reconnaissance — 2026-10-24

## Purpose

This note records a public, third-party firmware-diff lead relevant to the reported target iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1 build `23G83`. It is strictly a static-source review of published diff output. It does not attempt exploitation or claim that a component-level CVE is verified.

## Sources checked

1. Apple's iOS 26.7 security advisory: https://support.apple.com/en-us/149041
2. Public diff index: https://github.com/blacktop/ipsw-diffs
3. Public comparison, iOS 26.6 build 23G71 vs iOS 26.6.1 build 23G83: https://github.com/blacktop/ipsw-diffs/tree/main/iOS/26_6_23G71_vs_26_6_1_23G83
4. Published AppleAVE2 diff: https://github.com/blacktop/ipsw-diffs/blob/main/iOS/26_6_23G71_vs_26_6_1_23G83/KEXTS/com.apple.driver.AppleAVE2.md
5. Published APFS diff: https://github.com/blacktop/ipsw-diffs/blob/main/iOS/26_6_23G71_vs_26_6_1_23G83/KEXTS/com.apple.filesystems.apfs.md
6. Published kernel diff: https://github.com/blacktop/ipsw-diffs/blob/main/iOS/26_6_23G71_vs_26_6_1_23G83/KEXTS/com.apple.kernel.md
7. Public 26.7 vs 26.7.1 comparison: https://github.com/blacktop/ipsw-diffs/tree/main/iOS/26_7_23H24_vs_26_7_1_23H30
8. iPhone 16 Plus firmware catalog: https://ipsw.me/iPhone17%2C4/

## Results and limitations

### The key mismatch: public binary comparison is not for the target model

The comparison README explicitly names inputs `iPhone18,1_26.6_23G71_Restore.ipsw` and `iPhone18,1_26.6.1_23G83_Restore.ipsw`. `iPhone18,1` is not the target's `iPhone17,4`. This makes the comparison a useful lead only; it cannot be represented as an exact-target binary comparison.

### What the published diff says for that other model

- **AppleAVE2:** the published diff reports same-size changed content only in `__TEXT.__cstring`, with the displayed differences being build-time/date strings. This does not prove that no other relevant behavior changed in another model, in a different component packaging, or between 26.6.1 and 26.7.
- **APFS:** the published diff similarly reports same-size changed content only in `__TEXT.__cstring`, showing build-time/date strings.
- **Kernel:** the published diff shows a kernel version change from `12377.162.13.0.0` to `12377.162.14.0.0`, section-size changes, and added strings/assertions, including Exclaves memory checks. This establishes that the kernel binary changed in that comparison, but not that those changes map to any of the 12 tracked CVEs.
- The diff is **26.6 → 26.6.1**, not **26.6.1 → 26.7**. It is not the patch delta for the CVEs whose Apple bulletin says they were fixed in 26.7.

### Exact target and patched-build availability

The public IPSW catalogue lists iOS 26.6.1 build 23G83 for `iPhone17,4`, and also lists later iOS 26.6.2 build 23G90 for the device. Its iOS 26.7 listing does not show a full restore IPSW for `iPhone17,4`; third-party OTA catalogues list OTA artifacts for 26.7/26.7.1. Those OTA packages could be a future patch-baseline source, but this repository has not downloaded, verified, extracted, or compared them. No new OTA artifact should be trusted until its URL, manifest digest, package identity, and downloaded bytes are independently checked.

## Evidence conclusions

- Public component-diff output exists, but the inspected 26.6 → 26.6.1 comparison is for a different hardware identifier.
- The AppleAVE2/APFS summaries in that comparison show only timestamp-string changes; this is not evidence about the 26.6.1 → 26.7 fix delta.
- The kernel summary shows changes, but the changes have not been attributed to CVE-2026-43689 or any other tracked CVE.
- **Exact-target component comparison: still not established.**
- **Patch-level attribution for all 12 CVEs: still not established.**
- **CVE-2026-84607 exploitability/reproduction: still not established.**
- **End-to-end jailbreak: not verified.**

## Next safe evidence gate

Obtain an artifact appropriate to `iPhone17,4` from an authoritative or well-documented public source, verify its package digest and metadata before extraction, and compare exact component versions/hashes against the target build. If a matching 26.7 full IPSW is unavailable, document the OTA extraction pipeline and its verification limitations before using it. For any component delta, retain the component path, build identity, SHA-256, tool/version, and the original diff. Treat binary changes as leads until a public patch or other reproducible source connects them to a CVE.

No exploit was run, no payload was built, and no device was accessed or modified.
