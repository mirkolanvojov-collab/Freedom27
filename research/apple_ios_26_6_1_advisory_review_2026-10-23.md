# Primary-source review: iOS 26.6.1 security advisory

**Reviewed:** 2026-10-23  
**Target:** iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`  
**Primary source:** https://support.apple.com/en-us/148282  
**Decision:** useful for defining patched boundaries; not evidence of an exploitable vulnerability on the target build.

## What the source establishes

Apple's advisory states that iOS 26.6.1 was released on August 17, 2026, and that the update delivers security fixes first made available in iOS 27 / iPadOS 27 betas. It lists issues across several areas, including ImageIO, IOGPUFamily, IOMobileFrameBuffer, Kernel, WebKit and WebRTC. Examples include CVE-2026-65346 (ImageIO arbitrary code execution impact), CVE-2026-64736 (IOMobileFrameBuffer kernel-memory corruption impact), CVE-2026-65343 (Kernel unexpected system termination impact), and CVE-2026-65349 (Kernel out-of-bounds read impact).

The advisory describes these issues as addressed in iOS 26.6.1. Therefore, for a device already running build 23G83, these entries must **not** be treated as ready-made exploit leads without separate evidence that a specific issue remains reachable and unpatched on this exact build. A vulnerability's historical impact is not proof that a usable exploit exists, and a crash or information disclosure is not automatically privilege escalation.

## Evidence assessment

| Question | Assessment |
|---|---|
| Is this an Apple primary source? | Yes |
| Does it establish the target build's current exploitability? | No |
| Does it establish a complete jailbreak chain? | No |
| Can it help map patched boundaries? | Yes |
| Should Freedom27 execute any proof of concept from this advisory? | No; no PoC is provided or authorized |

## Next research action

For each candidate CVE, look for a primary researcher write-up or source revision that explicitly identifies affected and fixed builds, hardware assumptions, and the demonstrated primitive. Record a candidate only if its scope plausibly includes build `23G83`; otherwise mark it `patched_or_out_of_scope` or `unknown`. Do not infer that the prior iOS 27 beta fixes imply a vulnerability remains open in iOS 26.6.1.

## Safety and status

No exploit code was run, no device was modified, and no compatibility claim is upgraded by this review. This is documentation-level triage only.
