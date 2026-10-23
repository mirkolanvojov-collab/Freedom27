# Public research review: iPhone 16 Plus / iOS 26.6.1

Review date: 2026-10-23

## Target

- Device: iPhone 16 Plus
- Identifier: iPhone17,4
- OS: iOS 26.6.1
- Build: 23G83

This is a public-source review, not a device test. Freedom27 has not reproduced an exploit on this target.

## Findings

### 1. Public jailbreak status

The Apple Wiki's public iOS 26.x tracker lists no jailbreak tool for iOS 26.6.1. Its current device matrix also lists no jailbreak tool for the iPhone 16 Plus family on current iOS 27.x entries. This is a community-maintained tracker, not an Apple statement and not proof that no private exploit exists.

Source: https://theapplewiki.com/wiki/Jailbreak/26.x
Additional status overview: https://theapplewiki.com/wiki/Jailbreak

### 2. The nearest version-matching lead: bad_query

The upstream README describes a sandbox-escape proof of concept for iOS 26.0–26.6.1 and iOS 27.0 beta 4. It explicitly says it is for developers and is not meaningfully usable at present. It documents access to selected container paths.

Source: https://github.com/forcequitOS/bad_query

Assessment:
- Version overlap with iOS 26.6.1 is a research lead, not proof for iPhone17,4 / build 23G83.
- The README does not establish exact-device reproduction for this target.
- The described sandbox/container access is not itself kernel control, system-wide root, a complete jailbreak, persistence, or Cydia support.
- Freedom27 has not reproduced this behavior. Do not run an untrusted payload on a daily-use device just to check a claim.

### 3. Older-hardware projects do not transfer automatically

Projects with public reports for A12/A13-era hardware cannot be assumed to work on the iPhone 16 Plus. CPU generation, boot chain, mitigations, OS build, host requirements, and tested scope all matter.

Examples to review only within their documented scope:
- https://github.com/Xplo8E/Liter8
- https://github.com/Cyber-Scholar/usbliter8

### 4. What is currently missing

No reviewed public source establishes all of the following for iPhone17,4 / iOS 26.6.1 / 23G83:
1. Reproducible entry vulnerability on this exact target.
2. A reliable path from app/container context to the privileges needed for a jailbreak.
3. Kernel-level access or an equivalent documented route to the required control.
4. A way to handle the relevant code-signing, platform, and runtime protections.
5. A bootstrap/package-manager implementation that works on this exact target.
6. Independent reproduction by Freedom27.

These are research gates, not a promise that each stage must use a separate vulnerability.

## Research decision

Keep the exact target status **unverified / no public jailbreak tool listed**. The highest-value lead to inspect at source level is bad_query, because its stated OS range overlaps the target version. Source review should first establish its technical mechanism, prerequisites, limitations, and whether the code is safe to run in a controlled test environment. Do not infer a working jailbreak from README claims alone.

The next meaningful milestone is a source-level technical review with a reproducible, non-destructive test plan—not an invented exploit. Any test requiring an untrusted payload or modification of the daily-use phone should wait until the behavior, scope, and recovery path are understood.

## Limitations

This review is based on public pages available on the review date. It does not establish that private research does not exist, and it does not test the physical iPhone. Status may change; check the linked upstream sources again before acting.
