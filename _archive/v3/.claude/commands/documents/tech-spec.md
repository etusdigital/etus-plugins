---
description: Generate Technical Spec with NFRs and Architecture Decision Records (ADRs)
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Technical Spec

Creating tech spec with NFRs and ADRs for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/planning/user-stories.md && echo "✓ user-stories.md exists" || echo "⚠ Missing user stories (run /user-stories first)"`
!`test -f docs/design/architecture-diagram.md && echo "✓ architecture-diagram.md exists" || echo "⚠ Missing architecture diagram"`

## Setup

!`mkdir -p docs/design && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/architecture-chain/knowledge/tech-spec.md

## Interactive Technical Design

I'll help you define NFRs and create ADRs with implementation tactics:

### Step 1: Define NFRs (Non-Functional Requirements)

**Tech-spec is now the SINGLE SOURCE for NFR definitions.** We'll define NFR-# with numeric targets here.

**NFR Categories:**

1. **Performance NFRs** (response time, throughput, latency)
   - API response time targets (e.g., < 200ms for 95th percentile)
   - Page load time targets
   - Database query performance targets
   - Throughput targets (req/sec, events/sec)

2. **Security NFRs** (authentication, authorization, encryption, compliance)
   - Authentication mechanism (e.g., OAuth 2.0, JWT)
   - Authorization model (RBAC, ABAC)
   - Encryption standards (TLS 1.3, AES-256)
   - Compliance requirements (GDPR, HIPAA, SOC 2)
   - Vulnerability scanning frequency

3. **Scalability NFRs** (concurrent users, data growth, traffic peaks)
   - Max concurrent users target
   - Data storage growth expectations
   - Peak traffic handling (e.g., 10x normal load)
   - Geographic scaling strategy

4. **Reliability NFRs** (uptime, MTTR, backup)
   - Uptime target (e.g., 99.9% SLA)
   - Mean Time To Recovery (MTTR)
   - Backup frequency and retention
   - Disaster recovery RTO/RPO

5. **Maintainability NFRs** (code quality, logging, observability)
   - Code coverage targets
   - Logging and monitoring coverage
   - Documentation standards
   - Automated test coverage

6. **Usability NFRs** (accessibility, browser support)
   - WCAG compliance level (A, AA, AAA)
   - Browser/device support matrix
   - Mobile responsiveness requirements

**For each NFR category, ask:**

1. What is the numeric target? (e.g., 99.99% uptime, <2s response time)
2. Why is this target important? (business impact)
3. How will we measure/verify this? (monitoring, testing)
4. What's the priority? (MVP requirement vs. Phase 2?)

**Create NFR-# list:**

```
NFR-1: [Category] - [Requirement] - Target: [numeric value]
NFR-2: [Category] - [Requirement] - Target: [numeric value]
NFR-3: [Category] - [Requirement] - Target: [numeric value]
[Continue for all NFRs...]
```

Read existing documents for context:

@docs/planning/user-stories.md
@docs/design/architecture-diagram.md

### Step 2: Architecture Decision Records (ADRs)

**For each major architectural decision, ask:**

Let's document key architecture decisions as ADRs:

#### ADR-# Template:

1. **What decision are we documenting?** (e.g., database choice, API design, auth approach, frontend framework)
2. **Context**: Why is this decision needed? (5W2H analysis)
   - What problem does this solve?
   - What constraints exist?
   - What are we trying to achieve?
   - What NFRs drive this decision?
3. **Decision**: What are we proposing? (specific choice)
4. **Consequences**: What are the trade-offs?
   - Positive consequences?
   - Negative consequences?
   - Risks introduced?
5. **Alternatives Considered**: What else did we evaluate?
   - Option A: [description, pros/cons]
   - Option B: [description, pros/cons]
   - Why we didn't choose them?
6. **Status**: Proposed or Accepted?

[Create ADR-1, ADR-2, ADR-3, etc.]

**Key decision areas:**

- Technology stack choices (language, framework, database)
- Architectural patterns (microservices vs monolith, event-driven, etc.)
- Security approach (authentication, authorization, encryption)
- Data strategy (database, caching, replication)
- Integration approach (API design, message queues)
- DevOps strategy (CI/CD, hosting, monitoring)
- **Frontend technology decisions** (framework, state management, bundler, styling)
- **Frontend architecture** (component structure, routing, data fetching)

### Step 3: NFR Implementation Tactics

**For each NFR-#, ask:**

How will we implement **NFR-#**: [Requirement]?

1. **Implementation Approach**: Specific techniques/tactics to achieve this NFR
2. **Technologies/Tools**: What we'll use
3. **Owner**: Who's responsible for implementing this
4. **Timeline**: When will this be implemented? (MVP, Phase 2, etc.)
5. **Verification Plan**: How we'll test/measure success
6. **Dependencies**: What must exist first?

[Document tactics for each NFR-#]

**Example NFR Tactics:**

**NFR-1 (Response time < 200ms for 95th percentile):**
- Tactic 1: Implement Redis caching for frequently accessed data
- Tactic 2: Use CDN for static assets
- Tactic 3: Database query optimization with indexes
- Tactic 4: API response compression (gzip)
- Tactic 5: Connection pooling for database

**NFR-5 (TLS 1.3 encryption, AES-256 at rest):**
- Tactic 1: TLS 1.3 for all API endpoints
- Tactic 2: PostgreSQL encryption at rest
- Tactic 3: Encrypted S3 buckets
- Tactic 4: Secrets management with AWS Secrets Manager
- Tactic 5: Certificate pinning for mobile apps

**NFR-8 (99.99% uptime SLA):**
- Tactic 1: Multi-region deployment
- Tactic 2: Load balancing and auto-scaling
- Tactic 3: Database replication and failover
- Tactic 4: Health checks and automatic recovery
- Tactic 5: Monitoring and alerting infrastructure

### Step 4: Frontend Technology Decisions

**Tech-spec now absorbs frontend requirements.** For frontend:

1. **Framework choice**: React, Vue, Angular? Why?
2. **State management**: Context API, Redux, Zustand, etc.?
3. **Styling approach**: CSS-in-JS, Tailwind, styled-components?
4. **Build tooling**: Webpack, Vite, Parcel?
5. **Testing**: Vitest, Jest, Cypress for E2E?
6. **Component architecture**: Atomic design, feature-based, etc.?
7. **Performance optimization**: Code splitting, lazy loading, image optimization?
8. **Accessibility**: WCAG compliance strategy, a11y testing tools?

Document as ADRs for frontend decisions and include in tech-spec.

### Step 5: Deployment Strategy

**Ask about deployment approach:**

1. **Deployment pipeline**: CI/CD tool choice (GitHub Actions, GitLab CI, etc.)
2. **Environments**: Dev, Staging, Production setup
3. **Release strategy**: Blue-green, canary, rolling updates?
4. **Rollback plan**: How do we handle failed deployments?
5. **Monitoring**: APM, logging, alerting tools?

### Step 6: Runbooks

**Ask about operational procedures:**

1. **Deployment runbook**: Step-by-step deployment process
2. **Incident response**: How to handle outages/issues
3. **Backup/restore**: Procedures for data recovery
4. **Scaling runbook**: When and how to scale resources
5. **Common troubleshooting**: Known issues and fixes

### Step 7: Confirm Technical Design

"Here's the technical specification:

**NFRs Defined:**
- NFR-1: Performance - API response time < 200ms (95th percentile) - Verified via load testing
- NFR-2: Security - TLS 1.3 + AES-256 encryption - Verified via security audit
- NFR-3: Reliability - 99.99% uptime SLA - Verified via monitoring
[etc.]

**ADRs Documented:**
- ADR-1: Database choice (PostgreSQL) - chosen for ACID guarantees
- ADR-2: API design (REST) - chosen for simplicity and tooling
- ADR-3: Authentication (OAuth 2.0 + JWT) - chosen for security
- ADR-4: Frontend framework (React) - chosen for component reusability
[etc.]

**NFR Implementation:**
- NFR-1 → Redis caching, CDN, query optimization, connection pooling
- NFR-2 → TLS 1.3, encrypted storage, secrets management, cert pinning
- NFR-3 → Multi-region deployment, load balancing, health checks
[etc.]

**Deployment Strategy:** GitHub Actions CI/CD, blue-green deployments

Does this technical design address all NFRs and provide clear implementation guidance?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/tech-spec.md` using template structure.

**Document Structure:**
- Executive Summary
- Non-Functional Requirements (NFRs) - SINGLE SOURCE
  - For each NFR-#:
    - Category and numeric target
    - Business justification
    - Verification approach
    - Priority (MVP or Phase X)
- Architecture Decision Records (ADRs)
  - For each ADR-#:
    - Title and status
    - Context (5W2H)
    - Decision
    - Consequences
    - Alternatives considered
    - Related NFRs
  - Frontend technology ADRs included
- NFR Implementation Tactics
  - For each NFR-#:
    - Implementation approach
    - Technologies/tools
    - Owner and timeline
    - Verification plan
    - Dependencies
- Technology Stack
  - Frontend technologies
  - Backend technologies
  - Data storage
  - Infrastructure
  - DevOps tools
- Deployment Strategy
  - CI/CD pipeline
  - Environments
  - Release process
  - Rollback procedures
  - Monitoring and alerting
- Runbooks
  - Deployment runbook
  - Incident response
  - Backup/restore
  - Scaling procedures
  - Troubleshooting guide

## Validation

After generation:

!`test -f docs/design/tech-spec.md && echo "✓ tech-spec.md created" || echo "✗ Generation failed"`

**Tech spec checklist**:
!`if [ -f docs/design/tech-spec.md ]; then
  grep -o "NFR-[0-9]*" docs/design/tech-spec.md | sort -u | wc -l | xargs echo "NFRs defined:"
  grep -o "ADR-[0-9]*" docs/design/tech-spec.md | sort -u | wc -l | xargs echo "ADRs documented:"
  grep -ci "implementation\|tactic\|approach" docs/design/tech-spec.md | xargs echo "Implementation tactics:"
fi`

## Next Steps

**Validate Planning Gate**:
```
/validate-gate planning
```

**Continue to Deliver phase**:
```
/deliver
```

Or generate parallel workstreams:
```
/data-model      # 7 data documents
/ux-docs         # 8 UX documents
/api-spec        # Backend API spec
```

---

**Tech spec generated!** Non-functional requirements (NFRs) defined, architecture decisions (ADRs) and implementation tactics documented. Tech-spec is now the single source for NFRs and frontend technology decisions.
