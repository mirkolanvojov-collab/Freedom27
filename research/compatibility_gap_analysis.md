# Compatibility Research Gap Analysis

Reviewed: 2026-10-23

## What the public evidence currently says

### iPhone 18 Pro / iOS 27.0.1

Public reporting describes a Calif demonstration on an iPhone 18 Pro running iOS 27.0.1, build 24A446. The report describes root access that persisted across a reboot. The report also states that the vulnerabilities, implementation, and release timeline were not public at publication time.

Sources:
- https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- https://www.iclarified.com/102876/untethered-ios-2701-jailbreak-demonstrated-on-iphone-18-pro-video

Interpretation: mark the exact reported combination experimental, not verified. This does not establish compatibility with iPhone 14–17, other iPhone 18 variants, iOS 26, or any other iOS 27 build.

### Liter8 / usbliter8

The upstream Liter8 README states that its documented target is iPhone 11 (n104ap, A13), with a tethered workflow requiring a Mac and host-side tools. The README explicitly limits its tested claim to iPhone 11 and lists incomplete features.

Source:
- https://github.com/Xplo8E/Liter8

Interpretation: this project is useful as architecture and historical research context, but not as a ready-made path for Freedom27's iPhone 14–18 target or iPhone-only development constraint.

## Compatibility matrix rules

1. Every positive claim must identify an exact device/model identifier, iOS version, build number, and evidence source.
2. A conference demo is recorded as experimental until the relevant method is independently reproducible or supported by a public implementation with matching evidence.
3. A result on one device family or build must not be extrapolated to another.
4. A successful CI run proves only the checks actually executed; it does not prove device exploitability.
5. Do not install experimental firmware or run restore workflows on a personal device as a substitute for reproducible evidence.

## Highest-value next work

1. Track the public Calif disclosure/release and extract any exact supported models/builds once primary technical evidence appears.
2. For every iPhone 14–18 family, fill exact model identifiers and the actual OS/build combinations that exist, rather than treating a family name as one device.
3. Keep iOS 26 and iOS 27 separate; include patch-level builds.
4. Review whether the Freedom27 goal can be met without a Mac. Existing Liter8 instructions require a Mac; GitHub Actions is useful for tests but does not replace USB/DFU access to a physical iPhone.
5. Delay exploit-specific implementation claims until a public, applicable vulnerability and reproducible target-build evidence exist.

## Current conclusion

The matrix has one experimental evidence row for the reported iPhone 18 Pro / iOS 27.0.1 build 24A446 demonstration. It has no verified Freedom27 compatibility rows. This is the honest current state; no installable Freedom27 jailbreak is available from this repository.
