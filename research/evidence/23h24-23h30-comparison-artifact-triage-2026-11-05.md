# 23H24 ↔ 23H30 comparison evidence triage (2026-11-05)

## Verified run and outputs
Run [41905970197](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197), commit `bf5c08e3a50b3d6e92905ec2380e7946d4caa5a6`, completed successfully. Job `126840892246` completed the 23H24 dyld cache extraction, CoreGraphics comparison, and artifact uploads.

- [Comparison JSON bundle](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362383025), artifact 13362383025, SHA-256 of artifact ZIP `df8a960953ab83e738b6613b6afd243fb5b0843324d74fa94eaf9bd754c4ba84`, expires 2027-02-02.
- [23H24/23H30 CoreGraphics binaries](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13361134895), artifact 13361134895, ZIP SHA-256 `0c04cde67694923c55549e8cf65eff75c2c5de9754710d1315033e5434e83d0e`, expires 2026-12-04.
- [Diagnostics](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362148637), artifact 13362148637, expires 2026-11-11.

## Evidence boundaries
A successful comparison job establishes that the scripts ran and produced artifacts; it does not establish the presence of a vulnerability or exploitability. The comparison JSON bundle has not yet been independently reviewed field-by-field in this triage. Do not infer specific function changes or vulnerability attribution from the success flag alone.

The successful 23H24 extraction came from the comparison workflow's OTA download, **not** the separate Google Drive upload. The failed `Acquire 23H24 OTA and record integrity` workflow is a separate path and should not override the successful comparison-run evidence.

## Next checks
1. Inspect `coregraphics-26-7-patch-comparison.json` and `coregraphics-26-7-function-diff.json` for actual binary identities, changed functions, error fields, and comparison coverage.
2. Cross-reference observed changes with public advisory evidence for CVE-2026-86950; record ambiguity rather than equating a binary delta with a security fix.
3. Keep PR #37 draft; do not claim jailbreak progress without demonstrated exploit primitives.
