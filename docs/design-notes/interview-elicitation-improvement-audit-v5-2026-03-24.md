# Audit v5: ETUS PMDocs — Elicitation, Coverage, Brainstorm & Developer Handoff

**Date:** 2026-03-24
**Framework version:** v5.3
**Base:** Direct source code reading (9 agents, 45 skills, 13 commands, 5 gates, 6 hooks, state_defaults.py, coverage-matrix.yaml, all templates) + v3-AA strategic audit + v3-Claude code-grounded audit + v4-AA (with D6, R10, R15, Definition of Done) + v4-Claude (with SNAP-#, story probes, 6-phase brainstorm) + external research (GOV.UK, NNGroup, IDEO, Product Talk, Google Design Sprint)
**Objective:** Make the ETUS framework exceptional at extracting product ideas from the PO's head — leaving zero gaps — and producing documentation that lets a developer implement without guessing.

---

## Central Thesis

The ETUS PMDocs framework already has the right conceptual architecture: ideation before specification, upstream coverage via actors/JTBDs/journeys/use-cases/edge-cases/assumptions, a traceability chain (`BO-# → PRD-F-# → US-# → FS-# → impl-#`), SST enforcement, gates per phase, and 4-mode workflows. This puts it ahead of most product documentation approaches.

The core problem is one sentence:

> **The ETUS is prompt-rich and enforcement-poor.**

The right rules exist as text inside skills, agent instructions, and templates — but not as persistent state, progression blockers, validators, or operational artifacts. A seemingly "good" interview can still skip essential question types, accept vague answers, mark coverage without sufficiency, and advance through fatigue or haste.

The evolution the ETUS needs is not "more documents." It needs:

1. A story-based interview method that extracts concrete behavior instead of abstract opinions
2. Interview snapshots that capture each story immediately instead of synthesizing everything at the end
3. Two separate state files — one for coverage substance, one for interview execution
4. Semantic coverage that measures substance instead of counting items
5. EDGE-# resolution tracking so no edge case silently disappears
6. Disciplined brainstorming that separates divergence from convergence with HMW as bridge
7. Upstream template expansion so downstream handoff has content to pull from
8. Executable validation that mechanically catches placeholders and vagueness
9. A consolidated developer handoff that respects SST (derived, not authoritative)
10. Change propagation that actually updates connected documents

---

## System Architecture: 5 Layers

Every recommendation maps to exactly one layer. This makes it clear where each improvement acts and what it protects against.

### Layer 1 — Core Interview (extraction quality)

Skills: `ideate`, `discover`, `project-context`, `product-vision`, `feature-brief`

Where ideas leave the PO's head and enter the system. If this layer fails, everything downstream is built on thin air. Must optimize for: truth, concrete behavior, real context, friction, impact, constraints.

### Layer 2 — Structured Brainstorm (idea transformation)

Skills: `brainstorm` module inside `ideate`, `solution-discovery`

Does not extract the raw problem — transforms evidence into testable directions. If discovery fails, brainstorm becomes guesswork. If brainstorm fails, the solution becomes premature fixation.

### Layer 3 — Translation (specification fidelity)

Skills: `feature-brief`, `prd`, `user-stories`, `feature-spec`

Does not discover — translates. The quality of discovery and brainstorm must survive here without degradation. Upstream templates must be expanded (R11) to produce structured content that the handoff packet (R14) can pull.

### Layer 4 — Assurance (ambiguity detection)

Skills: `validate-gate`, `check-traceability`, `check-sst`, `/elicit`

Does not create — prevents ambiguities from escaping. Must be mechanical, not opinion-based.

### Layer 5 — Change & Continuity (drift protection)

Skills: `correct-course`, state/handoffs, `/retro`

Protects the framework from drift after scope changes and enables continuous learning. Currently the most underdeveloped layer in the ETUS.

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

The ideate skill Problem Framing asks: "What is the proposed solution?", "What is the underlying problem?", "What happens if we do nothing?"

The discovery-agent does 5W2H: "What is the problem/opportunity?", "Who are the users/stakeholders?"

The feature-brief Q1 asks: "What feature are you documenting?"

All abstract questions that produce abstract answers. Product Talk, NNGroup, and GOV.UK converge: the best discovery interviews are **story-based and past-focused**. Answers about the past are more concrete, more detailed, and reveal context that abstract questions cannot capture.

**Analogy:** Asking "What's the problem?" is like a doctor asking "What's wrong with you?" Asking "Tell me what happened" is like asking "When did it start? What did you feel? What did you do?" — the second approach produces a better diagnosis.

### D2 — Coverage measures quantity, not substance

**Evidence from code:**

`coverage-matrix.yaml` thresholds: `actors >= 2, jtbd >= 2, journeys >= 2, use_cases >= 4, edge_cases >= 3, assumptions >= 3` for Product mode. The readiness gate checks booleans: `problem_defined: false`, `actors_identified: false`, etc.

3 edge cases about "empty field" are worth less than 1 edge case about "what happens when the payment service fails mid-transaction." The count passes, the substance does not.

### D3 — Coverage state and interview state are conflated

**Evidence from code:**

`coverage-matrix.yaml` tries to track both what is covered (semantic coverage) and where the interview is (step_status, active_step, last_completed_step). These are two different concerns. If the interview pauses and resumes, the agent doesn't know which specific probe it was on. If coverage is met through low-quality answers, nothing detects it.

### D4 — Discovery and brainstorm need different dynamics

Discovery optimizes for: truth, context, real behavior, concrete friction, impact, constraints.

Brainstorm optimizes for: option breadth, structure, clustering, disciplined selection, assumption surfacing, test planning.

The brainstorm module says: "BMAD technique selection → candidate solution directions → risk discovery → stress test" — mixing idea generation with immediate evaluation. IDEO and Design Sprint are clear: divergence and convergence are different modes that must not be mixed.

### D5 — Developer gets 10+ documents and assembles the puzzle alone

No consolidated artifact says: "here is everything you need to implement this feature, in one place." The dev navigates opportunity-pack, feature-brief, user-stories, design-delta, tech-spec, api-spec, data-dictionary.

**Critical SST constraint:** The handoff packet cannot become a new source of truth. It must be derived, generated, regenerable, and non-authoritative. Each section points to its authority. The packet summarizes and consolidates but does not redefine.

### D6 — Edge cases can be identified but never resolved

**Evidence from code:**

The traceability chain validates `BO-# → PRD-F-# → US-# → FS-# → impl-#`. But it does not validate that each `EDGE-#` identified during ideation has a corresponding resolution downstream — a Given/When/Then that handles it, a FS-# rule, an ADR, or an API error code.

An edge case can pass through the entire pipeline unresolved: identified in ideation, never referenced in any downstream document, invisible to the gate because `failure_modes` dimension was marked `true` based on OTHER edge cases that were handled.

This is a traceability gap that neither the current `check-traceability` nor the readiness gate catches.

### D7 — Scope change is the most underdeveloped area

The framework is relatively sophisticated for: extracting, structuring, generating, validating. But it is weak for: propagating changes, preserving rejections, remembering user objections, updating connected docs. After a change-proposal is approved, downstream documents are not updated — the user must manually fix 5-10 files.

---

## Recommendations

### R1. Separate `coverage-matrix.yaml` and `elicitation-state.yaml`

**Problem:**
`coverage-matrix.yaml` tries to be both "what is covered" and "where the interview is." This creates a YAML with two responsibilities. If the interview pauses and resumes, the agent doesn't know which probe it was on within a module. If coverage is met through vague answers, nothing detects it.

**What to do:**

**A. `coverage-matrix.yaml` — Semantic coverage (what is covered)**

Responsible for: upstream IDs, semantic dimensions (R6), EDGE-# resolution tracking (R7), archetype dimensions, blockers, readiness gate.

```yaml
# coverage-matrix.yaml — SEMANTIC COVERAGE ONLY
meta:
  mode: product
  status: draft
  source_artifact: docs/ets/projects/{project-slug}/discovery/opportunity-pack.md

coverage:
  actors:
    threshold: 2
    count: 0
    items:
      - id: ACT-1
        label: ""
        status: not_started
        downstream: []

  # ... jtbd, journeys, use_cases, edge_cases, assumptions (same structure as today)

semantic_dimensions:
  # Mandatory (gate fails if missing without justification)
  problem_clarity:
    status: missing          # covered | partial | missing | not_applicable
    evidence: ""
  actor_roles_and_permissions:
    status: missing
    gap: ""
  trigger_and_preconditions:
    status: missing
  core_behavior:
    status: missing
  success_signal:
    status: missing
  explicit_non_goals:
    status: missing
  failure_modes:
    status: missing
  data_mutations:
    status: missing
  permissions_and_policy:
    status: missing

  # Recommended (warning if missing, no gate failure)
  degraded_behavior:
    status: missing
  side_effects_and_notifications:
    status: missing
  observability_needs:
    status: missing

  # Activated by archetype (R8)
  archetype_dimensions: {}

mandatory_dimensions:
  - problem_clarity
  - actor_roles_and_permissions
  - core_behavior
  - success_signal
  - explicit_non_goals
  - failure_modes
  - permissions_and_policy

edge_resolution:
  # Every EDGE-# must have a resolution or explicit deferral (R7)
  # EDGE-1: { status: unresolved, gap: "No US-# or FS-# handles corrupted file" }
  # EDGE-2: { status: resolved, via: "US-4 Given/When/Then" }
  # EDGE-3: { status: deferred, via: "NG-2 — deferred to Phase 2" }

readiness_gate:
  problem_defined: false
  actors_identified: false
  jtbd_covered: false
  journeys_covered: false
  use_cases_covered: false
  edge_cases_covered: false
  guardrails_defined: false
  blocking_questions_explicit: false
  all_mandatory_dimensions_covered: false
  all_edges_resolved_or_deferred: false
  recommendation: iterate

blocking_questions: []
pending_items: []
assumed_items: []
blockers: []
```

**B. `elicitation-state.yaml` — Interview execution (how the conversation is going)**

```yaml
# elicitation-state.yaml — INTERVIEW STATE ONLY
meta:
  mode: product
  session_id: "2026-03-24-001"
  started_at: "2026-03-24T10:00:00Z"
  last_activity: "2026-03-24T11:30:00Z"

current_module: actors
current_probe: "In the story you told me, who else was involved?"
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
  dont_know_count: 1
  dont_know_classified: 1

fatigue:
  threshold: 15
  current: 12
  offered_pause: false

active_archetypes: []

checkpoints:
  - snapshot: SNAP-1
    after_question: 3
    module: problem
    validated_by_user: true
  - snapshot: SNAP-2
    after_question: 5
    module: problem
    validated_by_user: true
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

**Files to create/change:**
- `.claude/skills/discovery/ideate/knowledge/elicitation-state.yaml` — new template
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml` — strip interview execution fields
- `.claude/skills/discovery/ideate/SKILL.md` — add entry rule referencing both files
- Each sub-skill (jtbd-extractor, journey-sweep, edge-case-sweep, use-case-matrix, assumption-audit) — add state read/write

**Effort:** ~180 lines | **Priority:** P0 | **Layer:** 1

---

### R2. Story-based interviewing as the primary extraction method

**Evidence from code:**

The ideate skill asks: "What is the proposed solution?", "What is the underlying problem?" The discovery-agent asks: "What is the problem/opportunity?" The feature-brief asks: "What feature are you documenting?" All abstract questions.

**What to do:**

Rewrite extraction prompts in 4 skills to use story-first:

| Skill | Current prompt | Story-based prompt |
|---|---|---|
| ideate (Problem Framing) | "What is the underlying problem?" | "Tell me about the last time this problem happened. What happened? Who was involved? What went wrong?" |
| ideate (Actor Map) | "Who feels the pain directly?" | "In the story you told me, who else was involved? Who approved? Who was affected without participating?" |
| jtbd-extractor | "What job is this person trying to get done?" | "Before thinking about the solution: what was this person trying to do at that moment? What would make them say 'it was worth it'?" |
| feature-brief (Q1) | "What feature are you documenting?" | "Tell me about a concrete situation where the user would need this feature. What did they try to do? Where did they get stuck?" |

Create a shared knowledge file with reusable story probes:

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

6. "How much time/money did that workaround cost?"
   - Use when: user described a current alternative

## Anti-patterns to avoid

- "Would you use X?" → always yes. Ask about past behavior instead.
- "Don't you think X is important?" → leading. Ask "What matters most to you?"
- "Is this a problem?" → primes for yes. Ask "Tell me about the last time..."
```

**Files to change:**
- `.claude/skills/discovery/ideate/SKILL.md` — rewrite modules 2, 3, 4 for story-first
- `.claude/skills/discovery/jtbd-extractor/SKILL.md` — rewrite EXTRACTION PROMPTS
- `.claude/skills/planning/feature-brief/SKILL.md` — rewrite Q1-Q3
- `.claude/agents/discovery-agent.md` — rewrite "Problem Interview" section
- Create `.claude/skills/discovery/knowledge/story-probes.md` (new)

**Effort:** ~210 lines | **Priority:** P0 | **Layer:** 1

---

### R3. Interview Snapshots (SNAP-#) — Micro-artifacts for immediate synthesis

**Problem:**
Ideation captures information directly in opportunity-pack.md. The entire conversation is distilled into one document at the end. Details, quotes, and context are lost between the conversation and the synthesis.

**What the research shows:**
IDEO recommends "download your learnings" immediately after each interview. Product Talk recommends "interview snapshots" — right after each story, not at the end of the process.

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

**Effort:** ~60 lines | **Priority:** P0 | **Layer:** 1

---

### R4. Vague response escalation table

**Evidence from code:**

The jtbd-extractor says "Do not accept 'save time' without specifying where and how." Good intention, no mechanics.

**What to do:**

Create a shared escalation table as knowledge file:

```markdown
# .claude/skills/discovery/knowledge/vague-response-escalation.md

| Vague pattern | Reaction |
|---|---|
| "it should be fast" | "In the story you told me, how long did it take? How long should it take for the user not to complain?" |
| "needs to be secure" | "Secure against what? Last time something went wrong, what happened?" |
| "easy to use" | "Describe someone who would struggle. What would they try and where would they get stuck?" |
| "needs to scale" | "How many simultaneous users today? In 12 months? In 3 years?" |
| "many/few/several" | "Give me a number. Order of magnitude: tens, hundreds, thousands?" |
| "we'll figure that out later" | "Does this block implementation? If yes, I need a decision. If no, I'll register as ASM-# deferred with deadline." |
| "like [competitor]" | "What exactly from [competitor]? What do you NOT want from it?" |
| "obvious/standard" | "Explain the 'obvious' as if I've never seen the system." |
| "real-time" | "Real-time means what latency? < 100ms? < 1s? < 5s?" |
| "robust" | "Handles which specific failures with which specific behavior?" |
```

**Files to create:**
- `.claude/skills/discovery/knowledge/vague-response-escalation.md` (new)
- Referenced by: ideate, jtbd-extractor, feature-brief, assumption-audit

**Effort:** ~50 lines | **Priority:** P0 | **Layer:** 1

---

### R5. "I don't know" differentiation

**Evidence from code:**

The assumption-audit has: "status: resolved | assumed | open." Does not differentiate between three types of "I don't know":

| Type | Meaning | Treatment |
|---|---|---|
| "I don't know and need to research" | Conscious gap | ASM-# open with owner + deadline |
| "I don't know and it's ok not to know now" | Conscious defer | ASM-# deferred with justification |
| "I never thought about this" | **Unconscious gap** | Deepen BEFORE moving on — most valuable case |

**What to do:**

Add instruction in discovery and planning agents:

```markdown
## Handling "I Don't Know"

When the user responds "I don't know", "good question", "I never thought about this":

Ask: "Help me classify this:
A) Do you know who would know? → I register as ASM-# open with owner
B) Is it safe to leave for later? → I register as ASM-# deferred
C) Could this change what we're building? → I need to explore more"

If the answer is C, DO NOT move forward. Ask 2-3 more questions about the topic
before moving to the next module.
```

**Files to change:**
- `.claude/agents/discovery-agent.md` — "Handling Uncertainty" section
- `.claude/agents/planning-agent.md` — same section
- `.claude/skills/discovery/assumption-audit/SKILL.md` — expand status options

**Effort:** ~40 lines | **Priority:** P0 | **Layer:** 1

---

### R6. Semantic coverage dimensions instead of counting

**Evidence from code:**

Thresholds: `actors >= 2, jtbd >= 2, use_cases >= 4, edge_cases >= 3` for Product mode. Readiness gate checks booleans.

**What to do:**

Keep count as minimum floor, add mandatory semantic dimensions to `coverage-matrix.yaml` (already shown in R1 template).

**Gate rule:** Ideation Readiness Gate fails if any mandatory dimension is `missing` without a `not_applicable` justification with reason.

Each archetype (R8) adds extra dimensions. Example for workflow: `state_machine_defined`, `invalid_transitions_documented`, `sla_timeout_defined`.

**Gate behavior change:**
- Current: "edge_cases >= 3 → pass"
- New: "failure_modes dimension == covered AND all EDGE-# resolved or deferred → pass"

**Files to change:**
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml` — add `semantic_dimensions` (already in R1)
- `.claude/skills/discovery/ideate/SKILL.md` — add dimension check to readiness gate
- `.claude/skills/validation/validate-gate/SKILL.md` — add dimension check to Layer 2
- `.claude/hooks/state_defaults.py` — add dimensions to defaults

**Effort:** ~100 lines | **Priority:** P0 | **Layer:** 4

---

### R7. EDGE-# resolution tracking

**Problem (D6):**

An edge case can pass through the entire pipeline unresolved: identified in ideation, never referenced in any downstream document, invisible to the gate because `failure_modes` was marked `true` based on OTHER edge cases.

**What to do:**

Add `edge_resolution` map to `coverage-matrix.yaml` (already shown in R1 template):

```yaml
edge_resolution:
  EDGE-1: { status: unresolved, gap: "No US-# or FS-# handles corrupted file" }
  EDGE-2: { status: resolved, via: "US-4 Given/When/Then" }
  EDGE-3: { status: deferred, via: "NG-2 — deferred to Phase 2" }
```

**Resolution rule:** The `failure_modes` dimension is only `covered` when ALL identified EDGE-# items have either:
- a resolution (US-# Given/When/Then, FS-# rule, ADR, API error code), OR
- an explicit deferral as NG-# with rationale

**Files to change:**
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml` — add `edge_resolution`
- `.claude/skills/validation/validate-gate/SKILL.md` — fail on unresolved EDGE-#
- `.claude/skills/validation/check-traceability/SKILL.md` — add EDGE-# resolution chain

**Effort:** ~60 lines | **Priority:** P0 | **Layer:** 4

---

### R8. Archetype-aware probe packs as post-story checklist

**Evidence from code:**

`edge-case-sweep/SKILL.md` has 8 generic categories. Good defaults, but they don't cover gaps specific to each type of feature.

**Correct sequence:** Stories (R2) → Snapshot (R3) → **Archetype checklist** (R8) to find what the stories didn't reveal. Archetypes are NOT the primary extraction method. They are a safety net.

**Start with 3, expand after stabilization:**

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

| Archetype | File | Key probes |
|---|---|---|
| Workflow / Approval | `workflow-approval.md` | States, transitions, timeout, delegation, reopen, audit |
| API / Integration | `api-integration.md` | Auth, retry, rate limit, idempotency, partial failure, versioning, webhooks |
| Import / Export | `import-export.md` | Formats, max size, malformed rows, preview, rollback, resume, duplicates, progress |

**After stabilization, expand to:**
- CRUD / Backoffice — Roles, bulk ops, soft delete, search/filter, audit, export
- AI / Copilot — Input boundaries, hallucination, human override, refusal, eval, latency
- Billing / Subscription — Cycle, upgrade/downgrade, pro-rata, dunning, refund, compliance

**Integration:** After "Actor Map" and "Journey Sweep" modules, the agent asks: "Based on what we discussed, this work looks most like [list of archetypes]. Which best describes what we're building?" → Load 1-3 probe packs → Run probes as checklist over what the stories didn't cover.

**Files to create:**
- `.claude/skills/discovery/elicitation-archetypes/` (directory)
- 3 files `.md`, one per archetype (~80 lines each)
- Reference in `.claude/skills/discovery/ideate/SKILL.md`

**Effort:** ~270 lines | **Priority:** P0 | **Layer:** 1

---

### R9. Non-goals as traceable objects (`NG-#`)

**Evidence from code:**

The feature-brief (Q4) asks "What is this feature explicitly NOT doing?". The opportunity-pack has "Constraints & Guardrails." Neither is traceable downstream. `check-traceability` does not trace non-goals. `ID_PATTERNS` in `state_defaults.py` does not include `NG-#`.

**What `NG-#` solves:** Not just scope creep. Also: downstream contradictions, rediscovery of rejected decisions, implementation of "obvious behaviors" that were never authorized.

**What to do:**

1. Add `NG-#` to `ID_PATTERNS`:
```python
"non_goals": r"\bNG-\d+\b",
```

2. For each `NG-#`:
```markdown
### NG-1: [What NOT to do]
- **Statement:** [what must NOT happen]
- **Reason:** [why excluded]
- **Scope:** permanent | deferred_to_v2 | conditional
- **Adjacent behavior:** [valid functionality that neighbors this non-goal]
- **Downstream docs that must respect:** [list]
```

3. Add check in `check-traceability`: if downstream doc mentions behavior that contradicts `NG-#`, flag as violation.

4. Add section in opportunity-pack template (between "Constraints & Guardrails" and "Assumptions").

**Files to change:**
- `state_defaults.py` — add NG-# to ID_PATTERNS
- `feature_lifecycle.py` — extract NG-# from docs
- `check-traceability/SKILL.md` — add NG-# violation check
- Template of opportunity-pack — add section
- Template of feature-brief — add section

**Effort:** ~120 lines | **Priority:** P0 | **Layer:** 1, 4

---

### R10. Separate divergence and convergence in brainstorm

**Evidence from code:**

The brainstorm module says: "BMAD technique selection → candidate solution directions → risk discovery → stress test." Mixes generation with evaluation.

The discovery-agent offers 4 techniques (Mind Mapping, HMW, Scenario Planning, JTBD) and asks the user to pick one.

**What to do:**

Rewrite the brainstorm module with 6 explicit phases:

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

**Initial techniques:** HMW + clustering (always), Crazy 8s (Phase C divergence), Gut Check (Phase D selection).

**Future expansion:** mash-ups, role play, reverse brainstorming, six thinking hats.

**Files to change:**
- `.claude/skills/discovery/ideate/SKILL.md` — rewrite module 10
- `.claude/agents/discovery-agent.md` — rewrite "Creative Exploration" section
- `.claude/skills/discovery/ideate/knowledge/template.md` — expand "Solution Directions" to include themes, HMWs, raw ideas, clusters, assumptions

**Effort:** ~160 lines | **Priority:** P0 | **Layer:** 2

---

### R11. Upstream template expansion for structured developer content

**Problem:**
R14 (handoff packet) pulls content from upstream docs. But several upstream skills do not yet generate this content in structured form. Without expanding upstream templates first, the packet will have empty sections or violate SST by generating content itself.

**What to add to each upstream template:**

| Upstream skill | New mandatory section | Contents |
|---|---|---|
| **feature-spec** | Error Handling Matrix | Scenario, trigger, system response, user message, retry, rollback — per error |
| **feature-spec** | State Machine (if >2 states) | Mermaid diagram + valid transitions + forbidden transitions + side effects |
| **feature-spec** | Permission Matrix | Action × Role grid with ✅/❌ |
| **data-dictionary** | Validation Rules per field | Required, format/regex, min/max, default, valid example, invalid example, behavior on invalid |
| **quality-checklist** | Observability Requirements | Logs (event, level, fields), metrics (name, type, labels), alerts (condition, severity, channel) |
| **api-spec** | Idempotency/Retry/Concurrency | Per endpoint: idempotency key, retry safety, concurrency model, timeouts |

**Note on ID prefixes:** Error scenarios use `EDGE-#` with a `resolution_type: error_handling` field instead of creating a new `ES-#` prefix. This avoids ID proliferation while keeping the traceability chain simpler.

**Files to change:**
- `.claude/skills/planning/feature-spec/SKILL.md` — add error matrix, state machine, permission matrix sections (~60 lines)
- `.claude/skills/planning/feature-spec/knowledge/template.md` — add templates (~40 lines)
- `.claude/skills/data-design/data-dictionary/SKILL.md` — add validation rules per field (~20 lines)
- `.claude/skills/implementation/quality-checklist/SKILL.md` — add observability section (~20 lines)
- `.claude/skills/api-design/api-spec/SKILL.md` — add idempotency/retry/concurrency per endpoint (~15 lines)

**Effort:** ~155 lines | **Priority:** P0 | **Layer:** 3

---

### R12. Fatigue management

**Problem:**
Nothing exists today. A complete Product mode interview can have 40+ questions. Quality degrades as the user gets tired.

**What to do:**

1. Order questions by criticality: implementation-blockers first, enrichment second.
2. After a configurable threshold (default: 15 questions), offer:
   - Continue deepening
   - Pause and resume later (checkpoint persisted in `elicitation-state.yaml`)
   - Accept explicit defaults for remaining dimensions
3. For dimensions with accepted defaults: register as `ASM-# assumed_default` with `revisit_required: true`.

**Blocking rule:** Mandatory dimensions (problem_clarity, failure_modes, permissions_and_policy) CANNOT be accepted as defaults. Non-blocking dimensions (observability, side_effects) CAN.

**Files to change:**
- `.claude/skills/discovery/ideate/SKILL.md` — add "Fatigue Management" section
- Fatigue tracking already included in `elicitation-state.yaml` template (R1)

**Effort:** ~30 lines | **Priority:** P1 | **Layer:** 1

---

### R13. Anti-placeholder and anti-vagueness validation

**Evidence from code:**

`validate-gate/SKILL.md` Layer 1 checks "No unresolved [TODO] or [TBD] placeholders." Layer 2 checks "User stories follow Given/When/Then with specific values (not placeholders)" and "Technical specs have quantified NFRs (numbers, not 'fast' or 'scalable')." Layer 2 is correct but LLM-dependent.

**Important: guard against false positives.** The validator must differentiate: real placeholder vs. example in template vs. quoted text vs. reference docs.

**What to add:**

Layer 1 extension (fast-fail, no LLM dependency):

```markdown
### Anti-Placeholder Patterns (Layer 1 extension)
Reject automatically if found in required sections:
- Text inside brackets: [SOMETHING], [USER], [ACTION], [RESULT], [VALUE]
- NFR-# without a number: "fast", "quick", "scalable", "secure", "reliable" without metric
- Given/When/Then with < 5 words per clause
- Empty table cells in required tables
- "TBD", "TODO", "to be defined", "a definir" in any form
```

Layer 2 extension:

```markdown
### Vagueness Checks (Layer 2)
- Every NFR-# must contain at least one number (ms, %, req/s, etc.)
- Every US-# happy-path must have at least 1 error-path sibling (US-# or EDGE-# resolution)
- Every permission claim ("only admin can...") must trace to a formal role definition
- Absence of at least 1 error scenario per feature is a CONTENT GAP

### Vague terms to flag with replacement guidance
| Term | Replacement |
|------|-------------|
| "fast" | "response time < X ms at p95" |
| "easy to use" | "new user completes [task] without help in < X min" |
| "secure" | specific threat model + encryption + auth |
| "scalable" | "supports X concurrent users / Y req/s" |
| "real-time" | "latency < X ms" |
| "robust" | "handles [specific failures] with [specific behavior]" |
| "seamless" | specific integration/transition requirements |
```

**Files to change:**
- `.claude/skills/validation/validate-gate/SKILL.md` — expand Layer 1 and Layer 2

**Effort:** ~60 lines | **Priority:** P0 | **Layer:** 4

---

### R14. Developer Handoff Packet — Generated, with explicit derivation rule

**Design rules:**
- Automatically generated from authoritative sources
- Regenerable at any time
- Non-authoritative (does not redefine)
- Scoped per feature or sprint, not per entire project

**SST derivation table:**

| Packet section | Authority | If missing |
|---|---|---|
| Context & non-goals | feature-brief + NG-# registry | ⚠️ Flag |
| Actors & permissions | opportunity-pack actor map + feature-spec permission matrix (R11) | ⚠️ Flag |
| Business rules | feature-brief FB-# + feature-spec | ⚠️ Flag |
| Acceptance criteria | user-stories.md (filtered by feature) | ⚠️ Flag |
| Error handling matrix | feature-spec error matrix (R11) + EDGE-# resolutions | ⚠️ Flag |
| State machine | feature-spec (R11) | Skip if not applicable |
| API contracts | api-spec (filtered by feature) | Skip if not applicable |
| Data mutations & validation | database-spec + data-dictionary validation rules (R11) | ⚠️ Flag |
| Performance requirements | tech-spec NFR-# | ⚠️ Flag |
| Observability | quality-checklist observability (R11) | ⚠️ Flag |
| Tasks (impl-#) | implementation-plan | ⚠️ Flag |
| Open questions | ASM-# open + feature-brief outstanding questions | Always present |

**Upstream dependency rule:** The packet pulls from upstream docs. It does not generate content that doesn't exist upstream. If a section is missing, the packet flags it as `⚠️ MISSING — [source doc] does not contain this section. Run /elicit to identify the gap.`

**Files to create:**
- `.claude/skills/implementation/implementation-packet/SKILL.md` (~200 lines)
- `.claude/skills/implementation/implementation-packet/knowledge/template.md` (~80 lines)

**Effort:** ~280 lines | **Priority:** P0 | **Layer:** 3

---

### R15. `/elicit` command — Semantic stress-test

**When to use:**
1. After `ideate`, before `feature` or `discover`
2. After `requirements`, before `design`
3. When the user says: "I want to challenge what's been specified"

**Does not generate new product artifacts. Generates a findings report.**

**8 interrogation techniques:**

1. **Developer simulation** — "If I were implementing [feature], what would I still need to know?"
2. **Cross-doc consistency** — DB constraints vs data-dictionary vs API schema vs feature-spec
3. **Vague quantifier scan** — "fast", "secure", "many" without metrics
4. **NG-# violation scan** — Do downstream docs contradict non-goals?
5. **Missing error siblings** — For each happy-path UC-#, does a corresponding error-path exist?
6. **Permission matrix gap** — Permission claims without formal role definition?
7. **State machine completeness** — For entities with states, are all transitions documented (including forbidden)?
8. **EDGE-# resolution audit** — For each EDGE-#, does resolution exist downstream?

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

## Unresolved Edges (EL-E-#)
- EL-E-1: EDGE-4 identified in ideation, no downstream resolution found
```

**False positive awareness:** The validator must differentiate real placeholder vs template example vs quoted text vs reference docs.

**Files to create:**
- `.claude/commands/elicit.md` (~60 lines)
- `.claude/skills/validation/elicit/SKILL.md` (~150 lines)

**Effort:** ~210 lines | **Priority:** P0 | **Layer:** 4

---

### R16. Gate decisions persistence with rationale

**Evidence from code:**

`default_workflow_state()` in `state_defaults.py` has `gates: { discovery_gate: "pending" }`. Just status. No feedback, reason, or rejected approaches.

**What to do:**

```yaml
gates:
  discovery_gate:
    status: iterate
    feedback: "Vision needs to emphasize cost reduction, not speed"
    timestamp: "2026-03-24T14:30:00Z"
    rejected_approaches:
      - "Speed-focused value proposition"
    iteration_count: 1
    unresolved_objections: []
```

This feeds: workflow state, memory, downstream prompts.

**Files to change:**
- `state_defaults.py` — expand gates
- `validate-gate/SKILL.md` — save feedback on ITERATE/NO-GO
- `memory-sync.py` — propagate gate decisions

**Effort:** ~80 lines | **Priority:** P1 | **Layer:** 5

---

### R17. Correct-course cascade with automatic propagation

**Problem (D7):**
After change-proposal approval, downstream documents are not updated. The user must manually fix 5-10 files.

**Mechanism:**

1. User approves change-proposal.md
2. `/correct-course` **greps** all project docs for IDs mentioned in the change (removed PRD-F-#, changed US-#, etc.)
3. **Lists** every document that references an affected ID, with the specific line
4. **Generates** proposed diffs for each affected document (remove reference, update wording, change priority)
5. **Presents** before/after for user approval (one doc at a time)
6. **Applies** approved changes
7. **Updates** coverage-matrix, workflow-state, feature-status
8. If execution adapter enabled, **flags** which external issues need updates

**Files to change:**
- `.claude/skills/planning/correct-course/SKILL.md` — add reconciliation phase (~50 lines)
- `.claude/commands/correct-course.md` — expand command to include cascade (~15 lines)

**Effort:** ~65 lines | **Priority:** P1 | **Layer:** 5

---

### R18. Post-implementation feedback loop

**Problem:**
Gaps found by the dev during implementation don't feed back. Archetype packs don't improve. The same questions get missed in the next project.

**What to do:**

Create `/retro` command:
1. Ask the dev: "What decisions did you make on your own during implementation?"
2. For each answer, classify: in which phase should this have been captured?
3. Save as learning in `docs/ets/projects/{slug}/learnings/`
4. If pattern repeats 2+ times in different projects, suggest adding to the corresponding archetype probe

This is what transforms archetype packs into assets that improve over time.

**Files to create:**
- `.claude/commands/retro.md` (~30 lines)
- `.claude/skills/retrospective/dev-feedback/SKILL.md` (~70 lines)

**Effort:** ~100 lines | **Priority:** P1 late / P2 | **Layer:** 5

---

## Implementation Roadmap

### Phase 1 — Interview Method (5-7 days)

Objective: make discovery and interview significantly better.

| # | Improvement | Impact | Effort |
|---|---|---|---|
| R1 | Separate coverage-matrix and elicitation-state | Clean state, resumable interviews | ~180 lines |
| R2 | Story-based interviewing | 3x richer extraction | ~210 lines |
| R3 | Interview Snapshots (SNAP-#) | Synthesis without context loss | ~60 lines |
| R4 | Vague response escalation table | More specific answers | ~50 lines |
| R5 | "I don't know" differentiation | Better classified unknowns | ~40 lines |
| R12 | Fatigue management | Consistent quality | ~30 lines |
| **Phase 1 total** | | | **~570 lines** |

### Phase 2 — Semantic Coverage & Archetypes (4-6 days)

Objective: stop measuring coverage only by count.

| # | Improvement | Impact | Effort |
|---|---|---|---|
| R6 | Semantic coverage dimensions | Gates that check substance | ~100 lines |
| R7 | EDGE-# resolution tracking | No edge case silently disappears | ~60 lines |
| R8 | Archetype probe packs (3 initial) | Right questions for the type of problem | ~270 lines |
| R9 | Non-goals traceable (NG-#) | Detectable scope creep | ~120 lines |
| **Phase 2 total** | | | **~550 lines** |

### Phase 3 — Brainstorm, Validation & Handoff (5-7 days)

Objective: disciplined brainstorm, executable validation, consolidated handoff.

| # | Improvement | Impact | Effort |
|---|---|---|---|
| R10 | Brainstorm divergence/convergence + HMW bridge | Disciplined ideation | ~160 lines |
| R11 | Upstream template expansion | Structured content for packet | ~155 lines |
| R13 | Anti-placeholder / anti-vagueness validation | Placeholders don't pass | ~60 lines |
| R14 | Developer Handoff Packet | Dev gets everything in 1 document | ~280 lines |
| R15 | `/elicit` command (stress-test) | Ambiguities detected before code | ~210 lines |
| **Phase 3 total** | | | **~865 lines** |

### Phase 4 — Continuity & Change (3-5 days)

Objective: prevent drift and leverage real learning.

| # | Improvement | Impact | Effort |
|---|---|---|---|
| R16 | Gate decisions persistence | Phases don't repropose rejected ideas | ~80 lines |
| R17 | Correct-course cascade | Automatic downstream propagation | ~65 lines |
| R18 | Post-implementation feedback loop | Framework learns from experience | ~100 lines |
| **Phase 4 total** | | | **~245 lines** |

---

## Effort Summary

| Phase | Lines | Days |
|---|---|---|
| Phase 1 — Interview Method | ~570 | 5-7 |
| Phase 2 — Semantic Coverage | ~550 | 4-6 |
| Phase 3 — Brainstorm, Validation & Handoff | ~865 | 5-7 |
| Phase 4 — Continuity & Change | ~245 | 3-5 |
| **Total** | **~2,230** | **17-25** |

**Realistic note:** A solid first version can ship earlier. But a truly calibrated version — without fragile rules or prompt-only enforcement — should be treated as 3-4 weeks of work, not a few days. The line count captures code; it doesn't capture iteration, testing, and prompt calibration.

---

## Success Metrics

### Primary Metrics

| Metric | How to measure | Target |
|---|---|---|
| Questions dev had to invent | Ask dev at end of each feature | < 3 per feature |
| Semantic dimensions covered in 1st pass | % of mandatory dimensions = covered before gate | > 80% |
| Archetype probes answered sufficiently | % of probes with concrete answer | > 70% |
| Vague responses correctly escalated | % of vague responses that trigger follow-up | > 90% |
| Gate iterations | Average ITERATEs before GO | < 1.5 |
| Stories extracted vs abstract answers | Ratio of SNAP-# vs generic responses | > 60% story-based |
| EDGE-# resolution rate before Implementation Readiness Gate | % resolved or explicitly deferred | 100% |
| Rejected changes reappearing downstream | NG-# violations in later docs | 0 |
| Feedback loop yield | New archetype probes added per quarter from `/retro` | > 3 |

### Gold Metric

> How many product/behavior decisions did the dev have to invent because the documentation didn't answer?

This is the single best measure of the system's true quality.

---

## Definition of Done

A feature or product is only interview-complete when:

1. The problem is clear independently from the proposed solution
2. At least 3 story snapshots (SNAP-#) have been collected and validated by the user
3. Archetype-specific probes have been exhausted for all applicable archetypes
4. All mandatory semantic dimensions are covered or justified as not_applicable
5. Actors, operators, and approvers are explicit with permission matrix
6. Non-goals are explicit and traceable as NG-# IDs
7. Every EDGE-# has a resolution (US-#, FS-#, ADR, API error code) or explicit deferral as NG-#
8. Active assumptions are classified (open/deferred/assumed_default) with owners and deadlines
9. The spec has been stress-tested via `/elicit` with zero unresolved EL-# blockers
10. Error handling matrix, state machines, validation rules, and observability are documented in upstream sources
11. Everything is consolidated into a single implementation packet (derived, not authoritative)
12. Remaining unknowns are explicit enough that engineering knows what to answer before coding
13. Gate decisions and rejected approaches are persisted for downstream phases

---

## Evolution: v3 → v4 → v5

| Aspect | v3-AA | v3-Claude | v4-AA | v4-Claude | v5 (this) |
|---|---|---|---|---|---|
| State management | 2 files separated | Expanded coverage-matrix (merged) | 2 files + quality log | 2 files + SNAP per module | **2 files** with full schema for both |
| Interview method | Story-based concept | Story probes + sufficiency | Story-based + anti-patterns | Story probes + sufficiency + anti-patterns | **Both**: probes with sufficiency + anti-patterns |
| Snapshots | Not present | SNAP-# with format | Not present | SNAP-# with format | **SNAP-#** with format + anchor for reflection |
| EDGE-# tracking | Not present | Not present | `edge_resolution` map | Not present | **`edge_resolution`** (from v4-AA) |
| Upstream templates | Not present | Not present | R10 expansion (ES-#, permissions, etc.) | Not present | **R11 expansion** without new ES-# prefix |
| Archetypes | 3 initial | 6 initial | 3 initial + sufficiency table | 6 initial | **3 initial** + sufficiency criteria from v4-AA |
| Brainstorm | 5 stages | 6 phases with code | 5 stages | 6 phases with prerequisites | **6 phases** + 3 techniques + SNAP prerequisite |
| Handoff packet | SST derivation rule | Template + generation | SST + upstream dependency | SST + template + generation | **SST** + upstream dependency + missing-section flags |
| Change management | Layer 5 concept | R14 gate persistence | R15 cascade with diffs | Gate persistence only | **Cascade** (v4-AA) + gate persistence + `/retro` |
| Effort estimate | 16-25 days | 9-13 days | 16-24 days | 15-24 days | **17-25 days** |
| Definition of Done | Not present | Not present | 12 criteria | Not present | **13 criteria** (added SNAP minimum) |

### The fundamental principle

> **Extract first, verify second.** Concrete stories produce 80% of coverage naturally. Archetypes, semantic dimensions, EDGE-# resolution tracking, and `/elicit` capture the remaining 20% that stories didn't reveal.

---

## Conclusion

The ETUS doesn't need to become a "heavier" framework. It needs to become a framework that is:

- **Story-driven** in extraction (not abstract-question-driven)
- **Explicit** in interview state (two separate files, resumable)
- **Semantic** in coverage (dimensions, not counts)
- **Traceable** in edge case resolution (every EDGE-# resolved or deferred)
- **Disciplined** in brainstorm (6 phases, divergence/convergence separated)
- **Structured** in upstream templates (so the handoff packet has content to pull)
- **Mechanical** in validation (anti-placeholder, anti-vagueness, false-positive-aware)
- **Safe** in developer handoff (derived, regenerable, SST-compliant)
- **Resilient** to changes (cascade propagation, gate rationale persistence)
- **Honest** about what it doesn't know yet (differentiated "I don't know", assumed defaults marked)

The future of the ETUS is to move from a well-documented methodology to an operational system of elicitation, decision, and handoff.
