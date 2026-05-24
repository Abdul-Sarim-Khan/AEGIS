# A08: Software and Data Integrity Failures

## Summary
Integrity failures occur when code or data is used without verifying it has not been tampered with — including insecure deserialization, unsigned updates, and untrusted build/deploy pipelines.

## Why it matters
If an application deserializes attacker-controlled data or pulls code from an unverified source, an attacker may achieve remote code execution or poison the software supply chain.

## Common vulnerable patterns
- Insecure deserialization: `pickle.loads(data)`, `yaml.load(data)` (without `SafeLoader`), `marshal.loads`.
- Auto-updating from an unsigned or untrusted source.
- CI/CD pipelines that run unverified third-party scripts.
- Trusting serialized objects from cookies or requests.

## Code indicators to flag
- `pickle.loads(`, `pickle.load(` on external input.
- `yaml.load(` without `Loader=yaml.SafeLoader`.
- `marshal.loads(`, `jsonpickle` on untrusted data.
- Downloading and executing remote scripts without integrity checks.

## Mitigations
- Never deserialize untrusted data with unsafe deserializers; prefer JSON or `yaml.safe_load`.
- Use digital signatures and integrity checks (hashes) for updates and critical data.
- Verify dependencies and lock files; use trusted, signed repositories.
- Harden CI/CD: review pipeline configs, isolate build steps, verify artifacts.
