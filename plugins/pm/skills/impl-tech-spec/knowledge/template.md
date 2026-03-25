---
doc_meta:
  id: tss
  display_name: Tech Spec (Standalone)
  pillar: Implementation
  owner_role: Tech Lead
  summary: Single-document bug/hotfix specification with root cause and fix plan.
  order: 0
  requires: []
  feeds: []
---

# Template: Tech Spec (Standalone)

**File:** `docs/ets/projects/{project-slug}/bugs/tech-spec-{slug}.md`

**Purpose:** Single document containing everything needed to understand, fix, test, and roll back a bug. Designed for Bug/Hotfix mode — no upstream dependencies.

## Responsaveis

- **Owner:** Tech Lead
- **Contribuem:** Dev responsavel pelo fix, QA
- **Aprovacao:** Tech Lead

## Table of Contents
1. [Complete Structure](#complete-structure)
2. [Filling Notes](#filling-notes)
3. [Concrete Example](#concrete-example-minimal)
4. [Validation](#validation)

---

## Complete Structure

```markdown
# Bug Fix: [Brief Description]

**Date:** [DATE]
**Author:** [NAME]
**Severity:** [Critical | High | Medium | Low]
**Status:** [DRAFT | APPROVED | FIXED]
**Mode:** Bug/Hotfix

---

## Problem Description

[What is broken? What is the user experiencing?]

## Reproduction Steps

1. [Step 1]
2. [Step 2]
3. [Expected: X, Actual: Y]

**Frequency:** [Always | Intermittent (~X% of the time) | Specific conditions]
**Environment:** [Production | Staging | Development | All]
**First observed:** [Date or deployment version]

## Root Cause Analysis

[Why is this happening? Trace through the code/system to identify the root cause.]

**Confidence:** [HIGH | MEDIUM | LOW]

### Affected Components
- [Component 1]: [how it's affected]
- [Component 2]: [how it's affected]

### Contributing Factors
- [Factor 1: e.g., recent deployment, data migration, config change]
- [Factor 2: if applicable]

## Fix Approach

### Recommended: [Approach Name]
[Description of the fix]

**What changes:**
- [File/component 1]: [specific change]
- [File/component 2]: [specific change]

**Pros:** [why this is best]
**Cons:** [tradeoffs]
**Effort:** [estimated hours/days]
**Risk:** [Low | Medium | High]

### Alternative: [Approach Name]
[Description]

**Pros:** [advantages]
**Cons:** [tradeoffs]
**Effort:** [estimate]
**Risk:** [level]

### Alternative: [Approach Name]
[If a third option exists]

## Test Plan

### Verification Tests
- [ ] [Test case 1: reproduce bug → verify fixed]
- [ ] [Test case 2: variation of the original scenario]

### Regression Tests
- [ ] [Test case 3: related functionality still works]
- [ ] [Test case 4: edge case that could be affected]

### Performance Tests
- [ ] [If applicable: verify fix doesn't degrade performance]

## Rollback Plan

[How to revert if the fix causes issues]

**Rollback steps:**
1. [Step 1]
2. [Step 2]

**Data impact:** [Does the fix change data? Is rollback data-safe?]
**Rollback time:** [Estimated time to complete rollback]

## Timeline

- **Investigation:** [completed / estimated hours]
- **Fix:** [estimated hours/days]
- **Test:** [estimated hours/days]
- **Deploy:** [target date/sprint]

## Related

- [Linear issue link if applicable]
- [Error log or monitoring dashboard link]
- [Related previous incidents]
```

---

## Filling Notes

### Section: Problem Description

- Write from the user's perspective — what do THEY see?
- Include error messages verbatim if available
- Quantify the impact: how many users, how often, what's the business cost?
- One paragraph is usually sufficient

### Section: Reproduction Steps

- Numbered steps, specific and reproducible
- Include environment details (browser, OS, API version)
- Last step should state Expected vs. Actual behavior
- If intermittent: document known conditions and frequency
- If you can't reproduce: state that clearly and document known conditions

### Section: Root Cause Analysis

- Trace the code path from user action to bug manifestation
- Reference specific files, functions, or services if known
- State confidence level honestly:
  - **HIGH** — You've confirmed the root cause in code/logs
  - **MEDIUM** — Strong hypothesis supported by evidence
  - **LOW** — Best guess, needs more investigation
- If LOW: list what additional investigation is needed

### Section: Fix Approach

- Always present at least 2 approaches
- Recommended approach should balance effort, risk, and thoroughness
- For each approach: be specific about what files/components change
- Effort estimates should be realistic (include testing time)
- Risk assessment considers: data safety, backward compatibility, scope of change

Common fix patterns:
- **Surgical fix** — Change the minimum code to fix the exact issue. Low risk, low effort, may not address root cause.
- **Root cause fix** — Address the underlying issue. Higher effort, eliminates the problem class.
- **Workaround + ticket** — Quick workaround now, proper fix later. Lowest effort, creates tech debt.

### Section: Test Plan

- First test case: always reproduce the original bug and verify it's fixed
- Second test case: variation of the original scenario (different data, different user)
- Third test case: regression — related functionality still works
- For Critical/High bugs: include a performance test if the fix touches hot paths

### Section: Rollback Plan

- Assume the fix might make things worse — plan for that
- Database migrations: are they reversible? Is there data loss on rollback?
- Feature flags: can the fix be disabled without a deployment?
- Communication: who needs to know if we roll back?

---

## Concrete Example (Minimal)

```markdown
# Bug Fix: Login Timeout on Mobile Safari

**Date:** 2026-03-17
**Author:** Engineering Team
**Severity:** High
**Status:** APPROVED
**Mode:** Bug/Hotfix

---

## Problem Description

Users on mobile Safari (iOS 17+) experience a 30-second timeout when attempting to log in. The login form submits, shows a spinner, then displays "Request timed out" error. Desktop browsers and Chrome on mobile work correctly. Approximately 15% of our user base is affected (mobile Safari users). Customer support has received 47 tickets about this in the past week.

## Reproduction Steps

1. Open the app in Safari on iOS 17+ (iPhone or iPad)
2. Navigate to /login
3. Enter valid credentials (email + password)
4. Tap "Sign In"
5. Expected: Redirect to dashboard within 2 seconds
6. Actual: Spinner shows for 30 seconds, then "Request timed out" error

**Frequency:** Always (100% reproducible on iOS 17+ Safari)
**Environment:** Production and Staging
**First observed:** 2026-03-12 (after v2.4.1 deployment)

## Root Cause Analysis

The v2.4.1 deployment updated the auth service to use `fetch()` with `keepalive: true` for session persistence. Safari on iOS 17+ has a known bug where `keepalive: true` combined with `credentials: 'include'` causes the request to hang until timeout when the response includes `Set-Cookie` headers with `SameSite=None`.

**Confidence:** HIGH — Confirmed by reproducing in Safari Technology Preview and verifying the fetch options in `auth-service.ts:L47`.

### Affected Components
- `auth-service.ts` (line 47): `fetch()` call with `keepalive: true`
- Login flow only — all other API calls use a different fetch wrapper without `keepalive`

### Contributing Factors
- v2.4.1 added `keepalive: true` to improve session persistence on page unload
- Safari iOS 17 WebKit bug (tracked: webkit.org/b/259835)

## Fix Approach

### Recommended: Conditional keepalive (Safari detection)
Disable `keepalive: true` for Safari on iOS by detecting the user agent before setting fetch options. Apply only to the auth endpoint.

**What changes:**
- `src/services/auth-service.ts`: Add Safari detection, conditionally set `keepalive`

**Pros:** Minimal change, fixes the issue, preserves keepalive for browsers that support it correctly
**Cons:** User agent detection is fragile (but this is a known WebKit bug, not a feature detection scenario)
**Effort:** 2 hours (including testing)
**Risk:** Low

### Alternative: Remove keepalive entirely
Remove `keepalive: true` from all auth fetch calls.

**Pros:** Simplest fix, no browser detection needed
**Cons:** Loses session persistence on page unload for ALL browsers (the original reason for adding it)
**Effort:** 30 minutes
**Risk:** Low (but degrades UX for non-Safari users)

## Test Plan

### Verification Tests
- [ ] Login works on Safari iOS 17+ (iPhone 15 Pro, iPad Air)
- [ ] Login works on Safari iOS 16 (regression)

### Regression Tests
- [ ] Login works on Chrome desktop
- [ ] Login works on Chrome mobile (Android)
- [ ] Session persistence on page unload still works on Chrome (keepalive preserved)

## Rollback Plan

Revert the single-file change in `auth-service.ts`. No database changes, no data migration.

**Rollback steps:**
1. `git revert [commit hash]`
2. Deploy to staging, verify Safari still broken (expected — back to pre-fix state)
3. Deploy to production

**Data impact:** None
**Rollback time:** <15 minutes

## Timeline

- **Investigation:** Completed (3 hours)
- **Fix:** 2 hours
- **Test:** 1 hour
- **Deploy:** Today (hotfix deployment)
```

---

## Validation

**Before finalizing Tech Spec (Standalone):**

- [ ] Problem description clearly states what is broken and who is affected
- [ ] Reproduction steps are specific enough to reproduce (or clearly marked as intermittent)
- [ ] Root cause analysis present with confidence level
- [ ] At least 2 fix approaches documented with pros/cons/effort/risk
- [ ] Recommended approach clearly identified
- [ ] Test plan has at least 2 test cases (verify fix + regression)
- [ ] Rollback plan documents how to revert and whether it's data-safe
- [ ] Severity assessment present

## O que fazer / O que nao fazer

**O que fazer:**
- Documentar root cause com evidencia (logs, traces, repro steps)
- Incluir impacto no usuario e severidade
- Descrever o fix com verificacao testavel
- Incluir plano de rollback se o fix falhar

**O que nao fazer:**
- Nao adivinhar root cause — investigar com dados
- Nao corrigir sem entender a causa raiz
- Nao pular testes de regressao
- Nao criar bug spec para typos ou config changes (overhead desnecessario)

