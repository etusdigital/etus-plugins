# Retro — Post-Implementation Feedback

Capture what the developer had to figure out on their own during implementation, classify gaps by phase, and feed learnings back into the framework.

## Usage
```
/retro                     # Start retro for current project
/retro [feature-slug]      # Retro for specific feature
```

## What It Does

Interviews the developer about decisions they made without documentation guidance. Classifies each gap by the phase where it should have been captured. Saves learnings for future improvement of archetype probe packs.

## Workflow

1. **Gather gaps** — Ask what decisions the developer made on their own
2. **Classify** — Map each gap to the phase where it should have been caught
3. **Save** — Write learnings to `docs/ets/projects/{project-slug}/learnings/`
4. **Detect patterns** — If running retro across multiple features, surface recurring gaps

## Execution

Spawn `.claude/skills/retrospective/dev-feedback/SKILL.md`

$ARGUMENTS
