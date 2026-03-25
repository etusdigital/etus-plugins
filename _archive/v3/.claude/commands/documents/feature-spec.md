---
description: Generate Feature Spec for a complex feature — business rules, state machines, edge cases, integrations
argument-hint: [feature-name-kebab]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Feature Spec

Creating feature-spec for: **$ARGUMENTS**

> **Purpose:** Detailed spec for complex features (>3 business rules or state machine). Not needed for simple CRUD.
> **Rule:** Story = observable behavior (Given/When/Then). Feature Spec = domain logic (rules, states, edge cases).

## Prerequisites

!`test -f docs/planning/prd.md && echo "✓ prd.md exists" || echo "⚠ Missing PRD (run /prd first)"`
!`test -f docs/planning/user-stories.md && echo "✓ user-stories.md exists" || echo "⚠ Missing stories (run /stories first)"`

## Setup

!`mkdir -p docs/planning/feature-specs && echo "✓ Created docs/planning/feature-specs/"`

## Template Reference

Reference template: @.claude/skills/orchestrator/knowledge/feature-spec.md

## Interactive Feature Decomposition

### Step 1: Identify Complexity

Read PRD to find the feature:

@docs/planning/prd.md

**Complexity check for $ARGUMENTS:**
- How many business rules does this feature have? (>3 = needs spec)
- Does it have a state machine? (yes = needs spec)
- Does it integrate with external systems?
- What edge cases are non-obvious?

If the feature is simple CRUD, suggest using a user story instead.

### Step 2: Extract Business Rules

For each business rule, capture:

1. **Rule ID:** FS-$ARGUMENTS-# (e.g., FS-context-merge-1)
2. **Description:** What the rule enforces
3. **Enforcement:** Client-side / Server-side / Both
4. **Error handling:** What happens when violated
5. **Test case:** Input → Expected outcome

### Step 3: Map State Transitions

If the feature has states:

1. What states exist?
2. What triggers each transition?
3. What are invalid transitions?
4. What recovery paths exist?
5. Draw mermaid stateDiagram if >3 states

### Step 4: Define Edge Cases

For each edge case:
1. **Scenario:** Description
2. **Expected behavior:** What should happen
3. **Fallback:** If primary behavior fails

### Step 5: Integration Points

If the feature talks to other systems/services:
1. **Dependency:** What it depends on
2. **Contract:** Expected input/output
3. **Failure mode:** What happens when dependency is down
4. **Timeout/retry:** Strategy

## Generate Document

Generate `docs/planning/feature-specs/feature-spec-$ARGUMENTS.md`

**Structure:**
1. **Feature Context** — Link to PRD-F-# and related US-#
2. **Business Rules** — FS-[nome]-# with enforcement and error handling
3. **State Machine** — States, transitions, mermaid diagram
4. **Edge Cases** — Non-obvious scenarios with expected behavior
5. **Integration Points** — Dependencies, contracts, failure modes
6. **Error Handling Strategy** — Categorized errors with recovery
7. **Performance Constraints** — Relevant NFR-# references
8. **Traceability** — PRD-F-# → US-# → FS-[nome]-# chain

## Validation

!`test -f docs/planning/feature-specs/feature-spec-$ARGUMENTS.md && echo "✓ feature-spec created" || echo "✗ Generation failed"`

!`if [ -f docs/planning/feature-specs/feature-spec-$ARGUMENTS.md ]; then
  grep -o "FS-[a-z0-9\\-]*-[0-9]*" docs/planning/feature-specs/feature-spec-$ARGUMENTS.md | sort -u | wc -l | xargs echo "Business rules defined:"
  grep -o "PRD-F-[0-9]*" docs/planning/feature-specs/feature-spec-$ARGUMENTS.md | sort -u | wc -l | xargs echo "PRD features traced:"
  grep -o "US-[0-9]*" docs/planning/feature-specs/feature-spec-$ARGUMENTS.md | sort -u | wc -l | xargs echo "User stories traced:"
fi`

## Next Steps

```
/tech-spec          # Architecture and NFRs
/implementation-plan  # Task decomposition before coding
```

---

**Feature Spec generated!** Complex feature decomposed into business rules (FS-[nome]-#), state machine, edge cases, and integration points.
