# Contributing to Freedom27

Freedom27 is currently a research scaffold, not an installable jailbreak.

## Evidence rules
- Record public sources and exact device/iOS build identifiers.
- Keep unknown or unreplicated findings marked `unverified` or `under-review`.
- A compatibility claim is usable only when its source is present and its build matches the target build.
- Never describe a proof of concept, simulator result, or generic advisory as proof that a specific iPhone can be jailbroken.
- Do not change `working_jailbreak` to `true` without independently reproducible end-to-end evidence and review.

## Checks
GitHub Actions runs the Python unit tests on pushes and pull requests. Locally, run:

```sh
python -m unittest discover -s tests -v
```

The project checks and diagnostics are read-only. They do not exploit, jailbreak, or modify an iPhone.

## Scope
Cydia integration, tweak loading, persistence, and installation remain future goals until a viable and responsibly documented platform path is established.
