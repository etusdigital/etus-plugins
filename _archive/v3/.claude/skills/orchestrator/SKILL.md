---
name: orchestrator
description: Orchestrate the complete solo developer workflow across all 6 chains (feature-development, ux, architecture, data, api-backend) with gate validation, parallel execution management, and Double Diamond phase enforcement. Use when generating complete product documentation from vision to implementation specs.
---

# Orchestrator

Coordinate the complete solo developer documentation workflow across all document generation chains with systematic gate validation and parallel workstream management.

## Purpose

This skill orchestrates the entire product development documentation workflow by:

1. **Managing Chain Execution** - Coordinate 5 specialized chain skills in proper sequence
2. **Enforcing Gates** - Validate Discovery, Planning, and Implementation Readiness gates using 5W2H
3. **Parallel Execution** - Launch Data, UX, and Backend chains in parallel during Design phase
4. **Dependency Validation** - Ensure prerequisite documents exist before dependent chains run
5. **Quality Assurance** - Verify traceability, completeness, and Single Source of Truth compliance
6. **Double Diamond Enforcement** - Ensure proper convergence/divergence at phase transitions

The orchestrator is the "conductor" that ensures all 21 core documentation files are generated in the correct order with complete traceability.

## Interactive Gate Reviews

**All gates in this orchestration workflow are COLLABORATIVE REVIEWS, not automatic checks.**

Gate validation is a conversation with the user to decide together whether to:
- **GO** - Proceed to next phase (requirements met, confidence high)
- **NO-GO** - Stop project (doesn't make business/technical sense)
- **ITERATE** - Refine current phase (gaps identified, need more work)

**Key Principle:** Gates are decision points, not checkboxes. The user must explicitly approve proceeding to each phase.

**Do NOT:**
- Automatically pass gates without user review
- Generate all documents without pausing at gates
- Skip validation conversations
- Proceed without explicit GO decision from user
- Ignore gate failures and continue anyway

**Success Criteria:** User actively participates in gate reviews and makes informed GO/NO-GO/ITERATE decisions at each phase transition.

## When to Use This Skill

Use this skill when:
- Starting a new product and need complete documentation set
- Want to generate all documents from vision through implementation specs
- Need to ensure proper workflow sequence and gate validation
- Managing complex documentation with parallel workstreams
- Validating completeness of existing documentation set

Do NOT use for:
- Generating individual documents (use specific chain skills instead)
- Updating existing documents (use chain skills directly)
- Learning about specific templates (read template files directly)

**Dependencies:** This skill invokes all 5 chain skills in orchestrated sequence.

## Methodology Integration

### Double Diamond Orchestration

The orchestrator enforces the complete Double Diamond across all chains:

```
DISCOVER          DEFINE          DEVELOP          DELIVER
(Diverge)       (Converge)      (Diverge)       (Converge)

feature-dev    → feature-dev →   architecture  →    converge
                                      ↓               at fe
                                   data ──────→
                                      ↓
                                   ux ────────→
                                      ↓
                                   api-backend →
```

**Phase Transitions Enforced:**
- Discover → Define: Problem validated, business case approved
- Define → Develop: Requirements complete, ready for technical design
- Develop → Deliver: Architecture defined, ready for parallel implementation
- Deliver → Release: Frontend convergence point reached, implementation ready

### 5W2H Gate Validation

Apply systematic questioning at each gate to ensure completeness:

**Gate Validation Questions:**

**WHAT:**
- What artifacts are required for this gate?
- What quality criteria must be met?
- What dependencies must be satisfied?

**WHO:**
- Who owns each deliverable?
- Who validates gate passage?
- Who is blocked if gate fails?

**WHERE:**
- Where are the required documents?
- Where are quality gaps?
- Where are dependency conflicts?

**WHEN:**
- When can we proceed to next phase?
- When must gate be passed (deadline)?
- When were artifacts last validated?

**WHY:**
- Why is this gate necessary?
- Why might we fail this gate?
- Why are specific criteria important?

**HOW:**
- How do we validate completeness?
- How do we verify quality?
- How do we resolve gate failures?

**HOW MUCH:**
- How much work remains before gate?
- How much risk in proceeding?
- How much rework if we skip validation?

### How Might We for Gate Failures

Transform gate blockers into opportunities:

**Example Transformations:**

```
Blocker: NFRs not quantified, can't pass Develop gate
↓
HMW: How might we quickly quantify NFRs using existing data?
↓
Solution: Reference industry benchmarks, competitor analysis, user research data
```

```
Blocker: Parallel workstreams have conflicting assumptions
↓
HMW: How might we align assumptions without blocking parallel work?
↓
Solution: Async architecture review, shared data dictionary as single source
```

```
Blocker: Frontend convergence missing backend API contracts
↓
HMW: How might we unblock frontend while backend APIs finalize?
↓
Solution: Generate mock API contracts from FRD, iterate on contracts separately
```

## Workflow Orchestration

### Sequential Execution (Phases 1-3)

**Phase 1: DISCOVERY (Divergent)**

```
feature-development-chain (project-context → vis → prd)
↓
DISCOVERY GATE VALIDATION
✓ Project context documented (problem, market, timeline)
✓ Vision statement clear
✓ 5W2H analysis complete
✓ North Star Metric defined
✓ Product requirements clear with PRD-F-# features
✓ Business objectives (BO-#) documented
```

**Decision:** GO (proceed to Planning) | NO-GO (kill project) | ITERATE (refine discovery)

**Phase 2: PLANNING (Convergent)**

```
feature-development-chain (user-stories → feature-specs)
↓
PLANNING GATE VALIDATION
✓ Every PRD feature (PRD-F-#) has ≥1 user story
✓ Every story has clear acceptance criteria (Given/When/Then)
✓ Feature specs created for complex features (on-demand)
✓ Complete traceability: vis → PRD-F-# → US-#
✓ 0 undefined TBD items in P0 scope
```

**Decision:** GO (proceed to Design) | DESCOPE (remove Should/Could) | ITERATE (clarify requirements)

**Phase 3: DESIGN (Divergent) - Architecture First**

```
architecture-chain (architecture-diagram → tech-spec)
↓
IMPLEMENTATION READINESS VALIDATION
✓ Architecture documented (C4 model)
✓ NFRs defined with targets and acceptance criteria
✓ Tech spec complete with implementation guidance
✓ ADRs document key decisions with alternatives
✓ Implementation plan clear
✓ No architectural debt in critical path
```

**Decision:** GO (start parallel workstreams) | REDESIGN (architecture inadequate) | ITERATE (refine design)

### Parallel Execution (Phase 4)

**Phase 4: IMPLEMENTATION (Parallel Workstreams)**

Launch THREE chains in parallel:

**Workstream A: Data Chain**
```
data-chain (data-requirements → erd → database-spec → data-dictionary → data-flow-diagram → data-catalog)

Data Track:
✓ All entities defined with relationships
✓ ERD complete and validated
✓ Database spec: schema, constraints, indexing
✓ Data dictionary: dict.* and ev.* defined
✓ Data flows mapped
✓ Data catalog for governance
```

**Workstream B: UX Chain**
```
ux-chain (user-journey → ux-sitemap → wireframes → style-guide)

UX Track:
✓ User journeys documented
✓ Sitemap complete with information architecture
✓ Wireframes for all key screens
✓ Style guide: design tokens (Single Source)
```

**Workstream C: Backend Chain**
```
api-backend (api-spec)

Backend Track:
✓ All API endpoints documented
✓ Request/response schemas defined
✓ Authentication/authorization specified
✓ Error handling and rate limiting policies
```

**Convergence Validation:**
- Data outputs link to API contracts
- UX design tokens consistent with implementation
- Backend supports all user story requirements
- No conflicting assumptions between tracks

**Decision:** GO (ready for implementation) | ITERATE (resolve conflicts) | BLOCK (one track incomplete)

## Chain Skill Invocation

### Feature Development Chain

**Invoke When:** Starting Discovery or Planning phase

**Input Required:**
- Problem statement (user input)
- Business context
- Target users

**Output Generated:**
- project-context.md (Project Context)
- product-vision.md (Product Vision)
- prd.md (Product Requirements with PRD-F-# features)
- user-stories.md (User Stories)
- feature-spec-[name].md (Feature Specs - on demand for complex features)

**Validation After Completion:**
- Discovery Gate passed (after vision + context)
- Planning Gate passed (after user stories)
- Complete traceability: vis → PRD-F-# → US-#

### Architecture Chain

**Invoke When:** Planning gate passed, entering Design phase

**Input Required:**
- user-stories.md and prd.md from feature-development-chain

**Output Generated:**
- architecture-diagram.md (C4 model)
- tech-spec.md (Technical Specification with NFRs and ADRs)

**Validation After Completion:**
- Implementation Readiness Gate passed
- Every NFR-# has: target, verification, owner, acceptance threshold
- Architecture supports all user story requirements
- ADRs document major decisions

### Data Chain

**Invoke When:** Implementation Readiness gate passed, parallel workstream A

**Input Required:**
- user-stories.md and prd.md from feature-development-chain
- tech-spec.md from architecture-chain

**Output Generated:**
- data-requirements.md (Data Requirements Document)
- erd.md (Entity Relationship Diagram)
- database-spec.md (Database Specification: schema, constraints, indexing)
- data-dictionary.md (Data Dictionary - dict.* and ev.* single source)
- data-flow-diagram.md (Data Flow Diagram)
- data-catalog.md (Data Catalog)

**Validation After Completion:**
- Data Track passed
- All dict.* fields defined (Single Source)
- All ev.* events defined (Single Source)
- Database spec complete with DDL

### UX Chain

**Invoke When:** Implementation Readiness gate passed, parallel workstream B

**Input Required:**
- user-stories.md and prd.md from feature-development-chain
- tech-spec.md from architecture-chain

**Output Generated:**
- user-journey.md (User Journey with pain points and opportunities)
- ux-sitemap.md (UX Sitemap - information architecture)
- wireframes.md (Wireframes for key screens)
- style-guide.md (Style Guide - design tokens single source)

**Validation After Completion:**
- UX Track passed
- All design tokens defined (Single Source)
- Sitemap complete with IA
- Wireframes cover key user flows
- Design tokens align with implementation

### API Backend

**Invoke When:** Implementation Readiness gate passed, parallel workstream C

**Input Required:**
- user-stories.md and prd.md from feature-development-chain
- tech-spec.md from architecture-chain

**Output Generated:**
- api-spec.md (API Specification - comprehensive API documentation)

**Validation After Completion:**
- Backend Track passed
- All API endpoints documented
- Authentication/authorization specified
- Request/response schemas defined
- Error handling defined

## Dependency Management

### Critical Dependency Rules

**Must Complete Before Starting:**

1. **feature-development-chain MUST complete before:**
   - architecture-chain (requires user-stories + prd)
   - data-chain (requires user-stories + prd)
   - ux-chain (requires prd + user-stories)
   - api-backend (requires user-stories + prd)

2. **architecture-chain MUST complete before:**
   - data-chain (requires tech-spec for NFRs)
   - api-backend (requires tech-spec for NFRs)

3. **Parallel workstreams (Data, UX, Backend) can start simultaneously IF:**
   - feature-development-chain complete
   - architecture-chain complete
   - No conflicting assumptions identified

### Dependency Validation Checks

Before launching any chain:

```
DEPENDENCY CHECK (5W2H):

WHAT dependencies required?
- List all required upstream documents
- Verify each document exists

WHO provides dependencies?
- Identify which chains produce required outputs
- Verify those chains completed successfully

WHERE are dependency gaps?
- Check for missing documents
- Identify incomplete sections

WHEN can we proceed?
- Validate all prerequisites met
- Check gate criteria passed

WHY are dependencies critical?
- Document rationale for dependencies
- Identify blocking vs nice-to-have

HOW do we resolve missing dependencies?
- Re-run upstream chains
- Generate missing documents
- Adjust scope if needed

HOW MUCH risk without dependency?
- Assess impact of proceeding
- Document assumptions if blocked
```

## Quality Assurance

### Traceability Validation

After all chains complete, validate complete traceability:

**Traceability Chains to Verify:**

1. **Problem → Solution:**
   - vis (vision) → PRD-F-# (product features)

2. **Requirements → Implementation:**
   - PRD-F-# → US-# (user stories)
   - US-# → FS-[name]-# (feature specs, if created)
   - US-# → NFR-# (non-functional requirements)

3. **Architecture → Components:**
   - NFR-# → architecture patterns (architecture-diagram.md)
   - NFR-# → implementation tactics (tech-spec.md)
   - ADRs document architecture decisions

4. **Data Traceability:**
   - US-# → entities (erd.md)
   - entities → database-spec.md
   - database-spec.md → dict.* (data-dictionary.md)
   - US-# → ev.* (events in data-dictionary.md)

5. **UX Traceability:**
   - US-# → wireframes.md
   - wireframes → style-guide.md tokens
   - style-guide.md: tok.* tokens (Single Source)
   - US-# user journeys

6. **API Traceability:**
   - FR-# → API endpoints (be)
   - API endpoints → request/response schemas (be)
   - be → fe (frontend references backend APIs)

**Validation Method:**
- Generate traceability matrix
- Check for orphaned IDs (not linked upstream)
- Verify bidirectional references
- Validate no broken links

### Single Source of Truth Validation

Ensure no duplicate definitions across documents:

**Single Sources to Enforce:**

1. **Given/When/Then** → ONLY in User Stories (user-stories.md)
   - Other docs reference US-# IDs
   - No acceptance criteria restated elsewhere

2. **NFR Targets** → ONLY in Tech Spec (tech-spec.md)
   - Other docs reference NFR-# IDs
   - No numeric targets restated

3. **API Schemas** → ONLY in API Spec (api-spec.md)
   - Other docs reference API endpoints
   - No request/response duplicated

4. **Design Tokens** → ONLY in Style Guide (style-guide.md)
   - Other docs reference design token IDs
   - No color/spacing/typography redefined

5. **Field Definitions** → ONLY in Data Dictionary (data-dictionary.md)
   - Other docs reference dict.* fields
   - No field semantics duplicated

6. **Event Definitions** → ONLY in Data Dictionary (data-dictionary.md)
   - Other docs reference ev.* events
   - No event schemas duplicated

7. **DDL Statements** → ONLY in Database Spec (database-spec.md)
   - Other docs reference table structures
   - No CREATE TABLE duplicated

**Validation Method:**
- Search for duplicate definitions
- Check for restated content
- Verify references instead of copying
- Flag any violations for correction

### Completeness Checks

Validate all required documents generated:

**Core Templates (21):**
- [ ] project-context.md
- [ ] product-vision.md
- [ ] prd.md
- [ ] user-stories.md
- [ ] feature-spec-[name].md (on demand for complex features)
- [ ] architecture-diagram.md
- [ ] tech-spec.md
- [ ] data-requirements.md
- [ ] erd.md
- [ ] database-spec.md
- [ ] data-dictionary.md
- [ ] data-flow-diagram.md
- [ ] data-catalog.md
- [ ] user-journey.md
- [ ] ux-sitemap.md
- [ ] wireframes.md
- [ ] style-guide.md
- [ ] api-spec.md
- [ ] implementation-plan.md (post-documentation)
- [ ] sprint-status.yaml (ongoing)
- [ ] quality-checklist.md (post-documentation)

**Supporting Files (as needed):**
- [ ] feature-spec-[name]-details.md - Extended specs for complex features
- [ ] workflow.md - Process documentation

## Error Handling

### Common Orchestration Failures

**Gate Failure:**
```
Symptom: Define gate validation fails, missing DoD in P0 stories
↓
HMW: How might we quickly add DoD without blocking progress?
↓
Solution:
1. Identify which P0 stories missing DoD
2. Generate DoD from acceptance criteria (us-#)
3. Validate DoD completeness with 5W2H
4. Re-run Define gate validation
```

**Dependency Conflict:**
```
Symptom: Frontend needs API contracts but backend incomplete
↓
HMW: How might we unblock frontend while backend finalizes?
↓
Solution:
1. Generate mock API contracts from FR-# requirements
2. Document assumptions in frontend specs
3. Add dependency note: "Validate against be when complete"
4. Proceed with frontend, flag for sync later
```

**Parallel Workstream Conflict:**
```
Symptom: Data chain defines field "user_status", UX chain also defines same field
↓
HMW: How might we resolve naming conflicts without blocking parallel work?
↓
Solution:
1. Identify conflict source (both defining dict.* field)
2. Determine authoritative source (Data Dictionary)
3. Update conflicting document to reference dict.user_status
4. Validate Single Source of Truth compliance
```

**Missing Traceability:**
```
Symptom: NFR-# doesn't trace back to any US-# or FR-#
↓
HMW: How might we establish traceability for orphaned NFR?
↓
Solution:
1. Review NFR context (why does it exist?)
2. Identify which FR-# or US-# it supports
3. Add explicit reference in NFR definition
4. Update traceability matrix
```

## Workflow Execution

### Standard Orchestration Flow

```
1. DISCOVERY PHASE (Sequential)
   └─ invoke: feature-development-chain (project-context → vis → prd)
   └─ validate: Discovery Gate
   └─ decision: GO | NO-GO | ITERATE

2. PLANNING PHASE (Sequential)
   └─ invoke: feature-development-chain (user-stories → feature-specs)
   └─ validate: Planning Gate
   └─ decision: GO | DESCOPE | ITERATE

3. DESIGN PHASE - Architecture (Sequential)
   └─ invoke: architecture-chain (architecture-diagram → tech-spec)
   └─ validate: Implementation Readiness Gate
   └─ decision: GO | REDESIGN | ITERATE

4. IMPLEMENTATION PHASE - Parallel Workstreams (Parallel)
   ├─ invoke: data-chain (data-requirements → erd → database-spec → data-dictionary → data-flow-diagram → data-catalog)
   │  └─ validate: Data Track
   ├─ invoke: ux-chain (user-journey → ux-sitemap → wireframes → style-guide)
   │  └─ validate: UX Track
   └─ invoke: api-backend (api-spec)
      └─ validate: Backend Track

   └─ CONVERGENCE VALIDATION
      └─ decision: GO | ITERATE | BLOCK
```

### Abbreviated Flows

**Fast Path (Core Templates Only):**
```
Generate 21 core templates without extended specs:
- project-context.md
- product-vision.md
- prd.md
- user-stories.md
- architecture-diagram.md
- tech-spec.md
- data-requirements.md → data-catalog.md (6 data docs)
- user-journey.md → style-guide.md (4 UX docs)
- api-spec.md
```

**Iterative Refinement:**
```
Allow iteration loops at any phase:
- vis ↔ project-context (align context and vision)
- prd ↔ user-stories (refine scope)
- user-stories ↔ feature-specs (clarify complex requirements)
- architecture ↔ tech-spec (optimize architecture)
```

## Gate Criteria Reference

### Discovery Gate - **INTERACTIVE REVIEW**

**After generating project-context, vis, and prd, conduct collaborative gate review:**

```
"Let's review the Discover Gate together to decide if we should proceed to Define phase:

**Vision Completeness:**
✓ Vision: '[One-line vision]' - Does this pass the 't-shirt test'? Is it clear and memorable?
✓ 5W2H: I've gathered [list what was covered] - What am I missing?
✓ North Star Metric: [Metric] from [baseline] to [target] in [window] - Is this the right metric to track?
✓ Critical Success Drivers: [List 3-5 drivers] - Are these the right priorities?
✓ Kill Criteria: [Criteria] - Under what conditions should we stop this project?

**Business Case:**
✓ Business Objectives: [N] BO-# objectives defined - Are these the right objectives?
✓ ROI: [X]% with [Y] month payback - Is this compelling enough to proceed?
✓ Stakeholders: [Key stakeholders] - Who else should be involved?
✓ Success Metrics: [Metrics] - How will we measure success?
✓ Risks: [Top 3 risks] - What are our mitigation plans?

**5W2H Coverage Check:**
- WHAT: [Problem statement] - Clear and specific?
- WHO: [Target users] - Do we understand them?
- WHERE: [Market context] - Competitive landscape clear?
- WHEN: [Timeline] - Realistic deadlines?
- WHY: [Business value] - Quantified?
- HOW: [Approach] - Measurement strategy defined?
- HOW MUCH: [Market size] - Revenue potential estimated?

**Gate Decision - What should we do?**

A) **GO** - Proceed to Planning phase
   - Problem validated
   - Business case approved
   - Confidence level high

B) **NO-GO** - Stop project
   - Doesn't make business sense
   - Market too small / too competitive
   - ROI insufficient

C) **ITERATE** - Refine vision or business case
   - Gaps in 5W2H analysis
   - Need more user research
   - Business case needs strengthening

What's your decision? Why?"
```

[**CRITICAL: Wait for user's explicit decision. Do NOT proceed to Define phase without GO approval.**]

If ITERATE, ask:
```
"What specific areas need refinement?
- Vision clarity?
- NSM definition?
- Business case numbers?
- Risk analysis?
- Other?"
```

[Return to feature-development-chain to refine identified areas, then re-review gate.]

### Planning Gate - **INTERACTIVE REVIEW**

**After generating prd, user-stories, and feature-specs, conduct collaborative gate review:**

```
"Let's review the Define Gate together to decide if we're ready for Develop phase:

**Requirements Completeness:**
✓ PRD Must Features: [N] features defined - Each PRD-F-# linked to user stories?
✓ User Stories: [N] stories created - Each has ≥3 acceptance criteria scenarios?
✓ User Stories: [N] P0 stories - Each has ≥3 scenarios (Happy/Alt/Error)?
✓ Story Quality: All stories have DoR met and DoD defined?
✓ FRD Coverage: Flows, business rules, states, error handling all documented?
✓ TBD Items: [N] TBD items remaining in P0 scope - Acceptable?
✓ FR Traceability: All FR-# IDs trace to US-# IDs?

**Traceability Chain Validation:**
I've validated the complete traceability chain:
- vis (vision) → BO-# (business objectives) ✓
- BO-# → PRD-F-# (product features) ✓
- PRD-F-# → FR-# (feature requirements - decomposition) ✓
- FR-# → US-# (user stories - implementation) ✓

Any orphaned IDs? [List any broken references]
Any missing links? [List any gaps]

**5W2H Coverage Check:**
- WHAT: All Must features detailed? Acceptance criteria clear?
- WHO: Owners assigned for each user story?
- WHERE: Feature boundaries and integration points clear?
- WHEN: Story priorities defined? Sprint planning ready?
- WHY: Rationale for each Must feature documented?
- HOW: Implementation approach outlined in FR-#?
- HOW MUCH: Effort estimates done? Scope validated?

**Scope Assessment:**
- Must Features: [N] features (Recommended: 3-5 for focused MVP)
- P0 User Stories: [N] stories
- Estimated Effort: [rough estimate if available]

Does this scope feel achievable? Too ambitious? Too conservative?

**Gate Decision - What should we do?**

A) **GO** - Proceed to Develop phase
   - Requirements complete and clear
   - Traceability validated
   - Confidence in scope

B) **DESCOPE** - Remove Should/Could features
   - Scope too large
   - Timeline too tight
   - Focus on smaller MVP

C) **ITERATE** - Clarify requirements
   - Gaps in requirements
   - Missing acceptance criteria
   - Broken traceability
   - Too many TBD items

What's your decision? Why?"
```

[**CRITICAL: Wait for user's explicit decision. Do NOT proceed to Develop phase without GO approval.**]

If DESCOPE, ask:
```
"Which features should we move from Must to Should/Could?
- Feature: [PRD-F-#] - Keep Must or descope?
- [Repeat for all Must features]

What's your new target scope?"
```

If ITERATE, ask:
```
"What needs clarification?
- Specific user stories missing acceptance criteria?
- FRD gaps in flows/rules/states?
- Traceability broken somewhere?
- Too many TBD items to address?
- Other?"
```

[Return to feature-development-chain to address identified issues, then re-review gate.]

### Implementation Readiness Gate - **INTERACTIVE REVIEW**

**After generating architecture-diagram and tech-spec, conduct collaborative gate review:**

```
"Let's review the Develop Gate together to decide if we're ready for parallel Deliver workstreams:

**Architecture Completeness:**
✓ NFR Coverage: [N] NFRs defined - Each has target, verification method, owner, acceptance threshold?
✓ NFR Categories: Covered performance, scalability, security, reliability, maintainability, usability?
✓ 5W2H Analysis: Key NFRs justified with 5W2H analysis?
✓ C4 Architecture: Context, Container, Component diagrams complete?
✓ NFR Support: Architecture supports all NFR-# requirements? Any conflicts?
✓ ADRs: [N] ADRs documented - Alternatives considered for major decisions?
✓ Implementation Tactics: Each P0 NFR has tactics defined?
✓ Validation Plan: Testing approach defined for NFRs?
✓ Architectural Debt: Any tech debt in critical path? [List if any]
✓ HMW Statements: Constraints transformed into opportunities?

**Architecture Decisions Review:**
Key decisions made:
- Architecture Style: [Monolith/Modular/Microservices] - Rationale: [why]
- Database Strategy: [Single/Per-Service/CQRS] - Rationale: [why]
- Integration Pattern: [Sync/Async/Hybrid] - Rationale: [why]

Do these decisions align with your NFRs and team capabilities?

**NFR Feasibility Check:**
Let me highlight critical NFRs and their tactics:
- NFR-1 ([category]): [target] - Tactic: [approach] - Feasible?
- NFR-2 ([category]): [target] - Tactic: [approach] - Feasible?
- [List all P0 NFRs]

Are these targets realistic? Do tactics achieve them?

**5W2H Coverage Check:**
- WHAT: All quality attributes quantified?
- WHO: NFR ownership assigned?
- WHERE: System boundaries clear?
- WHEN: Verification timing defined (CI/CD stage)?
- WHY: NFR targets justified with rationale?
- HOW: Implementation tactics documented?
- HOW MUCH: Infrastructure budget estimated?

**Gate Decision - What should we do?**

A) **GO** - Start parallel workstreams (Data, UX, Backend)
   - Architecture sound and supports NFRs
   - ADRs document decisions clearly
   - Validation plan in place
   - Confidence in technical approach

B) **REDESIGN** - Architecture inadequate
   - Architecture doesn't support NFRs
   - Major design flaws identified
   - Need fundamental rethinking

C) **ITERATE** - Refine NFRs or tactics
   - NFR targets unclear or unrealistic
   - Missing implementation tactics
   - ADRs need more alternatives explored
   - Validation plan incomplete

What's your decision? Why?"
```

[**CRITICAL: Wait for user's explicit decision. Do NOT proceed to Deliver phase without GO approval.**]

If REDESIGN, ask:
```
"What architectural issues need addressing?
- Architecture style wrong for requirements?
- Database strategy inadequate?
- Integration patterns won't scale?
- NFRs can't be met with this approach?
- Other fundamental concerns?"
```

If ITERATE, ask:
```
"What needs refinement?
- Specific NFRs need clearer targets?
- Missing implementation tactics for NFR-#?
- ADRs need more alternatives?
- Validation plan gaps?
- Other?"
```

[Return to architecture-chain to address identified issues, then re-review gate.]


## Best Practices

1. **Conduct Interactive Gate Reviews:** Every gate is a collaborative decision - wait for explicit GO from user
2. **Never Auto-Pass Gates:** Don't skip gate validation conversations - they prevent wasted downstream effort
3. **Present Gate Decisions Clearly:** Always offer GO/NO-GO/ITERATE options with clear rationale
4. **Respect Dependencies:** Never start dependent chains before prerequisites complete
5. **Pause at Phase Transitions:** Stop at each gate for user review before proceeding to next phase
6. **Parallel When Safe:** Launch Data/UX/Backend in parallel only after Develop gate passes
7. **Validate Traceability Early:** Check ID chains regularly, don't wait until Release gate
8. **Enforce Single Source:** Catch duplicate definitions early in each chain
9. **Use HMW for Blockers:** Transform gate failures into opportunities collaboratively
10. **Apply 5W2H Systematically:** Ensure completeness at every gate through structured questioning
11. **Document Assumptions:** When proceeding with uncertainty, document explicitly and flag at gates
12. **Iterate Freely:** Documents evolve with understanding - embrace revision cycles between gates
13. **Reference, Don't Restate:** Link to upstream IDs instead of copying content
14. **User Owns GO Decisions:** You present options and analysis; user decides to proceed or iterate

## Common Pitfalls to Avoid

- ❌ Skipping Discover gate (building wrong thing)
- ❌ Starting parallel workstreams too early (before architecture complete)
- ❌ Missing dependencies (starting chain without prerequisites)
- ❌ Ignoring gate failures (proceeding with incomplete work)
- ❌ Allowing duplicate definitions (violating Single Source of Truth)
- ❌ Breaking traceability chains (orphaned IDs)
- ❌ Skipping 5W2H validation (incomplete gate checks)
- ❌ No HMW for blockers (missing creative solutions)
- ❌ Treating documents as "done" (they evolve with product)
- ❌ Proceeding to Release with broken references

## Knowledge Base

This skill coordinates all chain skills which reference template files:

### Feature Development Chain Templates
- project-context.md, product-vision.md, prd.md (with PRD-F-# features), user-stories.md, feature-spec-[name].md (decomposes complex features)

### Architecture Chain Templates
- architecture-diagram.md, tech-spec.md (includes NFRs and ADRs)

### Data Chain Templates
- data-requirements.md, erd.md, database-spec.md (schema + constraints), data-dictionary.md, data-flow-diagram.md, data-catalog.md

### UX Chain Templates
- user-journey.md, ux-sitemap.md, wireframes.md, style-guide.md (with design tokens)

### Backend Chain Templates
- api-spec.md (includes endpoints, schemas, auth, error handling)

### Supporting Templates
- workflow.md, greenfield-fullstack.md, checklists.md, story-file-template.md, architect-checklist.md

### ID Registry
- `ids.yml` - ID management configuration for the ETUS (Event-Tracking Unified System)

**Purpose of ids.yml:**

The `ids.yml` file is a critical resource that defines:
- **ID patterns and conventions** (lowercase kebab-case, separators, invariants)
- **Document namespaces** (vis, prd, stor, arch, data, ux, be)
- **ID sequences** (BO-#, PRD-F-#, US-#, FS-[name]-#, NFR-#, ADR-#, be-ep-#)
- **Naming patterns** (routes, views, components, entities, events, tables)
- **Linting rules** (Single Source of Truth enforcement)
- **Governance policies** (change control, deprecation, versioning)

**How to Use:**

1. **For New Projects:**
   - Copy `ids.yml` from `orchestrator/knowledge/` to your project root
   - Update `registry.product`, `registry.namespace`, and `registry.owner` with your values
   - Initialize date: `registry.updated: "YYYY-MM-DD"`

2. **During Generation:**
   - Orchestrator references `ids.yml` patterns to generate compliant IDs
   - All generated IDs follow the conventions defined in `ids.yml`
   - Traceability chains respect the patterns (vis → BO-# → PRD-F-# → US-# → FS-[name]-#)

3. **Maintenance:**
   - Update `ids.yml` when adding new ID patterns
   - Increment `registry.version` when making changes
   - Use `aliases.deprecated` for ID migrations

**Key Sections:**

- `conventions`: Character set, casing rules, separators, invariants
- `namespaces.docs`: All document IDs (vis, prd, stor, arch, data, ux, be)
- `patterns`: Regex patterns for each ID type with `next` counters
- `sequences`: Current ID counters (incremented as IDs are generated)
- `documents`: Recommended file destinations and naming patterns
- `lint.rules`: Single Source of Truth enforcement rules
- `governance`: Change control and deprecation policies

**Example Usage:**

```yaml
# After generating documentation, ids.yml tracks:
sequences:
  BO: 4        # 3 business objectives defined
  PRD-F: 6     # 5 features defined in PRD
  US: 45       # 44 user stories written
  FS: 8        # Feature specs for complex features (FS-checkout-1, FS-auth-1, etc.)
  NFR: 23      # 22 non-functional requirements specified
  ADR: 7       # 6 architecture decisions recorded
  be-ep: 15    # 14 backend API endpoints specified
```

This registry ensures:
- ✅ **No ID collisions** across documents
- ✅ **Complete traceability** from vision to implementation
- ✅ **Consistent naming** across all teams
- ✅ **Single Source of Truth** enforcement
- ✅ **Governance compliance** for ID lifecycle

## Persistence Options

**After generating all documentation, offer the user these persistence options:**

### Default: Display in Conversation

By default, show generated documents in the conversation for user to review and manually save:

```
"I've generated all 21 core documentation files. Here's the complete set:

**Discovery & Planning (4 files):**
- project-context.md
- product-vision.md
- prd.md
- user-stories.md

**Architecture (2 files):**
- architecture-diagram.md
- tech-spec.md

**Data (6 files):**
- data-requirements.md
- erd.md
- database-spec.md
- data-dictionary.md
- data-flow-diagram.md
- data-catalog.md

**UX (4 files):**
- user-journey.md
- ux-sitemap.md
- wireframes.md
- style-guide.md

**Backend (1 file):**
- api-spec.md

I can show you each document here for you to copy/paste and save manually.

Alternatively, would you like me to save all files to a directory for you? Just provide the path (e.g., `/path/to/your-project/docs/`) and I'll use the Write tool to create all files automatically."
```

### Option 1: Save to Local Directory (User Requests)

If user provides a directory path, use Write tool to save all files:

```
User: "Save all documents to /Users/me/my-project/docs/"

Action:
1. Validate directory exists (or create it)
2. For each of the 25 core documents:
   - Use Write tool: file_path="/Users/me/my-project/docs/{filename}", content="{generated_content}"
3. For supporting files (if generated): Same process
4. Confirm: "✅ Saved 25 files to /Users/me/my-project/docs/"
```

### Option 2: Notion Integration (Future Enhancement)

Potential future option to persist to Notion workspace:

```
- Create Notion database with all 25 documents as pages
- Maintain cross-document links using @ mentions
- Preserve traceability chains (vis → BO-# → PRD-F-# → US-# → FS-[name]-#)
- Searchable and collaborative
```

**Implementation Note:** This requires Notion MCP tools to be available.

### Important: Templates vs Generated Content

**Templates are read-only:**
- Skills READ templates from `knowledge/` folders as reference guides
- Templates are NEVER modified or overwritten during generation
- Templates remain clean and version-controlled
- Generated content is NEVER written back to skill folders

**Generated content flow:**
1. Skill reads template from `knowledge/` folder (reference)
2. Conducts interactive interview with user
3. Generates content based on template structure + user input
4. Returns content to conversation OR saves to user's project directory
5. Skill's `knowledge/` folder remains unchanged

This clean separation ensures:
- ✅ Templates stay pristine and reusable
- ✅ Skills can be distributed without user-specific data
- ✅ Generated content goes where user wants it
- ✅ No risk of corrupting template files

## Next Steps After This Skill

After orchestration completes:

1. **Implementation Phase**: Use generated documents to build the product
2. **Validation Phase**: Test implementation against acceptance criteria (us-#) and NFRs (nfr-#)
3. **Iteration Phase**: Update documents based on implementation learnings
4. **Maintenance Phase**: Keep documents in sync with product evolution

The orchestrator ensures a complete, traceable, high-quality documentation foundation for rapid product development.
