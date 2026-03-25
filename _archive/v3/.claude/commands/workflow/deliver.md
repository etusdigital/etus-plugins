---
description: Run deliver phase - parallel data, UX, backend, and implementation workstreams
allowed-tools: Task, Read, Write, Bash, Grep
model: sonnet
---

# Deliver Phase

Running Deliver Phase (Parallel Workstreams → Convergence) - implementation specifications

## Phase Overview

The **Deliver Phase** launches **3 parallel workstreams** that converge at implementation readiness:
- **Workstream A**: Data Chain (6 documents in docs/design/)
- **Workstream B**: UX Chain (4 documents in docs/design/)
- **Workstream C**: Backend + Implementation (2 documents in docs/implementation/)

**Convergence Point**: All tracks complete and synchronized before implementation readiness gate

## Pre-flight Checks

**Prerequisites - Develop Phase Complete**:
!`test -f docs/implementation/architecture-diagram.md && echo "✓ architecture-diagram.md exists" || echo "✗ Missing architecture-diagram.md (run /develop first)"`

!`test -f docs/implementation/tech-spec.md && echo "✓ tech-spec.md exists" || echo "✗ Missing tech-spec.md (run /develop first)"`

**Output directories**:
!`mkdir -p docs/design docs/implementation && echo "✓ Created docs/design/ and docs/implementation/"`

## Parallel Execution Pattern

```
DEVELOP GATE ✓
     ↓
┌────┴────┬────────┬─────────────┐
│         │        │             │
Data    UX      Backend +
Chain   Chain   Implementation
│         │        │
└────┬────┴────────┴─────────────┘
     ↓
IMPLEMENTATION READINESS GATE ✓
```

## Workstream A: Data Chain

**Invoke**: data-chain skill

**Outputs** (6 documents in docs/design/):
1. **data-requirements.md** - Data Requirements Document (entities, attributes, constraints)
2. **erd.md** - Entity Relationship Diagram
3. **database-spec.md** - FUSED database specification (old database-requirements + database-schema combined)
   - Includes all DDL (CREATE TABLE, indexes, constraints) - **SINGLE SOURCE**
4. **data-dictionary.md** - Field definitions (dict.* namespace) and event schemas (ev.* namespace) - **SINGLE SOURCE**
5. **data-flow-diagram.md** - Data processing flows and transformations
6. **data-catalog.md** - Data governance, lineage, and cataloging

**Enhancements**: 5W2H for data entity analysis, HMW for modeling challenges

**Gate Criteria**:
- All entities defined with attributes and constraints
- ERD complete with relationships and cardinality
- database-spec.md contains all DDL (no separate database-schema.md)
- Data dictionary: ALL dict.* fields and ev.* events defined (Single Source)
- Data flows mapped end-to-end
- Data catalog for governance and lineage

**Invoking data-chain skill...**

## Workstream B: UX Chain

**Invoke**: ux-chain skill

**Outputs** (4 documents in docs/design/):
1. **user-journey.md** - Current and future state journey mapping with pain points
2. **ux-sitemap.md** - UX sitemap (routes, views, navigation structure)
3. **wireframes.md** - Layout specifications and interactive behaviors
4. **style-guide.md** - Design tokens (tok.* namespace - SINGLE SOURCE) and design system

**NOT INCLUDED** (removed from previous structure):
- jtbd.md (absorbed into product-vision.md from Discovery phase)
- uxdd.md (eliminated - consolidated into wireframes.md and style-guide.md)
- design-requirements.md (eliminated - component specs merged into wireframes.md)
- frontend-requirements.md (eliminated - frontend ADRs documented in tech-spec.md)

**Enhancements**: Double Diamond discovery through delivery, HMW for pain point transformation

**Gate Criteria**:
- Journey maps complete with pain points and opportunities
- Sitemap covers all routes, views, and navigation patterns
- Wireframes for all key screens at all breakpoints
- Style guide: ALL tok.* tokens defined (colors, spacing, typography, etc.) - Single Source
- Interactive behaviors and state transitions documented

**Invoking ux-chain skill...**

## Workstream C: Backend + Implementation

**Invoke**: api-backend skill

**Outputs** (2 documents in docs/implementation/):
1. **api-spec.md** - Complete API specification
   - All endpoints with request/response schemas
   - Authentication/authorization policies
   - Error handling envelope
   - API versioning strategy
   - Rate limiting policies
   - Observability standards (logging, metrics, tracing)

2. **implementation-plan.md** - NEW: Implementation task breakdown
   - Decomposes user stories (US-#) into granular implementation tasks
   - Task dependencies and sequencing
   - Effort estimates (story points or hours)
   - Team assignment guidelines

**Enhancements**: 5W2H for API design, HMW for integration challenges

**Gate Criteria**:
- All API endpoints documented with clear contracts
- Request/response schemas fully specified
- Authentication/authorization strategy defined
- Error handling envelope and status codes
- API versioning approach documented
- Rate limiting and throttling policies
- Observability standards (logging, metrics, tracing)
- Implementation plan with tasks, dependencies, and sequencing

**Invoking api-backend skill...**

## Convergence: Implementation Readiness

All three workstreams must converge before implementation begins:

**Data Track → API Track**:
- dict.* field definitions in data-dictionary.md
- ev.* event schemas in data-dictionary.md
- Database DDL in database-spec.md

**UX Track → Implementation Plan**:
- tok.* design tokens in style-guide.md
- Screen layouts in wireframes.md
- User stories (US-#) cross-referenced in implementation-plan.md

**API Track → Implementation Plan**:
- API endpoints in api-spec.md
- Request/response schemas
- Error handling contracts

## Single Source of Truth Validation

- [ ] tok.* tokens: ONLY defined in docs/design/style-guide.md
- [ ] dict.* fields: ONLY defined in docs/design/data-dictionary.md
- [ ] ev.* events: ONLY defined in docs/design/data-dictionary.md
- [ ] DDL (CREATE TABLE, indexes): ONLY defined in docs/design/database-spec.md
- [ ] API schemas: ONLY defined in docs/implementation/api-spec.md

**FORBIDDEN** (these files no longer exist):
- docs/implementation/srs.md (removed - NFRs now in tech-spec.md)
- docs/implementation/frd.md (removed - feature requirements in prd.md)
- docs/design/database-requirements.md (merged into database-spec.md)
- docs/design/database-schema.md (merged into database-spec.md)
- docs/design/frontend-requirements.md (eliminated - frontend ADRs in tech-spec.md)
- docs/design/design-requirements.md (eliminated - component specs in wireframes.md)
- docs/design/uxdd.md (eliminated - consolidated into wireframes.md and style-guide.md)

## Traceability Chains

**Data Traceability**:
```
PRD-F-# (prd) → entities (erd) → tables (docs/design/database-spec) → dict.* (docs/design/data-dictionary)
PRD-F-# (prd) → events → ev.* (docs/design/data-dictionary)
```

**UX Traceability**:
```
US-# (user-stories) → screens (docs/design/wireframes) → tok.* (docs/design/style-guide)
US-# (user-stories) → tasks (docs/implementation/implementation-plan)
```

**API Traceability**:
```
FS-* / US-# → API endpoints (api-spec)
FS-* / US-# → implementation tasks (implementation-plan)
```

## Step 3: Deliver Gate Validation

After all three workstreams complete, validating implementation readiness:

### Parallel Track Completeness

**Data Track**:
!`ls -1 docs/design/*.md 2>/dev/null | grep -E '(data-requirements|erd|database-spec|data-dictionary|data-flow-diagram|data-catalog)' | wc -l | xargs echo "Data documents:"`
Expected: 6 documents

**UX Track**:
!`ls -1 docs/design/*.md 2>/dev/null | grep -E '(user-journey|ux-sitemap|wireframes|style-guide)' | wc -l | xargs echo "UX documents:"`
Expected: 4 documents

**Backend + Implementation Track**:
!`test -f docs/implementation/api-spec.md && echo "✓ api-spec.md exists"`
!`test -f docs/implementation/implementation-plan.md && echo "✓ implementation-plan.md exists"`

### Convergence Validation

Checking style guide has all design tokens:
!`grep -c "^tok\." docs/design/style-guide.md 2>/dev/null || echo "0"` token definitions

Checking data dictionary has all fields and events:
!`grep -c "^dict\." docs/design/data-dictionary.md 2>/dev/null || echo "0"` field definitions
!`grep -c "^ev\." docs/design/data-dictionary.md 2>/dev/null || echo "0"` event definitions

Checking API spec has endpoints:
!`grep -c "^## " docs/implementation/api-spec.md 2>/dev/null || echo "0"` endpoint sections

### Single Source of Truth Validation

Verifying no duplicates across document boundaries:
!`if grep -l "tok\." docs/design/*.md docs/implementation/*.md 2>/dev/null | grep -v style-guide.md; then echo "✗ Tokens defined outside style-guide.md"; else echo "✓ Tokens isolated to style-guide.md"; fi`

!`if grep -l "dict\." docs/design/*.md docs/implementation/*.md 2>/dev/null | grep -v data-dictionary.md; then echo "✗ Fields defined outside data-dictionary.md"; else echo "✓ Fields isolated to data-dictionary.md"; fi`

!`if grep -l "CREATE TABLE" docs/design/*.md docs/implementation/*.md 2>/dev/null | grep -v database-spec.md; then echo "✗ DDL defined outside database-spec.md"; else echo "✓ DDL isolated to database-spec.md"; fi`

## Gate Decision

**Status**: Checking all workstreams complete and synchronized...
!`test -f docs/design/data-dictionary.md && test -f docs/design/style-guide.md && test -f docs/implementation/api-spec.md && test -f docs/implementation/implementation-plan.md && echo "✓ PASS - All workstreams complete" || echo "✗ FAIL - Workstream(s) incomplete"`

**Decision Options**:
- **GO**: All workstreams complete, SST validated, proceed to implementation readiness gate
- **ITERATE**: Resolve conflicts between tracks (data-UX-API mismatches)
- **BLOCK**: One or more workstreams incomplete, continue work

## Next Steps

If **Deliver Gate PASSED**:

All implementation specifications are ready:
- ✅ Data architecture complete (6 docs in docs/design/)
- ✅ UX specifications complete (4 docs in docs/design/)
- ✅ Backend API specs complete (api-spec.md in docs/implementation/)
- ✅ Implementation plan complete (implementation-plan.md in docs/implementation/)
- ✅ Traceability maintained (PRD-F-# → erd → database-spec → dict.*)
- ✅ Single Source of Truth validated (no duplicates)

**Ready for implementation planning!**

Run final validation:
```
/validate-gate implementation-readiness
```

Or check quality:
```
/check-traceability
/check-sst
```

---

**Deliver phase complete!** All parallel workstreams converged. Documentation ready for implementation.
