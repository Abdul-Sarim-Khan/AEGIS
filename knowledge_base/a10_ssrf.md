# A10: Server-Side Request Forgery (SSRF)

## Summary
SSRF occurs when an application fetches a remote resource using a URL supplied or influenced by the user, without validating the destination. The server can be tricked into making requests to unintended internal or external systems.

## Why it matters
Because the request originates from the server, SSRF can reach internal services behind a firewall, cloud metadata endpoints (e.g. 169.254.169.254 for credentials), and other resources the attacker could not reach directly.

## Common vulnerable patterns
- Fetching a user-supplied URL: `requests.get(request.args["url"])`, `urllib.request.urlopen(user_url)`.
- Webhook, image-proxy, PDF-generator, or link-preview features that accept arbitrary URLs.
- Following redirects to internal addresses without re-validation.
- Allowing `file://`, `gopher://`, or internal IP ranges.

## Code indicators to flag
- HTTP client calls (`requests.get`, `urlopen`, `httpx`, `curl`) whose target comes from request data.
- No allowlist or scheme/host validation before fetching.

## Mitigations
- Allowlist permitted destinations (hosts, schemes, ports); deny by default.
- Block requests to private/internal IP ranges and cloud metadata addresses.
- Disable unneeded URL schemes; do not follow redirects blindly.
- Enforce network-layer segmentation so the app server cannot reach sensitive internal hosts.
- Validate and canonicalize URLs before use.
