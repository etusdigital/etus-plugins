# Sprint Change Proposal Template

Use this template to document mid-sprint or mid-project changes. Fill all sections — trim sections marked (optional) if the change is small-scope.

---

```markdown
# Sprint Change Proposal: [Brief Description]

<!-- STATUS: DRAFT -->
<!-- Replace DRAFT with COMPLETE after approval -->

**Date:** [YYYY-MM-DD]
**Triggered by:** [who/what — stakeholder request, technical discovery, market shift, etc.]
**Criticality:** [Must change now / Should change soon / Can wait]
**Proposal author:** [Agent/person who created this proposal]

## Source Documents

| Document | Path | Status |
|----------|------|--------|
| [doc name] | [path] | [EXISTS/MISSING] |

## What Changed

[Clear description of the change, new requirement, or problem that triggered this proposal. Include context about when/how it was discovered and any supporting evidence.]

## Impact Analysis

| Document | Affected? | IDs Impacted | What Changes | Effort |
|----------|-----------|--------------|--------------|--------|
| prd.md | Yes/No | PRD-F-# | [description] | Low/Med/High |
| user-stories.md | Yes/No | US-# | [description] | Low/Med/High |
| ost.md | Yes/No | O-#, S-#.# | [description] | Low/Med/High |
| tech-spec.md | Yes/No | NFR-#, ADR-# | [description] | Low/Med/High |
| architecture-diagram.md | Yes/No | — | [description] | Low/Med/High |
| implementation-plan.md | Yes/No | impl-# | [description] | Low/Med/High |
| execution-status.yaml | Yes/No | — | [description] | Low/Med/High |
| api-spec.md | Yes/No | — | [description] | Low/Med/High |
| database-spec.md | Yes/No | — | [description] | Low/Med/High |
| data-dictionary.md | Yes/No | dict.*, ev.* | [description] | Low/Med/High |

**Total effort:** [Low / Medium / High / Very High]
**Documents affected:** [N of M]

## Recommended Approach

**Selected:** [One of: Direct adjustment / Rollback to phase / Re-plan sprint / Accept as tech debt]

**Rationale:**
[Why this approach was chosen over alternatives. Include effort/risk assessment.]

**Alternatives considered:**
1. [Alternative 1] — [why not chosen]
2. [Alternative 2] — [why not chosen]

## Detailed Changes

### PRD Changes (if affected)

| ID | Current | Proposed | Rationale |
|----|---------|----------|-----------|
| PRD-F-N | [current state] | [proposed state] | [why] |

### User Story Changes (if affected)

| ID | Current | Proposed | Rationale |
|----|---------|----------|-----------|
| US-N | [current criteria] | [new criteria] | [why] |

**New stories needed:**
- US-N+1: [new story statement] — linked to PRD-F-#

**Stories to remove/defer:**
- US-N: [reason for removal/deferral]

### Architecture Changes (if affected)

| Area | Current | Proposed | Rationale |
|------|---------|----------|-----------|
| [component/pattern] | [current] | [proposed] | [why] |

**ADR updates:**
- ADR-N: [current decision] → [new decision]

### Implementation Changes (if affected)

| ID | Current | Proposed | Rationale |
|----|---------|----------|-----------|
| impl-N | [current task/status] | [new task/status] | [why] |

**New tasks needed:**
- impl-N+1: [new task description] — linked to US-#

**Tasks to remove/defer:**
- impl-N: [reason for removal/deferral]

### Sprint Impact (if affected)

- Current sprint: [sprint N]
- Sprint capacity change: [+/- N points or T-shirt sizes]
- Timeline impact: [no change / delayed by N days / sprint extended]

### Other Document Changes (optional)

[List any other documents affected with brief change descriptions]

## Traceability

**Change propagation chain:**
```
[Change trigger]
  → PRD-F-# (if affected)
    → US-# (if affected)
      → impl-# (if affected)
        → sprint-status (if affected)
```

**Orphaned references to check:**
- [List any IDs that might become orphaned by this change]

## Linear Sync (if applicable)

| Action | ETUS ID | Linear ID | Description |
|--------|---------|-----------|-------------|
| Update | US-N | LIN-XXX | [what changes] |
| Create | US-N+1 | (new) | [new issue] |
| Close | US-N | LIN-XXX | [reason] |

## Decision

- [ ] Approved by: [name/role]
- [ ] Approval date: [YYYY-MM-DD]
- [ ] Documents updated: [list of updated docs]
- [ ] Linear issues updated: [if applicable]
- [ ] Sprint status updated: [if applicable]

## Notes

[Any additional context, risks, or follow-up items]
```
