# NVD affected-software configuration capture — 2026-10-23

> **Latest capture status (2026-10-23 23:21 UTC):** The later workflow run linked at the end of this file supersedes interim statements above that direct NVD capture was still outstanding. It returned HTTP 200 for all 12 CVE API and 12 CPE Match API requests and uploaded the 25-file raw-response artifact. This does **not** verify exploitability or exact build 23G83.

## Scope and method

This document began as a record of secondary representations. The later official NVD API capture is recorded below and supersedes any interim statement that direct capture remained outstanding. Secondary-source records remain separately labelled and are not represented as raw NVD payloads.

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
- **Historical note (superseded by the successful workflow capture below):** at the time of this initial pass, direct NVD API payloads had not yet been archived. Apple's iOS/iPadOS 26.7 security bulletin independently confirms disclosed impacts and fixes, but is not a substitute for machine-readable NVD configuration data. The later capture below closed the raw-response collection task; exact-build applicability and exploitability remain separate questions.

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

This was a successful alternate route for capturing the **CVE Program's vendor-supplied affected-version data for all 12 candidates**. At the time, it preceded the direct NVD capture recorded below. All 12 records list iOS/iPadOS below 26.7 and a separate range below 27; this is a version-range match for 26.6.1, not confirmation of the exact build.

## Primary-source cross-check and retrieval blocker

Apple's official iOS 26.7 / iPadOS 26.7 bulletin is available at https://support.apple.com/en-us/149041. It lists CVE-2026-84566 as a Kernel issue that may cause unexpected system termination or kernel-memory corruption, and CVE-2026-65405 as a Kernel information-disclosure issue that may reveal kernel memory layout. It also describes CVE-2026-84622 as an issue requiring root privileges to read uninitialized kernel memory. These impacts corroborate the general descriptions in the candidate ledger, and the bulletin says iOS/iPadOS 26.7 was released September 14, 2026. This does not independently prove that iOS 26.6.1 build 23G83 is affected or exploitable.

The official NVD API URL pattern was retried for CVE-2026-84566: `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-84566`. The retrieval interface returned an inaccessible-endpoint error rather than JSON. Accordingly, no official NVD API response is attached and no response fields are claimed as captured. This is an access limitation, not evidence that the NVD record is absent.

## Status

At the time of the initial inventory checkpoint, secondary NVD/CPE representations, official CVE Program Apple CNA records, and an Apple advisory cross-check were recorded, while direct NVD JSON was still pending. The successful workflow capture below supersedes that collection-status statement. No exploit was executed, no CVE was cracked, and the target device was not accessed or modified.


## Alternate feed retrieval attempt — 2026-10-23

To avoid the blocked direct NVD API route, the community-maintained [FKIE NVD JSON data-feed reconstruction](https://github.com/fkie-cad/nvd-json-data-feeds) was checked. Its README explicitly says it reconstructs legacy feeds from NVD API data and is not endorsed or certified by NVD. The repository's per-CVE directory structure was queried for all five relevant numeric prefixes (84xx, 43xx, 86xx, 65xx, 28xx). The available directory listings contained only four-digit CVE suffixes (for example, `CVE-2026-8499.json`), and none of the 12 five-digit-suffix candidates in this ledger was present in those listings. The mirror therefore did **not** provide configuration JSON for these candidates in the checked snapshot. This is a mirror coverage/freshness limitation, not evidence that the CVEs do not exist.

NIST's NVD status page says the current `/cves/` endpoint still returns the latest full affected JSON, while the history-feed format changed in August 2026: https://www.nist.gov/itl/nvd. The direct endpoint remains inaccessible through the current retrieval interface, so no NVD configuration payload or CPE match-criteria identifiers are claimed as captured. The Apple CNA records already captured remain useful version-range evidence, but are not a substitute for NVD CPE configuration data.

## Updated status

- Captured: official CVE Program / Apple CNA affected-version data for all 12 candidates.
- Checked: community NVD feed mirror directory listings for all five numeric prefixes; no matching candidate records were present.
- At the time of this checkpoint, direct NVD `configurations` JSON and associated CPE match-criteria records had not yet been captured; see the successful capture section below.
- Not established: exact build applicability for `23G83`, or exploitability on the user's device.
- Safety: no exploit was executed, no CVE was weaponized, and no device was accessed or modified.


## Reproducible direct-API capture utility added

A read-only retrieval utility is now committed at [`research/scripts/capture_nvd_configurations.py`](https://github.com/mirkolanvojov-collab/Freedom27/blob/main/research/scripts/capture_nvd_configurations.py). It queries the official NVD CVE API 2.0 and CPE Match API 2.0 sequentially for all 12 candidate identifiers, saves the complete raw JSON responses without rewriting their configuration fields, and emits a per-record HTTP/error summary. It accepts an optional `NVD_API_KEY` environment variable but does not require one by default. The utility only performs HTTP GET requests and writes local evidence files; it does not execute exploits or interact with a device.

**Historical execution status (superseded):** this paragraph describes the state before the GitHub Actions capture ran. The workflow later executed the script successfully; see the successful capture sections below for verified run IDs, HTTP statuses, and artifact digests.


## Successful direct NVD API capture — 2026-10-23

The GitHub Actions runner successfully executed `research/scripts/capture_nvd_configurations.py` against the official NVD endpoints. The run completed with HTTP 200 for all 12 CVE 2.0 lookups and all 12 CPE Match 2.0 lookups; each CVE response contained one record and one configuration object. The CPE Match endpoint returned between 3 and 7 match records per candidate. No request errors were recorded.

- Workflow run: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40029354991
- Raw evidence artifact (ZIP; 25 files, includes each full response and `capture_summary.json`): https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40029354991/artifacts/12534521313
- Artifact SHA-256 (ZIP): `adf4697a9bd9d2efcff3aaa1f7613432102da5186b58c50ba75a078a8080787c`
- Capture interval: 2026-10-23 21:48:07Z to 21:51:06Z
- API key: not used

### Findings from the returned NVD configurations

All 12 CVE records include vulnerable CPE matches for both `cpe:2.3:o:apple:iphone_os:*:*:*:*:*:*:*:*` and `cpe:2.3:o:apple:ipados:*:*:*:*:*:*:*:*`, each with `versionEndExcluding: 26.7`. The associated CPE Match identifiers returned consistently were:

- iPhone OS: `B331E4FC-727F-403B-8689-E647A51204FD`
- iPadOS: `0896A319-539F-45D2-ACA1-7225AE5C06ED`

The candidate records are: CVE-2026-84607, CVE-2026-43689, CVE-2026-84523, CVE-2026-86876, CVE-2026-86886, CVE-2026-84566, CVE-2026-43687, CVE-2026-43684, CVE-2026-43686, CVE-2026-65405, CVE-2026-84622, and CVE-2026-28968.

**Interpretation:** the NVD CPE bounds include versions below 26.7, so the reported version 26.6.1 is within the published version range. The records do not identify build `23G83` separately, and a version-range match does not establish that a usable exploit exists, that all exploit prerequisites are met, or that a jailbreak chain can be built. Validate the exact build and Apple advisory details separately before making device-specific conclusions.

### Evidence status

- Direct NVD CVE JSON: captured for 12/12 candidates.
- Direct NVD CPE Match JSON: captured for 12/12 candidates.
- Original API responses: preserved unchanged in the downloadable workflow artifact; not yet committed as 25 separate repository files.
- Exploit execution / device testing: not performed.


## Latest verified workflow artifact

- Workflow run: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40038959123
- Raw evidence artifact: https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/40038959123/artifacts/12538253226
- Artifact SHA-256 (ZIP): `4885397b1c735aa870ee3c0c3ff76819d72a1f90b44e1aec58788421827fc56b`
- Captured: 12/12 CVE JSON responses and 12/12 CPE Match JSON responses; all HTTP 200; zero failed records.
- Artifact: 25 files, including all raw response files and `capture_summary.json`.
- API key: not configured for this run.
- Exact build 23G83, exploitability, and a complete jailbreak chain remain unverified.
