# Guide: Interactive Interview for Feature Spec

**Objective:** Guide user through detailed technical specification of complex features, documenting business rules, state machines, validations, and error handling.

## Table of Contents
1. [Block 1: Feature Confirmation & Qualification](#block-1-feature-confirmation--qualification-2-3-min)
2. [Block 2: Business Rules Enumeration](#block-2-business-rules-enumeration-8-10-min)
3. [Block 3: State Machine](#block-3-state-machine-if-applicable-8-10-min)
4. [Block 4: Validation Rules](#block-4-validation-rules-5-8-min)
5. [Block 5: Error Handling & Recovery](#block-5-error-handling--recovery-8-10-min)
6. [Block 6: Edge Cases](#block-6-edge-cases-5-8-min)
7. [Block 7: Data Transformations](#block-7-data-transformations-if-applicable-5-8-min)
8. [Block 8: Business Logic Decisions](#block-8-business-logic-decisions-3-5-min)
9. [Block 9: Testing Scenarios](#block-9-testing-scenarios-5-min)
10. [Block 10: Consolidation & Generation](#block-10-consolidation--generation-2-3-min)
11. [General Notes](#general-notes)
12. [Reference: Gherkin Compatibility](#reference-gherkin-compatibility)

---

## Block 1: Feature Confirmation & Qualification (2-3 min)

### Context

user-stories.md exists. Skill invoked for feature that qualified as complex.

### Questions

1. **Confirmation:**
   "We'll detail feature-spec for: [Feature Name]
   Linked to US-#: [US-#]
   Kebab name (slug): [kebab-name]

   Correct?"

   - If no: "Correct the name or return to user-stories"
   - If yes: Proceed

2. **Reason Being Spec:**
   "You selected that this feature has:
   - [>3 business rules] OR
   - [State machine] OR
   - [Complex validation]

   Correct? Any aspect not mentioned?"

   - User confirms or adds reason
   - Document this (for Overview)

### Output

- Feature and kebab-name confirmed
- Complexity reason documented
- Ready to detail

---

## Block 2: Business Rules Enumeration (8-10 min)

### Context

Now, list ALL business rules that define feature behavior.

### Flow

**Initial Question:**

```
"What are ALL the business rules for [Feature Name]?

A business rule is a 'system must' or 'if X then Y'.

Example for 'Duplicate Invoice':
  1. Copy all items from original invoice
  2. Reset due date to default (30 days)
  3. Mark in audit as 'Duplicated from #123'
  4. Notify client if original was sent
  5. Don't allow duplicate if status != 'Final'

For your feature, what are the rules? (List all you know)"
```

User lists (ex):
```
1. Mark as paid changes status
2. Can mark as paid only if was sent
3. Records payment date
4. Records payment method
5. If save fails, retry
```

**Structuring:**

Skill converts to FS-[kebab-name]-# format:

```
FS-payment-tracking-1: State change on mark paid
FS-payment-tracking-2: Can only mark sent invoices
FS-payment-tracking-3: Track payment date
FS-payment-tracking-4: Track payment method
FS-payment-tracking-5: Retry on save failure
```

**Validation Question:**

```
"Do these [N] rules cover complete behavior?

Are there edge rules missing? For example:
  - If [scenario], then [behavior]?
  - Are there calculation/transformation rules?
  - Are there permission rules (who can do X)?
  - Are there audit rules (track when/who)?

Missing anything?"
```

User may add:
```
6. Only invoice owner can mark as paid
7. Audit: record who and when marked as paid
```

**Refinement:**

If user mentions "rule X", ask:

```
"Rule X: [User statement]

Specifically:
  - WHEN applies? (what condition triggers)
  - RESULT? (what system does / what state changes)
  - EXAMPLE? (concrete scenario)"

User details, skill documents for FS-[kebab-name]-#
```

### Result

- [N] business rules enumerated (minimum 3-4)
- Each rule has: Description, When applies, Result, Example
- FS-[kebab-name]-# IDs sequential 1, 2, 3, ...
- Ready for state machine (if applicable)

### Good vs Bad

**Good Rules:**

```
FS-invoice-1: Invoice status changes from "Sent" to "Paid" when marked

FS-invoice-2: Cannot mark invoice as Paid if status is Draft or Cancelled

FS-invoice-3: System records payment date and payment method

FS-invoice-4: Only invoice owner can mark invoice as paid (auth check)
```

**Bad:**

```
FS-feature-1: System should work

FS-feature-2: User wants to pay

FS-feature-3: Feature is good
```

---

## Block 3: State Machine (if applicable) (8-10 min)

### Context

Feature defined rules. Now, IF feature has multiple states, map state machine.

### Initial Question

```
"Does feature have MULTIPLE STATES (status/modes)?

Example: Invoice can be in:
  - Draft (not saved)
  - Sent (sent to client)
  - Paid (payment received)
  - Overdue (unpaid after 30 days)
  - Cancelled (cancelled)

Simple features (CRUD) may not have states.
Complex features (workflow) have states.

Does your feature [Feature] have states?"
```

**If NO state machine:**

```
User: "No, it's simple, no states"

Skill: "Great! Skip state machine. Move to validations."
```

**If YES state machine:**

```
User: "Yes, has states"

Question: "What are the POSSIBLE states?
(List each state and what it means)"

User describes:
```
States:
  - Draft: not sent yet
  - Sent: sent to client
  - Paid: client paid
  - Overdue: unpaid after 30 days
  - Archived: finished, can't modify
```
```

### Mapping Transitions

```
Question: "From each state, what TRANSITIONS are POSSIBLE?

Draft → [can go to which states?]
Sent → [can go to which?]
Paid → [can go to which?]
...

Example for Invoice:
Draft → Sent (send) or Deleted (cancel)
Sent → Paid (receive payment) or Overdue (30 days passed)
Paid → Archived (archive)
Overdue → Paid (receive late payment)"

User describes transitions
```

**Validation Question:**

```
"Are there IMPOSSIBLE transitions we explicitly don't want?

Example:
  - Paid → Draft (don't allow reverting)
  - Archived → Paid (don't return from archive)
  - Cancelled → * (cancellation is final)

For your feature, which transitions explicitly NOT allowed?"

User lists impossible transitions
```

### Mermaid Diagram Rendering

Skill creates stateDiagram-v2 Mermaid:

```
stateDiagram-v2
  [*] --> Draft
  Draft --> Sent: send()
  Draft --> [*]: delete()
  Sent --> Paid: markPaid()
  Sent --> Overdue: [30 days elapsed]
  Overdue --> Paid: markPaid()
  Paid --> Archived: archive()
  Archived --> [*]
```

**Validation:**

```
Question: "Is this diagram correct?

States:
  Draft, Sent, Paid, Overdue, Archived, [*] ✓?

Transitions:
  Draft → Sent, Deleted ✓?
  Sent → Paid, Overdue ✓?
  ...

Missing transition? Wrong transition?"

User validates and approves
```

### Result

- States and transitions completely mapped
- Mermaid stateDiagram-v2 ready
- Invalid transitions explicitly documented
- Ready for validations

---

## Block 4: Validation Rules (5-8 min)

### Context

Business rules and state machine documented. Now, validations that must run.

### Initial Question

```
"What VALIDATIONS must run for [Feature]?

Validation is: 'if condition is true, error and user can't continue'.

Example for 'Mark as Paid':
  - Validation: Client must exist (client_id must exist in DB)
  - Validation: Payment date can't be in future
  - Validation: Payment method must be valid (check/transfer/card/cash)

For your feature, what validations?"

User lists (ex):
```
1. Invoice status must be "Sent"
2. Payment date can't be in future
3. Payment method is required
4. Only owner can mark as paid
```
```

**Structuring:**

Skill creates table:

```
| Validation | Condition | Error Message | Field |
|-----------|----------|--------------|-------|
| Status Check | status != "Sent" | "Invoice must be Sent" | status |
| Date Check | payment_date > today | "Date can't be future" | payment_date |
| Method Check | payment_method empty | "Select payment method" | payment_method |
| Auth Check | user_id != owner_id | "Only owner can mark" | N/A |
```

**Refinement Question:**

```
"For each validation, what EXACT error message?

Validation 1 (Status): If status != "Sent", user sees:
  '[What exactly?]'"

User: "Invoice must be sent to mark as paid"

Skill documents: "Error Message: 'Invoice must be sent to mark as paid'"
```

### Result

- [N] validation rules in clear table
- Each validation has: Clear boolean condition, Exact error message (what user sees), Affected field
- Ready for error handling

---

## Block 5: Error Handling & Recovery (8-10 min)

### Context

Validations defined. Now, what can go WRONG beyond validation (ex: network, database)?

### Initial Question

```
"What can go WRONG for user using [Feature]?
Not validation (already covered), but SYSTEM FAILURES.

Example for 'Mark as Paid':
  - Error 1: Database doesn't respond when saving status
  - Error 2: Email notification fails
  - Error 3: Payment gateway rejects (if integrated)

For your feature, what failures are possible?"

User lists (ex):
```
1. Database save fails
2. Email notification fails
3. Concurrent edit (another user marked paid at same time)
```
```

**Structuring Error:**

For EACH error:

```
Question: "Error 1: [Error Name]

**Condition:** When exactly does it occur?
  User: 'Database doesn't respond when saving'

**User Message:** What does user see?
  User: 'Failed to save. Try again in a few minutes.'

**System Recovery:** How does system recover?
  User: 'Retry saving after 30 seconds, up to 3 times'

**Retry?** Yes/No/Depends?
  User: 'Yes, automatic retry in background'

**Timeout?** If applicable?
  User: '30 seconds per attempt'"

Skill documents:
```
### Error 1: Database Save Failure

**Condition:** Database doesn't respond for 30 seconds

**User Message:** "Failed to save. Try again in a few minutes."

**System Recovery:**
  1. Async retry every 30 seconds
  2. Up to 3 retries
  3. If all fail, notify user with "Try later"
  4. Log error for debugging

**Retry?** Yes
**Timeout?** 30 seconds per attempt
```
```

**Common Error Patterns:**

| Error Type | User Message | Recovery |
|-----------|--------------|----------|
| Validation fails | [Error specific] | User corrects and retries |
| Network timeout | "Failed. Try again in minutes" | Automatic retry 3x |
| Database fails | "Failed. Try again in minutes" | Automatic retry 3x |
| Permission denied | "No permission for this" | No retry, suggest escalate |
| Resource not found | "[Resource] not found" | No retry, show help |
| Concurrent conflict | "Another user changed this. Reloaded" | Manual retry |

### Result

- [N] error scenarios documented (typical 2-4)
- Each error: Condition, User message, Recovery steps, Retry policy
- Distinction between validation error (user fault) vs system error (retry)

---

## Block 6: Edge Cases (5-8 min)

### Context

Errors documented. Now, RARE BUT VALID situations.

### Initial Question

```
"Are there UNUSUAL but VALID situations system must handle?

Edge case is: rare situation that can happen, must have sensible behavior.

Example for 'Mark as Paid':
  - Edge case 1: User marks paid after marked Overdue automatically
    → System must allow, change from Overdue to Paid
  - Edge case 2: Invoice was duplicated, original marked paid
    → User tries mark duplicate paid too
    → System allows (separate invoices)

For your feature, what edge cases?"

User lists (ex):
```
1. User marks paid with past date (last month)
2. User tries marking twice (double-click, fast)
3. Invoice sent WHILE user marking paid (race condition)
```
```

**Structuring:**

For EACH edge case:

```
Question: "Edge case 1: [Description]

**Situation:** [When happens, why?]
  User: "User double-clicks on 'Mark as Paid'"

**Expected Behavior:** [What system does]
  User: "System processes 1x only, ignores 2nd click"

**Reason:** [Why this is right behavior]
  User: "Avoid marking paid 2x, confusing audit"

Does this make sense?"

Skill documents:
```
### Edge Case 1: Double-Click on Mark Paid

**Situation:** User tries mark invoice paid twice rapidly (double-click or refresh)

**Behavior:**
  System processes first time, ignores subsequent click (idempotent).
  User sees confirmation once.

**Reason:** Avoid duplicate payment record, confusing audit. Operation must be idempotent.
```
```

**Common Edge Cases:**

- Null/empty values (payment method not selected)
- Concurrent operations (two users do at same time)
- Timing issues (user clicks fast, browser refresh)
- Related entities deleted (client deleted after invoice created)
- State contradictions (status changed between UI render and save)

### Result

- [N] edge cases documented (typical 1-3)
- Each edge: Rare situation, Expected behavior, Sensible reason

---

## Block 7: Data Transformations (if applicable) (5-8 min)

### Context

Edge cases documented. IF feature transforms data, describe transformation.

### Initial Question

```
"Does feature TRANSFORM or CREATE data?

Transformation: Feature takes input, modifies, returns output.

Example for 'Duplicate Invoice':
  Input: Original invoice + user_id
  Transformation: Copy fields, reset dates, generate new ID
  Output: New draft invoice

For your feature [Feature], is there data transformation?"
```

**If NO transformation:**

```
User: "No, just updates status"

Skill: "Great! Skip transformations. Move to business logic decisions."
```

**If YES transformation:**

```
User: "Yes, copies items and recalculates totals"

Question: "Describe transformation:

**Input:** What data enters?
  User: "Original invoice object + new due date (optional)"

**Transformation:** What steps?
  User: "1. Copy items, 2. Recalculate totals, 3. Reset dates"

**Output:** What data exits?
  User: "New invoice object, Draft status, ready to send"

**Null Handling:** If field X is null, what happens?
  User: "If due_date is null, use 30 days default"

Complete?"

Skill documents:
```
### Data Transformation: Duplicate Invoice

**Input:**
  - original_invoice (object with all fields)
  - new_due_date (optional, date)
  - user_id (current user)

**Transformation:**
  1. Copy all fields from original (client, items, notes)
  2. Generate new invoice_id (UUID)
  3. For each item: copy qty, description, rate (not item_id)
  4. Recalculate: subtotal, tax, total
  5. Set status = "Draft"
  6. Set parent_invoice_id = original.id (audit)
  7. If new_due_date: use it; else: original.due_date + 30 days

**Output:**
  - new_invoice (object, identical structure to input)
  - ready to save/send

**Null Handling:**
  - If original.description is null → new.description = ""
  - If original.tax_rate is null → new.tax_rate = 0
  - If new_due_date is null → use original.due_date + 30 days
```
```

### Result

- Input, Transformation, Output mapped
- Null handling defined (what default if field empty?)
- Ready for testing scenarios

---

## Block 8: Business Logic Decisions (3-5 min)

### Context

Transformations documented. IF there are design decisions (alternatives explored), document.

### Initial Question

```
"Are there DESIGN DECISIONS in feature?

Decision: "Should we do X or Y?" We chose X because [reason].

Example for 'Mark Paid':
  Decision: "Can user edit invoice AFTER sent?"
  Explored: A) No (lock), B) Yes (versioning), C) Yes with Modified flag
  Chosen: A) No (lock for simplicity)
  Rationale: Simpler implementation, auditable, forces duplicate workflow

For your feature, design decisions?"

User: "Yes, if user double-clicks twice, process 1x or 2x?"

Question: "Decision 1:

**Question:** [Decision to make]
  User: "Should double-click mark paid twice or once?"

**Options:** [Alternatives explored]
  User: "A) Once (idempotent), B) Twice (process each), C) Error on duplicate"

**Chosen:** [Which we choose]
  User: "A) Once (idempotent)"

**Rationale:** [Why]
  User: "Simpler, avoid duplicate payment, user expects idempotent operation"

Make sense?"

Skill documents:
```
### Design Decision: Double-Click Handling

**Question:** Should double-click on "Mark Paid" process payment twice or once?

**Options:**
  A) Once (idempotent): First click processed, second ignored
  B) Twice: Both clicks processed, user gets 2 payments recorded
  C) Error: Second click shows "Already processing"

**Chosen:** A) Once (idempotent)

**Rationale:**
  Simpler implementation. Users expect idempotent operations.
  Prevents duplicate payment records and audit confusion.

**Tradeoff:** Users cannot "undo" by clicking again.
```
```

### Result

- Major design decisions documented
- Rationale clear
- Tradeoffs acknowledged

---

## Block 9: Testing Scenarios (5 min)

### Context

All details documented. Now, consolidate testing scenarios covering rules + states + errors.

### Initial Question

```
"Let's define test scenarios covering everything:
  - Business rules
  - States and transitions
  - Validations
  - Errors
  - Edge cases

Each scenario: Setup → Action → Expected Result → Coverage (which rules/states?)"

Examples:

Scenario 1: Happy path
  Setup: Invoice "Sent"
  Action: Click "Mark Paid", select method, confirm
  Expected: Status → "Paid", dashboard updates
  Coverage: Rules 1,3,4; State Sent→Paid; No errors

Scenario 2: Validation error
  Setup: Invoice "Sent"
  Action: Click "Mark Paid", submit without method
  Expected: Error "Select payment method"
  Coverage: Validation "Method required"

Scenario 3: System error
  Setup: Invoice "Sent"
  Action: Click "Mark Paid", database timeout
  Expected: "Failed. Try again."
  Coverage: Error handling, retry

For your feature, scenarios?"

User lists, skill structures in template.
```

### Result

- [N] testing scenarios (typical 4-6 covering happy + error + edge + validation)
- Each scenario: Setup, Action, Expected, Coverage
- Ready for generation

---

## Block 10: Consolidation & Generation (2-3 min)

### Context

All blocks completed. Consolidate and generate feature-spec-[kebab-name].md.

### Validation Question

```
"Feature-spec for [Feature]:
- [N] Business Rules ✓
- State Machine [YES/NO] ✓
- [M] Validation Rules ✓
- [P] Error Handling scenarios ✓
- [Q] Edge Cases ✓
- Data Transformation [YES/NO] ✓
- Design Decisions [YES/NO] ✓
- [R] Testing Scenarios ✓

Complete? Anything missing or needs refinement?"

User validates final
```

### Generation

```
Compile in docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-[kebab-name].md:
  - Overview (linked to US-#)
  - Business Rules with FS-[kebab-name]-# IDs
  - State Machine Mermaid (if applicable)
  - Validation Rules table
  - Error Handling & Recovery table
  - Edge Cases
  - Data Transformations (if applicable)
  - Business Logic Decisions (if any)
  - Testing Scenarios

Output: feature-spec-[kebab-name].md ready
```

### Offer to User

```
"Feature-spec generated!

Options:
1. View in chat (copy manually)
2. Save to docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-[kebab-name].md (automatic)
3. Review before saving (edit in chat)
"
```

---

## General Notes

### Language

- Use English
- Patterns: "Business rule", "State machine", "Error handling"
- Be technical but clear

### Timing

- Total expected: 20-30 minutes for interactive spec
- Can vary with feature complexity
- Simple spec: 15 min, complex (multiple states): 30+ min

### Common Errors

| Error | How to Avoid |
|-------|-------------|
| Rules too vague | Ask: "WHEN applies? RESULT? EXAMPLE?" |
| State machine incomplete | Validate: "Can go from X to Y? Missing transition?" |
| Validations mixed with rules | Rule: "Behavior", Validation: "Condition to reject" |
| Error message not specific | Ask: "What exact message does user see?" |
| Edge case too theoretical | "Can really happen? Way to prove?" |
| Documentation incomplete | Checklist: Overview? Rules? States? Errors? Edge? |

---

## Next Steps

After feature-spec GO decision:

1. **Consolidate Planning Output:**
   - prd.md ✓
   - user-stories.md ✓
   - feature-spec-[kebab-name].md ✓

2. **For EACH complex US-#, repeat feature-spec (if qualifies)**
   - Typical: 1-2 specs per entire PRD

3. **Present to Planning Gate:**
   "Planning complete. [N] features, [M] stories, [P] specs.
   Ready for Implementation Readiness Phase (architecture + data + UX + API)?"

---

## Reference: Gherkin Compatibility

Features with complex business rules (FS-#) must have BDD scenarios derived:

```gherkin
# feature: payment-tracking.feature

Feature: Payment Tracking

  Scenario: Mark invoice as paid (happy path)
    Given invoice in "Sent" status
    When click "Mark as Paid"
      E select "Bank Transfer"
      E confirm
    Then invoice changes to "Paid" status
      E audit records date and method
      E dashboard updates pending total

  Scenario: Validation - date in future
    Given invoice in "Sent" status
    When click "Mark as Paid"
      E enter future date
      E confirm
    Then see error "Date can't be future"
      E invoice stays "Sent"

  Scenario: Error - database fails
    Given invoice in "Sent" status
    When click "Mark as Paid" [database timeout]
    Then see message "Failed. Retrying..."
      E system retries automatically
```

Skill ensures FS-# rules → Gherkin scenarios direct mapping.
