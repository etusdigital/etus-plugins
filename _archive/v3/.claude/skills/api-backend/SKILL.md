---
name: api-backend
description: Generate comprehensive backend API specifications using 5W2H for systematic API design and How Might We for integration challenges. Defines all API endpoints, request/response schemas, authentication, error handling, and observability. Use when designing backend services or API contracts for solo developers.
---

# API Backend

Generate complete backend API specifications with systematic 5W2H analysis and HMW problem-solving for integration challenges.

## Purpose

This skill guides solo developers through backend API design by generating **through interactive conversation**:

1. **Backend Requirements** (be) - Complete API specification document

This SINGLE document (with MANY sections) defines:
- API endpoints and operations
- Request/response schemas (ONLY place - single source of truth)
- Authentication and authorization
- Error handling and status codes
- Rate limiting and quotas
- Versioning strategy
- Observability (logging, metrics, tracing)
- Integration patterns

The backend requirements document is a CONVERGENCE POINT that requires outputs from:
- Feature development chain (user-stories, feature-specs - requirements)
- Architecture chain (tech - NFRs, arch - system design)
- Data chain (data, erd, database-spec, dict - data model and field definitions)

## Interactive API Design

**This skill is conversation-driven for API strategy decisions.**

API design involves critical architectural choices that must be made collaboratively:
1. **API Style Discussion** - REST vs GraphQL vs gRPC (based on actual use cases)
2. **Authentication Strategy** - OAuth2 vs JWT vs API Keys (based on consumers)
3. **Endpoint Review** - Validate operations match user needs, not assumptions

**Key Principle:** Present options with trade-offs; don't dictate API architecture.

**Do NOT:**
- Assume REST without discussing alternatives
- Choose auth strategy without understanding API consumers
- Generate endpoints without validating against functional requirements

**Success Criteria:** API design reflects actual integration needs, not generic patterns.

## When to Use This Skill

Use this skill when:
- Designing REST, GraphQL, or gRPC APIs
- Need to document backend service contracts
- Establishing API standards for consistency
- Running Deliver phase parallel workstream (Backend track)
- Creating implementation-ready API specifications

Do NOT use for:
- Frontend implementation (use ux-chain skill instead)
- Data modeling (use data-chain skill instead)
- Business requirements (use feature-development-chain skill instead)

**Dependencies:** Requires `user-stories`, `feature-specs`, `tech-spec`, `data`, `erd`, `database-spec`, `dict` as inputs.

## Methodology Integration

### 5W2H for Systematic API Design

Apply rigorous questioning to ensure complete API specification:

**WHAT:**
- What operations does the API expose?
- What data does each endpoint accept/return?
- What authentication methods are supported?

**WHO:**
- Who can call each endpoint?
- Who owns the API (team/service)?
- Who consumes this API (clients)?

**WHERE:**
- Where is the API deployed?
- Where are errors logged?
- Where is API documentation hosted?

**WHEN:**
- When should we version the API?
- When do rate limits apply?
- When are requests retried?

**WHY:**
- Why REST vs GraphQL vs gRPC?
- Why synchronous vs asynchronous?
- Why this authentication approach?

**HOW:**
- How are requests validated?
- How are errors communicated?
- How is API performance monitored?

**HOW MUCH:**
- How much traffic can API handle?
- How much data per request?
- How much rate limiting?

### How Might We for API Challenges

Transform backend constraints into API design opportunities:

**Example Transformations:**

```
Challenge: Legacy system requires 3-second processing time
↓
HMW: How might we provide fast API response while processing takes time?
↓
Solution: Async pattern (POST returns 202 Accepted + job ID, GET /jobs/{id} polls status)
```

```
Challenge: Frontend needs data from 5 different microservices
↓
HMW: How might we reduce client complexity without tight coupling?
↓
Solution: Backend-for-Frontend (BFF) pattern aggregates calls, single client request
```

```
Challenge: Breaking API changes needed but clients can't update quickly
↓
HMW: How might we evolve API without breaking existing clients?
↓
Solution: API versioning (v1/v2 in path), deprecation schedule, backwards compatibility period
```

## How to Use This Skill

### Backend Requirements Document (be) - **INTERACTIVE API STRATEGY**

**BEFORE generating API spec**, discuss strategy with user:

```
"Let's design your API together. I need to understand your integration needs:

**API Style Decision:**
Your product needs APIs for [list FRs]. Which API style fits best?

Option A: **REST API**
- Best when: Simple CRUD, cacheable, well-understood
- Pros: Standard, works everywhere, easy to test
- Cons: Can over-fetch data, multiple round-trips

Option B: **GraphQL**
- Best when: Flexible client queries, reduce over-fetching
- Pros: Client-driven, single endpoint, type-safe
- Cons: More complex, caching harder, learning curve

Option C: **gRPC**
- Best when: High performance, internal services, streaming
- Pros: Fast, type-safe, bidirectional streaming
- Cons: Not browser-friendly, requires code generation

Which fits your needs? Why?

**Authentication Strategy:**
Who will use your API?
- Frontend app only (same domain)?
- Third-party integrations?
- Mobile apps?
- Internal services?

Based on consumers:
A) Session-based (simple, same domain only)
B) JWT (stateless, works anywhere)
C) OAuth 2.0 (delegated access, third-party integrations)
D) API Keys (service-to-service)

Which approach fits your security needs?"
```

[Wait for user's decisions. Record rationale for ADRs. Only then generate spec.]

#### Section 1: API Overview (After Strategy Discussion)

```
Apply 5W2H to API Strategy:

WHAT is this API?
- Purpose: What problem does it solve?
- Style: REST, GraphQL, gRPC, WebSocket?
- Scope: What operations are included?

WHY this API style?
- REST: Simple, cacheable, stateless
- GraphQL: Client-driven queries, reduce over-fetching
- gRPC: High performance, streaming, internal services
- WebSocket: Real-time bidirectional communication

WHO are the consumers?
- Web frontend: Browser-based application
- Mobile apps: iOS, Android native
- Third-party integrations: Partner systems
- Internal services: Microservice communication

WHERE is API deployed?
- Environment: Cloud provider, region
- Endpoint: Base URL (api.example.com)
- Documentation: Developer portal URL

HOW is API secured?
- Authentication: OAuth 2.0, API keys, JWT?
- Authorization: RBAC, ABAC, scope-based?
- Transport: TLS 1.3, certificate pinning?

HOW MUCH capacity?
- Traffic: Requests/second target
- Latency: Response time SLA
- Availability: Uptime SLA (99.9%?)
```

**Example:**
```
API: Invoicing Service API
Purpose: Enable programmatic invoice creation, retrieval, and payment tracking
Style: REST API (JSON)
Rationale: Standard, well-understood, cacheable, works with all clients
Traces to: US-# (user stories) and FS-[name]-# (feature specs) from feature-development-chain

WHY REST: Majority of consumers are web/mobile (REST libraries mature),
          operations are CRUD-like (good REST fit), caching helps performance

Consumers:
- Web App: Invoice creation/viewing UI
- Mobile App: Invoice notifications, quick view
- Third-party: Accounting software integrations (QuickBooks, Xero)

Base URL: https://api.example.com/v1
Documentation: https://docs.example.com/api
```

#### Section 2: Authentication & Authorization

```
Apply 5W2H to Auth:

WHAT auth methods?
- OAuth 2.0: For user-delegated access
- API Keys: For server-to-server
- JWT: For stateless auth tokens

WHO can access what?
- Roles: Admin, User, Guest
- Scopes: read:invoices, write:invoices, manage:users
- Permissions: RBAC matrix

HOW does auth flow work?
- Login: POST /auth/login → returns access_token + refresh_token
- Refresh: POST /auth/refresh → new access_token
- Logout: POST /auth/logout → revokes tokens

HOW MUCH security?
- Token lifetime: Access 15min, Refresh 7 days
- Rate limits: Auth endpoints limited (prevent brute force)
- Multi-factor: Required for admin operations
```

**Example:**
```
Authentication: OAuth 2.0 + JWT

Flow:
1. Client POSTs credentials to /auth/login
2. Server validates, returns:
   {
     "access_token": "eyJhbG...",  // JWT, 15min expiry
     "refresh_token": "rt_...",    // Opaque, 7 days
     "expires_in": 900
   }
3. Client includes "Authorization: Bearer {access_token}" in requests
4. When access_token expires, POST /auth/refresh with refresh_token
5. Server issues new access_token

Authorization Scopes:
- read:invoices: View own invoices
- write:invoices: Create/update own invoices
- read:all_invoices: View any invoice (admin)
- manage:users: User management (admin)

Security:
- All endpoints require authentication except /health, /docs
- Rate limit: /auth endpoints 5 req/min per IP
- JWT signed with RS256, public key at /.well-known/jwks.json
```

#### Section 3: API Endpoints

For EACH endpoint, apply 5W2H:

```
Endpoint: POST /invoices
Purpose: Create new invoice

WHAT operation?
- Create invoice resource
- Returns invoice ID and initial status

WHO can call?
- Authenticated users with write:invoices scope
- Admin users

WHERE processed?
- Invoice service handles creation
- Events published to queue for async processing

WHEN called?
- User completes invoice form
- Batch import via API

WHY this design?
- Synchronous creation for immediate feedback
- Async events for email, PDF generation

HOW validated?
- Schema validation (JSON Schema)
- Business rules (line items exist, amounts positive)
- Authorization (user can create invoice for this customer)

HOW MUCH?
- Request size: Max 10 line items, 100KB payload
- Rate limit: 100 requests/hour per user
- Response time: < 200ms p95
```

**Example Endpoint Specification:**
```
POST /invoices
Create a new invoice

Authentication: Required (write:invoices scope)

Request:
Content-Type: application/json

{
  "customer_id": "uuid",           // Required, references dict.customer.id
  "due_date": "2025-02-15",        // Required, ISO 8601 date
  "line_items": [                  // Required, 1-10 items
    {
      "description": "string",     // Required, max 500 chars
      "quantity": "number",        // Required, > 0
      "unit_price": "number",      // Required, >= 0, dict.money format
      "tax_rate": "number"         // Optional, 0-1 (e.g., 0.08 = 8%)
    }
  ],
  "notes": "string"                // Optional, max 2000 chars
}

Response: 201 Created
Content-Type: application/json

{
  "id": "uuid",
  "invoice_number": "INV-2025-001",
  "status": "draft",               // From dict.invoice.status
  "customer_id": "uuid",
  "subtotal": "number",            // Calculated
  "tax": "number",                 // Calculated
  "total": "number",               // Calculated
  "due_date": "2025-02-15",
  "created_at": "2025-01-15T10:30:00Z",
  "_links": {
    "self": "/invoices/{id}",
    "customer": "/customers/{customer_id}",
    "pdf": "/invoices/{id}/pdf"
  }
}

Errors:
400 Bad Request: Invalid request body
  {
    "error": "validation_error",
    "message": "Invalid request body",
    "details": [
      {"field": "line_items", "issue": "must have at least 1 item"}
    ]
  }

401 Unauthorized: Missing or invalid access_token
  {
    "error": "unauthorized",
    "message": "Authentication required"
  }

403 Forbidden: Insufficient permissions
  {
    "error": "forbidden",
    "message": "Missing required scope: write:invoices"
  }

404 Not Found: Customer doesn't exist
  {
    "error": "customer_not_found",
    "message": "Customer with ID {customer_id} does not exist"
  }

422 Unprocessable Entity: Business rule violation
  {
    "error": "business_rule_violation",
    "message": "Cannot create invoice for inactive customer"
  }

429 Too Many Requests: Rate limit exceeded
  {
    "error": "rate_limit_exceeded",
    "message": "Rate limit: 100 requests/hour. Try again in 45 minutes.",
    "retry_after": 2700
  }

500 Internal Server Error: Server error
  {
    "error": "internal_error",
    "message": "An unexpected error occurred. Contact support with request ID.",
    "request_id": "req_abc123"
  }

Events Emitted:
- ev.invoice.created (to data-dictionary for payload schema)

Rate Limits:
- 100 requests/hour per user
- 1000 requests/hour per organization
```

**Create HMW for Endpoint Optimization:**
```
Challenge: Invoice creation with 10 line items causes slow response (>500ms)
↓
HMW: How might we provide fast response while calculating tax and totals?
↓
Solution: Optimistic calculation (client-side preview), server validates + recalculates,
         if mismatch < 1% accept, else return correction for user confirmation
```

#### Section 4: Data Schemas (ONLY place for API request/response schemas)

**Critical Rule:** This is the SINGLE SOURCE OF TRUTH for API schemas. Reference data dictionary (dict.*) for field semantics.

```
Schema: Invoice
Description: Represents an invoice resource

{
  "id": "uuid",                    // dict.invoice.id
  "invoice_number": "string",      // dict.invoice.number (format: INV-YYYY-###)
  "customer_id": "uuid",           // dict.customer.id (FK)
  "status": "enum",                // dict.invoice.status (draft|sent|paid|overdue|cancelled)
  "line_items": [LineItem],        // Array of line item objects
  "subtotal": "decimal",           // dict.money (calculated sum of line items)
  "tax": "decimal",                // dict.money (calculated tax amount)
  "total": "decimal",              // dict.money (subtotal + tax)
  "due_date": "date",              // dict.date (ISO 8601)
  "created_at": "datetime",        // dict.datetime (ISO 8601 with timezone)
  "updated_at": "datetime",        // dict.datetime
  "_links": {                      // HATEOAS links
    "self": "string",
    "customer": "string",
    "pdf": "string"
  }
}

Schema: LineItem
Description: Individual line item within an invoice

{
  "id": "uuid",                    // dict.line_item.id
  "description": "string",         // dict.text (max 500 chars)
  "quantity": "decimal",           // dict.quantity (positive number)
  "unit_price": "decimal",         // dict.money (non-negative)
  "tax_rate": "decimal",           // dict.percentage (0-1, e.g., 0.08 = 8%)
  "amount": "decimal"              // dict.money (calculated: quantity * unit_price)
}
```

**Apply 5W2H to Schema Design:**
```
WHAT fields are required vs optional?
- Required: Core business logic needs (customer_id, total)
- Optional: Nice-to-have metadata (notes, tags)

WHY this structure?
- Normalization: line_items separate for flexibility
- Calculated fields: Include in response to avoid client calculation errors

HOW validated?
- Data types: JSON Schema validation
- Business rules: Subtotal = sum(line_items), total = subtotal + tax
- References: customer_id exists in database

WHERE is authoritative definition?
- Field semantics: dict.* in data-dictionary
- API structure: This document (backend-requirements)
```

#### Section 5: Error Handling

```
Apply 5W2H to Errors:

WHAT error types?
- Client errors (4xx): Invalid request, auth failure
- Server errors (5xx): Unexpected failures
- Business errors (422): Rule violations

HOW communicated?
- HTTP status code
- Error envelope (consistent structure)
- Request ID for tracing

WHY this format?
- Consistency: Same structure for all errors
- Debuggable: Request ID traces to logs
- Actionable: Details field explains how to fix
```

**Standard Error Envelope:**
```json
{
  "error": "error_code",           // Machine-readable error type
  "message": "Human-readable description",
  "details": [],                   // Optional array of specific issues
  "request_id": "req_abc123"       // Trace ID for debugging
}
```

**HTTP Status Code Policy:**
```
200 OK: Successful GET, PUT, PATCH
201 Created: Successful POST (resource created)
202 Accepted: Async operation started
204 No Content: Successful DELETE

400 Bad Request: Malformed request, validation error
401 Unauthorized: Missing or invalid authentication
403 Forbidden: Authenticated but insufficient permissions
404 Not Found: Resource doesn't exist
409 Conflict: Resource state conflict (e.g., duplicate)
422 Unprocessable Entity: Business rule violation
429 Too Many Requests: Rate limit exceeded

500 Internal Server Error: Unexpected server failure
502 Bad Gateway: Upstream service failure
503 Service Unavailable: Temporary outage, retry later
504 Gateway Timeout: Upstream service timeout
```

#### Section 6: API Versioning

```
Apply 5W2H to Versioning:

WHAT versioning strategy?
- URI versioning: /v1/invoices, /v2/invoices
- Header versioning: Accept: application/vnd.api+json; version=2
- Query parameter: /invoices?api_version=2

WHY this approach?
- URI: Most visible, cache-friendly, simple routing
- Header: Cleaner URLs, version negotiation
- Query: Easy testing, version switching

WHEN to version?
- Breaking changes: Field removed, type changed
- Non-breaking: Field added (optional), new endpoint
- Deprecation: 6-month notice before removal

HOW communicated?
- API docs: Changelog for each version
- Response headers: X-API-Version, X-API-Deprecated-At
- Sunset header: Warn clients of deprecation
```

**Example Versioning Strategy:**
```
Approach: URI versioning (/v1/, /v2/)

Versioning Policy:
- New version for breaking changes only
- Non-breaking changes added to current version
- Support N and N-1 versions concurrently
- 6-month deprecation notice before removal
- Sunset header on deprecated versions

Breaking Changes:
- Field removed from response
- Field type changed (string → number)
- Required field added to request
- Response structure significantly changed

Non-Breaking Changes:
- Optional field added to request
- Field added to response
- New endpoint added
- New HTTP method on existing endpoint

Example:
v1: POST /v1/invoices {"customer_id": "uuid", ...}
v2: POST /v2/invoices {"customer": {"id": "uuid"}, ...}
Breaking: customer_id moved to nested object

Response Headers:
v1: X-API-Version: 1, X-API-Deprecated-At: 2025-07-01, Sunset: Wed, 01 Jul 2025 00:00:00 GMT
v2: X-API-Version: 2
```

#### Section 7: Rate Limiting & Quotas

```
Apply 5W2H to Rate Limiting:

WHAT limits?
- Per-user: 100 req/hour for write operations
- Per-organization: 1000 req/hour aggregate
- Per-IP: 1000 req/hour (prevent abuse)

WHY rate limit?
- Fairness: Prevent single user monopolizing resources
- Stability: Protect backend from overload
- Security: Mitigate brute force, DDoS

HOW enforced?
- Token bucket algorithm
- Distributed rate limiter (Redis)
- Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset

WHEN reset?
- Sliding window: Rolling 1-hour window
- Fixed window: Reset on the hour
- Burst allowance: Allow brief spikes

HOW MUCH?
- Standard tier: 100 req/hour
- Pro tier: 1000 req/hour
- Enterprise: Custom limits
```

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1642329600 (Unix timestamp)
```

#### Section 8: Observability

```
Apply 5W2H to Observability:

WHAT to observe?
- Logs: Request/response, errors, business events
- Metrics: Latency, throughput, error rate
- Traces: Distributed tracing across services

WHERE logged?
- Logs: Centralized logging (ELK, CloudWatch)
- Metrics: Time-series DB (Prometheus, Datadog)
- Traces: APM (Jaeger, Zipkin, Datadog APM)

HOW structured?
- JSON logs: Parseable, searchable
- Correlation IDs: Trace requests across services
- Sampling: 100% errors, 1% successful requests

WHAT metrics?
- RED: Rate, Errors, Duration
- Latency: p50, p95, p99
- Saturation: Queue depth, CPU, memory
```

**Logging Standards:**
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "INFO",
  "request_id": "req_abc123",
  "user_id": "uuid",
  "endpoint": "POST /invoices",
  "status": 201,
  "duration_ms": 145,
  "ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0 ..."
}
```

**Key Metrics:**
```
- api.requests.total (counter): Total requests
- api.requests.duration (histogram): Response time distribution
- api.requests.errors (counter): Error count by type
- api.requests.rate_limited (counter): Rate limit hits
- api.active_connections (gauge): Current open connections
```

**Distributed Tracing:**
```
Headers:
- X-Trace-Id: Unique ID for entire request flow
- X-Span-Id: Unique ID for this service's span
- X-Parent-Span-Id: Previous service's span ID
```

## Workflow

### Single Document, Multiple Sections

```
Backend Requirements (be):
1. API Overview → Apply 5W2H to strategy
2. Authentication & Authorization → Define auth flows
3. API Endpoints → Document each endpoint with 5W2H
4. Data Schemas → SINGLE SOURCE OF TRUTH for API schemas
5. Error Handling → Standard error envelope
6. API Versioning → Breaking vs non-breaking policy
7. Rate Limiting → Quotas and headers
8. Observability → Logging, metrics, tracing standards

✅ BACKEND TRACK COMPLETE (API contracts ready for implementation)
```

### Dependencies

**Requires (must exist before generating be):**
- `user-stories`, `feature-specs`: User stories and feature specifications (what features API must support)
- `tech-spec`: NFRs (performance, security requirements)
- `arch`: Architecture patterns (sync vs async, caching strategy)
- `data`, `erd`, `database-spec`: Data model (what entities exist)
- `dict`: Field definitions (dict.*) and event schemas (ev.*)

**Feeds (who uses be output):**
- Frontend implementation references API contracts
- Implementation: Backend engineers build to this spec

## Gate Validation

### Backend Track Completion Criteria

Before frontend integration:

- [ ] All CRUD endpoints documented for entities from data model (database-spec)
- [ ] Request/response schemas complete and reference dict.*
- [ ] Each endpoint traces to user stories (US-#) and feature specs (FS-[name]-#)
- [ ] Authentication flows documented (login, refresh, logout)
- [ ] Authorization scopes defined per endpoint
- [ ] Error envelope standardized across all endpoints
- [ ] Rate limiting policy defined (informed by tech-spec NFRs)
- [ ] API versioning strategy documented
- [ ] Observability standards defined (logging, metrics, tracing)
- [ ] All schemas reference data-dictionary (dict.*), don't redefine
- [ ] All events reference data-dictionary (ev.*), don't redefine
- [ ] 5W2H analysis visible for key design decisions
- [ ] HMW statements document constraint-to-opportunity transformations

## Output Format

Generate backend requirements document, ensuring:

1. **Comprehensive:** All 8 sections present
2. **References:** Link to frd, srs, dict for traceability
3. **5W2H Evidence:** Show systematic analysis
4. **HMW Transformations:** Document problem-solving
5. **Single Source:** Schemas here, field semantics in dict
6. **Consistency:** Same error envelope, versioning, auth across endpoints

## Quality Checks

After generation, validate:

- **Completeness:** All entities from data model have CRUD endpoints
- **Consistency:** Same patterns across all endpoints
- **Traceability:** Each endpoint traces to user stories (US-#) and feature specs (FS-[name]-#)
- **Security:** All endpoints have auth/authz defined
- **Error Handling:** All error scenarios documented
- **Performance:** Rate limits and latency targets specified (from tech-spec NFRs)
- **Observability:** Logging and metrics defined

## Knowledge Base

This skill references template files in `knowledge/` directory:

- `backend-requirements.md` - Complete API specification template

## Best Practices

1. **API-First Design:** Define contracts before implementing
2. **Consistent Patterns:** Same auth, errors, versioning across API
3. **Reference dict.*:** Don't redefine field semantics
4. **Document WHY:** Future team needs to understand decisions
5. **HMW for Constraints:** Transform limitations into opportunities
6. **Version Conservatively:** Breaking changes are expensive
7. **Observe Everything:** Logs, metrics, traces are essential for debugging
8. **Rate Limit Early:** Easier to relax than add later

## Common Pitfalls to Avoid

- ❌ Redefining dict.* fields (breaks single source of truth)
- ❌ Inconsistent error format across endpoints
- ❌ Missing authentication on sensitive endpoints
- ❌ No rate limiting (invites abuse)
- ❌ Vague error messages (makes debugging impossible)
- ❌ No API versioning strategy (breaking changes break clients)
- ❌ Missing observability (can't debug production issues)
- ❌ Skipping 5W2H (leads to incomplete API design)
- ❌ No HMW for constraints (missed creative solutions)

## Next Steps After This Skill

After backend track completes:

1. **Frontend Implementation:** References API contracts from be
2. **Implementation:** Backend engineers build to specification
3. **API Documentation:** Generate OpenAPI/Swagger from be spec

Backend is one of three parallel workstreams in Deliver phase. Frontend implementation is the convergence point that requires backend complete.
