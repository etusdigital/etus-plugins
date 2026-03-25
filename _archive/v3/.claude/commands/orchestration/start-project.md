---
description: Initialize complete product documentation through 4 phases (Discovery → Planning → Design → Implementation)
argument-hint: [product-name]
allowed-tools: Task, Write, Bash, Read
model: sonnet
---

# Start New Product Project

Initialize complete documentation workflow for: **$ARGUMENTS**

## Pre-flight Checks

Checking current state:

**Current directory**: !`pwd`

**Git repository**: !`git rev-parse --is-inside-work-tree 2>/dev/null && echo "✓ Git repo found" || echo "⚠ Not a git repo (run: git init)"`

**Existing docs directory**: !`test -d docs && echo "✓ docs/ exists" || echo "⚠ docs/ does not exist (will create)"`

## Step 1: Setup Directory Structure

Creating v3 documentation structure:

!`mkdir -p docs/discovery docs/planning docs/planning/feature-specs docs/design docs/design/architecture docs/design/data docs/design/ux docs/design/api docs/implementation && echo "✓ Directory structure created"`

**Directory breakdown**:
- `docs/discovery/` - Discovery phase documents (project-context.md, product-vision.md)
- `docs/planning/` - Planning phase documents (prd.md, user-stories.md)
- `docs/planning/feature-specs/` - Feature specifications (feature-spec-[name].md)
- `docs/design/` - Design phase (overall architecture, NFRs)
- `docs/design/architecture/` - Architecture (architecture-diagram.md, tech-spec.md)
- `docs/design/data/` - Data design (7 documents: requirements → erd → database-spec → data-dictionary → flow → catalog)
- `docs/design/ux/` - UX design (4 documents: journey → sitemap → wireframes → style-guide)
- `docs/design/api/` - Backend API (api-spec.md)
- `docs/implementation/` - Implementation phase (implementation-plan.md, sprint-status.yaml, quality-checklist.md)

## Step 2: Initialize IDs Registry

Creating `docs/ids.yml` with project metadata:

```yaml
namespace: $ARGUMENTS
product: $ARGUMENTS
version: 1.0.0
created: !`date +%Y-%m-%d`
author: solo-developer
methodology: Double Diamond + 5W2H + JTBD
template_version: 3.0.0
```

## Step 3: Discovery Phase

Generate foundational project understanding:

**Phase Goal**: Validate problem space, establish vision, create discovery gate

**Documents generated**:
- `docs/discovery/project-context.md` - Problem space, market opportunity, business objectives
- `docs/discovery/product-vision.md` - Vision statement, target user, value proposition

**Activities**:
1. Answer 5W2H questions systematically
2. Define 3-5 Business Objectives (BO-1, BO-2, etc.)
3. Create vision statement
4. Validate with stakeholders

**Discovery Gate Review** (User Decision Required):
- Is the problem clearly defined? YES/NO
- Is the vision compelling and achievable? YES/NO
- Are business objectives measurable? YES/NO
- **Gate Decision**: GO → Planning Phase | NO-GO → Stop | ITERATE → Refine discovery

## Step 4: Planning Phase

Transform vision into actionable requirements:

**Phase Goal**: Define features, stories, and specifications for implementation

**Documents generated**:
- `docs/planning/prd.md` - Product requirements (features with Must/Should/Could priority)
  - Each feature tagged as PRD-F-# linking to BO-#
- `docs/planning/user-stories.md` - User stories with Given/When/Then acceptance criteria
  - Each story tagged as US-# linking to PRD-F-#
- `docs/planning/feature-specs/feature-spec-[name].md` - Detailed specs for each PRD-F-#
  - Each requirement tagged as FS-[name]-# linking to US-#

**Activities**:
1. Brainstorm features using HMW (How Might We) statements
2. Prioritize with MoSCoW (Must/Should/Could/Won't)
3. Write user stories with clear acceptance criteria
4. Decompose into feature specs if needed
5. Build traceability: BO-# → PRD-F-# → US-# → FS-[name]-#

**Planning Gate Review** (User Decision Required):
- Are all features clearly defined? YES/NO
- Is traceability complete (BO → PRD-F → US)? YES/NO
- Are user stories testable with Given/When/Then? YES/NO
- **Gate Decision**: GO → Design Phase | DESCOPE → Reduce features | ITERATE → Clarify requirements

## Step 5: Design Phase (Parallel Workstreams)

Design all aspects of the solution:

**Phase Goal**: Create technical, data, and UX designs; validate implementation readiness

**Workstream 1: Architecture & Technical Specification**
- `docs/design/architecture/architecture-diagram.md` - C4 diagrams, system components, integrations
- `docs/design/architecture/tech-spec.md` - Technology stack, NFR-# with quantified targets, design decisions (ADR-#)

**Workstream 2: Data Design** (Sequential pipeline)
1. `docs/design/data/data-requirements.md` - Data entities, relationships, flows
2. `docs/design/data/erd.md` - Entity relationship diagram
3. `docs/design/data/database-spec.md` - DDL statements, table schemas, indexes (Single Source)
4. `docs/design/data/data-dictionary.md` - Field definitions (dict.* IDs) and event catalog (ev.* IDs)
5. `docs/design/data/data-flow-diagram.md` - Data processing pipeline, transformations
6. `docs/design/data/data-catalog.md` - Data governance, classifications, retention

**Workstream 3: UX Design** (Sequential pipeline)
1. `docs/design/ux/user-journey.md` - User flows, emotional touchpoints, pain points
2. `docs/design/ux/ux-sitemap.md` - Route structure, views, navigation hierarchy
3. `docs/design/ux/wireframes.md` - Layout specifications, component placement
4. `docs/design/ux/style-guide.md` - Design tokens (tok.* IDs), typography, spacing, colors

**Workstream 4: Backend API**
- `docs/design/api/api-spec.md` - OpenAPI specification, endpoints (be-ep-#), request/response schemas

**Implementation Readiness Gate Review** (User Decision Required):
- Are all workstreams complete and consistent? YES/NO
- Do NFR-# targets align with tech-spec choices? YES/NO
- Is API design aligned with frontend needs? YES/NO
- Are data flows implementable? YES/NO
- **Gate Decision**: GO → Implementation Phase | REDESIGN → Fix architecture conflicts | ITERATE → Clarify specs | BLOCK → Wait for completion

## Step 6: Implementation Phase

Prepare for active development:

**Phase Goal**: Create implementation plans, tracking, and quality standards

**Documents generated**:
- `docs/implementation/implementation-plan.md` - Sprint breakdown, phases, dependencies, resource plan
- `docs/implementation/sprint-status.yaml` - Sprint structure, story mappings, velocity targets
- `docs/implementation/quality-checklist.md` - Definition of Done, acceptance criteria tracking, testing plan

**Activities**:
1. Break US-# into implementation tasks
2. Estimate sprint capacity
3. Define testing strategy
4. Create quality gates
5. Begin implementation with full traceability to vision

## Step 7: Post-Generation Validation

All documentation validated for quality:

**Traceability Chains** (Validated Automatically):
- Discovery → Planning: project-context → BO-# → PRD-F-# → US-# → FS-[name]-# ✓
- Design: US-# → NFR-# (from tech-spec), dict.* (from data-dictionary), ev.* (from data-dictionary), tok.* (from style-guide)
- Implementation: US-# → tasks → sprints → quality gates

**Single Source of Truth** (Enforced Automatically):
- Given/When/Then acceptance criteria: ONLY in user-stories.md ✓
- NFR-# with quantified targets: ONLY in tech-spec.md ✓
- Design tokens (tok.*): ONLY in style-guide.md ✓
- Field definitions (dict.*): ONLY in data-dictionary.md ✓
- Event definitions (ev.*): ONLY in data-dictionary.md ✓
- DDL statements: ONLY in database-spec.md ✓

**Gate Status**:
- Discovery Gate: PASSED ✓
- Planning Gate: PASSED ✓
- Implementation Readiness Gate: PASSED ✓

## Step 8: Generate Project README

Creating `docs/README.md` with project overview:

```markdown
# $ARGUMENTS - Product Documentation

Complete product documentation generated using Solo Templates v3 methodology.

## Documentation Inventory (21 Core Documents)

### Discovery Phase (docs/discovery/)
- project-context.md - Problem space, market opportunity, business objectives
- product-vision.md - Vision statement, target user, value proposition

### Planning Phase (docs/planning/)
- prd.md - Product requirements with PRD-F-# linking to BO-#
- user-stories.md - User stories (US-#) with Given/When/Then acceptance criteria
- feature-specs/ - Detailed specifications for each feature (feature-spec-[name].md)

### Design Phase (docs/design/)

**Architecture & Technical** (docs/design/architecture/)
- architecture-diagram.md - System components, integrations (C4 diagrams)
- tech-spec.md - Technology stack, NFR-# targets, design decisions (ADR-#)

**Data Design** (docs/design/data/)
- data-requirements.md - Entities, relationships, flow requirements
- erd.md - Entity relationship diagram
- database-spec.md - DDL (Single Source of Truth)
- data-dictionary.md - Fields (dict.*) and events (ev.*)
- data-flow-diagram.md - Processing pipeline and transformations
- data-catalog.md - Governance and retention

**UX Design** (docs/design/ux/)
- user-journey.md - User flows and emotional touchpoints
- ux-sitemap.md - Route structure and navigation
- wireframes.md - Layout specifications
- style-guide.md - Design tokens (tok.* - Single Source)

**API Design** (docs/design/api/)
- api-spec.md - OpenAPI specification with endpoints (be-ep-#)

### Implementation Phase (docs/implementation/)
- implementation-plan.md - Sprint breakdown and resource plan
- sprint-status.yaml - Sprint structure and velocity targets
- quality-checklist.md - Definition of Done and testing plan

## Traceability

Complete ID chain maintained:
- Discovery: project-context → BO-# → PRD-F-# → US-# → FS-[name]-# → NFR-# (linked in tech-spec)

## Methodology

- **Double Diamond**: Discover → Define → Develop → Deliver (adapted to 4 phases)
- **5W2H**: What/Who/Where/When/Why/How/How Much systematic questioning
- **JTBD**: Jobs To Be Done framework for user context

## Next Steps

1. Review all generated documents in order
2. Validate traceability chains
3. Confirm all gates passed
4. Begin implementation following sprint-status.yaml
```

## Deliverables Summary

✅ **Complete directory structure** (8 directories)
✅ **21 core documentation documents** (v3 structure)
✅ **Validated traceability chains** (Discovery → Implementation)
✅ **Project README** with inventory
✅ **ids.yml registry**
✅ **All 3 gates passed** (Discovery, Planning, Implementation Readiness)

## Quality Standards Met

- ✓ All documents reference upstream via ID chains
- ✓ Single Source of Truth maintained (no duplicate definitions)
- ✓ 5W2H analysis applied in discovery
- ✓ HMW transformations in planning
- ✓ Complete traceability from vision to implementation
- ✓ All gate validations passed
- ✓ Design phase workstreams converge cleanly
- ✓ 4-phase structure clear and sequential

---

**Project initialization complete!** All 21 core documentation documents are ready for review and implementation.
