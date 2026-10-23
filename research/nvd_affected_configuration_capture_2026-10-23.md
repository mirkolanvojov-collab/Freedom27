# NVD affected-software configuration capture — 2026-10-23

## Scope and method

This pass records publicly visible representations of NVD/CVE configuration data for the Freedom27 iOS 26.6.1 research candidates. Where a secondary site reproduces CPE configuration history or the CVE record's configuration JSON, the record is labelled as a secondary representation. It is **not** represented as a direct NVD API payload. A direct NVD API response capture remains a follow-up item.

Target context supplied by user: iPhone17,4 / iOS 26.6.1 / build 23G83. No device inspection or testing was performed.

## Captured iPhone OS / iPadOS CPE ranges

The CPE criteria below are normalized for readability from public records; wildcard fields are retained.

| CVE | iPhone OS CPE | iPadOS CPE | Evidence source |
|---|---|---|---|
| CVE-2026-84566 | `cpe:2.3:o:apple:iphone_os:*:*:*:*:*:*:*:*`, versionEndExcluding `26.7` | `cpe:2.3:o:apple:ipados:*:*:*:*:*:*:*:*`, versionEndExcluding `26.7` | https://www.cvefeed.io/vuln/detail/CVE-2026-84566 |
| CVE-2026-84622 | `cpe:2.3:o:apple:iphone_os:*:*:*:*:*:*:*:*`, versionEndExcluding `26.7` | `cpe:2.3:o:apple:ipados:*:*:*:*:*:*:*:*`, versionEndExcluding `26.7` | https://cvefeed.io/vuln/detail/CVE-2026-84622 |
| CVE-2026-28968 | `cpe:2.3:o:apple:iphone_os:*:*:*:*:*:*:*:*`, versionEndExcluding `26.7` | `cpe:2.3:o:apple:ipados:*:*:*:*:*:*:*:*`, versionEndExcluding `26.7` | https://basefortify.eu/cve-reports/2026/09/cve-2026-28968.html |
| CVE-2026-65405 | `cpe:2.3:o:apple:iphone_os:*:*:*:*:*:*:*:*`, versionEndExcluding `26.7` | `cpe:2.3:o:apple:ipados:*:*:*:*:*:*:*:*`, versionEndExcluding `26.7` | https://app.opencve.io/cve/CVE-2026-65405 |
| CVE-2026-86886 | Apple CNA data: iOS/iPadOS affected from `0` up to but excluding `26.7`; also separate range below `27`. NVD-enriched CPE representation lists wildcard iPhone OS/iPadOS entries. | Same Apple CNA affected ranges | https://vulnerability.circl.lu/vuln/cve-2026-86886 |

## Other captured CPE ranges

For CVE-2026-84566, CVE-2026-84622, CVE-2026-28968, and CVE-2026-65405, public NVD-configuration histories/JSON also list these platform ranges:

- macOS 15.0 inclusive to 15.8 exclusive
- macOS 26.0 inclusive to 26.7 exclusive
- Depending on CVE: tvOS, visionOS, and watchOS below 27.0

The exact per-record matches are stored under `nvd_configuration_capture.affected_cpe_matches` in the JSON validation ledger.

## Key interpretation

- The listed iPhone OS/iPadOS upper bound below 26.7 includes version 26.6.1 as a **version-range match**.
- It does not prove that a particular build (23G83) is vulnerable, that the vulnerability can be triggered, or that it yields a usable exploit primitive.
- Some Apple CNA records express ranges such as `0 < 26.7` and `0 < 27` separately. These source ranges are preserved as separate entries rather than silently merged.
- The capture is not yet a full direct-NVD API archive. An additional primary-source cross-check was completed against Apple's iOS/iPadOS 26.7 security bulletin (released September 14, 2026): it independently confirms the disclosed impacts and that these named issues were addressed in 26.7, but Apple's bulletin is not a substitute for the NVD's machine-readable configuration payload. The official NVD endpoint was retried during this pass and remained inaccessible through the available retrieval interface; no response body was captured. The remaining evidence-quality step is to retrieve and save the official NVD CVE API JSON response for every candidate, then compare `configurations` / CPE match fields and Apple CNA `affected` entries against these secondary representations.

## Remaining direct API capture list

Official endpoint pattern: `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-NNNNN`

Capture at minimum:
- `vulnerabilities[].cve.id`
- `vulnerabilities[].cve.configurations`
- each CPE match's `criteria`, `versionStartIncluding`, `versionStartExcluding`, `versionEndIncluding`, `versionEndExcluding`, and `vulnerable`
- `vulnerabilities[].cve.containers.cna.affected` where present
- `published`, `lastModified`, `sourceIdentifier`, and reference URLs

## Alternate primary-source route

Retrieved official CVE Program JSON records from `CVEProject/cvelistV5` via raw GitHub URLs for all 12 candidates in the validation ledger. These records are Apple CNA records, not NVD API responses. Each record's source URL, update timestamp, affected product/ranges, and impact summary are now stored under `official_cve_program_capture` for its candidate in the JSON ledger. For example:

- [CVE-2026-84566 official CVE record](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2026/84xxx/CVE-2026-84566.json) — `dateUpdated` 2026-10-20; Apple CNA lists iOS/iPadOS affected below `26.7` and in a separate range below `27`.
- [CVE-2026-84622 official CVE record](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2026/84xxx/CVE-2026-84622.json) — `dateUpdated` 2026-10-20; Apple CNA lists the same separate iOS/iPadOS ranges and describes the kernel-memory read as requiring root privileges.
- Official repository documentation: https://github.com/CVEProject/cvelistV5

This is a successful alternate route for capturing the **CVE Program's vendor-supplied affected-version data for all 12 candidates**. All 12 records list iOS/iPadOS below 26.7 and a separate range below 27; this is a version-range match for 26.6.1, not confirmation of the exact build. It does not replace the outstanding task of capturing NVD `configurations` and CPE match fields.

## Primary-source cross-check and retrieval blocker

Apple's official iOS 26.7 / iPadOS 26.7 bulletin is available at https://support.apple.com/en-us/149041. It lists CVE-2026-84566 as a Kernel issue that may cause unexpected system termination or kernel-memory corruption, and CVE-2026-65405 as a Kernel information-disclosure issue that may reveal kernel memory layout. It also describes CVE-2026-84622 as an issue requiring root privileges to read uninitialized kernel memory. These impacts corroborate the general descriptions in the candidate ledger, and the bulletin says iOS/iPadOS 26.7 was released September 14, 2026. This does not independently prove that iOS 26.6.1 build 23G83 is affected or exploitable.

The official NVD API URL pattern was retried for CVE-2026-84566: `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-84566`. The retrieval interface returned an inaccessible-endpoint error rather than JSON. Accordingly, no official NVD API response is attached and no response fields are claimed as captured. This is an access limitation, not evidence that the NVD record is absent.

## Status

Secondary NVD/CPE representations, official CVE Program Apple CNA records for all 12 candidates, and an Apple advisory cross-check are recorded. Direct NVD API JSON has not yet been saved because the endpoint could not be retrieved through the available interface. No exploit was executed, no CVE was cracked, and the target device was not accessed or modified.


## Alternate feed retrieval attempt — 2026-10-23

To avoid the blocked direct NVD API route, the community-maintained [FKIE NVD JSON data-feed reconstruction](https://github.com/fkie-cad/nvd-json-data-feeds) was checked. Its README explicitly says it reconstructs legacy feeds from NVD API data and is not endorsed or certified by NVD. The repository's per-CVE directory structure was queried for all five relevant numeric prefixes (84xx, 43xx, 86xx, 65xx, 28xx). The available directory listings contained only four-digit CVE suffixes (for example, `CVE-2026-8499.json`), and none of the 12 five-digit-suffix candidates in this ledger was present in those listings. The mirror therefore did **not** provide configuration JSON for these candidates in the checked snapshot. This is a mirror coverage/freshness limitation, not evidence that the CVEs do not exist.

NIST's NVD status page says the current `/cves/` endpoint still returns the latest full affected JSON, while the history-feed format changed in August 2026: https://www.nist.gov/itl/nvd. The direct endpoint remains inaccessible through the current retrieval interface, so no NVD configuration payload or CPE match-criteria identifiers are claimed as captured. The Apple CNA records already captured remain useful version-range evidence, but are not a substitute for NVD CPE configuration data.

## Updated status

- Captured: official CVE Program / Apple CNA affected-version data for all 12 candidates.
- Checked: community NVD feed mirror directory listings for all five numeric prefixes; no matching candidate records were present.
- Not captured: direct NVD `configurations` JSON and associated CPE match-criteria records.
- Not established: exact build applicability for `23G83`, or exploitability on the user's device.
- Safety: no exploit was executed, no CVE was weaponized, and no device was accessed or modified.


## Reproducible direct-API capture utility added

A read-only retrieval utility is now committed at [`research/scripts/capture_nvd_configurations.py`](https://github.com/mirkolanvojov-collab/Freedom27/blob/main/research/scripts/capture_nvd_configurations.py). It queries the official NVD CVE API 2.0 and CPE Match API 2.0 sequentially for all 12 candidate identifiers, saves the complete raw JSON responses without rewriting their configuration fields, and emits a per-record HTTP/error summary. It accepts an optional `NVD_API_KEY` environment variable but does not require one by default. The utility only performs HTTP GET requests and writes local evidence files; it does not execute exploits or interact with a device.

**Execution status:** the script has been added to the repository but has not been executed in this environment. The available GitHub retrieval interface cannot run arbitrary Python or make arbitrary outbound HTTP requests to the NVD service, and direct NVD requests from the research interface failed. Therefore the script's output has not yet been captured, and no claim is made that the 12 NVD responses were successfully retrieved. Once run in a normal Python environment with outbound HTTPS access, its summary will show per-CVE success or errors; preserve those raw responses as evidence rather than treating an HTTP failure as a missing CVE.
