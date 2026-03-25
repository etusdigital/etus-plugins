# Archetype: API / Integration

## Description

Use when the feature involves consuming or exposing APIs, integrating with external services, or building system-to-system communication. This archetype surfaces reliability gaps, missing error contracts, idempotency oversights, and versioning blind spots.

## When to Activate

Activate this archetype when stories or problem framing mention:
- REST/GraphQL/gRPC endpoints
- Third-party service integration
- Webhooks, callbacks, event subscriptions
- Data synchronization between systems
- OAuth, API keys, service-to-service auth

## Mandatory Probes

### Probe 1: Authentication & Scopes
**Question:** "How does the caller authenticate? What scopes or permissions are required? Is there a difference between user-level and service-level auth?"
- **Sufficient when:** Auth method specified (OAuth2, API key, JWT, etc.), scopes listed per endpoint/operation, user vs service distinction clear
- **Insufficient when:** "We use API keys" with no scope model or permission granularity

### Probe 2: Retry Safety
**Question:** "If a request fails mid-flight and the client retries, what happens? Is the operation safe to retry, or could it cause duplicates or side effects?"
- **Sufficient when:** Each mutating operation classified as idempotent or not, retry guidance documented
- **Insufficient when:** "The client can retry" with no analysis of side effects

### Probe 3: Idempotency Keys
**Question:** "For non-idempotent operations (create, charge, transfer), is there an idempotency key mechanism? How long are keys valid? What happens on key collision?"
- **Sufficient when:** Idempotency key strategy defined (header name, TTL, collision behavior, storage)
- **Insufficient when:** "We'll add idempotency later" or no mechanism for critical mutating operations

### Probe 4: Rate Limits
**Question:** "What are the rate limits? Per user, per API key, or global? What response does the caller get when rate-limited? Is there a retry-after header?"
- **Sufficient when:** Rate limit tiers defined, 429 response format specified, retry-after strategy documented
- **Insufficient when:** "We'll rate limit" with no numbers or strategy

### Probe 5: Partial Failure Handling
**Question:** "If a batch operation partially succeeds (e.g., 8 of 10 items created), what does the response look like? Does the caller know which items failed and why?"
- **Sufficient when:** Partial success response format defined, per-item error reporting, transaction semantics (all-or-nothing vs best-effort) specified
- **Insufficient when:** "It either succeeds or fails" with no partial failure consideration

### Probe 6: Error Contract Format
**Question:** "What does an error response look like? Is there a standard error schema? Does it include error codes, human-readable messages, and field-level detail?"
- **Sufficient when:** Error schema defined (code, message, details array, field errors), HTTP status mapping documented
- **Insufficient when:** "We return 400 or 500" with no structured error body

### Probe 7: Versioning Strategy
**Question:** "How is the API versioned? URL path, header, or query param? What is the deprecation policy? How are breaking changes communicated?"
- **Sufficient when:** Versioning method chosen, deprecation timeline defined, breaking change notification process documented
- **Insufficient when:** "We'll version when needed" with no strategy

### Probe 8: Webhooks & Replay
**Question:** "If the integration uses webhooks or event callbacks: what happens when delivery fails? Is there a retry schedule? Can events be replayed? Is there a dead-letter queue?"
- **Sufficient when:** Webhook retry policy defined (attempts, backoff, timeout), replay mechanism described, dead-letter handling specified
- **Insufficient when:** "We send webhooks" with no failure handling or "N/A" when the integration clearly involves async notifications

## Anti-Patterns

1. **Assuming always-available** — No circuit breaker, no fallback, no degraded mode when the external service is down
2. **No error contract** — Errors are ad-hoc strings with no schema, making client-side handling fragile
3. **No backward compatibility plan** — Breaking changes are deployed without versioning or migration path
4. **Fire-and-forget webhooks** — Events are sent once with no retry, no acknowledgment, no dead-letter queue

## Archetype Dimensions

These dimensions are added to `coverage-matrix.yaml` under `semantic_dimensions.archetype_dimensions`:

| Dimension | Covered when |
|-----------|-------------|
| `idempotency_defined` | Every mutating endpoint classified as idempotent or has idempotency key mechanism |
| `error_contract_defined` | Standard error schema documented with codes, messages, and field-level detail |
| `retry_policy_defined` | Retry safety classified per operation, rate limit strategy documented, webhook retry schedule defined |
