# Source review checkpoint — 2026-10-23

This checkpoint records repository structure and public documentation reviewed for Freedom27. It does **not** claim that upstream exploit source has been independently validated or run.

## CI status

The most recent Freedom27 GitHub Actions runs for the research engine, safe test planner, documentation, and research queue completed successfully. This confirms automated checks passed for those commits; it does not prove iOS behavior.

- Research engine tests: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/39979301576
- Safe test planner tests: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/39979432448
- Research queue integrity: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/39979484426

## bad_query

Repository: https://github.com/forcequitOS/bad_query

Public tree includes a Swift UI entry point, a C source file (bad_query/bad_query.c), C headers/bridging header, app entitlements, and an Xcode project. This indicates a native iOS app with a C implementation component; file layout alone does not establish mechanism, safety, or exact-device compatibility.

The upstream README calls it a sandbox-escape proof of concept for iOS 26.0–26.6.1 and iOS 27 beta 4 and explicitly says it is not meaningfully usable at present. It describes selected container paths rather than kernel control, system-wide root, persistence, or Cydia.

**Disposition:** mechanism review remains open. Next review must examine the C implementation, entitlements, project settings, dependencies, and exact upstream revision before any test. Do not execute the app or payload during static review.

## Erosion

Repository: https://github.com/jailbreakdotparty/Erosion

Public tree includes Swift app/UI files, ErosionManager.swift, an Exploits directory, file-manager code, tweak code, and a bridging header. This is consistent with an app coordinating customization and file-operation features, but structure alone does not prove a specific feature works on a given build.

The public README describes limited iOS 26.0–26.6.2 functionality and notes that some MobileGestalt-related tweaks are unavailable on iOS 26. The target OS version overlaps that broad range, but exact iPhone17,4 / build 23G83 compatibility has not been established by Freedom27.

**Disposition:** static review pending for ErosionManager.swift, Exploits, and individual tweak implementations. Do not install or run it on the target phone during initial review.

## EscapeOS

Repository: https://github.com/pwnapplehat/EscapeOS

Public tree includes application source, entitlements, build instructions, tests, vendor code, and documentation. The repository also contains a license and notice, which must be reviewed before reusing any code. Freedom27 will not copy code without checking license and attribution requirements.

Public descriptions position EscapeOS as a selected app-data/container access and management tool. That is materially narrower than a full jailbreak. Reports for another phone/build cannot be used as exact-target evidence for iPhone17,4 / 23G83.

**Disposition:** review build instructions, entitlements, tests, dependencies, and data-modification behavior before deciding whether any test can be performed safely.

## Corrected conclusion

The public research surface has concrete leads: a sandbox-escape PoC and related container/customization apps exist for some iOS 26 builds. This still does not demonstrate a full jailbreak, kernel/root access, persistence, or Cydia support on the exact target.

The immediate engineering task is static source review with exact upstream revisions and licensing—not running third-party payloads. Only after that review should a narrowly scoped, non-destructive test be considered.
