# Freedom27 Compatibility Target Matrix

## Goal

Freedom27 aims to investigate jailbreak feasibility across the iPhone 14 through iPhone 18 families on iOS 26 and iOS 27. This is a project goal, not a claim that these devices or builds are currently supported.

## Scope

- Hardware families: iPhone 14, 15, 16, 17, and 18, tracking **base, Plus, Pro, and Pro Max** as separate variants wherever that variant exists for the family.
- Do not assume every family has every variant: model availability changes by generation. Confirm each exact model identifier before treating a row as a real target.
- OS families: iOS 26 and iOS 27.
- Compatibility must be tracked per exact model identifier, chip/platform, OS version, and build number.
- Package-manager preference: Cydia, while keeping the design open to other maintained package managers if required by platform constraints.
- User experience goal: an accessible workflow with clear prerequisites and the fewest possible steps.

## Evidence policy

A device/build combination is **verified** only after reproducible evidence exists for that exact combination. A successful demonstration on one model or build does not establish support for another.

Each matrix entry should use one of these statuses:
- `not-investigated`
- `researching`
- `theoretical`
- `experimental`
- `verified`
- `not-supported`

Do not describe the project as an installable jailbreak until a compatible implementation is publicly buildable, its required steps are documented, and tests or device evidence support the claim.

## Current evidence and constraints

- The public Liter8 project documents iPhone 11/A13 support and requires a Mac; it is not evidence for iPhone 14–18 support or an iPhone-only workflow: https://github.com/Xplo8E/Liter8
- A reported iPhone 18 Pro/iOS 27.0.1 untethered demonstration is not, by itself, a public tool or a compatibility matrix: https://www.iclarified.com/102876/untethered-ios-2701-jailbreak-demonstrated-on-iphone-18-pro-video
- iOS 26 and iOS 27 builds must be tracked separately. Point releases and security patches may change exploitability.
- The development environment currently available to the project owner is iPhone-only. Host-side builds that require macOS/Xcode cannot be assumed feasible on that device alone; cloud CI can test supported project checks but cannot replace real-device validation.

## Next engineering gates

1. Maintain a sourced registry of public research and exact compatibility claims.
2. Build a model/build matrix with evidence links and explicit unknowns. The JSON matrix now has separate variant rows for base, Plus, Pro, and Pro Max across iPhone 14–18; rows for combinations that may not exist are placeholders requiring verification.
3. Add automated validation that prevents unsupported compatibility claims.
4. Evaluate whether a practical iPhone-only build/install workflow is possible; record any external-host requirement honestly.
5. Only then consider implementation work tied to a specific, documented vulnerability and exact supported build.

## Non-goals

- No claim of universal compatibility.
- No claim that an exploit demonstrated on one device transfers to another.
- No destructive restore or installation steps without explicit warnings, verified prerequisites, and a recoverability plan.
