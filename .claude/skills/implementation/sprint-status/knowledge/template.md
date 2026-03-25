# Execution Status Template

## Responsaveis

- **Owner:** PM + Tech Lead
- **Contribuem:** Dev team
- **Aprovacao:** PM

Use this template as a guide to structure execution-status.yaml when an execution adapter is enabled.

```yaml
project: "etus-pmdocs"
updated_at: "2026-03-20T15:30:00Z"
current_sprint: 1
total_sprints: 6

# Summary across all sprints
summary:
  total_capacity: 60
  total_completed: 8
  total_in_progress: 5
  total_blockers: 1
  velocity_average: 8
  health: "green" # green, yellow, red

# Individual sprint details
sprints:
  - sprint_number: 1
    status: "in-progress"
    theme: "Foundation: Database, Core API, Auth"

    capacity:
      estimated: 11
      completed: 8
      in_progress: 5
      blocked: 0
      remaining: 3
      velocity_percent: 73

    dates:
      start: "2026-03-17"
      end: "2026-03-28"
      days_elapsed: 4
      days_remaining: 7

    tasks:
      - impl_id: "impl-1"
        title: "Setup database schema"
        user_story: "US-1, US-2"
        status: "done"
        story_points: 3
        owner: "alice@example.com"
        progress: 100
        completed_date: "2026-03-19"
        blockers: []
        notes: "Schema finalized, indexes added per performance review"

      - impl_id: "impl-2"
        title: "Create User model & API"
        user_story: "US-1"
        status: "in-progress"
        story_points: 5
        owner: "bob@example.com"
        progress: 60
        completed_date: null
        blockers: []
        notes: "JWT integration complete, working on password hashing. Estimated done by 2026-03-22"

      - impl_id: "impl-3"
        title: "Implement auth middleware"
        user_story: "US-5"
        status: "todo"
        story_points: 3
        owner: "bob@example.com"
        progress: 0
        completed_date: null
        blockers: ["impl-2"] # Depends on impl-2
        notes: "Blocked by impl-2 completion. Will start 2026-03-22"

    blockers:
      - blocker_id: "B1"
        title: "Third-party API rate limiting"
        description: "Payment gateway API returns 429 on integration tests. Waiting for quota increase from vendor."
        severity: "high"
        blocking_tasks: ["impl-5"]
        reported_date: "2026-03-19"
        owner: "charlie@example.com"
        status: "open"
        mitigation: "Mocked API responses in local tests. Escalated to vendor, expect resolution by 2026-03-23"
        impact: "Delays dashboard API integration tests (impl-5)"

    summary:
      health: "green" # green, yellow, red
      burndown_status: "on-track"
      notes: "Sprint is on track. One blocker resolved by Friday. Velocity trending toward 11 points."

  - sprint_number: 2
    status: "planned"
    theme: "MVP Features: Signup, Dashboard"

    capacity:
      estimated: 18
      completed: 0
      in_progress: 0
      blocked: 0
      remaining: 18
      velocity_percent: 0

    dates:
      start: "2026-03-31"
      end: "2026-04-11"
      days_elapsed: 0
      days_remaining: 14

    tasks:
      - impl_id: "impl-4"
        title: "Build user signup form"
        user_story: "US-1"
        status: "todo"
        story_points: 5
        owner: "diana@example.com"
        progress: 0
        completed_date: null
        blockers: ["impl-2", "impl-3"]
        notes: "Blocked by API implementation (impl-2, impl-3). Ready to start after Sprint 1 completion."

      - impl_id: "impl-5"
        title: "Create dashboard API"
        user_story: "US-3"
        status: "todo"
        story_points: 8
        owner: "bob@example.com"
        progress: 0
        completed_date: null
        blockers: ["B1"]
        notes: "Currently blocked by third-party API quota (B1). If not resolved, will use mock data."

      - impl_id: "impl-6"
        title: "Build dashboard UI"
        user_story: "US-3"
        status: "todo"
        story_points: 5
        owner: "diana@example.com"
        progress: 0
        completed_date: null
        blockers: ["impl-5"]
        notes: "Ready to start after impl-5 API is complete."

    blockers: []

    summary:
      health: "green"
      burndown_status: "not-started"
      notes: "Sprint 2 is planned. Awaiting Sprint 1 completion to start tasks. B1 blocker resolution will determine if we use mock data or real API."

# Burndown Chart (ASCII, updated daily)
burndown_chart: |
  Sprint 1 Burndown

  Points
   12 |* (est)
   11 |
   10 |
    9 |
    8 |  * (day 4, completed 8pts)
    7 |
    6 |
    5 |
    4 |
    3 |
    2 |
    1 |
    0 |________________
      0 1 2 3 4 5 6 7 8 (days)

  Ideal line (red): Linear burndown from 11 to 0
  Actual (green): Points completed per day
  Status: On-track (slightly ahead of schedule)

# Health Metrics
health_metrics:
  velocity_trend: "8 pts/sprint (1 sprint completed)"
  forecast_accuracy: "85%" # Historical sprint vs estimated
  quality_issues: "0" # Critical bugs in last sprint
  test_coverage: "78%" # Code coverage %
  deployment_health: "green"

# Notes & Risks
notes: |
  - Sprint 1 is 73% complete with 4 days remaining
  - One blocker (B1) affects Sprint 2 planning
  - Velocity trending slightly above estimate
  - Team morale: High (all team members engaged)
  - No quality issues reported

risks:
  - risk_id: "R1"
    title: "Database migration in production"
    probability: "medium"
    impact: "high"
    mitigation: "Zero-downtime migration plan documented. Rollback tested."

  - risk_id: "R2"
    title: "API latency under load"
    probability: "low"
    impact: "high"
    mitigation: "Load testing scheduled for Sprint 3. Caching layer ready."
```

## Update Frequency

- **Daily:** Standup reports (end of day) → update progress, blockers
- **Weekly:** Review meeting (Friday) → update overall status, velocity
- **Sprint-end:** Retrospective → velocity finalized, notes added

## Burn-Down Chart (ASCII)

Generate daily using formula:
```
Remaining Points = Capacity - Completed Points

Ideal = Capacity - (Capacity / Sprint Days) * Days Elapsed
Actual = Capacity - Total Points Completed
```

## Health Status Rules

- **Green:** On-track velocity, no blockers, quality >90%
- **Yellow:** Velocity trending down, 1-2 blockers, quality 80-90%
- **Red:** Velocity <50%, multiple blockers, quality <80%

## O que fazer / O que nao fazer

**O que fazer:**
- Atualizar status diariamente (nao so na sprint review)
- Registrar blockers com owner e data de resolucao esperada
- Calcular velocity para calibrar sprints futuras
- Incluir burndown ou metricas de progresso

**O que nao fazer:**
- Nao usar status vagas ("em andamento" sem %)
- Nao esconder blockers — visibilidade e o objetivo
- Nao atualizar retrospectivamente (status deve refletir o momento)
- Nao confundir sprint status com implementation plan

