# Freedom27 exact-target research triage plan

## Target
- Device: iPhone 16 Plus (`iPhone17,4`)
- OS: iOS 26.6.1
- Build: `23G83`

## Current finding
The Apple Wiki's iOS 26 compatibility table currently lists no tool for iOS 26.6.1 on iPhone 16 Plus. This means no public compatible tool is documented; it does not prove that the target contains no exploitable vulnerability. Source: https://theapplewiki.com/wiki/Jailbreak/26.x

## Prioritized evidence work
1. **Exact-build evidence first.** Only treat a lead as target-specific if a primary source identifies the exact model or hardware family and firmware/build, and explains patch status.
2. **Separate bug from chain.** A CVE or security advisory is not a jailbreak by itself. Record primitive, privilege boundary, mitigation bypass, patch scope, and any public reproducible proof separately.
3. **Do not port older-device assumptions.** Existing Liter8/usbliter8 records describe older hardware; they do not establish A18 compatibility.
4. **Track the reported iPhone 18 Pro demo as a lead only.** A different model/build and news report do not establish a usable public tool or transferability to iPhone 16 Plus.
5. **Require reproduction evidence.** Before changing a status to verified, require a primary technical release and independently repeatable evidence for the exact target. Keep the phone unchanged while no such evidence exists.

## Next technical task
Build a read-only triage command that joins `vulnerability_registry.json` to `evidence_ledger.json`, compares each record with `target_profile.json`, and outputs scope mismatches, patch/reproduction state, and the next evidence gap. This must never label a lead as exploitable based only on a CVE title or a different device's demonstration.

## Limits
GitHub Actions can validate code and research metadata but cannot test the iPhone's hardware, USB/DFU path, or kernel behavior. The current project is a research scaffold, not an installable jailbreak.