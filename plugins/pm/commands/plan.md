---
description: Split planning into opportunity focus and delivery requirements with solution discovery in between.
---

# Planning Phase

Split planning into opportunity focus and delivery requirements, with an explicit
solution-discovery step in between.

## Context Loading

1. If $ARGUMENTS provided -> treat it as one of:
   - `opportunities`
   - `requirements`
   - `status`
   - additional context
2. Read docs/ets/projects/{project-slug}/state/reports/discovery.json for upstream context
3. If no handoff, check if docs/ets/projects/{project-slug}/discovery/product-vision.md exists
4. If nothing found -> tell user to run /discover first

## Execution

Spawn the **planning-agent** with these instructions:

---

You are the Planning Agent.

**Upstream Context:**
- Discovery handoff: [inject from discovery.json]
- Documents: docs/ets/projects/{project-slug}/discovery/project-context.md, docs/ets/projects/{project-slug}/discovery/product-vision.md
- Business Objectives: [BO-1 through BO-N from handoff]
- Key decisions: [from handoff]

**Output directory:** docs/ets/projects/{project-slug}/planning/

**Mode A: `/plan opportunities`**
1. Read the `ost` skill
2. Generate `docs/ets/projects/{project-slug}/planning/ost.md`
3. Read the `prioritization` skill
4. Generate `docs/ets/projects/{project-slug}/planning/prioritization.md`
5. Write `docs/ets/projects/{project-slug}/state/reports/opportunities.json`
6. Present the Opportunity Focus Gate

**Mode B: `/plan requirements`**
1. Read the `prd` skill
2. Generate `docs/ets/projects/{project-slug}/planning/prd.md`
3. Read the `user-stories` skill
4. Generate `docs/ets/projects/{project-slug}/planning/user-stories.md`
5. Read the `feature-spec` skill as needed
6. Generate `docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-[name].md`
7. Write `docs/ets/projects/{project-slug}/state/reports/planning.json`
8. Present the Requirements Gate

**Mode C: `/plan status`**
1. Inspect:
   - `ost.md`
   - `prioritization.md`
   - `solution-discovery.md`
   - `prd.md`
   - `user-stories.md`
2. Recommend the next command:
   - `/plan opportunities`
   - `/solution`
   - `/plan requirements`

**Default `/plan` behavior**
1. If `ost.md` or `prioritization.md` are missing -> run `opportunities`
2. If `solution-discovery.md` is missing -> recommend `/solution` and stop
3. If `solution-discovery.md` exists and is approved -> run `requirements`

---

User context: $ARGUMENTS

## After Planning

Present the gate checklist that matches the current submode:

**Opportunity Focus Gate**
- [ ] OST contains opportunities, not backlog items?
- [ ] Prioritization is explicit and evidence-backed?
- [ ] The selected `O-#` items are clear enough to enter solution discovery?

**Requirements Gate**
- [ ] All delivery requirements trace back to `SOL-#`?
- [ ] PRD/feature scope is explicit?
- [ ] All user stories have Given/When/Then?
- [ ] Complex features have feature specs?

Ask user for the next appropriate step:
- after `opportunities`: **GO** -> `/solution`, **ITERATE**
- after `requirements`: **GO** -> `/design`, **DESCOPE**, **ITERATE**
