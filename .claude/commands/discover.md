# Discovery Phase

Conduct product discovery on top of a prior ideation package. Discovery now
assumes the opening-diamond work has already captured actors, JTBDs, journeys,
use cases, edge cases, assumptions, and candidate directions.

## Context Loading

If $ARGUMENTS is provided, use it as the product description to jumpstart discovery.
Otherwise, begin by asking the user what product they want to document.

Check if docs/ets/projects/{project-slug}/discovery/ already has documents:
- If yes: ask user whether to refine existing or start fresh
- If no: proceed with new discovery

## Execution

Spawn the **discovery-agent** with these instructions:

---

You are the Discovery Agent. Your job is to generate two foundational documents
through interactive interviews with the user.

**Output directory:** docs/ets/projects/{project-slug}/discovery/

**Step 0: Ideate & Elicit (mandatory upstream)**
Read the ideate skill. Before Discovery, generate:
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml`

Only continue once the Ideation Readiness Gate passes.

**Step 1: Project Context (5W2H Interview derived from ideation)**
Read the project-context skill. Conduct a structured interview:
- What: What is this product? What problem does it solve?
- Who: Who are the users? Who are the stakeholders?
- Where: What platforms/markets?
- When: Timeline and milestones?
- Why: Why build this? What's the business case?
- How: How will it work at a high level?
- How Much: Budget, team size, constraints?

Use the opportunity-pack as the upstream source instead of re-eliciting the
same raw context from scratch.

Save to: `docs/ets/projects/{project-slug}/discovery/project-context.md`

**Step 2: Product Vision (brainstorm after coverage)**
Read the product-vision skill. Using the ideate package + 5W2H context:
1. Define problem statement and business objectives (BO-1, BO-2, ...)
2. Propose 3-4 BMAD brainstorm techniques to the user only after coverage is
   confirmed
3. User selects which to run
4. Execute selected technique -> generate insight artifact
5. Offer another technique or move on
6. Define target users, value proposition, success metrics

Save to: `docs/ets/projects/{project-slug}/discovery/product-vision.md`

**Step 3: Handoff Report (MANDATORY)**
Write `docs/ets/projects/{project-slug}/state/reports/discovery.json`:
```json
{
  "phase": "discovery",
  "status": "complete",
  "iteration": 1,
  "documents": [
    {"path": "docs/ets/projects/{project-slug}/discovery/project-context.md", "ids": []},
    {"path": "docs/ets/projects/{project-slug}/discovery/opportunity-pack.md", "ids": ["ACT-1", "JTBD-1", "..."]},
    {"path": "docs/ets/projects/{project-slug}/discovery/product-vision.md", "ids": ["BO-1", "..."]}
  ],
  "id_state": {"bo": N},
  "key_decisions": ["...top 3-5 decisions..."],
  "recommendations_for_next_phase": ["...what planning should focus on..."]
}
```

Update `ids.yml` sequences.bo with the last BO number used.

---

User context: $ARGUMENTS

## After Discovery

When the agent completes, present the Discovery Gate checklist:
- [ ] Ideation package exists and coverage threshold is met?
- [ ] 5W2H interview complete?
- [ ] Problem clearly defined and validated?
- [ ] Business opportunity quantified?
- [ ] At least 1 BO-# defined?
- [ ] Vision statement clear?

Ask user: **GO** (proceed to Planning), **ITERATE** (refine discovery), or **NO-GO** (stop)?
