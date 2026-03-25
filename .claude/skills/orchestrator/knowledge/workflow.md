# Complete Documentation Workflow

## Table of Contents

1. [Visual Diagram of 4 Phases](#visual-diagram-of-4-phases)
2. [Phase 1: DISCOVERY](#phase-1-discovery)
3. [Phase 2: PLANNING](#phase-2-planning)
4. [Phase 3a: DESIGN — Architecture](#phase-3a-design--architecture)
5. [Phase 3b: DESIGN — Parallel (Data + UX + API)](#phase-3b-design--parallel-data--ux--api)
6. [Phase 3 Complete: Implementation Readiness Gate](#phase-3-complete-implementation-readiness-gate)
7. [Phase 4: IMPLEMENTATION](#phase-4-implementation)
8. [ID Sequences and Traceability](#id-sequences-and-traceability)
9. [Decisions by Gate](#decisions-by-gate)
10. [Workflow Summary](#workflow-summary)

## Visual Diagram of 4 Phases

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DISCOVERY PHASE                             │
│                    (discovery-agent)                                │
│  Input: Problem / Product Idea                                      │
│  Output: project-context.md + product-vision.md                     │
│  Time: ~15 minutes                                                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                    ┌──────▼────────┐
                    │ DISCOVERY GATE │
                    │ GO / NO-GO /   │
                    │ ITERATE        │
                    └──────┬─────────┘
                           │ GO
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                        PLANNING PHASE                               │
│                    (planning-agent)                                 │
│  Input: vision + problem statement                                  │
│  Output: prd.md + user-stories.md + feature-spec-*.md              │
│  Time: ~15 minutes                                                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                    ┌──────▼────────┐
                    │ PLANNING GATE  │
                    │ GO / DESCOPE / │
                    │ ITERATE        │
                    └──────┬─────────┘
                           │ GO
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                       DESIGN PHASE (3a)                             │
│                  (architecture-agent)                               │
│  Input: prd.md + user-stories.md                                   │
│  Output: architecture-diagram.md + tech-spec.md (includes NFRs)    │
│  Time: ~10 minutes                                                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                    ┌──────────▼──────────────┐
                    │ Triggers Phase 3b        │
                    │ (3 agents in parallel)   │
                    └──────────┬───────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
    ┌───────▼───────┐  ┌──────▼──────┐  ┌──────▼──────┐
    │  DATA AGENT   │  │  UX AGENT   │  │ API AGENT   │
    │               │  │             │  │             │
    │ 6 docs:       │  │ 4 docs:     │  │ 1 doc:      │
    │ • data-req    │  │ • journey   │  │ • api-spec  │
    │ • erd         │  │ • sitemap   │  │             │
    │ • db-spec     │  │ • wireframes│  │             │
    │ • dict        │  │ • style-    │  │             │
    │ • flow        │  │   guide     │  │             │
    │ • catalog     │  │             │  │             │
    └───────┬───────┘  └──────┬──────┘  └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │
            ┌──────────────────▼──────────────────┐
            │ Waits for 3 agents completion       │
            │ (+ context from architecture-agent) │
            └──────────────────┬──────────────────┘
                               │
                ┌──────────────▼──────────────┐
                │ IMPLEMENTATION READINESS    │
                │ GATE                        │
                │ GO / REDESIGN / ITERATE     │
                └──────────────┬──────────────┘
                               │ GO
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                   IMPLEMENTATION PHASE                              │
│               (implementation-agent)                                │
│  Input: All 17 previous docs                                       │
│  Output: implementation-plan.md + quality-checklist.md +           │
│         release-plan.md                                             │
│  Time: ~10 minutes                                                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                    ┌──────▼─────────────┐
                    │ DOCUMENTATION      │
                    │ COMPLETE!          │
                    │ 21 docs generated  │
                    │ Ready to code!     │
                    └────────────────────┘
```

## Phase 1: DISCOVERY

**Objective:** Understand what is being built, why, and for whom.

**Input:** A problem statement or idea ("Invoice management system for freelancers")

**Activities:**
1. **5W2H Analysis** — Systematically answer:
   - **What?** What exactly is the product?
   - **Who?** Who are the users? Who pays?
   - **Where?** Where will it be used? (web, mobile, SaaS?)
   - **When?** Expected timeline? When to launch MVP?
   - **Why?** Why now? What's the problem? What's the opportunity?
   - **How?** How will it be delivered? What technologies?
   - **How much?** Budget? TAM/SAM/SOM?

2. **Validate Problem-Solution Fit** — Is the problem real? Does the proposed solution solve it?

3. **Generate Output:**
   - `docs/ets/projects/{project-slug}/discovery/project-context.md` — project context (5W2H answered)
   - `docs/ets/projects/{project-slug}/discovery/product-vision.md` — clear vision in 1-2 pages

**Expected Time:** ~15 minutes (interactive conversation)

**Expected Output:**
```
project-context.md:
- WHAT: Product description
- WHO: Personas + market
- WHERE: Delivery platforms
- WHEN: Timeline and milestones
- WHY: Problem + opportunity
- HOW: Conceptual architecture
- HOW MUCH: TAM/SAM/SOM, budget

product-vision.md:
- Vision statement (1 paragraph)
- Mission statement (1 paragraph)
- Core values (3-5)
- Success metrics (3-5)
- Problem solved (1 paragraph)
- Market opportunity (1 paragraph)
```

**Gate:** Discovery Gate → Clear vision? 5W2H complete? Problem validated? Opportunity justified?

---

## Phase 2: PLANNING

**Objective:** Translate vision into concrete requirements, prioritize and structure work.

**Input:** project-context.md + product-vision.md (from Phase 1)

**Activities:**
1. **Feature Brainstorm** — List all possible features (without filter)
2. **MoSCoW Prioritization** — Classify each feature:
   - **Must:** Essential for MVP
   - **Should:** Important, but can be delayed
   - **Could:** Nice to have
   - **Won't:** Discarded (out of scope)
3. **Write User Stories** — For each "Must" and "Should":
   - Format: "As [persona], I want [action] so that [benefit]"
   - Acceptance Criteria: Given/When/Then
4. **Feature Specs** — For complex features (>3 business rules):
   - State machines, validations, edge cases
   - Multi-step workflows, data transformations
   - Error handling, recovery flows

**Output:**
- `docs/ets/projects/{project-slug}/planning/prd.md` — Product Requirements Document
  - Business objectives (BO-1, BO-2, ...)
  - Feature list with prioritization (PRD-F-1, PRD-F-2, ...)
  - Success metrics
  - Out of scope

- `docs/ets/projects/{project-slug}/planning/user-stories.md` — User Stories + Acceptance Criteria
  - Stories organized by feature (US-1, US-2, ...)
  - Given/When/Then acceptance criteria
  - Dependencies

- `docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-[kebab-name].md` (as needed)
  - State machines / workflows
  - Business rules
  - Edge cases
  - Error scenarios

**Expected Time:** ~15 minutes (brainstorm + prioritization + writing)

**Gate:** Planning Gate → Requirements complete? Traceability validated? Scope realistic? Stories testable?

---

## Phase 3a: DESIGN — Architecture

**Objective:** Define technical architecture and non-functional requirements.

**Input:** prd.md + user-stories.md (from Phase 2)

**Activities:**
1. **Architecture Decisions**
   - Frontend / Backend / Database?
   - Monolith vs. Microservices?
   - Cloud provider (AWS/GCP/Azure)?
   - Real-time requirements?
   - Scalability needs?

2. **Define NFRs (Non-Functional Requirements)**
   - Performance: Latency targets, throughput
   - Availability: Uptime SLA (99.9%?)
   - Scalability: Concurrent users, data growth
   - Security: Auth, encryption, compliance
   - Reliability: RTO/RPO, disaster recovery

3. **ADRs (Architecture Decision Records)**
   - Document why each decision was made
   - Trade-offs considered

**Output:**
- `docs/ets/projects/{project-slug}/design/architecture-diagram.md` — Visual diagram (C4 model or similar)
  - Components (Frontend, API, Database, Services)
  - Data flows (requests, responses, queues)
  - External services (payment, auth, analytics)

- `docs/ets/projects/{project-slug}/design/tech-spec.md` — Technical Specification
  - Tech stack (languages, frameworks, DBs)
  - Architecture details
  - NFRs with numeric targets (NFR-1, NFR-2, ...)
  - ADRs (why each decision)
  - Deployment strategy
  - Security considerations
  - Monitoring & observability

**Expected Time:** ~10 minutes

**Note:** This is the **prerequisite** for Phase 3b. All 3 parallel agents (data, ux, api) receive the tech-spec as context.

---

## Phase 3b: DESIGN — Parallel (Data + UX + API)

**Objective:** Design data, UX and API in parallel, using architecture as base.

### Data Agent

**Input:** prd.md + user-stories.md + tech-spec.md

**Output:**
1. `docs/ets/projects/{project-slug}/design/data-requirements.md`
   - Entities identified
   - Entity relationships
   - Estimated data volume
   - Data retention

2. `docs/ets/projects/{project-slug}/design/erd.md`
   - Entity-relationship diagram
   - Tables and relationships
   - Primary keys, foreign keys

3. `docs/ets/projects/{project-slug}/design/database-spec.md`
   - DDL (CREATE TABLE statements)
   - Indexes and constraints
   - Normalization decisions

4. `docs/ets/projects/{project-slug}/design/data-dictionary.md`
   - Field by field (dict.domain.field)
   - Types, validations, defaults
   - Event catalog (ev.domain.action)

5. `docs/ets/projects/{project-slug}/design/data-flow-diagram.md`
   - How data flows through the system
   - Sources, transformations, sinks

6. `docs/ets/projects/{project-slug}/design/data-catalog.md`
   - Metadata: schemas, lineage, ownership
   - Data quality rules
   - Privacy/compliance rules (GDPR, etc)

**Time:** ~15 minutes

### UX Agent

**Input:** prd.md + user-stories.md + tech-spec.md

**Output:**
1. `docs/ets/projects/{project-slug}/design/user-journey.md`
   - End-to-end journey (user flow)
   - Touchpoints (web, email, mobile)
   - Emotional journey (pain points, moments of joy)

2. `docs/ets/projects/{project-slug}/design/ux-sitemap.md`
   - Site structure / navigation
   - Pages/screens and their relationships
   - User paths through the sitemap

3. `docs/ets/projects/{project-slug}/design/wireframes.md`
   - Low-fi wireframes (Excalidraw, mermaid)
   - Key screens/pages
   - Layout and components

4. `docs/ets/projects/{project-slug}/design/style-guide.md`
   - Design tokens (tok.color, tok.spacing, tok.typography)
   - Component library (button, card, modal, etc)
   - Accessibility guidelines (WCAG AA)
   - Visual language (colors, icons, illustrations)

**Time:** ~20 minutes

### API Agent

**Input:** prd.md + user-stories.md + tech-spec.md + data-dictionary.md

**Output:**
1. `docs/ets/projects/{project-slug}/design/api-spec.md`
   - OpenAPI 3.0 spec (or similar)
   - Endpoints (REST paths, HTTP methods)
   - Request/response schemas (referencing data-dictionary)
   - Error responses
   - Rate limiting, authentication
   - Versioning strategy

**Time:** ~10 minutes

### Parallel Execution

**How it works:**
```
Orchestrator: "Starting Parallel Design. Dispatching 3 agents..."

[Agent 1] Data Agent
  Input: PRD + user-stories + tech-spec + context
  Generates: 6 docs in docs/ets/projects/{project-slug}/design/
  Output: "REPORT: 6 docs generated. Tables: X. Entities: Y. Events: Z."

[Agent 2] UX Agent
  Input: PRD + user-stories + tech-spec + context
  Generates: 4 docs in docs/ets/projects/{project-slug}/design/
  Output: "REPORT: 4 docs generated. Screens: X. User flows: Y."

[Agent 3] API Agent
  Input: PRD + user-stories + tech-spec + data-dictionary (from Agent 1) + context
  Generates: 1 doc in docs/ets/projects/{project-slug}/design/
  Output: "REPORT: 1 doc generated. Endpoints: X. Schemas: Y."

[Orchestrator waits for 3 reports]

Orchestrator: "Design complete. Implementation Readiness Gate..."
```

**Total Time:** ~20 minutes (parallel, not sequential)

---

## Phase 3 Complete: Implementation Readiness Gate

**Checklist:**
- ✓ Tech stack chosen? (tech-spec.md)
- ✓ NFRs quantified? (NFR-1 to NFR-N in tech-spec.md)
- ✓ Data model validated? (database-spec.md + erd.md)
- ✓ UX flow is clear? (user-journey.md + wireframes.md)
- ✓ API contracts defined? (api-spec.md)
- ✓ Data dictionary complete? (data-dictionary.md)
- ✓ Security considered? (tech-spec.md)
- ✓ Scalability plausible? (tech-spec.md)
- ✓ No conflicts between tracks? (data ↔ api, ux ↔ backend)
- ✓ Ready to code?

**Decision:**
- **GO** → Implementation Phase
- **REDESIGN** → Redo architecture (back to 3a)
- **ITERATE** → Resolve specific gaps

---

## Phase 4: IMPLEMENTATION

**Objective:** Plan execution in sprints, define quality checklist.

**Input:** All 17 previous docs (discovery + planning + complete design)

**Activities:**
1. **Break Down into Tasks**
   - For each user story, identify technical tasks
   - Estimate effort (T-shirt sizing: XS/S/M/L/XL)
   - Identify dependencies

2. **Sprint Planning**
   - 1-2 week sprints (configurable)
   - Distribute tasks across sprints
   - Identify critical path

3. **Quality Checklist**
   - Unit test coverage target
   - E2E test scenarios
   - Code review criteria
   - Performance testing
   - Security testing
   - Deployment checklist

**Output:**
1. `docs/ets/projects/{project-slug}/implementation/implementation-plan.md`
   - Overview
   - Phase breakdown (MVP vs. Phase 2 vs. Phase 3)
   - Sprint structure
   - Task list (impl-1, impl-2, ...)
   - Dependencies
   - Risks & mitigations

2. `docs/ets/projects/{project-slug}/state/execution-status.yaml`
   - Sprints 1-N
   - Per-sprint tasks
   - Estimated vs. actual burn-down
   - Owner per task
   - Status (TODO/IN-PROGRESS/DONE/BLOCKED)

3. `docs/ets/projects/{project-slug}/implementation/quality-checklist.md`
   - Code quality targets
   - Test coverage targets
   - Performance benchmarks
   - Security checklist
   - Deployment readiness
   - Launch criteria

**Time:** ~10 minutes

---

## ID Sequences and Traceability

```
BO-1, BO-2, BO-3         ← Business Objectives (product-vision.md)
  ↓
PRD-F-1, PRD-F-2, ...    ← Product Features (prd.md)
  ↓
US-1, US-2, ...          ← User Stories (user-stories.md)
  ↓
FS-[kebab-name]-1, ...   ← Feature Specs (feature-spec-[name].md, when necessary)
  ↓
NFR-1, NFR-2, ...        ← Non-Functional Requirements (tech-spec.md)

ev.domain.action         ← Events (data-dictionary.md)
dict.domain.field        ← Data fields (data-dictionary.md)
tok.category.name        ← Design tokens (style-guide.md)

ADR-1, ADR-2, ...        ← Architecture Decisions (tech-spec.md)

impl-1, impl-2, ...      ← Implementation tasks (implementation-plan.md)
```

**Rule:** Every downstream ID references an upstream ID. No orphans.

---

## Decisions by Gate

### Discovery Gate (after Phase 1)
```
Criteria:
- [ ] Is the problem clear and validated?
- [ ] Were 5W2H answered?
- [ ] Is the opportunity quantified (TAM/SAM/SOM)?
- [ ] Is the vision statement aligned with stakeholders?

Decision:
GO → Proceed to Planning
NO-GO → Stop project (not viable)
ITERATE → Refine vision (run discovery again)
```

### Planning Gate (after Phase 2)
```
Criteria:
- [ ] Is the PRD complete and clear?
- [ ] Do user stories have testable acceptance criteria?
- [ ] Are feature specs done for complex features?
- [ ] Is MoSCoW prioritization accepted by stakeholders?
- [ ] Is scope realistic for 1 MVP?

Decision:
GO → Proceed to Design
DESCOPE → Remove "Could" features (keep only Must + Should)
ITERATE → Refine requirements (run planning again)
```

### Implementation Readiness Gate (after Phase 3)
```
Criteria:
- [ ] Is tech stack chosen and justified?
- [ ] Are NFRs quantified (latency, throughput, uptime)?
- [ ] Is database design validated and normalized?
- [ ] Is UX flow clear and wireframes ready?
- [ ] Are API contracts defined (OpenAPI spec)?
- [ ] Are security & compliance considered?
- [ ] Are there no conflicts between data/api/ux tracks?
- [ ] Is architecture scalable for expected growth?

Decision:
GO → Proceed to Implementation
REDESIGN → Go back to Phase 3a (redo architecture)
ITERATE → Resolve specific gaps (reconcile tracks)
```

---

## Workflow Summary (One Line per Phase)

| Phase | Agent | Input | Output | Gate | Time |
|-------|-------|-------|--------|------|------|
| 1 | discovery-agent | Problem | project-context + vision | Discovery | 15m |
| 2 | planning-agent | Vision | prd + stories + specs | Planning | 15m |
| 3a | architecture-agent | PRD + stories | architecture + tech-spec | — | 10m |
| 3b | data + ux + api (parallel) | arch context | 11 docs | Implementation Readiness | 20m |
| 4 | implementation-agent | 17 docs | plan + sprints + checklist | — | 10m |

**Total Time:** ~70 minutes end-to-end (with 3 interactive gates)

---

**Version:** 1.0 (2026-03-14)
**Language:** English
**Status:** Reference for orchestrator
