# Freedom27 — iOS 26.7 patch-evidence matrix (read-only)

**Reviewed:** 2026-10-23  
**Target:** reported iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`  
**Primary source:** https://support.apple.com/en-us/149041  
**Baseline source:** https://support.apple.com/en-us/148282  
**Scope:** public advisory interpretation and research planning only. No CVE was cracked, executed, or reproduced; no device was accessed or modified.

## What the source establishes

Apple's iOS 26.7 advisory says it was released September 14, 2026. It lists supported hardware beginning with iPhone 11 and later, which includes the reported device family. The advisory identifies fixes and high-level impacts, but it does **not** itself establish whether a particular vulnerability is present in the reported 26.6.1 build, whether a usable primitive exists, or whether several bugs can be composed into a jailbreak.

The user's reported 26.6.1 build predates the 26.7 release. That makes later fixes legitimate *patch-diff research leads*, not proof of a vulnerability. Exact build mapping and affected-version scope still require evidence.

## Priority patch-evidence matrix

| CVE | Component | Apple-published impact / fix summary | What to establish next | Current conclusion |
|---|---|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder | Sandboxed app may execute code with kernel privileges; race condition fixed with improved state management | Find public implementation/bug references; compare publicly available affected and fixed source where available; determine whether 26.6.1 is in affected scope | High-value lead; unverified on target |
| CVE-2026-43689 | Kernel | Malicious app may gain root; permissions issue fixed with additional restrictions | Identify affected permission path and version boundary from public evidence; distinguish root from kernel privilege | High-value lead; unverified on target |
| CVE-2026-84523 | APFS | App may cause system termination or write kernel memory | Locate public bug/patch references; determine whether “write kernel memory” is controllable or merely impact wording | High-value lead; primitive unproven |
| CVE-2026-86876 | CoreMedia | Sandboxed process may circumvent sandbox restrictions; out-of-bounds write fixed with bounds checking | Determine affected media parsing path and whether patch changes behavior on target version | High-value lead; unverified |
| CVE-2026-86886 | TCC | App may modify protected system files; path traversal fixed with input validation | Establish path-handling boundary, required entitlements, and fixed-version range | High-value lead; unverified |
| CVE-2026-84566 | Kernel | Unexpected termination or kernel-memory corruption; improved memory handling | Identify public patch details and whether a non-destructive regression test is possible | Memory-safety lead; exploitability unknown |
| CVE-2026-43687 | Kernel / NFS | Malicious NFS server may disclose kernel memory; improved memory handling | Establish preconditions, NFS reachability and exact fix boundary | Requires server-side interaction; target applicability unknown |
| CVE-2026-43684 | Kernel | Unexpected termination or kernel-memory corruption; use-after-free fixed with memory management | Locate public patch context and affected-version evidence | Memory-safety lead; exploitability unknown |
| CVE-2026-43686 | Kernel / NFS | Malicious NFS server may cause kernel memory corruption; use-after-free fixed with memory management | Establish preconditions and whether target's shipped code contains the vulnerable path | Requires server-side interaction; target applicability unknown |
| CVE-2026-65405 | Kernel | App may determine kernel memory layout; memory initialization fixed | Assess whether the leak meaningfully weakens mitigations and whether it is independently reachable | Information-disclosure lead; chain relevance unknown |
| CVE-2026-84622 | Kernel | App *with root privileges* may read uninitialized kernel memory | Treat as post-root only; do not count as an initial privilege-escalation bug | Not an initial-entry candidate |

**Note:** The table is a prioritized subset, not a complete count of all iOS 26.7 CVEs. The APFS entry appears once.

## Evidence checklist for each candidate

A candidate may be upgraded beyond “public advisory only” only when the repository records:

1. **Primary-source evidence:** exact Apple advisory section and date, with CVE ID and component.
2. **Version evidence:** public evidence that identifies the vulnerable and fixed version boundary; do not infer the vulnerable range solely from the release in which a fix appeared.
3. **Patch evidence:** a public patch, source change, bug tracker entry, or other reproducible source that explains the corrected condition. If none exists, record that as an evidence gap.
4. **Preconditions:** attacker position, process/sandbox, required entitlement, user interaction, and service reachability as supported by sources.
5. **Target mapping:** evidence mapping the relevant component to the exact target build. If unavailable, retain “not established.”
6. **Safe validation:** static analysis or a synthetic unit/regression test that checks the corrected condition without corrupting kernel memory, escaping a sandbox, modifying protected files, or executing an exploit.
7. **Reproducibility:** commands, tool versions, hashes, and expected output for safe tests. No reproduction claim without logs.

## What does not count as proof

- A CVE title or impact summary alone.
- The fact that a fix shipped in 26.7.
- A crash, panic, or generic memory corruption claim.
- A vulnerability that requires root being treated as an initial privilege escalation.
- A chain assembled from individually unverified assumptions.
- A test run on a different device/build without a defensible version mapping.

## Research outcome

No exploit chain is established. No CVE in this matrix is claimed to be cracked or reproduced. The next defensible work is to gather public patch references and precise version boundaries, then build non-destructive regression checks for behaviors that can be modeled outside the live device. If source or patch artifacts are unavailable, that limitation remains explicit rather than filled with guesses.
