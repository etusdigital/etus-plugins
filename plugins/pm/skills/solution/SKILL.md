---
name: solution
description: >
  Use when exploring candidate solutions after opportunities are selected and before
  writing delivery requirements. Also triggers on 'solution discovery', 'prototype',
  'concept test', 'value risk', 'usability risk', 'viability risk', or
  'feasibility risk'.
model: opus
version: 1.0.0
argument-hint: "[opportunity path or context]"
compatibility: "Optional: Figma MCP, Slack MCP, and external issue tracker adapters (for example, Linear)"
---

# Solution Discovery

## PURPOSE

Reduce product risk before delivery definition.

This skill sits between:
- opportunity selection (`ost.md`, `prioritization.md`)
- delivery definition (`prd.md`, `feature-brief`, `user-stories.md`)

Its job is to ensure the team does not convert an attractive opportunity directly
into implementation scope without first testing solution quality.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/planning/ost.md`
- `docs/ets/projects/{project-slug}/planning/prioritization.md`
- `docs/ets/projects/{project-slug}/discovery/product-vision.md`

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
- `docs/ets/projects/{project-slug}/discovery/baseline.md`
- `docs/ets/projects/{project-slug}/discovery/discovery-report.md`
- `docs/ets/projects/{project-slug}/discovery/project-context.md`
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml`

## ARTIFACT SAVE RULE

This skill MUST write:
1. `docs/ets/projects/{project-slug}/planning/solution-discovery.md`
2. `docs/ets/projects/{project-slug}/state/reports/solution-report.json`

It SHOULD write when experiments are defined:
3. `docs/ets/projects/{project-slug}/planning/solution-experiments.yaml`

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard, but it is explicitly a
**solution discovery** step, not a requirements step.

1. Ask one question per message
2. Compare 2-4 solution directions, not just one
3. Keep the conversation centered on risk reduction, not implementation detail
4. Present one solution option at a time, with tradeoffs
5. End with a recommendation plus unresolved risks

## FOUR RISKS

Every candidate solution must be evaluated against:
- **Value** — will users/customers actually want this?
- **Usability** — can they understand and use it?
- **Viability** — does it work for the business?
- **Feasibility** — can the team build and operate it?

## CONTEXT LOADING

Load context in this order:
1. `ost.md`
2. `prioritization.md`
3. `product-vision.md`
4. `opportunity-pack.md`
5. `baseline.md`
6. `discovery-report.md`
7. `coverage-matrix.yaml`
8. `$ARGUMENTS` as additional opportunity or concept context

## WORKFLOW

### 1. Select the opportunity focus
- Confirm which `O-#` items are in scope now
- Confirm which `O-#` item is the P0

### 2. Generate candidate solutions
- Create 2-4 `SOL-#` options
- Keep them high-level enough for comparison
- Do not write requirements or stories yet

### 3. Score the four risks
For each `SOL-#`, document:
- value risk
- usability risk
- viability risk
- feasibility risk

### 4. Define experiments and prototypes
When uncertainty exists, define `EXP-#` items with:
- hypothesis
- method
- success criteria
- owner
- duration

### 5. Recommend a direction
- Select one preferred solution direction
- List what was rejected and why
- List unresolved risks and blockers

## OUTPUT FORMAT

### solution-discovery.md

Must contain:
- selected outcome and `O-#` focus
- 2-4 `SOL-#` options
- four-risk matrix
- experiments/prototypes
- recommended solution
- unresolved risks
- conditions to proceed to requirements

### solution-experiments.yaml

Optional but recommended when any `EXP-#` exists.

## GATE

Before completion, validate:
- [ ] At least 2 `SOL-#` options were considered unless scope is trivially narrow
- [ ] The four risks were evaluated for each chosen direction
- [ ] A recommendation exists
- [ ] Unresolved risks are explicit
- [ ] Experiments are defined when confidence is not high

If any check fails, mark the artifact as DRAFT and do not recommend requirements.
