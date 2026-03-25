---
doc_meta:
  id: prd
  display_name: Product Requirements Doc
  pillar: Define
  owner_role: Product Lead
  summary: Translates vision into scoped features with success criteria, scope boundaries, and rollout strategy.
  order: 2
  gate: planning
  requires:
  - vis
  optional: []
  feeds:
  - stor
  - fs
uuid: <UUID>
version: 1.0.0
status: Draft
owners:
- <owner>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- PRD
- Planning
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Product Requirements Doc — [Tool Name]

**Author:** [Your Name] · **Date:** [YYYY-MM-DD]

> **Owner:** Defines WHAT we will deliver.
> **No** acceptance criteria here (User Stories own Given/When/Then).
> **No** NFRs here (Software Requirements Spec owns quantified targets).

---

## 0) Problem Context (summary)

Link to Product Vision (problem statement, North Star metric) that this PRD addresses.

**North Star Metric:** [Reference from Vision] — Baseline: [X], Target: [Y], Timeline: [when]

**Business Objectives (refs):** [Link to BO-# if this relates to broader business goals]

---

## 1) Goals & Success

### Product Goals

Clear statements tied to solving the problem:

- **Goal 1:** [Problem-focused outcome]
  - Tied to North Star: [how this moves the metric]
  - Success defined by: [measurable signal]

- **Goal 2:** [Secondary outcome]
  - Tied to: [metric or customer outcome]

### Global Success Criteria

Measurable outcomes that indicate features are working:

- [Quantified metric change]
  - Example: "Reduce average days-to-payment by 50% (37 → 18 days)"

- [Adoption metric]
  - Example: "50% of beta freelancers actively using automation"

- [Customer satisfaction]
  - Example: "NPS increase of 5+ points among users"

---

## 2) Scope & Non-Goals

### In-Scope

**Behaviors the product WILL support:**

- [Feature 1: what users can do]
- [Feature 2: what users can do]
- [Feature 3: what users can do]

### Out-of-Scope

**Explicitly EXCLUDED + rationale:**

- [Feature]: Why excluded (too complex for MVP, requires [dependency], post-MVP enhancement)
- [Feature]: Why excluded
- [Feature]: Why excluded

**Rationale:** Clear scope boundaries prevent feature creep and keep team focused.

### Constraints

**Legal/Compliance:**
- [Applicable regulations: GDPR, PCI-DSS, etc.]
- [Contractual obligations]

**Technical:**
- [Device/browser support]
- [Platform limitations]
- [Data residency requirements]

**Business:**
- [Time to market deadline]
- [Resource limitations]
- [Budget constraints]

---

## 3) Feature Set (PRD-F-#) — one block per feature

### PRD-F-1 — [Feature Name]

**Problem→Feature Link:** [Problem from Vision] → [Feature solving it] → [Success outcome]

**Feature Description:** [What users can do with this feature, in plain language]

**Success Criteria (measurable):**
- [Metric 1 that proves this feature worked]
- [Metric 2 showing adoption or value]
- [Metric 3 showing business impact]

**Key User Scenarios:**
- [Scenario 1: typical happy path]
- [Scenario 2: common variation]
- [Scenario 3: edge case or alternative]

**Dependencies:**
- **Platform:** [Required infrastructure or services]
- **Data:** [Required data sources or integrations]
- **Feature:** [Other features that must ship first]
- **External:** [Third-party integrations needed]

**Data Touchpoints:**
- **Events to emit:** ev.domain.action (example: ev.invoice.reminder-sent)
  - _(Payload schema lives in Data Dictionary, not here)_
- **Entities/Tables:** [Database entities this feature creates/updates]

**Integrations:**
- **Backend endpoints:** [API endpoints needed, refs as be-ep-#]
- **External services:** [Third-party APIs to call]

**UX Guardrails (rules, not pixels):**
- **Accessibility:** [WCAG requirements]
- **Internationalization:** [Languages/locales to support]
- **Consistency:** [Design system patterns to follow]

**Risks & Mitigations:**
- **R-1:** [Risk description] → [Mitigation strategy]
- **R-2:** [Risk] → [Mitigation]

**Open Questions:**
- **Q-1:** [Clarification needed]
- **Q-2:** [Decision pending]

**Assumptions:**
- **A-1:** [Assumption from Vision CSD]
- **A-2:** [Assumption we're making]

**Rollout & Flags:**
- **Feature flag:** [Flag name] — controls access
- **Rollout strategy:** [Gradual rollout to % of users? Or GA immediately?]
- **Success gates:** [What metrics must pass before expanding rollout?]
- **Failure gates:** [What metrics indicate we should rollback?]

**Traceability:**
- **Problem:** [Reference to Vision problem statement]
- **Acceptance:** User Stories: US-#, US-# (see User Stories for Given/When/Then)
- **Complexity:** [Does this feature need detailed spec (FS-[name])? Yes/No + reason]

---

### PRD-F-2 — [Next Feature Name]

[Repeat structure above for PRD-F-2]

---

### PRD-F-3 — [Additional Feature, if needed]

[Repeat structure]

---

## 4) Analytics & Telemetry Plan

### Key Events

Events this product will emit for tracking adoption and behavior:

| Event ID | Event Name | When it fires | Payload (link to Data Dict) | Dashboard |
| --- | --- | --- | --- | --- |
| ev.invoice.reminder_sent | Reminder sent to customer | User triggers or automation fires | [Link] | Reminder Activity |
| ev.payment.received | Payment received | Webhook from payment processor | [Link] | Cash Flow |
| ev.automation.enabled | User enabled automation | User toggles automation on | [Link] | Automation Adoption |

### Dashboards/KPIs

Where and how to track success:

- **Adoption:** Active users / total users (target: >50% in month 1)
- **Engagement:** Reminders sent / invoices created (target: >60%)
- **Business Impact:** Days to payment reduction (target: 50% improvement)
- **Satisfaction:** NPS / feature satisfaction survey (target: NPS +5)

### Guardrails

- **Attribution:** [How we attribute success/failure to feature vs other factors]
- **PII governance:** [What customer data we're safe to track]
- **Sampling:** [Are we sampling events or tracking 100%?]

---

## 5) Release & Rollout Plan

### Milestones

Staged rollout approach:

| Milestone | Users | Duration | Entry Criteria | Exit Criteria |
| --- | --- | --- | --- | --- |
| **Alpha (Internal)** | Team only (5-10) | 1 week | Feature developed | Team feedback incorporated |
| **Beta (Early Users)** | 50-100 power users | 2 weeks | Alpha gate passes | <5% critical bugs, NPS >7 |
| **Gradual GA** | 1% → 10% → 50% → 100% | 2 weeks | Beta gate passes | 95% p95 latency <500ms, <0.1% errors |
| **GA (General Availability)** | All users | Ongoing | Gradual GA passes | Revenue/engagement targets met |

### Feature Flags

Decouple deployment (code live) from release (feature visible):

| Flag | Purpose | Owner | Default | GA Timeline |
| --- | --- | --- | --- | --- |
| `enable_invoice_automation` | Control feature visibility | Product Lead | Off | Week 2 of Beta |
| `automation_reminder_cadence` | A/B test reminder frequency | Product/Data | "daily" | Week 1 of Beta |

### Communication Plan

Who needs to know what, when:

- **Engineering:** [Scope, timeline, dependencies] — kickoff meeting
- **Support:** [Feature overview, common questions] — 1 week before Beta
- **Customers:** [Feature announcement, signup/beta access] — 2 days before Beta
- **Leadership:** [Weekly progress, risk updates, launch readiness] — Friday standups

---

## 6) Risks & Decisions

### Risk Register

| Risk | Probability | Impact | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| [R-1 desc] | High | High | [Mitigation] | [Owner] | Active |
| [R-2 desc] | Medium | Medium | [Mitigation] | [Owner] | Active |

### Decision Log (Architecture Decision Records)

Link to Architecture Chain if major technical decisions exist:

- **ADR-#:** [Decision title + link]
- **ADR-#:** [Decision title + link]

---

## 7) References

### Upstream
- **vis** - Product Vision (problem statement, North Star, assumptions)

### Downstream
- **stor** - User Stories (acceptance criteria, Given/When/Then)
- **fs-[name]** - Feature Specifications (for complex features >3 rules or state machine)
- **arch** - Architecture Diagram (system design supporting this PRD)
- **srs** - Software Requirements Spec (NFRs: performance, scalability, security)
- **data** - Data Model (entities, relationships for this PRD)
- **uxs** - UX Sitemap (user journeys through features)
- **be** - Backend Requirements (API endpoints)
- **fe** - Frontend Requirements (components, UI)

---

## ✅ Planning Gate (PRD Review)

Before proceeding to Develop phase, validate:

- [ ] Clear success criteria per PRD-F-# (measurable, testable)
- [ ] Explicit non-goals & constraints (scope is defined)
- [ ] Feature set is MoSCoW prioritized (MUST/SHOULD/COULD/WON'T in separate doc)
- [ ] Every PRD-F-# has at least one user story (US-# in User Stories)
- [ ] Complex features (>3 rules or state machine) will have FS-[name] specs
- [ ] Traceability: Problem (vis) → Goal → PRD-F-# → US-# → FS (if needed)
- [ ] Rollout strategy defined with feature flags and exit criteria
- [ ] Analytics/telemetry plan covers key adoption metrics
- [ ] Risks identified with mitigations
- [ ] Team confident in scope (can you pitch this PRD in 5 min?)

**Decision:** GO (proceed to Develop phase) | DESCOPE (reduce feature set) | ITERATE (clarify requirements)

---

**End of Product Requirements Document**
