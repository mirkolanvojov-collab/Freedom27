# 23H24 CoreGraphics extraction — completed CI run (2026-11-04)

GitHub Actions run [41905970197](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197), job `126840892246`, completed successfully on commit `bf5c08e3a50b3d6e92905ec2380e7946d4caa5a6`.

The workflow's `Extract iOS 26.7 (23H24) dyld cache` step ran and printed a schema-1 JSON extraction report with `"complete":true`, including `23H24__iPhone17,4/System/Library/Caches/com.apple.dyld/dyld_shared_cache_arm64e` and its sidecars. Subsequent direct 23H24-to-23H30 CoreGraphics comparison and raw-binary artifact upload steps also succeeded.

Artifacts:
- [CoreGraphics 23H24–23H30 raw binaries](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13361134895)
- [CoreGraphics comparison evidence](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362383025)
- [Diagnostic logs](https://github.com/mirkolanvojov-collab/Freedom27/actions/runs/41905970197/artifacts/13362148637)

**Scope distinction:** This successful extraction is from the existing comparison workflow's independently resolved/downloaded 23H24 OTA. It does **not** demonstrate extraction or authenticate the separate user-uploaded Google Drive `.aea` file. The earlier Google Drive run only proved a successful transfer and observed SHA-256. The extracted binaries are research inputs, not evidence of a working jailbreak.

The original OTA and temporary dyld caches were removed during workflow cleanup; the small CoreGraphics artifacts persist subject to artifact retention.
