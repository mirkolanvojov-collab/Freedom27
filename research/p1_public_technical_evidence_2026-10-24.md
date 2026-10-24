# P1 public technical-evidence review — 2026-10-24 (follow-up)

## Outcome

The CVE-2026-84607 public lead has now been inspected at the repository-metadata and report-summary level. It is **more than a bare catalogue listing**: the public repository contains a detailed, AI-generated static-binary-analysis report proposing that a new state-consistency check in Apple's `AppleAVE2` driver is the fix associated with CVE-2026-84607.

That does **not** solve exact-build applicability or prove the CVE-to-code attribution. The report itself says it is AI-generated and not line-by-line human reviewed, acknowledges that Apple does not publish a per-CVE code mapping, withdraws one method used to argue that the check was absent pre-fix, and says the userspace AVEVideoEncoder components were not diffed. Its examined binaries are from the iOS 27.0 beta/GM cycle, not the target iOS 26.6.1 build `23G83`.

## CVE-2026-84607 — refined evidence status

### Public report inspected

- Repository: https://github.com/Ping-2o/ios.CVE-2026-84616-84607
- README: https://github.com/Ping-2o/ios.CVE-2026-84616-84607/blob/main/README.md
- Full report: https://github.com/Ping-2o/ios.CVE-2026-84616-84607/blob/main/REPORT_AVE_84607.md
- Repository API metadata: https://api.github.com/repos/Ping-2o/ios.CVE-2026-84616-84607
- Latest observed commit: `e30d5cfcd04e905860543b6693129d89c569fdc0`, dated 2026-09-16T11:26:50Z. Repository metadata shows updated 2026-10-20T16:49:42Z, but the latest observed content commit is earlier; the update timestamp alone is not evidence of new technical content.

### What the report claims, at a non-operational level

The report proposes that a state-consistency guard in the AppleAVE2 driver is associated with the race-condition fix, based on static comparison across iOS 27.0 beta and GM binaries. This is a **third-party binary-analysis hypothesis**, not an Apple-published patch mapping and not an independently reproduced finding.

### Credibility and applicability limits

1. The report labels itself AI-generated and says it did not receive line-by-line human review.
2. The author acknowledges Apple does not disclose a direct CVE-to-code mapping; attribution is inferential.
3. The report withdraws a prior method for establishing that the relevant check was absent in the earlier beta.
4. The report says userspace AVEVideoEncoder components were not compared across the fix window.
5. The analyzed versions are iOS 27.0 beta/GM, not iOS 26.6.1 build `23G83`.
6. No authoritative source diff, independent peer review, reproduction, or exact-target confirmation was found in this pass.

**Updated conclusion:** there is a concrete public technical hypothesis for CVE-2026-84607, but the root-cause attribution and relevance to the target build remain unverified. This is not a verified exploit and does not establish that the vulnerability is reachable on the target.

## CVE-2026-43689 — unresolved evidence gap

- Apple advisory: https://support.apple.com/en-us/149041
- NVD: https://nvd.nist.gov/vuln/detail/cve-2026-43689
- GitHub Advisory mirror: https://github.com/advisories/GHSA-4jgx-p7cx-g39r
- Secondary report: https://github.com/alan-turing-institute/cyber-threat-observatory/blob/3be96b8d69360acbfed4ebe7abeac0c0298533c8/reports/2026-09-14/TIER_3_CVE-2026-43689.md

The available material confirms Apple's high-level description that additional restrictions address a permissions issue, with potential root-privilege impact. This review did not find a primary patch diff or a secondary report with independently checkable implementation-level proof. The specific authorization change and exact-build behavior remain unresolved.

## Target and project status

- Target recorded in the project: iPhone 16 Plus, `iPhone17,4`, iOS 26.6.1, build `23G83`.
- Exact-build confirmations: **0**.
- Freedom27 reproductions: **0**.
- Full jailbreak chain verified: **no**.
- Authoritative patch diffs found in this review: **0**.

## Next evidence needed

1. Independent human-reviewed validation of the CVE-2026-84607 binary-analysis hypothesis.
2. A trustworthy comparison of the relevant vulnerable/fixed implementation on versions that bracket the target, with symbol/version provenance and reproducible metadata.
3. For CVE-2026-43689, primary patch-level evidence identifying the permission check or restriction that changed.
4. Evidence linking the affected implementation to build `23G83`; advisory version ranges alone do not prove runtime reachability.

No exploit was run. No device was accessed, installed on, downgraded, restored, or modified. This report records what public evidence supports and does not claim the remaining technical uncertainties are solved.
