---
doc_meta:
  id: stor
  display_name: User Stories
  pillar: Define
  owner_role: Product Lead
  summary: Authoritative Given/When/Then acceptance criteria linked to PRD features.
  order: 3
  gate: planning
  requires:
  - prd
  optional: []
  feeds:
  - fs
  - arch
  - data
  - ux
  - be
  - fe
uuid: <UUID>
version: 1.0.0
status: Draft
owners:
- <owner>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- Stories
- Gherkin
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# User Stories — [Product]

**Author:** [Your Name] · **Date:** [YYYY-MM-DD]

> **Only place with Acceptance (Gherkin).**
> **No** NFR numbers here (Software Requirements Spec owns NFRs).
> **No** detailed inputs/outputs here (Feature Spec owns detailed specs).

---

## Story Index

All stories decomposing PRD features, prioritized and linked to PRD-F-#:

| ID | Title | PRD Feature | Priority | Points | Scenario | Status |
| --- | --- | --- | --- | --- | --- | --- |
| US-1 | [Title] | PRD-F-1 | P0 | 5 | Happy path | Draft |
| US-2 | [Title] | PRD-F-1 | P0 | 3 | Error handling | Draft |
| US-3 | [Title] | PRD-F-2 | P1 | 8 | Alternative flow | Draft |

---

## Story: [Feature Name - Happy Path]

**ID:** US-1
**PRD Feature:** PRD-F-1
**Priority:** P0 (Must Have - MVP Core)
**Story Points:** 5 (estimate of effort)
**Scenario:** Primary success flow

**User Journey:** [Reference to user-journey.md if exists]
**UI Entry Point:** [Where user initiates this story — route/view]
**UI Exit Point:** [Where user ends — result page/confirmation]

---

### User Story Statement

**As a** [job doer — who is this user?]
**I want** [capability — what do they want to do?]
**So that** [benefit — why do they want it?]

**Example:**
- **As a** freelancer
- **I want** to send a payment reminder to a client with one click
- **So that** I get paid faster without writing a custom message

---

### Context & Preconditions

**Setup required before this story runs:**

- [ ] User is logged in with valid account
- [ ] User has at least one outstanding invoice (unpaid, >7 days old)
- [ ] User has client contact info on file (email or phone)
- [ ] User hasn't sent a reminder to this client in past 3 days

**Data state before story:**
- Invoice exists with status: "unpaid"
- Days outstanding: 7-30
- Client contact: available

---

### Acceptance Criteria (Gherkin)

**Happy Path (Primary Success):**

```
Given:
  - User is on the invoice detail page
  - Invoice is unpaid and >7 days overdue
  - "Send Reminder" button is visible

When:
  - User clicks "Send Reminder" button

Then:
  - Reminder email is sent to client immediately
  - Invoice status shows "reminder_sent" badge
  - User sees success message: "Reminder sent to [client name]"
  - System logs event: ev.invoice.reminder-sent
  - Button is disabled for 3 days (prevent spam)
```

**Alternative Path 1 (Multiple Reminders):**

```
Given:
  - User previously sent a reminder 4+ days ago
  - Invoice still unpaid

When:
  - User clicks "Send Reminder" again

Then:
  - Reminder email is sent (allowed after 3 day cooldown)
  - User sees: "Follow-up reminder sent to [client]"
  - System logs: ev.invoice.reminder-sent
  - Cooldown timer resets to 3 days
```

**Error Path 1 (Missing Contact):**

```
Given:
  - Invoice exists but client contact info is incomplete
  - Email address is missing

When:
  - User clicks "Send Reminder"

Then:
  - Action is blocked (button disabled or grayed out)
  - Tooltip shows: "Update client email to send reminder"
  - User is linked to edit client contact page
  - No email is sent
```

**Error Path 2 (Recently Reminded):**

```
Given:
  - Reminder was sent to this client 2 days ago
  - Cooldown period still active

When:
  - User clicks "Send Reminder"

Then:
  - Action is blocked
  - Message shows: "You can send another reminder in 1 day"
  - Button is disabled (grayed)
  - No email is sent
```

---

### Postconditions

**System state after story completes:**

- [ ] Reminder email delivered to client (verify via email log)
- [ ] Invoice marked as "reminder_sent" with timestamp
- [ ] Event emitted: ev.invoice.reminder-sent (payload: invoice_id, client_id, sent_at)
- [ ] User can see reminder history on invoice detail
- [ ] Cooldown timer starts (3 days before next reminder allowed)

---

### Trace & References

**Feature Decomposition:**
- PRD Feature: PRD-F-1 (Send payment reminders)
- Complex spec needed? No — this story is complete enough

**Implementation:**
- Backend API: POST /api/v1/invoices/{id}/send-reminder (be-ep-5)
- Frontend component: [InvoiceDetailPage.tsx - reminder section]
- Data: Invoice entity, InvoiceReminder events
- Event: ev.invoice.reminder-sent (payload in Data Dictionary)

**Related Stories:**
- US-2 (Error handling for failed email delivery)
- US-4 (Bulk remind multiple invoices)

---

### Definition of Done

Story is done when:

- [ ] Code changes reviewed and approved
- [ ] Automated tests pass (unit + integration)
- [ ] Acceptance criteria verified (all Gherkin paths tested)
- [ ] Event telemetry logged and visible in dashboard
- [ ] Accessibility check passed (WCAG 2.1 AA)
  - [ ] Button has aria-label
  - [ ] Success message is announced to screen readers
  - [ ] Keyboard navigation works (Tab, Enter)
- [ ] Error messages are clear and actionable
- [ ] UI tested on desktop + mobile
- [ ] Docs updated (if adding new API endpoint)
- [ ] Deployed to staging, verified by QA

---

---

## Story: [Feature Name - Error Handling]

**ID:** US-2
**PRD Feature:** PRD-F-1
**Priority:** P0 (Must Have)
**Story Points:** 3
**Scenario:** Handle email delivery failures gracefully

---

### User Story Statement

**As a** freelancer
**I want** to know if a payment reminder fails to send
**So that** I can try a different contact method or follow up manually

---

### Preconditions

- User has initiated reminder send (US-1)
- Email service is temporarily unavailable (transient error)
- OR client email bounces (permanent error)

---

### Acceptance Criteria (Gherkin)

**Transient Error (Retry Path):**

```
Given:
  - User clicks "Send Reminder"
  - Email service returns 503 Service Unavailable

When:
  - System retries up to 3 times (exponential backoff)
  - Retry succeeds on attempt 2

Then:
  - Email is sent successfully
  - User sees success message: "Reminder sent to [client]"
  - No error is shown to user
  - Event logged: ev.invoice.reminder-sent
```

**Permanent Error (Hard Fail Path):**

```
Given:
  - User clicks "Send Reminder"
  - Email bounces (invalid/deleted account)

When:
  - System retries 3 times and all fail
  - Final status: permanently failed

Then:
  - User sees error message: "Couldn't send reminder to [email]. Email may be invalid."
  - CTA shown: "Update client email"
  - Invoice status shows "reminder_failed" badge
  - Event logged: ev.invoice.reminder-failed with error_reason
  - Button re-enabled so user can retry
```

---

### Postconditions

- [ ] Reminder status is "sent" or "failed" (not ambiguous)
- [ ] User knows why it failed and what to do
- [ ] Error event is logged for monitoring

---

### Definition of Done

- [ ] Error handling code written and tested
- [ ] Retry logic implemented with exponential backoff
- [ ] User-facing error messages clear and actionable
- [ ] Event logging works for both success and failure paths
- [ ] Integration test covers transient + permanent failure scenarios
- [ ] QA verified on staging

---

---

## Story: [Feature Name - Bulk Action]

**ID:** US-3
**PRD Feature:** PRD-F-2
**Priority:** P1 (Should Have)
**Story Points:** 8
**Scenario:** Send reminders to multiple overdue invoices

---

### User Story Statement

**As a** freelancer with many overdue invoices
**I want** to send reminders to all overdue clients at once
**So that** I can collect payments faster without sending 20 individual reminders

---

### Preconditions

- User is on invoices list page
- At least 2+ unpaid invoices are >7 days overdue
- All invoices have client contact info

---

### Acceptance Criteria (Gherkin)

**Select & Bulk Send:**

```
Given:
  - User is on Invoices page
  - Invoices list shows: [Unpaid Invoice 1 (15 days), Unpaid Invoice 2 (20 days), etc.]
  - Bulk action checkbox visible for each invoice

When:
  - User selects checkboxes for 3 invoices
  - User clicks "Send Reminders" button

Then:
  - 3 reminders are sent (one per invoice)
  - User sees: "Reminders sent to 3 clients"
  - All 3 invoices show "reminder_sent" badge
  - Invoices are re-sorted (reminded invoices move to bottom)
  - User can undo: "Undo" link available for 10 seconds
```

**Partial Failure (Some Succeed, Some Fail):**

```
Given:
  - User selects 3 invoices for bulk reminder
  - 2 have valid email, 1 email is invalid

When:
  - System sends reminders

Then:
  - Reminders sent to 2 clients (success)
  - 1 invoice shows "reminder_failed" badge
  - User sees message: "Reminders sent to 2 clients. Failed for 1 (invalid email)."
  - Failed invoice highlighted for user to fix
```

---

### Postconditions

- [ ] All selected invoices have reminder_sent or reminder_failed status
- [ ] Events logged for each reminder (success or failure)
- [ ] User knows which reminders succeeded and which failed

---

### Definition of Done

- [ ] Bulk API endpoint implemented (POST /api/v1/invoices/bulk-send-reminders)
- [ ] Idempotency handled (retry safe)
- [ ] Partial success scenario tested
- [ ] Event logging works per-reminder
- [ ] UI shows clear status for each bulk action
- [ ] Undo mechanism tested

---

---

## Story Index (continued for other features)

[Repeat story structure above for PRD-F-2, PRD-F-3, etc.]

---

## ✅ Planning Gate (Stories Review)

Before proceeding to Develop phase, validate:

- [ ] Every PRD-F-# has at least one US-#
- [ ] Every US-# has Gherkin acceptance criteria (Given/When/Then)
- [ ] Happy path, alternative paths, and error paths covered
- [ ] Acceptance criteria are testable (QA could automate them)
- [ ] Preconditions and postconditions clear
- [ ] No acceptance criteria in Feature Specs (stories own this)
- [ ] Definition of Done checklist covers: code, tests, accessibility, docs
- [ ] Trace to backend endpoints and events clear
- [ ] Complex features link to FS-[name] specs
- [ ] Story points estimated (for capacity planning)
- [ ] Confidence: Could QA engineer test each story with no questions?

**Decision:** GO (proceed to Develop) | ITERATE (refine stories)

---

## References

### Upstream
- **prd** - Product Requirements (PRD-F-# features)
- **vis** - Product Vision (problem context)

### Downstream
- **fs-[name]** - Feature Specifications (detailed specs for complex features)
- **arch** - Architecture Diagram (system design)
- **data** - Data Dictionary (event payloads, entities)
- **be** - Backend Requirements (API endpoint specs)
- **fe** - Frontend Requirements (component specs)

---

**End of User Stories**
