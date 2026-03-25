# Template: PRD (Product Requirements Document)

**File:** `docs/ets/projects/{project-slug}/planning/prd.md`

**Purpose:** Single Source of Truth for product features with prioritization and success criteria.

## Table of Contents
1. [Complete Structure](#complete-structure)
2. [Filling Notes](#filling-notes)
3. [Concrete Example](#concrete-example-minimal)
4. [Validation](#validation)

---

## Complete Structure

```markdown
# PRD - Product Requirements Document

## Executive Summary

[1-2 paragraphs linking product-vision.md to feature scope]

**Selected Solution Direction:** [SOL-#]

**Example:**
"The vision defines [X]. This PRD operationalizes that vision through 12 priority features,
focusing on [Must Have features]. We expect to validate [key assumption] and measure success via [primary metric]."

---

## Scope

### In-Scope

- Feature 1 (PRD-F-1) - Brief description
- Feature 2 (PRD-F-2) - Brief description
- [...]

### Out-of-Scope

- [Explicitly not doing]
- [Deferred to V2]
- [Rejected feature with brief reason]

---

## Priority Features

### Must Have (Essential MVP)

#### PRD-F-1: [Feature Name]

**Description:** [2-3 sentences describing the feature]

**Problem/Opportunity Addressed:** BO-# (link to business objective)

**Selected Solution Direction:** SOL-#

**How Might We:** [HMW statement that generated this feature]

**Success Criteria:**
- [Quantitative or qualitative metric]
- [How will we measure?]
- [Expected target?]

**Dependencies:** [Other features, technology, data]

---

#### PRD-F-2: [Feature Name]

[Repeat structure from PRD-F-1]

---

### Should Have (Important, Not Critical)

#### PRD-F-#: [Feature Name]

[Same structure as above]

---

### Could Have (Nice-to-Have)

#### PRD-F-#: [Feature Name]

[Same structure as above]

---

### Won't Have (Out of Scope)

#### PRD-F-#: [Feature Name] (Rejected)

**Reason:** [Why not in this version?]

---

## Non-Functional Requirements

### Performance
- [e.g., p95 < X ms; maximum payload size; page load time]

### Reliability / Availability
- [e.g., retries, fault tolerance, offline behavior, SLA targets]

### Security & LGPD
- Data collected: [list]
- Legal basis / consent: [required? where?]
- Retention and access: [rules]
- Masking / anonymization: [if applicable]

### Observability (mandatory for P0 features)
- Product events (tracking): [minimum list]
- Technical logs and metrics: [list]
- Alerts: [thresholds]

---

## Events & Data (Tracking)

### Minimum Events
| Event Name | When It Fires | Key Properties |
|------------|---------------|----------------|
| [event_1] | [trigger condition] | [properties] |
| [event_2] | [trigger condition] | [properties] |

### Required Properties
- campaign_id, quiz_id, user_id/anon_id, channel, device, [others as applicable]

### Destinations / Integrations
- [Analytics], [CRM/BMS], [Data Lake], [other destinations]

---

## Dependencies & Assumptions

### Technical Dependencies

- [Technology X required for PRD-F-#]
- [Integration with system Y]

### Business Assumptions

- [User behavior we expect]
- [Demand/volume expected]
- [Market timing]

### Risks

- [If assumption fails, impact on PRD-F-#]

---

## Rollout Plan (High Level)

### Strategy
- [Feature flag? canary? beta? progressive rollout?]

### Initial Segment
- [Who enters first — segment, percentage, criteria]

### Ramp-Up Plan
- [e.g., 10% → 25% → 50% → 100%, with criteria to advance]

### Rollback
- **Triggers:** [conversion drop > X%, error rate > Y%, p95 > Z ms]
- **Decision makers:** [PM + Tech Lead]
- **Procedure:** [steps to disable, validate, communicate]

### Communication
- **Internal:** [CS, Ops, Growth, etc.]
- **External:** [if applicable]

---

## Release Criteria

**This PRD is ready when:**

- [ ] All features have clear success criteria
- [ ] In/Out scope validated with stakeholders
- [ ] User Stories derived (1+ stories per PRD-F-#)
- [ ] Feature Specs created for complex features (>3 business rules)
- [ ] Rough effort estimate (per sprint)
- [ ] Dependencies mapped and communicated
- [ ] Planning Gate approval (GO decision)

---

## Statistics

| Metric | Count |
|--------|-------|
| Total Features | #PRD-F |
| Must Have | # |
| Should Have | # |
| Could Have | # |
| Won't Have (Rejected) | # |

---

## Traceability

Each PRD-F-# feeds into:
- user-stories.md (1+ US-# per PRD-F-#)
- feature-spec-[name].md (if >3 business rules)
- architecture-diagram.md (design based on features)
- api-spec.md (endpoints per features)
- implementation-plan.md (tasks per PRD-F-#)

**Chain:** BO-# → O-# → SOL-# → PRD-F-# → US-# → (FS-[name]-# if complex) → NFR-# → impl-#

```

---

## Filling Notes

### Section: Executive Summary

- Reference product-vision.md directly
- Mention 1-2 most important must-haves
- Indicate main problem being solved
- **Don't** detail features here (only in Features section)

### Section: In-Scope / Out-of-Scope

- **In-Scope:** List only features in this PRD
- **Out-of-Scope:** Be explicit about what NOT to do (prevents confusion)
- If rejected a feature, put in "Won't Have" with brief reason

### Section: Priority Features

**Critical Structure:**

```
#### PRD-F-#: [Feature Name]

**Description:** [Concise. What is it? Who uses it? Why?]

**Problem/Opportunity Addressed:** BO-# [link]

**How Might We:** [HMW that generated feature. Documents thinking.]

**Success Criteria:** [IMPORTANT: How will we know it worked?]
  - Quantitative metric (ex: "30% conversion increase")
  - Qualitative metric (ex: "Users report less friction")
  - Technical metric (ex: "Latency < 200ms")

**Dependencies:** [What other features depend on it? Tech stack? Data?]
```

### Fields By MoSCoW Priority

**Must Have:**
- Essential for MVP
- Blocks release? Yes
- Users will stop using without it? Yes

**Should Have:**
- Important for experience
- Blocks release? No
- Competitive differentiator

**Could Have:**
- Nice-to-have
- Blocks release? No
- Deferrable to V2

**Won't Have:**
- Explicitly rejected
- Reason: out of scope, late priority, or business decision
- Document why not (prevents re-litigation)

### PRD-F-# IDs

- Sequential without gaps (PRD-F-1, PRD-F-2, ..., PRD-F-N)
- Registered in `ids.yml` with feature name
- Once assigned, don't change (traceability)
- Example: `PRD-F-1: Authentication via OAuth`

### BO-# Links (Business Objectives)

Each PRD-F-# must be linked to BO-# from product-vision.md.

- One feature can cover multiple BO-# (rare)
- One BO-# can have multiple features (common)
- Validate that all BO-# are covered by at least one PRD-F-#

### Success Criteria

**Not boilerplate. Specific and measurable.**

Good:
- "Users complete onboarding flow in <3 minutes (measured by analytics)"
- "Validation rejection rate drops from 40% to <10%"
- "NPS increases from 6 to >8"

Bad:
- "Feature is well made"
- "Users are happy"
- "Works well"

### Statistics

Fill at end:
- Total PRD-F-# count
- Breakdown by Must/Should/Could/Won't
- Helps validate scope (many Could = scope creep)

---

## Concrete Example (Minimal)

```markdown
# PRD - Invoicing System

## Executive Summary

The product vision is to empower freelancers to manage invoices effortlessly.
This PRD defines 5 priority features for MVP,
focusing on quick invoice creation and payment tracking.
We will validate demand via waitlist form.

---

## Scope

### In-Scope

- PRD-F-1: Invoice Creation (template)
- PRD-F-2: Email Sending
- PRD-F-3: Payment Tracking
- PRD-F-4: Invoice Dashboard

### Out-of-Scope

- Accounting integration (deferred to V2)
- Multi-currency (start with USD)

---

## Priority Features

### Must Have

#### PRD-F-1: Invoice Creation (Template)

**Description:** Create invoice from pre-filled templates with
client data and work items.

**Problem/Opportunity:** BO-1 (Reduce administrative time)

**How Might We:** Create 1-click invoice process?

**Success Criteria:**
- Create invoice in <2 minutes
- Template reusable (user saves 5+ minutes per invoice)

**Dependencies:** Client system (PRD-F-5)

---

#### PRD-F-2: Email Sending

**Description:** Send invoice as PDF attachment in email to client.

**Problem/Opportunity:** BO-1, BO-2

**How Might We:** Make 1-click sending without leaving platform?

**Success Criteria:**
- 95%+ email delivery
- Open tracking

**Dependencies:** Email service integration

---

### Should Have

#### PRD-F-3: Payment Tracking

**Description:** Mark invoice as paid, with date and method.

**Problem/Opportunity:** BO-2 (Cash flow visibility)

**Success Criteria:**
- 80%+ invoices manually marked as paid
- Stripe integration (10% automatic)

---

### Could Have

#### PRD-F-4: Invoice Dashboard

**Description:** Overview of invoices (pending, paid, etc.)

---

## Release Criteria

- [ ] User Stories derived
- [ ] Planning Gate GO decision
- [ ] Rough estimates per feature

```

---

## Validation

**Before finalizing PRD:**

- [ ] Each PRD-F-# has clear description (2-3 sentences)
- [ ] Each PRD-F-# linked to BO-# in product-vision.md
- [ ] HMW statements documented (thinking traceability)
- [ ] Success criteria are specific (not boilerplate)
- [ ] MoSCoW prioritization makes sense (Must ~30%, Should ~50%, Could ~20%)
- [ ] In-Scope vs Out-of-Scope is disjunct
- [ ] Sequential PRD-F-# IDs without gaps
- [ ] Statistics calculated
