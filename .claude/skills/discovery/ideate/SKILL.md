---
name: ideate
description: >
  Use when extracting a raw idea into a coverage-driven discovery package before
  writing product docs. Also triggers on 'ideate', 'brainstorm a feature',
  'explore the problem space', 'capture all use cases', 'JTBD', 'journeys',
  'edge cases', or 'turn this idea into something implementation-ready'.
model: opus
version: 1.1.0
argument-hint: "[subcommand] [idea description, link, file, or issue]"
compatibility: "Optional: Slack MCP, Figma MCP, audio/transcript inputs, and external issue tracker adapters (for example, Linear)"
---

# Ideate Skill

## PURPOSE

This skill creates the **opening diamond** of the ETUS workflow.

Its job is not to jump straight into solutions. Its job is to:
- collect raw signals from mixed sources
- extract the real problem behind the proposed solution
- map actors, JTBDs, journeys, use cases, and edge cases
- pressure-test assumptions
- produce a reusable upstream package for Discovery, Feature, Bug, or Spike work

The ideate phase exists because strong brainstorming without strong elicitation
still leaves blind spots. This skill is **coverage-driven**, not merely
interview-driven.

## SUBCOMMAND MODE

The ideate skill exposes a hybrid interface:
- `/ideate` runs the full flow end-to-end
- `/ideate <subcommand>` runs one semantic block and saves checkpoints

Supported public subcommands:
- `ingest`
- `problem`
- `actors`
- `jobs`
- `journeys`
- `cases`
- `edges`
- `assumptions`
- `brainstorm`
- `synth`
- `status`

Interpretation rules:
1. If the first argument matches a known subcommand, treat the remainder as context input.
2. If the first argument does not match a known subcommand, treat the whole argument as context and run the default flow.
3. `status` is read-only and should inspect progress, blockers, and the next recommended step.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** None. This is the new root artifact for every mode.

**ENRICHES** (load silently if available):
- `docs/ets/.memory/decisions.md`
- `docs/ets/.memory/preferences.md`
- `docs/ets/.memory/patterns.md`
- Existing product docs relevant to the same work item

## ARTIFACT SAVE RULE

This skill MUST write both of its outputs before declaring completion:

1. `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
2. `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml`

If either write fails, report the failure and stop.

Subcommand checkpoint behavior:
- Every subcommand updates only its owned blocks in `opportunity-pack.md`
- Every subcommand updates only its owned domains and step states in `coverage-matrix.yaml`
- `brainstorm` must not mark itself complete if minimum problem coverage is not satisfied
- `synth` must not conclude if critical unresolved items remain

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard, but with an important twist:
it separates **elicitation** from **ideation**.

1. **One question per message** — Ask one focused question, wait for the answer,
   then move forward.
2. **Coverage before creativity** — Do not run BMAD techniques until the problem
   space has minimum coverage.
3. **3-4 suggestions for choices** — When choosing direction or method, present
   structured options and a recommendation.
4. **Section-by-section approval** — Present synthesis by module and confirm it
   before continuing.
5. **Track unknowns explicitly** — Every unknown must be classified as
   `resolved`, `assumed`, or `open`.
6. **Show progress** — The user should always know what has been covered and what
   remains uncovered.
7. **Checkpoint after each semantic block** — Persist progress so the user can
   pause, audit, and resume safely.

## MIXED-SOURCE INPUT

The ideate phase accepts mixed-source input. Treat all of the following as valid:
- direct user conversation
- pasted text snippets
- Slack links or exported discussion context
- Linear issues
- docs, notes, strategy briefs
- Figma links
- transcripts or summaries from voice/audio inputs

Normalize inputs into four buckets:
- **Confirmed fact**
- **Stakeholder opinion**
- **Hypothesis**
- **Decision already taken**

If sources disagree, record the contradiction instead of silently resolving it.

## Elicitation Entry Rule

BEFORE asking anything in any module:
1. Read `knowledge/elicitation-state.yaml`
2. Find the corresponding module
3. If status == "covered" → summarize what exists, ask if user wants to go deeper
4. If status == "in_progress" → continue from current_probe
5. If status == "not_started" → start with story probe (see knowledge/story-probes.md)
6. After each question → update elicitation-state.yaml
7. After each story → generate SNAP-# (see Story Snapshots below)

## COVERAGE MODULES

Run these modules in order. Skip only when the user explicitly confirms the
module is irrelevant for this work item.

Public subcommand mapping:
- `ingest` -> Source Ingestion
- `problem` -> Problem Framing
- `actors` -> Actor Map
- `jobs` -> JTBD Extraction
- `journeys` -> Journey Sweep
- `cases` -> Use Case Matrix
- `edges` -> Edge Case Sweep
- `assumptions` -> Hypotheses & Unknowns
- `brainstorm` -> Solution Direction Brainstorm
- `synth` -> Synthesis & Prioritized Handoff
- `status` -> Progress inspection only

### 1. Source Ingestion
- What information already exists?
- Which sources are trustworthy?
- What claims conflict?

### 2. Problem Framing
- "Tell me about the last time this problem happened. What happened? Who was involved? What went wrong?"
- "What did people do after it went wrong? Was there a workaround?"
- "If we do nothing, what happens in the next 3 months?"
- "Is what you described the root problem, or a symptom of something deeper?"
- Refer to `knowledge/story-probes.md` for additional story-based probes.

After Problem Framing: propose likely archetypes based on stories collected.
"Based on what you've told me, this looks like a [Workflow/Approval | API/Integration | Import/Export] pattern. Does that sound right?"
Store detected archetypes in elicitation-state.yaml (active_archetypes).
Archetype probes run AFTER Journey Sweep.

### 3. Actor Map
- "In the story you told me, who else was involved? Who approved? Who was affected even without participating?"
- "Who benefits the most if this problem is solved?"
- "Who could block this workflow or make it fail?"
- "Is there someone who should NOT be optimized for — an anti-user or negative persona?"
- Refer to `knowledge/story-probes.md` for additional actor-discovery probes.

### 4. JTBD Extraction
- Functional job
- Emotional job
- Social job
- Trigger, anxiety, progress desired, current alternative
Use `.claude/skills/discovery/jtbd-extractor/SKILL.md` as the specialist guide.

### 5. Journey Sweep
- Before / during / after
- new user / returning user / blocked user
- happy path / alternate path / failure path
- channel, device, and context variations
Use `.claude/skills/discovery/journey-sweep/SKILL.md` as the specialist guide.

### Archetype Probe Execution

After Journey Sweep module completes:
1. Read active_archetypes from elicitation-state.yaml
2. For each confirmed archetype, load probe pack from knowledge/elicitation-archetypes/{name}.md
   (Note: probe packs are at .claude/skills/discovery/elicitation-archetypes/)
3. For each probe in the pack:
   a. Ask the probe question
   b. Evaluate sufficiency per the probe's criteria
   c. If insufficient → escalate (same as vague response handling)
   d. Mark probe as done in elicitation-state.yaml
4. Add archetype-specific dimensions to coverage-matrix.yaml semantic_dimensions.archetype_dimensions
5. Update dimension statuses based on probe answers
6. Probes are marked as: covered (sufficient answer), deferred (with rationale), or not_applicable

### 6. Use Case Matrix
- main trigger
- actor
- precondition
- action
- expected result
- observable success
Use `.claude/skills/discovery/use-case-matrix/SKILL.md` as the specialist guide.

### 7. Edge Case Sweep
- invalid states
- exception flows
- abuse or misuse flows
- rollback or manual fallback
- dependency failure and partial-success scenarios
Use `.claude/skills/discovery/edge-case-sweep/SKILL.md` as the specialist guide.

### 8. Constraints & Guardrails
- technical constraints
- business constraints
- legal/compliance constraints
- timeline and resourcing constraints
- what must NOT get worse

### 9. Hypotheses & Unknowns
- assumptions without evidence
- open questions
- validation needed before planning or implementation
Use `.claude/skills/discovery/assumption-audit/SKILL.md` as the specialist guide.

### 10. Solution Direction Brainstorm

#### Prerequisite
Brainstorm is BLOCKED until:
- Problem defined
- >= 1 actor
- >= 1 JTBD
- >= 1 journey
- >= 3 story snapshots (SNAP-#)

#### Phase A: Themes (convergence over evidence)
- Group story snapshots by theme
- Present grouping to user: "I see N themes: [X], [Y], [Z]. Does this make sense?"

#### Phase B: HMW Bridge
- For each theme, generate 2-3 HMW (How Might We) statements
- Example: "How might we [reduce approval time] without [compromising the audit trail]?"
- User selects the most relevant HMWs (max 3)

#### Phase C: Diverge (no judgment)
- For each selected HMW, generate 3-5 solution options
- Rule: DO NOT criticize, DO NOT evaluate, DO NOT say "but"
- Build on ideas ("what if also...", "what if instead...")
- Technique: Crazy 8s — rapid ideation, quantity over quality

#### Phase D: Cluster & Select
- Group similar ideas into clusters
- Present clusters to user
- User selects 2-3 directions to deepen
- Technique: Gut Check — quick confidence vote before deep analysis

#### Phase E: Stress Test (convergence)
- For each selected direction: tradeoffs, risks, what can go wrong
- Evaluate against the 4 risks: value, usability, viability, feasibility
- Ask: "What's the biggest reason this could fail?"

#### Phase F: Assumptions
- For each direction: "What needs to be true for this to work?"
- Register each as ASM-# with risk level and validation path
- Connect to solution-discovery downstream

### 11. Synthesis & Prioritized Handoff
Summarize what should feed the next artifact:
- Product mode -> project-context + product-vision
- Feature mode -> feature-brief
- Bug mode -> tech-spec-standalone
- Spike mode -> spike

## MINIMUM COVERAGE THRESHOLDS

**Source of truth for mandatory dimensions:** `MODE_DIMENSION_RULES` in `.claude/hooks/state_defaults.py`.
Coverage-matrix.yaml stores dimension status but does NOT define which are mandatory.
The active mode determines which dimensions must be "covered" before the gate passes.

The phase is not complete until the coverage matrix reaches the minimum
threshold for the detected mode.

### Product
- >= 2 actors
- >= 2 JTBDs
- >= 2 journeys
- >= 4 use cases
- >= 3 edge cases
- >= 3 assumptions

### Feature
- >= 1 primary actor
- >= 1 JTBD
- >= 1 journey
- >= 2 use cases
- >= 2 edge cases
- >= 1 assumption

### Bug
- >= 1 affected actor
- >= 1 failure journey
- >= 1 reproduction use case
- >= 2 edge/failure states

### Spike
- >= 1 decision to make
- >= 2 hypotheses or options
- >= 1 success criterion for the spike outcome

## OUTPUT FORMAT

### opportunity-pack.md

Use `knowledge/template.md`.

This document must contain:
- problem and context
- evidence register
- actor map
- JTBD inventory
- journey inventory
- use case matrix
- edge case register
- constraints and guardrails
- assumptions and open questions
- initial solution directions
- prioritized handoff per mode

### coverage-matrix.yaml

Use `knowledge/coverage-matrix.yaml`.

This file tracks:
- `ACT-#`
- `JTBD-#`
- `JOUR-#`
- `UC-#`
- `EDGE-#`
- `ASM-#`
- status: `not_started | in_progress | covered | assumed | deferred | blocked`
- downstream linkage targets (`FB-#`, `PRD-F-#`, `US-#`, `impl-#`)
- subcommand progress state
- last completed step
- next recommended step

## IDEATION READINESS GATE

Before completion, validate:
- [ ] Problem is described independently from the solution
- [ ] At least one primary actor is identified
- [ ] JTBD coverage meets mode threshold
- [ ] Journey coverage meets mode threshold
- [ ] Use-case coverage meets mode threshold
- [ ] Edge-case coverage meets mode threshold
- [ ] Guardrails are explicit
- [ ] Blocking questions are explicit

If any item fails, mark the opportunity pack as draft and tell the user what is
missing.

The gate output must explicitly say:
- which subcommand is incomplete
- whether the issue is a blocker or a deferable gap
- which command the user should run next (for example `/ideate jobs`)

## Story Snapshots (SNAP-#)

After each extracted story, BEFORE moving to the next question:
1. Generate a SNAP-# with: who told it, context, what happened, key quote, what went wrong, current workaround, detected opportunity, IDs fed
2. Present to user: "Does this summary capture what you told me? Anything I got wrong?"
3. Record SNAP-# ID in elicitation-state.yaml under current module
4. Update coverage-matrix.yaml with any new IDs extracted

## Vague Response Handling

When an answer matches any pattern in knowledge/vague-response-escalation.md:
1. Fire the corresponding escalation question
2. Increment vague_count in elicitation-state.yaml
3. If 3+ consecutive vague answers: trigger reflection checkpoint

## Handling "I Don't Know"

When the user responds "I don't know", "good question", "I never thought about this":
Ask: "Help me classify this:
A) Do you know who would know? → I register as ASM-# open with owner
B) Is it safe to leave for later? → I register as ASM-# deferred
C) Could this change what we're building? → I need to explore more"
If answer is C: ask 2-3 more questions before moving on.

## Fatigue Management

After configurable threshold (default: 15 substantive questions):
1. Offer: continue / pause and resume later / accept defaults for non-mandatory dimensions
2. Mandatory dimensions (problem_clarity, failure_modes, permissions) CANNOT be accepted as defaults
3. Non-mandatory defaults registered as ASM-# assumed_default with revisit_required: true
4. Pause persists checkpoint in elicitation-state.yaml

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the Opportunity Pack structure.
- Read `knowledge/coverage-matrix.yaml` for the machine-readable coverage format.
- Read `knowledge/elicitation-state.yaml` for the interview state template.
- Read `knowledge/story-probes.md` for story-based elicitation probes by module.
- Read `knowledge/vague-response-escalation.md` for vague-response patterns and escalation questions.
- Read `.claude/skills/discovery/jtbd-extractor/SKILL.md` for JTBD extraction.
- Read `.claude/skills/discovery/journey-sweep/SKILL.md` for journey mapping.
- Read `.claude/skills/discovery/use-case-matrix/SKILL.md` for use-case coverage.
- Read `.claude/skills/discovery/edge-case-sweep/SKILL.md` for exception coverage.
- Read `.claude/skills/discovery/assumption-audit/SKILL.md` for explicit unknown management.
- Solution ideation uses the 6-phase brainstorm structure (Themes → HMW → Diverge → Cluster → Stress Test → Assumptions)
  defined in Module 10 above. Techniques: HMW + clustering (always), Crazy 8s (Phase C), Gut Check (Phase D).

## CLOSING SUMMARY

After saving both artifacts, display:

```text
Ideate phase complete.

Saved:
- docs/ets/projects/{project-slug}/discovery/opportunity-pack.md
- docs/ets/projects/{project-slug}/state/coverage-matrix.yaml

Coverage status:
- Actors: [count]
- JTBDs: [count]
- Journeys: [count]
- Use cases: [count]
- Edge cases: [count]
- Assumptions: [count]

Checkpoints:
- Last completed step: [step]
- Next recommended step: [step or downstream command]

Next recommended step:
- Product -> /discover
- Feature -> /feature
- Bug -> /bugfix
- Spike -> /spike
```
