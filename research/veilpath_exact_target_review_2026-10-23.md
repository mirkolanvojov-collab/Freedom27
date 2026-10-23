# Candidate compatibility check: Veilpath — 2026-10-23

## Purpose

Check whether Veilpath is a suitable next step for Freedom27's recorded iPhone-only setup. This is a public-documentation review, not an installation or device test.

## Freedom27 target

- Device: iPhone 16 Plus (`iPhone17,4`)
- OS: iOS 26.6.1
- Build: `23G83`
- Constraint: development access is iPhone-only; no Mac or Windows PC available.

## Upstream documentation

Project: https://github.com/everettjf/veilpath

The upstream README describes Veilpath as a native container explorer and guarded file workspace built around the `bad_query` sandbox escape. It is a file/container tool, not a complete jailbreak. Its README reports physical-device validation on iPhone 17 Pro running iOS 27 beta 3 and iPad Air running iPadOS 27 beta 3, while warning that not all other versions have been validated. It says simulator builds only validate compilation and UI.

Upstream `bad_query` project: https://github.com/forcequitOS/bad_query

The `bad_query` README labels its project a developer proof of concept and says it is not meaningfully usable as-is. A listed version range is not independent evidence that every device/build combination works.

## Assessment for Freedom27

- Exact target iPhone 16 Plus / iOS 26.6.1 / 23G83: **not independently verified by the cited Veilpath documentation**.
- Full jailbreak, kernel privilege escalation, persistence, tweak injection, and Cydia: **not established by Veilpath's stated purpose**.
- iPhone-only installation and validation path for this exact target: **not established by the documentation reviewed**.
- Safety decision: **do not install or run it on the daily-use device as a supposed jailbreak**.

## Next evidence threshold

Reconsider only if the upstream project publishes an explicit, reproducible result for this exact device and build, with a supported iPhone-only installation path and a clear explanation of what capability is provided. A container explorer should remain classified as a container explorer unless evidence proves more.

## Limitations

This is a source review only. No code was built or executed, and no physical device was tested.
