# ETUS PMDocs v4.1 — Final Design Proposal

## Output Directory Structure

All generated artifacts go into `docs/ets-docs/` with clear subdirectories:

```
project-root/
├── .claude/                     # Framework (skills, agents, commands, hooks)
├── ids.yml                      # ID registry (project root)
└── docs/
    └── ets-docs/
        ├── .handoff/            # Phase handoff JSON files (machine-readable)
        │   ├── discovery.json
        │   ├── planning.json
        │   ├── design-architecture.json
        │   ├── design-data.json
        │   ├── design-ux.json
        │   ├── design-api.json
        │   ├── design.json      # Merged from the 4 above
        │   └── implementation.json
        │
        ├── discovery/
        │   ├── project-context.md
        │   └── product-vision.md
        │
        ├── planning/
        │   ├── prd.md
        │   ├── user-stories.md
        │   └── feature-specs/
        │       ├── feature-spec-checkout.md
        │       └── feature-spec-authentication.md
        │
        ├── architecture/
        │   ├── architecture-diagram.md
        │   └── tech-spec.md
        │
        ├── data/
        │   ├── data-requirements.md
        │   ├── erd.md
        │   ├── database-spec.md
        │   ├── data-dictionary.md
        │   ├── data-flow-diagram.md
        │   └── data-catalog.md
        │
        ├── ux/
        │   ├── user-journey.md
        │   ├── ux-sitemap.md
        │   ├── wireframes.md
        │   └── style-guide.md
        │
        └── implementation/
            ├── api-spec.md
            ├── implementation-plan.md
            ├── sprint-status.yaml
            └── quality-checklist.md
```

**Why this structure:**
- `docs/ets-docs/` namespaces all PMDocs output — won't conflict with other project docs
- `.handoff/` hidden with dot prefix — machine files, not for human browsing
- Subdirectories match the 4 phases + 2 design sub-tracks (data, ux)
- `api-spec.md` lives in `implementation/` because it's the convergence point between design and implementation

---

## Commands as Agent Prompts

### The Insight

Commands ARE pre-formatted prompts. Instead of storing prompt templates in
`knowledge/prompts/`, the commands themselves serve double duty:

1. **User invokes directly:** `/discover` → Claude follows command instructions
2. **Orchestrator reads command file:** uses it as Agent tool prompt template

This eliminates duplication and creates a single source of truth for each phase's execution logic.

### Command Architecture

```
.claude/commands/
├── start-project.md     # Init structure + start orchestrator
├── discover.md          # Phase 1: spawn discovery-agent with full context
├── plan.md              # Phase 2: spawn planning-agent with upstream context
├── design.md            # Phase 3: sequential arch + parallel data/ux/api
├── implement.md         # Phase 4: spawn implementation-agent
├── validate.md          # Gate validation (interactive)
└── orchestrator.md      # Full workflow: chains all commands
```

### How the Orchestrator Chains Commands

```markdown
# orchestrator.md (simplified)

## Workflow

### Phase 1: Discovery
Read the file at `${CLAUDE_SKILL_DIR}/../commands/discover.md`.
Use its content as the prompt for spawning the discovery-agent via Agent tool.
Pass any user context as arguments.

When the agent returns:
1. Verify docs/ets-docs/.handoff/discovery.json was written
2. Present Discovery Gate to user (read checklists from knowledge/)
3. Wait for GO/NO-GO/ITERATE decision

### Phase 2: Planning (only if Discovery Gate = GO)
Read the file at `${CLAUDE_SKILL_DIR}/../commands/plan.md`.
Read docs/ets-docs/.handoff/discovery.json for upstream context.
Construct agent prompt: command content + handoff context.
Spawn planning-agent.
...
```

### Command Template Pattern

Each command follows this structure:

```markdown
# [Phase Name]

## Context Loading
1. If $ARGUMENTS provided → use as upstream context
2. If docs/ets-docs/.handoff/{previous-phase}.json exists → read it
3. If upstream documents exist in docs/ets-docs/ → scan and use
4. If nothing found → ask user for context

## Agent Spawn
Spawn the {agent-name} with the following task:

### Upstream Context
- Documents: [list from handoff or scan]
- IDs generated so far: [from handoff or ids.yml]
- Key decisions: [from handoff]
- Gate result: [from handoff]

### Instructions
1. Read skill instructions: [list of skills]
2. Execute workflow: [steps]
3. Save outputs to: docs/ets-docs/{subdirectory}/
4. Write handoff: docs/ets-docs/.handoff/{phase}.json

### Handoff Report Schema
{JSON schema for this phase's handoff}

$ARGUMENTS
```

---

## Revised Command Designs

### discover.md

```markdown
# Discovery Phase

Conduct product discovery using 5W2H structured interview and BMAD Creative
Intelligence Suite brainstorm techniques.

## Context Loading

If $ARGUMENTS is provided, use it as the product description to jumpstart discovery.
Otherwise, begin by asking the user what product they want to document.

Check if docs/ets-docs/discovery/ already has documents:
- If yes: ask user whether to refine existing or start fresh
- If no: proceed with new discovery

## Execution

Spawn the **discovery-agent** with these instructions:

---

You are the Discovery Agent. Your job is to generate two foundational documents
through interactive interviews with the user.

**Output directory:** docs/ets-docs/discovery/

**Step 1: Project Context (5W2H Interview)**
Read the project-context skill. Conduct a structured interview:
- What: What is this product? What problem does it solve?
- Who: Who are the users? Who are the stakeholders?
- Where: What platforms/markets?
- When: Timeline and milestones?
- Why: Why build this? What's the business case?
- How: How will it work at a high level?
- How Much: Budget, team size, constraints?

Save to: `docs/ets-docs/discovery/project-context.md`

**Step 2: Product Vision (BMAD Brainstorm)**
Read the product-vision skill. Using the 5W2H context:
1. Define problem statement and business objectives (BO-1, BO-2, ...)
2. Propose 3-4 BMAD brainstorm techniques to the user
3. User selects which to run
4. Execute selected technique → generate insight artifact
5. Offer another technique or move on
6. Define target users, value proposition, success metrics

Save to: `docs/ets-docs/discovery/product-vision.md`

**Step 3: Handoff Report (MANDATORY)**
Write `docs/ets-docs/.handoff/discovery.json`:
```json
{
  "phase": "discovery",
  "status": "complete",
  "iteration": 1,
  "documents": [
    {"path": "docs/ets-docs/discovery/project-context.md", "ids": []},
    {"path": "docs/ets-docs/discovery/product-vision.md", "ids": ["BO-1", "..."]}
  ],
  "id_state": {"bo": N},
  "key_decisions": ["...top 3-5 decisions..."],
  "recommendations_for_next_phase": ["...what planning should focus on..."]
}
```

Update `ids.yml` sequences.bo with the last BO number used.

---

User context: $ARGUMENTS

## After Discovery

When the agent completes, present the Discovery Gate checklist:
- [ ] 5W2H interview complete?
- [ ] Problem clearly defined and validated?
- [ ] Business opportunity quantified?
- [ ] At least 1 BO-# defined?
- [ ] Vision statement clear?

Ask user: **GO** (proceed to Planning), **ITERATE** (refine discovery), or **NO-GO** (stop)?
```

### plan.md

```markdown
# Planning Phase

Transform product vision into prioritized requirements using HMW (How Might We)
and MoSCoW prioritization.

## Context Loading

1. If $ARGUMENTS provided → use as additional planning context
2. Read docs/ets-docs/.handoff/discovery.json for upstream context
3. If no handoff, check if docs/ets-docs/discovery/product-vision.md exists
4. If nothing found → tell user to run /discover first

## Execution

Spawn the **planning-agent** with these instructions:

---

You are the Planning Agent.

**Upstream Context:**
- Discovery handoff: [inject from discovery.json]
- Documents: docs/ets-docs/discovery/project-context.md, docs/ets-docs/discovery/product-vision.md
- Business Objectives: [BO-1 through BO-N from handoff]
- Key decisions: [from handoff]

**Output directory:** docs/ets-docs/planning/

**Step 1: PRD (Product Requirements Document)**
Read the prd skill. Using the product vision:
1. Brainstorm all possible features (diverge)
2. Apply HMW: transform problems from vision into "How might we..." opportunities
3. Apply MoSCoW: prioritize features as Must/Should/Could/Won't
4. Each PRD-F-# MUST reference which BO-# it serves
5. Define MVP scope (Must-haves only)

Save to: `docs/ets-docs/planning/prd.md`

**Step 2: User Stories**
Read the user-stories skill. For each PRD-F-#:
1. Write user stories (US-#) with "As a [persona], I want [action], so that [benefit]"
2. Each US-# MUST reference which PRD-F-# it implements
3. Write acceptance criteria in Given/When/Then format
4. This is the ONLY document that may contain Given/When/Then (SST rule)

Save to: `docs/ets-docs/planning/user-stories.md`

**Step 3: Feature Specs (on-demand)**
Read the feature-spec skill. For each feature with >3 business rules or a state machine:
1. Create feature-spec-[kebab-name].md
2. Each FS-[name]-# MUST reference which US-# it details
3. Document business rules, state transitions, validation logic

Save to: `docs/ets-docs/planning/feature-specs/feature-spec-[name].md`

**Step 4: Handoff Report (MANDATORY)**
Write `docs/ets-docs/.handoff/planning.json` with all document paths, IDs generated
(PRD-F-#, US-#, FS-# if any), MoSCoW summary, and recommendations for design.

Update `ids.yml` with prd-f, us sequences.

---

User context: $ARGUMENTS

## After Planning

Present Planning Gate checklist and ask: **GO**, **DESCOPE**, or **ITERATE**?
```

### design.md

```markdown
# Design Phase

Define architecture, data model, UX, and API specification. Runs in two stages:
architecture first (sequential), then data + UX + API in parallel.

## Context Loading

1. If $ARGUMENTS provided → use as design context/constraints
2. Read docs/ets-docs/.handoff/planning.json for upstream context
3. If no handoff, scan docs/ets-docs/planning/ for existing docs
4. If nothing found → tell user to run /plan first

## Execution — Stage 1: Architecture (Sequential)

Spawn the **architecture-agent** with:

---

You are the Architecture Agent.

**Upstream:** planning handoff + prd.md + user-stories.md
**Output directory:** docs/ets-docs/architecture/

1. Generate architecture-diagram.md (C4 model: Context, Container, Component)
2. Generate tech-spec.md (NFR-# quantified, ADR-# decisions)
3. Write docs/ets-docs/.handoff/design-architecture.json

---

## Execution — Stage 2: Parallel Agents

After architecture completes, read design-architecture.json, then spawn THREE
agents simultaneously:

### Data Agent
---
You are the Data Agent.
**Upstream:** architecture + planning handoff
**Output directory:** docs/ets-docs/data/
Generate 6 documents in sequence: data-requirements → erd → database-spec →
data-dictionary → data-flow-diagram → data-catalog
Write docs/ets-docs/.handoff/design-data.json
---

### UX Agent
---
You are the UX Agent.
**Upstream:** product-vision + user-stories + architecture
**Output directory:** docs/ets-docs/ux/
Generate 4 documents: user-journey → ux-sitemap → wireframes → style-guide
Write docs/ets-docs/.handoff/design-ux.json
---

### API Agent
---
You are the API Agent.
**Upstream:** tech-spec + database-spec + user-stories
**Output directory:** docs/ets-docs/implementation/
Generate api-spec.md
Write docs/ets-docs/.handoff/design-api.json
---

## Execution — Stage 3: Merge & Cross-Validate

After all 4 agents complete:
1. Merge handoffs into docs/ets-docs/.handoff/design.json
2. Cross-validate: data schemas ↔ API schemas, wireframes ↔ tok.* tokens
3. Report any conflicts to user

$ARGUMENTS

## After Design

Present Implementation Readiness Gate and ask: **GO**, **REDESIGN**, or **ITERATE**?
```

### implement.md

```markdown
# Implementation Phase

Create execution plan, sprint structure, and quality criteria.

## Context Loading

1. If $ARGUMENTS provided → use as implementation constraints
2. Read docs/ets-docs/.handoff/design.json for full context
3. If no handoff, scan docs/ets-docs/ for all existing documents
4. If insufficient docs → tell user to run /design first

## Execution

Spawn the **implementation-agent** with:

---

You are the Implementation Agent.

**Upstream:** all 17 documents from discovery + planning + design phases
**Output directory:** docs/ets-docs/implementation/

1. Read ALL upstream documents (paths from design.json handoff)
2. Generate implementation-plan.md:
   - Decompose user stories into tasks (impl-#)
   - Map dependencies between tasks
   - Estimate effort (T-shirt sizing)
   - Plan sprints (1-2 week cycles)
   - Identify risks and mitigations
3. Generate sprint-status.yaml:
   - Sprint structure with tasks assigned to sprints
   - Each task references impl-# and traces back to US-# or FS-#
4. Generate quality-checklist.md:
   - Test coverage requirements
   - Performance benchmarks (from NFR-#)
   - Security review items
   - Accessibility criteria
   - Deployment readiness checks

Write docs/ets-docs/.handoff/implementation.json

---

$ARGUMENTS

## After Implementation

All 21 documents are now complete. The project is ready for development.
Suggest: review sprint-status.yaml, assign team members, begin Sprint 1.
```

### validate.md

```markdown
# Validate

Run quality checks on documentation. Accepts a phase or check type as argument.

## Usage

```
/validate discover    → Discovery Gate
/validate plan        → Planning Gate
/validate design      → Implementation Readiness Gate
/validate sst         → Single Source of Truth check
/validate traceability → ID traceability chain check
/validate all         → Run all checks
```

## Routing

Based on $ARGUMENTS:

### Gate Validation (discover | plan | design)
Spawn validate-gate skill with phase = $0.
Present interactive checklist. Ask for GO/NO-GO/ITERATE decision.

### SST Check (sst)
Spawn check-sst skill (forked Explore agent — read-only).
Returns violation report.

### Traceability Check (traceability)
Spawn check-traceability skill (forked Explore agent — read-only).
Returns orphan ID report.

### Full Validation (all)
Run sst + traceability in parallel, then present combined report.

$ARGUMENTS
```

### orchestrator.md

```markdown
# Orchestrator

Run the complete product documentation workflow: 4 phases, 3 gates, 21 documents.

## Usage

```
/orchestrator              → Start from Phase 1 (or resume from last completed phase)
/orchestrator planning     → Jump to specific phase
/orchestrator resume       → Detect current state and continue
```

## Workflow

### Phase Detection

1. Read docs/ets-docs/.handoff/ directory
2. Find the latest completed phase
3. If $ARGUMENTS specifies a phase → jump there
4. If no arguments → start from next incomplete phase

### Execution Loop

For each phase:
1. Read the phase command file from .claude/commands/:
   - Phase 1: Read discover.md
   - Phase 2: Read plan.md
   - Phase 3: Read design.md
   - Phase 4: Read implement.md
2. Read the handoff file from previous phase (if any)
3. Construct the complete agent prompt: command + upstream context
4. Spawn the agent
5. When agent returns, verify handoff file was written
6. Present gate validation (read validate.md routing logic)
7. If GO → continue to next phase
8. If ITERATE → re-run current phase
9. If NO-GO/DESCOPE/REDESIGN → handle accordingly

### Context Chain

```
(nothing) → discover.md → discovery.json
                         → plan.md → planning.json
                                    → design.md → design.json
                                                 → implement.md → implementation.json
```

Each phase reads the previous handoff and passes it as context to the agent.
The orchestrator is the glue that reads handoffs and chains commands.

$ARGUMENTS
```

### start-project.md

```markdown
# Start Project

Initialize a new product documentation project and begin the orchestrator.

## What It Does

1. Create directory structure:
   ```
   docs/ets-docs/
   ├── .handoff/
   ├── discovery/
   ├── planning/
   │   └── feature-specs/
   ├── architecture/
   ├── data/
   ├── ux/
   └── implementation/
   ```

2. Copy ids.yml template to project root (if not exists)

3. Ask user for initial project metadata:
   - Product name → ids.yml registry.product
   - Namespace → ids.yml registry.namespace
   - Owner → ids.yml registry.owner

4. Hand off to orchestrator (Phase 1: Discovery)

$ARGUMENTS
```

---

## Revised .claude/ Structure (Final)

```
.claude/
├── agents/                          # 7 specialized agents
│   ├── discovery-agent.md           (model: opus)
│   ├── planning-agent.md            (model: opus)
│   ├── architecture-agent.md        (model: opus)
│   ├── data-agent.md                (model: sonnet)
│   ├── ux-agent.md                  (model: sonnet)
│   ├── api-agent.md                 (model: sonnet)
│   └── implementation-agent.md      (model: sonnet)
│
├── commands/                        # 7 commands (= agent spawn prompts)
│   ├── start-project.md             # Init + orchestrate
│   ├── discover.md                  # Phase 1 prompt
│   ├── plan.md                      # Phase 2 prompt
│   ├── design.md                    # Phase 3 prompt (seq + parallel)
│   ├── implement.md                 # Phase 4 prompt
│   ├── validate.md                  # Gate + SST + traceability router
│   └── orchestrator.md              # Full workflow chain
│
├── skills/                          # 25 skills (unchanged)
│   ├── orchestrator/                # Workflow knowledge (NO prompts/ dir)
│   │   ├── SKILL.md
│   │   └── knowledge/
│   │       ├── workflow.md
│   │       ├── handoff-schema.json  # NEW: handoff file schema
│   │       ├── ids.yml
│   │       └── checklists.md
│   ├── discovery/                   # 2 skills
│   ├── planning/                    # 3 skills
│   ├── architecture/                # 2 skills
│   ├── data-design/                 # 6 skills
│   ├── ux-design/                   # 4 skills
│   ├── api-design/                  # 1 skill
│   ├── implementation/              # 3 skills
│   └── validation/                  # 3 skills
│
├── hooks/
│   └── post-document-save.sh
│
└── settings.json
```

**Key changes from v4.0:**
- `knowledge/prompts/` directory REMOVED from orchestrator — commands serve this role
- `knowledge/handoff-schema.json` ADDED to orchestrator — schema for handoff files
- Commands rewritten as complete agent-spawning prompts with $ARGUMENTS
- All output paths updated: `docs/{subdir}/` → `docs/ets-docs/{subdir}/`

---

## Summary of ALL Changes for Implementation

### Structural Changes
1. Output directory: `docs/` → `docs/ets-docs/` (all paths in skills, commands, agents)
2. Handoff directory: `docs/ets-docs/.handoff/` (new)
3. Commands rewritten as agent spawn prompts (7 files)
4. `knowledge/prompts/` removed, `knowledge/handoff-schema.json` added

### Frontmatter Fixes (25 skills)
1. Add YAML frontmatter to 4 UX skills
2. Add `model:` to all 25 skills
3. Add `version: 1.0.0` to all 25 skills
4. Add `compatibility:` to 22 skills
5. Add `argument-hint:` to 5 skills
6. Add `context: fork` + `agent: Explore` to 2 validation skills
7. Set `user-invocable: false` on 2 validation skills
8. Remove invented fields from 6 data-design skills
9. Rewrite all descriptions (EN, pushy, trigger phrases)

### Language Migration (EN)
1. 25 SKILL.md bodies → English
2. 32 knowledge files → English
3. 7 agent prompts → English
4. 7 commands → English
5. CLAUDE.md → English
6. ids.yml → English (user already edited it, preserve structure)
7. Hook comments → English

### Progressive Disclosure Fixes
1. Add `knowledge/` pointers to 17 SKILL.md files
2. Add TOC to 16 knowledge files >300 lines

### Total: ~85 files to create/rewrite
