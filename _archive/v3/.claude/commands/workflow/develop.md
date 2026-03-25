---
description: Run design phase - create architecture diagram and tech spec with NFRs
allowed-tools: Task, Read, Write, Bash, Grep
model: sonnet
---

# Design Phase

Running Design Phase (Divergent) - defining technical foundation with architecture and specifications

## Phase Overview

The **Design Phase** (Divergent) establishes technical architecture and non-functional requirements before parallel implementation workstreams.

**Outputs**: architecture-diagram.md, tech-spec.md (absorbs NFRs and ADRs)

## Pre-flight Checks

**Prerequisites - Planning Phase Complete**:
!`test -f docs/planning/user-stories.md && echo "✓ user-stories.md exists" || echo "✗ Missing user-stories.md (run /define first)"`

**Output directory**:
!`mkdir -p docs/design && echo "✓ Created docs/design/"`

**Existing design documents**:
!`ls -1 docs/design/ 2>/dev/null || echo "No design documents yet"`

## Step 1: Invoke Architecture Chain

I'll invoke the **architecture-chain** skill to generate technical architecture documents.

The skill will apply:
- **5W2H for NFR systematic definition**
- **HMW for constraint-to-opportunity transformation**
- **C4 modeling for architecture diagrams**
- **ADRs for technical decisions**

### Expected Outputs:

**1. Architecture Diagram (architecture-diagram.md)**

C4 Model (Context → Container → Component → Code):
- Level 1: System boundary and external dependencies
- Level 2: Major components and technology choices
- Level 3: Internal structure of key containers
- Level 4: Class-level detail (for complex components only)

**HMW for Architecture Constraints**:
```
Constraint: Microservices increase operational complexity
↓
HMW: How might we get microservice benefits with reduced overhead?
↓
Solution: Managed Kubernetes, service mesh, observability platform
```

**Visual representation**:
- ASCII diagrams or Mermaid syntax for system context
- Component dependencies and data flow
- Technology stack decisions with rationale

**2. Technical Spec (tech-spec.md)**

Absorbs Software Requirements Spec (NFRs) and Architecture Decision Records (ADRs):

### Section A: Non-Functional Requirements (5W2H Analysis)

**Performance NFRs**:
- WHAT: Response time, throughput, resource usage
- HOW MUCH: API < 200ms p95, DB queries < 50ms p99
- WHEN: Under normal load (e.g., 1000 concurrent users)
- HOW: Measure via APM tools
- WHO: Backend team owns, QA verifies
- WHY: User research shows 200ms = "instant"
- WHERE: All API endpoints except batch operations

**Scalability NFRs**:
- WHAT: System must scale horizontally
- HOW MUCH: Support 10k → 100k users within 6 months
- WHEN: Auto-scale at 70% CPU utilization
- HOW: Stateless services, database read replicas
- WHO: DevOps owns, monitored via CloudWatch
- WHY: Growth projections show 10x in year 1

**Security, Reliability, Maintainability NFRs** with same rigor

**HMW for NFR Trade-offs**:
```
Challenge: Achieving <200ms requires expensive caching
↓
HMW: How might we achieve target performance within budget?
↓
Solutions: Edge caching, query optimization, async processing
```

### Section B: Architecture Decision Records (ADRs)

Format for each ADR:

```
ADR-#: [Decision Title]
Status: Proposed|Accepted|Deprecated
Context: 5W2H analysis of decision
Decision: What are we proposing?
Consequences: What becomes easier/harder?
Alternatives Considered: What else evaluated?
```

Examples:
- ADR-1: Microservices vs. monolith
- ADR-2: Database choice (SQL vs. NoSQL)
- ADR-3: Frontend framework selection
- ADR-4: Caching strategy (Redis, CDN, in-memory)
- ADR-5: Authentication/authorization (OAuth, JWT, session-based)

### Section C: NFR Implementation Tactics

For each NFR-# from architecture requirements, document:

**Tactic 1: Multi-layer caching**
- Owner: Backend team
- Timeline: Sprint 1-2
- Implementation: Redis, CDN, browser cache
- Metrics: Cache hit ratio, latency reduction
- Verification: Load test with 10k concurrent users

**Tactic 2: Database query optimization**
- Owner: Database team
- Timeline: Sprint 1
- Implementation: Query profiling, indexing strategy
- Metrics: Query execution time, CPU usage
- Verification: Production APM monitoring

**Tactic 3: Async processing**
- Owner: Platform team
- Timeline: Sprint 2-3
- Implementation: Job queue, background workers
- Metrics: Queue depth, processing latency
- Verification: Synthetic monitoring

**Verification**: How to test, pass/fail criteria

**Deployment strategy**: Blue/green, feature flags, rollback procedures

**Runbooks**: Common failures, debugging, recovery steps

## Step 2: Design Gate Validation

After generation, validating Design Gate criteria:

### Architecture Completeness
- [ ] Architecture diagram has C4 levels (Context, Container, Component minimum)
- [ ] System boundaries clearly defined with external dependencies
- [ ] Component relationships and data flow documented
- [ ] Technology stack choices documented with rationale
- [ ] Every NFR has: target value, verification method, owner, acceptance threshold
- [ ] NFRs cover: performance, scalability, security, reliability, maintainability
- [ ] 5W2H analysis documented for key NFRs
- [ ] ADRs document major decisions with alternatives considered
- [ ] Implementation tactics defined for each critical NFR
- [ ] Validation plan exists for testing NFRs
- [ ] No architectural debt in critical path
- [ ] HMW statements show constraint-to-opportunity transformations

### NFR Traceability

Checking NFR coverage:
!`grep -o "NFR-[0-9]*" docs/design/tech-spec.md 2>/dev/null | sort -u | wc -l | xargs echo "NFRs defined:"`

Checking ADR coverage:
!`grep -o "ADR-[0-9]*" docs/design/tech-spec.md 2>/dev/null | sort -u | wc -l | xargs echo "ADRs documented:"`

### Architecture Validation
```
Architecture diagram exists: ✓
Tech spec with NFRs exists: ✓
ADRs document decisions: ✓
Implementation tactics defined: ✓
NFR targets quantified: ✓
5W2H analysis complete: ✓
```

## Gate Decision

**Status**: !`test -f docs/design/architecture-diagram.md && test -f docs/design/tech-spec.md && echo "✓ PASS" || echo "✗ FAIL - Missing documents"`

**Decision Options**:
- **GO**: Proceed to Deliver phase (run `/deliver`)
- **REDESIGN**: Architecture inadequate, needs rework
- **ITERATE**: Refine NFRs, ADRs, or architecture diagram

## Next Steps

If **Design Gate PASSED**:
```
Run: /deliver
```

This will launch **parallel workstreams**:
- **Data Chain**: Generate 6 data architecture documents (data-requirements, erd, database-spec, data-dictionary, data-flow-diagram, data-catalog) in docs/design/
- **UX Chain**: Generate 4 UX documents (user-journey, ux-sitemap, wireframes, style-guide) in docs/design/
- **Backend Chain**: Generate API spec (api-spec.md) in docs/implementation/
- **Implementation**: Generate implementation plan (implementation-plan.md) in docs/implementation/

---

**Design phase complete!** Technical foundation ready for parallel implementation workstreams.
