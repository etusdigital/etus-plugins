---
doc_meta:
  id: wf-greenfield
  display_name: Greenfield Fullstack Plan
  pillar: Build
  owner_role: Engineering Lead
  summary: Guides end-to-end setup of a new fullstack project for solo developers.
  order: 0.8
  gate: meta
  requires: []
  optional: []
  feeds: []
uuid: <UUID>
version: 3.0.0
status: Guide
owners:
- <orchestrator>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- Workflow
- Process
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Workflow — Greenfield Fullstack

**Repository destination:** everything under `/docs` with phase subfolders.

---

## Phases → Outputs → Destination

| Phase          | Output (file)                      | Owner      | Destination                         |
| -------------- | ---------------------------------- | ---------- | ----------------------------------- |
| Discovery      | `project-context.md`               | Lead       | `docs/discovery/`                   |
| Discovery      | `product-vision.md`                | PM/Lead    | `docs/discovery/`                   |
| Planning       | `prd.md`                           | PM         | `docs/planning/`                    |
| Planning       | `user-stories.md`                  | PM         | `docs/planning/`                    |
| Planning       | `feature-spec-[name].md` (N files) | PM/Eng     | `docs/planning/feature-specs/`      |
| Design         | `architecture-diagram.md`          | Arch       | `docs/design/`                      |
| Design         | `tech-spec.md` (includes NFRs)     | Eng        | `docs/design/`                      |
| Design         | `data-requirements.md`             | Data       | `docs/design/`                      |
| Design         | `erd.md`                           | Data       | `docs/design/`                      |
| Design         | `database-spec.md`                 | Data       | `docs/design/`                      |
| Design         | `data-dictionary.md`               | Data       | `docs/design/`                      |
| Design         | `data-flow-diagram.md`             | Data       | `docs/design/`                      |
| Design         | `data-catalog.md`                  | Data       | `docs/design/`                      |
| Design         | `user-journey.md`                  | UX         | `docs/design/`                      |
| Design         | `ux-sitemap.md`                    | UX         | `docs/design/`                      |
| Design         | `wireframes.md`                    | UX         | `docs/design/`                      |
| Design         | `style-guide.md`                   | UX         | `docs/design/`                      |
| Implementation | `api-spec.md`                      | BE         | `docs/implementation/`              |
| Implementation | `implementation-plan.md`           | Tech Lead  | `docs/implementation/`              |
| Implementation | `sprint-status.yaml`               | Tech Lead  | `docs/implementation/`              |
| Implementation | `quality-checklist.md`             | Tech Lead  | `docs/implementation/`              |

**Total: 21 core documents** (+ N feature-spec files as needed)

---

## 3 Gates

| Gate                       | After Phase | Decision Options                      |
| -------------------------- | ----------- | ------------------------------------- |
| Discovery Gate             | Discovery   | GO / NO-GO / ITERATE                  |
| Planning Gate              | Planning    | GO / DESCOPE / ITERATE                |
| Implementation Readiness   | Design      | GO / REDESIGN / ITERATE / BLOCK       |

---

## Hand-offs (by ID)

project-context → Vision → BO-# → **PRD-F-#** → US-# → FS-[name]-# → **Tech Spec** (NFR-#) → Arch → API/Data/UX.

---

## Rules (No-Overlap / Single Source of Truth)

- Acceptance criteria (Given/When/Then): ONLY in **user-stories.md**
- NFR numeric targets (NFR-#): ONLY in **tech-spec.md**
- Design tokens (tok.*): ONLY in **style-guide.md**
- Field definitions (dict.*): ONLY in **data-dictionary.md**
- Event definitions (ev.*): ONLY in **data-dictionary.md**
- DDL statements: ONLY in **database-spec.md**

---

## Orchestration

- **PM/Lead** drives Discovery & Planning
- **Eng/Arch** drives Design & Implementation
- **Data/UX** execute parallel design workstreams
