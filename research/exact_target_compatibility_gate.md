# Freedom27 exact-target compatibility gate

**Status:** blocked / research only  
**Last reviewed:** 2026-10-23  
**Configured target:** iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`

This gate prevents a nearby version, another device, a README claim, or a passing repository test from being mistaken for a working jailbreak on the configured target.

## Required evidence by milestone

| Milestone | Minimum acceptable evidence | Current status |
|---|---|---|
| Source provenance | Exact upstream URL, immutable commit, reviewed files, license noted | Partially documented for reviewed leads |
| Target match | Device identifier and exact OS build match the configured target | Not demonstrated on the physical device |
| Entry-point behavior | Reproducible observation on the exact target, with expected and falsifying observations | Not demonstrated |
| Privilege boundary | Evidence of the specific privilege needed; do not infer kernel access from app-container access | Not demonstrated |
| System modification | Harmless, reversible proof that the required system boundary was crossed | Not demonstrated |
| Tweak loading | A minimal test component loads and can be removed cleanly | Not implemented / not demonstrated |
| Package management | Install, verify, remove, and rollback a harmless test package | Not implemented / not demonstrated |
| Persistence and recovery | Documented respring/reboot behavior and a tested recovery path | Not demonstrated |
| Independent reproduction | A second clean run with logs and matching target/build | Not demonstrated |

## Evidence rules

1. **Repository CI is not device validation.** Unit tests establish that the research tools behave as coded; they do not establish that an iOS vulnerability exists.
2. **A version range is not proof for this build.** Record the exact device identifier, iOS version, and build for every claimed result.
3. **Keep capability claims narrow.** App-container file access does not prove kernel read/write, root, code-signing bypass, persistence, or package-manager support.
4. **No inferred success.** A milestone stays blocked until its stated evidence exists and is reviewable.
5. **Do not test destructive or unreviewed payloads on the daily-use phone.** Use a reversible, harmless test and a recovery plan.
6. **Cydia is a downstream milestone.** Do not claim compatibility until the required privilege and tweak-loading foundations are proven.

## Current conclusion

Freedom27 has a functioning research scaffold and passing repository automation, but no reviewed evidence currently demonstrates a complete jailbreak on the configured target. The next useful milestone is a source-backed, falsifiable hypothesis for one specific security boundary—not a claim that the full chain already exists.

## Result record template

For each new experiment, record:

- Hypothesis ID:
- Exact source URL and immutable revision:
- Device identifier:
- iOS version and build:
- Preconditions:
- Non-destructive procedure:
- Expected observation:
- Falsifying observation:
- Actual result and log location:
- Recovery steps:
- Reviewer / independent reproduction:
- Narrow conclusion supported by the evidence:
