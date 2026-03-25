---
name: api-spec
description: >
  Use when defining API endpoints, documenting the API contract, or specifying
  request/response schemas. Also triggers on 'API spec', 'endpoint definitions',
  'what is the API contract', 'REST API', 'GraphQL schema', or 'integration
  specifications'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Upstream: docs/ets/projects/{project-slug}/architecture/tech-spec.md, docs/ets/projects/{project-slug}/data/database-spec.md, docs/ets/projects/{project-slug}/planning/user-stories.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — Needed for NFRs (rate limiting, auth) and ADRs (API style decisions).
- `docs/ets/projects/{project-slug}/data/database-spec.md` — Needed for data shapes to define request/response schemas.
- `docs/ets/projects/{project-slug}/planning/user-stories.md` — Needed for user behaviors to map to API endpoints.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` — Service boundaries improve endpoint organization.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `api-spec.requires: [tech-spec, database-spec, user-stories]`
2. Check all three required docs exist, non-empty, not DRAFT
3. If any missing → auto-invoke the missing skill → wait → continue
4. Check ENRICHES → warn if missing, proceed

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- New API from scratch (public or internal)
- API versioning or major breaking changes
- Third-party integration requiring formal contract documentation

**Use short version when:**
- Adding 1-3 endpoints to an existing API
- Updating request/response schemas for existing endpoints
- Even in short version, still include: endpoint definition, request/response schemas, error codes, and authentication requirements

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Never batch multiple questions. Ask one, wait for the answer, then ask the next. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction, present 3-4 concrete options with a brief description of each. Highlight your recommendation.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs and a recommendation.

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section, ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Resolve before next phase** — Blocks the handoff.
   - **Deferred to [phase name]** — Noted and carried forward.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing api-spec.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

### Skill-Specific Interaction

- **API style:** Propose the API paradigm with tradeoffs and a recommendation:
  - *REST* — resource-oriented, widely understood, good tooling (best for most CRUD products)
  - *GraphQL* — flexible querying, single endpoint, great for complex frontends (best when clients need varied data shapes)
  - *gRPC* — binary protocol, streaming, high performance (best for internal microservice communication)
  Ask which paradigm fits the product.
- **Authentication strategy:** Propose 3-4 auth approaches with tradeoffs:
  - *JWT Bearer tokens* — stateless, scalable, good for SPAs
  - *API Keys* — simple, good for service-to-service
  - *OAuth2* — industry standard for third-party access, complex setup
  - *Session-based* — server-side state, simpler for traditional web apps
  Ask which approach fits the security requirements.
- **Per-endpoint approval:** Present each endpoint specification (method, path, request/response schema, error codes) individually. Ask "Does this endpoint look correct? Anything to adjust?" before the next endpoint.
- **Error format:** Propose 2-3 error response standards:
  - *RFC 7807 (Problem Details)* — industry standard, machine-readable, extensible
  - *Custom envelope* — project-specific, full control over shape
  - *Platform-native* — match the framework's default error format for consistency
  Ask which standard to adopt.
- **Versioning strategy:** Propose versioning approaches with tradeoffs:
  - *URL path* (/v1/) — explicit, easy to route, clear in documentation
  - *Header* (Accept-Version) — cleaner URLs, harder to discover
  - *Content-type* (vendor media type) — REST-pure, most complex
  Ask which approach to use.
- **Handoff options:**
  1. Design phase complete — proceed to Implementation Readiness Gate (Recommended)
  2. Add more endpoints — expand API coverage
  3. Refine spec — adjust schemas, error handling, or auth flows
  4. Pause — save current progress and return later

# API Specification Generation

## MEMORY PROTOCOL

This skill reads and writes persistent memory to maintain context across sessions.

**On start (before any interaction):**
1. Read `docs/ets/.memory/project-state.md` — know where the project is
2. Read `docs/ets/.memory/decisions.md` — don't re-question closed decisions
3. Read `docs/ets/.memory/preferences.md` — apply user/team preferences silently
4. Read `docs/ets/.memory/patterns.md` — apply discovered patterns
5. If any memory file doesn't exist, create it with the default template

**On finish (after saving artifact, before CLOSING SUMMARY):**
1. `project-state.md` is updated **automatically** by the PostToolUse hook — do NOT edit it manually.
2. If the user chose between approaches during this skill → run via Bash:
   `python3 .claude/hooks/memory-write.py decision "<decision>" "<rationale>" "<this-skill-name>" "<phase>" "<tag1,tag2>"`
3. If the user expressed a preference → run via Bash:
   `python3 .claude/hooks/memory-write.py preference "<preference>" "<this-skill-name>" "<category>"`
4. If a recurring pattern was identified → run via Bash:
   `python3 .claude/hooks/memory-write.py pattern "<pattern>" "<this-skill-name>" "<applies_to>"`

**The `.memory/*.md` files are read-only views** generated automatically from `memory.db`. Never edit them directly.

## PURPOSE

Generate a comprehensive **api-spec.md** that serves as the Single Source of Truth for all API contracts. This is the convergence point where architecture (NFRs from tech-spec), data models (schemas from database-spec), and user behavior (workflows from user-stories) intersect. The API specification defines the boundaries of the system as experienced by clients.

## CRITICAL SST RULE

**All API schemas, endpoint definitions, and request/response formats are ONLY defined in api-spec.md.** Other documents may reference but not redefine API structures.

## CONTEXT LOADING (4-level fallback)

1. **$ARGUMENTS**: If `[upstream-path]` provided, load that document
2. **Handoff**: Check for `docs/ets/projects/{project-slug}/planning/user-stories.md` (user workflows that need API support)
3. **Scan**: If not found, check `docs/ets/projects/{project-slug}/architecture/tech-spec.md` (NFRs and tech decisions) and `docs/ets/projects/{project-slug}/data/database-spec.md` (data model)
4. **Ask**: If no context available, ask user for API style preference (REST/GraphQL) and primary use cases

Load the following sections from upstream:
- User workflows from user-stories.md (which workflows need external API?)
- Non-functional requirements from tech-spec.md (authentication, rate limiting, compliance)
- Data model from database-spec.md (entity shapes, required fields)
- Any existing API design decisions or versioning strategy

## PROCESS

1. **API Style Selection**: Determine paradigm
   - REST (most common): resource-oriented, HTTP verbs
   - GraphQL (if flexible querying needed): query-based, single endpoint
   - gRPC (if internal/performance-critical): binary, streaming support
2. **Versioning Strategy**: Define version management approach
   - URL path (/v1/, /v2/): explicit, clear
   - Header: Accept-Version, X-API-Version
   - Query parameter: ?api_version=v1
3. **Authentication & Authorization**:
   - Bearer token (JWT or session)
   - API Key (for service-to-service)
   - OAuth2 (if third-party integration)
   - Define token format, expiry, refresh flow
4. **Endpoint Extraction from User Stories**:
   - Identify workflows that require API calls
   - Map user story actions to HTTP methods (GET, POST, PUT, DELETE, PATCH)
   - Extract required fields from database-spec
5. **Request/Response Schema Definition**:
   - Request body (if POST/PUT): required fields, validation rules
   - Response body: data structure, metadata, error handling
   - Status codes: 200, 201, 400, 401, 403, 404, 422, 500
6. **Error Handling**:
   - Standard error response format
   - Error codes and messages
   - Validation error details
7. **Rate Limiting**:
   - Requests per minute/hour
   - Per-user vs global limits
   - Throttling behavior and retry guidance
8. **Pagination** (for list endpoints):
   - Cursor-based (stateless, opaque cursors)
   - Offset-based (page number + size)
   - Sorting and filtering
9. **Webhook/Event Documentation** (if applicable):
   - Events fired (reference ev.* from data-dictionary.md)
   - Event payload schema
   - Delivery retry logic

## OUTPUT FORMAT

Document structure:
- **Executive Summary**: API paradigm, authentication model, rate limits
- **Base URL & Versioning**: Current version, base URL, versioning strategy
- **Authentication & Authorization**:
  - Auth flow diagram (OAuth/Bearer flow)
  - Token format and lifecycle
  - Scopes/permissions
- **Endpoints**: Grouped by resource type
  - Endpoint summary table (method, path, summary, status)
  - Detailed section per endpoint:
    - Method, path, description
    - User story reference (US-#)
    - Request schema (required/optional fields, validation)
    - Response schema (success and error responses)
    - Example request/response (JSON)
    - Status codes with meanings
    - Rate limit applicability
- **Error Handling**: Standard error response format, error code reference
- **Rate Limiting**: Quotas, headers, behavior
- **Pagination**: Cursor/offset format, examples
- **Webhooks** (if applicable): Event catalog, payloads, retry policy
- **SDK Guidance**: Notes on recommended client libraries or SDK patterns

## PIPELINE CONTEXT

- **Input**: user-stories.md (user workflows), tech-spec.md (NFRs), database-spec.md (data shapes)
- **Output**: api-spec.md
- **Feeds**: implementation-plan.md (dev specifications), backend development
- **Convergence point**: Where design, architecture, and data model intersect

## Idempotency, Retry & Concurrency

For each mutation endpoint (POST, PUT, PATCH, DELETE), document:

| Endpoint | Idempotency Key | Retry Safety | Max Retries | Backoff | Concurrency Model | Client Timeout |
|----------|----------------|--------------|-------------|---------|-------------------|----------------|

- **Idempotency key:** header/parameter name and generation strategy
- **Retry safety:** safe (same result on retry) or unsafe (may duplicate)
- **Concurrency model:** optimistic locking / pessimistic / last-write-wins
- **Client timeout:** recommended timeout for callers

## SINGLE SOURCE OF TRUTH (SST)

**API endpoint definitions, schemas, request/response formats, authentication mechanisms, and error handling are EXCLUSIVELY defined here.** Tech-spec.md references authentication requirements but does not define auth flows. Database-spec.md defines entity shapes; api-spec.md transforms them into request/response structures.

## KNOWLEDGE POINTER

Refer to `docs/ets/projects/{project-slug}/implementation/template-api-spec.md` for:
- REST endpoint naming conventions (resource-oriented)
- JSON schema examples for requests/responses
- Error response format templates
- Authentication flow diagrams
- Rate limiting header conventions (X-RateLimit-*)
- Pagination examples (cursor and offset)

---

**Execution instruction**: Load context, identify user workflows requiring API support, select API style, define authentication and versioning, extract endpoints and schemas, map to database model, document error handling and rate limits, and output api-spec.md to docs/ets/projects/{project-slug}/implementation/.

## INPUT VALIDATION

**tech-spec.md** (BLOCKS):
- Must contain at least 1 NFR-# related to API (performance, rate limiting, auth)
- Must contain at least 1 ADR-#

**database-spec.md** (BLOCKS):
- Must contain at least 1 CREATE TABLE or entity definition

**user-stories.md** (BLOCKS):
- Must contain at least 3 US-# with Given/When/Then

**architecture-diagram.md** (ENRICHES):
- Should contain Container View with service boundaries

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] At least 5 API endpoints defined
- [ ] Each endpoint has: method, path, request schema, response schema, error codes
- [ ] Authentication/authorization documented
- [ ] Rate limiting strategy defined (referencing NFR-#)
- [ ] Versioning strategy documented
- [ ] API error response format standardized
- [ ] SST rule verified: API schemas defined ONLY here
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ api-spec.md saved to `docs/ets/projects/{project-slug}/api/api-spec.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document defines API endpoints and schemas, not traceable IDs)

→ Next step: validate-gate (Design Gate) or parallel completion — API design complete
  Run: /validate or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `tech-spec.md`, `database-spec.md`, `user-stories.md` (BLOCKS), `architecture-diagram.md` (ENRICHES)
- **Action:** Extract NFRs, data models, user flows, service boundaries
- **Output:** API requirements bundle
- **Why this matters:** The API spec sits at the intersection of architecture, data, and user behavior. Loading all three ensures endpoints reflect real requirements.

### Step 2: API Style Selection (Interactive)
- **Input:** API requirements + product context
- **Action:** Propose API paradigm (REST, GraphQL, gRPC) with tradeoffs and a recommendation. Ask the user which paradigm to use.
- **Output:** Selected API style
- **Why this matters:** The API paradigm shapes every endpoint definition. Choosing it first ensures consistency throughout the spec.

### Step 3: Authentication & Versioning (Interactive)
- **Input:** NFRs from tech-spec + selected API style
- **Action:**
  1. Propose 3-4 auth strategies (JWT, API keys, OAuth2, session-based) with tradeoffs. Ask which to use.
  2. Propose versioning strategy (URL path, header, content-type) with tradeoffs. Ask which to use.
  3. Propose error response format (RFC 7807, custom, platform-native) with tradeoffs. Ask which to adopt.
- **Output:** Cross-cutting decisions (auth, versioning, error format)
- **Why this matters:** These cross-cutting decisions affect every endpoint. Settling them before defining individual endpoints avoids inconsistency.

### Step 4: Per-Endpoint Design (Individual Approval)
- **Input:** API requirements + US-# behaviors + cross-cutting decisions
- **Action:** For each endpoint:
  1. Present endpoint spec (method, path, description, US-# reference)
  2. Present request schema (required/optional fields, validation rules)
  3. Present response schema (success and error responses, status codes)
  4. Ask "Does this endpoint look correct? Anything to adjust?" before the next endpoint
- **Output:** Individually approved endpoint specifications
- **Integration:** API schemas are SST — no other document may define them

### Step 5: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is lightweight work and the document has unnecessary sections → trim empty or boilerplate sections
  - If this is complex work and sections are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 6: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline still have to invent if this document is all they get?
  2. Do any sections depend on content claimed to be out of scope?
  3. Are there implicit decisions that should be explicit?
  4. Is there a low-effort addition that would make this significantly more useful for the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 7: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/api/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/api/api-spec.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/api/api-spec.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/architecture/tech-spec.md`, `docs/ets/projects/{project-slug}/data/database-spec.md`, `docs/ets/projects/{project-slug}/planning/user-stories.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 9: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/api/api-spec.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 10: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT
- **Handoff:** Present next step options:
  1. Design phase complete — proceed to Implementation Readiness Gate (Recommended)
  2. Add more endpoints
  3. Refine spec
  4. Pause

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing | Critical | Auto-invoke upstream skill | Block execution |
| Database schema too sparse | Medium | Ask user about data model | Generate placeholder schemas |
| No auth-related NFR found | Medium | Ask user about auth requirements | Default to bearer token |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
