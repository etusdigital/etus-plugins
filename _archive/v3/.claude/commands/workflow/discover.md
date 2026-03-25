---
description: Run discovery phase - validate problem and build product vision
argument-hint: [product-idea-description]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Discover Phase

Starting discovery phase for: **$ARGUMENTS**

## Phase Overview

The **Discover Phase** (Divergent) explores the problem space broadly to understand user needs, market context, and business viability.

**Outputs**: project-context.md, product-vision.md (absorbs business case and BO-# IDs)

## Pre-flight Checks

!`test -d docs/discovery && echo "✓ docs/discovery/ exists" || mkdir -p docs/discovery && echo "✓ Created docs/discovery/"`

**Current documents**:
!`ls -1 docs/discovery/ 2>/dev/null || echo "No documents yet"`

**Project context**:
!`test -f docs/project-context.md && echo "✓ docs/project-context.md exists" || echo "⚠ docs/project-context.md not found"`

## Step 1: Generate Project Context (Constitution)

The **project-context.md** is the "constitution" — foundational product identity that doesn't change during the discovery phase.

This document captures:
- Product name and namespace
- Owner and team structure
- Tech stack and architectural decisions (framework, database, deployment)
- Repository structure and folder organization
- Target markets and regions
- Compliance/regulatory requirements
- Success environment

### Expected Output:

**1. Project Context (docs/project-context.md)**
- Product name and slug
- Namespace (for IDs, databases, APIs)
- Owner and core team members
- Tech stack (frontend, backend, database, hosting)
- Repository structure
- Target markets/regions
- Regulatory/compliance constraints
- Success environment (staging, production)

**Generating project-context.md...**

I'll now ask you foundational questions about the product:

1. **Product Identity**
   - What is the product name?
   - What namespace should we use for IDs and system identifiers? (e.g., "inv" for invoice tracker)
   - Who is the project owner?

2. **Technical Foundation**
   - What is the primary tech stack? (e.g., Node.js + React + PostgreSQL)
   - Where will this be deployed? (e.g., Vercel, AWS, self-hosted)
   - What's the repository structure? (monorepo, multi-repo, single repo?)

3. **Scope**
   - What markets/regions is this for? (e.g., US, EU, global)
   - Are there regulatory constraints? (e.g., GDPR, CCPA)
   - What's the success environment? (e.g., staging, production, open beta)

Once you provide these answers, I'll generate **docs/project-context.md**.

---

## Step 2: Generate Product Vision (with embedded business case)

The **product-vision.md** is the 5W2H analysis that drives product strategy.

Unlike traditional approaches, business objectives (BO-# IDs) and the business case are **embedded as sections** of the vision document — not in a separate BRD.

This document captures:
- One-line vision statement (t-shirt test)
- 5W2H analysis
- North Star Metric (baseline → target → time window)
- Critical Success Drivers (3-5 prioritized)
- Business Objectives (BO-# IDs) with targets
- Kill criteria
- Risks and assumptions

### Expected Output:

**2. Product Vision (docs/discovery/product-vision.md)**
- One-line vision statement
- 5W2H analysis of problem space
- North Star Metric with baseline, target, time window
- 3-5 Critical Success Drivers (ranked by importance)
- Business Objectives (BO-1, BO-2, etc.) with baseline → target → timeline
- Go/no-go kill criteria
- Risks and assumptions
- ROI justification (revenue vs cost)

**Expected 5W2H Questions**:
```
WHAT: What problem are we solving? What is the desired outcome?
WHO: Who experiences this problem? Who are the stakeholders?
WHERE: Where does the problem occur? Where will solution be used?
WHEN: When does the problem happen? When is the target launch?
WHY: Why is this important? Why hasn't it been solved?
HOW: How are users solving this today? How will we measure success?
HOW MUCH: How much impact? Market size? Revenue potential?
```

**Generating product-vision.md...**

I'll now ask you discovery questions to build the vision:

1. **Problem & Solution (WHAT)**
   - What problem are you solving?
   - What should success look like?

2. **Users & Stakeholders (WHO)**
   - Who are your target users?
   - Who else needs to be involved (internal stakeholders)?

3. **Market & Context (WHERE)**
   - Where will this be used? (geographic, platform, industry)
   - Who are your competitors?

4. **Timeline (WHEN)**
   - When do you want to launch?
   - What are the critical milestones?

5. **Business Value (WHY)**
   - Why is this important?
   - What's the business impact or revenue model?

6. **Measurement (HOW)**
   - How will you measure success?
   - What are your baseline metrics?

7. **Scale (HOW MUCH)**
   - What's your target market size?
   - Revenue potential in first year?

Once you provide these answers, I'll generate **docs/discovery/product-vision.md** with embedded business objectives (BO-# IDs), business case, and ROI analysis.

---

## Step 3: Discover Gate Validation

After generation, validating Discover Gate criteria:

### Vision Completeness
- [ ] One-line vision statement is clear and compelling
- [ ] 5W2H analysis complete with quantified answers
- [ ] North Star Metric has baseline, target, and time window
- [ ] 3-5 Critical Success Drivers identified and prioritized
- [ ] Kill criteria explicitly documented

### Business Case (Embedded in Vision)
- [ ] BO-# IDs defined with baseline → target → timeline
- [ ] ROI justification is credible (revenue vs cost)
- [ ] Stakeholder analysis complete
- [ ] Success metrics defined and measurable
- [ ] Risks identified with mitigation strategy

### Project Context
- [ ] Product name and namespace defined
- [ ] Tech stack documented
- [ ] Repository structure defined
- [ ] Owner and team structure clear

### 5W2H Validation
```
WHAT: Clear problem statement without embedded solution ✓
WHO: Target users and stakeholders identified ✓
WHERE: Market context and competitive landscape understood ✓
WHEN: Timeline and milestones defined ✓
WHY: Business value quantified ✓
HOW: Success measurement approach defined ✓
HOW MUCH: Market size, revenue potential estimated ✓
```

## Gate Decision

**Status**: !`test -f docs/project-context.md && test -f docs/discovery/product-vision.md && echo "✓ PASS" || echo "✗ FAIL - Missing documents"`

**Decision Options**:
- **GO**: Proceed to Define phase (run `/define`)
- **NO-GO**: Kill project (criteria not met, vision unviable)
- **ITERATE**: Refine discovery (rerun `/discover` with feedback, clarify assumptions)

## Next Steps

If **Discover Gate PASSED**:
```
Run: /define
```

This will generate:
- prd.md (Product Requirements Document)
- user-stories.md (User Stories with Given/When/Then acceptance criteria)
- feature-spec-[name].md (One spec file per major feature)

---

**Discover phase complete!** Review generated documents before proceeding to Define phase.
