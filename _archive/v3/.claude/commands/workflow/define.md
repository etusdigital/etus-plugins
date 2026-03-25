---
description: Run planning phase - create PRD, user stories, and feature specs
allowed-tools: Task, Read, Write, Bash, Grep
model: sonnet
---

# Planning Phase

Running Planning Phase (Convergent) - synthesizing insights into prioritized requirements and feature specifications.

## Phase Overview

The **Planning Phase** (Convergent) synthesizes discovery insights into clear Product Requirements Document, user stories, and on-demand feature specifications.

**Outputs**: prd.md, user-stories.md, feature-spec-[name].md (on demand)

## Pre-flight Checks

**Prerequisites - Discovery Phase Complete**:
!`test -f docs/discovery/product-vision.md && echo "✓ product-vision.md exists" || echo "✗ Missing product-vision.md (run /discover first)"`

**Output directories**:
!`mkdir -p docs/planning docs/planning/feature-specs && echo "✓ Created docs/planning/ and docs/planning/feature-specs/"`

**Existing planning documents**:
!`ls -1 docs/planning/ 2>/dev/null || echo "No planning documents yet"`

## Step 1: Invoke Feature Development Chain (Planning)

I'll invoke the **feature-development-chain** skill to generate planning documents using **How Might We (HMW)** statements.

### HMW Transformation Process

For each problem identified in product-vision.md:
```
Problem: [Pain point or unmet need]
↓
HMW: How might we [achieve desired outcome] for [user] so that [benefit]?
↓
Features: Potential solutions from HMW exploration
```

### Expected Outputs:

**1. Product Requirements (prd.md)**
- Product features (PRD-F-# IDs)
- Must/Should/Could prioritization (MoSCoW)
- Success criteria for each Must feature
- Out of scope (explicit exclusions)
- Dependencies and assumptions
- HMW statements linking problems to features
- Sharding support for large PRDs (prd-shard-*.md)

**2. User Stories (user-stories.md)**
- User stories (US-# IDs) linked to PRD-F-#
- Given/When/Then acceptance criteria (ONLY HERE)
- ≥3 scenarios per P0 story: Happy path, Alternative path, Error path
- Tasks per story (breakdown into implementable units)
- Definition of Ready (DoR)
- Definition of Done (DoD)
- Priority (P0, P1, P2)

**3. Feature Specifications (docs/planning/feature-specs/feature-spec-[name].md) — On Demand**
- Generated for complex features (>3 business rules OR state machine)
- Feature Specification IDs (FS-[name]-# IDs)
- Linked to parent PRD-F-# and US-#
- Detailed business rules
- State transitions/workflows
- Error handling and edge cases

**Invoking feature-development-chain for planning phase...**

## Step 2: Planning Gate Validation

After generation, validating Planning Gate criteria:

### Requirements Completeness
- [ ] PRD-F-# count: All features documented with MoSCoW priority
- [ ] US-# count: Each PRD-F-# has ≥1 user story
- [ ] P0 stories have ≥3 scenarios (Happy/Alt/Error) with Given/When/Then
- [ ] Each story has tasks (DoR checklist) and DoD defined
- [ ] Complex features (>3 rules or state machine) have feature-spec-*.md
- [ ] 0 TBD items in P0 scope
- [ ] All US-# trace back to PRD-F-#
- [ ] All FS-*-# link to parent US-# and PRD-F-#

### Traceability Check
```
vis (vision)
  → BO-# (business objectives in discovery/product-vision.md)
    → PRD-F-# (product features in prd.md)
      → US-# (user stories in user-stories.md)
        → FS-*-# (feature specs for complex features)
```

Validating chain:
!`grep -o "BO-[0-9]*" docs/discovery/product-vision.md 2>/dev/null | sort -u | wc -l | xargs echo "Business objectives found:"`

!`grep -o "PRD-F-[0-9]*" docs/planning/prd.md 2>/dev/null | sort -u | wc -l | xargs echo "Product features found:"`

!`grep -o "US-[0-9]*" docs/planning/user-stories.md 2>/dev/null | sort -u | wc -l | xargs echo "User stories found:"`

!`ls -1 docs/planning/feature-specs/feature-spec-*.md 2>/dev/null | wc -l | xargs echo "Feature specifications found:"`

### 5W2H Validation
```
WHAT: All P0 features detailed with acceptance criteria ✓
WHO: Responsible owners/personas for each story ✓
WHERE: Feature boundaries and integration points clear ✓
WHEN: Story priorities and sequencing ready ✓
WHY: Rationale for each P0 feature documented ✓
HOW: Implementation approach outlined in feature specs ✓
HOW MUCH: Scope validated, complexity identified ✓
```

## Gate Decision

**Status**: !`test -f docs/planning/prd.md && test -f docs/planning/user-stories.md && echo "✓ PASS" || echo "✗ FAIL - Missing documents"`

**Decision Options**:
- **GO**: Proceed to Develop phase (run `/develop`)
- **DESCOPE**: Remove Should/Could features, focus on P0/P1
- **ITERATE**: Refine requirements (update prd.md and user-stories.md)

## Next Steps

If **Planning Gate PASSED**:
```
Run: /develop
```

This will generate:
- architecture-diagram.md (C4 architecture)
- tech-spec.md (Technical specifications with NFRs)

---

**Planning phase complete!** Requirements are ready for technical architecture design.
