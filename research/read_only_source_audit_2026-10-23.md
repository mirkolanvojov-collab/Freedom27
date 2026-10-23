# Freedom27 read-only research audit — 2026-10-23

## Scope and safety

This is a documentation-only review of public project descriptions. No proof-of-concept was built or run, no device was tested, and no device or repository state was changed as part of the source review that preceded this note. This note does not provide an exploit recipe.

Target recorded by Freedom27: iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`.

## Findings

### Apple CVE attribution

Primary source: https://support.apple.com/en-us/148282

Apple's advisory identifies CVE-2026-65343 as a kernel use-after-free and CVE-2026-65349 as a kernel out-of-bounds read. The third-party page below gives a more specific AppleKeyStore / KASLR explanation for CVE-2026-65343. That detailed attribution is not established by the Apple advisory alone.

Third-party source: https://github.com/ByteV0rtex/CVE-2026-65343

The third-party page itself states that its reported affected scope is iOS 26.6 (23G71) and earlier and that the issue is fixed in iOS 26.6.1 (23G83). Its claim therefore does not establish a working vulnerability on Freedom27's recorded target. No proof-of-concept was run and no independent reproduction was performed.

### bad_query

Source: https://github.com/forcequitOS/bad_query

The upstream README describes this as a developer proof of concept and says it is not meaningfully usable as-is. Container/sandbox access must not be treated as proof of kernel control, system-wide privilege escalation, persistence, package-manager compatibility, or a complete jailbreak.

### Erosion

Source: https://github.com/jailbreakdotparty/Erosion

The README describes a customization toolbox using bad_query and lists limited functionality on iOS 26, including lack of MobileGestalt tweaks. These claims do not establish a full jailbreak or Freedom27 compatibility on the exact target.

### EscapeOS

Source: https://github.com/pwnapplehat/EscapeOS

The README describes app-container browsing and backup/restore, not a full jailbreak. Its documented installation/pairing workflow includes a Windows host for initial setup, so it is not an end-to-end iPhone-only setup as documented.

## Decision

- Keep Freedom27's exact-target status as `blocked` / unverified.
- Do not install or run these projects on the daily-use phone as a substitute for evidence.
- Do not downgrade, restore, install unknown profiles, or execute unreviewed payloads.
- Revisit only when primary evidence or a release documents a compatible, independently verifiable result for iPhone 16 Plus / iOS 26.6.1 / 23G83.
- Treat CI as validation of repository tooling and metadata only, not as a test of the physical iPhone.

## Review limitations

This is a source-documentation review, not an independent technical reproduction or a complete audit of all source files and commit history.
