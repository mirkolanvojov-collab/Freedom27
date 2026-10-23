# Free-only development policy

**Effective:** 2026-10-23  
**Project:** Freedom27

Freedom27 development must use a zero-cost workflow. Do not recommend or introduce a paid dependency as a required step.

## Hard constraints

- No paid cloud Mac, hosted runner upgrade, subscription, or commercial development service.
- Prefer the existing free GitHub repository and GitHub Actions allowance, while monitoring usage limits.
- Use free, reputable, open-source tools where suitable.
- Do not require paid Apple Developer Program membership as a default. Explain any signing/install limitations before proposing a path that depends on it.
- Do not ask the user to enter payment details or purchase a service.
- Do not use unknown signing services, profiles, or prebuilt jailbreak downloads just because they advertise themselves as free.
- Never place passwords, private keys, tokens, or signing secrets in source files or commits.

## Practical implications

The current repository contains research tooling and documentation, not a confirmed native iOS app target. Do not set up remote Mac infrastructure. Continue with source review, Python tests, evidence validation, and free CI.

An iPhone-only workflow may limit native iOS building and physical-device testing. Be explicit about those limitations rather than quietly introducing paid infrastructure or claiming that CI proves device compatibility.

## Definition of progress

Progress means reproducible source-based checks and reliable evidence. A green GitHub Actions run is not proof of a jailbreak. Do not claim exploit compatibility, kernel access, persistence, or a complete jailbreak until those capabilities are independently reproduced on the exact target device/build.

## Next step

Audit repository workflows and dependencies for any paid service assumptions; keep all changes compatible with the free workflow. If a future task cannot be completed for free from an iPhone, state the blocker and continue with the best free, safe alternative.
