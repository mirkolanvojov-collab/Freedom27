# bad_query compatibility review

Review date: 2026-10-23

## Target under review

- Device: iPhone 16 Plus
- Model identifier: iPhone17,4
- OS: iOS 26.6.1
- Build: 23G83

## Primary-source findings

Source: https://github.com/forcequitOS/bad_query

The upstream README describes `bad_query` as a sandbox-escape proof of concept for iOS 26.0–26.6.1 and iOS 27.0 beta 4. It explicitly says it is for developers and is not meaningfully usable at present. Its documented scope is access to selected application, internal-daemon, plug-in, and App Group container paths; some paths differ by OS version and the iOS 26 App Group route has an additional requirement.

The repository contains an Xcode project, Swift UI code, a C implementation, headers, and entitlements. This is source code for an Apple-platform app, not a prebuilt, signed installation package. Building and signing an iOS app normally requires Xcode and an Apple development signing setup, which the current iPhone-only workflow does not provide directly.

## What this establishes

- The claimed OS-version range includes the user's reported iOS 26.6.1 version.
- The upstream README does not name iPhone 16 Plus / iPhone17,4 or build 23G83 as independently tested.
- The upstream project labels itself a proof of concept, not a usable jailbreak.
- A sandbox escape is not proof of kernel privilege escalation, arbitrary code execution in privileged processes, system-volume modification, persistence, or a Cydia-compatible package manager.
- Freedom27 has not reproduced this result on the exact target.

## Decision

Status remains **unverified for the exact target**. Keep this lead for compatibility tracking only. Do not present it as an installable jailbreak or recommend installing unsigned builds, profiles, or unknown packages based on this finding.

## Verification needed before changing status

1. A primary-source statement or reproducible test naming iPhone 16 Plus / iPhone17,4 and build 23G83.
2. Independent, non-destructive validation of the documented container-access behavior on that exact device/build.
3. Separate evidence for any stronger capability claimed; container access alone is not a jailbreak.
