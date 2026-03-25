---
description: Initialize or update sprint-status.yaml — living progress tracker per story/task
argument-hint: [action: init|update]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Sprint Status Tracker

Action: **$ARGUMENTS**

> **Purpose:** Living document that tracks progress per story/task. Updated every work session. If stale >2 sessions, system warns.

## Prerequisites

!`test -f docs/implementation/implementation-plan.md && echo "✓ implementation-plan.md exists" || echo "⚠ Missing plan (run /implementation-plan first)"`

## Initialize (if new)

If `sprint-status.yaml` doesn't exist, create it from implementation-plan.md:

Read @docs/implementation/implementation-plan.md and extract all tasks.

Generate `docs/sprint-status.yaml` with structure:

```yaml
sprint:
  id: 1
  goal: "[Sprint goal from implementation plan]"
  started: "YYYY-MM-DD"
  status: active  # active | completed | blocked

stories:
  - id: US-1
    title: "[Story title]"
    status: not-started  # not-started | in-progress | blocked | done
    tasks:
      - id: T-1
        description: "[Task description]"
        status: not-started
        done_criteria: "[What proves it's done]"
        blocked_by: null
        notes: ""
      - id: T-2
        description: "[Task description]"
        status: not-started
        done_criteria: "[What proves it's done]"
        blocked_by: "T-1"
        notes: ""

blockers: []

last_updated: "YYYY-MM-DD"
session_count: 0
```

## Update (if exists)

!`test -f docs/sprint-status.yaml && echo "✓ sprint-status.yaml exists — updating" || echo "⚠ No sprint-status.yaml — use 'init' action first"`

If updating:
1. Ask what was accomplished since last session
2. Update task statuses (not-started → in-progress → done)
3. Record any new blockers
4. Increment session_count
5. Update last_updated date

## Staleness Check

!`if [ -f docs/sprint-status.yaml ]; then
  last=$(grep "last_updated" docs/sprint-status.yaml | head -1 | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
  if [ -n "$last" ]; then
    echo "Last updated: $last"
  fi
fi`

## Validation

!`if [ -f docs/sprint-status.yaml ]; then
  grep -c "status: done" docs/sprint-status.yaml | xargs echo "Tasks done:"
  grep -c "status: in-progress" docs/sprint-status.yaml | xargs echo "Tasks in progress:"
  grep -c "status: blocked" docs/sprint-status.yaml | xargs echo "Tasks blocked:"
  grep -c "status: not-started" docs/sprint-status.yaml | xargs echo "Tasks not started:"
fi`

---

**Sprint status updated!** Progress tracked per story/task.
