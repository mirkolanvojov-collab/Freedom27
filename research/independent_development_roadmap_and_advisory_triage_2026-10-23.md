# Freedom27 independent development roadmap and advisory triage

**Review date:** 2026-10-23  
**Target under research:** iPhone 16 Plus, reported identifier `iPhone17,4`, iOS 26.6.1, build `23G83`  
**Project rule:** build Freedom27's own research, diagnostics, test infrastructure, and eventual components; do not import or depend on another jailbreak's toolchain. Public security advisories may be used as evidence, not as a substitute for original implementation.  
**Safety boundary:** source review and non-invasive tests only. No exploit execution, installation, downgrade, restore, or device modification is authorized by this document.

## What is and is not complete

Freedom27 already has an evidence-first framework, compatibility/claim checks, research triage, blocker analysis and resolution planning, a read-only security audit, and CI checks. These are useful project infrastructure, not a working jailbreak. CI success means the repository checks passed; it does not mean an exploit works on hardware.

## Advisory triage from Apple's iOS 26.7 security content

Primary source: https://support.apple.com/en-us/149041 (iOS 26.7 and iPadOS 26.7 security content; released 2026-09-14).

| Lead | Apple's published impact | What the public advisory supports | Current Freedom27 status |
|---|---|---|---|
| CVE-2026-43689 — Kernel | Malicious app may gain root privileges; permissions restrictions added | Root-privilege impact; fixed in iOS 26.7 | Highest-priority documented lead; exact build applicability and a reproducible route are not established |
| CVE-2026-86886 — TCC | App may modify protected system files; path traversal / input validation | Protected-file impact; fixed in iOS 26.7 | Relevant boundary lead; no demonstrated target exploit |
| CVE-2026-86876 — CoreMedia | Sandboxed process may circumvent sandbox restrictions; out-of-bounds write / bounds checking | Sandbox-boundary impact; fixed in iOS 26.7 | Relevant boundary lead; no demonstrated target exploit |
| CVE-2026-84566 — Kernel | Local attacker may cause system termination or corrupt kernel memory | Kernel memory impact; improved memory handling | Does not itself establish useful kernel read/write or privilege escalation |
| CVE-2026-84607 — AVEVideoEncoder | Sandboxed app may execute arbitrary code with kernel privileges; race condition / state management | High-impact kernel-privilege description | Requires further source review; do not infer target-specific applicability or reproducibility |
| CVE-2026-43687 — Kernel / NFS | Connecting to malicious NFS server may disclose kernel memory | Potential kernel memory disclosure under a specific server interaction | Environment-dependent; not an established route for the recorded target |
| CVE-2026-43684 / CVE-2026-43686 — Kernel | Kernel memory corruption is reported; exact trigger/subsystem details need individual-entry confirmation | Advisory summary only | Do not infer NFS reachability, a specific bug class, or an exploitable primitive from the combined summary |

Apple's advisory says affected hardware for these entries includes iPhone 11 and later, which encompasses the iPhone 16 generation. That is hardware coverage, not proof that every earlier iOS version or the exact build `23G83` is affected. The advisory is a patch summary, not a technical exploit disclosure.

## Evidence gates for every candidate

For each candidate, maintain separate fields for:
1. Apple advisory text and immutable URL.
2. CVE record and its stated affected/fixed version range.
3. Exact target version/build explicitly named by a trustworthy source, if any.
4. Vulnerability class and security boundary affected.
5. Public technical disclosure / patch-diff evidence, if available.
6. Whether the source describes a bug only, a primitive, or a complete exploit.
7. Reproducibility evidence and environment requirements.
8. Impact on code signing, sandbox, kernel privileges, persistence, and reboot behavior — each separately evidenced.
9. Independent Freedom27 reproduction status. Default: `not_reproduced`.
10. Risk and authorization gate before any device-side testing.

Do not combine separate CVEs into an assumed chain. Compatibility between primitives, reachability, build applicability, mitigations, and ordering must each be supported independently.

## Original Freedom27 workstream — execute in order

### A. Research and target facts
- Keep a source-pinned target manifest for device identifier, OS version, build, and source URLs.
- Build a version/advisory matrix and mark unknowns explicitly.
- Track candidates by evidence level, not by hype or claimed jailbreak status.
- Separate official documentation, third-party claims, and Freedom27's own results.

### B. Own diagnostic and test infrastructure
- Maintain non-invasive device/environment inventory fields the user can provide from Settings; do not ask for sensitive identifiers.
- Add offline parsers and validators for advisory records and compatibility claims.
- Expand deterministic unit tests for version comparison, missing evidence, contradictory claims, and stale source references.
- Keep any generated report reproducible and make CI fail closed when unsupported claims are introduced.

### C. Security-boundary modeling
- Model sandbox, TCC/privacy authorization, code signing/entitlements, kernel authorization/memory protections, and boot/system integrity as separate gates.
- For each gate, define the evidence required to mark it crossed. A root-privilege description alone must not mark kernel read/write, code-signing bypass, persistence, or jailbreak completion as achieved.

### D. Architecture independent of another jailbreak
- Specify Freedom27-owned module interfaces before implementing privileged components.
- Keep the user-space diagnostics, evidence registry, package metadata, and tweak API design separable from any unproven privilege mechanism.
- Document what can be implemented and tested on a stock device versus what requires privileged access.
- Treat Cydia compatibility as a later packaging/integration goal, not evidence of a working jailbreak and not a dependency on another jailbreak's exploit chain.

### E. Acceptance criteria
- `research_lead_confirmed`: credible version/build evidence supports applicability.
- `primitive_demonstrated`: reproducible, scoped evidence supports the claimed capability.
- `chain_verified`: every required boundary and transition is independently evidenced.
- `jailbreak_complete`: end-to-end authorized test establishes the declared behavior, limitations, reboot behavior, and recovery path.
- Until those criteria are met, the status remains blocked/incomplete.

## Current decision

Continue all work that is possible without a device exploit: expand source-backed triage, strengthen original evidence and compatibility tooling, define module interfaces, and test the framework in CI. The advisory leads are worth investigating but none currently establishes a complete Freedom27 jailbreak for build `23G83`. No device was accessed or modified during this review.


## Primary-source verification performed in this review

The Apple iOS 26.7 advisory was searched again on 2026-10-23. The indexed Apple page explicitly lists the following descriptions:
- **CVE-2026-43689 (Kernel):** “A malicious app may be able to gain root privileges”; permissions issue addressed with additional restrictions.
- **CVE-2026-86886 (TCC):** an app may be able to modify protected system files; path traversal addressed with improved input validation.
- **CVE-2026-86876 (CoreMedia):** a sandboxed process may circumvent sandbox restrictions; out-of-bounds write addressed with improved bounds checking.
- **CVE-2026-84607 (AVEVideoEncoder):** a sandboxed app may execute arbitrary code with kernel privileges; race condition addressed with improved state management.
- **CVE-2026-84566 (Kernel):** local attacker may cause unexpected termination or corrupt kernel memory; improved memory handling.
- **CVE-2026-43687 (Kernel/NFS):** connecting to a malicious NFS server may disclose kernel memory.
- **CVE-2026-43684 and CVE-2026-43686 (Kernel):** kernel memory corruption is reported. This summary does not assign a specific bug class or trigger to either CVE; check each individual Apple entry before making that attribution.

Source: Apple Support, “About the security content of iOS 26.7 and iPadOS 26.7,” https://support.apple.com/en-us/149041 (released September 14, 2026; the indexed page shows later additions dated October 19, 2026).

This verification strengthens confidence that the listed impacts appear in Apple's advisory. It does **not** establish that build 23G83 is exploitable, that a public exploit exists, or that any candidates form a compatible chain. The advisory's “iPhone 11 and later” product scope is not itself an affected-version range for every earlier OS build.

## Immediate implementation priorities

1. Add structured, source-pinned candidate records for the leads above to the existing evidence registry rather than leaving the leads only in prose.
2. Add validation that each candidate has a primary URL, source date, claimed fixed release, explicit applicability status, and reproduction status.
3. Add tests that reject claims of target confirmation or jailbreak completion when evidence is only an advisory summary.
4. Keep reports generated by CI deterministic and non-invasive; never run an exploit or modify a device as part of CI.
5. After implementation, inspect the exact GitHub Actions run associated with the new commit. A previous green run is not evidence that a later commit passed.


## Review correction (2026-10-23)

A consistency review found that the earlier summary grouped CVE-2026-43684 and CVE-2026-43686 under NFS and assigned a specific use-after-free mitigation without enough per-entry evidence in this record. Those claims have been removed from the structured candidate data and this document. The corrected entries deliberately retain only the broad kernel-memory-corruption impact pending individual-source confirmation. This is a correction of over-specific attribution, not a change in target applicability or exploit status.
