---
doc_meta:
  id: prd
  display_name: Product Requirements Doc
  pillar: Define
  owner_role: Product Lead
  summary: Translates vision into scoped features with success criteria and boundaries.
  order: 5
  gate: planning
  requires:
  - vis
  - per
  - jour
  - brd
  optional: []
  feeds:
  - epic
  - stor
  - uxs
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

> **Owner:** “what” we will deliver.  
> **No** Gherkin here (User Stories own acceptance). **No** NFR numbers here (SRS owns NFRs).

---

## 0) Problem Context (summary)

Link to Vision (problem/NSM) and BRD (BO-#). Scope below defines boundaries for the product solution.

## 1) Goals & Success

- **Business Objectives (refs):** BO-1, BO-2
- **Product Goals:** [clear statements tied to BOs]
- **Global Success Criteria:** [e.g., +X% activation, −Y min TTV, +Z NPS]

## 2) Scope & Non-Goals

- **In-scope:** [behaviors the product will support]
- **Out-of-scope:** [explicitly excluded + rationale]
- **Constraints:** [legal/compliance, device/browser, data residency, time]

## 3) Feature Set (PRD-F-#) — one block per feature

### PRD-F-1 — [Feature Name]

- **Problem→Feature:** [problem ref/ID] → [feature] → [measurable outcome]
- **Success Criteria:** [what proves this feature worked]
- **Key User Scenarios (refs):** Journey J#, routes r:/…, views view.… _(no acceptance here)_
- **Dependencies:** [platform/data/service/FF]
- **Data Touchpoints (refs):** ent./tbl. IDs; events **ev.domain.action** to emit _(payload lives in Data Dictionary)_
- **Integrations (refs):** backend endpoints (be-ep-# IDs), external services
- **UX Guardrails:** [accessibility/i18n/consistency — rules, not pixels; tokens in Style Guide]
- **Risks & Mitigations:** [R-1 → mitigation]
- **Open Questions:** [Q-1, Q-2]
- **Assumptions:** [A-1, A-2] (link to Vision CSD)
- **Rollout & Flags:** [feature_flag, phased rollout, success/fail gates]
- **Trace/IDs:** PRD-F-# → ep-# → US-# → FR-# | route/view | ev.\* | ent./tbl. | be-ep-# | dict.\*
- **NFR Impact:** see **SRS NFR-#** (do not restate numbers here)

### PRD-F-2 — [Feature Name]

- **Problem→Feature:** [problem ref/ID] → [feature] → [measurable outcome]
- **Success Criteria:** [what proves this feature worked]
- **Key User Scenarios (refs):** Journey J#, routes r:/…, views view.… _(no acceptance here)_
- **Dependencies:** [platform/data/service/FF]
- **Data Touchpoints (refs):** ent./tbl. IDs; events **ev.domain.action** to emit _(payload lives in Data Dictionary)_
- **Integrations (refs):** backend endpoints (be-ep-# IDs), external services
- **UX Guardrails:** [accessibility/i18n/consistency — rules, not pixels; tokens in Style Guide]
- **Risks & Mitigations:** [R-1 → mitigation]
- **Open Questions:** [Q-1, Q-2]
- **Assumptions:** [A-1, A-2] (link to Vision CSD)
- **Rollout & Flags:** [feature_flag, phased rollout, success/fail gates]
- **Trace/IDs:** PRD-F-# → ep-# → US-# → FR-# | route/view | ev.\* | ent./tbl. | be-ep-# | dict.\*
- **NFR Impact:** see **SRS NFR-#** (do not restate numbers here)

## 4) Analytics & Telemetry Plan (refs)

- **Key events (IDs):** ev.domain.action _(payload & schema live in Data Dictionary)_
- **Dashboards/KPIs:** [where/how to read success]
- **Guardrails:** attribution, PII governance, sampling

## 5) Release & Rollout Plan

- **Milestones:** [Alpha → Beta → GA]
- **Entry/Exit Criteria:** [objective signals]
- **Feature Flags:** [flag names, owner, default]
- **Communication:** [who needs to know what, when]

## 6) Risks & Decisions

- **Risk Register:** [R-# → mitigation → owner]
- **Decision Log (IDs):** ADR-# (link to Tech Spec/Architecture if needed)

## 7) References

Vision, BRD, JTBD, Journey, Epics, User Stories, UXSM/Wireframes/UXDD, Backend Reqs, ERD/DB Schema, SRS, Data Dictionary, Tech Spec, Architecture Diagram.

## ✅ PRD Gate

- [ ] Clear success criteria per PRD-F-#
- [ ] Explicit non-goals & constraints
- [ ] Trace to Epics/US/route/view/event/data/backend by **ID** (PRD-F-# → ep-# → US-# → FR-#)
- [ ] Rollout & analytics plan defined
