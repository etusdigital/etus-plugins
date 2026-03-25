---
title: "feat: ETUS PMDocs v5 — Complete Overhaul"
type: feat
status: active
date: 2026-03-17
origin: docs/design/framework-comparison-and-mode-proposal.md
---

# ETUS PMDocs v5 — Complete Overhaul

## Overview

Rewrite the ETUS PMDocs framework from v4.1 to v5.0, implementing everything identified across 4 design documents and the competitive analysis of 5+ frameworks (BMAD, Superpowers, Compound Engineering, GitHub Spec Kit, PM Skills).

**Three pillars of change:**
1. **Interaction overhaul** — Fix how ALL 21 skills interact with users (1 question at a time, 3-4 suggestions, approaches, approval gates)
2. **4-mode system** — Support Product, Feature, Bug/Hotfix, and Spike/Research work items with right-sized documentation
3. **Structural improvements** — Knowledge capture, adversarial review, named agents, help system, plugin distribution

## Problem Statement / Motivation

ETUS PMDocs v4.1 works but has critical UX and scope problems:
- Skills ask questions in blocks of 2-3 instead of one at a time — overwhelming the user
- Skills never propose alternative approaches — they jump straight to generating
- Skills don't ask for user approval before saving — they dump the full document
- The framework only supports "new product" — can't document a single feature, bug fix, or spike
- No learning capture between projects — same mistakes repeat
- No scale-adaptive routing — a 1-day bug fix requires the same 70-minute, 21-doc pipeline as a 6-month product
- Skills use heavy-handed "MUST/NEVER" tone instead of explaining WHY (against Anthropic best practices)

## Proposed Solution

### Phase 1: Interaction Pattern Overhaul (ALL 21 generator skills)

Rewrite the interaction logic of every generator skill to follow the patterns proven by Superpowers and Compound Engineering. This is the foundation — everything else builds on skills that interact well.

### Phase 2: 4-Mode System + New Artifacts

Add mode detection to the orchestrator and create 3 new lightweight pipelines (Feature, Bug, Spike) with their templates and relaxed dependency chains.

### Phase 3: Structural Improvements

Add knowledge capture, adversarial review, named agents, help system, and plugin packaging.

## Technical Considerations

- All changes are to `.claude/skills/*/SKILL.md` files (markdown, not code)
- Templates are in `.claude/skills/*/knowledge/template.md`
- Agent definitions are in `.claude/agents/*.md`
- Orchestrator is in `.claude/skills/orchestrator/SKILL.md`
- No external dependencies — pure Claude Code skill framework
- Must maintain backward compatibility (existing `docs/ets-docs/` structure unchanged for Product mode)

## System-Wide Impact

- **All 21 generator skills** get interaction overhaul
- **Orchestrator** gets mode detection router
- **7 agents** get named personalities
- **3 new templates** for Feature/Bug/Spike artifacts
- **New directories**: `docs/ets-docs/features/`, `docs/ets-docs/bugs/`, `docs/ets-docs/spikes/`, `docs/ets-docs/learnings/`
- **CLAUDE.md** must be updated to document v5 architecture

## Acceptance Criteria

### Phase 1: Interaction Overhaul
- [ ] Every generator skill asks exactly 1 question per message (not blocks)
- [ ] Every choice question offers 3-4 concrete suggestions with recommendation
- [ ] Every skill proposes 2-3 approaches with tradeoffs before deciding direction
- [ ] Every skill presents output section-by-section for user approval before saving
- [ ] Every skill tracks outstanding questions (blocks-planning vs deferred)
- [ ] Every skill offers multiple next-step options at handoff (not just one fixed path)
- [ ] Every skill uses `AskUserQuestion` tool when available
- [ ] Tone rewritten: WHY explanations replace heavy-handed MUSTs
- [ ] Descriptions optimized for CSO (trigger conditions only, no workflow summaries)

### Phase 2: 4-Mode System
- [ ] Orchestrator detects mode from trigger phrases, commands, or explicit flag
- [ ] `/feature` command works standalone — generates 3-5 docs without upstream deps
- [ ] `/bugfix` command generates single tech-spec-{slug}.md
- [ ] `/spike` command generates single spike-{slug}.md
- [ ] Feature mode relaxes BLOCKS → ENRICHES for project-context/product-vision
- [ ] Output Validation thresholds adjust per mode (lower for Feature/Bug/Spike)
- [ ] Auto-escalation: Feature mode suggests Product mode if scope grows
- [ ] New templates exist for feature-brief, design-delta, tech-spec-standalone, spike

### Phase 3: Structural Improvements
- [ ] Knowledge capture skill writes to `docs/ets-docs/learnings/`
- [ ] Adversarial review mode in validate-gate (min 5 findings before GO)
- [ ] All 7 agents have displayName, identity, communicationStyle
- [ ] etus-help skill detects project state and recommends next step
- [ ] CLAUDE.md updated for v5 (modes, new commands, new structure)

## Implementation Phases

### Phase 1: Interaction Pattern Overhaul (21 skills)

**Scope:** Rewrite the interaction sections of ALL 21 generator skills.

**Pattern to apply to EVERY skill:**

```markdown
## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard:

1. **One question per message** — Never batch multiple questions. Ask one, wait for answer, then ask the next. Use AskUserQuestion tool when available.

2. **Suggest 3-4 options for choices** — When the user needs to choose a direction, present 3-4 concrete options with your recommendation highlighted. Explain tradeoffs briefly.

3. **Propose approaches before deciding** — Before generating any content, propose 2-3 approaches with pros/cons. Let the user choose the direction.

4. **Present output section-by-section** — Don't dump the full document. Present each major section, ask "Does this look right?", and only proceed after approval.

5. **Track outstanding questions** — If a question can't be answered now:
   - "Resolve before next phase" → blocks handoff
   - "Deferred to [phase]" → noted, carried forward

6. **Multiple handoff options** — At completion, present 3-4 next-step options (proceed, refine, review, pause) instead of a single fixed path.
```

**Per-skill work:**

#### 1.1 Discovery Skills (2 skills)

**project-context** (`discovery/project-context/SKILL.md`):
- [ ] Rewrite INTERVIEW PROTOCOL: Change from 7 question blocks to 1-question-at-a-time flow
- [ ] Each 5W2H question gets its own message with probes as follow-ups
- [ ] Add scope assessment (Phase 0): "Is this a new product, feature, or exploration?"
- [ ] Add approach proposals after WHAT/WHY questions: "Based on what you described, I see 3 possible framings..."
- [ ] Add section-by-section approval before saving
- [ ] Add outstanding questions tracking
- [ ] Rewrite handoff: multiple options (proceed to vision, refine context, pause)
- [ ] Soften tone: replace MUSTs with WHY explanations

**product-vision** (`discovery/product-vision/SKILL.md`):
- [ ] Rewrite VISION INTERVIEW PROTOCOL: 1 question per message (not 4 blocks of 2-3)
- [ ] Add approach proposals before BO-# generation: "I see 3 strategic directions for this product..."
- [ ] BMAD brainstorm: present technique options as 3-4 suggestions with recommendation
- [ ] HMW transformation: present each HMW for approval individually
- [ ] Section-by-section approval (vision → BOs → personas → value prop → competitive → HMW)
- [ ] Outstanding questions: "Resolve before Planning" vs "Deferred to Planning"
- [ ] Handoff: multiple options (proceed to gate, refine vision, run another technique, pause)
- [ ] Soften tone

#### 1.2 Planning Skills (3 skills)

**prd** (`planning/prd/SKILL.md`):
- [ ] Rewrite feature brainstorm: 1 question at a time
- [ ] MoSCoW prioritization: present features 1 by 1 with suggested priority and 3-4 options (Must/Should/Could/Won't)
- [ ] Propose 2-3 scope approaches: "minimal MVP" vs "balanced" vs "ambitious"
- [ ] Section-by-section approval
- [ ] Outstanding questions tracking
- [ ] Handoff: multiple options (proceed to stories, refine PRD, review, pause)

**user-stories** (`planning/user-stories/SKILL.md`):
- [ ] Per-story generation: present each US-# for approval before next
- [ ] Given/When/Then: propose 2-3 acceptance criteria options per story
- [ ] Edge cases: suggest 2-3 edge cases for each Must Have story, ask which to include
- [ ] Outstanding questions tracking
- [ ] Handoff options

**feature-spec** (`planning/feature-spec/SKILL.md`):
- [ ] State machine: propose 2-3 state models, let user choose
- [ ] Business rules: present each FS-# rule for approval
- [ ] Edge cases: suggest explicitly, ask which are relevant
- [ ] Handoff options

#### 1.3 Architecture Skills (2 skills)

**architecture-diagram** (`architecture/architecture-diagram/SKILL.md`):
- [ ] Tech stack: propose 3-4 options per layer (frontend, backend, DB, infra) with tradeoffs
- [ ] Architecture style: propose 2-3 approaches (monolith, modular monolith, microservices)
- [ ] C4 diagrams: present each level for approval before going deeper
- [ ] Handoff options

**tech-spec** (`architecture/tech-spec/SKILL.md`):
- [ ] NFRs: propose targets with 3 tiers (minimum, recommended, stretch) for each
- [ ] ADRs: present each decision with 2-3 alternatives and tradeoffs, user picks
- [ ] Section-by-section approval
- [ ] Handoff options

#### 1.4 Data Design Skills (6 skills)

**data-requirements** (`data-design/data-requirements/SKILL.md`):
- [ ] Entity identification: propose entity list, ask "Any missing? Any to remove?"
- [ ] Data sources: suggest 3-4 options per source type
- [ ] Volume estimates: propose ranges, ask user to calibrate

**erd** (`data-design/erd/SKILL.md`):
- [ ] Relationship decisions: ask 1 at a time — "User → Project: 1:N or M:N?"
- [ ] Key strategy: propose UUID vs auto-increment with tradeoffs
- [ ] Present diagram for approval before proceeding

**database-spec** (`data-design/database-spec/SKILL.md`):
- [ ] Engine choice: propose 3-4 options (PostgreSQL, MySQL, SQLite, etc.) with tradeoffs
- [ ] Indexing strategy: propose per-table, ask approval
- [ ] Soft delete vs hard delete: propose with tradeoffs
- [ ] Present DDL section-by-section

**data-dictionary** (`data-design/data-dictionary/SKILL.md`):
- [ ] Field definitions: present per-entity for approval
- [ ] Event definitions: suggest events based on user stories, ask which to track
- [ ] Validation rules: propose per-field, ask confirmation

**data-flow-diagram** (`data-design/data-flow-diagram/SKILL.md`):
- [ ] Flow identification: propose flows, ask if complete
- [ ] Timing: ask per-flow — "Batch or real-time? Why?"
- [ ] Present diagram for approval

**data-catalog** (`data-design/data-catalog/SKILL.md`):
- [ ] Classification: propose per-entity (PII, sensitive, public), ask confirmation
- [ ] Retention: propose policies with 3 options per data type
- [ ] Ownership: ask per-dataset

#### 1.5 UX Design Skills (4 skills)

**user-journey** (`ux-design/user-journey/SKILL.md`):
- [ ] Journey identification: propose 2-3 key journeys, ask which to map first
- [ ] Per-step: present touchpoint, emotion, pain point — ask approval
- [ ] Edge cases: suggest alternative paths, ask which matter

**ux-sitemap** (`ux-design/ux-sitemap/SKILL.md`):
- [ ] Navigation: propose 2-3 IA structures (flat, hierarchical, hub-spoke)
- [ ] Page grouping: present proposed hierarchy for approval
- [ ] Present diagram

**wireframes** (`ux-design/wireframes/SKILL.md`):
- [ ] Layout: propose 2-3 layouts per key screen with tradeoffs
- [ ] Component choices: suggest options (tabs vs sidebar, cards vs list)
- [ ] Present each wireframe for approval individually
- [ ] Responsive: ask about breakpoint priorities

**style-guide** (`ux-design/style-guide/SKILL.md`):
- [ ] Color palette: propose 3-4 palette options with rationale
- [ ] Typography: propose 2-3 font combinations
- [ ] Spacing system: propose scale (4px, 8px base)
- [ ] Tokens: present per-category for approval

#### 1.6 API Design (1 skill)

**api-spec** (`api-design/api-spec/SKILL.md`):
- [ ] API style: propose REST vs GraphQL vs gRPC with tradeoffs
- [ ] Auth strategy: propose 3-4 options (JWT, API key, OAuth2, mTLS)
- [ ] Per-endpoint: present for approval before next
- [ ] Error format: propose standards, ask preference
- [ ] Versioning: propose strategies (URL, header, content-type)

#### 1.7 Implementation Skills (3 skills)

**implementation-plan** (`implementation/implementation-plan/SKILL.md`):
- [ ] Sprint duration: propose 1-week vs 2-week with tradeoffs
- [ ] Task decomposition: present per-story, ask about estimates
- [ ] Risk identification: propose risks, ask severity assessment
- [ ] Team allocation: ask 1 question at a time about capacity

**sprint-status** (`implementation/sprint-status/SKILL.md`):
- [ ] Sprint scope: propose task selection for sprint, ask approval
- [ ] Velocity: propose baseline, ask calibration
- [ ] Blockers: ask per-task

**quality-checklist** (`implementation/quality-checklist/SKILL.md`):
- [ ] Coverage targets: propose 3 tiers (minimum, recommended, stretch)
- [ ] Security requirements: propose based on tech-spec, ask which apply
- [ ] Accessibility: propose WCAG level (A, AA, AAA) with tradeoffs
- [ ] Performance benchmarks: propose based on NFRs, ask calibration

---

### Phase 2: 4-Mode System

#### 2.1 Mode Detection Router

**File:** `.claude/skills/orchestrator/SKILL.md` (update)

- [ ] Add `## MODE DETECTION` section at the top of the orchestrator
- [ ] Detection logic:
  1. Explicit command: `/start-project` → Product, `/feature` → Feature, `/bugfix` → Bug, `/spike` → Spike
  2. Trigger phrases: "fix bug" → Bug, "new feature" → Feature, "investigate" → Spike
  3. Context: if `project-context.md` exists + user asks about specific feature → Feature
  4. Fallback: Ask user "Is this a new product, feature, bug fix, or research?"
- [ ] Mode stored in `.handoff/mode.json`
- [ ] Each mode defines: which skills run, which are skipped, dependency relaxation, validation thresholds

#### 2.2 New Commands

- [ ] Create `.claude/commands/feature.md` — Feature mode entry point
- [ ] Create `.claude/commands/bugfix.md` — Bug mode entry point
- [ ] Create `.claude/commands/spike.md` — Spike mode entry point

#### 2.3 New Templates

**feature-brief-{slug}.md** (`.claude/skills/planning/feature-brief/`):
- [ ] Create SKILL.md — Problem, scope, personas affected, acceptance criteria
- [ ] Create knowledge/template.md — Lightweight PRD replacement
- [ ] No upstream BLOCKS (standalone)
- [ ] IDs: FB-# (Feature Brief items)

**design-delta-{slug}.md** (`.claude/skills/architecture/design-delta/`):
- [ ] Create SKILL.md — Only what changes: new endpoints, DB migrations, UI changes
- [ ] Create knowledge/template.md — Delta format (not full architecture)
- [ ] ENRICHES: architecture-diagram.md, tech-spec.md (if they exist)

**tech-spec-standalone-{slug}.md** (Bug mode):
- [ ] Create SKILL.md — Problem, root cause, fix plan, test plan, rollback plan
- [ ] Create knowledge/template.md — Single-doc bug spec
- [ ] No upstream dependencies

**spike-{slug}.md** (Spike mode):
- [ ] Create SKILL.md — Question, methodology, findings, options, recommendation
- [ ] Create knowledge/template.md — Research output format
- [ ] BMAD CIS techniques available

#### 2.4 Output Directory Structure

- [ ] Create `docs/ets-docs/features/` directory
- [ ] Create `docs/ets-docs/bugs/` directory
- [ ] Create `docs/ets-docs/spikes/` directory
- [ ] Update orchestrator to route output to correct directory per mode

#### 2.5 Dependency Relaxation Per Mode

- [ ] Update dependency-graph.yaml with mode-aware rules
- [ ] Feature mode: project-context → ENRICHES (not BLOCKS)
- [ ] Feature mode: product-vision → ENRICHES (not BLOCKS)
- [ ] Bug mode: no BLOCKS dependencies
- [ ] Spike mode: no BLOCKS dependencies
- [ ] Auto-escalation: Feature mode detects scope growth → suggests Product mode

#### 2.6 Validation Thresholds Per Mode

- [ ] Update validate-gate to accept mode parameter
- [ ] Feature mode: US-# ≥1 (not ≥5), acceptance criteria ≥1 per story (not ≥3)
- [ ] Bug mode: problem described + fix approach + test plan present
- [ ] Spike mode: question + findings + recommendation present

---

### Phase 3: Structural Improvements

#### 3.1 Knowledge Capture (Phase 5: Retrospective)

- [ ] Create `.claude/skills/retrospective/project-retrospective/SKILL.md`
- [ ] Template: what worked, what didn't, patterns discovered, decisions that paid off/backfired
- [ ] IDs: LEARN-# with tags (architecture, ux, data, process, etc.)
- [ ] Output: `docs/ets-docs/learnings/retro-{project-slug}.md`
- [ ] Create `.claude/agents/learnings-researcher.md` — searches learnings/ during Phase 1
- [ ] Integrate learnings-researcher into discovery-agent workflow

#### 3.2 Adversarial Review

- [ ] Update validate-gate SKILL.md: add `--adversarial` mode
- [ ] When adversarial: reviewer MUST find minimum 5 issues before recommending GO
- [ ] Findings categorized: HIGH (blocks GO), MEDIUM (should fix), LOW (informational)
- [ ] Zero findings triggers re-analysis
- [ ] Integrate into orchestrator: auto-run adversarial before Implementation Readiness Gate

#### 3.3 Named Agents with Personality

- [ ] Update all 7 agent .md files with YAML frontmatter:
  - `displayName`: Human name
  - `icon`: Emoji
  - `identity`: Background statement
  - `communicationStyle`: How they interact
  - `principles`: Core values
- [ ] Suggested names: discovery→Luna, planning→Atlas, architecture→Blueprint, data→Cipher, ux→Canvas, api→Gateway, implementation→Forge

#### 3.4 etus-help Skill

- [ ] Create `.claude/skills/help/etus-help/SKILL.md`
- [ ] Reads `.handoff/phase.json` to detect current state
- [ ] Scans `docs/ets-docs/` for existing artifacts
- [ ] Recommends next step with command
- [ ] Handles: "Where am I?", "What's next?", "What modes exist?", "Help"

#### 3.5 CLAUDE.md Update

- [ ] Document v5 architecture (4 modes, new commands, new directories)
- [ ] Document new commands (/feature, /bugfix, /spike, /help)
- [ ] Document interaction protocol (1 question, suggestions, approaches, approval)
- [ ] Update skill count, agent count, document count
- [ ] Add mode detection trigger phrases table

#### 3.6 Plugin Distribution

- [ ] Create `.claude-plugin/plugin.json` with metadata
- [ ] Write public README.md for marketplace
- [ ] Test installation via `/plugin install`
- [ ] Version: 5.0.0

## Alternative Approaches Considered

1. **Incremental patching** — Fix skills one by one without modes. Rejected: doesn't solve the "70min for a bug fix" problem.
2. **Separate plugins per mode** — One plugin for Product, one for Feature, etc. Rejected: fragments the experience and duplicates shared skills.
3. **Marketing-specific skills** — Create campaign-brief, creative-strategy, etc. Rejected by user: the plugin is a PM tool, not a marketing execution tool. Marketing is the domain context, not the output type.

## Dependencies & Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Rewriting 21 skills introduces regressions | High | High | Test each skill manually after rewrite; run validate-gate on sample project |
| Mode detection misroutes user intent | Medium | Medium | Fallback always asks user; explicit commands override detection |
| Interaction overhaul makes skills too long (>500 lines) | Medium | Low | Use progressive disclosure — move detailed protocols to knowledge/ files |
| Named agents feel gimmicky | Low | Low | Keep personalities subtle and professional |

## Success Metrics

- **Interaction quality:** Zero instances of "block of 3 questions" in any skill
- **Mode coverage:** All 4 modes functional and independently invocable
- **Time-to-doc:** Bug mode completes in <10min; Feature mode in <20min; Product mode unchanged (~70min)
- **User satisfaction:** User can complete a feature-brief without being asked to create product-vision first

## Sources & References

### Origin Documents

- **Framework comparison:** [docs/design/framework-comparison-and-mode-proposal.md](../../design/framework-comparison-and-mode-proposal.md) — 4-mode system, per-skill behavior matrix
- **Improvement report:** [docs/improvement-report-v5.md](../improvement-report-v5.md) — 36 improvements, gap analysis, competitive benchmarking
- **Discovery analysis:** [docs/design/discovery-methodology-analysis.md](../../design/discovery-methodology-analysis.md) — Interaction patterns from Superpowers/BMAD
- **Architecture proposal:** [docs/design/solo-templates-skill-architecture-proposal.md](../../design/solo-templates-skill-architecture-proposal.md) — v4 architecture decisions

### External References

- [Agent Skills Specification (agentskills.io)](https://agentskills.io/specification) — SKILL.md < 500 lines, progressive disclosure, WHY > MUST
- [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Theory of mind, eval-driven development
- [Superpowers brainstorming SKILL.md](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) — Checklist-driven, 1 question/time, spec review loop
- [Compound Engineering ce:brainstorm](https://github.com/EveryInc/compound-engineering-plugin) — 4-phase flow, scope assessment, outstanding questions
- [PM Skills (phuryn)](https://github.com/phuryn/pm-skills) — 13 atomic discovery skills, existing vs new separation
- [BMAD v6 Quick Flow](https://docs.bmad-method.org/explanation/quick-flow/) — Scale-adaptive routing, auto-escalation
