---
description: Generate User Stories with Given/When/Then acceptance criteria
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate User Stories

Creating user stories for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/planning/prd.md && echo "✓ prd.md exists" || echo "⚠ Missing PRD (recommended to run /prd first)"`

## Setup

!`mkdir -p docs/planning && echo "✓ Created docs/planning/"`

## Template Reference

Reference template: @.claude/skills/feature-development-chain/knowledge/user-stories.md

## Interactive Story Creation

I'll help you create user stories from PRD features:

### Step 1: Review PRD Features

Read existing PRD features (PRD-F-#):

@docs/planning/prd.md

### Step 2: Story Generation

**For each PRD feature, ask the user:**

Let's create user stories for **PRD-F-#: [Feature Title]**

1. What are the specific user tasks within this feature?
2. For each task:
   - Who is the user? (persona/role)
   - What do they want to accomplish?
   - Why do they need this? (value/benefit)

[Create US-1, US-2, US-3, etc. mapped to PRD-F-#]

### Step 3: Acceptance Criteria (Given/When/Then)

**For each story, ask:**

**US-#**: As a [user], I want to [action] so that [benefit]

Let's define Given/When/Then acceptance criteria:

1. **GIVEN** - What's the starting state/context?
2. **WHEN** - What action does the user take?
3. **THEN** - What's the expected outcome/result?

[Multiple Given/When/Then scenarios per story]

**Additional criteria:**
- What edge cases should we handle?
- What validation rules apply?
- What error states exist?

[Record all acceptance criteria - SINGLE SOURCE OF TRUTH]

### Step 4: Story Details & Tasks

For each US-#, capture:
- Priority (P0/P1/P2)
- Size estimate (S/M/L/XL or points)
- Dependencies on other stories
- Technical notes/constraints
- **Implementation tasks** (sub-items for developers: code changes, database migrations, config updates, etc.)

### Step 5: Confirm Stories

"Here are the user stories I've created:

**US-1**: As a [user], I want to [action] so that [benefit]
- Feature: PRD-F-1
- Priority: P0
- Size: M
- Tasks:
  - [Implement X component]
  - [Update Y service]
  - [Add Z validation]
- AC:
  - GIVEN [context], WHEN [action], THEN [outcome]
  - GIVEN [context], WHEN [action], THEN [outcome]

**US-2**: As a [user], I want to [action] so that [benefit]
[etc.]

Are these stories complete and accurate?"

[Wait for confirmation]

## Generate Document

Generate `docs/planning/user-stories.md` using template structure.

**Document Structure:**
- Story Catalog (US-# → PRD-F-# mapping)
- For each story:
  - US-# ID
  - User story format: As a [who], I want to [what] so that [why]
  - Links to PRD-F-#
  - Priority (P0/P1/P2)
  - Size estimate
  - Dependencies
  - **Implementation tasks** (sub-items)
  - **Acceptance Criteria (Given/When/Then)** - SINGLE SOURCE
  - Technical notes
  - Definition of Done

**CRITICAL**: Given/When/Then acceptance criteria ONLY appear in user-stories.md (Single Source of Truth)

## Validation

After generation:

!`test -f docs/planning/user-stories.md && echo "✓ user-stories.md created" || echo "✗ Generation failed"`

**User stories checklist**:
!`if [ -f docs/planning/user-stories.md ]; then
  grep -o "US-[0-9]*" docs/planning/user-stories.md | sort -u | wc -l | xargs echo "User stories defined:"
  grep -o "PRD-F-[0-9]*" docs/planning/user-stories.md | sort -u | wc -l | xargs echo "PRD features mapped:"
  grep -ci "GIVEN\|WHEN\|THEN" docs/planning/user-stories.md | xargs echo "Acceptance criteria (G/W/T):"
  grep -ci "As a .* I want .* so that" docs/planning/user-stories.md | xargs echo "Story format compliance:"
fi`

## Next Steps

**For complex features with >3 business rules or state machines:**
```
/feature-spec [feature-name]
```

**Or validate Define gate:**
```
/validate-gate planning
```

---

**User stories generated!** Detailed acceptance criteria (Given/When/Then) documented as Single Source of Truth.
