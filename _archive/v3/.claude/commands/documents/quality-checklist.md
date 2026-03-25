---
description: Run quality checklist before merge/deploy — spec compliance, tests, a11y, perf, security
argument-hint: [feature-name or PR-ref]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Quality Checklist

Checking: **$ARGUMENTS**

> **Purpose:** Behavioral enforcement — no merge without passing this checklist. Replaces the old Release Gate with continuous quality checks.
> **Rule:** Failing any P0 item = no merge. P1 items = warning, fix before next sprint.

## Spec Compliance (P0)

- [ ] Code implements what the user story specified (Given/When/Then match)
- [ ] If feature-spec exists, all business rules (FS-[nome]-#) are implemented
- [ ] State machine transitions match spec (no undocumented states)
- [ ] Error handling matches spec (correct HTTP status codes, error messages)
- [ ] Edge cases from spec are handled

## Tests (P0)

- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Edge cases from spec have test coverage
- [ ] No skipped or ignored tests without documented reason

## Performance (P1)

- [ ] Response times within NFR-# targets
- [ ] No N+1 queries introduced
- [ ] Database queries use indexes (no full table scans on production data)
- [ ] Memory usage reasonable under expected load

## Security (P1)

- [ ] Input validation on all user-provided data
- [ ] No secrets in code or logs
- [ ] Authentication/authorization checks in place
- [ ] PII handled according to data-dictionary classification

## Data Quality (P1 — for data-intensive features)

- [ ] Data flows match data-flow-diagram
- [ ] Field types match data-dictionary (dict.*)
- [ ] Events match catalog definitions (ev.*)
- [ ] Retention policies respected

## Accessibility (P2)

- [ ] Keyboard navigation works
- [ ] Screen reader labels present
- [ ] Color contrast meets WCAG AA

## Result

Generate or update `docs/quality-checklist.md` with results:

```markdown
# Quality Check: [feature/PR]
Date: YYYY-MM-DD
Result: PASS / FAIL / WARN

## P0 Items
- [x] Spec compliance: PASS
- [x] Tests: PASS

## P1 Items
- [x] Performance: PASS
- [ ] Security: WARN — [details]

## P2 Items
- [ ] Accessibility: SKIPPED — backend only

## Notes
[Any observations or follow-ups]
```

---

**Quality check complete!** Results recorded. PASS = merge allowed. FAIL = fix required.
