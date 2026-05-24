# A02: Cryptographic Failures

## Summary
This category covers failures related to protecting data in transit and at rest. The root cause is usually missing encryption, weak or outdated algorithms, poor key management, or sensitive data exposed where it should not be.

## Why it matters
Sensitive data (passwords, financial records, health information, tokens) that is transmitted or stored without strong protection can be intercepted or stolen, leading to identity theft, fraud, and regulatory penalties.

## Common vulnerable patterns
- Storing passwords in plaintext or with fast/unsalted hashes (`hashlib.md5`, `hashlib.sha1` for passwords).
- Hard-coded secrets and keys in source code (`API_KEY = "sk-..."`, `SECRET = "password123"`).
- Transmitting data over plain HTTP instead of TLS.
- Using deprecated protocols/ciphers (SSLv3, TLS 1.0, DES, RC4, ECB mode).
- Predictable randomness for security tokens (`random.random()` instead of the `secrets` module).
- Disabling certificate verification (`verify=False` in `requests`, `ssl._create_unverified_context()`).

## Code indicators to flag
- `hashlib.md5(`, `hashlib.sha1(` used on credentials.
- `verify=False`, `ssl.CERT_NONE`.
- `import random` used to generate tokens/keys/passwords.
- Literal credentials assigned to variables.

## Mitigations
- Hash passwords with a slow, salted KDF (bcrypt, scrypt, Argon2, or PBKDF2 with high iterations).
- Use the `secrets` module for tokens, not `random`.
- Enforce TLS everywhere; never disable certificate validation in production.
- Keep secrets out of source control; load them from environment variables or a secrets manager.
- Use authenticated encryption (AES-GCM) and keep libraries up to date.
