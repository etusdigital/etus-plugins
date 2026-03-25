# Template: User Stories

**File:** `docs/ets/projects/{project-slug}/planning/user-stories.md`

**Purpose:** Single Source of Truth for user stories and acceptance criteria. Executable document (Gherkin-compatible).

## Table of Contents
1. [Complete Structure](#complete-structure)
2. [Filling Notes](#filling-notes)
3. [Concrete Example](#concrete-example-minimal)
4. [Validation](#validation)

---

## Complete Structure

```markdown
# User Stories

## Summary

[1 paragraph: linking PRD to story scope]

**Example:**
"This document operationalizes the 8 features from PRD through 12 user-stories.
Each story includes acceptance criteria structured in Given/When/Then,
compatible with BDD and test automation. Total: 12 stories (7 Must Have, 4 Should Have, 1 Could Have)."

---

## Feature Index

| PRD-F-# | SOL-# | Feature | Stories | Priority |
|---------|------|---------|---------|----------|
| PRD-F-1 | SOL-1 | Invoice Creation | US-1, US-2 | Must Have |
| PRD-F-2 | SOL-1 | Email Sending | US-3 | Must Have |
| PRD-F-3 | SOL-2 | Dashboard | US-4, US-5 | Should Have |

---

## Personas

### Persona 1: [Name]

**Description:** [2-3 sentences about who they are, goals, context]

**Goals:** [Top 1-2 objectives when using product]

**Pain Points:** [Problems product solves]

---

### Persona 2: [Name]

[Same pattern]

---

## User Stories

### PRD-F-# [Feature Name]

#### US-#: [Story Title]

**Persona:** [Main persona using this story]

**As [Persona], I want [Action], Because [Benefit]**

---

**Acceptance Criteria:**

**Scenario 1: [Scenario Name]**
```
Given [pre-conditions / initial state]
When [user action / trigger]
Then [expected result / assertion]
```

**Scenario 2: [Scenario Name]**
```
Given [initial state]
When [action]
Then [result]
  E [additional result]
```

---

**Priority:** [Must Have / Should Have / Could Have] (inherited from PRD-F-#)

**Estimate:** [Placeholder, ex: "M", "8-13h", refine in refinement]

**Related to Feature:** PRD-F-#

**Selected Solution:** SOL-#

**Feature Spec Needed?** [YES/NO - use /check-feature-spec-rule to decide]

---

#### US-#: [Story Title]

[Repeat structure above]

---

### PRD-F-# [Feature Name]

[Repeat feature group with its stories]

---

## Statistics

| Metric | Count |
|--------|-------|
| Total User Stories | # |
| Must Have | # |
| Should Have | # |
| Could Have | # |
| Acceptance Scenarios (Given/When/Then) | # |

---

## Traceability

Each US-# feeds into:
- feature-spec-[name].md (if >3 business rules)
- BDD Gherkin scenarios (test automation)
- sprint-planning (estimate, burndown)
- implementation-plan.md (development tasks)

**Chain:** BO-# → O-# → SOL-# → PRD-F-# → US-# → (FS-# if complex) → impl-#

---

## Definition of Ready (DoR)

A story only enters the sprint if:
- [ ] Objective and description are clear
- [ ] Acceptance criteria are defined (Given/When/Then)
- [ ] Dependencies mapped
- [ ] Design / flow available (when applicable)
- [ ] Data / tracking defined (when applicable)
- [ ] Estimated (T-shirt or story points)
- [ ] Prioritized (MoSCoW from PRD-F-#)

---

## Definition of Done (DoD)

A story is only "Done" if:
- [ ] Acceptance criteria met (all Given/When/Then scenarios pass)
- [ ] Tests executed and approved (unit, integration, E2E as applicable)
- [ ] Tracking validated (events firing correctly per PRD)
- [ ] Logs / monitoring configured (when applicable)
- [ ] Documentation / release notes updated (when applicable)
- [ ] Approved by PM / QA (team process)

---

## Mandatory Quality Items

Use as a checklist to ensure delivery includes observability and quality, not just functionality.

### Observability
- [ ] Minimum technical logs and metrics configured
- [ ] Alerts / thresholds defined

### Tracking (Product / Data)
- [ ] Events implemented per PRD tracking section
- [ ] Payload / property validation (campaign_id, user_id, etc.)

### Tests
- [ ] Critical regression cases covered
- [ ] Automated tests (when applicable)

### Documentation
- [ ] Internal docs updated (how to operate / use)
- [ ] Release notes (if applicable)

---

## Single Source of Truth

**Given/When/Then acceptance criteria are the ONLY source for:**
- Definition of "done"
- Testable acceptance criteria
- Gherkin BDD generation
- QA validation

Nothing should rewrite or "translate" these criteria in another document.

```

---

## Filling Notes

### Summary

- Reference prd.md (bridge between features and stories)
- Mention total stories, breakdown by priority
- Indicate Gherkin-compatible
- **Don't** list stories here (only in Index)

### Feature Index

**Format:**

| PRD-F-# | Feature Name | Stories (US-# list) | Priority |
|---------|---|---|---|
| PRD-F-1 | Authentication | US-1, US-2, US-3 | Must Have |
| PRD-F-2 | Dashboard | US-4, US-5 | Should Have |

Order: Must Have features first, then Should Have, then Could Have.

### Personas

**Minimum 2, maximum 3 main personas.**

Structure:

```
### Persona: [Descriptive Name]

**Description:** [Who are they? Context? Why using product?]
Example: "Beginning freelancer, no billing experience,
looking for simple tools to invoice clients professionally."

**Goals:**
- [Primary goal]
- [Secondary goal]

**Pain Points:**
- [Problem 1 product solves]
- [Problem 2]
```

### User Stories - Critical Structure

**Format:**

```
#### US-#: [Story Title]

**Persona:** [One of personas defined above]

**As [Persona], I want [Action], Because [Benefit]**

[Blank line]

**Acceptance Criteria:**

**Scenario 1: [Scenario Name]**
```
Given [pre-condition / initial state]
When [action / trigger]
Then [expected result]
  E [additional assertion]
```

**Scenario 2: [Description]**
```
Given [...]
When [...]
Then [...]
```

**Priority:** [Must Have / Should Have / Could Have]
**Estimate:** [Placeholder: "S" or "M" or "L" or "5-8h"]
**Related to Feature:** PRD-F-#
**Feature Spec Needed?** [YES/NO]
```

**Critical Fields:**

1. **Persona:** One of personas defined above. Don't invent new personas.

2. **As/I want/Because:**
   - "As" = Persona (noun)
   - "I want" = Action/feature (verb + object)
   - "Because" = Benefit (outcome, not means)

   Good:
   ```
   As freelancer, I want to create invoices quickly,
   Because I don't want to spend >5 minutes per invoice
   ```

   Bad:
   ```
   As user, I want to use the feature,
   Because I want to use the feature
   ```

3. **Acceptance Criteria (Given/When/Then):**

   **Given:** Pre-condition. What state must be in effect?
   - "Given a logged-in freelancer with saved clients"
   - "Given an invoice draft in progress"
   - "Given invoices overdue by >30 days in system"

   **When:** User action or system trigger. What happens?
   - "When clicks 'New Invoice'"
   - "When navigates to /dashboard"
   - "When 30 days since creation pass"

   **Then:** Expected result. Assertion. What state results?
   - "Then sees form with pre-filled client"
   - "Then email sent to client@example.com"
   - "Then invoice highlighted as overdue"

   **Tips:**
   - Multiple assertions: use "E" (not And/Or/But)
   - Executable: must run in automation/Gherkin
   - Specific: not vague (not "system works well")
   - 1-3 scenarios per story typical

4. **Priority:** Inherited from PRD-F-#
   - Must Have (from Must Have PRD-F-#)
   - Should Have (from Should Have PRD-F-#)
   - Could Have (from Could Have PRD-F-#)

5. **Estimate:** Placeholder for refinement
   - T-shirt: XS / S / M / L / XL
   - Or hours: 1-3h / 5-8h / 13-21h
   - Or story points: 1 / 2 / 3 / 5 / 8
   - Refine in planning refinement session

6. **Related Feature:** PRD-F-# this story implements
   - Bidirectional traceability

7. **Feature Spec Needed?** YES/NO
   - Use /check-feature-spec-rule if unsure
   - YES if: >3 business rules, state machine, complex validation
   - NO if: simple CRUD, behavior clear in acceptance criteria

### Story Order

**Within each PRD-F-#:**
- Logical order (dependencies first)
- Typical: happy path scenario, then edge cases
- Simple → Complex

**Between PRD-F-#:**
- Must Have features first
- Then Should Have
- Then Could Have

### US-# IDs

- Sequential without gaps (US-1, US-2, ..., US-N)
- Registered in `ids.yml` with story title
- Once assigned, don't change
- Example: `US-1: Create invoice with template`

### PRD-F-# Links

Each US-# must be associated with exactly 1 PRD-F-#.

Validate: "All BO-# covered by at least 1 PRD-F-#, and all PRD-F-# have ≥1 US-#?"

### Statistics

Fill at end:
- Total US-# count
- Breakdown by Must/Should/Could
- Total Given/When/Then scenarios (sum of scenarios)
- Helps validate (too many/few stories for scope?)

---

## Concrete Example (Minimal)

```markdown
# User Stories

## Summary

This document operationalizes the 3 features from PRD (Invoice Creation, Sending, Dashboard)
through 5 user-stories. Total: 5 stories (3 Must Have, 2 Should Have).

---

## Feature Index

| PRD-F-# | Feature | Stories | Priority |
|---------|---------|---------|----------|
| PRD-F-1 | Invoice Creation | US-1, US-2 | Must Have |
| PRD-F-2 | Email Sending | US-3 | Must Have |
| PRD-F-3 | Dashboard | US-4, US-5 | Should Have |

---

## Personas

### Persona: Beginning Freelancer

**Description:** Freelancer just starting, no billing experience,
seeking simplicity in invoicing.

**Goals:**
- Create and send invoices quickly
- Track payments without complication

**Pain Points:**
- Spends 30+ minutes creating each invoice manually
- No clear view of overdue clients

---

### Persona: Invoice Recipient

**Description:** Entity receiving invoices from freelancers,
needs accounting record-keeping.

**Goals:**
- Receive professionally formatted invoice
- File for audit

**Pain Points:**
- Invoices in varying formats
- Hard to track payments

---

## User Stories

### PRD-F-1: Invoice Creation

#### US-1: Create invoice with recent client pre-filled

**Persona:** Beginning Freelancer

**As freelancer, I want to create invoice with pre-filled client data,
Because I don't want to retype already-saved information.**

**Acceptance Criteria:**

**Scenario 1: Happy path - recent client**
```
Given a logged-in freelancer with client history
When clicks "New Invoice"
Then sees invoice form
  E "Client" field shows dropdown with recent clients
  E most recent client is pre-selected
```

**Scenario 2: No recent client**
```
Given a new freelancer without client history
When clicks "New Invoice"
Then sees empty form ready to type
  E "Client" field is required
```

**Priority:** Must Have
**Estimate:** S (5-8h)
**Related to Feature:** PRD-F-1
**Feature Spec Needed?** NO

---

#### US-2: Suggest recent work items

**Persona:** Beginning Freelancer

**As freelancer, I want to see my recent work items suggested,
Because it speeds up invoice creation.**

**Acceptance Criteria:**

**Scenario 1: Items suggested**
```
Given freelancer creating invoice
When expands "Items" section
Then sees last 5 used items with checkbox
  E can click checkbox to add
```

**Scenario 2: Customize quantity**
```
Given suggested items in invoice
When changes quantity of an item
Then total auto-recalculates
```

**Priority:** Must Have
**Estimate:** M
**Related to Feature:** PRD-F-1
**Feature Spec Needed?** NO

---

### PRD-F-2: Email Sending

#### US-3: Send invoice by email

**Persona:** Beginning Freelancer

**As freelancer, I want to send invoice by email with 1 click,
Because I don't want to leave the platform.**

**Acceptance Criteria:**

**Scenario 1: Successful send**
```
Given a created and saved invoice
When clicks "Send by Email"
Then sees confirmation "Email sent to client@example.com"
  E email delivered in <1 minute
  E invoice marked as "Sent"
```

**Scenario 2: Invalid email**
```
Given invoice with invalid email
When clicks "Send by Email"
Then sees error "Invalid email: re-verify"
  E invoice not marked as sent
```

**Priority:** Must Have
**Estimate:** M
**Related to Feature:** PRD-F-2
**Feature Spec Needed?** NO

---

### PRD-F-3: Dashboard

#### US-4: View invoice overview on dashboard

**Persona:** Beginning Freelancer

**As freelancer, I want to see overview of my invoice status,
Because I want to track pending payments.**

**Acceptance Criteria:**

**Scenario 1: Dashboard with data**
```
Given freelancer with created invoices
When accesses /dashboard
Then sees cards showing:
  - Total pending (amount)
  - Number of invoices sent this month
  - Client with highest debt
```

**Scenario 2: Empty dashboard**
```
Given new freelancer without invoices
When accesses /dashboard
Then sees message "No invoices yet"
  E link to "Create first invoice"
```

**Priority:** Should Have
**Estimate:** M
**Related to Feature:** PRD-F-3
**Feature Spec Needed?** NO

---

#### US-5: Mark invoice as paid

**Persona:** Beginning Freelancer

**As freelancer, I want to mark invoice as paid,
Because I need to track cash flow.**

**Acceptance Criteria:**

**Scenario 1: Mark as paid**
```
Given invoice in "Sent" status
When clicks "Mark as Paid"
Then invoice changes to "Paid" status
  E payment date recorded (today by default)
  E dashboard updates pending amount
```

**Scenario 2: Undo payment**
```
Given invoice in "Paid" status
When clicks "Undo Payment"
Then invoice reverts to "Sent"
  E dashboard updates
```

**Priority:** Should Have
**Estimate:** S
**Related to Feature:** PRD-F-3
**Feature Spec Needed?** NO

---

## Statistics

| Metric | Count |
|--------|-------|
| Total User Stories | 5 |
| Must Have | 3 |
| Should Have | 2 |
| Could Have | 0 |
| Acceptance Scenarios | 11 |

```

---

## Validation

**Before finalizing user-stories.md:**

- [ ] Each PRD-F-# has ≥1 US-#
- [ ] Each US-# has: Persona, As/I want/Because
- [ ] Each US-# has ≥1 scenario Given/When/Then
- [ ] Given/When/Then is executable (Gherkin-compatible)
- [ ] Priority inherited from PRD-F-# (not invented)
- [ ] Sequential US-# IDs without gaps
- [ ] PRD-F-# links validated against prd.md
- [ ] Personas used in all stories (no new personas invented)
- [ ] Estimates are placeholders (will refine)
- [ ] Statistics calculated
- [ ] Distribution makes sense (not all Must Have)

**Expected Good Distribution:**
- Must Have: ~50-70% (core for MVP)
- Should Have: ~20-40% (important, not blocker)
- Could Have: ~5-15% (nice-to-have)
