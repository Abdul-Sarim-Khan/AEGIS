# A09: Security Logging and Monitoring Failures

## Summary
This category covers insufficient logging, monitoring, and alerting that prevents detection and timely response to attacks.

## Why it matters
Without adequate logging and monitoring, breaches go unnoticed for long periods. Attackers rely on the absence of detection to maintain access and exfiltrate data.

## Common vulnerable patterns
- Login attempts, access-control failures, and high-value transactions not logged.
- Logs stored only locally with no central aggregation or alerting.
- No alerting on suspicious patterns (many failed logins, privilege changes).
- Sensitive data (passwords, tokens, PII) written into logs.
- Logs that can be tampered with or are never reviewed.

## Code indicators to flag
- Exception handlers that silently `pass` without logging.
- Authentication and authorization failures with no log statement.
- Logging statements that include passwords, tokens, or full request bodies.

## Mitigations
- Log security-relevant events (auth success/failure, access denials, input validation failures) with enough context.
- Centralize logs and protect them from tampering.
- Set up alerting and a tested incident-response plan.
- Never log secrets or sensitive personal data.
- Ensure log formats support monitoring/SIEM ingestion.
