---
doc_meta:
  id: ctx
  display_name: Project Context
  pillar: Discovery
  owner_role: Product Lead
  summary: Living document capturing project identity, team context, technology stack decisions, and constraints that guide all downstream documentation.
  order: 0
  gate: discovery
  requires: []
  optional: []
  feeds:
    - vis
    - prd
    - arch
    - tech
uuid: <UUID>
version: 0.1.0
status: Draft
owners:
  - <owner>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
  - Discovery
  - Context
  - Governance
  - ETUS
ai_template_variables:
  - product
  - owner
  - namespace
---

# Project Context - [Project Name]

**Author:** [Your Name]
**Date:** [YYYY-MM-DD]
**Last Updated:** [YYYY-MM-DD]
**Status:** Living Document (Updated Throughout Project)

---

## Project Identity

**Project Name:** [Official project name]
**Namespace:** [Organizational code or domain, e.g., "acme-tools"]
**One-liner:** [Single sentence describing what this product does]

**Elevator Pitch:**
[2-3 sentences explaining the problem solved and target user, e.g., "An internal tool for freelance invoice tracking that replaces spreadsheets with real-time financial insights and automated tax reporting."]

**Mission Statement:**
[Why this project matters beyond just building software, e.g., "Enable solo freelancers to focus on their craft, not administrative overhead."]

---

## Team Context

### Team Composition

**Size:** [Solo / Small team (2-3) / Larger team]
**Structure:** [How the team is organized]

### Roles & Responsibilities

| Role              | Person            | Key Responsibilities |
| ----------------- | ----------------- | -------------------- |
| Product Lead      | [Your Name]       | [Vision, PRD, gate decisions] |
| Technical Lead    | [Name or TBD]     | [Architecture, tech decisions] |
| Designer/UX       | [Name or TBD]     | [UX, wireframes, design system] |
| Backend Lead      | [Name or TBD]     | [API, database, infrastructure] |
| QA/Testing        | [Name or TBD]     | [Test strategy, validation] |

### Communication Plan

- **Standup:** [Frequency and format, e.g., "Daily 9am async Slack"]
- **Gate reviews:** [How decisions are made, e.g., "Synchronous review with all leads"]
- **Document sharing:** [Where living docs are stored]

---

## Technology Stack Decisions

### Platform & Runtime

**Frontend Framework:** [React/Vue/Svelte/Other] - [Why chosen for this project]
**Backend Runtime:** [Node/Go/Python/Other] - [Why chosen for this project]
**Database:** [PostgreSQL/MySQL/MongoDB/SQLite] - [Why chosen for this project]
**Hosting:** [Vercel/Heroku/AWS/Self-hosted/Other] - [Cost, scalability, constraints]

### Key Technology Choices

| Technology      | Choice              | Rationale                                    |
| --------------- | ------------------- | -------------------------------------------- |
| Frontend        | [Framework/libs]    | [Why this choice]                            |
| Backend         | [Runtime/framework] | [Why this choice]                            |
| Database        | [System]            | [Why this choice]                            |
| Authentication  | [System]            | [Why this choice]                            |
| Hosting         | [Provider]          | [Cost, latency, compliance]                  |
| Monitoring      | [Tools]             | [Why this choice]                            |
| CI/CD           | [Platform]          | [Why this choice]                            |

### Technology Constraints

- **Must-use:** [Mandatory technologies, e.g., "Cloudflare Workers for edge"]
- **Must-avoid:** [Prohibited technologies, e.g., "No serverless due to latency SLA"]
- **Approved vendors:** [Restricted supplier list if applicable]
- **Licenses:** [GPL/MIT/Apache/commercial considerations]

### Development Environment

- **Node/Runtime version:** [e.g., "Node 20+"]
- **Package manager:** [npm/pnpm/yarn]
- **Local database:** [PostgreSQL/Docker/SQLite]
- **Dev tools:** [VS Code/WebStorm, linters, formatters]
- **Testing framework:** [Vitest/Jest/Testing Library]

---

## Constraints & Boundaries

### Business Constraints

- **Timeline:** [MVP deadline, e.g., "Q2 2026"]
- **Budget:** [Estimated cost, e.g., "$50K total for 3 months"]
- **Target users:** [Who will use this product]
- **Geographic scope:** [Countries/regions served]
- **Regulatory:** [GDPR/HIPAA/SOX/other compliance needs]

### Technical Constraints

- **Infrastructure budget:** [Max monthly spend, e.g., "$500/month"]
- **Concurrent users:** [Target capacity, e.g., "100 concurrent"]
- **Data volume:** [Expected records at launch and growth rate]
- **Latency requirement:** [SLA, e.g., "P95 < 200ms"]
- **Uptime requirement:** [99.9% / 99.95% / other]

### Scope Boundaries

**In Scope (MVP):**
- [Core feature 1]
- [Core feature 2]
- [Core feature 3]

**Out of Scope (Post-MVP):**
- [Feature postponed]
- [Advanced optimization deferred]
- [Complex integration delayed]

---

## Key Decisions Log

This section tracks lightweight ADRs (Architecture Decision Records) with pointers to full documentation.

### Decision 1: [Brief Title]

- **Date:** [YYYY-MM-DD]
- **Status:** [Accepted/Proposed/Superseded]
- **Context:** [Why this decision was needed]
- **Decision:** [What was decided]
- **Rationale:** [Why this choice]
- **Full ADR:** [Link to docs/architecture/decisions/adr-001.md if detailed]

### Decision 2: [Brief Title]

- **Date:** [YYYY-MM-DD]
- **Status:** [Accepted/Proposed]
- **Context:** [Why this decision was needed]
- **Decision:** [What was decided]
- **Rationale:** [Why this choice]

---

## Glossary & Domain Terms

| Term              | Definition                                                           |
| ----------------- | -------------------------------------------------------------------- |
| [Domain term 1]   | [Clear definition specific to this product]                          |
| [Domain term 2]   | [Clear definition specific to this product]                          |
| [Abbreviation]    | [What it stands for and means in this context]                       |
| [User role]       | [What this role does and responsibilities]                           |
| [Business entity] | [What it represents in the business domain]                          |

---

## External Dependencies

### Third-Party APIs & Services

| Service           | Purpose                    | Status | Cost/Tier |
| ----------------- | -------------------------- | ------ | --------- |
| [Service 1]       | [Why we use it]            | [Active/Planned] | [Pricing] |
| [Service 2]       | [Why we use it]            | [Active/Planned] | [Pricing] |

### SLA & Support Requirements

- **Support level needed:** [Community/Standard/Premium]
- **Uptime SLA required:** [99%/99.9%/other]
- **Response time requirement:** [For critical issues]

### Integration Points

- **Authentication:** [Auth0/Firebase/Custom]
- **Payment processing:** [Stripe/PayPal/other]
- **Analytics:** [Google Analytics/Mixpanel/custom]
- **Logging:** [Datadog/New Relic/CloudWatch]

---

## Governance & Change Management

### Documentation Standards

- **Living docs location:** [Where docs are stored, e.g., "GitHub /docs"]
- **Update frequency:** [How often docs are refreshed]
- **Review process:** [Who reviews doc changes]
- **Version control:** [How docs versioning is managed]

### Gate Decision Process

- **Gate reviews:** [Who participates in GO/NO-GO decisions]
- **Escalation path:** [Who decides on ITERATE/REDESIGN/BLOCK]
- **Approval criteria:** [What "ready" means at each gate]

### Known Risks & Mitigation

| Risk                | Impact | Likelihood | Mitigation                      |
| ------------------- | ------ | ---------- | ------------------------------- |
| [Technology risk]   | [High/Medium/Low] | [High/Medium/Low] | [What we're doing] |
| [Schedule risk]     | [High/Medium/Low] | [High/Medium/Low] | [What we're doing] |
| [Resource risk]     | [High/Medium/Low] | [High/Medium/Low] | [What we're doing] |

---

## Living Document Notice

**This document is maintained throughout the project lifecycle.**

- **Updated:** When new technology decisions are made
- **Updated:** When constraints change (budget, timeline, scope)
- **Updated:** When new team members join or roles change
- **Updated:** When regulatory or compliance requirements change
- **Referenced:** By all downstream documents (vis, prd, arch, tech)

**Change log:**
- [YYYY-MM-DD] - Initial creation
- [YYYY-MM-DD] - [What changed]

---

**Last Reviewed:** [YYYY-MM-DD]
**Next Review Date:** [YYYY-MM-DD]
