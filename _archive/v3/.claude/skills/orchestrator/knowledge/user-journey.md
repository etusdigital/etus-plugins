---
doc_meta:
  id: jour
  display_name: User Journey
  pillar: Design
  owner_role: UX Lead
  summary: Maps stages, pains, and opportunities across before/during/after experiences.
  order: 3
  gate: vision
  requires:
  - vis
  - per
  optional: []
  feeds:
  - brd
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
- Journey
- DoubleDiamond
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Discovery‑Driven User Journey — [Journey Name]

**Author:** [Your Name] · **Date:** [YYYY-MM-DD]

> Journey only: goals, pains, metrics per stage, happy/alt/error paths, and IDs.  
> **No** feature lists (PRD), **no** acceptance (User Stories), **no** schemas (Backend).

---

## Overview

- **Problem / JTBD:** see `product-vision.md`
- **Per‑stage metrics:** each J# includes a measurable target

## Stages (J1..Jn)

### J1 — [Stage Name]

- **Goal:** […]
- **Pain points:** […]
- **Metrics:** [e.g., TTV < 2 min p95]
- **Events (ev.\*):** [ev.stage.entry, ev.stage.exit]
- **Paths:**
  - **Happy:** […]
  - **Alternative:** […]
  - **Error:** […]

### J2 — [Stage Name]

- _(same structure)_

### J3 — [Stage Name]

- _(same structure)_

## Stage Evidence (optional)

| J#  | Evidence snippet / link | Severity | Note |
| --- | ----------------------- | -------- | ---- |
| J1  | […]                     | High     | […]  |
| J2  | […]                     | Medium   | […]  |

## Trace Table

| J#  | PRD-F-# | US-#       | route_id      | view_id             | events            |
| --- | ------- | ---------- | ------------- | ------------------- | ----------------- |
| J1  | PRD-F-1 | US-1, US-2 | r:/auth/login | view.auth.login     | ev.auth.login     |
| J2  | PRD-F-2 | US-3       | r:/dashboard  | view.dashboard.home | ev.dashboard.view |

## ✅ Journey Gate

- [ ] Each J# has metric + alt + error path
- [ ] J# references **PRD-F / US / route / view / ev.\*** by ID
- [ ] Evidence captured or linked where available
- [ ] No duplicated PRD/US/BE content
