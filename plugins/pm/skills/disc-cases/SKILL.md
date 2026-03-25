---
name: disc-cases
description: >
  Use when turning journeys and requests into explicit use cases. Also triggers
  on 'use case', 'use-case matrix', 'actor trigger action result', or 'main
  scenarios'.
model: opus
version: 1.0.0
argument-hint: "[workflow or actor]"
compatibility: "Optional: external issue tracker adapter (for example, Linear)"
---

# Use Case Matrix

## Elicitation Entry Rule

BEFORE asking anything in this module:
1. Read elicitation-state.yaml (at docs/ets/projects/{project-slug}/state/ or knowledge/ template)
2. Find this module's entry in module_state
3. If status == "covered" → summarize what exists, ask if user wants to go deeper
4. If status == "in_progress" → continue from current_probe
5. If status == "not_started" → start with story probe (see .claude/skills/discovery/knowledge/story-probes.md)
6. After each question → update elicitation-state.yaml

## PURPOSE

Convert fuzzy workflows into explicit `UC-#` entries so that feature briefs,
PRDs, user stories, and implementation plans all trace back to observable
behavior.

## OUTPUT CONTRACT

Every `UC-#` must include:
- actor
- trigger
- preconditions
- action
- expected result
- visible success criterion
- downstream target if known (`FB-#`, `PRD-F-#`, `US-#`)

## MINIMUM SCENARIO SET

Try to cover:
- main trigger
- common repeat action
- blocked or invalid start state
- one partial-success or fallback scenario when applicable

## ANTI-PATTERNS

- Do not describe technical implementation here
- Do not merge two different triggers into one use case
- Do not leave the expected result vague
