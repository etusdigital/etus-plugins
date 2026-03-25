# Gate Checklists — Interactive Decision Points

## Table of Contents

1. [Discovery Gate](#discovery-gate-after-phase-1)
2. [Planning Gate](#planning-gate-after-phase-2)
3. [Implementation Readiness Gate](#implementation-readiness-gate-after-phase-3)
4. [How to Use These Checklists](#how-to-use-these-checklists)
5. [Gate Frequency](#gate-frequency)

## Discovery Gate (after Phase 1)

**When:** After discovery-agent completes project-context.md + product-vision.md

**Objective:** Validate that the problem is real, the vision is clear, and the opportunity justifies an MVP.

**Review Checklist:**

```markdown
### Context (project-context.md)

- [ ] WHAT: What exactly is the product?
      └─ Clear description in 1 paragraph?

- [ ] WHO: Who are the primary users?
      └─ 2-3 personas defined with needs?

- [ ] WHERE: Where will it be delivered (web/mobile/desktop)?
      └─ Platforms identified?

- [ ] WHEN: Expected timeline?
      └─ MVP date + Phase 2 date defined?

- [ ] WHY: Why now? What's the problem?
      └─ Problem statement quantified?
      └─ Market trend or pain point validated?

- [ ] HOW: Solution concept (high-level)?
      └─ Clear approach (app, SaaS, plugin, etc)?

- [ ] HOW MUCH: Market opportunity?
      └─ TAM/SAM/SOM estimated?
      └─ Budget allocated?

### Vision (product-vision.md)

- [ ] Vision Statement: One inspirational sentence?
      └─ Ex: "Make freelancer invoicing as easy as sending an email"

- [ ] Mission Statement: What does the product DO?
      └─ Ex: "Automate invoice generation, sending and tracking"

- [ ] Core Values: 3-5 key values?
      └─ Ex: "Simplicity, privacy, speed"

- [ ] Success Metrics: 3-5 KPIs?
      └─ Ex: "1000 MAU in month 3", "80% retention", "< 2min setup"

- [ ] Problem Solved: Problem summary?
      └─ Clear to someone who doesn't know the project?

- [ ] Market Opportunity: Why does this matter?
      └─ Market size, growth, competitive landscape?

### General Validation

- [ ] Has the problem been validated with potential users? (conversations, surveys)
      └─ "Yes, I talked to 5 freelancers and 4/5 have this pain"

- [ ] Is solution fit clear?
      └─ "Yes, proposed solution solves the problem in a viable way"

- [ ] Is competitive differentiation identified?
      └─ "Yes, we are faster/cheaper/more private than [competitor]"

- [ ] Are stakeholders aligned on the vision?
      └─ "Yes, product owner + CEO approved"

- [ ] Does the team believe it's viable?
      └─ "Yes, tech stack chosen, timeline realistic"
```

**Approval Criteria:** All [ ] must be [x]

**Possible Decisions:**

| Decision | Next Step | Why? |
|----------|-----------|------|
| **GO** | Start Planning Phase | All criteria ok, problem validated, opportunity clear |
| **NO-GO** | Stop project | Problem is not real OR opportunity is small OR team not convinced |
| **ITERATE** | Run discovery again | Vision still unclear, need to refine problem/solution fit |

**Decision Output:**
```
Decision: [GO / NO-GO / ITERATE]
Reason: [1-2 sentences]
Next Actions: [if GO: "Start Planning"; if NO-GO: "Archive"; if ITERATE: "Refine vision"]
```

---

## Planning Gate (after Phase 2)

**When:** After planning-agent completes prd.md + user-stories.md + feature-specs/*

**Objective:** Validate that requirements are complete, stories are testable, scope is realistic for MVP.

**Review Checklist:**

```markdown
### PRD (prd.md)

- [ ] Business Objectives: BO-# derived from vision?
      └─ 3-5 BO-# quantified (ex: "Reduce time 80%", "Reach 1000 MAU")

- [ ] Feature List: PRD-F-# mapped with prioritization?
      └─ Must (MVP): 5-8 features
      └─ Should (Phase 2): 3-5 features
      └─ Could (Backlog): 5+ features
      └─ Won't: Clearly discarded (negative scope)

- [ ] Does each PRD-F-# reference BO-#?
      └─ Traceability: "PRD-F-1 addresses BO-1 (Reduce time 80%)"

- [ ] Success Metrics: Measurable metrics per feature?
      └─ Ex: "PRD-F-1: 80% reduction in invoice creation time"

- [ ] Out of Scope: Clearly documented?
      └─ "We did not include: multi-currency, custom templates, etc"

- [ ] Dependencies: Interdependent features identified?
      └─ Ex: "Authentication (PRD-F-2) is prerequisite for Invoicing (PRD-F-3)"

### User Stories (user-stories.md)

- [ ] Does each PRD-F-# have US-#?
      └─ Minimum 2-3 stories per feature

- [ ] Correct Format: "As [persona], I want [action] so that [benefit]"?
      └─ Ex: "As freelancer, I want to generate invoices automatically to save 2h/week"

- [ ] Acceptance Criteria: Given/When/Then?
      └─ Minimum 3-5 testable criteria per story
      └─ Ex: "Given user logged in WHEN user clicks 'Generate Invoice' THEN invoice is generated in < 2s"

- [ ] Does each US-# reference PRD-F-#?
      └─ Traceability: "US-1 implements PRD-F-1 (Invoice Generation)"

- [ ] Are stories independent (or dependencies mapped)?
      └─ "US-5 depends on US-3 (must complete first)"

- [ ] Is no story too big?
      └─ Can each story fit in 1 sprint? If not, break into sub-stories

- [ ] Are personas described?
      └─ Freelancer: independent, 1-10 clients/month, 0-5000 billing/month
      └─ SMB: small business, 50+ clients, automation important

### Feature Specs (feature-specs/feature-spec-[kebab-name].md)

- [ ] Do specs exist only for complex features?
      └─ Rule: >3 business rules, multi-step workflows, state machines

- [ ] For each spec, is there corresponding US-#?
      └─ Traceability: "FS-[kebab]-1 details US-5"

- [ ] Does each spec have:
      └─ [ ] State machine or workflow diagram (visual)
      └─ [ ] Business rules listed (conditional logic)
      └─ [ ] Edge cases and error handling
      └─ [ ] Validations (constraints)

- [ ] Are examples included for clarity?
      └─ "Example: User creates invoice with $1000, tax calc = $80, total = $1080"

### General Validation

- [ ] Is scope realistic for 1 MVP?
      └─ "Yes, Must = 5 features, we estimate 8 weeks with team of 3"

- [ ] Is traceability 100% (BO → PRD-F → US → FS)?
      └─ No orphan BO-#
      └─ No PRD-F-# without US-#
      └─ No US-# without PRD-F-#
      └─ No FS-# without US-#

- [ ] Are stories testable (Given/When/Then)?
      └─ Can QA validate each story? "Yes"

- [ ] Do stakeholders approve scope?
      └─ "Yes, PM + exec aligned on Must/Should/Could"

- [ ] Does team believe in timeline?
      └─ "Yes, 8 weeks with team of 3 is viable"

- [ ] Have prioritization conflicts been resolved?
      └─ "Yes, 'Widget X' and 'Widget Y' were discussed, Widget X won"
```

**Approval Criteria:** All [ ] must be [x]

**Possible Decisions:**

| Decision | Next Step | Why? |
|----------|-----------|------|
| **GO** | Start Design Phase | Requirements complete, stories testable, scope viable |
| **DESCOPE** | Remove "Could" + "Should" | Scope too large, timeline not realistic → keep only Must |
| **ITERATE** | Refine requirements | Stories ambiguous OR traceability broken OR scope confusing |

**Decision Output:**
```
Decision: [GO / DESCOPE / ITERATE]
Descoped Features (if DESCOPE): [list of PRD-F-#]
Reason: [1-2 sentences]
Next Actions: [if GO: "Start Design Phase"; if DESCOPE: "Remove features, run gate again"]
```

---

## Implementation Readiness Gate (after Phase 3)

**When:** After architecture-agent + data-agent + ux-agent + api-agent complete their docs

**Objective:** Validate that design is viable, architecture is solid, no conflicts between tracks, ready to code.

**Review Checklist:**

```markdown
### Architecture & Tech Stack (tech-spec.md)

- [ ] Is tech stack chosen and justified?
      └─ Frontend: [React/Vue/Svelte], Backend: [Node/Go/Rust], DB: [PostgreSQL/MongoDB]
      └─ Cloud: [AWS/GCP/Azure]
      └─ Justification: "We chose Node because team knows it, quick time-to-market"

- [ ] Is there a high-level architecture diagram?
      └─ Components: Frontend, API, Database, Services?
      └─ Data flows: requests, responses, queues?
      └─ External services (payment, email, etc)?

- [ ] Is deployment strategy defined?
      └─ "Docker + Kubernetes" OR "Vercel + Supabase" OR "Heroku"
      └─ Is CI/CD pipeline planned?

- [ ] Is security considered?
      └─ [ ] Authentication method (JWT? OAuth? Sessions?)
      └─ [ ] Authorization model (RBAC? ABAC?)
      └─ [ ] Data encryption (at-rest, in-transit?)
      └─ [ ] GDPR/compliance concerns addressed?

- [ ] Is scalability plausible?
      └─ "We estimate 1000 MAU = X req/sec. Stack scales to 10X."

### NFRs (Non-Functional Requirements) — tech-spec.md

- [ ] Are Performance NFRs: NFR-1, NFR-2, ... quantified?
      └─ [ ] API response time < 200ms (p95)?
      └─ [ ] Page load < 3s?
      └─ [ ] Search indexing < 5min after write?
      └─ Each NFR has clear metric?

- [ ] Is Availability SLA defined?
      └─ [ ] 99.5% uptime? 99.9%? 99.99%?
      └─ [ ] Backup/recovery strategy?
      └─ [ ] RTO (Recovery Time Objective)?
      └─ [ ] RPO (Recovery Point Objective)?

- [ ] Are Scalability limits identified?
      └─ [ ] Max concurrent users?
      └─ [ ] Max data volume (GB/month)?
      └─ [ ] Max requests/second?

- [ ] Is Reliability error handling defined?
      └─ [ ] Max acceptable error rate?
      └─ [ ] Circuit breaker strategy?
      └─ [ ] Retry logic for transient failures?

- [ ] Are Security NFRs defined?
      └─ [ ] Password policy (length, complexity)?
      └─ [ ] Session timeout?
      └─ [ ] Rate limiting (per IP, per user)?
      └─ [ ] Audit logging requirements?

### ADRs (Architecture Decision Records) — tech-spec.md

- [ ] Are key decisions documented?
      └─ ADR-1: "Why monolith and not microservices?"
      └─ ADR-2: "Why PostgreSQL and not NoSQL?"
      └─ ADR-3: "Why React and not Vue?"

- [ ] Are trade-offs considered for each ADR?
      └─ "Monolith: simple, quick deploy. Drawback: limited scalability (mitigated by caching)"

### Data Design (data-requirements.md, erd.md, database-spec.md, data-dictionary.md)

- [ ] Are entities identified?
      └─ User, Invoice, Payment, etc?
      └─ Relationships mapped (1:1, 1:N, N:M)?

- [ ] Is ER Diagram validated?
      └─ Normal form (3NF minimum)?
      └─ No obvious redundancies?

- [ ] Is database spec complete?
      └─ [ ] CREATE TABLE statements for all entities?
      └─ [ ] Primary keys defined?
      └─ [ ] Foreign keys mapped?
      └─ [ ] Indexes for main queries?
      └─ [ ] Constraints (NOT NULL, UNIQUE, CHECK)?

- [ ] Is Data Dictionary complete?
      └─ [ ] Each field (dict.domain.field) has description?
      └─ [ ] Types clearly defined (STRING, INT, TIMESTAMP)?
      └─ [ ] Validations/constraints documented?
      └─ [ ] Default values defined?

- [ ] Is Event Catalog documented?
      └─ [ ] Events identified (ev.domain.action)?
      └─ [ ] When each event is triggered?
      └─ [ ] Payload of each event?
      └─ [ ] Consumer of each event?

- [ ] Is data volume estimated?
      └─ "We expect 1M invoices/year = X GB/year"

- [ ] Is backup/recovery for data planned?
      └─ "Daily snapshots, 30-day retention"

### UX Design (user-journey.md, ux-sitemap.md, wireframes.md, style-guide.md)

- [ ] Are user journeys mapped?
      └─ End-to-end flow for each persona (freelancer, client)?
      └─ Happy path + alternate paths?
      └─ Pain points identified and addressed?

- [ ] Is sitemap/navigation clear?
      └─ Logical structure (pages/screens related)?
      └─ User paths through the navigation?
      └─ Deep linking strategy?

- [ ] Are wireframes for key screens done?
      └─ [ ] Login screen?
      └─ [ ] Dashboard/home?
      └─ [ ] Main workflows (create invoice, view invoice, etc)?
      └─ [ ] Error states?

- [ ] Are design tokens defined?
      └─ [ ] Colors (primary, secondary, danger)?
      └─ [ ] Typography (headings, body, code)?
      └─ [ ] Spacing (padding, margin scale)?
      └─ [ ] Icons?

- [ ] Is component library planned?
      └─ Button, Card, Modal, Form, etc?
      └─ Accessibility (WCAG AA minimum)?

- [ ] Is responsive design considered?
      └─ Desktop, tablet, mobile breakpoints?

### API Design (api-spec.md)

- [ ] Is there OpenAPI 3.0 spec (or similar)?
      └─ All endpoints documented?
      └─ Request/response schemas?

- [ ] Are REST endpoints listed?
      └─ [ ] GET /api/invoices — list
      └─ [ ] POST /api/invoices — create
      └─ [ ] GET /api/invoices/{id} — read
      └─ [ ] PATCH /api/invoices/{id} — update
      └─ [ ] DELETE /api/invoices/{id} — delete
      └─ [ ] Other endpoints?

- [ ] Do schemas reference data-dictionary?
      └─ "Invoice schema uses dict.invoice.* fields"

- [ ] Are error responses defined?
      └─ [ ] 400 Bad Request (validation errors)?
      └─ [ ] 401 Unauthorized?
      └─ [ ] 403 Forbidden?
      └─ [ ] 404 Not Found?
      └─ [ ] 500 Internal Server Error?

- [ ] Is rate limiting documented?
      └─ "100 req/min per user"

- [ ] Is authentication strategy defined?
      └─ "JWT tokens, 24h expiry"

- [ ] Is versioning strategy defined?
      └─ "API v1 in URL: /api/v1/..."

### Cross-Track Validation

- [ ] Are data model ↔ API schemas aligned?
      └─ "Yes, invoice schema in api-spec references invoice table in erd"

- [ ] Are data model ↔ UX flows aligned?
      └─ "Yes, invoices listed in dashboard correspond to the model"

- [ ] Are API ↔ Tech stack aligned?
      └─ "Yes, Node/Express chosen supports schema patterns from api-spec"

- [ ] Are UX ↔ Feasibility aligned?
      └─ "Yes, design tokens + components implementable in React"

- [ ] Is there no conflict between architecture + data + api + ux?
      └─ "Yes, everything converges to same goal"

### General

- [ ] Is all documentation updated (17 docs from Phase 1-3)?
      └─ No "TODO" or "TBD" left?

- [ ] Is it ready to send to engineering team?
      └─ "Yes, everything clear, no ambiguity"

- [ ] Does a risk register exist?
      └─ "Yes, 5 risks identified + mitigations"

- [ ] Is go-to-market plan considered (out of scope, but considered)?
      └─ "Yes, landing page + email campaign planned"
```

**Approval Criteria:** All [ ] must be [x]

**Possible Decisions:**

| Decision | Next Step | Why? |
|----------|-----------|------|
| **GO** | Start Implementation Phase | Design coherent, architecture viable, no conflicts, ready to code |
| **REDESIGN** | Go back to Phase 3a | Fundamental architecture is flawed OR irreconcilable conflict between tracks |
| **ITERATE** | Resolve specific gaps | Minor gaps (ex: add 1 NFR, clarify 1 endpoint) |

**Decision Output:**
```
Decision: [GO / REDESIGN / ITERATE]
Gaps to Resolve (if ITERATE): [list of specific gaps]
Reason: [1-2 sentences]
Next Actions: [if GO: "Start Implementation"; if REDESIGN: "Redo architecture"]
```

---

## How to Use These Checklists

### 1. Before Invoking Gate Skill

```bash
# User says: "I think we're ready for the next phase"
# You select the correct checklist based on which phase was completed
# (Discovery, Planning, or Implementation Readiness)
```

### 2. During Gate Review

```bash
# Present checklist to user
# Together, go through each item [ ]
# If any is [x], continue
# If any is [ ], ask "What's missing here?"
```

### 3. Explicit Decision

```bash
# When all items are [x]:
# User: "All criteria seem ok. Can I move on?"
# You: "Yes, official decision: GO to [next phase]"
#      "Reason: [checklist summary]"
```

### 4. If Any Item Fails

```bash
# User: "Wait, we haven't described personas yet"
# You: "Ok, so decision is ITERATE. Let's refine planning?"
# Or: "DESCOPE? Remove feature that's taking your time?"
```

---

## Gate Frequency

```
Discovery Gate → after 15 minutes (discovery-agent)
                 ↓ GO (or ITERATE)

Planning Gate → after 30 minutes (planning-agent)
               ↓ GO (or DESCOPE/ITERATE)

Implementation Readiness Gate → after 50 minutes (arch + parallel design)
                                 ↓ GO (or REDESIGN/ITERATE)
```

---

**Version:** 1.0 (2026-03-14)
**Purpose:** Interactive checklists for 3 gates
**Status:** Ready for orchestrator integration
