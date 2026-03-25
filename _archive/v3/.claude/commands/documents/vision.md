---
description: Generate product vision document using 5W2H analysis
argument-hint: [problem-statement]
allowed-tools: Task, Write, Bash
model: sonnet
---

# Generate Product Vision

Creating product vision for: **$ARGUMENTS**

## Overview

Quick generation of product-vision.md without running full Discover phase.

**Output**: `docs/discovery/product-vision.md`

**Companion document**: `docs/discovery/project-context.md` (ctx)

## Setup

!`mkdir -p docs/discovery && echo "✓ Created docs/discovery/"`

## Template Reference

Reference template: @.claude/skills/feature-development-chain/knowledge/product-vision.md

## Generate Vision

I'll create a product vision document through interactive 5W2H analysis.

**Document will include:**

- One-line vision statement (T-shirt test)
- 5W2H systematic analysis:
  - **WHAT**: Problem statement without embedded solution
  - **WHO**: Target users and stakeholders
  - **WHERE**: Market context
  - **WHEN**: Timeline and milestones
  - **WHY**: Business value
  - **HOW**: Success measurement
  - **HOW MUCH**: Market size and potential
- North Star Metric (baseline → target → time window)
- 3-5 Critical Success Drivers
- Kill criteria
- Risks and assumptions

Let's start with the 5W2H questions to understand your product vision.

## Validation

After generation:

!`test -f docs/discovery/product-vision.md && echo "✓ product-vision.md created" || echo "✗ Generation failed"`

**Vision checklist**:
!`if [ -f docs/discovery/product-vision.md ]; then
  grep -qi "north star" docs/discovery/product-vision.md && echo "✓ North Star Metric defined"
  grep -qi "kill criteria" docs/discovery/product-vision.md && echo "✓ Kill criteria documented"
  grep -qi "WHAT\|WHO\|WHERE\|WHEN\|WHY\|HOW" docs/discovery/product-vision.md && echo "✓ 5W2H analysis present"
fi`

## Next Steps

**Continue with planning phase**:
```
/define
```

---

**Vision document generated!** Review and refine as needed.
