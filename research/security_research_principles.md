# Freedom27 security research principles

## Working principle

Do not assume a security boundary is impossible to cross. Investigate its design, assumptions, attack surface, known weaknesses, and measurable failure modes. Equally, do not assume a bypass exists until evidence demonstrates it.

## Research loop

1. **Define the boundary.** State which protection or privilege boundary is being studied and what behavior would count as crossing it.
2. **Gather evidence.** Prefer primary sources, source code, technical papers, advisories, and reproducible reports.
3. **Form a falsifiable hypothesis.** Describe what should happen if the hypothesis is correct and what result would disprove it.
4. **Test safely and narrowly.** Use non-destructive, authorized tests, controlled environments where possible, and explicit stop/recovery criteria.
5. **Record exact scope.** Include device identifier, OS version/build, prerequisites, steps, outputs, and whether another researcher independently reproduced the result.
6. **Update the conclusion.** Keep failed attempts and negative results. Do not generalize beyond the evidence.
7. **Only then integrate.** A lead is not a working exploit; a sandbox escape is not automatically kernel control or a full jailbreak.

## Evidence labels

- **Hypothesis:** plausible idea not yet tested.
- **Source-supported:** visible in public source or technical documentation, not independently reproduced.
- **Demonstrated:** observed under recorded conditions.
- **Independently reproduced:** repeated by another tester or in a separate controlled run.
- **Exact-target verified:** reproduced on iPhone17,4 / iOS 26.6.1 / build 23G83.
- **Not established:** evidence is missing or inconclusive.

## Guardrails

- Focus on the user's own device and authorized research.
- Do not run opaque payloads on the daily-use phone before reviewing their code, effects, prerequisites, and recovery path.
- Preserve backups and stop if a test risks data loss, device instability, or unrecoverable changes.
- Keep public claims precise. Never label Freedom27 a working jailbreak or claim Cydia support without exact-target evidence.
- A failed test narrows the hypothesis; it does not prove that all possible routes are impossible.
