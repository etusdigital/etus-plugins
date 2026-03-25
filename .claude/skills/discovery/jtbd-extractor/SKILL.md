---
name: jtbd-extractor
description: >
  Use when extracting Jobs To Be Done from interviews, ideas, notes, or product
  requests. Also triggers on 'JTBD', 'job to be done', 'switch interview',
  'functional job', 'emotional job', or 'social job'.
model: opus
version: 1.0.0
argument-hint: "[idea or source excerpt]"
compatibility: "Optional: Slack MCP, external issue tracker adapter (for example, Linear)"
---

# JTBD Extractor

## Elicitation Entry Rule

BEFORE asking anything in any module:
1. Read `knowledge/elicitation-state.yaml`
2. Find the corresponding module
3. If status == "covered" → summarize what exists, ask if user wants to go deeper
4. If status == "in_progress" → continue from current_probe
5. If status == "not_started" → start with story probe (see knowledge/story-probes.md)
6. After each question → update elicitation-state.yaml
7. After each story → generate SNAP-# (see Story Snapshots in ideate SKILL.md)

## PURPOSE

Extract the real progress the actor is trying to make, not the feature they
asked for.

This skill exists because users often describe a desired solution while the
underlying job remains implicit. Its output should be written into the
Opportunity Pack as `JTBD-#` entries linked to `ACT-#`.

## OUTPUT CONTRACT

For each JTBD found, capture:
- type: `functional | emotional | social`
- actor: `ACT-#`
- trigger
- situation before
- anxiety or friction
- progress desired
- current alternative
- confidence: `high | medium | low`

## EXTRACTION PROMPTS

Use these prompts one at a time, story-first:
- "Before thinking about the solution: what was this person trying to do at that moment? What would make them say 'it was worth it'?"
- "What changed that made this matter now? Tell me about the specific moment it became urgent."
- "Walk me through what feels risky or frustrating in how they do it today. What's the worst part?"
- "What do they use today instead? How did they end up with that workaround?"
- "If we nailed this, what progress would they actually feel — not just functionally, but emotionally?"

Refer to `knowledge/story-probes.md` for additional story-based probes per module.
Refer to `knowledge/vague-response-escalation.md` for handling vague or generic answers.

## ANTI-PATTERNS

- Do not write JTBDs as features
- Do not confuse persona description with the job itself
- Do not stop at the functional job when emotional or social jobs are relevant
- Do not accept "save time" without specifying where and how
