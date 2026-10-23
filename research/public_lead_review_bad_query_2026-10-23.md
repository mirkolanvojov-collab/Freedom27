# Public lead review: bad_query and adjacent projects

**Review date:** 2026-10-23  
**Freedom27 target under review:** iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`  
**Classification:** static public-source review; not a test on the user's device

## Strongest relevant lead: bad_query

- Repository: https://github.com/forcequitOS/bad_query
- Reviewed revision: `73ef6da1adabef0982fd00e36cb85f21b8f8194a`
- README describes a sandbox-escape proof of concept for iOS 26.0–26.6.1 and iOS 27.0 beta 4.
- The README explicitly says it is a developer proof of concept and is not meaningfully usable as-is.
- Documented access is limited to named container and app-data paths. That is not evidence of kernel read/write, arbitrary root, a code-signing bypass, persistence, or a complete jailbreak.

### Exact-target interpretation

The stated iOS 26.0–26.6.1 range includes the reported OS version, but the public README does not establish that this exact device identifier/build has been tested. Therefore:

- Source-level compatibility lead: **yes**
- Exact-device reproduction: **not recorded**
- Full-jailbreak chain: **not established**
- Safe conclusion: investigate only the documented, limited scope; do not claim a full jailbreak.

## Adjacent project cross-checks

### Erosion

- Repository: https://github.com/jailbreakdotparty/Erosion
- Public README states iOS 26.0–26.6.2 support with limited functionality and says some features, including MobileGestalt tweaks, do not work on iOS 26.
- This is a customization toolbox relying on bad_query, not proof of a traditional full jailbreak.
- Its published version range is a lead, not independent proof for this exact phone/build.

### Veilpath

- Repository: https://github.com/everettjf/veilpath
- Public README says it uses bad_query for container exploration and documents physical-device validation on other named devices/builds.
- It explicitly distinguishes Simulator compilation/UI checks from physical-device validation.
- No claim is made here that its validated device is the user's iPhone 16 Plus on build 23G83.

### EscapeOS

- Repository: https://github.com/pwnapplehat/EscapeOS
- Public README describes selected app-data browsing/backup functionality and lists device/build-specific validation for a different iPhone/build.
- This is a useful example of how to record narrow capability and hardware validation; it is not a full-jailbreak demonstration for the target.

## Next evidence gate

1. Keep the immutable source revision and relevant files attached to every research note.
2. Separate upstream claims from behavior independently reproduced by Freedom27.
3. Do not promote the target status beyond `source_supported` without reproducible evidence for the exact device/build.
4. Do not attempt to turn this limited sandbox lead into a privilege-escalation chain based on assumptions. The repository currently contains no verified kernel primitive or complete chain for this target.

## Sources

- bad_query README: https://github.com/forcequitOS/bad_query/blob/73ef6da1adabef0982fd00e36cb85f21b8f8194a/README.md
- Erosion README: https://github.com/jailbreakdotparty/Erosion/blob/main/README.md
- Veilpath README: https://github.com/everettjf/veilpath/blob/main/README.md
- EscapeOS README: https://github.com/pwnapplehat/EscapeOS/blob/main/README.md
