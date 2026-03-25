---
description: Define architecture, data model, UX, and API specification in sequential and parallel stages.
---

# Design Phase

Define architecture, data model, UX, and API specification. Runs in two stages:
architecture first (sequential), then data + UX + API in parallel.

## Context Loading

1. If $ARGUMENTS provided -> use as design context/constraints
2. Read docs/ets/projects/{project-slug}/state/reports/planning.json for upstream context
3. If no handoff, scan docs/ets/projects/{project-slug}/planning/ for existing docs
4. If nothing found -> tell user to run /plan first

## Execution — Stage 1: Architecture (Sequential)

Spawn the **architecture-agent** with:

---

You are the Architecture Agent.

**Upstream:** planning handoff + prd.md + user-stories.md
**Output directory:** docs/ets/projects/{project-slug}/architecture/

1. Read the prd and user stories from docs/ets/projects/{project-slug}/planning/
2. Read the architecture-diagram skill and generate architecture-diagram.md
   - C4 model: Context, Container, Component diagrams (Mermaid)
   - Technology choices with rationale
3. Read the tech-spec skill and generate tech-spec.md
   - NFR-# with quantified targets (latency, throughput, uptime)
   - ADR-# architecture decisions with context, decision, consequences
4. Write docs/ets/projects/{project-slug}/state/reports/design-architecture.json

---

## Execution — Stage 2: Parallel Agents

After architecture completes, read design-architecture.json, then spawn THREE
agents simultaneously:

### Data Agent
---
You are the Data Agent.
**Upstream:** architecture + planning handoff
**Output directory:** docs/ets/projects/{project-slug}/data/
Generate 6 documents in sequence: data-requirements -> erd -> database-spec ->
data-dictionary -> data-flow-diagram -> data-catalog.
Each document feeds the next. Follow the skill for each document.
Write docs/ets/projects/{project-slug}/state/reports/design-data.json
---

### UX Agent
---
You are the UX Agent.
**Upstream:** product-vision + user-stories + architecture
**Output directory:** docs/ets/projects/{project-slug}/ux/
Generate 4 documents in sequence: user-journey -> ux-sitemap -> wireframes -> style-guide.
Each document feeds the next. Follow the skill for each document.
Write docs/ets/projects/{project-slug}/state/reports/design-ux.json
---

### API Agent
---
You are the API Agent.
**Upstream:** tech-spec + database-spec + user-stories
**Output directory:** docs/ets/projects/{project-slug}/api/
Generate api-spec.md following the api-spec skill.
Write docs/ets/projects/{project-slug}/state/reports/design-api.json
---

## Execution — Stage 3: Merge & Cross-Validate

After all 4 agents complete:
1. Merge handoffs into docs/ets/projects/{project-slug}/state/reports/design.json
2. Cross-validate:
   - Data schemas match API request/response schemas?
   - Wireframe components reference tok.* tokens from style-guide?
   - API endpoints cover all user stories?
   - Database entities match ERD?
3. Report any conflicts to user

$ARGUMENTS

## After Design

Present Implementation Readiness Gate checklist:
- [ ] Architecture addresses all NFRs?
- [ ] Data model covers all entities from user stories?
- [ ] All wireframes reference style-guide tokens?
- [ ] API spec covers all user-facing operations?
- [ ] No cross-validation conflicts?

Ask user: **GO** (proceed to Implementation), **REDESIGN** (rework specific area), or **ITERATE** (refine design)?
