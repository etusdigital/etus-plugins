# ETUS PMDocs — Product Documentation Framework v5.3

Product documentation framework with 9 agents, 48 skills, 4 work modes, an ideation layer, explicit solution discovery, and an interactive workflow based on Double Diamond, BMAD, and Superpowers methodologies.

## Quick Start

```bash
/ideate              # Ideate layer: opportunity-pack + coverage matrix
/ideate status       # Inspect checkpoints, blockers, and next ideate step
/ideate jobs         # Resume JTBD extraction
/ideate journeys     # Resume journey mapping
/ideate synth        # Consolidate the opportunity pack and prepare handoff
/plan opportunities  # Build OST + prioritization
/solution            # Reduce value/usability/viability/feasibility risk
/plan requirements   # Define PRD + user-stories + feature-spec
/start-project        # Product mode: full 4-phase pipeline (26 docs)
/feature              # Feature mode: 3-5 focused docs for a single feature
/feature status       # Inspect the canonical state hub of a feature
/bugfix               # Bug mode: single tech-spec with root cause + fix plan
/spike                # Spike mode: single research/brainstorm document
/orchestrator         # Full workflow (auto-detects mode)
```

## 4-Mode System

The orchestrator auto-detects the right mode from commands, trigger phrases, or project context. Each mode generates only the documentation appropriate for the scope of work.

| Mode | When to use | Docs generated | Pipeline |
|------|-------------|----------------|----------|
| **Product** | New product/platform from scratch | All 26 docs | Discovery → Planning → Design → Implementation (4 phases, 3 gates) |
| **Feature** | New feature within existing product | 5-6 scoped artifacts + state | Ideate → Solution → Brief → Stories → Delta → Impl |
| **Bug** | Bug fix, hotfix, performance patch | 1 doc | Problem → Root Cause → Fix → Test Plan → Rollback |
| **Spike** | Investigation, POC, brainstorm | 1 doc | Question → Methodology → Findings → Recommendation |

**Detection triggers:**
- Explicit commands: `/start-project` → Product, `/feature` → Feature, `/bugfix` → Bug, `/spike` → Spike
- Phrases: "fix bug"/"hotfix" → Bug, "new feature"/"add feature" → Feature, "investigate"/"research"/"spike" → Spike
- Context: existing project-context.md + scoped request → Feature
- Fallback: asks the user to choose

## Architecture

**9 Agents → 48 Skills → 27 Documents → 5 Gates**

```
Opening Layer: IDEATE (Opus)
  → opportunity-pack.md
  → coverage-matrix.yaml

Phase 1: DISCOVERY (discovery-agent, Opus)
  → derives from opportunity-pack.md
  → project-context.md
  → baseline.md (current state metrics & data quality)
  → discovery-report.md (evidence synthesis, insights, hypotheses H-#)
  → product-vision.md (vision + BO-# + BMAD brainstorm)
  → Discovery Gate (GO/NO-GO/ITERATE)

Phase 2A: OPPORTUNITY FOCUS (planning-agent, Opus)
  → ost.md (opportunity solution tree)
  → prioritization.md (ICE/RICE scoring → P0/P1/P2)
  → Opportunity Focus Gate (GO/ITERATE)

Phase 2B: SOLUTION DISCOVERY (planning-agent, Opus)
  → solution-discovery.md
  → solution-report.json
  → Solution Readiness Gate (GO/ITERATE/NO-GO)

Phase 2C: REQUIREMENTS (planning-agent, Opus)
  → prd.md + user-stories.md + feature-spec-*.md
  → HMW + MoSCoW prioritization
  → Requirements Gate (GO/DESCOPE/ITERATE)

Phase 3: DESIGN (4 agents, Sonnet)
  3a. architecture-agent → architecture-diagram.md + tech-spec.md
  3b. PARALLEL: data-agent (6 docs) + ux-agent (4 docs) + api-agent (1 doc)
  → Implementation Readiness Gate (GO/REDESIGN/ITERATE)

Phase 4: IMPLEMENTATION (implementation-agent, Sonnet)
  → implementation-plan.md + quality-checklist.md + release-plan.md
  → release-plan.md (rollout strategy, rollback, monitoring)
```

## Output Structure

All generated artifacts are saved to `docs/ets/`, with one project root per initiative:

```text
docs/ets/
├── catalog/
├── projects/
│   └── {project-slug}/
│       ├── discovery/
│       ├── planning/
│       ├── architecture/
│       ├── data/
│       ├── ux/
│       ├── implementation/
│       ├── features/
│       │   └── {feature-slug}/
│       ├── bugs/
│       ├── spikes/
│       ├── adrs/
│       ├── learnings/
│       └── state/
│           ├── project-status.yaml
│           ├── workflow-state.yaml
│           ├── feature-index.yaml
│           ├── execution-status.yaml   # optional
│           └── execution-sync.yaml     # optional
└── schemas/
```

## Framework Structure

```
.claude/
├── agents/           # 9 specialized subagents
│   ├── discovery-agent.md      (Opus)
│   ├── planning-agent.md       (Opus)
│   ├── architecture-agent.md   (Opus)
│   ├── data-agent.md           (Sonnet)
│   ├── ux-agent.md             (Sonnet)
│   ├── api-agent.md            (Sonnet)
│   ├── implementation-agent.md (Sonnet)
│   ├── learnings-researcher.md (Sonnet)
│   └── spec-reviewer.md       (inherit)
│
├── commands/         # 15 commands (= agent spawn prompts)
│   ├── start-project.md        # Product mode: init + orchestrate
│   ├── ideate.md               # Opening ideation layer
│   ├── discover.md             # Phase 1 prompt
│   ├── solution.md             # Solution discovery stage
│   ├── plan.md                 # Phase 2 prompt
│   ├── design.md               # Phase 3 prompt (seq + parallel)
│   ├── implement.md            # Phase 4 prompt
│   ├── validate.md             # Gate + SST + traceability router
│   ├── orchestrator.md         # Full workflow chain (auto-detects mode)
│   ├── feature.md              # Feature mode entry point
│   ├── bugfix.md               # Bug/Hotfix mode entry point
│   ├── spike.md                # Spike/Research mode entry point
│   ├── correct-course.md      # Mid-sprint change management
│   ├── elicit.md              # Semantic stress-test: ambiguities, contradictions, gaps
│   └── retro.md               # Post-implementation feedback: capture what dev had to guess
│
├── skills/           # 48 skills across discovery, planning, design, implementation, validation, help, and retrospective
│   ├── orchestrator/           # Maestro — delegates to agents
│   ├── discovery/              # project-context, product-vision
│   ├── planning/               # prd, user-stories, feature-spec
│   ├── architecture/           # architecture-diagram, tech-spec
│   ├── data-design/            # 6 data docs
│   ├── ux-design/              # 4 UX docs
│   ├── api-design/             # api-spec
│   ├── implementation/         # implementation-plan, quality-checklist, release-plan
│   └── validation/             # check-traceability, check-sst, validate-gate
│
├── hooks/            # Automation
│   ├── post-document-save.sh   # Real-time SST validation
│   ├── memory-sync.py          # PostToolUse hook — auto-updates project-state.md
│   ├── memory-init.py          # One-time DB setup / migration
│   └── memory-write.py         # Skill wrapper: decision/preference/pattern/linear/query
│
└── settings.json     # Hook configuration
```

## Persistent Memory System

The framework uses a **hybrid SQLite + Markdown** memory architecture that persists state across sessions.

**How it works:**
- **Markdown in `docs/ets/projects/{project-slug}/...`** — source of truth for semantic product context and design intent
- **YAML in `docs/ets/projects/{project-slug}/state/...`** — source of truth for workflow state and optional execution adapter state
- **SQLite DB** (`~/.claude/etus-memory/memory-{hash}.db`) — index, memory, and fast-query layer

**Six memory files:**

| File | Purpose | Updated by |
|------|---------|------------|
| `project-state.md` | Current phase, mode, docs completed, next step | `memory-sync.py` (hook, automatic) |
| `decisions.md` | Architectural and product decisions (DEC-#) | `memory-write.py decision` |
| `preferences.md` | User/team preferences (PREF-#) | `memory-write.py preference` |
| `patterns.md` | Recurring document patterns (PAT-#) | `memory-write.py pattern` |
| `linear-mapping.md` | ETUS ID ↔ Linear issue mapping | `memory-write.py linear` |
| `repo-docs.md` | Index of all `.md` files in `docs/` (design docs, plans, notes) | `memory-sync.py` (hook) + `memory-write.py index-docs` |

**Skill commands (called via Bash tool in skills):**
```bash
python3 .claude/hooks/memory-write.py decision  "<text>" "<rationale>" "<skill>" "<phase>" "<tags>"
python3 .claude/hooks/memory-write.py preference "<text>" "<skill>" "<category>"
python3 .claude/hooks/memory-write.py pattern    "<text>" "<skill>" "<applies_to>"
python3 .claude/hooks/memory-write.py linear     "<etus_id>" "<linear_id>" "<title>" "<type>" "<status>"
python3 .claude/hooks/memory-write.py supersede  "<DEC-NNN>" "<reason>"
python3 .claude/hooks/memory-write.py query      <decisions|preferences|patterns|linear|repo-docs>
python3 .claude/hooks/memory-write.py index-docs  # re-scan docs/ and update index
```

**Initialization (first time or after container reset):**
```bash
python3 .claude/hooks/memory-init.py           # init DB only
python3 .claude/hooks/memory-init.py --migrate  # init + import existing docs
```

## Workflow State

Each phase writes state into `docs/ets/projects/{project-slug}/state/`. The next phase reads local YAML state and reports from there for upstream context.

```text
state/coverage-matrix.yaml
  -> state/reports/discovery.json
  -> state/reports/opportunities.json
  -> state/reports/solution-report.json
  -> state/reports/planning.json
  -> state/reports/design.json
  -> state/reports/implementation.json
```

## IDs and Traceability

```
BO-# → PRD-F-# → US-# → FS-[name]-# → impl-#
                                ↕
                          NFR-#, ADR-#
                    dict.*, ev.*, tok.*

Auxiliary IDs:
  NG-#   — Non-Goals (opportunity-pack, feature-brief; traced for violation detection)
  SNAP-# — Story Snapshots (ideation interview stories → JTBD-#, JOUR-#)
  EL-#   — Elicitation Findings (/elicit output; subcategories: EL-A, EL-C, EL-B, EL-H, EL-E, EL-D)
```

## Single Source of Truth (SST)

| Content | Exclusive Document |
|---------|-------------------|
| Given/When/Then | user-stories.md |
| NFR-# targets | tech-spec.md |
| ADR-# decisions | tech-spec.md |
| DDL (CREATE TABLE) | database-spec.md |
| dict.*/ev.* definitions | data-dictionary.md |
| tok.* design tokens | style-guide.md |
| API schemas | api-spec.md |
| Baseline metrics (current state) | baseline.md |
| Structured opportunities + candidate solutions | ost.md |
| Rollout strategy + rollback plan + monitoring | release-plan.md |
| Discovery evidence, method/sample, insights by theme | discovery-report.md |
| ICE/RICE scores, P0/P1/P2 ranking, trade-offs | prioritization.md |

## Commands

```bash
# Mode entry points
/start-project    # Product mode: create structure + start Discovery (full pipeline)
/ideate           # Opening ideation layer: opportunity-pack + coverage-matrix
/ideate status    # Show ideate checkpoints, blockers, and next recommended step
/plan opportunities # Build OST + prioritization
/solution         # Run solution discovery before delivery requirements
/plan requirements # Define delivery requirements after solution is chosen
/feature          # Feature mode: document a feature (3-5 docs, no gates required)
/bugfix           # Bug mode: root cause + fix plan + test plan (1 doc)
/spike            # Spike mode: research/brainstorm/feasibility (1 doc)

# Product mode phases (also usable standalone)
/discover         # Phase 1: interview + vision
/plan             # Phase 2: PRD + stories + feature specs
/design           # Phase 3: architecture + data/ux/api parallel
/implement        # Phase 4: plan + sprints + quality

# Utilities
/validate         # Validation: traceability, SST, or gate
/orchestrator     # Full workflow (auto-detects mode from context)
/correct-course   # Mid-sprint change management: impact analysis + document updates
/elicit            # Semantic stress-test: find ambiguities, contradictions, gaps
/retro             # Post-implementation feedback: capture what dev had to guess
```

## Interaction Protocol

All skills follow a consistent interaction pattern:

1. **One question per message** — Skills ask one question at a time, waiting for the answer before proceeding
2. **3-4 suggestions for choices** — When a decision point is reached, skills present 3-4 concrete options with tradeoffs and a recommendation
3. **Approaches before generating** — Before creating content, skills propose 2-3 approaches and let the user choose direction
4. **Section-by-section approval** — Documents are presented one section at a time for user review before saving
5. **Outstanding questions tracked** — Unresolved questions are classified as "blocks next phase" or "deferred"
6. **Multiple handoff options** — At completion, skills offer 3-4 next steps instead of a single fixed path

## Parallel Agents

Parallel agents are a **context management** technique (not related to team size).

Required rules:
1. **Complete prompt** — each agent starts with zero context
2. **Mandatory report** — each agent must generate a report of what it did
3. **Consolidation** — orchestrator consolidates results via handoff files

## Methodologies

- **Double Diamond** — Discover → Define → Develop → Deliver
- **5W2H** — Structured interview (What, Who, Where, When, Why, How, How Much)
- **HMW** — How Might We (transform problems into opportunities)
- **MoSCoW** — Must/Should/Could/Won't (feature prioritization)
- **BMAD CIS** — 8 user-selectable brainstorm techniques

## MCP Compatibility

- **Slack MCP** — Used during discovery and planning for stakeholder communication
- **External tracker integrations** — Optional adapters for issue tracking systems such as Linear
- **Figma MCP** — Used during UX design for importing design tokens and styles

## Version

- **v5.3** — 2026-03-17
- 4-mode system (Product, Feature, Bug, Spike) with auto-detection
- Dedicated ideation layer (`/ideate`) before downstream docs
- 9 agents, 48 skills, 15 commands, 3 hooks
- 5 new skills: baseline, ost, release-plan, discovery-report (evidence synthesis), prioritization (ICE/RICE)
- Mode detection router in orchestrator
- Handoff protocol for automated phase chaining
- **Persistent memory system** (hybrid SQLite + Markdown): project-state, decisions, preferences, patterns, linear-mapping
- All content in English
