# Priority research pass: source reconciliation and verification plan — 2026-10-24

## Scope
Read-only public-source research for the 12 Freedom27 candidate CVEs. This report does not contain exploit triggers, payloads, race timing, device attack steps, or exploit-chain construction. Public advisory summaries support triage and safe test properties, not proof of exploitability on a particular device.

## Priority 1 — reconcile advisory identity and source facts
The prior regression-spec report flagged CVE-2026-86876 and CVE-2026-86886 as uncertain. A search of the official CVE Program repository and independent normalized advisory records yields the following correction:

- **CVE-2026-86876**: public descriptions identify an **out-of-bounds write**, fixed with improved bounds checking; reported impact is that a sandboxed process may circumvent sandbox restrictions. Do not describe it as CoreMedia until a primary source explicitly supports that component.
  - Official CVE JSON: https://github.com/CVEProject/cvelistV5/blob/main/cves/2026/86xxx/CVE-2026-86876.json
  - Corroborating normalized advisory record: https://github.com/ferralon-ai/vulnerability-corpus/blob/main/2026/09/CVE-2026-86876.json
- **CVE-2026-86886**: public descriptions identify a **path traversal** issue fixed with improved input validation; reported impact is that an app may modify protected system files. Do not describe it as TCC-specific until a primary source explicitly supports that component.
  - Official CVE JSON: https://github.com/CVEProject/cvelistV5/blob/main/cves/2026/86xxx/CVE-2026-86886.json
  - Corroborating normalized advisory record: https://github.com/ferralon-ai/vulnerability-corpus/blob/main/2026/09/CVE-2026-86886.json

The normalized advisory corpus is secondary evidence. For component names and exact affected releases, prefer Apple’s bulletin and the official CVE JSON; the NVD is an index, not source code.

## Priority 2 — evidence status and claims discipline
For every candidate, keep these fields separate:
1. **Advisory impact** — what Apple says may happen.
2. **Version range** — published affected range; a range containing 26.6.1 does not verify device build 23G83.
3. **Patch evidence** — source diff/function-level evidence, if any is published.
4. **Reproduction evidence** — independently repeatable benign regression test in a controlled harness.
5. **Chain relevance** — not established by a CVE description alone.

Current known gap: no public Apple source diff or exact implementation/function mapping was established in this pass. Do not infer a working jailbreak chain, a reliable primitive, or target-build reachability from advisory text.

## Priority 3 — safe regression properties
These are abstract security invariants for vendor-controlled tests or a model; they are not claimed to reproduce the original bugs.

| CVE | Public issue class | Safe invariant to test |
|---|---|---|
| CVE-2026-84607 | AVEVideoEncoder race; kernel-privilege impact reported | State transitions and authorization remain valid under concurrent lifecycle changes. |
| CVE-2026-43689 | Kernel permissions; root impact reported | Every privileged entry point enforces authorization/entitlement checks. |
| CVE-2026-84523 | APFS out-of-bounds write | Length/offset validation precedes writes; overflow and boundary inputs fail closed. |
| CVE-2026-86876 | Out-of-bounds write; sandbox restrictions impact reported | Parsing validates all buffer bounds and cannot change sandbox policy. |
| CVE-2026-86886 | Path traversal; protected-file modification impact reported | Authorization applies to canonical resolved paths; protected roots cannot be escaped. |
| CVE-2026-84566 | Kernel memory handling | Object lifetime and ownership invariants hold on cleanup/error paths. |
| CVE-2026-43687 | NFS/kernel information disclosure | Responses contain only initialized, in-scope data. |
| CVE-2026-43684 | Kernel use-after-free | References remain valid throughout each operation; cleanup respects outstanding references. |
| CVE-2026-43686 | NFS/kernel use-after-free | Request teardown and asynchronous completion preserve ownership/lifetime invariants. |
| CVE-2026-65405 | Kernel memory-layout disclosure | User-visible outputs are initialized and disclose no out-of-scope addresses/bytes. |
| CVE-2026-84622 | Root-context uninitialized kernel memory | Returned data is fully initialized; root prerequisite is documented and not misrepresented as initial access. |
| CVE-2026-28968 | Kernel out-of-bounds write | Index/length arithmetic is validated before access; rejected inputs leave adjacent state unchanged. |

## Priority 4 — next evidence collection order
1. CVE-2026-84607 and CVE-2026-43689: find vendor-authored patch notes, public source changes, or credible technical write-ups; keep impact separate from proof of a reproducible primitive.
2. CVE-2026-84523, CVE-2026-84566, CVE-2026-43684, CVE-2026-43686, CVE-2026-28968: seek exact public fix detail and safe unit-testable invariants.
3. CVE-2026-86876 and CVE-2026-86886: correct prior component labels unless a primary source supports them; keep advisory identity anchored to the official CVE record.
4. CVE-2026-43687, CVE-2026-65405, CVE-2026-84622: document disclosure scope and prerequisites; do not overstate these as initial privilege escalation.

## Verification checklist
- [ ] Confirm each CVE's description and affected versions from the official CVE JSON.
- [ ] Compare those facts with Apple’s iOS/iPadOS 26.7 bulletin.
- [ ] Keep NVD CPE range evidence separate from exact-build verification.
- [ ] Add a source link and retrieval date for each changed claim.
- [ ] Mark patch diffs and reproductions “not found” rather than filling gaps with guesses.
- [ ] Only add abstract, non-exploit regression tests that do not exercise real device vulnerabilities.

## Sources
- Apple iOS 26.7 / iPadOS 26.7 security content: https://support.apple.com/en-us/149041
- Official CVE Program record for CVE-2026-86876: https://github.com/CVEProject/cvelistV5/blob/main/cves/2026/86xxx/CVE-2026-86876.json
- Official CVE Program record for CVE-2026-86886: https://github.com/CVEProject/cvelistV5/blob/main/cves/2026/86xxx/CVE-2026-86886.json
- Example NVD record: https://nvd.nist.gov/vuln/detail/CVE-2026-84607

## Status
Read-only source reconciliation only. No exploit code was run or added; no device was accessed or modified. No exact-build exploitability claim is made.
