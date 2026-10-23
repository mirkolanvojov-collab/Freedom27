# Historical iOS 26.5.2 advisory leads relevant to Freedom27

**Reviewed:** 2026-10-23  
**Target:** iPhone 16 Plus / `iPhone17,4` / iOS 26.6.1 / build `23G83`

Primary Apple source: https://support.apple.com/en-us/127594

Apple states iOS 26.5.2 was released June 29, 2026 and delivered security fixes first made available in the iOS 26.6 beta. Since the target is iOS 26.6.1, the entries below were fixed in an earlier release and must not be labelled known-unpatched issues on the target.

| CVE | Component | Apple-published impact | Fix | Target disposition |
|---|---|---|---|---|
| CVE-2026-43743 | IOGPUFamily | App may cause unexpected system termination | Race condition; improved state handling | Fixed before target release; not an unpatched lead |
| CVE-2026-43724 | Kernel | App may cause unexpected system termination or write kernel memory | Improved input sanitization | Fixed before target release; not an unpatched lead |
| CVE-2026-43722 | Kernel | App may leak sensitive kernel state | Improved input sanitization | Fixed before target release; not an unpatched lead |
| CVE-2026-39868 | Kernel | App may cause unexpected system termination or corrupt kernel memory | Improved input validation | Fixed before target release; not an unpatched lead |
| CVE-2026-43735 | WebKit | Malicious website may exfiltrate data cross-origin | Improved checks | Fixed before target release; not an unpatched lead |
| CVE-2026-43725 | WebKit | Malicious website may process restricted web content outside the sandbox | Improved input validation | Fixed before target release; not an unpatched lead |
| CVE-2026-43731 | WebKit | Malicious web content may cause memory corruption | Use-after-free; improved memory management | Fixed before target release; not an unpatched lead |
| CVE-2026-43705 | WebKit | Malicious website may process restricted web content outside the sandbox | Improved checks | Fixed before target release; not an unpatched lead |

The advisory includes additional entries, particularly numerous WebKit issues. This is a prioritised subset, not a complete transcription. The CVE descriptions above are Apple advisory summaries, not proof of an exploit, exact build applicability, or a compatible chain.

## What the evidence means

- Hardware applicability listed as “iPhone 11 and later” includes the device family, but does not prove a particular earlier build is affected.
- Fixes released in 26.5.2 and 26.6 are not valid leads for a 26.6.1 target unless independent evidence demonstrates a regression or an unpatched variant.
- The next coverage task is to enumerate every Apple advisory from iOS 26.0 through 26.6.1, preserving every CVE and first fixed release, then deduplicate the set and validate against CVE.org/NVD.
- No exploit was run and the device was not accessed or modified.

## Sources

- Apple Support, “About the security content of iOS 26.5.2 and iPadOS 26.5.2”: https://support.apple.com/en-us/127594
- Apple Support, “Apple security releases”: https://support.apple.com/en-euro/100100
