# Freedom27 Roadmap

## Phase 1 — Research scaffold
- Track device/build details and public research sources.
- Maintain a vulnerability registry with explicit verification status.
- Build compatibility and diagnostics utilities that do not modify the device.
- Run automated tests in GitHub Actions.

## Phase 2 — Evidence and feasibility
- Identify public research relevant to the exact device and iOS build.
- Record prerequisites, mitigations, reliability, and source links before considering implementation.
- Do not claim exploitability without reproducible evidence.
- Keep the Calif iPhone 18 Pro / iOS 27.0.1 presentation classified as an external report until a primary technical disclosure and reproducible evidence are available.
- Do not infer that CVE-2026-28968 or CVE-2026-86886 belongs to the demonstrated chain.

## Phase 3 — Device and build inventory
- Capture the user's exact iPhone model identifier and iOS version/build before evaluating compatibility.
- Compare that configuration against official Apple support data and documented public research.
- Mark unsupported or uninvestigated combinations explicitly; do not generalize from one demo device.
- Since development is iPhone-only, use GitHub Actions for repository checks and clearly label all device-dependent validation as not performed until actual device evidence exists.

## Phase 4 — Framework exploration
- Define package-management and tweak-compatibility interfaces only after a viable, documented platform path is established.
- Treat Cydia integration, untethered persistence, and tweak compatibility as unverified goals.
- Do not present a scaffold or compatibility metadata as an installable jailbreak.

## Release gate
Before calling any build usable, require a documented implementation, provenance for its source, exact supported model/build scope, automated test results, a real-device validation record, and a clearly documented recovery/uninstall path.

## Safety and scope
This repository is a research scaffold, not a working jailbreak. No exploit chain or device modification is included.
