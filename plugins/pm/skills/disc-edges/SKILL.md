---
name: disc-edges
description: >
  Use when surfacing exceptions, abuse cases, and failure states before design
  or implementation. Also triggers on 'edge cases', 'failure cases',
  'exceptions', 'abuse flow', 'what can go wrong', or 'pre-mortem'.
model: opus
version: 1.0.0
argument-hint: "[workflow or scenario]"
compatibility: "Optional: external issue tracker adapter (for example, Linear), Slack MCP"
---

# Edge Case Sweep

## Elicitation Entry Rule

BEFORE asking anything in this module:
1. Read elicitation-state.yaml (at docs/ets/projects/{project-slug}/state/ or knowledge/ template)
2. Find this module's entry in module_state
3. If status == "covered" → summarize what exists, ask if user wants to go deeper
4. If status == "in_progress" → continue from current_probe
5. If status == "not_started" → start with story probe (see .claude/skills/discovery/knowledge/story-probes.md)
6. After each question → update elicitation-state.yaml

## PURPOSE

Find the scenarios that usually get remembered too late: invalid states,
dependency failures, abuse paths, rollback needs, and partial success.

This skill populates `EDGE-#` entries in the Opportunity Pack and should be
used before user stories are finalized.

## SWEEP CATEGORIES

Check for:
- invalid input or invalid state
- dependency unavailable
- race condition / double action
- permission or role mismatch
- partial success
- abuse or misuse
- rollback / undo / manual fallback
- observability blind spot

## OUTPUT CONTRACT

For each `EDGE-#`, capture:
- scenario
- trigger
- risk level
- expected handling
- fallback or recovery
- downstream impact

## ANTI-PATTERNS

- Do not stop after technical failures; include human and operational failures
- Do not assume a happy-path fix covers the edge case
- Do not skip what the user sees when the system degrades
