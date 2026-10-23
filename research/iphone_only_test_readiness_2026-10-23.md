# Exact-target test readiness: iPhone-only workflow

**Target recorded by Freedom27:** iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`  
**Current status:** no exact-target test result recorded  
**Purpose:** identify what can and cannot be validated from an iPhone-only setup

## Current CI result

The previous public-lead assessment passed GitHub Actions. That validates repository automation and report integrity only. It does not run an iOS app on the user's phone or prove a sandbox escape.

Run: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/39981188282

## Device testing constraint

The public Veilpath instructions require Xcode 27 beta, an Apple development team for signing, and a physical iPhone/iPad for validating the access path. GitHub's hosted Linux CI cannot substitute for the iOS/Xcode build and physical-device run. With an iPhone-only development setup, there is currently no confirmed, reproducible build-and-install path in Freedom27 that yields a trustworthy test result.

Source: https://github.com/everettjf/veilpath

## Do not treat these as test evidence

- A README's supported version range
- A GitHub Actions green check
- A Simulator build
- An unsigned IPA or an unknown download site
- A configuration profile from an unknown source
- A screenshot that does not show the exact device/build and test result

## Safe evidence record

When a trusted, properly signed diagnostic build and supported install route are available, capture the following without collecting private app data:

- Device model identifier:
- iOS version:
- Build number:
- Diagnostic app name and version:
- Exact source commit:
- Signing/distribution route:
- Self-test report file name:
- Test name:
- Pass/fail/inconclusive:
- Error text (redact personal data):
- What capability was actually tested:
- What the result does **not** establish:

Do not share app container contents, tokens, personal files, or diagnostic archives containing private data.

## Next milestone

First establish a legitimate way to build and sign a minimal, source-reviewed diagnostic app for the physical device. Only then run a narrow, non-destructive self-test and record the output. Until that is possible, the honest status remains **source lead identified; exact-target behavior unverified**.

No downgrade, restore, profile installation, or unreviewed payload is needed for this research checkpoint.
