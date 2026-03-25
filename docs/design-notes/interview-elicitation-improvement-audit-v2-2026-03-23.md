# Interview Elicitation Improvement Audit v2

**Date:** 2026-03-23  
**Scope:** ETUS PMDocs v5.3 interview quality, semantic coverage, developer handoff completeness, executable validation, continuity, and change management  
**Goal:** Evolve ETUS from a strong document-generation framework into a system that reliably extracts product intent, surfaces hidden constraints, preserves rejected options, and hands engineering an implementation-ready packet with minimal guesswork.

---

## What Changed From v1

This version sharpens the diagnosis in five important ways:

1. It reframes the main weakness from "missing interview best practices" to **prompt-rich, enforcement-poor**.
2. It distinguishes between **signals already present in templates** and **requirements that are actually guaranteed**.
3. It treats **semantic completeness** as the primary gap, not raw document count or item count.
4. It upgrades the target from "good docs" to **developer-safe handoff**.
5. It prioritizes **shared workflow primitives** over copying more instructions into every agent.

---

## Executive Summary

ETUS PMDocs already has strong bones:

- ideation before specification
- actors, JTBDs, journeys, use cases, edge cases, assumptions
- feature and product workflows
- SST and traceability rules
- quality gates
- explicit state files
- feature lifecycle automation

The problem is not that the framework lacks categories.

The problem is that ETUS still relies too much on:

- prompt wording
- human discipline
- count-based coverage
- late validation
- distributed downstream documents

Instead of reliably enforcing:

- interview progression
- semantic completeness for the specific problem archetype
- contradiction detection
- rejection memory
- implementation-ready packaging

In short:

**ETUS currently knows how to structure product thinking, but it does not yet guarantee that it interrogated the right gaps before handing work to engineering.**

---

## Current Assessment

| Dimension | Current | Target | Main Reason For Gap |
|---|---:|---:|---|
| Interview quality | 7.8/10 | 9.5/10 | Good prompts, weak enforcement and weak probe specialization |
| Semantic completeness | 5.2/10 | 9.2/10 | Coverage measured by counts, not by critical dimensions |
| Developer handoff completeness | 4.8/10 | 9.0/10 | No single implementation packet; error/permission/ops concerns are fragmented |
| Validation effectiveness | 5.8/10 | 9.0/10 | Validation policy exists, but too little is executable |
| Phase continuity | 7.2/10 | 9.0/10 | Handoffs compress context; rejections and rationale are not fully persisted |
| Change management | 3.5/10 | 8.5/10 | Correct-course exists conceptually, but propagation is weak |

---

## What ETUS Already Has, But Does Not Yet Fully Operationalize

This distinction matters. Several concerns are **not absent** from the framework; they are **present but not mandatory, not propagated, or not validated**.

### Anti-requirements and "what not to build"

Signals already exist:

- Out-of-scope questioning in `feature-brief`
- Guardrails in ideation
- In/Out-of-scope sections in PRD templates

But the framework does not yet treat these as a first-class traceable object that downstream docs must respect.

### Error handling and state machines

Signals already exist:

- `feature-spec` template already includes Error Handling & Recovery
- `feature-spec` template already includes State Machine
- adversarial validation mentions fallbacks, migration strategy, edge cases

But these are not consistently triggered, not systematically required, and not strongly validated.

### Observability

Signals already exist:

- PRD includes observability considerations
- tech-spec includes observability stack and NFRs
- quality-checklist mentions monitoring and runbooks

But per-feature operational requirements are not consolidated into a developer-safe handoff.

### Content validation

Signals already exist:

- `validate-gate` defines Structure, Content, and Dependency layers
- adversarial review is described in detail

But the current system still lacks enough executable checks to enforce quality consistently.

---

## Core Diagnosis

## D1 — The real root cause is not missing prompts; it is missing enforcement

The framework contains many strong interview instructions:

- one question per message
- section-by-section approval
- track unknowns
- show progress
- pressure-test assumptions

But these are still mostly **behavioral guidelines**, not a workflow engine.

Consequences:

- the agent can still skip probes
- a vague answer can still pass without escalation
- a step can still be marked "covered" because an item exists
- the user can approve a section that remains semantically incomplete

**Reframe:** ETUS is currently **instruction-rich but state-light**.

That is the main architectural reason interview quality is not yet reliable enough.

---

## D2 — Count-based coverage is too weak for real completeness

Current ideation coverage is primarily count-based:

- number of actors
- number of journeys
- number of use cases
- number of edge cases
- number of assumptions

This is useful as a minimum floor, but it does not answer the developer's question:

> "Did we cover the critical dimensions of this problem?"

Examples of dimensions that can still be completely missing even when thresholds pass:

- permissions and role boundaries
- user-visible degraded behavior
- side effects and downstream systems
- data mutation rules
- observability/debug requirements
- notifications and timing
- explicit non-goals
- operational/manual fallback
- concurrency and retry rules

**Reframe:** the next version of ETUS should validate **semantic coverage dimensions**, not just item counts.

---

## D3 — Generic interviews are not enough; ETUS needs archetype-aware interrogation

The framework currently interviews in a mostly generic way.

That is insufficient for extracting implementation-critical details from real product ideas.

Different problem types need very different probes:

- upload/import
- workflow/approval
- API/webhook/integration
- billing/subscription
- AI assistant/copilot
- SDK/instrumentation
- admin/backoffice
- onboarding/funnel/conversion

Without archetype-aware questioning, ETUS can produce documentation that looks thorough while still missing the details senior engineers would immediately ask for.

**Reframe:** ETUS should classify the work item early and activate specialized probe packs.

---

## D4 — Developer completeness is a packaging problem as much as a coverage problem

The framework produces many useful artifacts, but the implementation burden is still distributed across multiple documents.

That means ETUS may be globally complete and locally inconvenient.

Engineering still needs to reconstruct:

- what behavior is required
- what behavior is forbidden
- what happens on failure
- who can do what
- which data rules are authoritative
- where the API contract lives
- which NFRs matter for this feature
- what still remains unresolved

**Reframe:** ETUS needs a final, generated **implementation packet / developer handoff** artifact.

---

## D5 — Validation is defined more clearly than it is executed

The framework has good validation language, but too much of it still lives at the policy level.

Examples of what should become executable:

- reject placeholder Gherkin
- reject NFRs without number + unit
- reject feature docs without explicit out-of-scope
- reject missing error-path coverage for high-risk stories
- reject contradictions across DB/API/dictionary/permission definitions

**Reframe:** ETUS needs more validators that act like schema and consistency checks, not only reviewer guidance.

---

## D6 — Change management is currently underpowered relative to the rest of the framework

This is one of the largest asymmetries in ETUS.

Upstream generation is sophisticated. Mid-stream change propagation is not.

When requirements shift, ETUS currently lacks a strong mechanism to:

- identify all impacted docs
- preserve rejected approaches
- update downstream docs consistently
- reflect feature-level priority changes back into product-level docs

This creates long-term drift between truth and documentation.

---

## Findings And Recommendations

## P0 — Highest Leverage Improvements

### P0.1 Build a reusable Elicitation Engine

Do not solve this primarily by adding more lines to all 7 agents.

Instead, add one shared workflow primitive that manages:

- current module
- current question
- question intent
- answer status: confirmed / assumed / open
- escalation rule when answer is vague
- reflection checkpoints
- block/continue logic

**Why P0**

This improves every interview-driven workflow at once.

**Best implementation path**

- Add a shared skill or protocol used by `ideate`, `project-context`, `feature-brief`, `product-vision`, and `solution-discovery`
- Extend workflow state to persist interview progress explicitly

---

### P0.2 Replace coverage counts with semantic dimensions

Extend ideation coverage to track mandatory dimensions such as:

- problem clarity
- trigger/preconditions
- actor/approver/operator roles
- success signal
- explicit non-goals
- integration/dependency impact
- failure handling
- permissions/policy
- data side effects
- observability/support expectations

**Why P0**

This is the biggest shift needed to reduce "we thought it was covered, but it wasn't."

---

### P0.3 Add archetype-aware probe packs

Introduce a small library of mandatory follow-up probes by archetype:

- upload/import
- approval workflow
- API/webhook
- billing/subscription
- AI/copilot
- SDK/telemetry
- admin/backoffice

Each archetype should define:

- must-ask questions
- likely failure states
- likely forbidden states
- likely developer-critical contracts

**Why P0**

This is how ETUS starts asking the questions a senior PM or architect would remember automatically.

---

### P0.4 Make reflection checkpoints mandatory

At least every 3-4 substantive questions, ETUS should pause and summarize:

> "Here is what I believe I understood. What is wrong, missing, or overstated?"

This should happen before major state transitions.

**Why P0**

It reduces silent misunderstanding more than adding three more open-ended questions.

---

### P0.5 Promote anti-requirements to a first-class object

The framework should not treat "what must not happen" as side commentary.

Introduce a traceable construct such as:

- `NG-#`
- or `WONT-#`

Capture:

- the forbidden behavior
- why it is forbidden
- what adjacent idea it rejects
- whether it is permanently rejected or just deferred

**Why P0**

Many implementation mistakes happen because the "no" was never formalized.

---

### P0.6 Create a Developer Handoff / Implementation Packet

Generate a consolidated artifact that engineering can use directly.

It should include:

- problem and non-goals
- business rules
- acceptance criteria
- error handling matrix
- permission matrix
- state transitions
- validation rules
- API contracts
- data and event rules
- NFRs
- observability requirements
- unresolved blockers

**Why P0**

This is the highest leverage change for improving "completude para desenvolvedor."

---

### P0.7 Upgrade validation from advisory to partially executable

Make these checks machine-enforced wherever possible:

- placeholder detection
- vague NFR detection
- missing anti-requirements
- missing error scenario coverage
- invalid or contradictory state transitions
- contradiction between DB/API/data dictionary definitions

**Why P0**

Without executable validation, strong prompt text still leaks low-quality docs.

---

## P1 — Strong Improvements With Moderate Scope

### P1.1 Formalize error handling as a required matrix

Do not leave error handling to optional narrative sections.

Require a matrix for relevant features:

- trigger
- system response
- user-facing response
- retry behavior
- escalation/fallback

### P1.2 Formalize permission and policy rules

Permissions should not live only as prose.

Require at least one explicit matrix for any feature with restricted actions or admin behavior.

### P1.3 Formalize data validation rules

For key fields and key entities, capture:

- required/optional
- format
- allowed values
- bounds
- default
- valid example
- invalid example

### P1.4 Formalize observability at feature level

For any high-priority feature, define:

- logs
- metrics
- alerts
- dashboards
- operator ownership

### P1.5 Add contradiction validation across documents

ETUS should detect contradictions like:

- DB says required, dictionary says optional
- story says editor can act, permission matrix forbids it
- API spec says sync success, feature spec says async completion

### P1.6 Preserve gate feedback and rejected approaches

Add durable state for:

- gate decision
- user rationale
- rejected approaches
- unresolved objections

### P1.7 Treat handoff JSON as index, not source of truth

Downstream agents should read:

1. handoff JSON for structure
2. authoritative docs for full context

This should become an explicit rule, not a convention.

---

## P2 — Valuable After The Core Is Hardened

### P2.1 Personalize interviews through memory

Use history to adapt:

- level of detail
- preferred tradeoff framing
- recurring blind spots
- preferred granularity of questions

### P2.2 Expose interview coverage in the console

The console should eventually show:

- active module
- semantic coverage gaps
- unresolved assumptions
- rejected approaches
- developer blockers

### P2.3 Add confidence scoring only when it changes behavior

Do not score everything.

Use confidence only where low confidence blocks progression or triggers follow-up.

---

## Recommended Target State

ETUS should consider a work item "interview-complete" only when:

- the problem is stated independently from the proposed solution
- the main actor, operator, and approver are explicit
- anti-requirements are explicit
- critical journeys and failure paths are covered
- high-risk assumptions have validation paths
- the selected direction has been stress-tested
- contradiction checks pass
- a developer handoff packet can be generated without major ambiguity

That is the right bar if the goal is:

> "A developer should be able to implement with minimal guessing."

---

## Recommended File-Level Changes

### Highest-priority existing files to evolve

- `.claude/skills/discovery/ideate/SKILL.md`
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml`
- `.claude/skills/discovery/project-context/SKILL.md`
- `.claude/skills/planning/feature-brief/SKILL.md`
- `.claude/skills/planning/user-stories/SKILL.md`
- `.claude/skills/planning/feature-spec/SKILL.md`
- `.claude/skills/validation/validate-gate/SKILL.md`
- `.claude/hooks/state_defaults.py`
- `.claude/hooks/feature_lifecycle.py`
- `.claude/hooks/memory-sync.py`

### New files worth adding

- `.claude/commands/elicit.md`
- `.claude/skills/discovery/elicit/SKILL.md`
- `.claude/skills/discovery/elicitation-archetypes/*.md`
- `.claude/skills/validation/check-contradictions/SKILL.md`
- `.claude/skills/implementation/developer-handoff/SKILL.md`

---

## Reprioritized Roadmap

### Sprint 1 — Interview Engine And Coverage

1. Add shared elicitation engine
2. Add reflection checkpoints
3. Add vague-answer escalation rules
4. Upgrade coverage matrix to semantic dimensions
5. Add archetype-aware probe packs

**Expected effect:** biggest improvement in interview quality with the least duplication.

### Sprint 2 — Developer-Safe Handoff

1. Introduce anti-requirements as first-class objects
2. Require error handling matrix where applicable
3. Require permission matrix where applicable
4. Require data validation rules where applicable
5. Add developer handoff artifact
6. Add observability minimums for priority features

**Expected effect:** biggest improvement in developer completeness.

### Sprint 3 — Executable Validation

1. Placeholder/schema validation
2. Contradiction validation across docs
3. Missing error-path detection
4. Measurable NFR enforcement
5. Traceability checks that include anti-requirements and gate outcomes

**Expected effect:** biggest improvement in gap detection quality.

### Sprint 4 — Continuity And Change Management

1. Persist gate decisions and rejected approaches
2. Enrich handoff reports with rationale and objections
3. Implement true correct-course propagation
4. Back-propagate feature changes into product-level docs
5. Expand workflow state with rationale fields

**Expected effect:** biggest improvement in continuity and mid-project correctness.

---

## Final Conclusion

The next leap for ETUS is not "more documentation."

It is:

- better interview mechanics
- better semantic completeness tracking
- better packaging for engineering
- better executable validation
- better change propagation

If ETUS does those five things well, it stops being merely a strong product-doc framework and becomes a true **idea extraction and implementation-readiness system**.
