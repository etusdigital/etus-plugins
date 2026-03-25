---
doc_meta:
  id: fb
  display_name: Feature Brief
  pillar: Planning
  owner_role: Product Lead
  summary: Lightweight feature documentation for single features within existing products.
  order: 0
  requires: []
  feeds: [user-stories, design-delta, impl-plan]
---

# Template: Feature Brief

**File:** `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md`

**Purpose:** Single document capturing problem, scope, personas, and acceptance criteria for a single feature. Lightweight alternative to a full PRD for Feature mode.

## Responsaveis

- **Owner:** PM (Product Manager)
- **Contribuem:** Tech Lead, Design Lead
- **Aprovacao:** PM + Tech Lead

## Table of Contents
1. [Complete Structure](#complete-structure)
2. [Filling Notes](#filling-notes)
3. [Concrete Example](#concrete-example-minimal)
4. [Validation](#validation)

---

## Complete Structure

```markdown
# Feature Brief: [Feature Name]

**Date:** [DATE]
**Author:** [NAME]
**Status:** [DRAFT | APPROVED]
**Mode:** Feature

---

## Problem Statement

[What problem does this feature solve? Who has this problem? How are they solving it today?]

## Source Coverage

### Selected Solution
- [SOL-#] [Chosen direction]

### Referenced JTBD
- [JTBD-#] [Summary]

### Referenced Use Cases
- [UC-#] [Summary]

### Referenced Edge Cases
- [EDGE-#] [Summary or "Not applicable" with reason]

## Feature Description

### FB-1: [Core Behavior]
[Description of the primary behavior this feature delivers]

### FB-2: [Secondary Behavior]
[If applicable]

## Target Users

### Primary User
**Persona:** [Name/role]
**Pain Point:** [What frustrates them today]
**Expected Outcome:** [What success looks like for them]

### Secondary User
**Persona:** [Name/role]
**Pain Point:** [What frustrates them today]
**Expected Outcome:** [What success looks like for them]

## Acceptance Criteria

- [ ] [Criterion 1 — specific, testable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Scope Boundaries

### In Scope
- [What this feature includes]

### Out of Scope
- [What this feature explicitly does NOT include]

## Non-Goals Registry

### NG-1: [What NOT to do]
- **Statement:** [what must NOT happen — specific and testable]
- **Reason:** [why excluded]
- **Scope:** permanent | deferred_to_v2 | conditional
- **Adjacent behavior:** [valid functionality that neighbors this non-goal]
- **Downstream docs that must respect:** [user-stories, feature-spec, api-spec, tech-spec, wireframes, impl-plan]

### NG-2: [What NOT to do]
- **Statement:** [what must NOT happen — specific and testable]
- **Reason:** [why excluded]
- **Scope:** permanent | deferred_to_v2 | conditional
- **Adjacent behavior:** [valid functionality that neighbors this non-goal]
- **Downstream docs that must respect:** [user-stories, feature-spec, api-spec, tech-spec, wireframes, impl-plan]

## Design Considerations

[Any technical or UX considerations that affect how this should be built]

## Dependencies

- [External dependency 1]
- [Internal dependency 1]

## Outstanding Questions

### Resolve Before Implementation
- [Blocking question]

### Deferred
- [Non-blocking question]


## O que fazer / O que nao fazer

**O que fazer:**
- Definir escopo claro com o que esta dentro e fora
- Incluir user stories com aceite verificavel
- Vincular a BO-# ou PRD-F-# existentes quando disponivel
- Manter conciso — feature brief nao e PRD completo

**O que nao fazer:**
- Nao iniciar sem definir o problema primeiro
- Nao misturar multiplas features em um brief
- Nao pular metricas de sucesso
- Nao detalhar arquitetura aqui (isso e design-delta)

## Related Documents

- Project Context: [link if exists]
- PRD: [link if exists]
- Product Vision: [link if exists]
```

---

## Filling Notes

### Section: Problem Statement

- Be specific about WHO has the problem and WHAT they do today
- Avoid generic statements like "users need a better way to..."
- Include the cost of the current approach (time wasted, errors made, revenue lost)
- One paragraph is usually sufficient

### Section: Source Coverage

- Every feature brief should explicitly point back to the ideation layer
- At minimum, reference:
  - 1 JTBD that justifies the feature
  - 1 use case that proves the workflow exists
  - 1 edge case or an explicit "not applicable" note
- This section is what prevents the feature brief from becoming disconnected from the upstream problem space

### Section: Feature Description (FB-#)

- Each FB-# represents a distinct behavior or capability
- Keep to 1-4 FB-# items — more suggests the feature is actually a product initiative
- Each FB-# should be independently understandable
- Use action-oriented descriptions: "User can..." or "System automatically..."

### Section: Target Users

- Primary user = who benefits most
- Secondary user = who else interacts with this feature (admins, reviewers, etc.)
- Each persona needs a concrete pain point (not "they want it" but "they spend 20 min/day doing X manually")

### Section: Acceptance Criteria

- Every criterion must be testable — a QA engineer should be able to verify pass/fail
- Minimum 2 criteria, typically 3-5
- Include both happy path and key edge cases
- Format: "[Actor] can [action] and [expected result]"

Good:
- "User can upload a CSV file up to 10MB and see a preview of the first 5 rows within 3 seconds"
- "System rejects files over 10MB with a clear error message showing the size limit"

Bad:
- "Upload works well"
- "Feature is fast"

### Section: Scope Boundaries

- **In Scope:** What the feature DOES deliver
- **Out of Scope:** What the feature explicitly does NOT deliver
- Out of Scope prevents scope creep and sets expectations
- Be specific: "Multi-language support (deferred to Q3)" not just "internationalization"

### Section: Non-Goals Registry (NG-#)

- Each NG-# represents a specific behavior that must NOT be built
- Every NG-# needs a clear statement (testable), reason, and scope classification
- **Scope values:** `permanent` (never build), `deferred_to_v2` (build later), `conditional` (build only if X)
- **Adjacent behavior** clarifies where the boundary between allowed and forbidden lies
- **Downstream docs that must respect** lists which downstream documents must not contradict this non-goal
- Minimum 1 NG-# per feature brief
- The check-traceability skill will scan downstream docs for NG-# violations

### Section: Design Considerations

- Technical constraints (must work with existing API, must use existing auth)
- UX considerations (must be accessible, must work on mobile)
- Performance expectations (must handle N concurrent users)
- Migration considerations (existing data, backward compatibility)

---

## Concrete Example (Minimal)

```markdown
# Feature Brief: CSV Bulk Import

**Date:** 2026-03-17
**Author:** Product Team
**Status:** APPROVED
**Mode:** Feature

---

## Problem Statement

Operations managers spend 2-3 hours per week manually entering customer data one record at a time through the admin panel. They already have this data in spreadsheets but have no way to upload it in bulk. This causes data entry errors (estimated 5% error rate) and delays customer onboarding by 2-3 business days.

## Source Coverage

### Selected Solution
- SOL-1: Guided CSV import with preview + row-level validation

### Referenced JTBD
- JTBD-1: Upload customer data in bulk without manual correction

### Referenced Use Cases
- UC-1: Manager uploads a valid CSV and reviews a preview before import

### Referenced Edge Cases
- EDGE-1: Uploaded CSV contains invalid phone numbers and must return row-level validation errors

## Feature Description

### FB-1: CSV Upload and Preview
User uploads a CSV file through a drag-and-drop interface, sees a preview of the first 10 rows with column mapping, and can correct mappings before importing.

### FB-2: Import Validation and Error Reporting
System validates all rows against data rules before importing. Invalid rows are flagged with specific error descriptions. User can fix and re-upload only the failed rows.

## Target Users

### Primary User
**Persona:** Operations Manager (Sarah)
**Pain Point:** Spends 2-3 hours/week on manual data entry with 5% error rate
**Expected Outcome:** Bulk import 500+ records in under 5 minutes with automated validation

## Acceptance Criteria

- [ ] User can upload a CSV file up to 10MB via drag-and-drop or file picker
- [ ] System displays preview of first 10 rows with auto-detected column mapping
- [ ] User can manually adjust column mapping before importing
- [ ] Invalid rows are rejected with specific error messages (row number + field + reason)
- [ ] User can download a CSV of failed rows, fix them, and re-upload

## Scope Boundaries

### In Scope
- CSV file format only
- Customer data entity (name, email, phone, company)
- Single-file upload (one file at a time)

### Out of Scope
- Excel (.xlsx) support (deferred to next iteration)
- Other data entities (products, orders) — separate feature briefs
- Automated scheduled imports (API integration, not UI upload)
- Real-time progress bar during import (show spinner + completion message)

## Non-Goals Registry

### NG-1: No Excel support in v1
- **Statement:** The import feature must NOT accept .xlsx or .xls files
- **Reason:** Adds library dependency (openpyxl) and sheet-selection UI complexity; CSV covers 90% of use cases
- **Scope:** deferred_to_v2
- **Adjacent behavior:** CSV upload is fully supported; users can export Excel to CSV before uploading
- **Downstream docs that must respect:** user-stories, feature-spec, api-spec, impl-plan

### NG-2: No scheduled/automated imports
- **Statement:** The system must NOT trigger imports automatically or via API without user interaction
- **Reason:** Automated imports require audit trail, idempotency keys, and rate-limiting infra not in scope
- **Scope:** permanent
- **Adjacent behavior:** Manual upload via UI is supported; API batch creation endpoint exists but is not exposed for scheduled use
- **Downstream docs that must respect:** api-spec, tech-spec, impl-plan

## Design Considerations

- Must integrate with existing customer data model (no schema changes)
- File processing should happen asynchronously to avoid UI blocking
- Consider rate limiting to prevent abuse (max 5 imports/hour per user)
- Must handle UTF-8 encoding for international customer names

## Dependencies

- Existing customer API (POST /api/v1/customers) must support batch creation
- File storage service for temporary CSV storage during processing

## Outstanding Questions

### Resolve Before Implementation
- What is the maximum number of rows per CSV? (Proposal: 10,000 rows)

### Deferred
- Should we support CSV templates for download? (Nice-to-have, not blocking)

## Related Documents

- Project Context: docs/ets/projects/{project-slug}/discovery/project-context.md
- PRD: docs/ets/projects/{project-slug}/planning/prd.md (PRD-F-7: Data Management)
```

---

## Validation

**Before finalizing Feature Brief:**

- [ ] Problem statement is specific (names a persona, quantifies the pain)
- [ ] At least 1 FB-# item defined with clear behavior description
- [ ] At least 1 persona with concrete pain point and expected outcome
- [ ] At least 2 acceptance criteria that are specific and testable
- [ ] In Scope and Out of Scope sections both populated
- [ ] At least 1 NG-# defined with statement, reason, scope, adjacent behavior, and downstream docs
- [ ] Outstanding Questions section present (even if empty)
