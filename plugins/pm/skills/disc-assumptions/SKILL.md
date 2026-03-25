---
name: disc-assumptions
description: >
  Use when surfacing assumptions, unknowns, and unanswered questions before
  planning or implementation. Also triggers on 'assumptions', 'unknowns', 'open
  questions', 'what are we assuming', or 'dependency interview'.
model: opus
version: 1.0.0
argument-hint: "[idea or context]"
compatibility: "Optional: Slack MCP, external issue tracker adapter (for example, Linear)"
---

# Assumption Audit

## Elicitation Entry Rule

BEFORE asking anything in this module:
1. Read elicitation-state.yaml (at docs/ets/projects/{project-slug}/state/ or knowledge/ template)
2. Find this module's entry in module_state
3. If status == "covered" → summarize what exists, ask if user wants to go deeper
4. If status == "in_progress" → continue from current_probe
5. If status == "not_started" → start with story probe (see .claude/skills/discovery/knowledge/story-probes.md)
6. After each question → update elicitation-state.yaml

## PURPOSE

Separate what is known from what is merely believed.

This skill turns hidden uncertainty into explicit `ASM-#` records with status
and validation paths. It is the main protection against false confidence in the
ideation phase.

## Assumption Status Options

Each ASM-# must have one of these statuses:

- **resolved** — Confirmed answer exists. Evidence documented.
- **open** — Conscious gap. Has owner + deadline for resolution.
- **deferred** — Conscious decision to defer. Has justification + target phase/milestone.
- **assumed_default** — Accepted during fatigue management (R10). Marked with revisit_required: true. Cannot be used for mandatory dimensions.
- **unconscious_gap** — Discovered via "I never thought about this" response. Was deepened with 2-3 follow-up questions before proceeding.

## OUTPUT CONTRACT

For each `ASM-#`, capture:
- statement
- evidence available
- status: `resolved | open | deferred | assumed_default | unconscious_gap`
- risk if false
- validation needed
- owner / phase if known

## AUDIT QUESTIONS

Ask one at a time:
- "What are we assuming about user behavior?"
- "What are we assuming about technical feasibility?"
- "What are we assuming about data quality or integrations?"
- "What are we assuming about approvals, policies, or dependencies?"
- "If this assumption is false, what breaks first?"

## ANTI-PATTERNS

- Do not hide assumptions inside prose
- Do not mark something as resolved without evidence
- Do not leave a high-risk unknown without a validation path
