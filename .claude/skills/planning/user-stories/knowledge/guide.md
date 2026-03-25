# Guide: Interactive Interview for User Stories

**Objective:** Guide user through derivation of user-stories from PRD, structuring acceptance criteria in Given/When/Then with high quality.

## Table of Contents
1. [Block 1: Setup & PRD Confirmation](#block-1-setup--prd-confirmation-2-3-min)
2. [Block 2: Persona Definition](#block-2-persona-definition-5-min)
3. [Block 3: User Story Derivation](#block-3-user-story-derivation-15-20-min)
4. [Block 4: Consolidated Validation](#block-4-consolidated-validation-5-min)
5. [Block 5: user-stories.md Generation](#block-5-user-storiesmd-generation-automatic)
6. [Block 6: Feature-Spec Qualification](#block-6-feature-spec-qualification-2-3-min)
7. [Block 7: Planning Gate Decision](#block-7-planning-gate-decision-2-3-min)
8. [General Notes](#general-notes)
9. [Reference: Gherkin Compatibility](#reference-gherkin-compatibility)
10. [Validation Commands](#validation-commands)

---

## Block 1: Setup & PRD Confirmation (2-3 min)

### Context

User passed Planning Gate with validated prd.md.

### Questions

1. "Confirming: your PRD contains [N] features:
   [List PRD-F-# names with Must/Should/Could priorities].
   Correct?"
   - If no: "Let's return to prd.md"
   - If yes: Proceed

2. "From these [N] features, we'll derive user-stories for:
   - All Must Have + Should Have (essential)
   - Could Have (optional, we can skip)

   Want to include Could Have or just Must+Should?"
   - User input: Usually "Must+Should only"
   - Register scope

3. "Any changes since PRD was validated? Scope, customers, constraints?"
   - Register context updates (if any)

### Output

- PRD confirmed and story scope defined
- ~10-15 stories expected (typical for ~7-feature PRD)
- Ready for Phase 2

---

## Block 2: Persona Definition (5 min)

### Context

Now, define 2-3 PRIMARY personas who use the product.

### Flow

1. **Present Concept:**
   "To derive good stories, we need to understand who your main users are.
   Not 'generic types', but specific personas with goals and context.

   Example: in invoicing,
   - Persona 1: Beginning freelancer (no billing experience)
   - Persona 2: Client receiving invoice (accounting)"

2. **Question 1: Main Personas**
   "Who are the 2-3 main personas of [your product]?
   For each one, describe:
   - Who are they (profession, experience)
   - Their main goal
   - 1-2 pain points this product solves"

   User describes (ex):
   ```
   Persona 1: Beginning Freelancer
   - Goal: Create/send invoices quickly
   - Pain: Spends 30min per invoice

   Persona 2: Invoice Recipient
   - Goal: Professional files, accounting integration
   - Pain: Invoices in different formats
   ```

3. **Validation:**
   "Do these personas cover all PRD features?
   Is there a feature only for one outlier persona?"

   - If yes in 3a: Add 3rd persona (rare)
   - If no: "We're good with [2-3]"

4. **Consolidation:**
   Skill documents:
   ```
   ### Persona: [Name]
   [Description, goals, pain points]
   ```

### Output

- 2-3 personas documented
- Each persona has clear goals + pain points
- Ready to derive stories per persona

---

## Block 3: User Story Derivation (15-20 min)

### Context

Personas defined. Now, for EACH PRD-F-#, derive 1+ US-#.

### General Flow

```
For EACH PRD-F-# (in order: Must Have → Should Have):
  - Feature confirmation
  - Scenario brainstorming (who, how, why)
  - User story structuring (1+ per feature)
  - Given/When/Then writing
  - User validation
```

### Step 1: Feature Confirmation

For FIRST feature (PRD-F-1):

```
Question: "First feature is PRD-F-1: [Name]
Description: [Read from prd.md]
Priority: [Must Have]

Is this correct? Anything changed since PRD?"

- If no: Return to PRD
- If yes: Proceed
```

For NEXT features:
```
Question: "Next: PRD-F-2: [Name] [Must Have]
Correct?"

- If yes: Proceed
```

### Step 2: Scenario Brainstorming

```
Question: "For [PRD-F-1: Feature Name],
what are the MAIN ways personas use this?

Think about:
- Persona 1 using feature: main scenario, edge cases
- Persona 2 using feature: specific scenario for them
- Success cases, error cases

List 2-4 scenarios per feature (typical)"

User describes:
```
Example for "Invoice Creation":

Scenario A: Freelancer creates with recent client
  - Has saved client
  - Choose client → auto-filled
  - Add recent items (suggested)
  - Save

Scenario B: New freelancer, no client
  - Fill client from scratch
  - Fill items manually
  - Save

Scenario C: Unsaved draft
  - Start filling
  - Navigate away
  - Prompt "Discard draft?"
```
```

Skill validates: "Do these scenarios cover main cases? Missing anything?"

### Step 3: User Story Structuring

For EACH scenario:

```
Question: "Scenario A: [Description]

Which PERSONA is using this?
What ACTION do they want to do?
Why do they want to do it (BENEFIT)?

Structure as:
'As [Persona], I want [Action], Because [Benefit]'

Example:
'As freelancer, I want to create invoice with pre-filled client,
Because it speeds up process and reduces typos'

Is this correct?"

User confirms/refines
```

Skill structures:

```
### PRD-F-1: Invoice Creation

#### US-1: Create invoice with recent client pre-filled

**Persona:** Beginning Freelancer

**As freelancer, I want to create invoice with pre-filled client,
Because it speeds up process and reduces typos.**

[Now: Acceptance Criteria - Step 4]
```

### Step 4: Given/When/Then Writing

**CRITICAL:** This is the heart. Ensure Given/When/Then is executable, specific, Gherkin-compatible.

```
Question: "For US-1, let's structure acceptance criteria in Given/When/Then.

**Test Scenario:** [Describe scenario in plain language]

**Pre-conditions (Given):**
'Given a logged-in freelancer with saved clients'
[Refine: "What initial data? How many clients? What state?"]

**User Action (When):**
'When clicks "New Invoice"'
[Refine: "Is it a button? Where? Modal or page?"]

**Expected Result (Then):**
'Then sees form with pre-selected client'
[Refine: "Which client? How do we know it's 'recent'? Ordered how?"]

Does this sound right? Anything a QA would be unclear about?"

User confirms/refines
```

**Good Given/When/Then Practices:**

| Level | Good | Bad |
|-------|------|-----|
| **Given** | "Given a logged-in freelancer with 3 clients" | "Given a user" |
| **When** | "When clicks on 'New Invoice' button" | "When uses feature" |
| **Then** | "Then sees dropdown with clients in recent order" | "Then it works" |

### Step 5: Multiple Scenarios per Story

After 1st scenario, ask:

```
Question: "US-1 is done. Are there other test scenarios?

Example: 'What if client is new (no saved client)?'
or 'What if navigate away without saving (draft)?'"

User lists:
- "Yes, new freelancer without client"
- "Yes, draft should have autosave"
- "No, think those 2 cover it"

Structure each as Scenario 2, Scenario 3, etc.
(typical 1-3 scenarios per story)
```

Format for multiple scenarios:

```
#### US-1: Create invoice...

**Scenario 1: Freelancer with recent client**
Given ...
When ...
Then ...

**Scenario 2: New freelancer without client**
Given a new freelancer (no saved clients)
When clicks "New Invoice"
Then sees empty form
  E field Client is required

**Scenario 3: Unsaved draft**
Given a freelancer mid-creating invoice
When navigates away
Then sees prompt "Discard draft?"
  E can save or discard
```

### Step 6: Priority & Estimate

```
Question: "Priority of this story is [Must Have, inherited from PRD-F-1]
Estimate (for refinement): S, M, or L?

- S: 1-3 hours / <3 story points
- M: 5-8 hours / 3-5 story points
- L: 13+ hours / 8+ story points

For US-1 (create with dropdown), which?"

User: "M I think (integrate data, render dropdown, etc.)"

Skill documents:
```
**Priority:** Must Have
**Estimate:** M
```

### Step 7: Feature Spec Rule?

```
Question: "Is it clear in Given/When/Then how this feature works?
Or does it need additional technical document (business rules, state machine, validations)?

Example: If feature is 'Duplicate invoice' with auto-calculation,
might need feature-spec.

For US-1 (client dropdown), does it need?"

User: "No, it's simple, Given/When/Then is enough"

Skill documents:
```
**Feature Spec Needed?** NO
```

**Rule (use /check-feature-spec-rule if unsure):**
- >3 business rules? → YES
- State machine? → YES
- Complex validation/calculation? → YES
- Simple CRUD + clear Given/When/Then? → NO

### Step 8: Iteration & Validation

```
Question: "Review this story:

US-1: Create invoice with recent client pre-filled
Persona: Beginning Freelancer
As/I want/Because: As freelancer, I want to create invoice...
Scenarios: 3 (new client, recent, draft)
Priority: Must Have
Estimate: M

Is this right? Change anything?"

If user: "Yes, it's good" → Next story
If user: "No, missing [X]" → Refine quickly → Revalidate
```

### Context: Iteration per Feature

Repeat Steps 1-8 for EACH PRD-F-#.

**Order:** Must Have features first (sequentially US-1, US-2, ...)
Then Should Have features (continuing sequence US-N...)

Example for 7-feature PRD:
```
PRD-F-1 (Must) → US-1, US-2 [2 stories]
PRD-F-2 (Must) → US-3 [1 story]
PRD-F-3 (Must) → US-4, US-5 [2 stories]
PRD-F-4 (Should) → US-6 [1 story]
PRD-F-5 (Should) → US-7, US-8 [2 stories]
PRD-F-6 (Could) → Skip (decide with user)
PRD-F-7 (Could) → Skip

Total: 8 US-# for 5 in-scope features
```

---

## Block 4: Consolidated Validation (5 min)

### Context

All stories derived. Now, final consolidated review.

### Questions

1. **Complete Coverage?**
   "You reviewed all [N] features from PRD.
   Does each PRD-F-# have ≥1 story?
   Any gap?"

   - If YES gap: "Which feature is missing? Derive story?"
   - If NO gap: "Perfect"

2. **Number of Stories Makes Sense?**
   "Total of [N] stories for [M] features.
   Does this represent correct scope?
   Any story too big or too small?"

   - If big: "Break into 2?"
   - If small: "Consolidate?"
   - If OK: Proceed

3. **Priority Distribution:**
   "You have [X] Must Have, [Y] Should Have, [Z] Could Have.
   Does this make sense with PRD prioritization?"

   - Expected: Must ~60%, Should ~35%, Could ~5%
   - If unbalanced: "Reclassify?"

4. **Personas Used?**
   "Looking at stories: all use personas defined at top?
   Or inventing new persona?"

   - If yes new: "Remove or add as 3rd persona?"

5. **Quality Given/When/Then?**
   "Review 3 random stories. Is each Given/When/Then:
   - Executable (QA can test)?
   - Specific (not vague)?
   - Scenarios cover happy path + edge cases?"

   - If YES: "Great"
   - If NO: "Which needs refinement?" → Quick iteration

### Output

- All stories validated
- Ready for generation

---

## Block 5: user-stories.md Generation (Automatic)

### Context

Interview complete. Data collected:
- Personas defined (2-3)
- [N] user-stories derived per PRD-F-#
- Each US-# with: Persona, As/I want/Because, 1-3 scenarios Given/When/Then
- Priorities inherited from PRD
- Feature-spec rule evaluated (YES/NO)

### Generation Process

1. **Internal Validation:**
   - Each US-# linked to PRD-F-#? ✓
   - Each Given/When/Then specific? ✓
   - Sequential US-# IDs without gaps? ✓
   - Priorities consistent with PRD? ✓

2. **Render:**
   - Structure in docs/ets/projects/{project-slug}/planning/user-stories.md
   - Follow template.md exactly
   - Personas at top
   - Grouped by PRD-F-#
   - Sequential IDs US-1, US-2, ...

3. **Pre-Write Checklist:**
   ```
   Before saving user-stories.md:
   - [ ] Feature index with US-# count
   - [ ] Personas defined (2-3)
   - [ ] Each PRD-F-# has ≥1 US-#
   - [ ] Each US-# has: Persona, As/I want/Because
   - [ ] Each US-# has ≥1 scenario Given/When/Then
   - [ ] Given/When/Then is Gherkin-compatible
   - [ ] Priorities inherited correctly
   - [ ] Sequential US-# IDs
   - [ ] PRD-F-# links validated
   - [ ] Feature-spec rule evaluated for each US-#
   - [ ] Statistics calculated
   ```

4. **Result File:**
   ```
   docs/ets/projects/{project-slug}/planning/user-stories.md
   - [X] lines
   - [N] stories
   - Ready for feature-specs (if needed)
   ```

### Offer to User

"User-stories generated! Options:
1. View in chat (copy manually)
2. Save to docs/ets/projects/{project-slug}/planning/user-stories.md (automatic)
3. Review before saving (edit in chat)
"

---

## Block 6: Feature-Spec Qualification (2-3 min)

### Context

User-stories generated. Now, decide if any story/feature needs feature-spec.

### Flow

```
Question: "For each story, we evaluated if it needs feature-spec
(technical document with business rules, state machine, validation).

Rule:
- >3 business rules → YES
- State machine (multiple states, transitions) → YES
- Complex validation/calculation → YES
- Simple CRUD or clear Given/When/Then behavior → NO

Review [N] stories:
- US-1: [Feature], needs? NO (CRUD)
- US-2: [Feature], needs? YES (state machine: draft → sent → paid)
- US-3: [Feature], needs? NO (simple)
- ...

Which ones need spec?"

User indicates: "US-2, maybe US-5"

Skill notes:
```
US-2: Feature Spec Needed = YES → feature-spec-payment-tracking.md
US-5: Feature Spec Needed = YES → feature-spec-invoice-validation.md
```

### Validation /check-feature-spec-rule

If user unsure:
```
/check-feature-spec-rule "Feature Name"
→ Returns: "YES, has >3 rules: [...]" or "NO, it's CRUD"
```

---

## Block 7: Planning Gate Decision (2-3 min)

### Context

User-stories + (feature-specs decisions) generated. Before proceeding to Implementation Readiness, gate review.

### Planning Gate Criteria

```
✓ Each PRD-F-# has ≥1 US-#?
✓ Each US-# is clear (Persona, Action, Benefit)?
✓ Each US-# has specific Given/When/Then (not boilerplate)?
✓ Priorities (Must/Should/Could) distribution makes sense (~60/35/5)?
✓ Feature-spec rule evaluated (know which specs needed)?
✓ Estimates are placeholders (will refine)?
```

### Possible Decisions

1. **GO**
   → Next steps: feature-specs (if needed), then architecture/design
   → "User-stories is ready. Next: feature-specs for complex stories, then design"

2. **DESCOPE**
   → Remove Could Have or Should Have stories
   → Reclassify to prioritize only Must Have
   → "Which story do we remove to simplify?"

3. **ITERATE**
   → Refine stories (clearer Given/When/Then)
   → Break big stories
   → Consolidate small stories
   → "Which aspect to refine?"

### Result

- Explicit decision made
- Next step clear
- User-stories locked in for downstream (specs, implementation)

---

## General Notes

### Language

- Use English throughout interview
- Patterns: "Given", "When", "Then" instead of local language
- Be conversational

### Timing

- Total expected: 15-25 minutes for interactive interview
- Typical: 6-8 features → 10-15 stories
- Can vary with complexity

### Common Errors

| Error | How to Avoid |
|-------|-------------|
| Vague US (ex: "Use feature") | Add specific Given/When/Then |
| Given without clear state | Ask: "What's the initial setup?" |
| When not user action | Refine: "What button clicks?" |
| Then vague ("works well") | Refine: "What specific result sees?" |
| Inconsistent priority | Validate: "Is this Must Have like PRD?" |
| Inconsistent personas | Use defined personas, don't invent |
| Given/When/Then mixed levels | Given: setup, When: action, Then: assertion |
| Too many scenarios per story | Consolidate if redundant (1-3 typical) |
| No link to PRD-F-# | Validate during generation |

---

## Next Steps

After user-stories GO decision:

1. **Create Feature Specs (if needed):**
   For each US-# with "YES":
   - /feature-spec "Feature Name"
   - Interview about business rules, state machine
   - Generate feature-spec-[kebab-name].md

2. **Consolidate Planning Output:**
   - prd.md ✓
   - user-stories.md ✓
   - feature-spec-[name].md (as needed) ✓

3. **Present to Planning Gate:**
   "Requirements complete. [N] features, [M] stories, [P] specs.
   Scope ~[X] sprints. Ready for Implementation Readiness Phase?"

---

## Reference: Gherkin Compatibility

Given/When/Then in user-stories.md will be used to generate Gherkin BDD:

```gherkin
# feature: create-invoice.feature

Feature: Quick Invoice Creation

  Scenario: Freelancer creates invoice with recent client
    Given a logged-in freelancer with saved clients
    When clicks "New Invoice"
    Then sees form with pre-selected client

  Scenario: New freelancer without client
    Given a new freelancer without saved clients
    When clicks "New Invoice"
    Then sees empty form
      And Client field is required
```

**Skill ensures:** 100% compatibility between user-stories.md Given/When/Then and generated Gherkin.

---

## Validation Commands

```bash
/check-sst             # Validate SST (Given/When/Then unique source)
/check-feature-spec-rule "Feature Name"  # Decide if spec needed
/validate-gate planning  # After this skill
```
