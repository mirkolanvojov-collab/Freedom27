# Upstream static review — 2026-10-23

## Purpose and limits

This is a read-only source review of public repositories to assess whether they establish a route to a full Freedom27 jailbreak. No upstream code was built or executed, and no exploit was run on a device. This is not a security audit and does not establish compatibility with the project's exact device (iPhone17,4 / iOS 26.6.1 / build 23G83).

## Revisions reviewed

- `forcequitOS/bad_query`: default-branch source `bad_query/bad_query.c`; repository HEAD observed as `73ef6da1adabef0982fd00e36cb85f21b8f8194a`.
- `jailbreakdotparty/Erosion`: `ErosionManager.swift` and README; HEAD `d16f7f12470458c7028dc274b343a80b85b408be`.
- `pwnapplehat/EscapeOS`: README and `EscapeOS.entitlements`; HEAD `a318e5b576552d66608323fb6b6c3f7d2f1d0fe2`.

## Findings

### 1. bad_query: scoped sandbox access, not a full jailbreak

The C implementation dynamically resolves container-manager and sandbox-extension APIs, constructs a container query, requests a sandbox token, and consumes that token. Its own comments describe selected container paths and specific app-group/system-group routes. It contains explicit cleanup/error returns for failed symbol resolution, query creation, missing results, and token issuance.

What this establishes: the code is a focused sandbox-boundary technique for selected paths when the required OS behavior and privileges are present.

What it does not establish: kernel read/write, arbitrary root execution, disabling code signing, persistence across reboot, or installation of a package manager. A sandbox extension handle is not equivalent to those capabilities. The source's own comments also describe limits around parent-directory access.

### 2. Erosion: customization toolbox that depends on bad_query

The README describes Erosion as an iOS customization toolbox using bad_query, with limited functionality on iOS 26 and some MobileGestalt tweaks unavailable. The manager file exposes UI state for logs, respring requests, and file navigation. These are app/toolbox features, not evidence of a complete jailbreak chain.

The README claims support for selected iOS 26 versions and early iOS 27 developer betas. These are upstream claims; this review did not independently reproduce them, and they do not establish compatibility with Freedom27's exact device/build.

### 3. EscapeOS: app-data file manager, explicitly not a jailbreak

EscapeOS describes itself as an on-device file browser and app-data backup/restore tool using a path-scoped container sandbox escape. It explicitly says “No jailbreak. No Keychain,” limits access to app Data containers, and documents external pairing/setup requirements for app listing. Its entitlement file contains `get-task-allow`, which by itself does not grant arbitrary system privileges.

This is useful as an example of a bounded, testable user-facing workflow, but it is not a substitute for the kernel/root/persistence components needed by a full jailbreak.

## Compatibility status for Freedom27

| Requirement | Evidence in this review | Status |
|---|---|---|
| iPhone17,4, iOS 26.6.1, build 23G83 verified in person | No device test available | **Not verified** |
| Sandbox/container access on exact target | Upstream project claims overlap the OS version; no reproducible Freedom27 test | **Unverified** |
| Kernel privilege escalation | No demonstrated component in these reviewed files | **Missing evidence** |
| Root access / remount or equivalent system modification | Not demonstrated | **Missing evidence** |
| Code-signing / trust bypass needed for broader execution | Not demonstrated | **Missing evidence** |
| Persistence and recovery behavior | Not demonstrated | **Missing evidence** |
| Cydia or another package manager installed by Freedom27 | Not implemented or tested here | **Not done** |
| Automated research engine and safe test-plan tests | Existing Freedom27 CI runs passed | **Passed for repository code only** |

## Next safe engineering gates

1. Preserve this source review and pin any future source conclusions to a commit SHA.
2. Keep the research queue explicit about the boundary between sandbox/container access and full jailbreak privileges.
3. Add tests for Freedom27's own code and validate static assumptions before any device test.
4. Require a full backup and a documented recovery path before any potentially destructive device experiment.
5. Do not label Freedom27 a jailbreak until exact-device evidence demonstrates the required privileges, system modifications, package manager behavior, and recovery/reboot behavior.

## Bottom line

The upstream sources provide a lead for bounded app-container access and customization workflows. They do **not** prove a full jailbreak for iPhone17,4 on iOS 26.6.1 build 23G83. Freedom27's research tooling and CI tests are working as repository software, but Freedom27 is not yet a completed, device-verified jailbreak.
