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
- Computes effective verification transitively, so an unverified prerequisite prevents dependent gates from being counted as complete.

## Run

With the repository checked out in a Python environment:

```sh
python -m Framework.blocker_resolution_engine
```

The command prints a JSON plan to standard output. GitHub Actions also generates and validates `research/blocker_resolution_report.json` on pushes and pull requests.

## What it cannot do

It cannot create a vulnerability, defeat a mitigation without a valid underlying vulnerability, infer a full jailbreak from a sandbox escape, or prove that a research claim works on the phone. Do not run unreviewed proof-of-concept payloads on a daily-use device. Device-level exploit tests remain unauthorized unless the project owner explicitly approves them first.
