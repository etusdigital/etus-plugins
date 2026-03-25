# Audit v4: ETUS PMDocs — Elicitation, Coverage, Brainstorm e Developer Handoff

**Date:** 2026-03-24
**Framework version:** v5.3
**Base:** Direct source code reading (9 agents, 45 skills, 13 commands, 5 gates, 6 hooks, state_defaults.py, coverage-matrix.yaml, all templates) + v3-AA strategic audit + v3-Claude code-grounded audit + external research (GOV.UK, NNGroup, IDEO, Product Talk, Google Design Sprint)
**Objective:** Make the ETUS framework exceptional at extracting product ideas from the PO's head — leaving zero gaps — and producing documentation that lets a developer implement without guessing.

---

## Central Thesis

The ETUS PMDocs framework already has the right conceptual architecture: ideation before specification, upstream coverage via actors/JTBDs/journeys/use-cases/edge-cases/assumptions, a traceability chain (`BO-# → PRD-F-# → US-# → FS-# → impl-#`), SST enforcement, gates per phase, and 4-mode workflows. This puts the framework ahead of most product documentation approaches.

The core problem is one sentence:

> **The ETUS is prompt-rich and enforcement-poor.**

Meaning: the right rules exist as text inside skills, agent instructions, and templates — but not as persistent state, progression blockers, validators, or operational artifacts. A seemingly "good" interview can still skip essential question types, accept vague answers, mark coverage without sufficiency, and advance through fatigue or haste.

The evolution the ETUS needs is not "more documents." It needs:

1. A story-based interview method that extracts concrete behavior instead of abstract opinions
2. An interview state machine that tracks where the conversation stopped and what quality was achieved
3. Semantic coverage that measures substance instead of counting items
4. Disciplined brainstorming that separates divergence from convergence
5. Executable validation that mechanically catches placeholders and vagueness
6. A consolidated developer handoff that respects SST

---

## System Architecture: 5 Layers

Every recommendation in this audit maps to exactly one layer. This makes it clear where each improvement acts and what it protects against.

### Layer 1 — Core Interview (extraction quality)

Skills: `ideate`, `discover`, `project-context`, `product-vision`, `feature-brief`

This is where ideas leave the PO's head and enter the system. If this layer fails, everything downstream is built on thin air. This layer must optimize for: truth, concrete behavior, real context, friction, impact, and constraints.

### Layer 2 — Structured Brainstorm (idea transformation)

Skills: `brainstorm` module inside `ideate`, `solution-discovery`

This layer does not extract the raw problem — it transforms evidence into testable directions. If discovery fails, brainstorm becomes guesswork. If brainstorm fails, the solution becomes premature fixation.

### Layer 3 — Translation (specification fidelity)

Skills: `feature-brief`, `prd`, `user-stories`, `feature-spec`

This layer does not discover — it translates. The quality of discovery and brainstorm must survive here without degradation.

### Layer 4 — Assurance (ambiguity detection)

Skills: `validate-gate`, `check-traceability`, `check-sst`, new validators

This layer does not create — it prevents ambiguities from escaping. Must be mechanical, not opinion-based.

### Layer 5 — Change & Continuity (drift protection)

Skills: `correct-course`, state/handoffs, post-implementation feedback

This layer protects the framework from drift after scope changes and enables continuous learning. Currently the most underdeveloped layer in the ETUS.

---

## What Already Works (Preserve)

**1. The ideation macro-sequence is correct.**
`ingest → problem → actors → jobs → journeys → cases → edges → assumptions → brainstorm → synth` — coverage before creativity. Do not change the order.

**2. Anti-requirements exist as seeds.**
The feature-brief (Q4: "What is this feature explicitly NOT doing?") and the opportunity-pack ("Constraints & Guardrails" → "what must NOT get worse") already capture what not to do. The problem is not absence of intention — it's absence of first-class enforcement.

**3. Traceability chain is a real competitive advantage.**
`BO-# → PRD-F-# → US-# → FS-# → impl-#` with automated validation. Keep and extend.

**4. Pressure test in feature-brief has good instinct.**
4 challenge questions: "Is this the right problem?", "What happens if we do nothing?", "Is there a better framing?", "Are we building for the right user?" — needs more mechanical enforcement.

**5. Coverage matrix with traceable IDs.**
`ACT-#`, `JTBD-#`, `JOUR-#`, `UC-#`, `EDGE-#`, `ASM-#` with status tracking and downstream linkage. The infrastructure exists.

**6. Contradiction register.**
"If sources disagree, record the contradiction instead of silently resolving it." Correct intention. Needs mechanics.

**7. Solution discovery with 4 risks.**
Value, Usability, Viability, Feasibility — correct framework for evaluating solutions before committing to requirements.

**8. Validate-gate 3-layer architecture.**
Structure → Content → Dependencies. Right architecture. Needs stronger criteria in Layer 2.

---

## Diagnostics

### D1 — Interview method produces abstract answers

**Evidence from code:**

The ideate skill Problem Framing module asks: "What is the proposed solution?", "What is the underlying problem?", "What happens if we do nothing?", "Is the stated problem a symptom or a root problem?"

The discovery-agent does 5W2H: "What is the problem/opportunity?", "Who are the users/stakeholders?"

The feature-brief Q1 asks: "What feature are you documenting?"

These are all abstract questions that ask for opinions and hypotheses. Product Talk, NNGroup, and GOV.UK converge on the same finding: the best discovery interviews are **story-based and past-focused**. Instead of "What is the problem?", ask "Tell me about the last time this happened. What happened? Who was involved? What went wrong? What did you do next?"

Answers about the past are more concrete, more detailed, and reveal context that abstract questions cannot capture. When someone tells a real story, workarounds emerge, hidden actors appear, and pain points surface that the PO didn't know mattered.

**Analogy:** Asking "What's the problem?" is like a doctor asking "What's wrong with you?" Asking "Tell me what happened" is like asking "When did it start? What did you feel? What did you do?" — the second approach produces a better diagnosis.

### D2 — Coverage measures quantity, not substance

**Evidence from code:**

`coverage-matrix.yaml` thresholds: `actors >= 2, jtbd >= 2, journeys >= 2, use_cases >= 4, edge_cases >= 3, assumptions >= 3` for Product mode. The readiness gate checks booleans: `problem_defined: false`, `actors_identified: false`, etc.

3 edge cases about "empty field" are worth less than 1 edge case about "what happens when the payment service fails mid-transaction." The count passes, the substance does not.

The right question for implementation is: did we cover the right dimensions for this type of problem? Not: do we have enough items?

### D3 — Coverage state and interview state are conflated

**Evidence from code:**

`coverage-matrix.yaml` tries to track both what is covered (semantic coverage) and where the interview is (step_status, active_step, last_completed_step). These are two different concerns. If the interview pauses and resumes, the agent doesn't know which specific probe it was on within a module. If coverage is met but through low-quality answers, nothing detects it.

### D4 — Discovery and brainstorm need different dynamics

Discovery should optimize for: truth, context, real behavior, concrete friction, impact, constraints.

Brainstorm should optimize for: option breadth, structure, clustering, disciplined selection, assumption surfacing, test planning.

Today the ETUS suggests this separation but doesn't execute it with enough rigor. The brainstorm module says: "BMAD technique selection → candidate solution directions → risk discovery → stress test of the preferred direction" — mixing idea generation with immediate evaluation. IDEO and Design Sprint are clear: divergence and convergence are different modes that must not be mixed.

### D5 — Developer gets 10+ documents and assembles the puzzle alone

No consolidated artifact says: "here is everything you need to implement this feature, in one place." The dev navigates opportunity-pack, feature-brief, user-stories, design-delta, tech-spec, api-spec, data-dictionary to assemble the complete picture.

**Critical SST constraint:** The handoff packet cannot become a new source of truth. It must be derived, generated, regenerable, and non-authoritative. Each section must point to its authority: rules → feature-spec, acceptance criteria → user-stories, contracts → api-spec, data semantics → data-dictionary, NFRs → tech-spec. The packet summarizes and consolidates but does not redefine.

### D6 — Scope change is the most underdeveloped area

The framework is relatively sophisticated for: extracting, structuring, generating, validating. But it is weak for: propagating changes, preserving rejections, remembering user objections, updating connected docs. This is a clear P0-late / P1 area.

---

## Recommendations

### R1. Separate `coverage-matrix.yaml` and `elicitation-state.yaml`

**Problem:**
Previous proposals pushed too much responsibility onto `coverage-matrix.yaml` — mixing interview execution state (where the conversation stopped, response quality, fatigue signals) with semantic coverage (which dimensions are covered, which IDs exist, readiness gate). This creates a confusing YAML with two responsibilities.

**What to do:**

Create two distinct artifacts:

**A. `coverage-matrix.yaml` — Semantic coverage (what is covered)**

Responsible for: upstream IDs, semantic dimensions (R5), archetype dimensions, blockers, readiness gate.

**B. `elicitation-state.yaml` — Interview execution (how the conversation is going)**

```yaml
# elicitation-state.yaml

meta:
  mode: product
  session_id: "2026-03-24-001"
  started_at: "2026-03-24T10:00:00Z"
  last_activity: "2026-03-24T11:30:00Z"

current_module: actors
current_probe: "Na história que você contou, quem mais estava envolvido?"
questions_asked: 12
stories_collected: 3

module_state:
  ingest:
    status: covered
    questions_asked: 2
  problem:
    status: covered
    questions_asked: 4
    stories_collected: 2
    snapshots: [SNAP-1, SNAP-2]
  actors:
    status: in_progress
    questions_asked: 3
    stories_collected: 1
    archetype_probes_done: false
    snapshots: [SNAP-3]
  jobs:
    status: not_started
  journeys:
    status: not_started
  cases:
    status: not_started
  edges:
    status: not_started
  assumptions:
    status: not_started
  brainstorm:
    status: blocked
    blocked_by: "Minimum coverage not met"
  synth:
    status: not_started

response_quality:
  vague_count: 2
  escalated_count: 2
  "dont_know_count": 1
  "dont_know_classified": 1

fatigue:
  threshold: 15
  current: 12
  offered_pause: false

checkpoints:
  - snapshot: SNAP-1
    after_question: 3
    module: problem
    validated_by_user: true
  - snapshot: SNAP-2
    after_question: 5
    module: problem
    validated_by_user: true
  - snapshot: SNAP-3
    after_question: 10
    module: actors
    validated_by_user: false
```

**Entry rule for every sub-skill:**

```
BEFORE asking anything:
1. Read elicitation-state.yaml
2. Find the corresponding module
3. If status == "covered" → summarize what exists, ask if user wants to go deeper
4. If status == "in_progress" → continue from current_probe
5. If status == "not_started" → start with story probe (R2)
6. After each question → update elicitation-state.yaml
```

**Files to change:**
- `.claude/skills/discovery/ideate/knowledge/` — create `elicitation-state.yaml` template
- `.claude/skills/discovery/ideate/SKILL.md` — add entry rule referencing both files
- Each sub-skill (jtbd-extractor, journey-sweep, edge-case-sweep, use-case-matrix, assumption-audit) — add state read/write

**Files to keep:**
- `coverage-matrix.yaml` — strip interview execution fields, keep only IDs, counts, thresholds, semantic dimensions, readiness gate

**Effort:** ~150 lines (new template + integration)

**Priority:** P0
**Layer:** 1

---

### R2. Story-based interviewing as the primary extraction method

**Evidence from code:**

The ideate skill (Problem Framing) asks: "What is the proposed solution?", "What is the underlying problem?", "What happens if we do nothing?". The discovery-agent does 5W2H: "What is the problem/opportunity?", "Who are the users/stakeholders?". The feature-brief asks: "What feature are you documenting?"

All abstract questions that produce abstract answers.

**What to do:**

Rewrite extraction prompts in 4 skills to use story-first:

| Skill | Current prompt | Story-based prompt |
|---|---|---|
| ideate (Problem Framing) | "What is the underlying problem?" | "Tell me about the last time this problem happened. What happened? Who was involved? What went wrong?" |
| ideate (Actor Map) | "Who feels the pain directly?" | "In the story you told me, who else was involved? Who approved? Who was affected even without participating?" |
| jtbd-extractor | "What job is this person trying to get done?" | "Before thinking about the solution: what was this person trying to do at that moment? What would make them say 'it was worth it'?" |
| feature-brief (Q1) | "What feature are you documenting?" | "Tell me about a concrete situation where the user would need this feature. What did they try to do? Where did they get stuck?" |

Create a shared knowledge file with 5 reusable story probes:

```markdown
# .claude/skills/discovery/knowledge/story-probes.md

## Core Story Probes (use one at a time, in order)

1. "Tell me about the last time this happened."
   - Sufficient when: answer includes who, what, when, and outcome
   - Insufficient when: answer is generic or hypothetical

2. "Walk me through step by step what happened."
   - Sufficient when: steps are concrete and sequential
   - Insufficient when: skips steps or generalizes

3. "What happened next?"
   - Use when: the story stopped in the middle

4. "Can you give me another example?"
   - Use when: need a pattern (1 story = anecdote, 2+ = pattern)

5. "Why was that important to you?"
   - Use at the end of the story, not at the beginning
```

**Files to change:**
- `.claude/skills/discovery/ideate/SKILL.md` — rewrite modules 2, 3, 4 for story-first
- `.claude/skills/discovery/jtbd-extractor/SKILL.md` — rewrite EXTRACTION PROMPTS
- `.claude/skills/planning/feature-brief/SKILL.md` — rewrite Q1-Q3
- `.claude/agents/discovery-agent.md` — rewrite "Problem Interview" section
- Create `.claude/skills/discovery/knowledge/story-probes.md` (new)

**Effort:** ~180 lines (rewrite) + ~30 lines (new file) = ~210 lines

**Priority:** P0
**Layer:** 1

---

### R3. Interview Snapshots — Micro-artifacts for immediate synthesis

**Problem:**
Today, ideation captures information directly in opportunity-pack.md. The entire conversation is distilled into one document at the end. Details, quotes, and context are lost between the conversation and the synthesis.

**What the research shows:**
IDEO recommends "download your learnings" immediately after each interview. Product Talk recommends "interview snapshots" that capture: key context, memorable quote, experience map, opportunities, and insights — right after each story, not at the end of the process.

**What to do:**

Add a new section to the opportunity-pack template between "Evidence Register" and "Actor Map":

```markdown
## Story Snapshots

### SNAP-1: [descriptive title of the story]
- **Who told it:** [PO / stakeholder / observed user]
- **Context:** [when it happened, what circumstance]
- **What happened:** [narrative in 3-5 sentences]
- **Key quote:** "[most revealing phrase, verbatim]"
- **What went wrong:** [concrete pain point]
- **Current workaround:** [what the person does today]
- **Detected opportunity:** [O-# if applicable]
- **IDs fed:** ACT-#, JTBD-#, JOUR-#, UC-#, EDGE-# extracted from this story
```

**Operation rule:** After each extracted story (R2), the agent generates the snapshot and asks: "Does this summary capture what you told me? Anything I got wrong?"

This is the reflection checkpoint — not arbitrary every N questions, but anchored in each unit of information (story).

**Files to change:**
- `.claude/skills/discovery/ideate/knowledge/template.md` — add Story Snapshots section
- `.claude/skills/discovery/ideate/SKILL.md` — add instruction to generate snapshot after each story
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml` — add `snapshots: []` with SNAP-# IDs

**Effort:** ~60 lines

**Priority:** P0
**Layer:** 1

---

### R4. Separate divergence and convergence in brainstorm

**Evidence from code:**

The "Solution Direction Brainstorm" module in ideate says: "BMAD technique selection → candidate solution directions → risk discovery → stress test of the preferred direction." This mixes idea generation with immediate evaluation.

The discovery-agent offers 4 techniques (Mind Mapping, HMW, Scenario Planning, JTBD) and asks the user to pick one.

**What the research shows:**

IDEO and Design Sprint are clear: divergence and convergence are different modes. When you criticize ideas while generating them, you kill generation. The correct sequence is: Themes → HMW → Diverge → Cluster → Select → Stress Test → Assumptions.

HMW is in the wrong place. Today it's mentioned in the PRD as a prioritization technique and in the discovery-agent as a brainstorm option. But it's not used as the **bridge between discovery and brainstorm** — which is its strongest use.

**What to do:**

Rewrite the brainstorm module in ideate with explicit phases:

```markdown
### 10. Solution Direction Brainstorm

#### Prerequisite
Brainstorm is BLOCKED until:
- Problem defined
- >= 1 actor
- >= 1 JTBD
- >= 1 journey
- >= 3 story snapshots

#### Phase A: Themes (convergence over evidence)
- Group story snapshots by theme
- Present grouping to user: "I see 3 themes: [X], [Y], [Z]. Does this make sense?"

#### Phase B: HMW Bridge
- For each theme, generate 2-3 HMW statements
- Ex: "How might we [reduce approval time] without [compromising the audit trail]?"
- User selects the most relevant HMWs

#### Phase C: Diverge (no judgment)
- For each selected HMW, generate 3-5 options
- Rule: DO NOT criticize, DO NOT evaluate, DO NOT say "but"
- Build on ideas ("what if also...", "what if instead...")

#### Phase D: Cluster & Select
- Group similar ideas
- User selects 2-3 directions to deepen

#### Phase E: Stress Test (convergence)
- For each direction: tradeoffs, risks, what can go wrong
- Evaluate against the 4 risks: value, usability, viability, feasibility

#### Phase F: Assumptions
- For each direction: "What needs to be true for this to work?"
- Register as ASM-# with risk level and validation path
- Connect to solution-discovery downstream
```

**Initial recommended techniques (keep it small):**
- HMW + clustering (always)
- Crazy 8s (for Phase C divergence)
- Gut Check (for Phase D selection)

Leave as future expansion: mash-ups, role play, reverse brainstorming, six thinking hats.

**Files to change:**
- `.claude/skills/discovery/ideate/SKILL.md` — rewrite module 10
- `.claude/agents/discovery-agent.md` — rewrite "Creative Exploration" section
- `.claude/skills/discovery/ideate/knowledge/template.md` — expand "Solution Directions" to include themes, HMWs, raw ideas, clusters, assumptions

**Effort:** ~120 lines (rewrite) + ~40 lines (template) = ~160 lines

**Priority:** P0
**Layer:** 2

---

### R5. Semantic coverage dimensions instead of counting

**Evidence from code:**

Thresholds: `actors >= 2, jtbd >= 2, journeys >= 2, use_cases >= 4, edge_cases >= 3, assumptions >= 3` for Product mode. The readiness gate checks booleans: `problem_defined: false`, `actors_identified: false`, etc.

**What to do:**

Keep count as a minimum floor, but add **mandatory semantic dimensions** to `coverage-matrix.yaml`:

```yaml
semantic_dimensions:
  # Mandatory (gate fails if false without justification)
  problem_independent_of_solution: false
  actor_roles_and_permissions: false
  trigger_and_preconditions: false
  core_behavior_described: false
  success_signal_defined: false
  explicit_non_goals: false
  failure_modes_covered: false
  data_mutations_identified: false

  # Recommended (warning if false, no failure)
  degraded_behavior: false
  side_effects_and_notifications: false
  observability_needs: false
  permissions_and_policy: false

  # Activated by archetype (R6)
  archetype_dimensions: {}
```

**Gate rule:** Ideation Readiness Gate fails if any mandatory dimension is `false` without a `not_applicable` justification with reason.

**Each archetype (R6) adds extra dimensions.** Example for workflow: `state_machine_defined: false`, `invalid_transitions_documented: false`, `sla_timeout_defined: false`.

**Files to change:**
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml` — add `semantic_dimensions`
- `.claude/skills/discovery/ideate/SKILL.md` — add dimension check to readiness gate
- `.claude/skills/validation/validate-gate/SKILL.md` — add dimension check to Layer 2
- `.claude/hooks/state_defaults.py` — add dimensions to defaults if needed

**Effort:** ~100 lines

**Priority:** P0
**Layer:** 4

---

### R6. Archetype-aware probe packs as post-story checklist

**Evidence from code:**

`edge-case-sweep/SKILL.md` has 8 generic categories: invalid input, dependency unavailable, race condition, permission mismatch, partial success, abuse, rollback, observability. Good defaults, but they don't cover gaps specific to each type of feature.

**Correct sequence (research insight):**

Stories (R2) → Snapshot (R3) → **Archetype checklist** (R6) to verify what the stories didn't reveal.

Archetype probes are NOT the primary extraction method. They are a safety net that runs AFTER stories, to find what the PO didn't tell because they didn't think of it.

**Start with 3 archetypes, expand after stabilization:**

```markdown
# .claude/skills/discovery/elicitation-archetypes/workflow-approval.md

## Archetype: Workflow / Approval

### Mandatory probes (ask one at a time)
1. "What are all the possible states? List them all."
   - Sufficient: list with 3+ states and clear names
   - Insufficient: "pending and approved" (missing rejected, expired, cancelled)

2. "When someone rejects, what happens? Goes back to whom? Is the requester notified?"
   - Sufficient: clear rejection flow with next step
   - Insufficient: "the person corrects and resends" (no detail)

3. "If nobody approves within X days, what should happen?"
   - Sufficient: timeout with automatic action or escalation
   - Insufficient: "I don't know" → register as ASM-# open

4. "Can someone delegate the approval? Does the delegate have the same powers?"

5. "Is there an audit trail? Who needs to see the approval history?"

6. "Can something already approved be reopened? Under what conditions?"

### Anti-patterns for this archetype
- Implicit states (e.g., "in review" that nobody defined)
- Impossible transitions not documented
- SLA without consequence
```

**3 initial archetypes:**

| Archetype | File | Probes |
|---|---|---|
| Workflow / Approval | `workflow-approval.md` | States, transitions, timeout, delegation, reopen, audit |
| API / Integration | `api-integration.md` | Auth, retry, rate limit, idempotency, partial failure, versioning |
| Import / Export | `import-export.md` | Formats, max size, malformed rows, preview, rollback, resume, encoding, progress feedback |

**After stabilization, expand to:**
- CRUD / Backoffice — Roles, bulk ops, soft delete, search/filter, audit, export
- AI / Copilot — Input boundaries, hallucination, human override, refusal, eval, latency
- Billing / Subscription — Cycle, upgrade/downgrade, pro-rata, dunning, refund, compliance

**Integration:** After the "Actor Map" and "Journey Sweep" modules in ideation, the agent asks: "Based on what we discussed, this work looks most like [list of archetypes]. Which best describes what we're building?" → Load 1-3 probe packs → Run probes as checklist over what the stories didn't cover.

**Files to create:**
- `.claude/skills/discovery/elicitation-archetypes/` (directory)
- 3 files `.md`, one per archetype (~80 lines each)
- Reference in `.claude/skills/discovery/ideate/SKILL.md`

**Effort:** ~240 lines (3 × 80) + ~30 lines (integration) = ~270 lines

**Priority:** P0
**Layer:** 1

---

### R7. Non-goals as traceable objects (`NG-#`)

**Evidence from code:**

The feature-brief (Q4) asks "What is this feature explicitly NOT doing?". The opportunity-pack has a "Constraints & Guardrails" section with "what must NOT get worse." But neither is traceable downstream — if a user story or impl-plan reintroduces something declared out of scope, nobody detects it.

`check-traceability/SKILL.md` traces `BO-# → PRD-F-# → US-# → FS-# → impl-#` but does NOT trace non-goals. `ID_PATTERNS` in `state_defaults.py` does not include `NG-#`.

**What `NG-#` solves:**

Not just scope creep. Also: downstream contradictions, rediscovery of rejected decisions, implementation of "obvious behaviors" that were never authorized.

**What to do:**

1. Add `NG-#` to `ID_PATTERNS`:
```python
"non_goals": r"\bNG-\d+\b",
```

2. For each `NG-#`:
- statement: what MUST NOT happen
- reason: why it's excluded
- scope: `permanent | deferred_to_v2 | conditional`
- adjacent_behavior: valid functionality that neighbors this non-goal
- downstream_must_respect: list of docs that cannot contradict

3. Add check in `check-traceability`: if downstream doc mentions behavior that contradicts `NG-#`, flag as violation.

4. Add section in opportunity-pack template (between "Constraints & Guardrails" and "Assumptions"):

```markdown
## Non-Goals Registry

### NG-1: [What NOT to do]
- **Reason:** [why it's excluded]
- **Scope:** permanent | deferred_to_v2 | conditional
- **Adjacent behavior:** [valid functionality that neighbors this non-goal]
- **Downstream docs that must respect:** [list]
```

**Files to change:**
- `state_defaults.py` — add NG-# to ID_PATTERNS
- `feature_lifecycle.py` — extract NG-# from docs
- `check-traceability/SKILL.md` — add NG-# violation check
- Template of opportunity-pack — add section
- Template of feature-brief — add section

**Effort:** ~120 lines

**Priority:** P0
**Layer:** 1, 4

---

### R8. Vague response escalation table

**Evidence from code:**

The jtbd-extractor says "Do not accept 'save time' without specifying where and how." Good intention, no mechanics.

With story-based interviewing (R2), vague answers happen less frequently because concrete narratives naturally produce details. But when they happen, the agent needs to know how to react.

**What to do:**

Create a shared escalation table:

```markdown
# .claude/skills/discovery/knowledge/vague-response-escalation.md

| Vague pattern | Reaction |
|---|---|
| "it should be fast" | "In the story you told me, how long did it take? How long should it take for the user not to complain?" |
| "it needs to be secure" | "Secure against what? Last time something went wrong, what happened?" |
| "many/few/several" | "Give me a number. Order of magnitude: tens, hundreds, thousands?" |
| "we'll figure it out later" | "Does this block implementation? If yes, I need a decision. If no, I'll register as ASM-# deferred." |
| "like [competitor]" | "What exactly? Show me or describe the specific part you want." |
| "obvious/standard" | "Explain the 'obvious' as if I've never seen the system." |
```

**Files to create:**
- `.claude/skills/discovery/knowledge/vague-response-escalation.md` (new)
- Referenced by: ideate, jtbd-extractor, feature-brief, assumption-audit

**Effort:** ~50 lines

**Priority:** P0
**Layer:** 1

---

### R9. "I don't know" differentiation

**Evidence from code:**

The assumption-audit has: "status: resolved | assumed | open." But it doesn't differentiate between three types of "I don't know":

| Type | Meaning | Treatment |
|---|---|---|
| "I don't know and need to research" | Conscious gap | ASM-# open with owner + deadline |
| "I don't know and it's ok not to know" | Conscious defer | ASM-# deferred with justification |
| "I never thought about this" | **Unconscious gap** | Deepen BEFORE moving on — this is the most valuable case |

**What to do:**

Add instruction in discovery and planning agents:

```markdown
## Handling "I Don't Know"

When the user responds "I don't know", "good question", "I never thought about this":

Ask: "Help me classify this:
A) Do you know who would know? → register as ASM-# open with owner
B) Is it safe to leave for later? → register as ASM-# deferred
C) Could this change what we're building? → I need to explore more"

If the answer is C, DO NOT move forward. Ask 2-3 more questions about the topic
before moving to the next module.
```

**Files to change:**
- `.claude/agents/discovery-agent.md` — "Handling Uncertainty" section
- `.claude/agents/planning-agent.md` — same section
- `.claude/skills/discovery/assumption-audit/SKILL.md` — expand status options

**Effort:** ~40 lines

**Priority:** P0
**Layer:** 1

---

### R10. Fatigue management

**Problem:**
Nothing exists today. A complete Product mode interview can have 40+ questions. Quality degrades as the user gets tired, but the framework has no mechanism to detect or adapt to this.

**What to do:**

1. Order questions by criticality: implementation-blockers first, enrichment second.
2. After a configurable threshold of substantive questions (default: 15), offer:
   - Continue deepening
   - Pause and resume later (checkpoint persisted in `elicitation-state.yaml`)
   - Accept explicit defaults for remaining dimensions
3. For dimensions with accepted defaults: register as `ASM-# assumed_default` with `revisit_required: true`.

**Files to change:**
- `.claude/skills/discovery/ideate/SKILL.md` — add "Fatigue Management" section
- `.claude/skills/discovery/ideate/knowledge/elicitation-state.yaml` — fatigue tracking fields already included in R1 template

**Effort:** ~25 lines

**Priority:** P1
**Layer:** 1

---

### R11. Anti-placeholder and anti-vagueness validation

**Evidence from code:**

`validate-gate/SKILL.md` Layer 1 checks "No unresolved [TODO] or [TBD] placeholders." Layer 2 checks "User stories follow Given/When/Then with specific values (not placeholders)" and "Technical specs have quantified NFRs (numbers, not 'fast' or 'scalable')."

Layer 2 is correct in intention but LLM-dependent — no mechanical rejection criteria.

**Important: guard against false positives.** Simple regex isn't enough. The validator must differentiate: real placeholder vs. example in template vs. quoted text vs. reference docs.

**What to add:**

Anti-patterns for Layer 1 (fast-fail, no LLM dependency):

```markdown
### Anti-Placeholder Patterns (Layer 1 extension)
Reject automatically if found in required sections:
- Text inside brackets: [SOMETHING], [USER], [ACTION], [RESULT], [VALUE]
- NFR-# without a number: "fast", "quick", "scalable", "secure", "reliable" without metric
- Given/When/Then with < 5 words per clause
- Empty table cells in required tables
- "TBD", "TODO", "to be defined", "a definir" in any form
```

Anti-vagueness for Layer 2:

```markdown
### Vagueness Checks (Layer 2)
- Every NFR-# must contain at least one number (ms, %, req/s, etc.)
- Every US-# happy-path must have at least 1 US-# or EDGE-# error-path sibling
- Every permission claim ("only admin can...") must trace to a formal role definition
- Absence of at least 1 error scenario per feature is a CONTENT GAP
```

**Files to change:**
- `.claude/skills/validation/validate-gate/SKILL.md` — expand Layer 1 and Layer 2

**Effort:** ~50 lines

**Priority:** P0
**Layer:** 4

---

### R12. `/elicit` command — Semantic stress-test

**Problem:**
Scattered pieces exist: pressure test in feature-brief (4 questions), adversarial review language in validate-gate, edge-case-sweep in ideation. None is focused on "find what remained implicit in existing documents."

**When to use:**
1. After `ideate`, before `feature` or `discover`
2. After `requirements`, before `design`
3. When the user says: "I want to challenge what's already been specified"

**What it does:**
Does not generate new product artifacts. It generates a findings report.

**7 specific techniques:**

1. **Developer simulation** — "If I were implementing [feature], what would I need to ask?"
2. **Cross-doc consistency** — DB constraints vs data-dictionary vs API schema
3. **Vague quantifier scan** — "fast", "secure", "many" without metric
4. **NG-# violation scan** — Do downstream docs contradict non-goals?
5. **Missing error siblings** — For each happy-path UC-#, does a corresponding error-path exist?
6. **Permission matrix gap** — Permission claims without formal role definition?
7. **State machine completeness** — For entities with states, are all transitions documented?

**Output:**

```markdown
# Elicitation Findings: [Feature/Project Name]

## Ambiguities (EL-A-#)
- EL-A-1: US-3 says "notify user" but doesn't specify channel

## Contradictions (EL-C-#)
- EL-C-1: PRD says "CSV only", api-spec accepts XLSX

## Missing Boundaries (EL-B-#)
- EL-B-1: No doc defines what happens when rate limit is reached

## Hidden Assumptions (EL-H-#)
- EL-H-1: All docs assume single-tenant without explicitly stating it

## Developer Questions (EL-D-#)
- EL-D-1: "If I implement US-3, which notification channel do I use?"
```

**Files to create:**
- `.claude/commands/elicit.md` (~50 lines)
- `.claude/skills/validation/elicit/SKILL.md` (~150 lines)

**Effort:** ~200 lines

**Priority:** P0
**Layer:** 4

---

### R13. Developer Handoff Packet — Generated, with explicit derivation rule

**Design rules:**

The packet must be: automatically generated, derived from authoritative sources, regenerable, non-authoritative.

**SST derivation table (each section points to its authority):**

| Packet section | Authority |
|---|---|
| Context & non-goals | feature-brief + NG-# registry |
| Actors & permissions | opportunity-pack actor map |
| Business rules | feature-brief FB-# + feature-spec |
| Acceptance criteria | user-stories.md (filtered by feature) |
| Error handling matrix | EDGE-# + user-stories error scenarios |
| State machine | feature-spec |
| API contracts | api-spec (filtered by feature) |
| Data mutations & validation | database-spec + data-dictionary |
| Performance requirements | tech-spec NFR-# |
| Observability | NEW — doesn't exist today |
| Tasks (impl-#) | implementation-plan |
| Open questions | ASM-# open + feature-brief outstanding questions |

**Scope:** The handoff packet should exist per feature or per sprint scope, not necessarily per entire project.

**Files to create:**
- `.claude/skills/implementation/implementation-packet/SKILL.md` (~180 lines)
- `.claude/skills/implementation/implementation-packet/knowledge/template.md` (~80 lines)

**Effort:** ~260 lines

**Priority:** P0
**Layer:** 3

---

### R14. Gate decisions persistence with rationale

**Evidence from code:**

`default_workflow_state()` in `state_defaults.py` has `gates: { discovery_gate: "pending" }`. Just status. No feedback, reason, or rejected approaches.

If the user says "ITERATE because the vision needs to emphasize cost reduction", the next phase doesn't know this.

**What to do:**

Expand gate state in workflow-state.yaml:

```yaml
gates:
  discovery_gate:
    status: iterate
    feedback: "Vision needs to emphasize cost reduction, not speed"
    timestamp: "2026-03-23T14:30:00Z"
    rejected_approaches:
      - "Focus on speed as value proposition"
    iteration_count: 1
    unresolved_objections: []
```

This feeds: workflow state, memory, next prompts.

**Files to change:**
- `state_defaults.py` — expand gates
- `validate-gate/SKILL.md` — save feedback on ITERATE/NO-GO
- `memory-sync.py` — propagate gate decisions

**Effort:** ~80 lines

**Priority:** P1
**Layer:** 5

---

### R15. Post-implementation feedback loop

**Problem:**
Gaps found by the dev during implementation don't feed back into the framework. Archetype packs don't improve. The same questions get missed in the next project.

**What to do:**

Create `/retro` that:
1. Asks the dev: "What decisions did you make on your own during implementation?"
2. Classifies each gap: in which phase should it have been captured?
3. Saves as learning in `docs/ets/projects/{slug}/learnings/`
4. If a pattern repeats 2+ times in different projects, suggests adding to the corresponding archetype probe

This is what transforms archetype packs into assets that improve over time.

**Files to create:**
- `.claude/commands/retro.md` (~50 lines)
- `.claude/skills/implementation/retro/SKILL.md` (~100 lines)

**Effort:** ~150 lines

**Priority:** P1 late / P2
**Layer:** 5

---

## Implementation Roadmap

### Phase 1 — Interview Method (4-6 days)

Objective: make discovery and interview significantly better.

| # | Improvement | Impact | Effort |
|---|---|---|---|
| R1 | Separate coverage-matrix and elicitation-state | Clean state, resumable interviews | ~150 lines |
| R2 | Story-based interviewing | 3x richer extraction | ~210 lines |
| R3 | Interview Snapshots (SNAP-#) | Synthesis without context loss | ~60 lines |
| R8 | Vague response escalation table | More specific answers | ~50 lines |
| R9 | "I don't know" differentiation | Better classified unknowns | ~40 lines |
| R10 | Fatigue management | Consistent quality | ~25 lines |
| **Phase 1 total** | | | **~535 lines** |

### Phase 2 — Semantic Coverage & Archetypes (3-5 days)

Objective: stop measuring coverage only by count.

| # | Improvement | Impact | Effort |
|---|---|---|---|
| R5 | Semantic coverage dimensions | Gates that check substance | ~100 lines |
| R6 | Archetype probe packs (3 initial) | Right questions for the type of problem | ~270 lines |
| R7 | Non-goals traceable (NG-#) | Detectable scope creep | ~120 lines |
| **Phase 2 total** | | | **~490 lines** |

### Phase 3 — Brainstorm & Validation (3-5 days)

Objective: disciplined brainstorm and executable validation.

| # | Improvement | Impact | Effort |
|---|---|---|---|
| R4 | Brainstorm divergence/convergence + HMW bridge | More disciplined ideation | ~160 lines |
| R11 | Anti-placeholder / anti-vagueness validation | Placeholders don't pass | ~50 lines |
| R12 | `/elicit` command (stress-test) | Ambiguities detected before code | ~200 lines |
| **Phase 3 total** | | | **~410 lines** |

### Phase 4 — Handoff & Continuity (5-8 days)

Objective: reduce ambiguity for engineering and prevent drift.

| # | Improvement | Impact | Effort |
|---|---|---|---|
| R13 | Developer Handoff Packet | Dev gets everything in 1 document | ~260 lines |
| R14 | Gate decisions persistence | Phases don't repropose rejected ideas | ~80 lines |
| R15 | Post-implementation feedback loop | Framework learns from experience | ~150 lines |
| **Phase 4 total** | | | **~490 lines** |

---

## Effort Summary

| Phase | Lines | Days |
|---|---|---|
| Phase 1 — Interview Method | ~535 | 4-6 |
| Phase 2 — Semantic Coverage | ~490 | 3-5 |
| Phase 3 — Brainstorm & Validation | ~410 | 3-5 |
| Phase 4 — Handoff & Continuity | ~490 | 5-8 |
| **Total** | **~1,925** | **15-24** |

**Realistic note:** A solid first version can ship earlier. But a truly calibrated version — without fragile rules or prompt-only enforcement — should be treated as 3-4 weeks of work, not a few days. The line count captures code; it doesn't capture iteration, testing, and prompt calibration.

---

## Success Metrics

### Primary Metrics

| Metric | How to measure | Target |
|---|---|---|
| Questions dev had to invent | Ask dev at end of each feature | < 3 per feature |
| Semantic dimensions covered in 1st pass | % of mandatory dimensions = true before gate | > 80% |
| Archetype probes answered with sufficient response | % of probes with concrete answer | > 70% |
| Vague responses correctly escalated | % of vague responses that trigger follow-up probe | > 90% |
| Gate iterations | Average ITERATEs before GO | < 1.5 |
| Stories extracted vs abstract answers | Ratio of SNAP-# vs generic responses | > 60% story-based |
| Rejected changes reappearing downstream | NG-# violations in later docs | 0 |

### Gold Metric

> How many product/behavior decisions did the dev have to invent because the documentation didn't answer?

This is the single best measure of the system's true quality.

---

## Differences: v3-AA → v3-Claude → v4

| Aspect | v3-AA | v3-Claude | v4 (this document) |
|---|---|---|---|
| Strategic framing | 5 layers, D1-D5 diagnostics | 3-layer diagnosis | 5 layers + 6 diagnostics with code evidence |
| State management | `coverage-matrix` + `elicitation-state` separated | Expanded `coverage-matrix` (merged) | **Separated** per v3-AA (cleaner design) |
| Interview method | Story-based + reflection | Story-based + story probes + sufficiency criteria | Story-based + probes + **snapshots** + sufficiency |
| Archetypes | 3 initial, expand later | 6 initial | **3 initial** (v3-AA's prudent approach) + 3 planned |
| Brainstorm | 5 stages + 3 initial techniques | 7 phases with code | **6 phases** + HMW bridge + 3 initial techniques |
| Handoff packet | SST derivation rule explicit | Template + generation rule | **Both**: SST derivation table + template + generation rule |
| Scope change | Layer 5 + D5 diagnostic | R13 gate persistence | Layer 5 + D6 + gate persistence + `/retro` |
| Effort estimate | 16-25 days (realistic) | 9-13 days (optimistic) | **15-24 days** (calibrated) |
| Elicitation engine | Centralized shared mechanism | Decentralized rule per skill | **Decentralized** (realistic for prompt-based agents) + shared state file |
| Code artifacts | Concepts described | YAML, Markdown, Python snippets per R | **Full artifacts** per R with file paths |

### The fundamental principle of v4

> **Extract first, verify second.** Concrete stories produce 80% of coverage naturally. Archetypes, semantic dimensions, and `/elicit` capture the remaining 20% that stories didn't reveal.

---

## Conclusion

The ETUS doesn't need to become a "heavier" framework. It needs to become a framework that is:

- **Explicit** in interview state
- **Semantic** in coverage
- **Story-driven** in extraction
- **Disciplined** in brainstorm
- **Mechanical** in validation
- **Safe** in developer handoff
- **Resilient** to changes

The future of the ETUS is to move from a well-documented methodology to an operational system of elicitation, decision, and handoff.
