---
description: Generate API specification with endpoints and schemas
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate API Specification

Creating comprehensive API specification.

## Prerequisites

!`test -f docs/planning/user-stories.md && echo "✓ user-stories.md exists" || echo "⚠ Missing user stories (recommended to run /define first)"`

!`test -f docs/design/tech-spec.md && echo "✓ tech-spec.md exists" || echo "⚠ Missing tech spec (recommended to run /develop first)"`

!`test -d docs/planning/feature-specs/ && echo "✓ Feature specs directory found" || echo "ℹ No feature specs directory (optional)"`

## Setup

!`mkdir -p docs/implementation && echo "✓ Created docs/implementation/"`

## Template Reference

Reference template: @.claude/skills/api-backend/knowledge/backend-requirements.md

## Interactive API Specification Creation

I'll help you create a comprehensive API specification with:

### API Specification Contents

**1. Authentication & Authorization**:
- Authentication methods (OAuth 2.0, JWT, API keys)
- Authorization scopes and permissions
- Token management

**2. API Endpoints (5W2H analysis)**:
For each endpoint:
- HTTP method and path
- Request parameters
- Request body schema
- Response schema (success + errors)
- Authentication requirements
- Rate limits
- Example requests/responses

**3. Error Handling Envelope**:
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

**4. API Versioning Strategy**:
- Version format (v1, v2)
- Deprecation policy
- Migration guides

**5. Rate Limiting**:
- Rate limit tiers
- Headers (X-RateLimit-*)
- Throttling behavior

**6. Observability Standards**:
- Logging format
- Metrics to track
- Distributed tracing
- Health check endpoints

**HMW for Integration Challenges**:
- Transform API constraints into opportunities
- Document creative solutions

**Generating api-spec.md...**

## Validation

After generation:

!`test -f docs/implementation/api-spec.md && echo "✓ api-spec.md created" || echo "✗ Generation failed"`

**API spec checklist**:
!`if [ -f docs/implementation/api-spec.md ]; then
  grep -E "^(GET|POST|PUT|DELETE|PATCH) " docs/implementation/api-spec.md | wc -l | xargs echo "API endpoints:"
  grep -qi "authentication\|authorization" docs/implementation/api-spec.md && echo "✓ Auth documented"
  grep -qi "rate limit" docs/implementation/api-spec.md && echo "✓ Rate limiting defined"
  grep -o "PRD-F-[0-9]*" docs/implementation/api-spec.md | wc -l | xargs echo "Product features referenced:"
  grep -o "US-[0-9]*" docs/implementation/api-spec.md | wc -l | xargs echo "User stories referenced:"
fi`

## Next Steps

**Generate complementary specs**:
```
/data-model    # Data architecture
/ux-docs       # UX specifications
```

**Validate complete delivery**:
```
/validate-gate implementation-readiness
```

---

**API specification generated!** Ready for frontend integration and backend implementation.
