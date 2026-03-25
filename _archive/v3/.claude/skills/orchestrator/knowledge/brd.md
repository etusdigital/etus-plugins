---
doc_meta:
  id: brd
  display_name: Business Requirements Doc
  pillar: Define
  owner_role: Product Lead
  summary: Summarizes business case, business objectives (BO-#), ROI justification, and success metrics.
  order: 4
  gate: vision
  requires:
  - vis
  optional:
  - per
  - jour
  feeds:
  - prd
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
- BRD
- Business
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Business Requirements Doc — [Tool Name]

**Author:** [Your Name] · **Date:** [YYYY-MM-DD]

> Business case & outcomes. No acceptance, no feature details (those live in PRD/US).

---

## 1) Strategic Rationale

- **Problem Fit:** [link to Vision/JTBD/Journey]
- **Why Now:** […]
- **Competitive/Benchmark signals:** […]

## 2) Business Objectives (BO‑#)

| BO‑# | Outcome (business)          | Baseline | Target | Timeline |
| ---- | --------------------------- | -------- | ------ | -------- |
| BO‑1 | [e.g., increase activation] | X        | Y      | [date]   |
| BO‑2 | […]                         | X        | Y      | [date]   |

## 3) Success Metrics (tracking plan at business level)

| KPI | Baseline | Target | Measurement Source |
| --- | -------- | ------ | ------------------ |
| …   | …        | …      | …                  |

## 4) Assumptions & Risks (business)

- **Assumptions** (link to Vision CSD): [A‑1, A‑2]
- **Risks + mitigation:** [R‑1 → mitigation] · Owner: [name]

## 5) ROI Hypothesis (lightweight)

- **Drivers:** [#users, conversion, ARPU, cost]
- **Formula:** [e.g., ΔRevenue = Users × Conv × ARPU − ΔCost]
- **Confidence:** Low/Medium/High

## 6) Scope (business)

- **In‑scope:** […]
- **Out‑of‑scope:** […]

## 7) Dependencies & Stakeholders

| Area  | Dependency | Impact if late | Owner |
| ----- | ---------- | -------------- | ----- |
| Data  | […]        | High           | […]   |
| Legal | […]        | Medium         | […]   |

## 8) Approvals (Go/No‑Go to Define)

| Role | Name | Decision | Date | Notes |
| ---- | ---- | -------- | ---- | ----- |
| PM   | […]  | Go       | …    | …     |
| Eng  | […]  | Go       | …    | …     |

## References

Vision, JTBD, Journey. Downstream: PRD.
