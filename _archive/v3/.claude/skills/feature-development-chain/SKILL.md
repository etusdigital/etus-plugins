---
name: feature-development-chain
description: Generate core planning documents (product vision, requirements, user stories, and feature specifications) through interactive conversation using 5W2H systematic analysis, How Might We problem framing, and MoSCoW prioritization. Best for solo developers defining product scope and detailed requirements before architectural or technical implementation work.
---

# Feature Development Chain

Generate core planning documentation from problem discovery through feature specification using systematic methodology and interactive workflow.

## Purpose

This skill guides solo developers through the Discovery and Define phases by generating:

1. **Product Vision** (vis) - Problem statement, North Star metric, critical assumptions
2. **Product Requirements Doc** (prd) - Features (PRD-F-#) with success criteria and scope
3. **User Stories** (stor) - Acceptance criteria (Gherkin) linked to PRD features
4. **Feature Specifications** (fs) - Detailed specs for complex features (>3 business rules or state machine)

Each document maintains traceability with lowercase IDs (BO-#, PRD-F-#, US-#, FS-[name]-#), forming the foundation for all downstream technical and UX work.

## Key Changes from Previous System

**Eliminated:**
- Business Requirements Document (BRD) - Absorbed into product-vision.md
- Epics - Stories now link directly to PRD-F-# features
- Monolithic FRD - Evolved into feature-spec-[name].md (individual spec per complex feature)

**Evolved:**
- Feature Spec rule: >3 business rules OR state machine needed → feature-spec-[name].md required. CRUD-only → story suffices.
- ID patterns: BO-# (business objectives), PRD-F-# (product features), US-# (user stories), FS-[kebab-name]-# (feature spec items)

## Interactive Feature Development Workflow

**This skill is conversation-driven for collaborative problem-solving.**

Product development requires understanding customer needs, translating them into features, and validating assumptions. This skill:

1. **Discovers the problem** using 5W2H systematic questioning
2. **Frames opportunities** using How Might We (HMW) transformations
3. **Prioritizes ruthlessly** using MoSCoW framework (Must/Should/Could/Won't)
4. **Confirms understanding** at each gate through explicit review
5. **Generates clear requirements** only after user validates direction

**Key Principle:** Requirements emerge from conversation, not templates. User understanding and confidence is the success metric.

**Do NOT:**
- Generate vision without asking 5W2H questions about the problem
- Create PRD features without understanding user context and pain points
- Write user stories without confirming acceptance criteria with product owner
- Define feature specs without discussing complexity and business rules
- Proceed past gate without explicit user confirmation

**Success Criteria:** User can articulate problem, features, and acceptance criteria confidently. Requirements are measurable and testable.

## When to Use This Skill

Use this skill when:
- Starting new product or major feature initiative
- Need to define scope and success criteria
- Translating customer feedback into requirements
- Building consensus on what to build and why
- Creating specifications for implementation teams

Do NOT use for:
- Technical architecture (use architecture-chain skill instead)
- Non-functional requirements like performance (use architecture-chain skill instead)
- UX design decisions (use ux-chain skill instead)
- Data modeling (use data-chain skill instead)

**Dependencies:** Optional project-context.md for historical context. Feeds into: architecture-chain, data-chain, ux-chain, api-backend.

## Methodology Integration

### 5W2H for Problem Discovery

Apply rigorous questioning to deeply understand customer problems before proposing solutions:

**WHAT:**
- What is the core problem?
- What are customers unable to do?
- What is success?

**WHO:**
- Who experiences this problem?
- Who are primary vs secondary users?
- Who are extreme users we haven't considered?

**WHERE:**
- Where does this problem occur?
- In what contexts?
- On what platforms or devices?

**WHEN:**
- When does this problem surface?
- What triggers it?
- How frequently does it occur?

**WHY:**
- Why is this a problem now?
- Why haven't previous solutions worked?
- Why does this matter to your business?

**HOW:**
- How do customers cope today?
- How painful is the workaround?
- How would they solve it if resources were unlimited?

**HOW MUCH:**
- How much time is wasted?
- How much money is lost?
- What is the opportunity cost?

### How Might We (HMW) for Feature Ideation

Transform problem statements into opportunity framings:

**Example Transformations:**

```
Problem: Freelancers lose 5 hours/week chasing invoice payments
↓
HMW: How might we make payment collection effortless for freelancers?
↓
Opportunity: Automated reminders, payment tracking, one-click follow-up

Problem: Users don't trust sending financial data to new apps
↓
HMW: How might we build trust through transparency and security?
↓
Opportunity: Show data encryption, share security certifications, audit logs
```

### MoSCoW for Feature Prioritization

Ruthlessly scope features using Must/Should/Could/Won't framework:

**MUST Have (MVP Core):**
- Features without which product has no value
- What users will judge you on at launch
- What differentiates from competitors
- Estimate: 40-50% of brainstormed features

**SHOULD Have (V1.1):**
- Important features but not MVP-blocking
- Enhance user experience or efficiency
- Address secondary use cases
- Estimate: 30-40% of brainstormed features

**COULD Have (V2+):**
- Nice-to-have features
- Address niche use cases
- Low-effort polish items
- Estimate: 10-20% of brainstormed features

**WON'T Have (Explicitly Out of Scope):**
- Features that are out of scope for this version
- Features requiring disproportionate effort
- Features that don't align with vision
- Decision to say "no" is as important as "yes"

### Double Diamond Mapping

Feature development chain implements the DISCOVER/DEFINE phase divergence:

```
DISCOVER (Expand)    →    DEFINE (Converge)    →    DEVELOP
      ↓                        ↓                      ↓
   vis/brd              prd/stor/fs          arch/data/ux/be
```

After understanding the problem (Discovery), converge on specific features and requirements (Define) before diverging into technical work.

## How to Use This Skill

### Step 1: Product Vision (vis) — **INTERACTIVE PROBLEM DISCOVERY**

**BEFORE generating vision**, conduct problem discovery conversation:

```
"Let's deeply understand the problem before designing a solution. I'll ask systematic questions:

**Problem Understanding (5W2H):**

1. WHO is experiencing this problem?
   - Who is your primary user?
   - Are there secondary or extreme user segments?
   - How many people have this problem?

2. WHAT is the core problem?
   - What can't they do today?
   - What pain point are they experiencing?
   - What would success look like?

3. WHERE does this problem occur?
   - What contexts? (work, home, mobile, desktop)
   - What platforms or tools?
   - What environments?

4. WHEN does this problem surface?
   - What triggers it?
   - How frequently?
   - What are critical moments?

5. WHY is this a problem now?
   - Why hasn't it been solved?
   - What changed recently?
   - Why does your business care?

6. HOW do they cope today?
   - What workarounds exist?
   - How painful are they? (1-10 scale)
   - What time/money is wasted?

7. HOW MUCH is the problem costing?
   - Time lost per week/month?
   - Revenue impact?
   - Opportunity cost?
"
```

[Wait for user's answers. Probe for specificity when vague.]

**FOLLOW-UP PROBES:**

If user says "users are frustrated":
```
"What specifically frustrates them? Can you describe a recent example? How much time does this cost them per week?"
```

If user says "market demand is strong":
```
"What evidence shows strong demand? How many customers asking? What would they pay for a solution?"
```

If user says "competition is doing it wrong":
```
"What specifically are competitors missing? What would you do differently? Why haven't they fixed it?"
```

**STEP 2: Confirm Problem Framing**

After gathering 5W2H insights, confirm understanding:

```
"Let me confirm what I've understood about the problem:

**Core Problem:** [Restate concisely]
**Primary Users:** [Who/count]
**Critical Context:** [Where/when it happens]
**Current Impact:** [Time/money wasted]
**Why Now:** [Market timing]

**North Star (Success Metric):** If we fixed this, what would change?
- What would users be able to do?
- How would we measure success?
- What's the baseline vs target?

Is this an accurate picture of the problem?"
```

[Wait for confirmation. Iterate if understanding differs.]

**STEP 3: Identify Critical Assumptions**

```
"What assumptions are we making about this problem?

For each assumption, let's assess:
- How confident are we? (High/Medium/Low)
- What's the risk if we're wrong?
- How could we validate/invalidate it?

Examples:
- Assumption: Users will pay $X/month for solution
- Assumption: Market is 50K+ potential customers
- Assumption: Problem is high priority vs nice-to-have
"
```

[Record assumptions. These inform vision CSD section.]

**STEP 4: Generate Product Vision Document**

Only after confirming problem understanding, generate vision using validated inputs.

---

**Now define problem vision using 5W2H + HMW framework:**

- **Problem Statement:** One-line, solution-free description
- **5W2H Analysis:** Complete map of problem across all dimensions
- **How Might We:** 2-3 opportunity framings from problem statement
- **North Star Metric:** What success looks like (baseline → target → timeline)
- **Anti-Goals:** Explicit boundaries (what NOT to solve)
- **Critical Assumptions:** CSD matrix (Certainties/Suppositions/Doubts)
- **Evidence & Severity:** Data proving problem exists and matters
- **Stakeholders:** Decision makers, input providers, impacted parties

**Template Reference:** See `knowledge/product-vision.md` for complete problem discovery framework

---

### Step 2: Product Requirements Doc (prd) — **INTERACTIVE FEATURE BRAINSTORM & PRIORITIZATION**

**BEFORE generating PRD**, conduct feature brainstorm and prioritization:

```
"Now that we understand the problem, let's define what we'll build to solve it.

**Feature Brainstorm (HMW + MoSCoW):**

Given the problem we just mapped, what features would help users?

I'll guide brainstorming using How Might We:
'How might we [problem reframed as opportunity]?'

Examples (from your problem):
- HMW: [Opportunity 1]
- HMW: [Opportunity 2]
- HMW: [Opportunity 3]

What features come to mind? Don't filter yet - just brainstorm."
```

[Collect feature ideas. Listen for user's mental model of solution.]

**STEP 2: Prioritize Using MoSCoW**

```
"Now let's prioritize using MoSCoW framework.

I've listed the features you mentioned. For each, ask:
- Is this MUST HAVE? (product meaningless without it)
- Is this SHOULD HAVE? (important but not MVP-blocking)
- Is this COULD HAVE? (nice-to-have)
- Is this WON'T HAVE? (explicitly out of scope)

Let's go through each:

Feature: [Feature 1]
- Is [Feature 1] core to solving the problem? (MUST/SHOULD/COULD/WON'T)
- What if we removed it? Would product still work?
- What would users judge you on at launch?

[Repeat for each feature]
"
```

[Wait for prioritization. Probe reasoning.]

**STEP 3: Confirm Feature Scope**

```
"Let me confirm your feature scope for MVP:

**MUST HAVE (MVP Core):**
[Feature 1, Feature 2, Feature 3]
These directly solve: [problem]

**SHOULD HAVE (V1.1):**
[Feature 4, Feature 5]
These enhance: [UX/efficiency/trust]

**COULD HAVE (V2+):**
[Feature 6, Feature 7]
These add: [polish/niche value]

**WON'T HAVE (Out of Scope):**
[Feature 8]
Reason: [too complex/not core/requires [dependency]]

Does this scope feel right? Is anything missing from MUST HAVE? Anything we should move to SHOULD?
"
```

[Wait for confirmation. This informs PRD feature list.]

**STEP 4: Define Success Criteria Per Feature**

```
"For each feature, how will we know it worked?

Feature: [Feature Name]
- What will users be able to do?
- How will we measure adoption? (usage metric, satisfaction, business KPI)
- What's success vs failure?

[Repeat for each feature]
"
```

[Record success criteria. These go in PRD as measurable outcomes.]

**STEP 5: Generate PRD Document**

Only after confirming feature scope and success criteria, generate PRD using validated inputs.

---

**Now document feature requirements using scope + success criteria:**

- **Problem Context:** Link to vision and business objectives
- **Product Goals:** Clear statements tied to objectives and success criteria
- **Feature Set (PRD-F-#):** One block per feature with:
  - Problem→Feature mapping
  - Success criteria (measurable outcomes)
  - Key user scenarios
  - Dependencies and data touchpoints
  - UX guardrails and risks
  - Rollout strategy
- **Analytics Plan:** Events to emit, dashboards to track
- **Release & Rollout:** Milestones, feature flags, communication plan
- **Risks & Decisions:** Risk register and decision log

**Template Reference:** See `knowledge/prd.md` for complete PRD structure and scope framework

---

### Step 3: User Stories (stor) — **INTERACTIVE ACCEPTANCE CRITERIA**

**BEFORE generating user stories**, define acceptance criteria collaboratively:

```
"For each feature, let's write user stories with clear acceptance criteria.

User stories have the format:
'As a [user type], I want [capability], so that [benefit]'

Then we add Given/When/Then acceptance criteria (Gherkin).

Feature: [PRD Feature Name]
Related Stories: [List features this decomposes into]

Story 1: [Feature scenario]
- As a [job doer]
- I want [capability]
- So that [benefit]

Happy path acceptance criteria:
- Given [precondition]
- When [action]
- Then [result]

Alternative scenario:
- Given [precondition]
- When [alternative action]
- Then [alternative result]

Error scenario:
- Given [error condition]
- When [error trigger]
- Then [error handling]

Does this capture what we're trying to enable?"
```

[Wait for user to review and confirm. Iterate on criteria.]

**STEP 2: Confirm Story Coverage**

```
"Let me confirm we've covered all important user scenarios:

Feature: [Feature Name]
- Happy path (main success): [Story]
- Alternative paths (valid variations): [Stories]
- Error scenarios (failure handling): [Stories]
- Edge cases (unusual conditions): [Stories]

Are we missing any important scenarios?
"
```

[Add missing stories. Confirm coverage.]

**STEP 3: Generate User Stories Document**

Only after confirming acceptance criteria and story coverage, generate stories document.

---

**Now document user stories using Gherkin acceptance criteria:**

- **Story Index:** All stories with epic, priority, journey reference
- **Story Structure:** AS/I WANT/SO THAT + preconditions/postconditions
- **Acceptance (Gherkin):** Happy/Alternative/Error paths with Given/When/Then
- **Trace:** Links to functional requirements (FR-#) and backend endpoints
- **Definition of Done:** Telemetry, accessibility, error messages, docs

**Template Reference:** See `knowledge/user-stories.md` for complete story structure with Gherkin examples

---

### Step 4: Feature Specifications (fs) — **INTERACTIVE COMPLEXITY ASSESSMENT**

**BEFORE generating feature specs**, determine which features need detailed specs:

```
"For some complex features, we need detailed specifications beyond user stories.

Feature Spec is needed when:
1. Feature has >3 distinct business rules
2. Feature has state machine/workflow with multiple states
3. Feature has complex data transformations
4. Feature has API interactions with multiple endpoints
5. Feature has conditional logic that's hard to express in Gherkin

Feature Spec includes:
- Inputs/outputs with data types
- Business rules (validation, transformation, calculation, constraint, state, authorization, temporal)
- State transitions with conditions
- API endpoint hints
- Error handling
- Implementation guidance

Let's review each feature:

Feature: [Feature Name]
- How many distinct business rules? [Count]
- Does it need a state machine? (Yes/No)
- How complex are the rules?

Decision: NEEDS SPEC / STORY SUFFICES
"
```

[For each feature, make spec/story decision together.]

**STEP 2: Define Feature Spec Scope**

For features needing specs:

```
"For Feature: [Complex Feature Name]

Let's define the detailed specification.

**Business Rules (what must always be true):**
- Validation rules (checks on inputs)
- Transformation rules (data conversion)
- Calculation rules (formulas)
- Constraint rules (business logic)
- State rules (transitions)
- Authorization rules (who can do what)
- Temporal rules (time-based)

For each rule:
- What is the rule?
- When does it apply?
- What happens if violated?
- Who enforces it? (client/server/both)

**State Transitions (if this feature has state machine):**
- What states exist?
- What triggers transitions?
- What conditions allow/block transitions?
- What happens on transition?

**Inputs & Outputs:**
- What data goes in?
- What data comes out?
- What are constraints on each field?

**API Endpoints (if applicable):**
- What endpoints are needed?
- What methods (GET/POST/PUT/DELETE)?
- What auth is required?
- What error responses?
"
```

[Record detailed spec requirements collaboratively.]

**STEP 3: Generate Feature Spec Document**

Only after confirming specification scope, generate feature spec document.

---

**Now document feature specification with detailed business rules and state handling:**

- **Feature Context:** Link to PRD feature and user stories
- **Complexity Justification:** Why this feature needs detailed spec (>3 rules/state machine)
- **Inputs:** Parameters with types, constraints, validation
- **Outputs:** Return values, data structures, HTTP status codes
- **Business Rules:** Categorized by type (validation, transformation, calculation, constraint, state, authorization, temporal)
- **State Transitions:** Initial state, triggers, transitions, recovery paths, edge cases
- **State Machine Diagram:** Mermaid diagram for complex flows
- **API Endpoint Hints:** Endpoint path, method, auth, request/response schemas
- **Error Handling:** Error types, retry strategy, fallback behavior
- **Implementation Guidance:** Technology recommendations, code patterns, performance targets

**Spec IDs:** FS-[kebab-feature-name]-# (e.g., FS-invoice-calc-1, FS-payment-retry-2)

**Template Reference:** See `knowledge/feature-spec.md` for complete detailed specification framework evolved from FRD

---

## Workflow Sequence

```
1. vis (Product Vision)
   → Use 5W2H to deeply understand problem
   → Every question has specific answer
   → Critical assumptions identified and testable
   ↓

2. prd (Product Requirements Doc)
   → HMW brainstorm for features
   → MoSCoW prioritization (MUST/SHOULD/COULD/WON'T)
   → PRD-F-# features with success criteria
   → Explicit non-goals and constraints
   ↓

3. stor (User Stories)
   → Gherkin acceptance criteria (Given/When/Then)
   → Stories link directly to PRD-F-# (no epics)
   → Happy/Alternative/Error scenarios covered
   → Definition of Done checklist
   ↓

4. fs (Feature Specifications) — ON DEMAND
   → Generated only for complex features (>3 rules or state machine)
   → FS-[name]-# IDs for traceability
   → Inputs/outputs, business rules, state transitions
   → API endpoint hints and error handling
   ↓

✅ DISCOVERY GATE (vision clear, problem understood, assumptions testable)

✅ PLANNING GATE (scope defined, requirements clear, acceptance criteria specific)
```

## Gate Validation

### Discovery Gate Criteria

After generating Product Vision, validate:

- [ ] Clear, solution-free problem statement
- [ ] 5W2H complete (every dimension addressed)
- [ ] North Star metric with baseline/target/timeline
- [ ] Anti-goals set (what NOT to solve)
- [ ] Critical assumptions identified
- [ ] CSD matrix populated (Certainties/Suppositions/Doubts)
- [ ] Evidence cited (data, customer quotes, market research)
- [ ] Severity quantified (time/money/opportunity impact)
- [ ] Stakeholders identified with decision rights
- [ ] Confidence level: Can you articulate the problem without looking?

**Decision:** GO (proceed to Define) | NO-GO (stop, pivot on problem) | ITERATE (refine vision)

### Planning Gate Criteria

After generating PRD, User Stories, and Feature Specs, validate:

- [ ] Feature scope is MoSCoW prioritized (MUST/SHOULD/COULD/WON'T)
- [ ] Success criteria per feature are measurable and testable
- [ ] Every PRD-F-# feature has at least one US-# user story
- [ ] User stories have specific Gherkin acceptance criteria
- [ ] Complex features (>3 rules or state machine) have FS-[name]-# specs
- [ ] Trace complete: PRD-F-# → US-# → (FS-[name]-#) for complex features
- [ ] Non-goals clearly stated
- [ ] Constraints documented
- [ ] Analytics/telemetry plan defined
- [ ] Rollout strategy sketched
- [ ] Confidence level: Could you describe features and success criteria to stakeholders?

**Decision:** GO (proceed to Develop) | DESCOPE (reduce feature set) | ITERATE (clarify requirements)

## Output Format

Generate each document in sequence, ensuring:

1. **YAML Frontmatter:** Complete doc_meta with ID, pillar, gate, feeds
2. **Problem→Feature→Story Traceability:** Every item links upstream
3. **Measurable Criteria:** No vague statements ("users will be happy" → "NPS +5 points")
4. **Gherkin Syntax:** User stories use correct Given/When/Then format
5. **Business Rules Categorized:** Feature specs organize rules by type
6. **State Machines Diagrammed:** Complex features show Mermaid state diagrams
7. **ID Consistency:** BO-#, PRD-F-#, US-#, FS-[name]-# used throughout

## Quality Checks

After generation, validate:

- **Problem Clarity:** Can you explain problem in one sentence?
- **Feature Justification:** Does each PRD-F-# solve part of the problem?
- **Acceptance Specificity:** Could QA engineer test each story with no questions?
- **Scope Ruthlessness:** Are MUST/SHOULD/COULD decisions defensible?
- **Complexity Assessment:** Is feature-spec decision (needed/not needed) correct?
- **Traceability Chain:** Can trace from problem → feature → story → spec (if needed)
- **Success Measurability:** Can you track success metrics without guessing?

## Knowledge Base

This skill references template files in `knowledge/` directory:

**Core Templates (4 documents):**
- `product-vision.md` - Problem discovery with 5W2H + CSD matrix
- `prd.md` - Product requirements with PRD-F-# features and scope
- `user-stories.md` - User stories with Gherkin acceptance criteria
- `feature-spec.md` - Detailed feature specifications with business rules and state transitions

**Supporting Resources:**
- `example-conversation.md` - Interactive workflow examples

## Best Practices

1. **Ask Before Generating:** Never assume user needs - always discuss first
2. **Quantify Everything:** Vague requirements are untestable (press for numbers)
3. **Show Your Understanding:** Restate requirements back to confirm accuracy
4. **Present Options:** Show trade-offs in prioritization, don't dictate scope
5. **Document Rationale:** Capture WHY decisions were made
6. **Validate at Gates:** Explicit confirmation before proceeding
7. **5W2H Discipline:** Leave no question unanswered in problem discovery
8. **MoSCoW Ruthlessness:** "Won't Have" list is as important as "Must Have"
9. **HMW for Opportunity:** Transform constraints into creative possibilities
10. **Gherkin Precision:** User story acceptance criteria should be testable by automation
11. **Spec Judgment:** Only write detailed specs for genuinely complex features
12. **Conversation Over Template:** If uncertain, ask - don't fill in blanks

## Common Pitfalls to Avoid

- ❌ Starting PRD without understanding problem (vision → prd always)
- ❌ Vague user stories ("user can create invoice" → "given invoice form is open, when user fills fields X/Y/Z, then invoice is saved")
- ❌ Skipping 5W2H in vision (leads to shallow problem understanding)
- ❌ No MoSCoW prioritization (scope creep when all features seem important)
- ❌ Missing acceptance criteria in stories (QA doesn't know what "done" means)
- ❌ Creating spec for simple CRUD feature (unnecessary complexity)
- ❌ Not documenting success metrics (can't prove feature worked)
- ❌ Assuming user needs (always confirm understanding)
- ❌ Forgetting anti-goals (what you DON'T build is as important)
- ❌ Missing edge cases in stories (happy path only → bugs in production)

## Next Steps After This Skill

After Planning gate passes, launch specialized chains:

1. **Architecture Chain:** Generate srs/arch/tech (uses PRD for context)
2. **Data Chain:** Generate data model/schema/dictionary (uses PRD features)
3. **UX Chain:** Generate journeys/wireframes/design (uses stories + PRD)
4. **API Backend:** Generate endpoint specs (uses stories + FRD)

Feature development chain outputs (vision, prd, stor, fs) inform all downstream work and serve as single source of truth for "what we're building and why."
