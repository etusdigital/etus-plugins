---
description: Create implementation documentation and release readiness artifacts.
---

# Implementation Phase

Create implementation documentation and release readiness artifacts.

## Context Loading

1. If $ARGUMENTS provided -> use as implementation constraints
2. Read docs/ets/projects/{project-slug}/state/reports/design.json for full context
3. If no handoff, scan docs/ets/projects/{project-slug}/ for all existing documents
4. If insufficient docs -> tell user to run /design first

## Execution

Spawn the **implementation-agent** with:

---

You are the Implementation Agent.

**Upstream:** all 17 documents from discovery + planning + design phases
**Output directory:** docs/ets/projects/{project-slug}/implementation/

1. Read ALL upstream documents (paths from design.json handoff)
2. Generate implementation-plan.md:
   - Decompose user stories into tasks (impl-#)
   - Map dependencies between tasks
   - Estimate effort (T-shirt sizing: XS, S, M, L, XL)
   - Plan sprints (1-2 week cycles)
   - Identify risks and mitigations
   - Each impl-# traces back to US-# or FS-#
3. Generate quality-checklist.md:
   - Test coverage requirements per feature
   - Performance benchmarks (from NFR-#)
   - Security review items
   - Accessibility criteria (WCAG AA)
   - Deployment readiness checks
4. Generate release-plan.md:
   - Rollout strategy
   - Rollback plan
   - Monitoring expectations

Write docs/ets/projects/{project-slug}/state/reports/implementation.json
Update ids.yml with impl sequences.

---

$ARGUMENTS

## After Implementation

Implementation planning is complete. The project is ready for development.

Summary of deliverables:
- 2 discovery docs (project-context, product-vision)
- 2-3 planning docs (prd, user-stories, feature-specs)
- 2 architecture docs (architecture-diagram, tech-spec)
- 6 data docs (data-requirements through data-catalog)
- 4 UX docs (user-journey through style-guide)
- 1 API doc (api-spec)
- 3 implementation docs (implementation-plan, quality-checklist, release-plan)

Suggest: review `implementation-plan.md`, validate readiness, and proceed with execution in the system of your choice.
