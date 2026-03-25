---
description: Generate Implementation Plan — task decomposition with ordered steps and done criteria (gate for coding)
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Implementation Plan

Creating implementation-plan for: **$ARGUMENTS**

> **Purpose:** Decompose stories into ordered tasks with done criteria. This is the GATE before coding — no approved plan = no code.
> **Inspired by:** BMAD sprint planning + Superpowers ExecPlans.

## Prerequisites

!`test -f docs/planning/user-stories.md && echo "✓ user-stories.md exists" || echo "⚠ Missing stories (run /stories first)"`
!`test -f docs/design/tech-spec.md && echo "✓ tech-spec.md exists" || echo "⚠ Missing tech-spec (run /tech-spec first)"`

## Setup

!`mkdir -p docs/implementation && echo "✓ Created docs/implementation/"`

## Interactive Planning

### Step 1: Prioritize Stories for Implementation

Review user stories and PRD features:

@docs/planning/user-stories.md

Which stories are in scope for this implementation cycle?
Rank by dependency order (what must exist first).

### Step 2: Decompose Each Story into Tasks

For each US-# in scope:
1. What tasks are needed? (setup, implement, test, integrate)
2. What order? (dependency chain)
3. Done criteria for each task (specific, verifiable)
4. Estimated complexity (S/M/L)
5. Risks or blockers?

### Step 3: Define Quality Gates

For each task:
- What tests prove it works?
- What spec does it implement? (US-# / FS-[nome]-#)
- Any performance criteria? (NFR-#)

### Step 4: Order the Work

Create a dependency-aware sequence:
1. Infrastructure/setup tasks first
2. Core data layer
3. Business logic
4. API endpoints
5. Frontend
6. Integration tests
7. Polish and edge cases

## Generate Document

Generate `docs/implementation/implementation-plan.md`

**Structure:**
1. **Scope** — Which US-# and PRD-F-# are in this cycle
2. **Task List** — Ordered tasks with: ID, description, story ref, done criteria, size, dependencies
3. **Dependency Graph** — What blocks what (mermaid if complex)
4. **Risk Register** — Known risks with mitigations
5. **Quality Gates** — Per-task verification criteria
6. **Sequence** — Recommended implementation order

## Validation

!`test -f docs/implementation/implementation-plan.md && echo "✓ implementation-plan.md created" || echo "✗ Generation failed"`

!`if [ -f docs/implementation/implementation-plan.md ]; then
  grep -o "US-[0-9]*" docs/implementation/implementation-plan.md | sort -u | wc -l | xargs echo "Stories covered:"
  grep -ci "done criteria\|done:" docs/implementation/implementation-plan.md | xargs echo "Done criteria defined:"
fi`

## Next Steps

```
/validate implementation-readiness  # Gate review before coding
/sprint-status                       # Initialize tracking
```

---

**Implementation Plan generated!** Tasks decomposed and ordered. Ready for Implementation Readiness gate.
