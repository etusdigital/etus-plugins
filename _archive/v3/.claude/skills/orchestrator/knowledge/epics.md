---
doc_meta:
  id: epic
  display_name: Epics
  pillar: Define
  owner_role: Product Lead
  summary: Groups PRD must-haves into epics with scope, success signals, and dependencies.
  order: 6
  gate: planning
  requires:
  - prd
  optional: []
  feeds:
  - stor
  - frd
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
- Epics
- Planning
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Epics — [Collection Name]

> Epics group value, sequencing, dependencies, and delivery milestones.  
> No discovery/journey content (those live in Vision/JTBD/Journey). No acceptance here.

---

## Epic: [Name] — ep-1

- **Goal & Business Value:** […]
- **Success Metric:** [e.g., +X% activation (BO‑#)]
- **Definition of Ready (DoR):** data ready, JTBD/Journey linked, risks known
- **Kill Criteria:** [objective stop conditions]
- **Dependencies:** [ep‑0], [platform], [data readiness]
- **Milestones:** [M1], [M2], [M3]
- **Capacity Assumptions:** [team size, velocity estimate]
- **Stories (P0):** US‑1, US‑2 _(acceptance lives in User Stories)_
- **Trace/IDs:** PRD‑F‑1; routes/views: r:/…, view.…; events: ev.…

## Epic: [Name] — ep-2

- _(same structure)_

## Cross‑Epic Dependencies (graph)

- ep‑1 → ep‑2 → ep‑3

## Roadmap & Critical Path

- **Order:** ep‑1 → ep‑2 → ep‑3
- **Risk notes:** [where slippage hurts most]

## ✅ Epic Gate

- [ ] DoR + Kill Criteria present
- [ ] Milestones & capacity reasonable
- [ ] Critical Path clear
- [ ] P0 stories listed and traced
