---
name: journey-sweep
description: >
  Use when mapping user journeys before requirements or solution design. Also
  triggers on 'journey', 'happy path', 'failure path', 'alternate flow',
  'before during after', or 'anti-journey'.
model: opus
version: 1.0.0
argument-hint: "[actor or workflow]"
compatibility: "Optional: Figma MCP, Slack MCP"
---

# Journey Sweep

## Elicitation Entry Rule

BEFORE asking anything in this module:
1. Read elicitation-state.yaml (at docs/ets/projects/{project-slug}/state/ or knowledge/ template)
2. Find this module's entry in module_state
3. If status == "covered" → summarize what exists, ask if user wants to go deeper
4. If status == "in_progress" → continue from current_probe
5. If status == "not_started" → start with story probe (see .claude/skills/discovery/knowledge/story-probes.md)
6. After each question → update elicitation-state.yaml

## PURPOSE

Map the workflow around the problem so that downstream docs don't jump straight
to screens or APIs.

This skill writes journey coverage into the Opportunity Pack as `JOUR-#`
entries and should connect each journey to actors, JTBDs, and use cases.

## REQUIRED COVERAGE

For each important actor, try to cover:
- before / during / after
- new user / returning user / blocked user
- happy path
- alternate path
- failure path
- manual fallback or recovery path

## JOURNEY FIELDS

For each `JOUR-#`, capture:
- actor
- path type
- trigger
- steps
- moment of friction
- success signal
- fallback or recovery

## ANTI-PATTERNS

- Do not map only the ideal path
- Do not confuse a journey with a UI flow
- Do not skip the "before" state and trigger
- Do not skip what happens after failure or partial success
