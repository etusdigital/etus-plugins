# Implementation Plan: ETUS PMDocs Audit v5.1

**Date:** 2026-03-24
**Source:** `interview-elicitation-improvement-audit-v5.1-2026-03-24.md`
**Executor:** Claude (agent) with human review at checkpoints
**Scope:** All 4 phases, 18 recommendations, 41 tasks, ~2,285 lines across ~38 files
**Estimated effort:** 17-25 days

---

## Execution Protocol

This plan is optimized for agent execution. Each task follows this contract:

```
TASK FORMAT:
- id: T-{phase}.{sequence}
- maps_to: R# from audit v5.1
- files: exact paths to read, create, or edit
- action: CREATE | EDIT | ADD_SECTION | REWRITE_SECTION
- input: what to read first (dependencies)
- output: what the file should contain after the task
- acceptance: how to verify the task is done
- depends_on: [T-x.y] — must be completed first
```

**Agent rules:**
1. Before editing any file, READ IT FIRST to understand current structure
2. After each task, verify the acceptance criteria
3. At each checkpoint, pause for human review
4. Never create a new ID prefix without explicit approval (P5)
5. All content in English
6. **Multi-phase files:** The following files are edited across multiple phases. ALWAYS re-read the full file before each edit to avoid overwriting previous changes:
   - `ideate/SKILL.md` → Phase 1 (T-1.5a/b/c), Phase 2 (T-2.4), Phase 3 (T-3.1)
   - `validate-gate/SKILL.md` → Phase 2 (T-2.1), Phase 3 (T-3.8), Phase 4 (T-4.2)
   - `state_defaults.py` → Phase 2 (T-2.5, T-2.10), Phase 4 (T-4.1)
   - `template.md` (opp-pack) → Phase 1 (T-1.6), Phase 2 (T-2.7), Phase 3 (T-3.3)
   - `discovery-agent.md` → Phase 1 (T-1.9), Phase 3 (T-3.2)
   - `check-traceability/SKILL.md` → Phase 2 (T-2.2, T-2.9)

---

## Phase 1 — Interview Method

**Objective:** Make discovery interviews significantly richer by switching from abstract questions to story-based extraction with persistent state.
**Dependencies:** None (this is the foundation)
**Estimated effort:** 5-7 days | ~570 lines

### T-1.1: Create `elicitation-state.yaml` template

**Maps to:** R1
**Action:** CREATE
**Files:**
- Create: `.claude/skills/discovery/ideate/knowledge/elicitation-state.yaml`

**Output:** Full YAML template with:
- `meta` block (mode, session_id, started_at, last_activity)
- `current_module`, `current_probe`, `questions_asked`, `stories_collected`
- `module_state` with all 10 modules (ingest, problem, actors, jobs, journeys, cases, edges, assumptions, brainstorm, synth) each with: status, questions_asked, stories_collected, snapshots, archetype_probes_done
- `response_quality` block (vague_count, escalated_count, dont_know_count, dont_know_classified)
- `fatigue` block (threshold: 15, current: 0, offered_pause: false)
- `pending_probes` list (empty)
- `unresolved_dimensions` list (empty)
- `reflection_due` boolean
- `active_archetypes` list (empty)
- `checkpoints` list (empty)

**Acceptance:**
- File exists at path
- Valid YAML (parseable)
- Contains all sections listed above
- Does NOT contain `questions_remaining` (rejected field)
- Contains `pending_probes` and `unresolved_dimensions` instead

**Depends on:** —

---

### T-1.2: Refactor `coverage-matrix.yaml` — strip interview state

**Maps to:** R1
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml`
- Edit: same file

**Input:** Current coverage-matrix has both coverage AND interview execution fields (step_status, active_step, last_completed_step).

**What to do:**
1. Remove interview execution fields: `step_status`, `active_step`, `last_completed_step`, `progress_summary` (if present)
2. Keep: `meta`, `coverage` (actors, jtbd, journeys, etc.), `readiness_gate`, `blocking_questions`, `pending_items`, `assumed_items`, `blockers`
3. Add new section `semantic_dimensions` with all 11 dimensions (status: missing for each)
4. Add new section `mandatory_dimensions` list
5. Add new section `edge_resolution` (empty map with comment showing format)
6. Add two new readiness_gate booleans: `all_mandatory_dimensions_covered: false`, `all_edges_resolved_or_deferred: false`

**Acceptance:**
- No interview execution fields remain
- `semantic_dimensions` has 11 dimensions (9 mandatory + 2 recommended + archetype_dimensions placeholder)
- `edge_resolution` section exists
- `readiness_gate` has the two new booleans
- Valid YAML

**Depends on:** —

---

### T-1.3: Create `story-probes.md` knowledge file

**Maps to:** R2
**Action:** CREATE
**Files:**
- Create: `.claude/skills/discovery/knowledge/story-probes.md`

**Output:** Markdown with:
- 6 core story probes, each with: question text, "sufficient when", "insufficient when"
- Anti-patterns section (4 patterns to avoid with explanation)
- Copy exactly from audit v5.1 R2

**Acceptance:**
- File exists
- Contains 6 numbered probes with sufficiency criteria
- Contains anti-patterns section

**Depends on:** —

---

### T-1.4: Create `vague-response-escalation.md` knowledge file

**Maps to:** R4
**Action:** CREATE
**Files:**
- Create: `.claude/skills/discovery/knowledge/vague-response-escalation.md`

**Output:** Markdown table with 10 vague patterns and their escalation reactions. Copy exactly from audit v5.1 R4.

**Acceptance:**
- File exists
- Contains 10 pattern→reaction pairs
- Each reaction references stories or asks for specifics (not abstract)

**Depends on:** —

---

### T-1.5a: Rewrite ideate SKILL.md — entry rule + story-first modules

**Maps to:** R1, R2, R3
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/ideate/SKILL.md`
- Edit: same file

**Changes:**

**1. Add Elicitation Entry Rule** (new section, before any module definition)
```
## Elicitation Entry Rule

BEFORE asking anything in any module:
1. Read `knowledge/elicitation-state.yaml`
2. Find the corresponding module
3. If status == "covered" → summarize what exists, ask if user wants to go deeper
4. If status == "in_progress" → continue from current_probe
5. If status == "not_started" → start with story probe (see knowledge/story-probes.md)
6. After each question → update elicitation-state.yaml
7. After each story → generate SNAP-# (see Story Snapshots below)
```

**2. Rewrite Module 2 (Problem Framing)** — replace abstract questions with story-based:
- Old: "What is the underlying problem?"
- New: "Tell me about the last time this problem happened. What happened? Who was involved? What went wrong?"
- Reference `knowledge/story-probes.md`

**3. Rewrite Module 3 (Actor Map)** — story-based:
- Old: "Who feels the pain directly?"
- New: "In the story you told me, who else was involved? Who approved? Who was affected without participating?"

**4. Add SNAP-# generation instruction** (new section after each extraction module):
```
## Story Snapshots (SNAP-#)

After each extracted story, BEFORE moving to the next question:
1. Generate a SNAP-# with: who told it, context, what happened, key quote, what went wrong, current workaround, detected opportunity, IDs fed
2. Present to user: "Does this summary capture what you told me? Anything I got wrong?"
3. Record SNAP-# ID in elicitation-state.yaml under current module
4. Update coverage-matrix.yaml with any new IDs extracted
```

**Acceptance:**
- Entry rule section exists before modules
- Modules 2 and 3 use story-based prompts
- SNAP-# generation instruction exists
- References both `knowledge/elicitation-state.yaml` and `knowledge/story-probes.md`

**Depends on:** T-1.1, T-1.2, T-1.3

---

### T-1.5b: Rewrite ideate SKILL.md — vague response + "I don't know" handling

**Maps to:** R4, R5
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/ideate/SKILL.md`
- Edit: same file

**Changes:**

**1. Add vague-response handling** (new section):
```
## Vague Response Handling

When an answer matches any pattern in knowledge/vague-response-escalation.md:
1. Fire the corresponding escalation question
2. Increment vague_count in elicitation-state.yaml
3. If 3+ consecutive vague answers: trigger reflection checkpoint
```

**2. Add "I Don't Know" handling** (new section):
```
## Handling "I Don't Know"

When the user responds "I don't know", "good question", "I never thought about this":
Ask: "Help me classify this:
A) Do you know who would know? → I register as ASM-# open with owner
B) Is it safe to leave for later? → I register as ASM-# deferred
C) Could this change what we're building? → I need to explore more"
If answer is C: ask 2-3 more questions before moving on.
```

**Acceptance:**
- Vague-response handling section exists referencing `knowledge/vague-response-escalation.md`
- "I Don't Know" handling section exists with 3 classifications (A/B/C)
- References `knowledge/elicitation-state.yaml` for vague_count increment

**Depends on:** T-1.5a, T-1.4

---

### T-1.5c: Rewrite ideate SKILL.md — fatigue management + archetype detection hint

**Maps to:** R5, R6, R9
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/ideate/SKILL.md`
- Edit: same file

**Changes:**

**1. Add Fatigue Management** (new section):
```
## Fatigue Management

After configurable threshold (default: 15 questions):
1. Offer: continue / pause and resume later / accept defaults for non-mandatory dimensions
2. Mandatory dimensions CANNOT be accepted as defaults
3. Defaults registered as ASM-# assumed_default with revisit_required: true
```

**2. Add archetype detection hint** (in existing module flow, after Problem Framing):
```
After Problem Framing: propose likely archetypes based on stories collected.
"Based on what you've told me, this looks like a [Workflow/Approval | API/Integration | Import/Export] pattern. Does that sound right?"
Store detected archetypes in elicitation-state.yaml (active_archetypes).
Archetype probes run AFTER Journey Sweep (R9).
```

**Acceptance:**
- Fatigue management section exists with configurable threshold
- Mandatory dimensions protected from default acceptance
- Archetype detection hint exists after Problem Framing
- References `knowledge/elicitation-state.yaml` for active_archetypes

**Depends on:** T-1.5a

---

### T-1.6: Add Story Snapshots section to opportunity-pack template

**Maps to:** R3
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/ideate/knowledge/template.md`
- Edit: same file

**What to do:** Add a new `## Story Snapshots` section between "Evidence Register" and "Actor Map":

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

**Acceptance:**
- Section exists in template between Evidence Register and Actor Map
- SNAP-# format matches spec

**Depends on:** —

---

### T-1.7: Rewrite jtbd-extractor SKILL.md — story-first

**Maps to:** R2
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/jtbd-extractor/SKILL.md`
- Edit: same file

**What to do:**
1. Add same Elicitation Entry Rule (reads elicitation-state.yaml)
2. Replace extraction prompts:
   - Old: "What job is this person trying to get done?"
   - New: "Before thinking about the solution: what was this person trying to do at that moment? What would make them say 'it was worth it'?"
3. Reference `knowledge/story-probes.md` and `knowledge/vague-response-escalation.md`

**Acceptance:**
- Entry rule exists
- Primary prompts are story-based
- References shared knowledge files

**Depends on:** T-1.5a, T-1.3, T-1.4

---

### T-1.8: Rewrite feature-brief SKILL.md — story-first

**Maps to:** R2
**Action:** EDIT
**Files:**
- Read: `.claude/skills/planning/feature-brief/SKILL.md`
- Edit: same file

**What to do:**
1. Add Elicitation Entry Rule
2. Rewrite Q1:
   - Old: "What feature are you documenting?"
   - New: "Tell me about a concrete situation where the user would need this feature. What did they try to do? Where did they get stuck?"
3. Reference shared knowledge files

**Acceptance:**
- Q1 is story-based
- Entry rule exists
- References knowledge files

**Depends on:** T-1.5a, T-1.3, T-1.4

---

### T-1.9: Rewrite discovery-agent.md — story-based + "I don't know"

**Maps to:** R2, R5
**Action:** EDIT
**Files:**
- Read: `.claude/agents/discovery-agent.md`
- Edit: same file

**What to do:**
1. Rewrite "Problem Interview" section to use story-based probes instead of 5W2H abstract questions
2. Add "Handling Uncertainty" section with the 3-type "I don't know" classifier
3. Reference `knowledge/story-probes.md`

**Acceptance:**
- Problem Interview uses story-first approach
- "Handling Uncertainty" section exists with A/B/C classification
- References shared knowledge

**Depends on:** T-1.3

---

### T-1.10: Add "I don't know" handling to planning-agent.md

**Maps to:** R5
**Action:** EDIT
**Files:**
- Read: `.claude/agents/planning-agent.md`
- Edit: same file

**What to do:** Add "Handling Uncertainty" section (same as T-1.9)

**Acceptance:**
- Section exists with A/B/C classification

**Depends on:** —

---

### T-1.11: Expand assumption-audit status options

**Maps to:** R5
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/assumption-audit/SKILL.md`
- Edit: same file

**What to do:** Expand status options from `resolved | assumed | open` to:
- `resolved` — confirmed answer
- `open` — conscious gap, has owner + deadline
- `deferred` — conscious defer, has justification
- `assumed_default` — fatigue-accepted, `revisit_required: true`
- `unconscious_gap` — "never thought about it", deepened before moving on

**Acceptance:**
- All 5 statuses documented
- Each status has clear definition and treatment

**Depends on:** —

---

### T-1.12: Add entry rules to remaining sub-skills

**Maps to:** R1
**Action:** EDIT (4 files)
**Files:**
- `.claude/skills/discovery/journey-sweep/SKILL.md`
- `.claude/skills/discovery/edge-case-sweep/SKILL.md`
- `.claude/skills/discovery/use-case-matrix/SKILL.md`
- `.claude/skills/discovery/assumption-audit/SKILL.md`

**What to do:** Add the same Elicitation Entry Rule to each (6-line block reading elicitation-state.yaml).

**Acceptance:**
- Each file has the entry rule section
- Each references `elicitation-state.yaml`

**Depends on:** T-1.1

---

### 🔍 CHECKPOINT 1 — Human Review

**What to review:**
- [ ] elicitation-state.yaml template is complete and parseable
- [ ] coverage-matrix.yaml no longer has interview execution fields
- [ ] story-probes.md and vague-response-escalation.md exist with correct content
- [ ] ideate SKILL.md has all new sections: entry rule + story-first (T-1.5a), vague + "I don't know" (T-1.5b), fatigue + archetype hint (T-1.5c)
- [ ] jtbd-extractor, feature-brief, discovery-agent rewritten story-first
- [ ] All sub-skills have entry rules
- [ ] Run: `grep -r "questions_remaining" .claude/` → should return 0 results
- [ ] Run: `python3 -c "import yaml; yaml.safe_load(open('.claude/skills/discovery/ideate/knowledge/elicitation-state.yaml'))"` → no error
- [ ] Run: `python3 -c "import yaml; yaml.safe_load(open('.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml'))"` → no error

**Mini-smoke test (functional):**
- [ ] Open ideate SKILL.md and verify: the first question in Module 2 starts with a story probe (not "What is the underlying problem?")
- [ ] Verify: SNAP-# generation instruction appears BEFORE any "move to next question" instruction
- [ ] Verify: `grep -c "elicitation-state.yaml" .claude/skills/discovery/ideate/SKILL.md` → >= 4 (entry rule + vague + fatigue + archetype)
- [ ] Verify: `grep -c "story-probes.md" .claude/skills/discovery/ideate/SKILL.md` → >= 1

---

## Phase 2 — Semantic Coverage & Archetypes

**Objective:** Stop measuring coverage by count only. Add semantic dimensions, EDGE-# resolution, archetypes, and non-goals.
**Dependencies:** Phase 1 (elicitation-state.yaml and coverage-matrix.yaml must exist)
**Estimated effort:** 4-6 days | ~550 lines

### T-2.1: Add semantic dimension check to validate-gate

**Maps to:** R7
**Action:** EDIT
**Files:**
- Read: `.claude/skills/validation/validate-gate/SKILL.md`
- Edit: same file

**What to do:**
1. In Layer 2 (Content Checks), add:
   ```
   ## Semantic Dimension Check
   For each mandatory dimension in coverage-matrix.yaml:
   - If status == "missing" AND no "not_applicable" justification → FAIL
   - If status == "partial" → WARN
   Mode-aware rules:
   - Product: all mandatory dimensions must be "covered"
   - Feature: all mandatory dimensions must be "covered"
   - Bug: only problem_clarity, failure_modes, success_signal required
   - Spike: only problem_clarity required
   ```
2. Add EDGE-# resolution check:
   ```
   ## EDGE Resolution Check
   For each EDGE-# in edge_resolution:
   - If status == "unresolved" → FAIL with gap description
   - failure_modes dimension is only "covered" when ALL EDGE-# are resolved or deferred
   ```

**Acceptance:**
- Layer 2 has semantic dimension check section
- Mode-aware rules documented
- EDGE-# resolution check exists
- Gate fails on unresolved EDGE-#

**Depends on:** T-1.2

---

### T-2.2: Add EDGE-# resolution chain to check-traceability

**Maps to:** R8
**Action:** EDIT
**Files:**
- Read: `.claude/skills/validation/check-traceability/SKILL.md`
- Edit: same file

**What to do:** Add a new validation rule:
```
## EDGE-# Resolution Chain
For each EDGE-# found in discovery artifacts:
1. Search downstream docs (user-stories, feature-spec, api-spec, tech-spec) for references
2. If found → status: resolved, via: [doc + section]
3. If not found → check NG-# registry for explicit deferral
4. If neither → flag as TRACEABILITY GAP: "EDGE-{N} has no downstream resolution"
```

**Acceptance:**
- New validation rule exists
- Covers: resolved via downstream doc, deferred via NG-#, or flagged as gap

**Depends on:** —

---

### T-2.3: Create archetype probe packs (3 files)

**Maps to:** R9
**Action:** CREATE (3 files + directory)
**Files:**
- Create directory: `.claude/skills/discovery/elicitation-archetypes/`
- Create: `.claude/skills/discovery/elicitation-archetypes/workflow-approval.md`
- Create: `.claude/skills/discovery/elicitation-archetypes/api-integration.md`
- Create: `.claude/skills/discovery/elicitation-archetypes/import-export.md`

**Output per file:**
- Title + archetype description
- 6-8 mandatory probes, each with: question, "sufficient when", "insufficient when"
- Anti-patterns for this archetype (3-4)
- Archetype-specific dimensions to add to coverage-matrix

**Content for each archetype:**

**workflow-approval.md:**
Probes: states, rejection flow, timeout/SLA, delegation, audit trail, reopen conditions
Dimensions: `state_machine_defined`, `invalid_transitions_documented`, `sla_timeout_defined`

**api-integration.md:**
Probes: auth+scopes, retry safety, idempotency keys, rate limits, partial failure, versioning, webhooks/replay
Dimensions: `idempotency_defined`, `error_contract_defined`, `retry_policy_defined`

**import-export.md:**
Probes: accepted formats, max size, malformed rows, preview, rollback, resume, duplicates, progress, permissions
Dimensions: `format_constraints_defined`, `failure_recovery_defined`, `volume_limits_defined`

**Acceptance:**
- 3 files exist in new directory
- Each has 6+ probes with sufficiency criteria
- Each has anti-patterns
- Each has archetype-specific dimensions

**Depends on:** —

---

### T-2.4: Add archetype activation to ideate SKILL.md

**Maps to:** R9
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/ideate/SKILL.md`
- Edit: same file

**What to do:** Add archetype execution section (AFTER Journey Sweep module):

```
## Archetype Probe Execution

After Journey Sweep module completes:
1. Read active_archetypes from elicitation-state.yaml
2. For each confirmed archetype, load probe pack from knowledge/elicitation-archetypes/{name}.md
3. For each probe in the pack:
   a. Ask the probe question
   b. Evaluate sufficiency
   c. If insufficient → escalate (same as vague response handling)
   d. Mark probe as done in elicitation-state.yaml
4. Add archetype-specific dimensions to coverage-matrix.yaml semantic_dimensions.archetype_dimensions
5. Update dimension statuses based on probe answers
```

**Acceptance:**
- Section exists after Journey Sweep
- References archetype files
- Updates both elicitation-state and coverage-matrix
- Probes marked as covered, deferred with rationale, or marked not applicable (NOT "exhausted")

**Depends on:** T-1.5c, T-2.3

---

### T-2.5: Add `NG-#` to state_defaults.py

**Maps to:** R10
**Action:** EDIT
**Files:**
- Read: `.claude/hooks/state_defaults.py`
- Edit: same file

**What to do:** Add to `ID_PATTERNS` dict:
```python
"non_goals": r"\bNG-\d+\b",
```

**Acceptance:**
- `ID_PATTERNS` contains `"non_goals"` key
- Regex matches `NG-1`, `NG-12`, etc.

**Depends on:** —

---

### T-2.6: Add NG-# extraction to feature_lifecycle.py

**Maps to:** R10
**Action:** EDIT
**Files:**
- Read: `.claude/hooks/feature_lifecycle.py`
- Edit: same file

**What to do:** Add NG-# to the ID extraction logic (wherever it scans for ACT-#, JTBD-#, etc.).

**Acceptance:**
- NG-# IDs are extracted from documents
- Included in traceability reports

**Depends on:** T-2.5

---

### T-2.7: Add NG-# section to opportunity-pack template

**Maps to:** R10
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/ideate/knowledge/template.md`
- Edit: same file

**What to do:** Add `## Non-Goals Registry` section between "Constraints & Guardrails" and "Assumptions":

```markdown
## Non-Goals Registry

### NG-1: [What NOT to do]
- **Statement:** [what must NOT happen]
- **Reason:** [why excluded]
- **Scope:** permanent | deferred_to_v2 | conditional
- **Adjacent behavior:** [valid functionality that neighbors this non-goal]
- **Downstream docs that must respect:** [list]
```

**Acceptance:**
- Section exists in template
- NG-# format matches spec

**Depends on:** —

---

### T-2.8: Add NG-# section to feature-brief template

**Maps to:** R10
**Action:** EDIT
**Files:**
- Read: `.claude/skills/planning/feature-brief/SKILL.md`
- Edit: same file

**What to do:** Expand Q4 ("What is this feature explicitly NOT doing?") to generate NG-# IDs with the standard format.

**Acceptance:**
- Q4 generates NG-# IDs
- Each NG-# has statement, reason, scope, adjacent behavior

**Depends on:** —

---

### T-2.9: Add NG-# violation check to check-traceability

**Maps to:** R10
**Action:** EDIT
**Files:**
- Read: `.claude/skills/validation/check-traceability/SKILL.md`
- Edit: same file

**What to do:** Add:
```
## NG-# Violation Check
For each NG-# in upstream docs:
1. Search downstream docs for behavior that contradicts the non-goal statement
2. If found → flag as NG VIOLATION: "NG-{N} says '{statement}' but {doc} contains '{contradicting text}'"
```

**Acceptance:**
- NG-# violation check exists
- Scans downstream docs against NG-# statements

**Depends on:** —

---

### T-2.10: Add semantic dimensions to state_defaults.py

**Maps to:** R7
**Action:** EDIT
**Files:**
- Read: `.claude/hooks/state_defaults.py`
- Edit: same file

**What to do:** Add a `SEMANTIC_DIMENSIONS` constant dict and a `MODE_DIMENSION_RULES` constant dict matching the mode-aware table from v5.1 R7.

```python
SEMANTIC_DIMENSIONS = {
    "problem_clarity": "missing",
    "trigger_and_preconditions": "missing",
    "core_behavior": "missing",
    "success_signal": "missing",
    "anti_requirements": "missing",
    "actors_and_permissions": "missing",
    "failure_modes": "missing",
    "data_mutations": "missing",
    "degraded_behavior": "missing",
    "side_effects": "missing",
    "observability": "missing",
}

MODE_DIMENSION_RULES = {
    "product": {
        "required": ["problem_clarity", "trigger_and_preconditions", "core_behavior", "success_signal", "anti_requirements", "actors_and_permissions", "failure_modes"],
        "conditional": ["data_mutations"],
        "recommended": ["degraded_behavior", "side_effects", "observability"],
    },
    "feature": {
        "required": ["problem_clarity", "trigger_and_preconditions", "core_behavior", "success_signal"],
        "conditional": ["anti_requirements", "actors_and_permissions", "failure_modes", "data_mutations", "side_effects", "observability"],
        "recommended": ["degraded_behavior"],
    },
    "bug": {
        "required": ["problem_clarity", "trigger_and_preconditions", "core_behavior", "success_signal", "failure_modes"],
        "conditional": ["actors_and_permissions", "data_mutations", "degraded_behavior", "side_effects", "observability"],
        "recommended": [],
    },
    "spike": {
        "required": ["problem_clarity"],
        "conditional": ["failure_modes"],
        "recommended": ["success_signal"],
    },
}
```

**Acceptance:**
- Both constants exist
- Mode rules match v5.1 R7 table
- All 4 modes defined

**Depends on:** —

---

### 🔍 CHECKPOINT 2 — Human Review

**What to review:**
- [ ] validate-gate has semantic dimension check with mode-aware rules
- [ ] check-traceability has EDGE-# resolution chain AND NG-# violation check
- [ ] 3 archetype files exist with 6+ probes each
- [ ] ideate SKILL.md has archetype execution section (after Journey Sweep)
- [ ] state_defaults.py has NG-# in ID_PATTERNS + SEMANTIC_DIMENSIONS + MODE_DIMENSION_RULES
- [ ] feature_lifecycle.py extracts NG-#
- [ ] Templates have NG-# sections
- [ ] Run: `grep -r "NG-" .claude/hooks/state_defaults.py` → should match
- [ ] Run: `python3 -c "from hooks.state_defaults import MODE_DIMENSION_RULES; print(list(MODE_DIMENSION_RULES.keys()))"` → `['product', 'feature', 'bug', 'spike']`

---

## Phase 3 — Brainstorm, Validation & Handoff

**Objective:** Disciplined brainstorm, executable validation, and a consolidated developer handoff packet.
**Dependencies:** Phase 1 + Phase 2
**Estimated effort:** 5-7 days | ~870 lines

### T-3.1: Rewrite brainstorm module in ideate SKILL.md

**Maps to:** R11
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/ideate/SKILL.md`
- Edit: same file (Module 10)

**What to do:** Replace existing Module 10 with 6-phase structure:

- Phase A: Themes (group snapshots by theme)
- Phase B: HMW Bridge (2-3 HMW per theme)
- Phase C: Diverge (3-5 options per HMW, NO judgment)
- Phase D: Cluster & Select (user picks 2-3 directions)
- Phase E: Stress Test (tradeoffs, risks, 4-risk evaluation)
- Phase F: Assumptions (what must be true, ASM-# with validation path)

Add prerequisite block:
```
Brainstorm is BLOCKED until:
- Problem defined
- >= 1 actor
- >= 1 JTBD
- >= 1 journey
- >= 3 story snapshots
```

**Acceptance:**
- 6 phases clearly labeled
- Prerequisite block exists with SNAP-# minimum
- Phase C has explicit "no judgment" rule
- Phase F generates ASM-# IDs
- Old brainstorm module fully replaced

**Depends on:** T-1.5a

---

### T-3.2: Rewrite discovery-agent.md "Creative Exploration" section

**Maps to:** R11
**Action:** EDIT
**Files:**
- Read: `.claude/agents/discovery-agent.md`
- Edit: same file

**What to do:** Replace brainstorm technique selection with reference to the 6-phase structure. Initial techniques: HMW + clustering (always), Crazy 8s (Phase C), Gut Check (Phase D).

**Acceptance:**
- Section references 6-phase structure
- Does NOT offer 4 techniques for user to pick (old approach)

**Depends on:** T-3.1

---

### T-3.3: Expand opportunity-pack template for brainstorm

**Maps to:** R11
**Action:** EDIT
**Files:**
- Read: `.claude/skills/discovery/ideate/knowledge/template.md`
- Edit: same file

**What to do:** Expand "Solution Directions" section to include: Themes, HMW statements, Raw ideas (per HMW), Clusters, Selected directions, Assumptions per direction.

**Acceptance:**
- Template has subsections for all 6 brainstorm phases
- Each subsection has clear format

**Depends on:** —

---

### T-3.4: Add error handling matrix to feature-spec

**Maps to:** R12
**Action:** EDIT
**Files:**
- Read: `.claude/skills/planning/feature-spec/SKILL.md`
- Edit: same file
- Read: `.claude/skills/planning/feature-spec/knowledge/template.md` (if exists)

**What to do:** Add 3 new mandatory sections:

**Error Handling Matrix:**
```
| Scenario | EDGE-# | Trigger | System Response | User Message | Retry? | Rollback? |
```

**State Machine (if >2 states):**
```
Mermaid diagram + valid transitions table + forbidden transitions + side effects per transition
```

**Permission Matrix:**
```
| Action | Role A | Role B | Role C |
```

**Acceptance:**
- 3 new sections in SKILL.md with instructions
- Template updated (if template file exists)
- Error matrix uses `EDGE-#` (not `ES-#`)

**Depends on:** —

---

### T-3.5: Add validation rules to data-dictionary

**Maps to:** R12
**Action:** EDIT
**Files:**
- Read: `.claude/skills/data-design/data-dictionary/SKILL.md`
- Edit: same file

**What to do:** Add "Validation Rules per Field" section:
```
For each dict.* field, add:
- Required: yes/no
- Format/regex: pattern
- Min/max: range
- Default value
- Valid example
- Invalid example
- Behavior on invalid input
```

**Acceptance:**
- Validation rules section exists
- Template format specified

**Depends on:** —

---

### T-3.6: Move observability authority to tech-spec

**Maps to:** R12
**Action:** EDIT (2 files)
**Files:**
- Read + Edit: `.claude/skills/architecture/tech-spec/SKILL.md`
- Read + Edit: `.claude/skills/implementation/quality-checklist/SKILL.md`

**What to do:**

**In tech-spec SKILL.md:** Add new section "Observability Requirements":
```
## Observability Requirements

For each feature or service boundary:
- Logs: event name, log level, structured fields
- Metrics: metric name, type (counter/gauge/histogram), labels
- Alerts: condition, severity, notification channel
- Dashboards: key views needed for operational monitoring
```

**In quality-checklist SKILL.md:** Change observability from "define requirements" to "validate implementation against tech-spec requirements":
```
Observability: validate that implementation covers all observability requirements defined in tech-spec.
If tech-spec has no observability section → flag as gap, do NOT define requirements here.
```

**Acceptance:**
- tech-spec has observability requirements section as authoritative source
- quality-checklist references tech-spec, does not define requirements
- Authority chain: tech-spec → quality-checklist (validation only)

**Depends on:** —

---

### T-3.7: Add idempotency/retry to api-spec

**Maps to:** R12
**Action:** EDIT
**Files:**
- Read: `.claude/skills/api-design/api-spec/SKILL.md`
- Edit: same file

**What to do:** Add per-endpoint section:
```
## Idempotency, Retry & Concurrency

For each mutation endpoint:
- Idempotency key: header/parameter name and generation strategy
- Retry safety: safe/unsafe, max retries, backoff
- Concurrency model: optimistic locking / pessimistic / last-write-wins
- Timeout: client timeout recommendation
```

**Acceptance:**
- Section exists for mutation endpoints
- Covers all 4 aspects

**Depends on:** —

---

### T-3.8: Expand validate-gate with anti-placeholder checks

**Maps to:** R13
**Action:** EDIT
**Files:**
- Read: `.claude/skills/validation/validate-gate/SKILL.md`
- Edit: same file

**What to do:**

**Layer 1 extension:**
```
### Anti-Placeholder Patterns (Layer 1)
Reject automatically if found in required sections:
- Text inside brackets: [SOMETHING], [USER], etc.
- NFR-# without a number: "fast", "quick", "scalable" without metric
- Given/When/Then with < 5 words per clause
- Empty table cells in required tables
- "TBD", "TODO", "to be defined", "a definir"
Exception: skip template files, example blocks, and quoted guidance.
```

**Layer 2 extension:**
```
### Vagueness Checks (Layer 2)
- Every NFR-# must contain at least one number
- Every US-# happy-path must have at least 1 error-path sibling
- Every permission claim must trace to a formal role definition
- Absence of error scenario per feature = CONTENT GAP

### Vague Terms Flag Table
| Term | Required Replacement |
| "fast" | "response time < X ms at p95" |
... (7 terms from v5.1 R13)
```

**Acceptance:**
- Layer 1 has anti-placeholder patterns with false-positive exception
- Layer 2 has vagueness checks and term flag table
- 7 vague terms with replacements

**Depends on:** —

---

### T-3.9: Create `/elicit` command

**Maps to:** R14
**Action:** CREATE (2 files)
**Files:**
- Create: `.claude/commands/elicit.md`
- Create: `.claude/skills/validation/elicit/SKILL.md`

**Output:**

**elicit.md (~60 lines):** Command definition that spawns the elicit skill. Accepts optional scope (feature name, phase).

**elicit/SKILL.md (~150 lines):**
- 8 interrogation techniques (developer simulation, cross-doc consistency, vague quantifier scan, NG-# violation, missing error siblings, permission matrix gap, state machine completeness, EDGE-# resolution audit)
- Output format with EL-A-#, EL-C-#, EL-B-#, EL-H-#, EL-D-#, EL-E-# categories
- False-positive awareness rules

**Acceptance:**
- Command file exists
- Skill file exists with 8 techniques
- Output format matches v5.1 R14
- Does NOT generate new product artifacts (findings only)

**Depends on:** —

---

### T-3.10: Create Developer Handoff Packet skill

**Maps to:** R15
**Action:** CREATE (2 files + directory)
**Files:**
- Create directory: `.claude/skills/implementation/implementation-packet/`
- Create: `.claude/skills/implementation/implementation-packet/SKILL.md`
- Create: `.claude/skills/implementation/implementation-packet/knowledge/template.md`

**Output:**

**SKILL.md (~200 lines):**
- SST derivation table (12 sections with authorities)
- Generation logic: read each authority doc, extract relevant section, format into packet
- Missing-section detection: if source doc lacks section → flag as `MISSING — run /elicit`
- Scope: per feature or per sprint
- Regeneration: packet can be regenerated at any time without side effects

**template.md (~80 lines):**
- Full packet template with all 12 sections
- Each section header includes `[Authority: {doc}]`
- Open questions section always present

**Acceptance:**
- SKILL.md has SST derivation table matching v5.1 R15
- Template has 12 sections
- Each section references authority
- Observability section references tech-spec (NOT quality-checklist)
- Missing-section flags reference `/elicit`
- Packet is marked as non-authoritative in header

**Depends on:** T-3.4, T-3.5, T-3.6, T-3.7

---

### 🔍 CHECKPOINT 3 — Human Review

**What to review:**
- [ ] ideate SKILL.md brainstorm is 6 phases with SNAP-# prerequisite
- [ ] feature-spec has error matrix, state machine, permission matrix sections
- [ ] tech-spec owns observability, quality-checklist only validates
- [ ] validate-gate has anti-placeholder Layer 1 + vagueness Layer 2
- [ ] `/elicit` command and skill exist with 8 techniques
- [ ] Implementation packet skill exists with SST derivation table
- [ ] Run: `grep -r "ES-" .claude/skills/` → should return 0 results (no ES-# prefix)
- [ ] Run: `grep -l "observability" .claude/skills/architecture/tech-spec/SKILL.md` → should match
- [ ] Run: `ls .claude/commands/elicit.md` → exists

---

## Phase 4 — Continuity & Change

**Objective:** Prevent drift and leverage real learning from implementation.
**Dependencies:** Phase 1-3
**Estimated effort:** 3-5 days | ~245 lines

### T-4.1: Expand gate decision storage in state_defaults.py

**Maps to:** R16
**Action:** EDIT
**Files:**
- Read: `.claude/hooks/state_defaults.py`
- Edit: same file

**What to do:** Find the gate defaults (currently `{ discovery_gate: "pending" }`) and expand to:
```python
def default_gate_state():
    return {
        "status": "pending",
        "feedback": "",
        "timestamp": "",
        "rejected_approaches": [],
        "iteration_count": 0,
        "unresolved_objections": [],
    }
```

**Acceptance:**
- Gate defaults have all 6 fields
- Function exists and is callable

**Depends on:** —

---

### T-4.2: Save gate feedback in validate-gate

**Maps to:** R16
**Action:** EDIT
**Files:**
- Read: `.claude/skills/validation/validate-gate/SKILL.md`
- Edit: same file

**What to do:** After ITERATE or NO-GO decision:
```
When gate result is ITERATE or NO-GO:
1. Ask user for feedback: "What needs to change?"
2. Save to workflow-state.yaml gate section:
   - feedback: user's feedback text
   - rejected_approaches: list of what was tried and failed
   - timestamp: current ISO timestamp
   - increment iteration_count
3. Propagate to memory via memory-sync.py
```

**Acceptance:**
- Gate section saves feedback on ITERATE/NO-GO
- Saves rejected approaches
- Increments iteration count

**Depends on:** T-4.1

---

### T-4.3: Propagate gate decisions in memory-sync.py

**Maps to:** R16
**Action:** EDIT
**Files:**
- Read: `.claude/hooks/memory-sync.py`
- Edit: same file

**What to do:** When syncing state, also extract gate decisions and write to `decisions.md` memory file via `memory-write.py decision`.

**Acceptance:**
- Gate decisions appear in memory
- Rejected approaches are persisted

**Depends on:** T-4.1

---

### T-4.4: Add cascade to correct-course skill

**Maps to:** R17
**Action:** EDIT
**Files:**
- Read: `.claude/skills/planning/correct-course/SKILL.md`
- Edit: same file

**What to do:** Add "Reconciliation Phase" after change-proposal approval:

```
## Reconciliation Phase

After user approves change-proposal:
1. Extract all IDs mentioned in the change (removed PRD-F-#, changed US-#, etc.)
2. Grep all project docs for these IDs
3. List every document that references an affected ID with the specific line
4. Generate proposed diffs for each affected document
5. Present before/after for user approval (one doc at a time)
6. Apply approved changes
7. Update: coverage-matrix, workflow-state, feature-status
8. If execution adapter enabled: flag which external issues need updates
```

**Acceptance:**
- Reconciliation phase exists after approval
- Steps 1-8 documented
- Presents diffs for approval (not auto-applies)

**Depends on:** —

---

### T-4.5: Expand correct-course command

**Maps to:** R17
**Action:** EDIT
**Files:**
- Read: `.claude/commands/correct-course.md`
- Edit: same file

**What to do:** Add mention of the reconciliation/cascade phase to the command definition.

**Acceptance:**
- Command references cascade
- Mentions ID-based grep + diff presentation

**Depends on:** T-4.4

---

### T-4.6: Create `/retro` command and skill

**Maps to:** R18
**Action:** CREATE (2 files + directory)
**Files:**
- Create: `.claude/commands/retro.md`
- Create directory: `.claude/skills/retrospective/dev-feedback/`
- Create: `.claude/skills/retrospective/dev-feedback/SKILL.md`

**Output:**

**retro.md (~30 lines):** Command that spawns the dev-feedback skill. Asks: which feature/project?

**dev-feedback/SKILL.md (~70 lines):**
```
## Dev Feedback Interview

1. Ask: "What decisions did you make on your own during implementation?"
2. For each answer:
   a. Classify: in which phase should this have been captured? (ideation/planning/design)
   b. Classify: which dimension was missing? (from semantic_dimensions)
   c. Would an archetype probe have caught this?
3. Save as learning in docs/ets/projects/{slug}/learnings/{date}-{feature}.md
4. If pattern repeats 2+ times across projects:
   → Suggest adding probe to corresponding archetype pack
   → Log suggestion for human approval
```

**Acceptance:**
- Command exists
- Skill exists with 4-step interview
- Saves to learnings directory
- Cross-project pattern detection described

**Depends on:** —

---

### T-4.7: Update CLAUDE.md with new commands, skills, and knowledge files

**Maps to:** All (framework documentation)
**Action:** EDIT
**Files:**
- Read: `CLAUDE.md`
- Edit: same file

**What to do:**

1. **Commands section:** Add `/elicit` and `/retro` with descriptions:
   ```
   /elicit            # Semantic stress-test: ambiguities, contradictions, gaps
   /retro             # Post-implementation feedback: capture what dev had to guess
   ```

2. **Framework Structure section:** Add new skills and knowledge files:
   ```
   skills/
   ├── validation/
   │   └── elicit/                    # Semantic stress-test (8 techniques)
   ├── implementation/
   │   └── implementation-packet/     # Developer Handoff Packet (SST-derived)
   ├── retrospective/
   │   └── dev-feedback/              # Post-implementation feedback loop
   └── discovery/
       ├── knowledge/
       │   ├── story-probes.md        # 6 story-based probes with sufficiency
       │   └── vague-response-escalation.md  # 10 vague patterns + escalation
       └── elicitation-archetypes/    # 3 archetype probe packs
           ├── workflow-approval.md
           ├── api-integration.md
           └── import-export.md
   ```

3. **Skills count:** Update "48 skills" to "51 skills" (added: elicit, implementation-packet, dev-feedback)

4. **Commands count:** Update "15 commands" to "17 commands" (added: elicit, retro)

5. **IDs section:** Add `SNAP-#` and `EL-#` to Auxiliary IDs

6. **SST table:** Add `elicitation-state.yaml` as exclusive document for interview execution state

**Acceptance:**
- CLAUDE.md lists `/elicit` and `/retro` in commands
- Framework structure includes all new directories and files
- Counts updated (51 skills, 17 commands)
- SNAP-# and EL-# documented in IDs section
- No stale references to old counts

**Depends on:** T-3.9, T-3.10, T-4.6

---

### 🔍 CHECKPOINT 4 — Final Review

**What to review:**
- [ ] state_defaults.py has expanded gate state with 6 fields
- [ ] validate-gate saves feedback on ITERATE/NO-GO
- [ ] memory-sync propagates gate decisions
- [ ] correct-course has reconciliation phase with ID-based grep + diffs
- [ ] `/retro` command and skill exist
- [ ] CLAUDE.md updated with new commands, skills, and counts
- [ ] Run full validation: `grep -r "ES-" .claude/` → 0 (no ES-# prefix anywhere)
- [ ] Run: `grep -r "questions_remaining" .claude/` → 0
- [ ] Run: `grep -c "NG-" .claude/hooks/state_defaults.py` → >= 1
- [ ] Run: `grep -c "/elicit\|/retro" CLAUDE.md` → >= 2
- [ ] Count new files created: should be ~12 new files
- [ ] Count files edited: should be ~25 files

---

## Post-Implementation Validation

After all 4 phases, run these global checks:

### V-1: YAML Validation
```bash
for f in $(find .claude/skills -name "*.yaml"); do
  python3 -c "import yaml; yaml.safe_load(open('$f'))" || echo "FAIL: $f"
done
```

### V-2: ID Consistency
```bash
# Verify NG-# is in ID_PATTERNS
python3 -c "from hooks.state_defaults import ID_PATTERNS; assert 'non_goals' in ID_PATTERNS"

# Verify SEMANTIC_DIMENSIONS exists
python3 -c "from hooks.state_defaults import SEMANTIC_DIMENSIONS; print(len(SEMANTIC_DIMENSIONS))"

# Verify MODE_DIMENSION_RULES has 4 modes
python3 -c "from hooks.state_defaults import MODE_DIMENSION_RULES; assert len(MODE_DIMENSION_RULES) == 4"
```

### V-3: No Rejected Patterns
```bash
# No ES-# prefix (rejected in P5)
grep -r "ES-\d" .claude/ && echo "FAIL: ES-# found" || echo "PASS"

# No questions_remaining (rejected field)
grep -r "questions_remaining" .claude/ && echo "FAIL" || echo "PASS"

# No observability defined in quality-checklist as authority
grep -l "Observability Requirements" .claude/skills/implementation/quality-checklist/SKILL.md && echo "FAIL: quality-checklist should validate, not define" || echo "PASS"
```

### V-4: New Files Inventory
```
Expected new files:
.claude/skills/discovery/ideate/knowledge/elicitation-state.yaml
.claude/skills/discovery/knowledge/story-probes.md
.claude/skills/discovery/knowledge/vague-response-escalation.md
.claude/skills/discovery/elicitation-archetypes/workflow-approval.md
.claude/skills/discovery/elicitation-archetypes/api-integration.md
.claude/skills/discovery/elicitation-archetypes/import-export.md
.claude/commands/elicit.md
.claude/skills/validation/elicit/SKILL.md
.claude/skills/implementation/implementation-packet/SKILL.md
.claude/skills/implementation/implementation-packet/knowledge/template.md
.claude/commands/retro.md
.claude/skills/retrospective/dev-feedback/SKILL.md
```

### V-5: Smoke Test
Run `/ideate` on a test feature and verify:
1. Story-based probes fire (not abstract questions)
2. SNAP-# generated after first story
3. Vague answer triggers escalation
4. "I don't know" triggers A/B/C classification
5. Archetype suggested after Problem Framing
6. Semantic dimensions tracked in coverage-matrix
7. Gate checks dimensions, not just counts

---

## Summary

| Phase | Tasks | New files | Edited files | Lines |
|---|---|---|---|---|
| Phase 1 — Interview | 14 | 3 | 9 | ~570 |
| Phase 2 — Coverage | 10 | 3 | 7 | ~550 |
| Phase 3 — Validation | 10 | 5 | 7 | ~870 |
| Phase 4 — Change | 7 | 2 | 6 | ~295 |
| **Total** | **41 tasks** | **13 new** | **~25 edited** | **~2,285** |

| Checkpoint | After | Key verifications |
|---|---|---|
| CP-1 | Phase 1 | YAML valid, story-probes exist, entry rules in all sub-skills |
| CP-2 | Phase 2 | Mode-aware dimensions, archetypes, NG-# in state_defaults |
| CP-3 | Phase 3 | 6-phase brainstorm, /elicit, packet, observability in tech-spec |
| CP-4 | Phase 4 | Gate persistence, cascade, /retro, CLAUDE.md updated |
| V-Final | All | Global YAML, ID consistency, no rejected patterns, smoke test |

---

## Task Dependency Graph

```
Phase 1:
T-1.1 (elicitation-state) ──┐
T-1.2 (coverage-matrix)  ───┼── T-1.5a (ideate: entry rule + story) ── T-1.5b (ideate: vague + idk) ── T-1.5c (ideate: fatigue + archetype)
T-1.3 (story-probes)     ───┘         │                                        │
T-1.4 (vague-escalation) ─────────────┘                                        │
T-1.6 (template SNAP)                                                          │
T-1.7 (jtbd) ← T-1.5a                                                         │
T-1.8 (feature-brief) ← T-1.5a                                                │
T-1.9 (discovery-agent) ← T-1.3                                               │
T-1.10 (planning-agent)                                                        │
T-1.11 (assumption-audit)                                                      │
T-1.12 (sub-skill entry rules) ← T-1.1                                        │

Phase 2:
T-2.1 (validate-gate semantic) ← T-1.2
T-2.2 (check-traceability EDGE)
T-2.3 (archetype files)
T-2.4 (archetype activation) ← T-1.5c, T-2.3
T-2.5 (NG-# state_defaults)
T-2.6 (NG-# feature_lifecycle) ← T-2.5
T-2.7 (NG-# opp-pack template)
T-2.8 (NG-# feature-brief)
T-2.9 (NG-# check-traceability)
T-2.10 (dimensions state_defaults)

Phase 3:
T-3.1 (brainstorm rewrite) ← T-1.5a
T-3.2 (discovery-agent brainstorm) ← T-3.1
T-3.3 (template brainstorm)
T-3.4 (feature-spec error/state/perm)
T-3.5 (data-dict validation)
T-3.6 (observability tech-spec)
T-3.7 (api-spec idempotency)
T-3.8 (validate-gate anti-placeholder)
T-3.9 (/elicit command + skill)
T-3.10 (handoff packet) ← T-3.4, T-3.5, T-3.6, T-3.7

Phase 4:
T-4.1 (gate state expansion)
T-4.2 (validate-gate feedback) ← T-4.1
T-4.3 (memory-sync gates) ← T-4.1
T-4.4 (correct-course cascade)
T-4.5 (correct-course command) ← T-4.4
T-4.6 (/retro command + skill)
T-4.7 (CLAUDE.md update) ← T-3.9, T-3.10, T-4.6
```

**Parallelizable tasks per phase:**
- Phase 1: T-1.1 + T-1.2 + T-1.3 + T-1.4 + T-1.6 in parallel → T-1.5a → T-1.5b + T-1.5c in parallel → T-1.7 + T-1.8 + T-1.9 + T-1.10 + T-1.11 + T-1.12 in parallel
- Phase 2: T-2.1 + T-2.2 + T-2.3 + T-2.5 + T-2.7 + T-2.8 + T-2.9 + T-2.10 in parallel → then T-2.4 + T-2.6
- Phase 3: T-3.1 + T-3.3 + T-3.4 + T-3.5 + T-3.6 + T-3.7 + T-3.8 + T-3.9 in parallel → then T-3.2 + T-3.10
- Phase 4: T-4.1 + T-4.4 + T-4.6 in parallel → then T-4.2 + T-4.3 + T-4.5 → then T-4.7
