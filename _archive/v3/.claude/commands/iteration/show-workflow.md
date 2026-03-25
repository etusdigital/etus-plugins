---
description: Display product development workflow diagram and phase descriptions
allowed-tools: Read, Bash
model: sonnet
---

# Show Workflow

Display the product development workflow diagram and phase descriptions.

## Overview

This command shows the visual workflow diagram and descriptions for:
- **Double Diamond methodology** (Discover, Define, Develop, Deliver)
- **Phase outputs** and deliverables
- **Gate criteria** between phases
- **Parallel workstreams** in Deliver phase

## Display Workflow

### Check Available Workflows

!`if [ -f ../skills/orchestrator/knowledge/workflow.md ]; then
  echo "✓ Full workflow.md available"
elif [ -f ../skills/orchestrator/knowledge/greenfield-fullstack.md ]; then
  echo "✓ Greenfield workflow available"
else
  echo "⚠ No workflow files found"
fi`

### Main Workflow Diagram

```
ETUS Workflow (Evidence-based Through Unit-tested Solution)
═══════════════════════════════════════════════════════════

┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ DISCOVER │─▶│  DEFINE  │─▶│ DEVELOP  │─▶│ DELIVER  │─▶ RELEASE
│ (Diverge)│  │(Converge)│  │ (Diverge)│  │(Converge)│
└──────────┘  └──────────┘  └──────────┘  └──────────┘
     │             │              │              │
     ▼             ▼              ▼              ▼
  Vision        PRD/FRD        SRS/Arch     Data/UX/API
  BRD/JTBD      Epics       Architecture    Parallel →
  Journey     User Stories      NFRs        Frontend
     │             │              │              │
     ▼             ▼              ▼              ▼
 GATE: VIS    GATE: PLAN    GATE: TECH    GATE: DELIVER
```

### Phase Details

**DISCOVER** (Divergent - Explore Problem Space):
- Outputs: project-context.md, product-vision.md
- Purpose: Validate problem, understand users, map current state
- Gate: Vision validated with 5W2H, NSM defined, musts identified

**DEFINE** (Convergent - Solution Scope):
- Outputs: prd.md, user-stories.md, feature-spec-[name].md
- Purpose: Define features, functional requirements, acceptance criteria
- Gate: Traceability (BO-# → PRD-F-# → EP-# → US-# → FR-#)

**DEVELOP** (Divergent - Technical Design):
- Outputs: architecture-diagram.md, tech-spec.md, data-requirements.md
- Purpose: NFRs, system design, ADRs, deployment strategy
- Gate: C4 diagrams complete, NFRs quantified, deploy targets chosen

**DELIVER** (Convergent - Parallel Execution):
- Outputs: 3 parallel tracks converge on implementation
  - Data Chain: data-requirements.md → erd.md → database-spec.md → data-dictionary.md → data-flow-diagram.md → data-catalog.md
  - UX Chain: user-journey.md → ux-sitemap.md → wireframes.md → style-guide.md
  - Backend Chain: api-spec.md with endpoints
- Gate: All parallel tracks complete, implementation plan integrates data/UX/API

### Parallel Workstreams in DELIVER Phase

```
     DEVELOP GATE ✓
          ↓
     ┌────┴────┬────────┬────────┐
     │         │        │        │
   Data       UX     Backend
   Chain     Chain    Chain
     │         │        │
   7 docs    8 docs   1 doc
   (dict.*) (tok.*)  (API)
     │         │        │
     └────┬────┴────────┴────────┘
          ↓
     Frontend (fe)
     CONVERGENCE
          ↓
     DELIVER GATE ✓
```

## View Full Workflow

To see complete workflow documentation:

!`if [ -f ../skills/orchestrator/knowledge/workflow.md ]; then
  echo "Reading full workflow..."
  head -100 ../skills/orchestrator/knowledge/workflow.md
elif [ -f ../skills/orchestrator/knowledge/greenfield-fullstack.md ]; then
  echo "Reading greenfield workflow..."
  head -100 ../skills/orchestrator/knowledge/greenfield-fullstack.md
fi`

## Gate Checklists

For detailed gate criteria, run:
```
/list-gates
```

For automated gate validation:
```
/validate-gate [discover|define|develop|deliver|release]
```

## Next Steps

**Start new project**:
```
/start-project [product-name]
```

**Run specific phase**:
```
/discover
/define
/develop
/deliver
```

---

**Workflow reference ready!** Use this to understand phase outputs and dependencies.
