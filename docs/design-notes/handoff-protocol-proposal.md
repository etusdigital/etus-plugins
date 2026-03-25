# Handoff Protocol Design — ETUS PMDocs v4.1

## How Context Flows in Claude Code (Facts)

### What Works

```
$ARGUMENTS     — String substitution BEFORE Claude sees the skill
$0, $1, $2     — Positional arguments (space-separated)
${CLAUDE_SKILL_DIR}  — Absolute path to skill directory (for loading scripts/resources)
${CLAUDE_SESSION_ID} — Current session ID
!`command`     — Shell preprocessing (runs BEFORE Claude sees anything)
```

### What Doesn't Work

- Skills cannot invoke other skills directly
- Subagents cannot spawn sub-subagents (max depth = 1)
- No real-time context sharing between parallel subagents
- $ARGUMENTS is string-only (no structured data)

### The Execution Chain

```
User invokes /command or /skill
    ↓
$ARGUMENTS substituted → Claude receives final text
    ↓
Skill instructs Claude to use Agent tool
    ↓
Agent spawns with COMPLETE prompt (no prior context)
    ↓
Agent has preloaded skills (via skills: field in agent frontmatter)
    ↓
Agent reads upstream docs, generates output, writes handoff report
    ↓
Result returns to caller (orchestrator)
    ↓
Orchestrator reads handoff, constructs next agent prompt, spawns next agent
```

**Key insight:** The agent prompt IS the context. There's no magic inheritance.
The orchestrator must construct a complete, self-contained prompt for each agent.

---

## The Handoff Protocol

### Concept: Handoff Files

Each phase writes a structured handoff file when complete. The next phase reads it.

```
docs/
├── .handoff/
│   ├── discovery.json      ← Written by discovery-agent
│   ├── planning.json       ← Written by planning-agent
│   ├── design.json         ← Written by architecture/data/ux/api agents
│   └── implementation.json ← Written by implementation-agent
```

### Handoff File Schema

```json
{
  "phase": "discovery",
  "status": "complete",
  "gate_result": "GO",
  "iteration": 1,
  "documents": [
    {
      "path": "docs/discovery/project-context.md",
      "type": "project-context",
      "ids_generated": []
    },
    {
      "path": "docs/discovery/product-vision.md",
      "type": "product-vision",
      "ids_generated": ["BO-1", "BO-2", "BO-3"]
    }
  ],
  "id_state": {
    "bo": 3,
    "prd-f": 0,
    "us": 0,
    "nfr": 0,
    "adr": 0,
    "impl": 0
  },
  "key_decisions": [
    "Target market: Brazilian SMBs",
    "Mobile-first approach",
    "API-first architecture"
  ],
  "recommendations_for_next_phase": [
    "Focus PRD on invoice generation workflow",
    "Consider offline capability as Must-have",
    "Address LGPD compliance early"
  ],
  "timestamp": "2026-03-14T15:30:00Z"
}
```

### How It Flows

```
Phase 1: DISCOVERY
┌─────────────────────────────────────────┐
│ Orchestrator reads: nothing (first)     │
│ Spawns: discovery-agent                 │
│ Agent prompt includes:                  │
│   - Full skill instructions             │
│   - "Write handoff to docs/.handoff/"   │
│ Agent writes: docs/.handoff/discovery.json │
│ Agent returns: summary report           │
│ Orchestrator: presents gate to user     │
│ User: GO → orchestrator continues       │
└─────────────────────────────────────────┘
                    ↓
Phase 2: PLANNING
┌─────────────────────────────────────────┐
│ Orchestrator reads: discovery.json      │
│ Constructs prompt with:                 │
│   - Upstream docs paths                 │
│   - IDs generated (BO-1..BO-3)          │
│   - Key decisions from discovery        │
│   - Gate result                         │
│ Spawns: planning-agent                  │
│ Agent writes: docs/.handoff/planning.json │
│ Orchestrator: presents gate to user     │
└─────────────────────────────────────────┘
                    ↓
Phase 3: DESIGN (parallel)
┌─────────────────────────────────────────┐
│ Orchestrator reads: planning.json       │
│ Spawns architecture-agent FIRST (needs  │
│   to complete before parallel agents)   │
│ Then spawns IN PARALLEL:                │
│   - data-agent (with arch + plan ctx)   │
│   - ux-agent (with arch + plan ctx)     │
│   - api-agent (with arch + plan ctx)    │
│ Each writes partial handoff             │
│ Orchestrator merges into design.json    │
│ Orchestrator: presents gate to user     │
└─────────────────────────────────────────┘
                    ↓
Phase 4: IMPLEMENTATION
┌─────────────────────────────────────────┐
│ Orchestrator reads: design.json         │
│ Spawns: implementation-agent            │
│ Agent writes: implementation.json       │
│ Done: all 21 docs + handoff chain       │
└─────────────────────────────────────────┘
```

---

## Pre-Formatted Agent Prompts

### The Pattern

The orchestrator skill contains **prompt templates** for each agent. These templates
use placeholders that the orchestrator fills in at runtime by reading handoff files.

This is NOT $ARGUMENTS substitution — it's the orchestrator constructing the prompt
dynamically using the Agent tool.

### Template: Discovery Agent Spawn

```markdown
## DISCOVERY AGENT PROMPT TEMPLATE

When spawning the discovery-agent, use this prompt with the Agent tool:

---

You are the Discovery Agent for the ETUS PMDocs framework.

**PROJECT:** [Read from ids.yml: registry.product, or ask user if empty]

**YOUR TASK:**
1. Read `${CLAUDE_SKILL_DIR}/../discovery/project-context/SKILL.md` and follow its protocol
   - Conduct the 5W2H interview with the user
   - Save output to `docs/discovery/project-context.md`
2. Read `${CLAUDE_SKILL_DIR}/../discovery/product-vision/SKILL.md` and follow its protocol
   - Conduct BMAD brainstorm (propose techniques, user selects)
   - Save output to `docs/discovery/product-vision.md`

**HANDOFF REPORT (MANDATORY):**
When both documents are complete, write `docs/.handoff/discovery.json` with:
```json
{
  "phase": "discovery",
  "status": "complete",
  "documents": [<paths and IDs generated>],
  "id_state": {"bo": <last BO number>},
  "key_decisions": [<top 3-5 from interview>],
  "recommendations_for_next_phase": [<what planning should focus on>]
}
```

Also update `ids.yml` sequences.bo with the last BO number used.

---
```

### Template: Planning Agent Spawn

```markdown
## PLANNING AGENT PROMPT TEMPLATE

Read `docs/.handoff/discovery.json` first. Then use this prompt:

---

You are the Planning Agent for the ETUS PMDocs framework.

**UPSTREAM CONTEXT:**
- Discovery phase: {gate_result} (iteration {iteration})
- Documents available:
  {for each doc in discovery.json.documents:}
  - {doc.path} (IDs: {doc.ids_generated})
  {end}
- Key decisions from discovery: {discovery.json.key_decisions}
- Recommendations: {discovery.json.recommendations_for_next_phase}

**YOUR TASK:**
1. READ the upstream documents listed above — they contain the full product context
2. Read the prd skill and generate `docs/planning/prd.md`
   - Use HMW to transform problems into opportunities
   - Use MoSCoW to prioritize features
   - Each PRD-F-# MUST reference a BO-# from product-vision
3. Read the user-stories skill and generate `docs/planning/user-stories.md`
   - Each US-# MUST reference a PRD-F-#
   - Acceptance criteria in Given/When/Then format
4. For complex features (>3 business rules), generate feature-spec-[name].md

**HANDOFF REPORT (MANDATORY):**
Write `docs/.handoff/planning.json` with:
- All document paths and IDs generated
- id_state with updated sequences (prd-f, us, fs if any)
- MoSCoW summary (which features are Must/Should/Could/Won't)
- Recommendations for design phase

---
```

### Template: Design Phase (Sequential + Parallel)

```markdown
## DESIGN PHASE PROMPT TEMPLATE

Read `docs/.handoff/planning.json` first. Execute in TWO stages:

### Stage 1: Architecture (Sequential — must complete first)

Spawn architecture-agent with:

---

You are the Architecture Agent for the ETUS PMDocs framework.

**UPSTREAM CONTEXT:**
- Planning phase: {gate_result}
- PRD: docs/planning/prd.md ({N} features: {PRD-F-1..PRD-F-N})
- User Stories: docs/planning/user-stories.md ({M} stories)
- MoSCoW summary: {planning.json.key_decisions}

**YOUR TASK:**
1. READ docs/planning/prd.md and docs/planning/user-stories.md
2. Generate docs/design/architecture-diagram.md (C4 model)
3. Generate docs/design/tech-spec.md (NFRs + ADRs)

**HANDOFF:** Write partial handoff to docs/.handoff/design-architecture.json

---

### Stage 2: Parallel Agents (after architecture completes)

Read docs/.handoff/design-architecture.json, then spawn THREE agents simultaneously:

**Data Agent prompt:**

---

You are the Data Agent. UPSTREAM: architecture-diagram.md, tech-spec.md, prd.md, user-stories.md.
Generate 6 documents: data-requirements → erd → database-spec → data-dictionary → data-flow-diagram → data-catalog.
Handoff: docs/.handoff/design-data.json

---

**UX Agent prompt:**

---

You are the UX Agent. UPSTREAM: product-vision.md, user-stories.md, architecture-diagram.md.
Generate 4 documents: user-journey → ux-sitemap → wireframes → style-guide.
Handoff: docs/.handoff/design-ux.json

---

**API Agent prompt:**

---

You are the API Agent. UPSTREAM: tech-spec.md, database-spec.md, user-stories.md.
Generate 1 document: api-spec.md.
Handoff: docs/.handoff/design-api.json

---

### Stage 3: Merge

After all 4 agents complete, merge their handoffs into docs/.handoff/design.json.
Cross-validate: do data schemas match API schemas? Do wireframes reference tok.* from style-guide?
```

### Template: Implementation Agent Spawn

```markdown
## IMPLEMENTATION AGENT PROMPT TEMPLATE

Read `docs/.handoff/design.json` first. Then:

---

You are the Implementation Agent.

**UPSTREAM CONTEXT:**
- All 17 documents from discovery + planning + design
- ID state: {design.json.id_state}
- Key architecture decisions: {design.json.key_decisions}

**YOUR TASK:**
1. Read ALL upstream documents (paths listed in design.json)
2. Generate docs/implementation/implementation-plan.md
3. Generate docs/implementation/sprint-status.yaml
4. Generate docs/implementation/quality-checklist.md

**HANDOFF:** Write docs/.handoff/implementation.json

---
```

---

## How $ARGUMENTS Fits In

### Direct Skill Invocation (User Bypassing Orchestrator)

When a user invokes a skill directly (not through orchestrator), $ARGUMENTS provides
the upstream context. This enables ad-hoc usage.

**Example: User wants to generate just the PRD**

```
/prd upstream:docs/discovery/product-vision.md
```

The prd SKILL.md would contain:

```markdown
---
name: prd
description: >
  Generate prd.md with prioritized features (PRD-F-#) using HMW and MoSCoW...
model: claude-opus-4
version: 1.0.0
argument-hint: "[upstream-doc-path]"
---

# PRD Generation

## Context Loading

If arguments were provided, read the upstream document:
- Upstream document: $ARGUMENTS

If no arguments, scan for existing discovery documents:
1. Check if docs/.handoff/discovery.json exists → read it
2. Check if docs/discovery/product-vision.md exists → read it
3. If neither exists, ask the user for product context

## Process
...
```

### Argument Patterns for Each Skill

| Skill | Argument | Example |
|---|---|---|
| orchestrator | `[phase]` | `/orchestrator planning` |
| project-context | (none — interactive) | `/project-context` |
| product-vision | `[context-path]` | `/product-vision docs/discovery/project-context.md` |
| prd | `[upstream-path]` | `/prd docs/discovery/product-vision.md` |
| user-stories | `[upstream-path]` | `/user-stories docs/planning/prd.md` |
| feature-spec | `[feature-name]` | `/feature-spec checkout` |
| validate-gate | `[phase]` | `/validate-gate discovery` |
| sprint-status | `[sprint-number]` | `/sprint-status 2` |
| check-sst | `[doc-path]` | `/check-sst docs/planning/prd.md` |
| check-traceability | `[id-prefix]` | `/check-traceability US` |
| All data/ux/api skills | `[upstream-path]` | `/erd docs/data/data-requirements.md` |

### Fallback Chain (When No Arguments)

Every skill should follow this priority:
1. **$ARGUMENTS provided** → use it as upstream context
2. **Handoff file exists** → read docs/.handoff/{phase}.json
3. **Upstream doc exists** → scan docs/ directory
4. **Nothing found** → ask user for context

This makes skills work both in automated (orchestrator) and manual (direct invocation) modes.

---

## Revised Orchestrator SKILL.md Structure

```
orchestrator/
├── SKILL.md                    # Main skill (~200 lines)
│   ├── Workflow overview
│   ├── Phase detection logic
│   ├── Gate interaction protocol
│   └── Pointers to knowledge/ files
│
└── knowledge/
    ├── workflow.md             # Full 4-phase workflow
    ├── prompts/                # Pre-formatted agent prompts
    │   ├── discovery-prompt.md
    │   ├── planning-prompt.md
    │   ├── design-prompt.md
    │   └── implementation-prompt.md
    ├── handoff-schema.json     # Handoff file schema
    ├── ids.yml                 # ID registry template
    └── checklists.md           # Gate checklists
```

The `prompts/` directory is the key addition. Each file contains the complete
prompt template that the orchestrator uses when spawning agents. The orchestrator:
1. Reads the handoff file from previous phase
2. Reads the prompt template for next phase
3. Fills in the context (upstream docs, IDs, decisions)
4. Spawns the agent with the constructed prompt

---

## Updated Frontmatter Summary

With this handoff protocol, the frontmatter changes:

### Skills that accept $ARGUMENTS

| Skill | argument-hint | $ARGUMENTS usage |
|---|---|---|
| orchestrator | `[phase]` | Jump to specific phase |
| product-vision | `[context-path]` | Path to project-context.md |
| prd | `[upstream-path]` | Path to product-vision.md |
| user-stories | `[upstream-path]` | Path to prd.md |
| feature-spec | `[feature-name]` | Feature to spec |
| sprint-status | `[sprint-number]` | Which sprint |
| validate-gate | `[phase]` | Which gate to validate |
| check-sst | `[doc-path]` | Optional: specific doc to check |
| check-traceability | `[id-prefix]` | Optional: specific ID chain |
| All other skills | `[upstream-path]` | Path to upstream doc |

### Skills that write handoff files

| Agent | Handoff File | Contents |
|---|---|---|
| discovery-agent | docs/.handoff/discovery.json | BO-# IDs, decisions, recommendations |
| planning-agent | docs/.handoff/planning.json | PRD-F-#, US-#, MoSCoW summary |
| architecture-agent | docs/.handoff/design-architecture.json | NFR-#, ADR-#, tech stack |
| data-agent | docs/.handoff/design-data.json | dict.*, ev.*, DDL summary |
| ux-agent | docs/.handoff/design-ux.json | tok.*, journey touchpoints |
| api-agent | docs/.handoff/design-api.json | Endpoints, schemas |
| implementation-agent | docs/.handoff/implementation.json | impl-#, sprint plan |

---

## Decision Points

1. **Handoff as JSON vs Markdown** — JSON is more parseable by the model, but Markdown
   is more readable for humans. Recommendation: JSON for machine handoff, with a summary
   section in each document's YAML frontmatter for human readability.

2. **Prompt templates as separate files vs inline** — Separate files in `knowledge/prompts/`
   keep the orchestrator SKILL.md lean (<200 lines) and make templates independently
   editable. Recommended.

3. **Fallback chain complexity** — The 4-level fallback ($ARGUMENTS → handoff → scan → ask)
   adds resilience but also code. Worth it because it makes skills work in both automated
   and manual modes.

4. **Handoff directory (.handoff/)** — Hidden directory to keep docs/ clean. Alternative:
   `docs/_meta/` or `docs/.state/`. Recommendation: `.handoff/` because it's descriptive
   and the dot prefix hides it in most file browsers.
