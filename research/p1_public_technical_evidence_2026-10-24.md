# P1 public technical-evidence sweep — 2026-10-24

## Summary

This read-only review found a **new public-source lead for CVE-2026-84607** that the prior sweep did not capture: a GitHub repository is indexed by GitHub's PoC collection as describing research on finding the bug and fix for CVE-2026-84616 and CVE-2026-84607. This changes the earlier blanket statement that no public PoC reference had been found. It does **not** establish that the repository contains a working iOS PoC, that it is trustworthy, or that it applies to iOS 26.6.1/build 23G83. Repository code was not retrieved, executed, or analyzed for exploit mechanics.

For CVE-2026-43689, the reviewed primary and secondary sources still provide only a high-level impact/fix summary. A GitHub-hosted cyber-threat-observatory report exists, but its indexed summary cites Apple and NVD and does not establish a patch diff or independent reproduction. It should be treated as secondary analysis, not vendor patch evidence.

## Target context

- Recorded target: iPhone 16 Plus (`iPhone17,4`), iOS 26.6.1, build `23G83`.
- Apple lists both CVEs in its iOS 26.7/iPadOS 26.7 security advisory, which is the primary vendor source.
- The published version range includes versions below 26.7. This is a version-range match only; no public source reviewed pins vulnerable code to build 23G83.
- No Freedom27 reproduction, device test, or complete jailbreak chain is established.

## Evidence ledger

### CVE-2026-84607 — AVEVideoEncoder race condition

**Primary evidence**
- Apple iOS 26.7 security advisory: https://support.apple.com/en-us/149041
- NVD record: https://nvd.nist.gov/vuln/detail/cve-2026-84607
- NVD lists the fix in iOS/iPadOS 26.7 and states that a sandboxed app may execute arbitrary code with kernel privileges. Its record reports publication on 2026-09-14 and last modification on 2026-09-16.
- Apple describes the fix as improved state management for a race condition. No vulnerable function, state invariant, or source-level diff is disclosed in the reviewed advisory.

**New public-source lead (unverified)**
- GitHub repository indexed by a PoC catalogue: https://github.com/Ping-2o/ios.CVE-2026-84616-84607
- Catalogue index entry: https://github.com/nomi-sec/PoC-in-GitHub/blob/f4d2ec57715ec1b2e01248b8f384db5e415ea4eb/2026/CVE-2026-84616.json
- The indexed repository description says it concerns research on finding the bug and fix for CVE-2026-84616 and CVE-2026-84607, and the catalogue metadata shows an update on 2026-10-20.
- Assessment: **public technical lead found; contents, correctness, and applicability not verified**. Do not label this as a confirmed working PoC based on index metadata alone. No exploit code was fetched or run.

### CVE-2026-43689 — Kernel permissions issue

**Primary evidence**
- Apple iOS 26.7 security advisory: https://support.apple.com/en-us/149041
- NVD record: https://nvd.nist.gov/vuln/detail/cve-2026-43689
- GitHub Advisory Database mirror: https://github.com/advisories/GHSA-4jgx-p7cx-g39r
- Apple says additional restrictions address a permissions issue and that a malicious app may gain root privileges. NVD records publication on 2026-09-14 and last modification on 2026-09-15.
- The reviewed records do not identify the affected kernel function, the authorization check that changed, or a source-level patch diff.

**Secondary report**
- GitHub-hosted report: https://github.com/alan-turing-institute/cyber-threat-observatory/blob/3be96b8d69360acbfed4ebe7abeac0c0298533c8/reports/2026-09-14/TIER_3_CVE-2026-43689.md
- The indexed summary characterizes it as local privilege escalation and lists Apple/NVD as sources. That supports awareness of secondary analysis, but not independent reproduction or exact-build applicability. Its conclusions should not be treated as patch-level proof without validating its underlying evidence.

## Change from previous report

The previous report stated that the focused search did not surface a public PoC reference for these P1 candidates. The new search found a PoC-catalogue index entry linking to a repository whose description mentions CVE-2026-84607. Therefore:
- **84607:** upgrade status from “no public PoC reference surfaced in the prior sweep” to “public repository lead indexed; unverified.”
- **43689:** no authoritative patch diff or independently validated reproduction found in the reviewed source set.
- **Both:** exact build 23G83 applicability remains unverified; version-range matching is not proof of reachability or exploitability.

## Metadata and retrieval method

- Observation date: 2026-10-24 (UTC).
- Source timestamps are preserved as the dates exposed by NVD/GitHub search metadata; they are not asserted as exact retrieval times.
- Source classes are separated into vendor/CVE records, catalogue metadata, and secondary commentary.
- Search-index snippets are leads only; they can be stale, incomplete, or misleading.
- This is not an exhaustive proof that no additional public or private material exists.

## Safe next steps

1. Monitor the Apple advisory and CVE/NVD record history for changes.
2. Re-check the linked repository's public metadata and provenance without executing its code.
3. Seek vendor-published patch-level details or a reputable write-up with verifiable sources.
4. Keep exact-build reachability and Freedom27 exploitability explicitly unverified until there is independent, safe evidence.

No exploit was executed. No device was accessed, installed on, downgraded, restored, or modified.
