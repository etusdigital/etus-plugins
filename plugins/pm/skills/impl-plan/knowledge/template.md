# Implementation Plan Template

## Responsaveis

- **Owner:** PM + Tech Lead
- **Contribuem:** Dev team, QA
- **Aprovacao:** PM + Tech Lead

Use this template as a guide to structure implementation-plan.md.

## 1. Implementation Strategy

```markdown
# Implementation Plan

## Implementation Strategy

### Approach: Phased Release

**Rationale:** Incremental delivery reduces risk, allows early feedback, validates assumptions progressively.

### Timeline
- **Total Duration:** 12 weeks
- **Sprint Length:** 2 weeks
- **Number of Sprints:** 6
- **Release Milestones:** MVP (Sprint 2), Beta (Sprint 4), GA (Sprint 6)

### Team Composition
- Backend: 2 engineers
- Frontend: 1 engineer
- QA: 1 engineer
- PM: 0.5 (shared)

**Total Capacity:** ~60 story points/sprint
```

## 2. Task Breakdown

```markdown
## Task Breakdown

### Task Naming Convention
- `impl-#`: Unique task ID
- Linked to `US-#` (user story) or `PRD-F-#` (feature)
- Estimated in story points: 1, 2, 3, 5, 8, 13

| impl-# | Title | US-# Link | Sprint | Est. | Dependencies | Status |
|--------|-------|----------|--------|-----|--------------|--------|
| impl-1 | Setup database schema | US-1, US-2 | Sprint 1 | 3 | — | — |
| impl-2 | Create User model & API | US-1 | Sprint 1 | 5 | impl-1 | — |
| impl-3 | Implement auth middleware | US-5 | Sprint 1 | 3 | impl-2 | — |
| impl-4 | Build user signup form | US-1 | Sprint 2 | 5 | impl-2, impl-3 | — |
| impl-5 | Create dashboard API | US-3 | Sprint 2 | 8 | impl-2 | — |
| impl-6 | Build dashboard UI | US-3 | Sprint 2 | 5 | impl-5 | — |

**Total:** 29 story points (Sprint 1 = 11, Sprint 2 = 18)
```

## 3. Sprint Plan

```markdown
## Sprint Plan

### Sprint 1 (Week 1-2): Foundation

**Capacity:** 11 story points
**Goal:** Database, core API, authentication

| Task | impl-# | Points | Owner | Status |
|------|--------|--------|-------|--------|
| Setup database schema | impl-1 | 3 | Backend | — |
| Create User model & API | impl-2 | 5 | Backend | — |
| Implement auth middleware | impl-3 | 3 | Backend | — |

**Sprint Dates:** March 17–28, 2026
**Blockers:** None
**Risks:** Database migration complexity

---

### Sprint 2 (Week 3-4): MVP Features

**Capacity:** 18 story points
**Goal:** User signup, dashboard

| Task | impl-# | Points | Owner | Status |
|------|--------|--------|-------|--------|
| Build user signup form | impl-4 | 5 | Frontend | — |
| Create dashboard API | impl-5 | 8 | Backend | — |
| Build dashboard UI | impl-6 | 5 | Frontend | — |

**Sprint Dates:** March 31–April 11, 2026
**Blockers:** None
**Risks:** API latency under load
```

## 4. Risk Register

```markdown
## Risk Register

| Risk ID | Description | Probability | Impact | Mitigation | Owner |
|---------|-------------|-------------|--------|-----------|-------|
| R1 | Database migration performance | Medium | High | Load test early, optimize indexes | Backend Lead |
| R2 | API authentication complexity | Low | High | Use proven library (JWT), code review | Backend Lead |
| R3 | Frontend responsive design issues | Medium | Medium | Test on multiple devices, use CSS grid | Frontend Lead |
| R4 | Team member unavailability | Low | High | Cross-train, document decisions | PM |

**Escalation:** If risk occurs, PM notified within 24h. Mitigation plan executed immediately.
```

## 5. Definition of Done

```markdown
## Definition of Done

### Per Implementation Task

- ✅ Code written (linted, formatted)
- ✅ Unit tests written (>80% coverage)
- ✅ Integration tests passing
- ✅ Code reviewed (2 approvals)
- ✅ Documentation updated (inline comments, README)
- ✅ Merged to main branch
- ✅ Deployed to staging environment
- ✅ QA tested against user story acceptance criteria
- ✅ No new bugs in regression testing
- ✅ Performance metrics meet NFR targets

### Per Sprint

- ✅ All tasks completed or carried forward (with reason)
- ✅ Sprint retrospective held
- ✅ Velocity tracked (for planning)
- ✅ Increment demonstrated to stakeholders
- ✅ Release notes updated
```

## 6. Dependency Graph

```
impl-1 (Schema)
  ↓
impl-2 (User API)
  ├─→ impl-3 (Auth)
  ├─→ impl-4 (Signup Form)
  └─→ impl-5 (Dashboard API)
      ↓
      impl-6 (Dashboard UI)
```

## Notes

- Tasks are broken down to 1-2 day items maximum
- Dependencies reduce parallelism but ensure quality
- Story points use Fibonacci (1, 2, 3, 5, 8, 13)
- Velocity = points completed per sprint (for forecasting)
- Sprint burn-down tracked daily (not shown here, tracked in execution-status.yaml when an execution adapter is enabled)

## O que fazer / O que nao fazer

**O que fazer:**
- Quebrar em tasks com impl-# IDs rastreaveies
- Estimar esforco com unidade clara (story points ou horas)
- Definir dependencias entre tasks
- Vincular cada impl-# a US-# upstream

**O que nao fazer:**
- Nao criar tasks maiores que 1 sprint
- Nao estimar sem input do time tecnico
- Nao ignorar tasks de infraestrutura e devops
- Nao planejar sem considerar tech debt e riscos

