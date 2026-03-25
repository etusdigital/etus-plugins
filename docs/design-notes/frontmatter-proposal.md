# Frontmatter Redesign Proposal — ETUS PMDocs v4.1

## Design Principles

### Execution Flow

The framework has three layers of invocation:

```
User → /command → Skill (inline) → Agent (fork) → Agent's Skills (inline within agent)
```

**Key insight:** Skills run inline within their parent context (either main conversation or agent). Agents are the fork boundary. So:

- Skills used by agents: `context` not needed (they run inline within the agent)
- Standalone validation utilities: `context: fork` + `agent: Explore` (read-only subagent)
- Orchestrator: inline (needs conversation to interact with user and spawn agents)

### Model Assignment Strategy

| Complexity | Model | Rationale |
|---|---|---|
| Strategic reasoning (discovery, planning, architecture) | `claude-opus-4` | Needs deep analysis, trade-offs, creative exploration |
| Execution/template-filling (data, ux, api, implementation) | `claude-sonnet-4` | Well-defined structure, follows patterns |
| Read-only validation (check-sst, check-traceability) | `claude-sonnet-4` + `context: fork` | Lightweight scanning, no interaction needed |
| Interactive gate validation | `claude-opus-4` | Judgment calls on GO/NO-GO/ITERATE |

### Invocation Control Matrix

| Scenario | `user-invocable` | `disable-model-invocation` |
|---|---|---|
| User AND Claude can trigger | `true` (default) | `false` (default) |
| User only (dangerous/heavyweight) | `true` | `true` |
| Claude only (internal utility) | `false` | `false` |
| Inaccessible (invalid) | `false` | `true` |

### Tool Restriction Strategy

- **Document generation:** `Read, Write, Edit, Glob, Grep` (standard set)
- **Read-only validation:** `Read, Grep, Glob` (no Write/Edit)
- **Orchestrator:** no restriction (needs Agent tool to spawn subagents)

---

## Proposed Frontmatter — All 25 Skills

### 1. ORCHESTRATOR

```yaml
---
name: orchestrator
description: >
  Orchestrate the complete product documentation workflow across 4 phases:
  Discovery, Planning, Design, and Implementation. Delegates to 7 specialized
  agents, manages 3 quality gates (GO/NO-GO/ITERATE), and ensures traceability
  across 21 documents. Use this skill whenever the user wants to run the full
  documentation pipeline, says "orchestrate", "full workflow", "start documentation",
  or needs to coordinate multiple documentation phases end-to-end.
model: claude-opus-4
version: 1.0.0
argument-hint: "[phase]"
---
```

**Rationale:**
- No `context: fork` — needs conversation history to interact with user at gates
- No `allowed-tools` restriction — needs Agent tool to spawn subagents
- No `disable-model-invocation` — should auto-trigger when user describes full workflow
- `argument-hint: [phase]` — user can jump to specific phase: `/orchestrator planning`

---

### 2. DISCOVERY — project-context

```yaml
---
name: project-context
description: >
  Generate project-context.md via structured 5W2H interview — captures project
  identity, tech stack, constraints, team composition, and business context.
  This is always the first document in any product documentation effort. Use
  whenever starting a new project, when the user says "new project", "project
  context", "5W2H interview", "what are we building", or when the discovery-agent
  begins its workflow.
model: claude-opus-4
version: 1.0.0
---
```

**Rationale:**
- No `argument-hint` — purely interactive (interview)
- No `compatibility` — this is the root document, no upstream dependencies
- Opus because the 5W2H interview requires deep probing and follow-up questions

---

### 3. DISCOVERY — product-vision

```yaml
---
name: product-vision
description: >
  Generate product-vision.md with problem statement, business objectives (BO-#),
  target users, value proposition, success metrics, and competitive landscape.
  Includes BMAD Creative Intelligence Suite brainstorm with user-selectable
  techniques (5 Whys, SCAMPER, Reverse Brainstorming, Six Thinking Hats, etc.).
  Use whenever the user wants to define product vision, business objectives,
  "what problem are we solving", target audience, or brainstorm product ideas.
model: claude-opus-4
version: 1.0.0
compatibility: "Upstream: project-context.md"
---
```

**Rationale:**
- Opus for strategic vision + creative brainstorm (BMAD CIS)
- `compatibility` documents the dependency chain for the model

---

### 4. PLANNING — prd

```yaml
---
name: prd
description: >
  Generate prd.md with prioritized features (PRD-F-#) using HMW (How Might We)
  and MoSCoW prioritization. Transforms product vision into actionable requirements
  with scope boundaries and MVP definition. Use whenever the user wants to create
  a PRD, define features, prioritize requirements, says "product requirements",
  "feature list", "what should we build first", or "MoSCoW".
model: claude-opus-4
version: 1.0.0
compatibility: "Upstream: product-vision.md"
---
```

---

### 5. PLANNING — user-stories

```yaml
---
name: user-stories
description: >
  Generate user-stories.md with user stories (US-#) and acceptance criteria in
  Given/When/Then format. Single Source of Truth for all Gherkin-style acceptance
  criteria — no other document may contain Given/When/Then blocks. Use whenever
  the user wants to write user stories, acceptance criteria, "as a user I want",
  behavioral specifications, or BDD scenarios.
model: claude-opus-4
version: 1.0.0
compatibility: "Upstream: prd.md"
---
```

---

### 6. PLANNING — feature-spec

```yaml
---
name: feature-spec
description: >
  Generate feature-spec-[name].md for complex features (>3 business rules or
  state machines). This is an on-demand document — only created when a feature
  exceeds the complexity threshold. Use whenever a feature has intricate business
  logic, multiple state transitions, complex validation rules, or when the user
  says "this feature needs a detailed spec" or "feature specification".
model: claude-opus-4
version: 1.0.0
argument-hint: "[feature-name]"
compatibility: "Upstream: user-stories.md"
---
```

**Rationale:**
- `argument-hint: [feature-name]` — user invokes `/feature-spec checkout` to spec a specific feature
- Opus because feature specs require deep analysis of business rules and state machines

---

### 7. ARCHITECTURE — architecture-diagram

```yaml
---
name: architecture-diagram
description: >
  Generate architecture-diagram.md with C4 model views (Context, Container,
  Component), technology stack decisions, and Mermaid diagrams. Defines the
  high-level system structure that all other design documents build upon. Use
  whenever the user wants system architecture, C4 diagrams, "how does the system
  fit together", technology choices, or infrastructure overview.
model: claude-opus-4
version: 1.0.0
compatibility: "Upstream: prd.md, user-stories.md"
---
```

---

### 8. ARCHITECTURE — tech-spec

```yaml
---
name: tech-spec
description: >
  Generate tech-spec.md with quantified NFRs (NFR-#), Architecture Decision
  Records (ADR-#), and technical design decisions. Single Source of Truth for
  all non-functional requirements and architecture decisions — no other document
  may define NFR-# targets or ADR-# records. Use whenever the user wants
  technical specifications, performance requirements, "what are the NFRs",
  architecture decisions, or scalability/security/reliability requirements.
model: claude-opus-4
version: 1.0.0
compatibility: "Upstream: architecture-diagram.md"
---
```

---

### 9-14. DATA-DESIGN (6 skills)

All data-design skills share this pattern:

```yaml
model: claude-sonnet-4
version: 1.0.0
```

#### 9. data-requirements

```yaml
---
name: data-requirements
description: >
  Generate data-requirements.md — entity inventory, data sources, integrity rules,
  and volume estimates. First document in the data design pipeline, establishing
  what data the system needs before modeling relationships. Use whenever starting
  data modeling, defining entities, "what data do we need", data sources, or
  when the data-agent begins its workflow.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: prd.md"
---
```

#### 10. erd

```yaml
---
name: erd
description: >
  Generate erd.md — Entity-Relationship Diagram in Mermaid with cardinalities,
  key attributes, and relationship descriptions. Translates data requirements
  into a visual data model. Use whenever the user wants an ER diagram, entity
  relationships, "how do entities relate", cardinality mapping, or data modeling.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: data-requirements.md"
---
```

#### 11. database-spec

```yaml
---
name: database-spec
description: >
  Generate database-spec.md with DDL statements, indexes, and migration strategy.
  Single Source of Truth for all CREATE TABLE statements — no other document may
  contain DDL. Use whenever the user wants database schema, table definitions,
  "create the tables", migration scripts, or index strategy.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: erd.md"
---
```

#### 12. data-dictionary

```yaml
---
name: data-dictionary
description: >
  Generate data-dictionary.md — field definitions (dict.*), event definitions
  (ev.*), and enumerated types. Single Source of Truth for all dict.* and ev.*
  identifiers — no other document may define field or event semantics. Use
  whenever the user wants a data dictionary, field definitions, event catalog,
  "what does this field mean", or domain terminology.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: erd.md, database-spec.md"
---
```

#### 13. data-flow-diagram

```yaml
---
name: data-flow-diagram
description: >
  Generate data-flow-diagram.md — data flows between components, processes, and
  storage in Mermaid. Shows how data moves through the system from input to output.
  Use whenever the user wants data flow diagrams, "how does data move", ETL flows,
  process-to-storage mappings, or integration data paths.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: architecture-diagram.md, database-spec.md"
---
```

#### 14. data-catalog

```yaml
---
name: data-catalog
description: >
  Generate data-catalog.md — inventory of all data assets with classification,
  ownership, lineage, and retention policies. Final document in data design
  pipeline, providing a searchable registry of all data assets. Use whenever the
  user wants a data catalog, asset inventory, data ownership, lineage tracking,
  or data governance documentation.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: data-dictionary.md, data-flow-diagram.md"
---
```

---

### 15-18. UX-DESIGN (4 skills)

All UX-design skills share:

```yaml
model: claude-sonnet-4
version: 1.0.0
```

#### 15. user-journey

```yaml
---
name: user-journey
description: >
  Generate user-journey.md — user journey maps with touchpoints, emotions,
  pain points, and opportunities. Maps each persona's path through the product
  from awareness to goal completion. Use whenever the user wants journey maps,
  user flows, "what's the user experience", touchpoint analysis, or emotional
  mapping of the product experience.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: product-vision.md, user-stories.md"
---
```

#### 16. ux-sitemap

```yaml
---
name: ux-sitemap
description: >
  Generate ux-sitemap.md — hierarchical page/screen map with navigation patterns
  and information architecture. Defines how users discover and access content
  across the product. Use whenever the user wants a sitemap, navigation structure,
  information architecture, "how are screens organized", or page hierarchy.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: user-journey.md"
---
```

#### 17. wireframes

```yaml
---
name: wireframes
description: >
  Generate wireframes.md — low-fidelity layouts in ASCII/Markdown with interaction
  annotations, responsive breakpoints, and accessibility notes. Use whenever
  the user wants wireframes, screen layouts, "what does this page look like",
  UI structure, or component placement planning.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: ux-sitemap.md"
---
```

#### 18. style-guide

```yaml
---
name: style-guide
description: >
  Generate style-guide.md — design tokens (tok.*), typography, color palette,
  spacing system, and component patterns. Single Source of Truth for all tok.*
  identifiers — no other document may define design tokens. Use whenever the
  user wants a style guide, design tokens, "what colors/fonts", brand guidelines,
  component library documentation, or visual design system.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: wireframes.md"
---
```

---

### 19. API-DESIGN — api-spec

```yaml
---
name: api-spec
description: >
  Generate api-spec.md — REST/GraphQL endpoints, request/response schemas,
  authentication, error handling, rate limiting, and versioning strategy. Single
  Source of Truth for all API schemas. Convergence point that references tech-spec
  (NFRs), database-spec (data shapes), and user-stories (behaviors). Use whenever
  the user wants API documentation, endpoint definitions, "what's the API contract",
  request/response schemas, or integration specifications.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: tech-spec.md, database-spec.md, user-stories.md"
---
```

---

### 20-22. IMPLEMENTATION (3 skills)

#### 20. implementation-plan

```yaml
---
name: implementation-plan
description: >
  Generate implementation-plan.md — task decomposition (impl-#), dependency
  graph, effort estimates (T-shirt sizing), sprint roadmap, and risk register.
  Translates design into an executable development plan. Use whenever the user
  wants an implementation plan, sprint planning, "how do we build this", task
  breakdown, or development roadmap.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: all design phase documents (17 docs)"
---
```

#### 21. sprint-status

```yaml
---
name: sprint-status
description: >
  Generate or update sprint-status.yaml — sprint structure with tasks (impl-#),
  assignments, progress tracking, and blockers. Updated iteratively each sprint.
  Use whenever the user wants to track sprint progress, update task status,
  "how is the sprint going", add blockers, or review sprint burndown.
model: claude-sonnet-4
version: 1.0.0
argument-hint: "[sprint-number]"
compatibility: "Upstream: implementation-plan.md"
---
```

#### 22. quality-checklist

```yaml
---
name: quality-checklist
description: >
  Generate quality-checklist.md — pre-release quality criteria covering test
  coverage, performance benchmarks, security review, accessibility, deployment
  readiness, and acceptance criteria verification. Use whenever the user wants
  a quality checklist, "are we ready to ship", release criteria, QA requirements,
  or pre-launch validation.
model: claude-sonnet-4
version: 1.0.0
compatibility: "Upstream: user-stories.md, implementation-plan.md"
---
```

---

### 23-25. VALIDATION (3 skills)

#### 23. check-sst

```yaml
---
name: check-sst
description: >
  Validate Single Source of Truth rules across all documents — detect duplicate
  definitions (Given/When/Then outside user-stories.md, NFR-# outside tech-spec.md,
  DDL outside database-spec.md, tok.* outside style-guide.md, dict.*/ev.* outside
  data-dictionary.md). Returns a violation report. Use whenever checking document
  consistency, during gate validation, or when the orchestrator runs quality checks.
user-invocable: false
context: fork
agent: Explore
model: claude-sonnet-4
version: 1.0.0
---
```

**Rationale:**
- `user-invocable: false` — internal utility, user accesses via `/validate sst` (which routes through validate-gate)
- `context: fork` + `agent: Explore` — runs as an isolated read-only subagent. Explore agent has Read, Grep, Glob but no Write/Edit. Perfect for scanning documents without risk of modification.
- Sonnet is sufficient for pattern matching across files

#### 24. check-traceability

```yaml
---
name: check-traceability
description: >
  Validate the traceability chain between IDs: BO-# → PRD-F-# → US-# → FS-# →
  impl-#. Detects orphan IDs (no upstream reference), broken links, and missing
  cross-references. Returns a violation report. Use whenever validating ID
  consistency, checking for orphan references, or during gate validation.
user-invocable: false
context: fork
agent: Explore
model: claude-sonnet-4
version: 1.0.0
---
```

**Rationale:** Same as check-sst — read-only scanner that returns a report.

#### 25. validate-gate

```yaml
---
name: validate-gate
description: >
  Execute interactive quality gate validation for any phase (Discovery, Planning,
  Design). Checks document completeness, runs SST and traceability validation,
  presents results to the user, and asks for a GO/NO-GO/ITERATE decision. Use
  whenever the user says "validate", "are we ready", "gate check", "review phase",
  or wants to approve moving to the next documentation phase.
model: claude-opus-4
version: 1.0.0
argument-hint: "[phase]"
---
```

**Rationale:**
- NOT forked — needs conversation context to present results and ask the user for a decision
- Opus because gate decisions require judgment (is the documentation complete enough?)
- `argument-hint: [phase]` — user invokes `/validate-gate discovery`

---

## Summary of Changes vs. Current State

| Change | Files Affected | Impact |
|---|---|---|
| Add YAML frontmatter | 4 UX skills | **Critical** — skills currently invisible |
| Rewrite descriptions (EN, pushy, trigger phrases) | 25 skills | **High** — improves auto-triggering accuracy |
| Add `model` field | 25 skills | **Medium** — ensures correct model per task |
| Add `version: 1.0.0` | 25 skills | **Low** — tracking/governance |
| Add `compatibility` | 22 skills | **Medium** — documents dependency chain |
| Add `argument-hint` | 5 skills | **Low** — improves UX for advanced users |
| Add `context: fork` + `agent: Explore` | 2 validation skills | **High** — enables parallel read-only validation |
| Set `user-invocable: false` | 2 validation skills | **Medium** — hides internal utilities from menu |
| Remove invented fields (`pillar`, `sequence`, `depends_on`, `feeds_to`) | 6 data-design skills | **Medium** — removes dead weight |
| Migrate all content PT-BR → EN | ~75 files | **High** — improves model performance + portability |
| Add `knowledge/` pointers in SKILL.md body | 17 skills | **High** — enables progressive disclosure |
| Add TOC to knowledge files >300 lines | 16 files | **Medium** — improves model navigation |

---

## Decision Points for Review

1. **`context: fork` for validation skills** — Do you agree that check-sst and check-traceability should run as isolated Explore subagents? This means they can't modify files (safe) and can run in parallel (fast), but they lose conversation context.

2. **`user-invocable: false` for check-sst/check-traceability** — These would only be accessible through validate-gate or agent invocation. The user uses `/validate sst` which goes through the validate command. OK?

3. **Model assignments** — Opus for discovery/planning/architecture/gates, Sonnet for data/ux/api/implementation/validation-scans. Does this match your expectations?

4. **`argument-hint` choices** — Only 5 skills have them (orchestrator, feature-spec, sprint-status, validate-gate + one implicit in commands). Should any others accept arguments?

5. **`compatibility` as upstream docs** — Using this field to document which docs must exist before running the skill. This is informational (not enforced), but helps the model decide if prerequisites are met.

6. **Full EN migration** — All SKILL.md bodies, knowledge files, agent prompts, commands, CLAUDE.md, ids.yml, and hook comments will be rewritten in English. The only Portuguese will be in user-facing examples (if the product being documented is in PT-BR).
