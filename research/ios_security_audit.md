# iOS Security Audit Planner

This read-only planner catalogs major iOS security boundaries for Freedom27 and gives a safe research task for each. It is deliberately not a bypass, exploit runner, privilege-escalation tool, or device modification utility.

## Run

In a Python environment with the repository checked out:

```sh
python -m Framework.ios_security_audit
```

GitHub Actions also runs the unit tests for this module.

## Covered areas

- Code signing
- App sandbox
- Entitlements
- Kernel memory protections
- Secure boot and boot chain
- Signed system volume
- Code-signing trust
- Persistence

## Interpretation

The report is a research checklist. It does not query the phone, prove a control is vulnerable, or make changes. A security feature can only be described as bypassed when there is legitimate, independently reproduced evidence in an authorized controlled environment. Never install unknown profiles/certificates or run unreviewed payloads on a daily-use phone.
