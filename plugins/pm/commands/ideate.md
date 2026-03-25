---
description: Run the ETUS ideation and elicitation layer before Discovery, Feature, Bug, or Spike documentation.
---

# Ideate

Run the ETUS ideation and elicitation layer before Discovery, Feature, Bug, or Spike documentation.

## Usage

```
/ideate                              -> Run the full ideate flow end-to-end
/ideate [context]                    -> Run the full flow from a pasted idea, link, issue, or file path
/ideate ingest [context]             -> Normalize sources, evidence, claims, and contradictions
/ideate problem [context]            -> Separate the proposed solution from the underlying problem
/ideate actors [context]             -> Define actors, anti-users, and operational stakeholders
/ideate jobs [context]               -> Extract JTBDs
/ideate journeys [context]           -> Map before/during/after and flow variants
/ideate cases [context]              -> Convert actors + journeys into use cases
/ideate edges [context]              -> Capture failure, abuse, fallback, and rollback cases
/ideate assumptions [context]        -> Capture assumptions, unknowns, and validation needs
/ideate brainstorm [context]         -> Explore solution directions after minimum coverage
/ideate synth [context]              -> Consolidate the opportunity pack and prepare handoff
/ideate status                       -> Show progress, thresholds, blockers, and next recommended step
```

## What It Does

1. If no subcommand is provided, run this default sequence:
   - ingest -> problem -> actors -> jobs -> journeys -> cases -> edges -> assumptions -> brainstorm -> synth

2. If a subcommand is provided, run only that semantic block and save checkpoints.

3. Collect mixed-source inputs:
   - user conversation
   - pasted text
   - Slack / Linear / Figma context if available
   - notes, docs, or transcripts

4. Run the coverage modules in order:
   - Source Ingestion
   - Problem Framing
   - Actor Map
   - JTBD Extraction
   - Journey Sweep
   - Use Case Matrix
   - Edge Case Sweep
   - Constraints & Guardrails
   - Hypotheses & Unknowns
   - Solution Direction Brainstorm
   - Synthesis & Prioritized Handoff

5. Save checkpoints to:
   - `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
   - `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml`

6. Present an Ideation Readiness summary and recommend the next command:
   - `/discover`
   - `/feature`
   - `/bugfix`
   - `/spike`

$ARGUMENTS
