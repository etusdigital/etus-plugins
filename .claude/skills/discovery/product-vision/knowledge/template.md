---
doc_meta:
  id: vis
  display_name: Product Vision
  pillar: Discovery
  owner_role: Product Lead
  summary: Defines vision, business objectives, target users, value proposition, and success criteria.
  order: 1
  gate: discovery
  requires: [ctx]
  feeds: [prd, stor, arch, tech, data, ux, api]
---

# Product Vision

**Last Updated:** [DATE]
**Owner:** [PRODUCT_LEAD_NAME]
**Status:** [DRAFT | APPROVED]

---

## Vision Statement

### One-Line Vision
[Inspiring, concise vision. Example: "Enable solo freelancers to get paid faster by automating invoice follow-ups across all payment channels."]

### Vision Narrative (3-5 sentences)
[Expanded vision describing the desired future state and why it matters.]

---

## Problem Statement

### The Core Problem
[Reiterate from project-context.md with any refinements from vision interview.]

### Impact Quantified
[Data or estimates on revenue loss, time waste, user frustration, market opportunity.]

### Why Now?
[Market timing, technology readiness, competitive landscape shifts.]

---

## Business Objectives

Business Objectives (BO-#) are strategic aims that define success for the product. Each has measurable success criteria.

### BO-1: [Objective Name]
**Description:** [What we want to achieve and why it matters.]

**Success Criteria:**
- Metric 1: [Target value, timeline]
- Metric 2: [Target value, timeline]

**Related to:** [Which problem/user segment does this address?]

---

### BO-2: [Objective Name]
**Description:** [What we want to achieve and why it matters.]

**Success Criteria:**
- Metric 1: [Target value, timeline]
- Metric 2: [Target value, timeline]

**Related to:** [Which problem/user segment does this address?]

---

### BO-3: [Objective Name]
**Description:** [What we want to achieve and why it matters.]

**Success Criteria:**
- Metric 1: [Target value, timeline]
- Metric 2: [Target value, timeline]

**Related to:** [Which problem/user segment does this address?]

---

## Target Users & Personas

### Primary Persona
**Name:** [Persona name]
**Profile:** [Demographics, role, key characteristics]
**Current Pain:** [Their top 3 struggles with the current solution]
**Outcome Desired:** [What does success look like for them?]
**Influence on Decision:** [Decision maker, influencer, or user?]

---

### Secondary Persona
**Name:** [Persona name]
**Profile:** [Demographics, role, key characteristics]
**Current Pain:** [Their top 3 struggles]
**Outcome Desired:** [What does success look like?]
**Influence on Decision:** [Decision maker, influencer, or user?]

---

## Value Proposition

### What Value Do We Provide?
[Specific, measurable value. Example: "Save 5 hours/week on invoice tracking and follow-ups"]

### For Whom?
[Target audience segment with clarity. Example: "Freelancers billing $30K-$200K annually"]

### How Are We Different?
[Differentiation vs. alternatives. Why choose us?]

---

## Differentiation

### Competitive Landscape
| Competitor | Strengths | Weaknesses | Our Advantage |
|---|---|---|---|
| [Competitor A] | [What they do well] | [Where they fall short] | [Why we're better] |
| [Competitor B] | [What they do well] | [Where they fall short] | [Why we're better] |

### Our Unique Value
[1-2 sentences on what makes us different and defensible.]

---

## North Star Metric

**Metric:** [One overarching metric that captures product success]

**Definition:** [How is it calculated?]

**Target:** [What value do we want to reach and by when?]

**Why This Metric:** [Why does this matter most to the business?]

---

## How Might We (HMW) Questions

HMW questions transform problems into opportunity-focused framing. These guide feature ideation.

- **HMW-1:** [Transformed from Problem 1]
- **HMW-2:** [Transformed from Problem 2]
- **HMW-3:** [Transformed from Problem 3]

---

## Critical Assumptions

**To validate before investing heavily:**

1. **Assumption 1:** [e.g., "Users will adopt if invoice sync reduces manual entry by 80%"]
   - **Validation Method:** [How to test? e.g., user interviews, prototype test, survey]
   - **Timeline:** [When to validate?]

2. **Assumption 2:** [e.g., "Stripe API integration will support real-time webhooks without rate-limiting issues"]
   - **Validation Method:** [How to test?]
   - **Timeline:** [When to validate?]

3. **Assumption 3:** [e.g., "Freelancers will pay $29/month for automated invoice tracking"]
   - **Validation Method:** [How to test?]
   - **Timeline:** [When to validate?]

---

## Guardrails

Guardrails are metrics that must NOT degrade as a result of pursuing the business objectives. They act as safety boundaries for the product.

- **Guardrail 1:** [name] — limit: [[define]]
- **Guardrail 2:** [name] — limit: [[define]]
- **Guardrail 3:** [name] — limit: [[define]]

---

## Product Principles

Product principles are the "rules of the game" — 3-5 guiding principles that help the team make trade-off decisions consistently. When two options conflict, principles break the tie.

1. **[Principle Name]** — [e.g., "Security before speed" — we never ship a faster flow that weakens data protection.]
2. **[Principle Name]** — [e.g., "Simplicity over completeness" — we launch with fewer features done well rather than many features done poorly.]
3. **[Principle Name]** — [e.g., "Data-driven defaults" — every default value must be backed by evidence, not assumption.]
4. **[Principle Name]** — [optional, 4th principle]
5. **[Principle Name]** — [optional, 5th principle]

---

## Anti-Goals

Anti-goals are explicit trade-offs — things we will NOT do in this cycle, with clear reasoning. They prevent scope creep and align expectations.

- We will NOT [X] in this cycle because [reason].
- We will NOT [Y] until [condition is met].
- We will NOT [Z] because [trade-off rationale].

---

## Success Criteria

### Launch Criteria (MVP)
The product is ready for launch when:
- [ ] Criterion 1 (e.g., "Can sync invoices from 3+ payment gateways")
- [ ] Criterion 2 (e.g., "Page load time < 2 seconds")
- [ ] Criterion 3 (e.g., "NPS validation with 10 beta users > 40")

### 90-Day Goals (Post-Launch)
**User Growth:** [Target: X active users]
**Engagement:** [Target: Y% weekly active, Z average session duration]
**Satisfaction:** [Target: NPS > W, Retention rate > V%]
**Business:** [Target: MRR $X, CAC < $Y]

---

## Risks & Mitigations

### Risk 1: [Risk name]
**Scenario:** [What could go wrong?]
**Impact:** [Consequence if it happens]
**Probability:** [High / Medium / Low]
**Mitigation:** [How to prevent or prepare]

### Risk 2: [Risk name]
**Scenario:** [What could go wrong?]
**Impact:** [Consequence if it happens]
**Probability:** [High / Medium / Low]
**Mitigation:** [How to prevent or prepare]

---

## Brainstorm Insights

[Optional section to capture learnings from brainstorming techniques run during vision workshop]

### Technique 1: [Technique Name]
**Key Insights:**
- Insight 1
- Insight 2

### Technique 2: [Technique Name]
**Key Insights:**
- Insight 1
- Insight 2

---

## Document Metadata

**Document ID:** vis
**Version:** 1.0
**Last Reviewed:** [DATE]
**Next Review:** [DATE]
**Approval Chain:** [Who approved this?]

---

## Related Documents

- Requires: [project-context.md](../project-context.md)
- Feeds into: [prd.md](../../planning/prd.md), [user-stories.md](../../planning/user-stories.md)
- Referenced by: [architecture-diagram.md](../../design/architecture-diagram.md), [tech-spec.md](../../design/tech-spec.md)

---

## Discovery Gate: Ready for Planning?

**Gate Review Criteria:**
- [ ] Vision is clear and inspiring?
- [ ] Business objectives (BO-#) are measurable?
- [ ] Target users are well-defined?
- [ ] Value proposition is compelling?
- [ ] Critical assumptions documented?
- [ ] Success criteria (launch + 90-day) realistic?
- [ ] Risks identified with mitigations?

**Gate Status:** ⬜ Pending Review

**Reviewer:** [Name]
**Review Date:** [DATE]
**Decision:** [ ] GO → Planning | [ ] NO-GO | [ ] ITERATE
**Notes:** [Any refinements needed?]
