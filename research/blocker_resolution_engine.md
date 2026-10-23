# Blocker Resolution Engine

The engine creates an ordered, fail-closed research plan for the exact Freedom27 target. It does not attempt to bypass iOS security controls and does not modify or connect to a device.

## Target

- iPhone 16 Plus (`iPhone17,4`)
- iOS 26.6.1, build `23G83`

## What it does

- Lists all eight required gates and their safe next actions.
- Marks unmet prerequisites so downstream stages cannot be treated as ready prematurely.
- Validates evidence records against the exact device, model identifier, OS version, and build.
- Requires immutable source revisions; a claim marked `verified` also needs an evidence note, confirmed scope, and independent reproduction.
- Fails closed: unknown or mismatched evidence remains unverified.

## Run through GitHub Actions

The repository workflow runs Python unit tests. To generate a local plan in an environment where the repository is checked out:

```sh
python -m Framework.blocker_resolution_engine
```

The module's current CLI integration is intentionally not included; use the repository's existing blocker analyzer for JSON output until a workflow step explicitly invokes `build_plan`.

## What it cannot do

It cannot create a vulnerability, defeat a mitigation without a valid underlying vulnerability, infer a full jailbreak from a sandbox escape, or prove that a research claim works on the phone. Do not run unreviewed proof-of-concept payloads on a daily-use device. Device-level exploit tests remain unauthorized unless the project owner explicitly approves them first.
