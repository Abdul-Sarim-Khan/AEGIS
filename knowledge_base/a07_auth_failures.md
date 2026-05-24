# A07: Identification and Authentication Failures

## Summary
This category covers weaknesses in confirming a user's identity and managing their session, including weak passwords, broken session handling, and missing protection against automated attacks.

## Why it matters
If authentication or session management is weak, attackers can take over accounts through credential stuffing, brute force, session hijacking, or session fixation.

## Common vulnerable patterns
- Permitting weak or common passwords with no strength policy.
- No protection against automated guessing (no lockout, throttling, or MFA).
- Session IDs exposed in URLs, not rotated after login, or with no expiry.
- Storing session tokens insecurely; missing `HttpOnly`/`Secure`/`SameSite` cookie flags.
- Predictable password-reset tokens.

## Code indicators to flag
- Login handlers with no attempt counter or delay.
- Cookies set without `httponly=True`, `secure=True`, `samesite`.
- Session identifiers placed in query strings.
- Reset tokens generated with `random` instead of `secrets`.

## Mitigations
- Enforce strong password policies and check against breached-password lists.
- Offer and encourage multi-factor authentication.
- Rate-limit and lock out after repeated failures.
- Use a vetted session framework; rotate IDs on login; set secure cookie flags and expiry.
- Generate tokens with a cryptographically secure RNG.
