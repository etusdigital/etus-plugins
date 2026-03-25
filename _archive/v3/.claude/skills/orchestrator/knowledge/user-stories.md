---
doc_meta:
  id: stor
  display_name: User Stories
  pillar: Define
  owner_role: Product Lead
  summary: Authoritative Given/When/Then acceptance linked to PRD features and epics.
  order: 7
  gate: planning
  requires:
  - prd
  - epic
  optional: []
  feeds:
  - frd
  - be
  - fe
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
- Stories
- Gherkin
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# User Stories — [Product]

> **Only** place with Acceptance (Gherkin).  
> No NFR numbers here (SRS owns NFRs). No payload schemas here (Backend owns API).

---

## Story Index

| ID   | Title   | Epic | Priority | Points | Journey | Status |
| ---- | ------- | ---- | -------- | ------ | ------- | ------ |
| US-1 | [Title] | ep-1 | P0       | 5      | J1      | Draft  |
| US-2 | [Title] | ep-1 | P0       | 3      | J2      | Draft  |

---

### Story: [Title]

**ID:** US‑1 · **Epic:** ep‑1 · **Priority:** P0 · **Points:** [1–8]  
**JTBD:** per‑[id] · **Journey:** J#  
**UI Trace:** route: r:/… · view: view.…  
**Events:** ev.domain.action@v1

**As a** [job doer]  
**I want** [capability]  
**So that** [benefit]

**Preconditions:** [required state/data/permissions]  
**Postconditions:** [resulting state/data/logs]

**Acceptance (Gherkin):**

- **Happy:**  
  _Given_ […], _When_ […], _Then_ […]
- **Alternative:**  
  _Given_ […], _When_ […], _Then_ […]
- **Error:**  
  _Given_ […], _When_ […], _Then_ [error handling UX]

**Trace:**

- **FR:** FR‑1, FR‑3 _(Functional Reqs live in FRD)_
- **Backend refs:** be.domain.resource.post _(see Backend Requirements)_
- **Frontend refs:** cmp.table.data-grid _(see Frontend Requirements)_
- **Data refs:** ent./tbl. IDs; **events:** ev.… _(payload in Data Dictionary)_

**Definition of Done:**

- [ ] Telemetry (ev.\*) fired
- [ ] A11y (labels/focus/contrast) ok
- [ ] Error messages clear and actionable
- [ ] Docs updated

---

<!-- Repeat the structure above for US‑2, US‑3, … -->
