# Next-step decision: remote iOS build path

**Date:** 2026-10-23  
**Target:** iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`  
**Constraint:** development work is being done from an iPhone only.

## New verified repository checkpoint

The iPhone-only test-readiness documentation passed GitHub Actions:
https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/39981343840

This is a repository check, not a device test.

## What the research establishes

- GitHub Codespaces/browser editing can support source work, but a Linux Codespace does not run Xcode.
- Building and signing an iOS app requires Xcode on macOS. A remote macOS runner or cloud Mac can remove the need to own a Mac, but it does not remove Apple's signing and provisioning requirements.
- Apple documents that physical-device execution requires a signed app and provisioning setup.
- A TestFlight workflow is not automatically appropriate for a jailbreak research payload. The first candidate should be a harmless diagnostic app with no exploit, no privileged operations, no collection of personal app data, and no claims of jailbreak capability.

References:
- Apple, running on physical devices and signing: https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices
- GitHub, signing Xcode applications in Actions: https://docs.github.com/en/actions/how-tos/deploy/deploy-to-third-party-platforms/sign-xcode-applications
- GitHub Codespaces/iOS workflow overview (secondary source): https://nomac.app/blog/github-codespaces-ios-development

## Decision gate before spending money or sharing credentials

Do **not** create a paid cloud-Mac account or upload signing credentials yet. First confirm:
1. Whether the repository contains a native Xcode project or only research tooling.
2. Whether a harmless diagnostic app is actually needed for the next evidence milestone.
3. Whether the user has an Apple account suitable for the intended signing route and accepts any potential cost.

Do not put Apple passwords, private signing keys, API keys, or provisioning secrets in source files or commits. If remote signing is later chosen, use repository/environment secrets with minimum access and a trusted workflow.

## Current conclusion

A remote Mac is a possible future build route, not evidence that a working jailbreak can be produced. The project still lacks a reproducible exact-target test, verified kernel primitive, and complete jailbreak chain. Continue with static source and evidence work until the build/signing path is justified and safely available.
