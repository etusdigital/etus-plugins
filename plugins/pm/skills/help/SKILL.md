---
name: help
description: >
  Use when the user needs guidance, is unsure how to proceed, or wants to see
  project status. Also triggers on 'help', 'where am I', 'what is next', 'what
  can I do', 'show me the commands', or 'how does this work'.
model: sonnet
version: 1.0.0
---

# ETUS Help Skill

## PURPOSE

This skill provides contextual guidance by detecting where the user is in the documentation workflow and recommending the most logical next step. It helps new users understand what ETUS PMDocs can do and helps returning users pick up where they left off.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard:

1. **One question per message** — If clarification is needed, ask one question at a time.
2. **3-4 suggestions for choices** — Present options with brief descriptions and a recommendation.
3. **Multiple handoff options** — Always end with actionable next steps.

## WORKFLOW

### Step 1: Detect Current State

Check the following sources in order to determine project status:

1. **Workflow State** — Read `docs/ets/projects/{project-slug}/state/workflow-state.yaml` if it exists. This contains the last completed phase and gate decision.
2. **Project Status** — Read `docs/ets/projects/{project-slug}/state/project-status.yaml` if it exists. This contains the active mode, execution adapter, and workflow version.
3. **Feature Status** — If Feature mode is active or a feature slug is provided, read `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-status.md` first. This is the canonical state hub for that feature.
4. **Document Scan** — Scan `docs/ets/projects/{project-slug}/` for existing artifacts to infer progress:
   - `discovery/` — opportunity-pack.md, project-context.md, product-vision.md
   - `planning/` — prd.md, user-stories.md, feature-specs/
   - `architecture/` — architecture-diagram.md, tech-spec.md
   - `data/` — 6 data design documents
   - `ux/` — 4 UX design documents
   - `implementation/` — api-spec.md, implementation-plan.md, quality-checklist.md, release-plan.md
   - `state/` — workflow state, feature index, and optional execution adapter state
   - `features/` — feature docs and status files
   - `bugs/` — bug tech specs
   - `spikes/` — spike research documents
   - `learnings/` — retrospective documents
5. **No State Found** — If nothing exists, this is a fresh workspace.

### Step 2: Build Status Report

Present a clear status overview:

```
=== ETUS PMDocs — Project Status ===

Mode: [Product | Feature | Bug | Spike | Not set]
Execution Adapter: [none | local | linear | Not set]
Phase: [Discovery | Planning | Design | Implementation | Not started]
Last Gate: [GO | ITERATE | NO-GO | None]

Documents Found:
  Discovery:      [X/3+] opportunity-pack.md, project-context.md, product-vision.md
  Planning:       [X/3+] prd.md, user-stories.md, feature-specs
  Architecture:   [X/2] architecture-diagram.md, tech-spec.md
  Data Design:    [X/6] data-requirements, erd, database-spec, data-dictionary, data-flow-diagram, data-catalog
  UX Design:      [X/4] user-journey, ux-sitemap, wireframes, style-guide
  Implementation: [X/4] api-spec, implementation-plan, quality-checklist, release-plan
  Features:       [X] feature folders / feature-status docs
  Bugs:           [X] bug specs
  Spikes:         [X] spike docs
  Learnings:      [X] retrospectives
```

### Step 3: Recommend Next Step

Based on the detected state, recommend the single most logical next action with the exact command to run:

| State | Recommendation |
|-------|---------------|
| No documents exist | "Start ideation with `/ideate` or initialize with `/start-project`" |
| Ideation missing | "Start ideation with `/ideate`" |
| Ideation partial | "Run `/ideate status` and continue with the next recommended ideate subcommand" |
| Feature state found | "Run `/feature status [slug]` or continue with the next feature subcommand from feature-status.md" |
| Discovery incomplete | "Continue discovery with `/discover`" |
| Discovery complete, no opportunity focus | "Start with `/plan opportunities`" |
| Opportunities complete, no solution discovery | "Run `/solution`" |
| Solution complete, no requirements | "Run `/plan requirements`" |
| Planning complete, no design | "Start design with `/design`" |
| Design complete, no implementation | "Start implementation planning with `/implement`" |
| Implementation complete | "Run a retrospective with `/retro` or validate with `/validate`" |
| Mid-phase (partial documents) | "Resume the current phase — here's what's missing: [list]" |

### Step 4: Show Available Modes

```
=== Available Modes ===

Product Mode (default) — Full 4-phase pipeline for new products
  Ideation + full 4-phase pipeline, 3 gates, 7 specialized agents + support reviewers
  Command: /start-project or /orchestrator

Feature Mode — Lightweight pipeline for adding features to existing products
  Feature-scoped folder + feature-status hub + public subcommands
  Command: /feature

Bug/Hotfix Mode — Single-document spec for bug fixes
  1 document (tech-spec-standalone)
  Command: /bugfix

Spike/Research Mode — Time-boxed exploration and research
  1 document (spike report)
  Command: /spike
```

### Step 5: Show Available Commands

```
=== Available Commands ===

Workflow Commands:
  /ideate          — Opening ideation layer (full flow)
  /ideate status   — Show checkpoints, blockers, and next recommended ideate step
  /ideate jobs     — Resume JTBD extraction
  /ideate journeys — Resume journey mapping
  /ideate synth    — Consolidate the opportunity pack and prepare handoff
  /start-project   — Initialize project structure and begin Discovery
  /orchestrator    — Run the full workflow end-to-end
  /discover        — Phase 1: Discovery interview + vision
  /plan opportunities — Build OST + prioritization
  /solution        — Run solution discovery
  /plan requirements — Define PRD + user stories + feature specs
  /design          — Phase 3: Architecture + data/UX/API design
  /implement       — Phase 4: Implementation plan + sprints + quality

Mode Commands:
  /feature        — Start Feature mode (lightweight pipeline)
  /feature status — Show canonical feature state and next step
  /feature ideate — Run feature-scoped ideation
  /feature solution — Run feature-scoped solution discovery
  /feature brief  — Generate or refine the feature brief
  /feature stories — Generate scoped user stories
  /feature delta  — Generate the design delta
  /feature impl   — Generate the implementation plan
  /bugfix         — Start Bug/Hotfix mode (single tech spec)
  /spike          — Start Spike/Research mode (exploration)

Validation Commands:
  /validate       — Run quality gate, SST check, or traceability check

Other:
  /help           — Show this status and guidance (you are here)
```

## OUTPUT FORMAT

The output is displayed directly in chat — no file is written. The skill presents:

1. Current project status (documents found, phase, mode)
2. Recommended next step with exact command
3. Available modes with brief descriptions
4. Available commands reference
5. Execution adapter awareness (`none`, `local`, or `linear`) when available

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| No docs/ets/ directory | Info | This is a fresh workspace | Recommend `/start-project` |
| Handoff files corrupted or malformed | Low | Ignore handoff, infer state from documents | Report inferred state |
| Mixed-mode artifacts (e.g., feature + product docs) | Low | Report both, ask user to clarify | Show all found artifacts |
