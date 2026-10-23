# EscapeOS compatibility evidence review — 2026-10-23

## Target
- Device: iPhone 16 Plus (iPhone17,4)
- OS: iOS 26.6.1
- Build: 23G83
- Assessment type: public-source review only; no device execution

## Public lead
- Repository: https://github.com/pwnapplehat/EscapeOS
- Related upstream project: https://github.com/forcequitOS/bad_query
- EscapeOS documents limited app-container browsing/backup functionality using bad_query.
- Its documentation reports testing on an iPhone 17 running iOS 26.5.1. This is a different model and build.
- The documented OS version range overlapping iOS 26.6.1 is not evidence that this exact target is compatible.
- App discovery documentation describes a pairing-file and LocalDevVPN dependency on newer OS versions; the documented setup is not established as iPhone-only.

## Source review observations
- EscapeOS AppDiscovery.swift states that installed-app enumeration requires a pairing file and local tunnel.
- EscapeOS SandboxEscape.swift wraps bad_query and tracks/releases returned handles.
- EscapeOS Engine/bad_query.c dynamically resolves private container-management and sandbox-extension APIs. Its error paths show that successful access is not guaranteed.
- These source details are descriptive findings, not instructions to execute or modify an exploit.

## Evidence classification
- OS-range claim: documented upstream/project claim; not independently verified here.
- Physical-device report: iPhone 17 / iOS 26.5.1; not the exact target.
- Exact target iPhone17,4 / 23G83: NOT VERIFIED.
- Kernel primitive or privilege escalation: NOT ESTABLISHED.
- Persistence/bootstrap/package manager/Cydia: NOT ESTABLISHED.
- Complete jailbreak: NOT ESTABLISHED.
- Freedom27 physical-device test: NOT PERFORMED.

## Next evidence gate
Find a public, reproducible primary-source report matching iPhone17,4 and build 23G83, or retain the blocked status. Do not infer compatibility from a version range or from a different device. Do not run unreviewed payloads on the daily-use phone as a substitute for evidence.

## Limitations
This is a source/documentation review, not an independent validation, security audit, or device test.