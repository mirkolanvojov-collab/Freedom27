# Device crash-safety preflight

**Current decision: BLOCKED — do not run a full jailbreak on the daily-use iPhone.**

The recorded target is iPhone 16 Plus (iPhone17,4), iOS 26.6.1, build 23G83. The repository has no complete jailbreak implementation and no independently reproduced exact-target exploit chain. Its unit tests and GitHub Actions validate research tooling, not device stability.

## Fail-closed gates

Before any future device testing is even considered, each item needs reviewable, target-specific evidence:

- Exact-target chain is independently verified for the exact model and build.
- A current backup is complete and verified.
- A recovery/restore path is available and understood.
- All executable code and dependencies have been reviewed from pinned sources.
- A narrowly scoped non-destructive test passed on the exact target.
- Crash/reboot recovery has been tested on a separate, non-critical test device.
- The project status itself records an independently verified exact-target chain.

Missing or unreviewable evidence blocks the preflight. The machine-readable checklist is research/device_safety_attestations.json; it intentionally starts with every gate missing.

## What the gate does — and does not do

Run python -m Framework.device_safety_gate to print the report. It exits non-zero while blockers remain. The report is a metadata check only: it does not touch the phone, inspect a backup, verify an exploit, or guarantee crash-free execution. A fabricated or superficial attestation is not real validation. No device execution is authorized by this tool.

A jailbreak that reaches kernel-level code can panic or boot-loop a device due to timing, memory corruption, wrong offsets, hardware differences, mitigations, or cleanup errors. No checklist can guarantee zero crashes. The practical way to protect the daily-use phone is not to run unverified exploit code on it; use a dedicated test device and a tested recovery path.
