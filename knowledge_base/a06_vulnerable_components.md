# A06: Vulnerable and Outdated Components

## Summary
Applications depend on libraries, frameworks, and runtimes. When any of these are outdated or contain known vulnerabilities, the application inherits those vulnerabilities.

## Why it matters
A known CVE in a popular dependency can be exploited en masse using public proof-of-concept code. Many major breaches trace back to an unpatched component rather than custom code.

## Common vulnerable patterns
- Unpinned or wildly outdated dependencies in `requirements.txt` / `package.json`.
- No process to track which versions are in use or whether they have known CVEs.
- Pulling unverified packages or running unmaintained libraries.
- Using end-of-life runtimes (e.g. an unsupported Python version).

## Code indicators to flag
- Dependency files with no version pins, or versions years out of date.
- Imports of libraries known to be deprecated or abandoned.

## Mitigations
- Maintain an inventory (SBOM) of all components and versions.
- Pin versions and update regularly through a tested process.
- Run dependency scanners (e.g. `pip-audit`, `safety`, OWASP Dependency-Check, GitHub Dependabot).
- Remove unused dependencies to shrink the attack surface.
- Obtain components from official, signed sources.
