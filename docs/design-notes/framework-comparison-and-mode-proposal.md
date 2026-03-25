# Framework Comparison & Mode Proposal for ETUS PMDocs v5

**Date:** 2026-03-16
**Author:** AA + Claude
**Status:** Draft — Awaiting Review

---

## 1. Executive Summary

ETUS PMDocs v4.1 was designed for one use case: documenting a **new product from scratch**. This document compares 5 leading AI-agent frameworks (BMAD, Superpowers, Compound Engineering, GitHub Spec Kit, AIOX/Synkra) to identify what work item types and scale-adaptive modes the industry supports — and what ETUS PMDocs is missing.

**Key finding:** BMAD v6 is the closest reference architecture. It solves the exact problem we have with a **3-track scale-adaptive router** that adjusts documentation depth based on work item complexity. The other frameworks confirm the pattern from different angles.

**Recommendation:** Adopt a **4-mode system** (Product, Feature, Bug/Hotfix, Spike/Research) with automatic detection and adjustable documentation depth per mode.

---

## 2. Framework Analysis

### 2.1 BMAD v6 (Breakthrough Method for Agile AI-Driven Development)

**Repo:** [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
**Docs:** [docs.bmad-method.org](https://docs.bmad-method.org/)
**Version:** v6 (19 agents, 50+ workflows)

**Scale-Adaptive Routing — 3 Tracks:**

| Track | Use Case | Artefacts | Time |
|-------|----------|-----------|------|
| **Quick Flow** | Bug fixes, small features, rapid prototyping | Single `tech-spec-{slug}.md` (replaces PRD + Architecture + Stories) | 5-15 min |
| **BMad Method** | Products and platforms | PRD + Architecture + UX + Epic/Story breakdown | 30-60 min |
| **Enterprise** | Large-scale systems with compliance/regulatory needs | Extended planning with all BMad Method docs + compliance artifacts | 60+ min |

**Key insight:** Quick Flow replaces the entire upstream chain (PRD → Architecture → Stories) with **a single tech-spec file** that contains everything a fresh agent needs to implement. This is the exact solution to our "5 docs to spec 1 feature" problem.

**Work item types supported:**
- Bug fixes (Quick Flow → tech-spec only)
- Small features (Quick Flow → tech-spec only)
- Product features (BMad Method → PRD + Architecture)
- Full products (BMad Method → full pipeline)
- Enterprise platforms (Enterprise → extended pipeline)

**What ETUS PMDocs can learn:**
- The **router concept** — detect complexity and route to the right track
- The **single-doc mode** — for bugs and small features, one doc is enough
- The **scale threshold** — Quick Flow if <3-5 days of work; BMad Method if more

---

### 2.2 Superpowers (obra/superpowers)

**Repo:** [obra/superpowers](https://github.com/obra/superpowers)
**Stars:** 82K+ (March 2026)

**Workflow:** Brainstorm → Spec → Plan → TDD → Subagent Dev → Review → Finalize

**Scale-Adaptive Routing — Implicit via entry point:**

| Entry Point | Trigger | Workflow |
|-------------|---------|----------|
| "Let's build X" | New feature/product | Brainstorm → Spec → Plan → Implement |
| "Fix this bug" | Bug | Debug → Domain skills → Fix → Test |
| "Refactor this" | Tech debt | Analysis → Plan → Implement → Review |

**Key insight:** Superpowers doesn't have explicit "modes" — it uses **trigger detection**. The phrase "fix this bug" skips brainstorming and goes straight to debugging. This is elegant but less controllable than BMAD's explicit tracks.

**Work item types supported (implicit):**
- New features ("build X")
- Bug fixes ("fix this bug")
- Refactoring ("refactor this")
- Any task that starts with a brainstorm

**What ETUS PMDocs can learn:**
- **Trigger-based routing** — detect the work type from user intent, not just frontmatter
- **Skip-to-relevant-phase** — a bug doesn't need a brainstorm; a refactor doesn't need personas
- **Composable skills** — each skill activates based on context, not a rigid pipeline

---

### 2.3 Compound Engineering (EveryInc)

**Repo:** [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)
**Philosophy:** Each unit of work makes the next one easier.

**Workflow:** Brainstorm → Plan → Work → Review → Compound → Repeat

**23 workflow commands, 13 skills.** Key workflows:

| Command | Purpose |
|---------|---------|
| `/ce:brainstorm` | Clarify requirements, compare approaches |
| `/workflows:plan` | Architecture, constraints, edge cases |
| `/workflows:work` | Execute with progress tracking |
| `/workflows:review` | 14 specialized reviewers in parallel |
| `/workflows:compound` | Capture learnings for future cycles |

**Key insight:** Compound Engineering doesn't differentiate work item types at all. Every piece of work goes through the same cycle (brainstorm → plan → work → review → compound). The **compound step** at the end is the differentiator — it captures patterns, decisions, and learnings that improve future cycles.

**Work item types supported:**
- Not differentiated. Same cycle for features, bugs, refactors.

**What ETUS PMDocs can learn:**
- The **compound/learning step** — after each work item, capture what was learned
- The **14-reviewer parallel review** — multiple specialized reviewers catch different issues
- The **docs/brainstorms/ folder** — ephemeral brainstorm artifacts that feed into plans

---

### 2.4 GitHub Spec Kit

**Repo:** [github/spec-kit](https://github.com/github/spec-kit)
**Blog:** [Spec-driven development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)

**Workflow:** Specify (`/specify`) → Plan (`/plan`) → Tasks (`/tasks`) → Implement

**Core concept:** Specifications are the primary artifact; code is the generated output. A `constitution.md` file establishes non-negotiable principles.

**Key features:**
- Tasks organized by **user story** with dependency management
- Parallel execution markers `[P]` for tasks that can run simultaneously
- **Evolving specs** — specs change as features are added to existing projects

**Work item types supported:**
- New features (full /specify → /plan → /tasks flow)
- Enhancements to existing features (evolving specs discussion: [#152](https://github.com/github/spec-kit/discussions/152))
- Bug fixes (lighter spec, but same /specify flow)

**Key insight:** Spec Kit treats every work item as needing a spec, even bugs. The spec depth varies, but the process doesn't skip steps. The `constitution.md` is analogous to our `project-context.md` but lives at the repository level, not per-project.

**What ETUS PMDocs can learn:**
- **constitution.md** — a permanent project-level context file that doesn't need regeneration per feature
- **Evolving specs** — specs are not one-time artifacts; they grow with the project
- **Task parallelism markers** — explicit `[P]` for parallel-safe tasks

---

### 2.5 AIOX / Synkra

**Repo:** [SynkraAI/aiox-core](https://github.com/SynkraAI/aiox-core)
**Concept:** AI-Orchestrated System for Full Stack Development

**Key features:**
- **God Mode** — a skill (markdown file) that orchestrates the entire framework
- **SYNAPSE** — adaptive context engine with 8-layer processing pipeline
- **Squads** — modular teams of AI agents (analyst, PM, architect, scrum master, dev, QA)
- **Dedicated agents** collaborate to create PRD and Architecture docs
- **Scrum Master agent** transforms plans into "hyper-detailed" development stories

**Work item types supported:**
- Similar to BMAD — products, features, stories
- Less explicit about bug fixes or lightweight modes

**Key insight:** AIOX's SYNAPSE engine adapts context injection based on context window usage — it doesn't have explicit "modes" but adjusts depth dynamically. The "Squads" concept is similar to our agents but more flexible in composition.

**What ETUS PMDocs can learn:**
- **Dynamic context adaptation** — adjust documentation depth based on available context, not just explicit modes
- **Squad composition** — allow different agent combinations per work type (not all 7 agents for every work item)

---

## 3. Comparative Matrix

| Capability | ETUS PMDocs v4.1 | BMAD v6 | Superpowers | Compound Eng. | Spec Kit | AIOX |
|---|---|---|---|---|---|---|
| **Explicit work item modes** | None (product only) | 3 tracks (Quick/BMad/Enterprise) | Implicit (trigger detection) | None (same cycle for all) | None (same flow, varying depth) | Dynamic (SYNAPSE adapts) |
| **Bug fix support** | No | Yes (Quick Flow) | Yes (debug → fix) | Yes (same cycle) | Yes (light spec) | Partial |
| **Feature-only mode** | No | Yes (Quick Flow) | Yes (brainstorm → spec) | Yes (same cycle) | Yes (/specify) | Yes |
| **Product mode** | Yes (only mode) | Yes (BMad Method) | Yes (full pipeline) | Yes (same cycle) | Yes (full /specify) | Yes |
| **Enterprise mode** | No | Yes (Enterprise track) | No | No | No | Yes (Squads) |
| **Auto-detection of scope** | No | Yes (scale-adaptive router) | Yes (trigger phrases) | No | No | Yes (SYNAPSE) |
| **Single-doc lightweight output** | No (min 2 docs) | Yes (tech-spec-{slug}.md) | Yes (spec.md) | Yes (brainstorm.md → plan.md) | Yes (spec.md) | No (PRD + Architecture) |
| **Standalone invocation (no deps)** | No (rigid chain) | Yes (Quick Flow has no deps) | Yes (any skill standalone) | Yes (any workflow standalone) | Yes (/specify works alone) | Partial |
| **Learning/compound step** | No | No | No | Yes (compound step) | No | No |
| **Parallel agent execution** | Yes (Phase 3 only) | Yes | Yes (subagent dev) | Yes (14 reviewers) | Yes ([P] markers) | Yes (Squads) |

---

## 4. What Modes Should ETUS PMDocs Support?

Based on the comparison, the industry converges on **3-4 distinct scope levels**, with the main differentiator being how much documentation is generated.

### Proposed: 4-Mode System

| Mode | When to use | Docs generated | Pipeline | Detection triggers |
|---|---|---|---|---|
| **Product** | New product/platform from scratch | All 21 docs (full pipeline) | Discovery → Planning → Design → Implementation | "new product", "start project", `/start-project`, `/orchestrator` |
| **Feature** | New feature within existing product | 3-5 docs (feature-spec, user-stories, api-delta, impl-plan) | Feature Brief → Stories → Design Delta → Implementation | "new feature", "add feature", Linear issue with `feature` label, PRD-F-# reference |
| **Bug/Hotfix** | Bug fix, performance fix, small patch | 1 doc (tech-spec-{slug}.md) | Problem → Root Cause → Fix Plan → Implementation | "fix bug", "hotfix", "fix this", Linear issue with `bug` label |
| **Spike/Research** | Investigation, POC, brainstorm, feasibility study | 1 doc (spike-{slug}.md) | Question → Research → Findings → Recommendation | "investigate", "research", "brainstorm", "spike", "POC" |

### Mode Details

#### Product Mode (current behavior, unchanged)
- Full 4-phase pipeline: Discovery → Planning → Design → Implementation
- All 21 documents generated
- All 7 agents activated
- 3 quality gates (GO/NO-GO/ITERATE)
- All dependency chains enforced
- Traceability: BO-# → PRD-F-# → US-# → FS-# → impl-#

#### Feature Mode (new — inspired by BMAD Quick Flow + Superpowers)
- **Input:** Feature description (from user, Linear issue, or Slack thread)
- **Docs generated:**
  - `feature-brief-{slug}.md` — Problem, scope, acceptance criteria, personas affected (replaces project-context + product-vision + prd for this feature)
  - `user-stories-{slug}.md` — US-# with Given/When/Then (SST exception: feature-scoped stories)
  - `design-delta-{slug}.md` — Only what changes: new API endpoints, DB migrations, UI changes (replaces full architecture + data + ux pipeline)
  - `impl-plan-{slug}.md` — impl-# tasks, T-shirt sizing, sprint assignment
- **Agents activated:** planning-agent + 1 design agent (whichever is relevant)
- **No quality gates** (optional validation with `/validate`)
- **Dependencies relaxed:** No upstream product-vision.md required. Uses `project-context.md` if it exists (ENRICHES, not BLOCKS).
- **Output Validation thresholds lowered:**
  - US-#: ≥1 (not ≥5)
  - Acceptance criteria: ≥1 per story (not ≥3)
  - No coverage matrix required
  - No competitive landscape required

#### Bug/Hotfix Mode (new — inspired by BMAD Quick Flow)
- **Input:** Bug description (from user, Linear issue, error log)
- **Docs generated:**
  - `tech-spec-{slug}.md` — Single doc containing: problem description, root cause analysis, fix approach, affected components, test plan, rollback plan
- **Agents activated:** None (orchestrator handles directly, or implementation-agent for complex bugs)
- **No quality gates**
- **No upstream dependencies** — completely standalone
- **Output Validation:** Problem described, fix approach clear, test plan present

#### Spike/Research Mode (new — inspired by Superpowers brainstorm + Compound learning)
- **Input:** Research question or investigation topic
- **Docs generated:**
  - `spike-{slug}.md` — Question, methodology, findings, options evaluated (with pros/cons), recommendation, decision (if made)
- **Agents activated:** discovery-agent (for brainstorm/interview) or none
- **BMAD CIS techniques available** (brainstorm tools work here)
- **No upstream dependencies** — completely standalone
- **Output feeds into:** Next work item (feature, product, or decision record)
- **Compound step:** Findings saved for future reference

---

## 5. Implementation Strategy

### 5.1 Mode Detection (Auto-Router)

The orchestrator should detect mode automatically based on:

1. **Explicit command:** `/start-project` → Product, `/feature` → Feature, `/bugfix` → Bug, `/spike` → Spike
2. **Trigger phrases:** "fix bug" → Bug, "new feature" → Feature, "investigate" → Spike
3. **Linear issue labels:** `bug` → Bug, `feature` → Feature, `spike` → Spike
4. **Context:** If `project-context.md` exists but user asks about a specific feature → Feature mode
5. **Fallback:** Ask user "Is this a product, feature, bug, or research?"

### 5.2 What Changes Per Skill

| Skill | Product | Feature | Bug | Spike |
|---|---|---|---|---|
| project-context | Full 5W2H interview | Skip (use existing or ask 3 questions) | Skip | Skip |
| product-vision | Full BMAD CIS | Skip | Skip | BMAD CIS available |
| prd | Full MoSCoW, ≥5 PRD-F-# | Inline in feature-brief | Skip | Skip |
| user-stories | Full, ≥1 per Must Have | Scoped to feature, ≥1 US-# | Skip (test plan in tech-spec) | Skip |
| feature-spec | On-demand (>3 rules) | Always generated (it IS the feature) | Skip | Skip |
| architecture-diagram | Full C4 | Skip (reference existing) | Skip | Skip |
| tech-spec | Full NFRs + ADRs | Delta only (new NFRs if any) | Single tech-spec-{slug}.md | Skip |
| data-* (6 skills) | Full pipeline | Delta only (new tables/fields) | Skip | Skip |
| ux-* (4 skills) | Full pipeline | Delta only (new screens/flows) | Skip | Skip |
| api-spec | Full | Delta only (new endpoints) | Skip | Skip |
| implementation-plan | Full | Scoped to feature | Inline in tech-spec | Skip |
| sprint-status | Full | Feature tasks added to existing sprint | Bug task added to current sprint | Skip |
| quality-checklist | Full | Scoped to feature | Inline in tech-spec (test plan) | Skip |
| orchestrator | Full 4-phase | Feature pipeline (2 phases) | Bug pipeline (1 phase) | Spike pipeline (1 phase) |
| check-sst | Full scan | Feature-scoped scan | Skip | Skip |
| check-traceability | Full chain | Feature chain only | Skip | Skip |
| validate-gate | 3 gates | Optional | Skip | Skip |

### 5.3 New Artifacts Needed

| Artifact | Mode | Template needed |
|---|---|---|
| `feature-brief-{slug}.md` | Feature | Yes — problem, scope, personas, acceptance criteria |
| `design-delta-{slug}.md` | Feature | Yes — API delta, DB delta, UI delta |
| `tech-spec-{slug}.md` (standalone) | Bug | Yes — problem, root cause, fix, test plan, rollback |
| `spike-{slug}.md` | Spike | Yes — question, methodology, findings, recommendation |

### 5.4 Output Directory Structure

```
docs/ets-docs/
├── discovery/          # Product mode only
├── planning/           # Product + Feature mode
├── architecture/       # Product mode only
├── data/               # Product mode only
├── ux/                 # Product mode only
├── implementation/     # All modes
├── features/           # NEW — Feature mode artifacts
│   ├── feature-brief-checkout.md
│   ├── user-stories-checkout.md
│   ├── design-delta-checkout.md
│   └── impl-plan-checkout.md
├── bugs/               # NEW — Bug mode artifacts
│   └── tech-spec-fix-login-timeout.md
├── spikes/             # NEW — Spike mode artifacts
│   └── spike-evaluate-redis-vs-memcached.md
└── .handoff/           # Phase handoff JSON files
```

---

## 6. Priority Ordering

| Priority | Change | Impact | Effort |
|---|---|---|---|
| **P0** | Add mode detection to orchestrator | Enables all other modes | Medium |
| **P0** | Create Bug/Hotfix mode (tech-spec-{slug}.md template) | Highest frequency use case after features | Low |
| **P1** | Create Feature mode (feature-brief + design-delta templates) | Core gap identified in audit | High |
| **P1** | Relax dependency chains (BLOCKS → ENRICHES for Feature/Bug modes) | Enables standalone invocation | Medium |
| **P1** | Add adjustable Output Validation thresholds per mode | Prevents permanent DRAFT for feature-scoped docs | Medium |
| **P2** | Create Spike mode (spike-{slug}.md template) | Supports research/brainstorm use case | Low |
| **P2** | Add compound/learning step (inspired by Compound Engineering) | Long-term knowledge accumulation | Medium |
| **P3** | Enterprise mode (extended compliance artifacts) | Not needed now | High |

---

## 7. Sources

- [BMAD METHOD v6 — GitHub](https://github.com/bmad-code-org/BMAD-METHOD)
- [BMAD Quick Flow Documentation](https://docs.bmad-method.org/explanation/quick-flow/)
- [BMAD Scale-Adaptive Routing — DeepWiki](https://deepwiki.com/bmadcode/BMAD-METHOD/4.2-context-engineered-development-(ide))
- [Superpowers — GitHub (obra)](https://github.com/obra/superpowers)
- [Superpowers Blog Post (October 2025)](https://blog.fsck.com/2025/10/09/superpowers/)
- [Compound Engineering Plugin — GitHub (EveryInc)](https://github.com/EveryInc/compound-engineering-plugin)
- [Compound Engineering Philosophy](https://every.to/guides/compound-engineering)
- [GitHub Spec Kit — GitHub](https://github.com/github/spec-kit)
- [Spec-Driven Development Blog (GitHub)](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [AIOX / Synkra — GitHub](https://github.com/SynkraAI/aiox-core)
- [Comprehensive Guide: Kiro, GitHub Spec Kit, BMAD — Medium](https://medium.com/@visrow/comprehensive-guide-to-spec-driven-development-kiro-github-spec-kit-and-bmad-method-5d28ff61b9b1)
