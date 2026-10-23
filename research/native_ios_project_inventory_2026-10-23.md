# Native iOS project inventory

**Date:** 2026-10-23  
**Repository:** Freedom27  
**Purpose:** decide whether a remote Xcode build is currently the right next step.

## Inventory result

The repository root currently contains project documentation, configuration, research records, a `Framework/` directory, tests, and GitHub Actions workflows. The root listing does not show a native iOS application target such as `.xcodeproj`, `.xcworkspace`, or a Swift Package intended to produce an iOS app.

Therefore, there is no confirmed native app target to build and sign at this checkpoint. Setting up a paid remote Mac now would be premature.

## Decision

Continue with the existing Python research/validation tooling in GitHub Actions. Before creating any iOS app, define a narrowly scoped, harmless diagnostic app only if it is necessary to collect a specific missing evidence item. It must not contain exploit payloads, attempt privilege escalation, or collect personal app data.

## Acceptance criteria for a future app

- Source and purpose reviewed before signing.
- No exploit, persistence, kernel access, or privilege escalation code.
- No unnecessary permissions or private-data collection.
- Build and signing process documented and reproducible.
- Test output reports only the specific capability actually measured.
- No claim of jailbreak compatibility without a physical-device reproduction on the exact target build.

## Status

**Native app target:** not identified in root inventory  
**Remote Mac required now:** no  
**Exact-target device result:** still unverified  
**Next action:** keep improving source-based evidence quality and avoid spending money or exposing signing credentials until an actual app target and test requirement exist.
