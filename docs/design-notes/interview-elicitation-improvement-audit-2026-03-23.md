# Interview Elicitation Improvement Audit

**Date:** 2026-03-23  
**Scope:** ETUS PMDocs v5.3 interview effectiveness, coverage enforcement, gap prevention, and developer handoff completeness  
**Goal:** Make the framework exceptionally good at extracting product and feature intent from a founder/PM's head without leaving hidden gaps for implementation.

---

## Executive Summary

ETUS PMDocs already has a strong **coverage model** on paper:

- ideation before specification
- actors, JTBDs, journeys, use cases, edge cases, assumptions
- scope boundaries and out-of-scope sections
- SST and traceability validation
- feature and product modes
- adversarial review ideas in validation

That is a strong foundation.

The main weakness is not lack of methodology. The main weakness is that the framework still relies too much on **prompt discipline** and **count-based completeness**.

In practice, this means:

1. the agent can still ask the wrong question at the wrong time
2. the interview can feel complete while critical dimensions remain uncovered
3. gaps are detected late, after documents already exist
4. the final documentation is distributed across many artifacts, but not always consolidated into a developer-ready implementation packet

If the target is: "a developer can implement without guessing", then ETUS needs to move from:

- **coverage suggested by prompts**

to:

- **coverage enforced by state, archetype-aware probes, contradiction checks, and implementation-readiness packaging**

---

## What Is Already Strong

These are real strengths and should be preserved:

### 1. Coverage-first ideation exists

The ideation layer already tries to force:

- problem framing before solutioning
- actors before specs
- journeys and use cases before architecture
- assumptions and edge cases before planning

This is directionally correct and better than most spec workflows.

### 2. The framework already recognizes "what not to build"

This appears in:

- `feature-brief`
- `prd`
- guardrails and assumptions in the Opportunity Pack

That is essential for avoiding scope creep and ambiguity.

### 3. Traceability and SST are a real competitive advantage

The chain from ideation artifacts into downstream docs is one of the strongest parts of the framework. This is the right backbone for completeness enforcement.

### 4. Validation is more mature than in many frameworks

The existence of:

- `check-sst`
- `check-traceability`
- `validate-gate`
- adversarial review language

means the project already has a place where stronger enforcement can be added without redesigning everything.

---

## Core Diagnosis

### The biggest systemic gap

The framework captures many categories of information, but it does **not yet guarantee semantic completeness** for the specific type of product or feature being discussed.

Today the system mostly answers:

- "Did we cover some actors?"
- "Did we cover some journeys?"
- "Did we write some edge cases?"

But the real implementation question is:

- "Did we cover the right questions for this kind of problem?"

Examples:

- If the feature is upload-related, did we ask about file size, formats, retries, antivirus, progress, replacement rules, and partial failure?
- If the feature is approval workflow-related, did we ask about states, rejections, timeouts, delegation, audit trail, notifications, and re-open rules?
- If the feature is API/integration-related, did we ask about idempotency, retries, versioning, rate limits, auth scopes, failure contracts, and webhook replay?
- If the product is SaaS/admin-heavy, did we ask about roles, permissions, tenancy, support tooling, audit logs, and impersonation?

Without **archetype-aware interrogation**, a strong generic interview still leaves dangerous blind spots.

---

## Findings And Recommendations

## P0 — Highest Leverage Improvements

### P0.1 Add a dedicated Elicitation Engine, not just elicitation instructions

**Problem**

The framework repeatedly says:

- one question per message
- section-by-section approval
- track open questions
- show progress

But this is mostly a prompt convention, not a hard workflow engine.

**Why it matters**

When interview quality depends on prompt obedience alone, the system will eventually:

- batch questions
- skip probes
- advance too early
- overfit to the user's first phrasing

**Recommendation**

Create a first-class elicitation layer with explicit state and transition rules:

- current module
- active question
- why this question is being asked
- what counts as sufficient answer
- whether the answer is confirmed, assumed, or open
- what follow-up question is unlocked next

**Implementation direction**

- Extend `.claude/skills/discovery/ideate/SKILL.md`
- Extend `.claude/skills/planning/feature-brief/SKILL.md`
- Add a new reusable skill such as `.claude/skills/discovery/elicitation-engine/SKILL.md`
- Extend `.claude/hooks/state_defaults.py` and `.claude/hooks/feature_lifecycle.py` with interview-state fields
- Persist interview progress inside `coverage-matrix.yaml` or a new `elicitation-state.yaml`

**Expected outcome**

The interview becomes a guided decision tree instead of a best-effort conversation.

---

### P0.2 Replace count-based coverage with semantic coverage dimensions

**Problem**

Current thresholds like:

- actors >= 1
- use cases >= 2
- edge cases >= 2

are useful as a floor, but they are easy to satisfy without achieving real completeness.

**Why it matters**

A feature can have:

- 2 use cases
- 2 edge cases
- 1 assumption

and still be missing:

- role/permission rules
- explicit non-goals
- success/failure visibility
- integration boundaries
- operational fallback
- data and event impacts

**Recommendation**

Change coverage from raw counts to **dimension coverage**. For each work item, track whether the following dimensions are covered:

- problem clarity
- user and operator roles
- trigger and preconditions
- core behavior
- expected success signal
- explicit non-goals
- dependencies and integrations
- failure modes and degraded behavior
- permissions and policy constraints
- data mutations and side effects
- notifications and downstream consequences
- observability and support/debug needs

**Implementation direction**

- Redesign `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml`
- Add fields like `dimensions`, `mandatory_dimensions`, `coverage_score`, `critical_gaps`
- Update `validate-gate` to fail on missing mandatory dimensions, not just low counts

**Expected outcome**

The framework stops equating "some artifacts exist" with "the problem space is adequately specified."

---

### P0.3 Add archetype-aware probe packs

**Problem**

The current interview is strong but mostly generic.

**Why it matters**

Generic questions are not enough for complete handoff. Different problem types need different gap-checks.

**Recommendation**

At the start of ideation, classify the work item into one or more archetypes, then activate specialized probe packs.

Suggested archetypes:

- CRUD/backoffice
- workflow/approval
- analytics/reporting
- data import/export
- API/integration/webhooks
- marketplace/two-sided platform
- subscriptions/billing
- AI/copilot/agent feature
- SDK/instrumentation
- onboarding/funnel/conversion
- notifications/messaging
- search/filter/discovery

Each archetype should have mandatory probes.

Examples:

- **Import/export:** formats, size limits, malformed rows, preview, validation, rollback, resumability
- **Workflow:** states, transitions, invalid transitions, SLA, escalation, auditability
- **API/integration:** auth, retries, rate limits, idempotency, partial failure, replay, backward compatibility
- **AI feature:** input boundaries, hallucination risk, human override, refusal rules, evaluation criteria

**Implementation direction**

- New folder such as `.claude/skills/discovery/elicitation-archetypes/`
- Add archetype selection to `ideate` and `feature-brief`
- Extend `coverage-matrix.yaml` to record active archetypes and unresolved archetype probes

**Expected outcome**

The framework asks the questions a senior PM or architect would remember, not just generic product-discovery questions.

---

### P0.4 Introduce a dedicated `/elicit` or `/stress-test` command between ideation and final spec lock

**Problem**

There is no dedicated, explicit "interrogate the spec until ambiguity is gone" phase.

The closest pieces are spread across:

- ideation
- feature brief pressure test
- validate gate
- adversarial review language

**Why it matters**

Great implementation docs require a final pass focused on:

- ambiguity
- contradiction
- missing boundaries
- hidden assumptions
- "what happens when this goes wrong?"
- "what should never happen?"

**Recommendation**

Create a separate command:

- `/elicit`
- or `/stress-test`

This command should not create new solution ideas. It should challenge the current understanding.

It should run focused interrogations such as:

- goal vs non-goal clash
- actor/permission mismatch
- missing lifecycle states
- missing failure handling
- hidden operational dependencies
- missing developer-facing contract details

**Implementation direction**

- Add `.claude/commands/elicit.md`
- Add `.claude/skills/discovery/elicit/SKILL.md`
- Make it callable after `/ideate`, before `/feature brief`, and before Planning Gate

**Expected outcome**

The framework gains a formal anti-gap phase instead of relying on late validation alone.

---

### P0.5 Create a final Implementation Packet artifact

**Problem**

The framework produces many useful documents, but the developer still needs to synthesize across them.

That means the documentation may be complete globally while still being inconvenient locally.

**Why it matters**

"Everything needed to implement" is not only about coverage. It is also about **packaging**.

**Recommendation**

Add a generated artifact such as:

- `implementation-packet.md`
- or `dev-handoff.md`

This should consolidate only what engineering needs to build correctly:

- problem and non-goals
- target actors and roles
- scoped feature list
- business rules
- states and transitions
- API contracts
- data mutations and event contracts
- edge cases and failure handling
- permissions and policy constraints
- NFRs
- rollout and rollback triggers
- test scenarios
- unresolved blockers

**Implementation direction**

- New skill under `.claude/skills/implementation/implementation-packet/`
- Generated after `plan requirements` in Product mode and after `feature stories` or `design-delta` in Feature mode
- Consumes PRD, feature brief, user stories, feature specs, tech spec, API spec, data dictionary

**Expected outcome**

A developer can implement from one packet without guessing which upstream doc is authoritative for a given concern.

---

### P0.6 Promote non-goals and negative requirements to first-class traceable objects

**Problem**

The framework mentions out-of-scope sections, but they are not treated as a first-class traceability object.

**Why it matters**

Many implementation bugs come from building what was never desired, not from failing to build what was desired.

**Recommendation**

Introduce explicit negative requirement IDs, for example:

- `NG-#` for non-goals
- or `WONT-#`

Each should include:

- statement
- why it is excluded
- what adjacent behavior it rejects
- until when it is out of scope
- what downstream docs must respect it

**Implementation direction**

- Add section and IDs to Opportunity Pack, Feature Brief, PRD
- Extend `check-traceability` so downstream docs cannot quietly reintroduce rejected behavior
- Extend `validate-gate` to flag design or implementation scope that conflicts with non-goals

**Expected outcome**

"What I do not want" becomes as operationally clear as "what I want."

---

## P1 — Strong Improvements With Moderate Scope

### P1.1 Add contradiction detection across artifacts

**Problem**

The ideation layer has a contradiction register, but there is no strong cross-document contradiction system.

**Recommendation**

Add a validator that looks for conflicts such as:

- PRD says admin-only, API spec exposes editor access
- feature brief says CSV only, API spec accepts XLSX
- user story says synchronous confirmation, feature spec says async eventual completion
- rollout says canary, implementation plan assumes big bang

**Implementation direction**

- New validation skill: `.claude/skills/validation/check-contradictions/SKILL.md`
- Integrate into `validate-gate`

---

### P1.2 Turn assumptions into a lifecycle, not a list

**Problem**

Assumptions are captured, but they are not yet fully operationalized.

**Recommendation**

Each `ASM-#` should include:

- risk score
- evidence strength
- owner
- deadline phase
- validation mechanism
- blocking status

And the gate should block progress if a high-risk assumption remains unresolved without an agreed validation path.

**Implementation direction**

- Extend `assumption-audit`
- Extend `coverage-matrix.yaml`
- Add assumption status checks in `validate-gate`

---

### P1.3 Add a Feature Boundary Map

**Problem**

The framework traces features, but it does not strongly visualize boundary interactions between them.

**Recommendation**

Add a compact matrix that shows:

- feature/capability
- shared entities
- upstream dependencies
- downstream dependencies
- risk of overlap
- hidden coupling

**Why it matters**

This is especially useful when users describe multiple adjacent ideas as if they were one feature.

**Implementation direction**

- Add to PRD or a new planning artifact
- Auto-generate from PRD-F, FB, UC, and SOL links

---

### P1.4 Add a Developer Ambiguity Check

**Problem**

The framework validates completeness, but does not explicitly simulate the developer's confusion.

**Recommendation**

Create a review mode that asks:

- what would a fresh developer still need to ask?
- where could two engineers implement different behaviors and both think they are correct?
- where are values or thresholds missing?
- where does the spec imply a policy without naming it?

**Implementation direction**

- Extend `spec-reviewer`
- Or create a new `developer-handoff-reviewer`

---

### P1.5 Add domain-specific "must ask" libraries

**Problem**

Even with archetypes, some domains deserve reusable must-ask prompts.

Suggested probe libraries:

- auth and permissions
- billing and subscription lifecycle
- notifications
- audit logs and support operations
- data deletion, privacy, and retention
- accessibility and responsive constraints
- migration and backward compatibility
- observability and operational ownership

**Implementation direction**

- Reusable markdown guides under `.claude/skills/discovery/`
- Loaded only when triggered by the archetype

---

### P1.6 Add example-driven elicitation

**Problem**

Many ambiguous requirements sound clear until the user is forced into concrete examples.

**Recommendation**

Systematically ask for:

- one canonical success example
- one ugly edge example
- one "this should definitely not happen" example

This should happen before a brief is approved.

**Expected outcome**

Less abstract ambiguity, more implementation-ready specificity.

---

## P2 — Important, but After The Core Workflow Is Hardened

### P2.1 Personalize interviews using memory

Use previous projects and preference memory to adapt:

- level of detail
- preferred output style
- risk tolerance
- preferred tradeoff framing
- recurring blind spots

This should personalize the interview without skipping hard questions.

---

### P2.2 Improve the console/UI around interview progress

The local console is currently read-only.

There is an opportunity to surface:

- active interview phase
- completed coverage dimensions
- unresolved blockers
- assumptions still open
- contradictions detected
- "questions you still need answered before this is implementation-safe"

This would turn the framework into a visibly guided interview system instead of an invisible prompt protocol.

---

### P2.3 Add confidence scoring only where it changes behavior

Confidence scoring is only useful if low confidence forces action.

Recommended usage:

- per problem framing
- per selected solution
- per critical business rule cluster
- per developer handoff packet

Do not score everything. Score only areas that may block implementation.

---

## Missing Coverage Areas That Deserve Explicit Ownership

These areas are partially present today, but they should become explicit "must resolve or explicitly defer" categories during elicitation:

- permissions and role boundaries
- lifecycle states and invalid transitions
- explicit non-goals
- side effects and downstream systems
- notifications and user-visible consequences
- admin and support workflows
- observability and debugging expectations
- migration/backfill/backward compatibility
- privacy, retention, and compliance triggers
- event tracking and analytics semantics
- degraded-mode behavior
- rollback and manual recovery behavior
- "what must not get worse" guardrails

The current framework touches many of these later in design and implementation, but the interview should surface them much earlier when they change scope and behavior.

---

## Proposed Roadmap

### Phase 1 — Harden interview quality

1. Add elicitation state machine
2. Upgrade coverage matrix to semantic dimensions
3. Add archetype-aware probe packs
4. Add `/elicit` stress-test command

### Phase 2 — Harden gap detection

1. Add contradiction checker
2. Promote non-goals to traceable IDs
3. Upgrade assumptions to lifecycle objects
4. Add developer ambiguity review

### Phase 3 — Harden handoff quality

1. Add implementation packet
2. Add feature boundary map
3. Expose progress and unresolved gaps in the console

---

## Recommended File-Level Changes

### Highest priority files to change first

- `.claude/commands/ideate.md`
- `.claude/skills/discovery/ideate/SKILL.md`
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml`
- `.claude/skills/planning/feature-brief/SKILL.md`
- `.claude/skills/validation/validate-gate/SKILL.md`
- `.claude/skills/validation/check-traceability/SKILL.md`
- `.claude/hooks/feature_lifecycle.py`
- `.claude/hooks/state_defaults.py`

### New files worth adding

- `.claude/commands/elicit.md`
- `.claude/skills/discovery/elicit/SKILL.md`
- `.claude/skills/validation/check-contradictions/SKILL.md`
- `.claude/skills/implementation/implementation-packet/SKILL.md`
- `.claude/skills/discovery/elicitation-archetypes/README.md`
- `.claude/skills/discovery/elicitation-archetypes/*.md`

### Optional UI follow-up

- `apps/etus-console/backend/app/etus_reader.py`
- console frontend views for unresolved gaps and coverage dimensions

---

## If The Goal Is "No Gaps For Developers", The New Definition Of Done Should Be:

A feature or product is only interview-complete when:

- the problem is clear independently from the proposed solution
- actors, operators, and approvers are explicit
- non-goals are explicit and traceable
- critical journeys, use cases, and edge cases are covered
- active assumptions have owners and validation paths
- the chosen solution has been stress-tested
- contradictions have been checked
- developer-critical details are consolidated into a single implementation packet
- the remaining unknowns are explicit enough that engineering knows what must be answered before coding

That is the shift from "good documentation framework" to "exceptionally effective elicitation system."

---

## Bottom Line

ETUS PMDocs already has the right bones.

To become truly exceptional at interviewing and extracting product intent, it does **not** primarily need more document types.

It needs:

1. stronger enforcement of interview behavior
2. smarter, archetype-aware questioning
3. semantic completeness checks instead of count thresholds
4. contradiction and ambiguity detection
5. a final developer-ready implementation packet

Those five changes would materially reduce the chance that a team says:

"The docs existed, but we still had to guess."
