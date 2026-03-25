---
name: dev-feedback
description: >
  Use after implementation to capture what the developer had to figure out on their own.
  Triggers on 'retro', 'dev feedback', 'what did you have to guess', 'implementation gaps'.
model: sonnet
version: 1.0.0
argument-hint: "[feature-slug]"
---

# Dev Feedback — Post-Implementation Learning Capture

## Purpose

Capture implementation gaps — decisions developers made without documentation guidance — and feed them back into the framework so future projects benefit. This is the learning loop that makes ETUS documentation progressively better.

## Dev Feedback Interview

### Step 1: Gather gaps

Ask: "What decisions did you make on your own during implementation that weren't covered in the documentation?"

For each answer, ask:
- "What did you end up deciding?"
- "Where did you look for the answer first?"
- "How confident are you in your decision?" (High / Medium / Low)

Continue asking "Anything else?" until the developer says no. Aim for at least 3 gaps before moving on. If the developer struggles to recall, prompt with categories:
- Error handling decisions
- Data format or schema choices
- API contract ambiguities
- UX behavior in edge cases
- Performance trade-offs
- Security decisions
- Third-party integration details

### Step 2: Classify by phase

For each gap, classify:

a. **Phase origin** — In which phase should this have been captured?
   - Ideation (opportunity-pack, coverage-matrix)
   - Discovery (project-context, product-vision, baseline)
   - Planning (PRD, user-stories, feature-spec)
   - Design (architecture, tech-spec, data, UX, API)
   - Implementation (impl-plan, quality-checklist)

b. **Missing dimension** — Which semantic dimension was missing? (from coverage-matrix dimensions: problem_clarity, trigger_and_preconditions, core_behavior, success_signal, anti_requirements, actors_and_permissions, failure_modes, data_mutations, degraded_behavior, side_effects, observability)

c. **Archetype match** — Would an archetype probe have caught this? If yes, which archetype? (e.g., workflow-approval, api-integration, import-export, or "none — new archetype needed")

### Step 3: Save as learning

Save to `docs/ets/projects/{project-slug}/learnings/{date}-{feature-slug}.md`:

```markdown
# Implementation Learnings: [Feature Name]
Date: [date]
Developer: [name if provided]

## Gaps Found

### Gap 1: [description]
- **Decision made:** [what the dev decided]
- **Confidence:** [High/Medium/Low]
- **Looked first in:** [where they searched]
- **Should have been in:** [phase]
- **Missing dimension:** [dimension]
- **Archetype match:** [archetype or "none"]

### Gap 2: [description]
...

## Recommendations
- [Specific probe to add to archetype pack]
- [Specific dimension to make mandatory for this project type]
- [Specific section to add to template]
```

### Step 4: Pattern detection

If running retro for 2+ features in the same project or across projects:
- Compare gaps across features
- If same gap appears 2+ times → recommend adding to archetype probe pack
- If same dimension is consistently missing → recommend making it mandatory
- Present recommendation for human approval before any framework changes

**Cross-project detection:**
1. Read all files in `docs/ets/projects/*/learnings/*.md`
2. Extract gap classifications
3. Group by (phase, dimension, archetype)
4. If count >= 2 for any group → flag as pattern
5. Present: "Pattern detected: [N] features had gaps in [dimension] during [phase]. Recommend adding probe: [specific probe text]"

## Output Validation

Before saving:
- [ ] At least 1 gap documented
- [ ] Each gap has all 3 classifications (phase, dimension, archetype)
- [ ] Recommendations section is non-empty
- [ ] File saved to correct learnings directory

## Closing Summary

```text
Dev feedback saved to docs/ets/projects/{project-slug}/learnings/{date}-{feature-slug}.md

Gaps found: [count]
Phase breakdown: Ideation: [N] | Planning: [N] | Design: [N] | Implementation: [N]
Patterns detected: [count] (across [N] features)
```

Next steps:
1. **Review recommendations** — Check if probes should be added to archetype packs
2. **Run another retro** — `/retro [other-feature]` to build pattern data
3. **Continue to project retrospective** — `/retro project` for full project-level retro
