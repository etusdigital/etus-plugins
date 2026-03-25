---
description: Generate product requirements document with Must/Should/Could prioritization
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Product Requirements Document

Creating PRD with feature prioritization and HMW statements.

## Prerequisites

!`test -f docs/discovery/product-vision.md && echo "✓ product-vision.md exists" || echo "⚠ Missing vision (recommended to run /discover first)"`

!`test -f docs/project-context.md && echo "✓ project-context.md exists (optional)" || echo "ℹ No project context file (optional)"`

## Setup

!`mkdir -p docs/planning && echo "✓ Created docs/planning/"`

## Template Reference

Reference template: @.claude/skills/feature-development-chain/knowledge/prd.md

## Interactive PRD Creation

I'll help you create a Product Requirements Document with interactive HMW brainstorming:

**How Might We (HMW) Transformation**:
- For each problem → create HMW statement
- HMW → generate potential features
- Features prioritized as Must/Should/Could

**PRD Contents**:
- Product features (PRD-F-# IDs)
- Must/Should/Could prioritization (MoSCoW)
- Success criteria for each Must feature
- Out of scope (explicit exclusions)
- Dependencies and assumptions
- HMW statements linking problems to features

**Generating PRD...**

## Validation

After generation:

!`test -f docs/planning/prd.md && echo "✓ prd.md created" || echo "✗ Generation failed"`

**PRD checklist**:
!`if [ -f docs/planning/prd.md ]; then
  grep -o "PRD-F-[0-9]*" docs/planning/prd.md | sort -u | wc -l | xargs echo "Features defined:"
  grep -ci "MUST" docs/planning/prd.md | xargs echo "Must features:"
  grep -qi "How might we\|HMW" docs/planning/prd.md && echo "✓ HMW statements present"
  grep -o "BO-[0-9]*" docs/planning/prd.md | wc -l | xargs echo "Business objectives referenced:"
fi`

## Next Steps

**Continue with Define phase**:
```
/user-stories
/feature-spec [feature-name]
```

Or proceed to full workflow:
```
/define
```

---

**PRD generated!** Review feature prioritization and success criteria.
