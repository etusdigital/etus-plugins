---
description: Run explicit solution discovery after opportunity selection and before delivery requirements.
---

# Solution Discovery

Run explicit solution discovery after opportunity selection and before delivery requirements.

## Usage

```
/solution                   -> Start solution discovery from the selected OST opportunities
/solution [context]         -> Start from a specific opportunity, note, or file path
/feature solution [slug]    -> Run feature-scoped solution discovery in `features/{feature-slug}/`
```

## Workflow

1. Read the selected opportunities and priorities from:
   - `docs/ets/projects/{project-slug}/planning/ost.md`
   - `docs/ets/projects/{project-slug}/planning/prioritization.md`
2. Validate that discovery evidence exists:
   - `opportunity-pack.md`
   - `baseline.md`
   - `discovery-report.md`
   - `product-vision.md`
3. Explore 2-4 candidate solutions per selected opportunity
4. Score each solution against the four product risks:
   - value
   - usability
   - viability
   - feasibility
5. Define experiments, prototypes, or tests needed to reduce uncertainty
6. Select the recommended direction and document unresolved risks
7. Save:
   - `docs/ets/projects/{project-slug}/planning/solution-discovery.md`
   - `docs/ets/projects/{project-slug}/state/reports/solution-report.json`
   - optionally `docs/ets/projects/{project-slug}/planning/solution-experiments.yaml`
8. Present the Solution Readiness Gate and recommend the next command:
   - `/plan requirements`
   - `/design`

## Feature Mode Override

When this logic is invoked via `/feature solution`, use the feature-scoped contract instead:

- Read `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-status.md`
- Save `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md`
- Optionally save `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-experiments.yaml`
- Update `feature-status.md` with:
  - `discovery_state: solution_selected`
  - `current_step`
  - `last_completed_step`
  - `next_recommended_step`
  - `linked_docs.solution_discovery`
  - `traceability.solutions`

$ARGUMENTS
