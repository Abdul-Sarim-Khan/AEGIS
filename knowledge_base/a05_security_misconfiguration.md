# A05: Security Misconfiguration

## Summary
Misconfiguration covers insecure default settings, incomplete setups, verbose errors, unnecessary features left enabled, and unhardened cloud or framework configuration.

## Why it matters
Attackers actively scan for default credentials, exposed admin panels, debug modes, and leaked stack traces. A single misconfigured setting can expose the whole system regardless of code quality.

## Common vulnerable patterns
- Debug mode enabled in production (`app.run(debug=True)`, `DEBUG = True`) leaking stack traces and an interactive console.
- Default or sample accounts and passwords left active.
- Detailed error messages returned to users revealing internals.
- Directory listing enabled; backup or `.git` folders served publicly.
- Overly permissive cloud storage buckets or security groups.
- Missing security headers (CSP, HSTS, X-Content-Type-Options).

## Code indicators to flag
- `debug=True`, `DEBUG = True`.
- Wildcard CORS or `0.0.0.0` bindings combined with debug.
- Exception handlers returning the raw traceback to the client.

## Mitigations
- Disable debug and verbose errors in production; return generic error pages.
- Harden defaults; remove unused features, sample apps, and default accounts.
- Automate configuration with repeatable, reviewed infrastructure-as-code.
- Apply least-privilege to cloud resources and storage.
- Set security headers and review configuration regularly.
