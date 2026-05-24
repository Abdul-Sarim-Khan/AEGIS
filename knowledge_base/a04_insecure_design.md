# A04: Insecure Design

## Summary
Insecure design refers to flaws in the architecture and logic of an application rather than bugs in implementation. The system was designed without adequate threat modeling, so even perfectly written code enforces an unsafe plan.

## Why it matters
You cannot patch your way out of a bad design. A missing security control at the design stage (e.g. no rate limiting on a money transfer, no business-logic check on a workflow) leaves a hole that secure coding alone cannot close.

## Common vulnerable patterns
- No rate limiting or anti-automation on sensitive flows (login, password reset, checkout) enabling credential stuffing or resource abuse.
- Business-logic flaws: skipping a payment step, replaying a coupon, negative-quantity orders.
- Trusting a multi-step workflow's order without enforcing state on the server.
- Recovery flows that leak whether an account exists.
- No segregation of tenants/users at the design level.

## Code indicators to flag
- Endpoints performing sensitive actions with no throttling, captcha, or attempt counter.
- Workflow handlers that accept a "final" step without verifying prior steps completed.
- Price, discount, or quantity values trusted from the client.

## Mitigations
- Perform threat modeling early; document trust boundaries and abuse cases.
- Establish secure design patterns and a reusable library of vetted components.
- Enforce business rules and limits on the server side.
- Write unit and integration tests for abuse cases, not just happy paths.
- Use rate limiting, resource quotas, and tenant isolation by design.
