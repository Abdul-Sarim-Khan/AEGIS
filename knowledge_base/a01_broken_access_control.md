# A01: Broken Access Control

## Summary
Access control enforces that users can only act within their intended permissions. It is broken when the application fails to check, on the server side, whether the currently authenticated user is actually allowed to perform the requested action or view the requested resource.

## Why it matters
When access control fails, an ordinary user can read or modify other users' data, escalate to administrator functions, or bypass restrictions entirely. It is consistently one of the most widespread and impactful web application weaknesses.

## Common vulnerable patterns
- Trusting a client-supplied identifier without re-checking ownership (Insecure Direct Object Reference / IDOR), e.g. `GET /account?user_id=123` where the server returns the record without verifying it belongs to the session user.
- Relying on hiding a URL or button rather than enforcing a permission check (security by obscurity).
- Authorization checks performed only in the frontend (JavaScript) and never re-validated on the server.
- Missing checks on API endpoints: `@app.route("/admin/delete")` with no role verification inside the handler.
- Allowing privilege escalation via tampering with cookies, JWT claims, or hidden form fields such as `is_admin=false`.
- Misconfigured CORS allowing untrusted origins (`Access-Control-Allow-Origin: *` on authenticated endpoints).

## Code indicators to flag
- Database lookups keyed on a request parameter (`request.args.get("id")`, `request.form["account"]`) used directly in a query with no ownership check.
- Decorators or middleware that authenticate (verify identity) but never authorize (verify permission).
- Direct file access built from user input: `open("/data/" + request.args["file"])`.

## Mitigations
- Deny by default; grant access explicitly per role/resource.
- Enforce every access decision on the server, never the client.
- Check resource ownership on each request (the record's owner must equal the session user).
- Use a centralized authorization layer rather than scattering ad-hoc `if` checks.
- Log access-control failures and alert on repeated denials.
