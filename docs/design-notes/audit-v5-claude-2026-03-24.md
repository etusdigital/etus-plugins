# Audit v5-Claude: ETUS PMDocs — Elicitation, Coverage, Brainstorm and Developer Handoff

**Date:** 2026-03-24
**Framework version:** v5.3
**Base:** v4-AA (best architectural document) + 3 gap-closers identified in cross-analysis + all prior iterations
**Goal:** Make the ETUS exceptional at extracting product ideas from the PO's head — zero gaps — and producing documentation that lets a developer implement without guessing.

---

## Central Thesis

> **The ETUS is prompt-rich and enforcement-poor.**

The right rules exist as text inside skills, agent instructions, and templates — but not as persistent state, progression blockers, validators, or operational artifacts. The evolution needs:

1. Story-based interview that extracts concrete behavior instead of abstract opinions
2. Interview state machine that tracks where the conversation stopped and what quality was achieved
3. Semantic coverage that measures substance instead of counting items
4. Disciplined brainstorming that separates divergence from convergence
5. Executable validation that mechanically catches placeholders and vagueness
6. A consolidated developer handoff that respects SST
7. Change management that actually propagates
8. Upstream templates that generate the structured content the handoff packet needs

---

## 5 Layers

| Layer | Skills | Optimizes for |
|-------|--------|---------------|
| 1. Core Interview | ideate, discover, project-context, product-vision, feature-brief | Truth, concrete behavior, friction, constraints |
| 2. Structured Brainstorm | brainstorm module, solution-discovery | Option breadth, clustering, disciplined selection |
| 3. Translation | feature-brief, prd, user-stories, feature-spec | Specification fidelity, structured dev content |
| 4. Assurance | validate-gate, check-traceability, check-sst, new validators | Ambiguity detection, mechanical enforcement |
| 5. Change & Continuity | correct-course, state/handoffs, feedback | Drift protection, continuous learning |

---

## Diagnostics

**D1** — Interview produces abstract answers (asks "What is the problem?" instead of "Tell me about the last time").
**D2** — Coverage measures quantity, not substance (>= 3 edge cases passes regardless of relevance).
**D3** — Coverage state and interview state are conflated in one YAML.
**D4** — Discovery and brainstorm need different dynamics (currently mixed).
**D5** — Developer gets 10+ documents and assembles the puzzle alone.
**D6** — Scope change is the most underdeveloped area.
**D7** — Edge cases can be identified but never resolved (EDGE-# passes through pipeline unhandled).
**D8** — Upstream templates lack structured developer-critical content (no ES-#, no permission matrix, no validation rules).

---

## Recommendations

### R1. Separate `coverage-matrix.yaml` and `elicitation-state.yaml`

**`coverage-matrix.yaml`** — what is covered: IDs, semantic dimensions, edge resolution, blockers, readiness gate.
**`elicitation-state.yaml`** — how the conversation is going: current module/probe, questions asked, stories collected, response quality, fatigue, checkpoints.

```yaml
# elicitation-state.yaml (key fields)
current_module: actors
current_probe: "In the story you told me, who else was involved?"
questions_asked: 12
stories_collected: 3
module_state:
  problem: { status: covered, stories_collected: 2, snapshots: [SNAP-1, SNAP-2] }
  actors:  { status: in_progress, archetype_probes_done: false }
  brainstorm: { status: blocked, blocked_by: "Minimum coverage not met" }
response_quality: { vague_count: 2, escalated_count: 2, dont_know_classified: 1 }
fatigue: { threshold: 15, current: 12, offered_pause: false }
```

Entry rule: Read state → if covered, summarize → if in_progress, continue → if not_started, start with story probe → update after each question.

**Effort:** ~150 lines | **P0** | Layer 1

---

### R2. Story-based interviewing as primary extraction method

| Skill | Current | Story-based |
|---|---|---|
| ideate (Problem) | "What is the underlying problem?" | "Tell me about the last time this happened. What happened? Who was involved?" |
| ideate (Actors) | "Who feels the pain?" | "In the story, who else was involved? Who approved? Who was affected?" |
| jtbd-extractor | "What job is this person trying to get done?" | "What was this person trying to do? What would make them say 'it was worth it'?" |
| feature-brief Q1 | "What feature?" | "Tell me a concrete situation where the user needs this. Where did they get stuck?" |

5 reusable story probes with sufficiency criteria in `story-probes.md`.

**Effort:** ~210 lines | **P0** | Layer 1

---

### R3. Interview Snapshots (SNAP-#)

After each extracted story, generate a structured snapshot in opportunity-pack:

```
SNAP-1: [title]
- Who told it / Context / What happened / Key quote
- What went wrong / Current workaround
- Detected opportunity / IDs fed: ACT-#, JTBD-#, EDGE-#
```

After generating, ask: "Does this capture what you told me? Anything I got wrong?" — This IS the reflection checkpoint, anchored in the story.

**Effort:** ~60 lines | **P0** | Layer 1

---

### R4. Separate divergence and convergence in brainstorm

HMW is in the wrong place. Its strongest use is as the **bridge between discovery and brainstorm**.

6 explicit phases:
1. **Themes** — Group snapshots by theme
2. **HMW Bridge** — Generate HMW statements per theme, user selects
3. **Diverge** — 3-5 options per HMW, NO criticism
4. **Cluster & Select** — User picks 2-3 directions
5. **Stress Test** — Tradeoffs, 4-risk evaluation
6. **Assumptions** — ASM-# with validation path

Prerequisite: >= 1 actor, >= 1 JTBD, >= 1 journey, >= 3 snapshots.
Initial techniques: HMW+clustering, Crazy 8s, Gut Check.

**Effort:** ~160 lines | **P0** | Layer 2

---

### R5. Semantic coverage dimensions with EDGE-# resolution tracking

```yaml
semantic_dimensions:
  # Mandatory (gate fails if false)
  problem_independent_of_solution: false
  actor_roles_and_permissions: false
  trigger_and_preconditions: false
  core_behavior_described: false
  success_signal_defined: false
  explicit_non_goals: false
  failure_modes_covered: false    # only TRUE when ALL edge_resolution entries resolved/deferred
  data_mutations_identified: false
  # Recommended (warning only)
  degraded_behavior: false
  side_effects_and_notifications: false
  observability_needs: false
  permissions_and_policy: false
  # Archetype-activated
  archetype_dimensions: {}

edge_resolution:
  EDGE-1: { status: unresolved, gap: "No US-# handles corrupted file" }
  EDGE-2: { status: resolved, via: "US-4 Given/When/Then" }
  EDGE-3: { status: deferred, via: "NG-2 — Phase 2" }
```

**Gate rules:** `failure_modes_covered` = true only when ALL EDGE-# are resolved or deferred. Requirements Gate and Implementation Gate also check edge_resolution.

**Effort:** ~120 lines | **P0** | Layer 4

---

### R6. Archetype-aware probe packs as post-story checklist

**Correct sequence:** Stories (R2) → Snapshot (R3) → **Archetype checklist** (R6). Archetypes are safety net, NOT primary extraction.

3 initial archetypes with probes + sufficiency criteria + anti-patterns:

| Archetype | Key probes |
|---|---|
| **Workflow/Approval** | States, transitions, forbidden transitions, timeout/SLA, delegation, reopen, audit |
| **API/Integration** | Auth, retry, rate limit, idempotency, partial failure, error contract, versioning |
| **Import/Export** | Formats, max size, malformed rows, preview, rollback, resume, progress, duplicates |

Later: CRUD/Backoffice, AI/Copilot, Billing/Subscription.

**Effort:** ~270 lines | **P0** | Layer 1

---

### R7. Non-goals as traceable objects (NG-#)

Add to ID_PATTERNS. Each NG-#: statement, reason, scope (permanent/deferred/conditional), adjacent_behavior, downstream_must_respect. Violation check in check-traceability. Section in opportunity-pack and feature-brief templates.

**Effort:** ~120 lines | **P0** | Layer 1, 4

---

### R8. Vague response escalation table

Shared knowledge file anchored in story probes:

| Pattern | Reaction |
|---|---|
| "fast" | "In the story, how long did it take? How long should it take?" |
| "secure" | "Secure against what? Last time something went wrong?" |
| "many/few" | "Give me a number. Tens, hundreds, thousands?" |
| "later" | "Blocks implementation? If yes, decide now. If no, ASM-# deferred." |
| "like [competitor]" | "What exactly? Describe the specific part." |
| "obvious" | "Explain as if I've never seen the system." |

**Effort:** ~50 lines | **P0** | Layer 1

---

### R9. "I don't know" differentiation

| Type | Treatment |
|---|---|
| Need to research | ASM-# open with owner + deadline |
| OK not to know now | ASM-# deferred with justification |
| Never thought about it | **Deepen first** — most valuable case. Ask 2-3 more questions before moving on. |

**Effort:** ~40 lines | **P0** | Layer 1

---

### R10. Fatigue management

After 15 questions: offer continue / pause / accept defaults. Blocking dimensions (problem, failure_modes, permissions) cannot be defaulted.

**Effort:** ~25 lines | **P1** | Layer 1

---

### R11. Anti-placeholder and anti-vagueness validation

Guard against false positives (template examples, quoted text).

**Layer 1 (fast-fail):** Brackets, NFR without number, Given/When/Then < 5 words, empty tables, TBD/TODO.
**Layer 2 (content):** NFR must have number, happy-path needs error sibling, permission claims need role definition.

**Effort:** ~50 lines | **P0** | Layer 4

---

### R12. `/elicit` — Semantic stress-test

8 techniques: developer simulation, cross-doc consistency, vague scan, NG-# violation, EDGE-# resolution audit, missing error siblings, permission gap, state machine completeness.

Output: EL-A-# (ambiguities), EL-C-# (contradictions), EL-B-# (missing boundaries), EL-H-# (hidden assumptions), EL-E-# (unresolved edges), EL-D-# (dev questions).

**Effort:** ~200 lines | **P0** | Layer 4

---

### R13. Upstream template expansion for structured developer content

| Upstream | New mandatory section |
|---|---|
| **feature-spec** | Error Handling Matrix (ES-#): Scenario, Trigger, System Response, User Message, Retry, Rollback |
| **feature-spec** | State Machine (if >2 states): Mermaid + valid/forbidden transitions + side effects |
| **feature-spec** | Permission Matrix: Action × Role grid |
| **data-dictionary** | Validation Rules per field: Required, Format, Min/Max, Default, Valid/Invalid examples |
| **quality-checklist** | Observability: Logs, Metrics, Alerts with thresholds |
| **api-spec** | Idempotency/Retry/Concurrency per endpoint |

New ID prefix: `ES-#`. Without this, the handoff packet (R14) has empty sections or violates SST.

**Effort:** ~160 lines | **P0** | Layer 3

---

### R14. Developer Handoff Packet — Generated, SST-compliant

| Section | Authority |
|---|---|
| Context & non-goals | feature-brief + NG-# |
| Actors & permissions | opportunity-pack + feature-spec permission matrix |
| Business rules | feature-brief FB-# + feature-spec |
| Acceptance criteria | user-stories (filtered) |
| Error handling ES-# | feature-spec |
| State machine | feature-spec |
| API contracts | api-spec (filtered) |
| Data mutations & validation | database-spec + data-dictionary |
| Performance NFR-# | tech-spec |
| Observability | quality-checklist |
| Tasks impl-# | implementation-plan |
| Open questions | ASM-# open |

If upstream section missing: `⚠️ MISSING — [source] does not contain this. Run /elicit.`
**Dependency:** R13 before R14. One packet per feature or sprint scope.

**Effort:** ~260 lines | **P0** | Layer 3

---

### R15. Gate decisions persistence

Status + feedback + rejected_approaches + iteration_count + unresolved_objections. Feeds workflow state, memory, next prompts.

**Effort:** ~80 lines | **P1** | Layer 5

---

### R16. Correct-course cascade

After change-proposal approval: grep affected IDs → list docs with lines → generate diffs → present before/after → apply → update state → flag external issues.

**Effort:** ~65 lines | **P1** | Layer 5

---

### R17. Post-implementation feedback loop (`/retro`)

Ask dev what they invented → classify by phase → save as learning → if pattern repeats 2+, suggest archetype probe addition.

**Effort:** ~150 lines | **P1-P2** | Layer 5

---

## Roadmap

| Phase | Scope | Lines | Days |
|---|---|---|---|
| **1. Interview** | R1, R2, R3, R8, R9, R10 | ~535 | 4-6 |
| **2. Coverage** | R5, R6, R7 | ~510 | 3-5 |
| **3. Brainstorm + Validation + Handoff** | R4, R11, R12, R13→R14 | ~830 | 5-7 |
| **4. Change + Continuity** | R15, R16, R17 | ~295 | 3-5 |
| **Total** | 17 recommendations | **~2,170** | **15-23** |

Phase 3 dependency: R13 before R14. A calibrated version = 3-4 weeks including iteration and prompt calibration.

---

## Metrics

| Metric | Target |
|---|---|
| Questions dev invented | < 3/feature |
| Semantic dimensions 1st pass | > 80% |
| Archetype probes sufficient | > 70% |
| Vague responses escalated | > 90% |
| Gate iterations | < 1.5 avg |
| SNAP-# vs abstract | > 60% story-based |
| NG-# violations | 0 |
| EDGE-# resolved | 100% |
| /retro probes added/quarter | > 3 |

**Gold:** How many decisions did the dev invent because docs didn't answer?

---

## What v5 adds over v4-AA

| Gap in v4-AA | v5 fix |
|---|---|
| EDGE-# identified but never resolved | R5 `edge_resolution` + R12 EDGE audit |
| Correct-course doesn't cascade | R16 grep→diffs→approve→apply |
| Upstream templates empty → packet empty | R13 expansion (ES-#, permissions, validation, observability, idempotency) |
| Packet can't flag missing upstream | R14 `⚠️ MISSING` flag |
| D7/D8 not diagnosed | D7 + D8 added |

Everything else from v4-AA preserved: 5 layers, SNAP-#, story-based extraction, HMW bridge, 6-phase brainstorm, separated state, "extract first verify second", SST derivation rule, 3 initial archetypes, "I don't know" classifier, fatigue management, decentralized elicitation.

---

## Definition of Done

1. Problem clear independently from solution
2. Stories captured as SNAP-# snapshots
3. Archetype probes exhausted for applicable archetypes
4. All mandatory semantic dimensions covered or justified
5. Every EDGE-# resolved (US-#, FS-#, ADR, ES-#) or deferred as NG-#
6. Actors explicit with permission matrix
7. NG-# traceable and enforced
8. Assumptions classified with owners and deadlines
9. Stress-tested via `/elicit` with zero unresolved blockers
10. ES-#, state machines, validation rules, observability documented upstream
11. Implementation packet generated (derived, not authoritative)
12. Unknowns explicit enough for engineering
13. Gate decisions persisted for downstream

---

## Principle

> **Extract first, verify second.** Stories produce 80% of coverage naturally. Archetypes, dimensions, and `/elicit` capture the 20% that stories didn't reveal.
