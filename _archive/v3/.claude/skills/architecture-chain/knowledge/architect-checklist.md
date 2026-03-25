---
doc_meta:
  id: archcheck
  display_name: Architecture Checklist
  pillar: Build
  owner_role: Solution Architect
  summary: Ensures architecture decisions, risks, and review gates are complete before
    build.
  order: 10.1
  gate: technical
  requires: []
  optional: []
  feeds: []
uuid: <UUID>
version: 1.0.0
status: Checklist
owners:
- <architect>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- Checklist
- Architecture
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Architect Checklist

**Recommended path:** `docs/meta/checklists/architect-checklist.md`

---

## Inputs ready

- [ ] Vision/JTBD/Journey/BRD available
- [ ] PRD features (PRD‑F‑#) clear with non‑goals

## Quality attributes

- [ ] NFRs mapped to components (see SRS)
- [ ] Performance targets (UI/API/Data) feasible
- [ ] Availability & resilience patterns defined
- [ ] Security model (AuthN/AuthZ, secrets, PII) clear
- [ ] Observability plan (logs/metrics/traces) complete

## Data & Integrations

- [ ] Entities & relationships in ERD; DDL in SQL
- [ ] External integrations (auth, payments, etc.) planned
- [ ] Event namespacing (`ev.*`) consistent

## Delivery

- [ ] Deploy model & environments clear
- [ ] Runbooks & SLO dashboards planned
- [ ] Risks & ADRs documented
