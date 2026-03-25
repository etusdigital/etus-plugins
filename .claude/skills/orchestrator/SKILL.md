---
name: orchestrator
description: >
  Use when running the full documentation pipeline, coordinating multiple phases,
  or managing the end-to-end workflow. Also triggers on 'orchestrate', 'full
  workflow', 'start documentation', 'run all phases', or 'coordinate the pipeline'.
model: opus
version: 1.0.0
argument-hint: "[phase]"
compatibility: "Optional: Slack MCP, Figma MCP, and external issue tracker adapters (for example, Linear) for context enrichment across phases"
---

# Orchestrator Skill

## MODE DETECTION

Before any workflow begins, the orchestrator determines the **work mode**. The mode controls which skills run, which dependencies apply, where output is saved, and whether quality gates are enforced.

### Detection Priority (first match wins)

**1. Explicit command (highest priority):**

| Command | Mode |
|---------|------|
| `/start-project` | Product |
| `/orchestrator` | Product |
| `/feature` | Feature |
| `/bugfix` | Bug |
| `/spike` | Spike |

**2. Trigger phrases in user message:**

| Phrases | Mode |
|---------|------|
| "fix bug", "hotfix", "fix this", "patch", "fix issue", "regression" | Bug |
| "new feature", "add feature", "feature request", "enhance" | Feature |
| "investigate", "research", "spike", "brainstorm", "POC", "proof of concept", "feasibility", "explore options" | Spike |
| "new product", "start project", "build platform", "full documentation" | Product |

**3. Context detection:**
- If `docs/ets/projects/{project-slug}/discovery/project-context.md` exists AND the user's message describes a specific, scoped change (a single feature, endpoint, screen, or workflow) → **Feature** mode.
- If `docs/ets/projects/{project-slug}/discovery/project-context.md` does NOT exist AND the user describes something broad (a product, platform, or system) → **Product** mode.

**4. Fallback — ask the user:**

If none of the above match, ask using `AskUserQuestion`:

> What type of work is this?
>
> 1. **Product** — New product or platform from scratch (full 4-phase pipeline, 26 docs)
> 2. **Feature** — New feature within an existing product (3-5 focused docs)
> 3. **Bug/Hotfix** — Bug fix with root cause analysis and test plan (1 doc)
> 4. **Spike/Research** — Investigation, brainstorm, or feasibility study (1 doc)

### Storing the Mode

After detection, write to `docs/ets/projects/{project-slug}/state/project-status.yaml`:

```json
{
  "mode": "product | feature | bug | spike",
  "workflow_version": "6.0",
  "detected_from": "command | trigger | context | user",
  "detected_at": "ISO-8601 timestamp",
  "trigger_detail": "the command or phrase that triggered detection"
}
```

All subsequent orchestrator decisions read `mode.json` to determine routing and
workflow compatibility. Legacy projects without `workflow_version` should be
treated as pre-solution-discovery until explicitly migrated.

---

## MODE-SPECIFIC BEHAVIOR

### Product Mode (full pipeline — existing behavior)

- **Skills activated:** Ideate + all product skills across Discovery, Opportunity Focus, Solution Discovery, Requirements, Design, and Implementation, including the specialist elicitation subskills (`jtbd-extractor`, `journey-sweep`, `use-case-matrix`, `edge-case-sweep`, `assumption-audit`)
- **Pipeline:** Ideate → Discovery → Opportunity Focus → Solution Discovery → Requirements → Design → Implementation
- **Dependencies:** Full BLOCKS/ENRICHES enforcement
- **Quality gates:** 3 mandatory gates (Discovery, Planning, Implementation Readiness)
- **Validation thresholds:** Standard (US-# ≥5, acceptance criteria ≥3 per story, coverage matrix required)
- **Output directory:** `docs/ets/projects/{project-slug}/` (standard subdirectories: discovery/, planning/, architecture/, data/, ux/, implementation/)
- **Traceability:** Full chain — BO-# → PRD-F-# → US-# → FS-# → impl-#
- **Agents:** All 7 agents activated

This is the existing workflow described in the sections below. No changes.

### Feature Mode (lightweight pipeline — 3-5 docs)

- **Skills activated:** ideate → solution-discovery → feature-brief → user-stories (scoped) → design-delta → impl-plan (scoped)
- **Pipeline:** Ideate → Solution Discovery → Feature Brief → User Stories → Design Delta → Implementation Plan
- **Dependencies relaxed:**
  - `project-context.md` → **ENRICHES** (read if exists, skip if not — no blocking)
  - `product-vision.md` → **ENRICHES** (read if exists, skip if not — no blocking)
  - No other upstream BLOCKS dependencies
- **Quality gates:** None mandatory. User can optionally run `/validate` at any point.
- **Validation thresholds (lowered):**
  - US-# ≥1 (not ≥5)
  - Acceptance criteria ≥1 per story (not ≥3)
  - `feature-status.md` required as the canonical state hub
  - Coverage matrix recommended because Feature mode now starts from ideation
  - No competitive landscape required
- **Output directory:** `docs/ets/projects/{project-slug}/features/{feature-slug}/`
  - `feature-status.md` — canonical state hub, tracking mode, next step, linked docs
  - `solution-discovery.md` — feature-scoped solution selection
  - `feature-brief.md` — Problem, scope, personas affected, acceptance criteria
  - `user-stories.md` — US-# with Given/When/Then (feature-scoped)
  - `design-delta.md` — Only what changes: new endpoints, DB migrations, UI changes
  - `impl-plan.md` — impl-# tasks, T-shirt sizing, sprint assignment
- **Agents:** planning-agent + 1 relevant design agent (architecture, data, ux, or api — based on feature scope)
- **Traceability:** SOL-# → FB-# → US-# → impl-# (simplified chain)
- **Auto-escalation:** If during Feature mode the scope grows beyond thresholds (>5 user stories OR >3 feature-specs needed OR user describes cross-cutting concerns affecting multiple subsystems), inform the user:
  > This feature's scope suggests it may benefit from the full Product mode pipeline. Product mode provides comprehensive architecture, data design, and UX coverage across all subsystems. Would you like to escalate to Product mode?

### Bug Mode (single document)

- **Skills activated:** ideate + tech-spec-standalone
- **Pipeline:** Ideate → Problem → Root Cause → Fix Plan → Test Plan → Rollback Plan (all in one document)
- **Dependencies:** None. Completely standalone. No upstream documents required.
- **Quality gates:** None.
- **Validation:** Problem described + fix approach present + test plan present
- **Output directory:** `docs/ets/projects/{project-slug}/bugs/`
  - Single document: `tech-spec-{slug}.md`
  - Contains: problem description, root cause analysis, affected components, fix approach, test plan, rollback plan
- **Agents:** None (orchestrator handles directly). For complex bugs affecting multiple subsystems, optionally spawn implementation-agent.
- **Traceability:** None required. Optionally links to existing US-# or PRD-F-# if the bug relates to a documented feature.

### Spike Mode (single document)

- **Skills activated:** ideate + spike
- **Pipeline:** Ideate → Question → Methodology → Research → Findings → Recommendation
- **Dependencies:** None. Completely standalone.
- **Quality gates:** None.
- **Validation:** Research question stated + findings documented + recommendation present
- **Output directory:** `docs/ets/projects/{project-slug}/spikes/`
  - Single document: `spike-{slug}.md`
  - Contains: research question, methodology, findings, options evaluated (with pros/cons), recommendation, decision (if made)
- **Agents:** Optionally discovery-agent for BMAD CIS brainstorm techniques
- **BMAD CIS techniques available:** All 8 brainstorm techniques can be used during spike research
- **Output feeds into:** Next work item. A spike can recommend creating a Feature, Product, or Bug work item.
- **Traceability:** None required. Spike document can be referenced as a source in future feature-brief or PRD documents.

### Mode Routing Summary

```
User request arrives
  │
  ├─ Mode = Product? ──→ Ideate → full 4-phase pipeline
  │
  ├─ Mode = Feature? ──→ Feature pipeline:
  │                       1. Generate opportunity-pack.md + coverage-matrix.yaml
  │                       2. Create or update feature-status.md
  │                       3. Generate solution-discovery.md
  │                       4. Generate feature-brief.md
  │                       5. Generate user-stories.md
  │                       6. Generate design-delta.md
  │                       7. Generate impl-plan.md
  │                       8. Save all to docs/ets/projects/{project-slug}/features/{feature-slug}/
  │
  ├─ Mode = Bug? ──────→ Bug pipeline:
  │                       1. Generate opportunity-pack.md + coverage-matrix.yaml
  │                       2. Interview: what broke, when, impact, reproduction steps
  │                       3. Generate tech-spec-{slug}.md
  │                       4. Save to docs/ets/projects/{project-slug}/bugs/
  │
  └─ Mode = Spike? ────→ Spike pipeline:
                          1. Generate opportunity-pack.md + coverage-matrix.yaml
                          2. Clarify research question
                          3. Select methodology (BMAD CIS techniques available)
                          4. Generate spike-{slug}.md
                          5. Save to docs/ets/projects/{project-slug}/spikes/
```

---

## Purpose

This skill is the **maestro** of the ETUS PMDocs framework. It orchestrates the complete 4-phase documentation workflow:

0. **Opening Layer: Ideate** (discovery/ideate) — Cover actors, JTBDs, journeys, use cases, edge cases, assumptions
1. **Phase 1: Discovery** (discovery-agent) — Understand the problem, vision, constraints
2. **Phase 2A: Opportunity Focus** (planning-agent) — Define which opportunities matter now
3. **Phase 2B: Solution Discovery** (planning-agent) — Reduce value/usability/viability/feasibility risk
4. **Phase 2C: Requirements** (planning-agent) — Define delivery-ready scope and stories
5. **Phase 3: Design** (4 agents in parallel) — Architecture, data design, UX design, API design
6. **Phase 4: Implementation** (implementation-agent) — Plan, schedule, quality checklist

Between phases, gates ensure document consistency and readiness to proceed: Ideation Readiness, Discovery Gate, Opportunity Focus Gate, Solution Readiness Gate, Requirements Gate, and Implementation Readiness.

The orchestrator:
- Detects current phase (from `state/reports/` metadata)
- Spawns appropriate agent(s) with complete context
- Validates phase completion
- Manages gate decisions
- Ensures traceability across 26 documents
- Handles parallel execution (Phase 3) correctly
- Logs decisions to `state/reports/` for audit trail

## Workflow Overview (Ideate → Discovery → Opportunities → Solution → Requirements → Design → Implementation)

```
IDEATE (Opus)
  ↓ Generate: opportunity-pack.md
  ↓ Generate: coverage-matrix.yaml
  ↓ IDEATION READINESS GATE: GO/ITERATE
  ↓
DISCOVERY (Opus)
  ↓ Derive from: opportunity-pack.md
  ↓ Generate: project-context.md
  ↓ Generate: baseline.md (dados & contexto — current state metrics)
  ↓ Generate: discovery-report.md (evidence synthesis, insights, hypotheses H-#)
  ↓ Generate: product-vision.md (vision + BO-# + BMAD brainstorm)
  ↓ Validate: check-sst, check-traceability (lightweight)
  ↓ DISCOVERY GATE: GO/ITERATE/NO-GO
  ↓
OPPORTUNITY FOCUS (Opus)
  ↓ Generate: ost.md (opportunity solution tree)
  ↓ Generate: prioritization.md (ICE/RICE scoring → P0/P1/P2)
  ↓ OPPORTUNITY FOCUS GATE: GO/ITERATE
  ↓
SOLUTION DISCOVERY (Opus)
  ↓ Generate: solution-discovery.md
  ↓ Generate: solution-report.json
  ↓ SOLUTION READINESS GATE: GO/ITERATE/NO-GO
  ↓
REQUIREMENTS (Opus)
  ↓ Generate: prd.md, user-stories.md, feature-spec-*.md
  ↓ Validate: check-sst, check-traceability (strict)
  ↓ REQUIREMENTS GATE: GO/DESCOPE/ITERATE
  ↓
DESIGN (Opus + Sonnet x3, PARALLEL)
  ├─ Architecture Agent (Opus) → architecture-diagram.md, tech-spec.md
  ├─ Data Agent (Sonnet) → database-spec.md, data-dictionary.md, data-flow-diagram.md, schema-migration.md
  ├─ UX Agent (Sonnet) → wireframes.md, interaction-design.md, accessibility-spec.md, design-system-guide.md
  └─ API Agent (Sonnet) → api-spec.md
  ↓ Generate: style-guide.md (if not already from UX agent)
  ↓ Validate: check-sst (strict), check-traceability
  ↓ IMPLEMENTATION READINESS GATE: GO/REDESIGN/ITERATE/NO-GO
  ↓
IMPLEMENTATION (Sonnet)
  ↓ Generate: implementation-plan.md, quality-checklist.md, release-plan.md
  ↓ Generate: release-plan.md (rollout strategy, rollback, monitoring — final doc)
  ↓ Link impl-# to FS-#, estimate work, assign to sprints
  ↓ Final validation: check-traceability (end-to-end)
  ↓ No gate; documentation core is complete and ready for execution in any system
```

## Phase Detection (from Memory + state/reports/ Metadata)

The orchestrator reads two sources to determine current state, in priority order:

**1. Memory (primary — always up to date):**
Read `docs/ets/.memory/project-state.md` first. This file is auto-generated by the
PostToolUse hook after every document save — it always reflects the true current state.

```
project-state.md fields used by orchestrator:
  Current phase: [discovery | planning | design | implementation | feature | bug | spike | not started]
  Current mode:  [product | feature | bug | spike | not set]
  Next Step:     [human-readable suggestion for what to run next]
```

**2. Handoff files (secondary — for agent context and gate decisions):**

```
state/reports/
├── mode.json               # {mode: "product|feature|bug|spike", workflow_version: "6.0", detected_from: …}
├── phase.json              # {phase: "discovery|…", status: "in_progress|completed"}
├── gate-log.md             # Decision log (audit trail)
├── discovery-report.json   # Output from discovery-agent
├── planning-report.json    # Output from planning-agent
├── design-report.json      # Output from design agents
└── implementation-report.json # Output from implementation-agent
```

**Phase Detection Logic (4-level fallback):**
1. Read `docs/ets/.memory/project-state.md` → `Current phase` and `Current mode` (most reliable)
2. Read `state/project-status.yaml` → determine mode and `workflow_version`
3. Read `state/workflow-state.yaml` → cross-check and get detailed status
4. Scan `docs/ets/projects/{project-slug}/` for existing documents → infer phase from what exists
5. Start with Discovery if nothing found

User can override: `--phase planning` to jump to Planning phase directly (for resuming work).

## Execution Loop

For each phase:

### 1. Load Context (4-Level Fallback)

- **From state/reports/** (if exists) — Previous phase outputs
- **From docs/ets/projects/{project-slug}/** (if exists) — Existing documents (partial or draft)
- **From user input** — User provides context/answers in interactive session
- **Ask user** — If no context found, ask guiding questions

### 2. Spawn Agent(s)

**Single-agent phases** (Discovery, Planning, Implementation):
```
Prompt = [System instructions] + [Phase-specific task] + [Context from step 1]
Agent = [discovery-agent | planning-agent | implementation-agent]
Model = Opus
Output = Report + Generated documents
```

**Multi-agent phase** (Design — Architecture + Data + UX + API in parallel):
```
1. Architecture Agent (sequential) → architecture-diagram.md, tech-spec.md
   (Other agents wait for tech-spec.md as dependency)

2. PARALLEL:
   - Data Agent → database-spec.md, data-dictionary.md, data-flow-diagram.md, schema-migration.md
   - UX Agent → wireframes.md, interaction-design.md, accessibility-spec.md, design-system-guide.md
   - API Agent → api-spec.md

3. Consolidate (Orchestrator) → Merge reports, write style-guide.md if needed

Each agent receives:
- Full system instructions (from .claude/agents/*.md)
- Phase task (from .claude/skills/[phase]/*)
- Context (from docs/ets/projects/{project-slug}/ and state/reports/)
- Expectation to write artifact to docs/ets/projects/{project-slug}/[path]
- Expectation to write report to stdout
```

### 3. Validate Phase Completion

Run validation checks:

1. **Document completeness** — All required docs present and % filled?
2. **check-sst** — No SST rule violations?
3. **check-traceability** — No orphan IDs, no broken links?
4. **Content quality** — Sections populated, no [TODO] markers?

### 4. Present Gate & Collect Decision

Call **validate-gate** skill:
- Displays gate checklist, validation results
- Shows recommendation (GO/ITERATE/DESCOPE/REDESIGN/NO-GO)
- Asks user for decision (interactive prompt)

### 5. Record Decision & Proceed

Update `state/reports/`:
```json
{
  "phase": "discovery",
  "workflow_version": "6.0",
  "status": "completed",
  "gate_decision": "GO",
  "gate_timestamp": "2026-03-14T10:30:00Z",
  "gate_notes": "Vision clear, constraints documented. Ready for Planning."
}
```

If decision == GO:
- Update `phase.json` to next phase, `status = "in_progress"`
- Proceed to next phase (loop back to step 1)

If decision == ITERATE:
- Keep current phase, `status = "in_progress"`
- Show feedback and ask: "Revise and re-validate? (y/n)"

If decision == NO-GO:
- Stop workflow, ask: "Kill project or reassess? (kill/reassess)"

## Parallel Execution (Phase 3: Design)

Design phase uses **parallel agent pattern** for efficiency:

1. **Architecture Agent runs first** (Opus, sequential)
   - Reads tech spec from product vision
   - Generates architecture-diagram.md, tech-spec.md
   - Reports back with NFRs and ADRs

2. **Other agents wait** (Data, UX, API)
   - Receive architecture-diagram.md and tech-spec.md as input
   - Begin in parallel

3. **Data Agent** (Sonnet) — Depends on tech-spec.md
   - Generates database-spec.md, data-dictionary.md, data-flow-diagram.md, schema-migration.md

4. **UX Agent** (Sonnet) — Independent of architecture
   - Generates wireframes.md, interaction-design.md, accessibility-spec.md, design-system-guide.md

5. **API Agent** (Sonnet) — Independent of architecture
   - Generates api-spec.md

6. **Consolidate** (Orchestrator)
   - Merge all reports into design-report.json
   - Check for conflicts (e.g., API schema vs. database schema)
   - Write unified style-guide.md (if data + UX agents didn't already)

7. **Adversarial Review** (Orchestrator)
   - Challenge assumptions in architecture decisions (ADR-#)
   - Identify missing failure modes in data flow and API paths
   - Question whether NFR targets are realistic given chosen architecture
   - Flag conflicts between parallel design streams (data vs UX vs API)
   - Generate Challenge Report with severity levels (Critical/Major/Minor)
   - Escalate Critical concerns to user; others can be tracked as impl-# tech debt

**Parallelism timing:**
- Architecture: 30-40 min (takes longest)
- Data + UX + API: 20-30 min each (concurrent)
- Adversarial Review: 10-15 min
- Total: ~50-65 min (vs. 90-120 min if sequential)

## Handoff Protocol (JSON)

Each phase leaves a `state/reports/` directory with:

```
state/workflow-state.yaml:
{
  "phase": "discovery" | "planning" | "design" | "implementation",
  "status": "in_progress" | "completed",
  "started_at": "2026-03-14T09:00:00Z",
  "completed_at": "2026-03-14T10:30:00Z",
  "gate_decision": "GO" | "ITERATE" | "NO-GO" | "DESCOPE" | "REDESIGN",
  "gate_notes": "User feedback / decision rationale"
}

state/reports/[phase]-report.json:
{
  "agent": "discovery-agent" | "planning-agent" | ... ,
  "documents_generated": ["project-context.md", "product-vision.md"],
  "validation_status": "passed" | "failed",
  "violations": [ {rule, file, line, remediation} ],
  "summary": "Completed discovery phase. Generated 2 documents. Vision is clear..."
}
```

## Knowledge Pointers

- **Agent specs**: `.claude/agents/*.md` — 7 agent definitions (discovery, planning, architecture, data, ux, api, implementation)
- **Skill specs**: `.claude/skills/*/SKILL.md` — 30 skills (26 doc generation + 3 validation + orchestrator)
- **Workflow guide**: `docs/ets/projects/{project-slug}/.guides/workflow.md` — Step-by-step guide for using orchestrator
- **Handoff schema**: `docs/ets/projects/{project-slug}/state/reports/schema.json` — JSON schema for phase.json, reports
- **ID scheme**: `docs/ets/projects/{project-slug}/ids.yml` — Centralized ID registry
- **Checklists**: `docs/ets/projects/{project-slug}/.guides/gate-checklists.md` — Gate validation checklists

## Integration with External MCPs (Optional)

The orchestrator can enrich context using external tools:

- **Slack MCP** — Post gate decisions, ask for stakeholder approval, notify team
- **Execution adapters** — Optional integration layer for execution systems outside the documentation core
- **Figma MCP** — Import existing wireframes or architecture diagrams as context

If these integrations are available, offer them as optional enrichments, never as a requirement of the ETUS core workflow.

## Common Scenarios

### Scenario 1: Start Fresh (New Project)

```
User: "Start documentation for our new analytics platform"
Orchestrator:
  1. Check state/reports/ — empty
  2. Assume Phase 1: Discovery
  3. Spawn discovery-agent with guiding questions
  4. Generate project-context.md, product-vision.md
  5. Run validate-gate (Discovery Gate)
  6. Ask: "Ready for Planning?" → if GO, move to Phase 2
```

### Scenario 2: Resume Phase (Partial Work)

```
User: "Continue from where we left off"
Orchestrator:
  1. Read state/workflow-state.yaml → "planning", "in_progress"
  2. Read state/reports/planning-report.json → "Generated prd.md, user-stories.md. FS-# incomplete."
  3. Ask user: "Resume Planning and complete FS-#?" → spawn planning-agent with feedback
  4. Regenerate feature-spec-*.md
  5. Re-run validate-gate → if issues, iterate
```

### Scenario 3: Jump to Phase (Overwrite)

```
User: "Jump to Design phase, I have all planning docs"
Orchestrator:
  1. Detect user override: --phase design
  2. Load all Planning docs (prd.md, user-stories.md, feature-spec-*.md)
  3. Spawn architecture-agent (and wait for tech-spec.md)
  4. Then spawn data-agent, ux-agent, api-agent in parallel
  5. Consolidate and validate
  6. Run Implementation Readiness Gate
```

## DEPENDENCY RESOLUTION PROTOCOL

All skills in this framework follow a unified dependency resolution protocol. The centralized dependency graph lives at `.claude/skills/orchestrator/dependency-graph.yaml`.

### Two-Tier Classification

**BLOCKS** (`requires` in dependency-graph.yaml):
- The skill REFUSES to run if the required document is missing or is marked DRAFT.
- The orchestrator auto-invokes the upstream skill to generate the missing document.
- Recursion depth limit: 5 hops. If exceeded → hard error.

**ENRICHES** (`enriched-by` in dependency-graph.yaml):
- The skill WARNS the user but proceeds without the enriching document.
- Output quality is lower but acceptable.
- No auto-invocation. No "continue anyway?" prompt — just warn and proceed.

### Auto-Invocation Protocol

When a skill starts and finds a BLOCKS dependency missing:

1. Read `dependency-graph.yaml` → find this skill's `requires` list
2. For each required document: check if file exists AND is non-empty AND is not marked `<!-- STATUS: DRAFT -->`
3. If missing or DRAFT:
   a. INFORM user: "⚠ [skill-name] requires [doc-name]. Generating it now."
   b. Invoke the upstream skill (which will recursively check ITS dependencies)
   c. Wait for completion
   d. Resume current skill with the newly generated document as input
4. If all BLOCKS deps satisfied → proceed normally
5. Check ENRICHES deps → warn if missing, proceed regardless

### DRAFT vs COMPLETE

- A document is COMPLETE when its `## OUTPUT VALIDATION` checklist passes (≥90% of checks).
- A document is DRAFT when validation fails. It carries `<!-- STATUS: DRAFT -->` at the top.
- A DRAFT document does NOT satisfy a BLOCKS dependency.
- A DRAFT document DOES satisfy an ENRICHES dependency (partial context is better than none).

### Handoff Dependency Status

Each phase handoff JSON includes document status:

```json
{
  "phase": "planning",
  "status": "complete",
  "documents": {
    "prd.md": { "status": "COMPLETE", "path": "docs/ets/projects/{project-slug}/planning/prd.md", "ids": ["PRD-F-1", "PRD-F-2", "PRD-F-3"] },
    "user-stories.md": { "status": "COMPLETE", "path": "docs/ets/projects/{project-slug}/planning/user-stories.md", "ids": ["US-1", "US-2", "US-3"] },
    "feature-spec-auth.md": { "status": "DRAFT", "path": "docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-auth.md", "ids": [] }
  },
  "unresolved_dependencies": [],
  "gate_result": "GO"
}
```

## ANTI-RATIONALIZATION RULES

When enforcing dependency checks, NEVER use these rationalizations to skip or weaken enforcement:

1. **"The user seems to know what they want"** → Dependencies still apply. The user's confidence doesn't replace documented context.
2. **"I can infer the context from conversation"** → Inferred context ≠ documented context. Conversation is ephemeral; documents persist and are consumed by downstream skills.
3. **"This is a simple/small project"** → All projects need upstream documents. Complexity is not an excuse to skip the pipeline.
4. **"The user said continue anyway"** → Only valid for ENRICHES dependencies. NEVER valid for BLOCKS dependencies. If the user insists on skipping a BLOCKS dep, explain why it matters and offer to auto-generate it instead.
5. **"I'll add the missing info later"** → Missing context produces cascading errors downstream. A PRD without BO-# traceability means user stories have no business justification.
6. **"The upstream doc exists but seems incomplete"** → Run INPUT VALIDATION. Don't assume — verify structural completeness (required sections, minimum IDs, minimum length).
7. **"I already have enough context from the chat"** → Chat context evaporates on session end. Documents are the durable contract between phases.
8. **"It's faster to just generate without the dependency"** → Speed without quality creates rework. The auto-invoke protocol adds ~2 minutes per missing dep — worth it.

## SOURCE DOCUMENTS REQUIREMENT

Every document generated by any skill in this framework MUST include a `## Source Documents` section immediately after the title. This section lists all upstream documents consumed during generation.

### Template

```markdown
## Source Documents

| Document | Path | Status | Key References |
|----------|------|--------|----------------|
| [name] | `docs/ets/projects/{project-slug}/[path]` | COMPLETE/DRAFT | [IDs or sections consumed] |
```

### Rules

- All BLOCKS dependencies MUST appear in Source Documents (they were required to run).
- ENRICHES dependencies appear only if they were actually read.
- If a BLOCKS dep was auto-generated during this skill's execution, note it: `Status: COMPLETE (auto-generated)`
- Key References should cite specific IDs (e.g., "BO-1..BO-5") or sections (e.g., "C4 Container View") consumed.

## Notes

- **Orchestrator is stateless** — All state lives in `state/reports/` (survives restart)
- **Modularity** — Each agent/skill can be invoked independently (not just via orchestrator)
- **Phases are sequential** — No phase skipping (unless user explicitly overrides)
- **Gates are mandatory** — Workflow doesn't proceed without gate decision
- **Audit trail** — Every decision logged in `state/reports/gate-log.md`

## Execution Steps

1. **Detect mode** — Run MODE DETECTION logic (command → trigger → context → fallback ask). Write `mode.json` with `workflow_version`.
2. **Route by mode:**
   - If mode = **Product** → continue to step 3 (full pipeline below)
   - If mode = **Feature** → execute Feature pipeline (see MODE-SPECIFIC BEHAVIOR) and stop
   - If mode = **Bug** → execute Bug pipeline (see MODE-SPECIFIC BEHAVIOR) and stop
   - If mode = **Spike** → execute Spike pipeline (see MODE-SPECIFIC BEHAVIOR) and stop
3. Detect current phase (from state/workflow-state.yaml or user input)
4. Load context (4-level fallback)
5. If phase is "design", spawn architecture-agent first, then parallel agents
6. Otherwise, spawn single agent
7. Collect agent reports
8. Run validation checks (check-sst, check-traceability)
9. **Adversarial review before Implementation Readiness Gate:** Before presenting the Implementation Readiness Gate (the gate between Phase 3 Design and Phase 4 Implementation), automatically run `validate-gate` with the `--adversarial` flag. This ensures design documents are rigorously challenged before committing to implementation. For all other gates (Discovery, Planning), proceed directly to standard validation.
10. Call validate-gate to present results and collect decision
11. Update state/reports/ with decision
12. Loop to next phase (if GO) or iterate (if ITERATE)
