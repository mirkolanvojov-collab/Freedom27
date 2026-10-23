# Hypothesis harness

This module is a safe research-record validator, not an exploit. It helps Freedom27
keep a hypothesis, a non-destructive test description, expected observation, result,
and evidence note together.

## Use

Create a blank record:

```sh
python -m Framework.hypothesis_harness --init
```

Save the output as a JSON file, fill in the hypothesis and test fields, then validate:

```sh
python -m Framework.hypothesis_harness --check path/to/hypothesis.json
```

A passing schema check only means the record is complete. It does not establish that
a vulnerability exists or that a device is exploitable. Use authorized lab systems,
avoid destructive tests on a daily-use phone, and preserve enough evidence for another
researcher to reproduce the observation.
