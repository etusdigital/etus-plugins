---
name: val-quick
description: >
  Use for a 60-second quality check across all documents. Triggers on 'quick check',
  'quality check', 'are the docs ready', 'sanity check', 'check rapido',
  'check rápido', or 'are we ready'.
model: sonnet
version: 1.0.0
---

# Quick Quality Check (60s)

## PURPOSE

Run a rapid 8-question diagnostic across all documents in `docs/ets/projects/{project-slug}/`. This is NOT a deep validation — it is a fast sanity check that flags obvious gaps before a full gate review. Think of it as a smoke test for documentation quality.

## PROCESS

1. **Scan** `docs/ets/projects/{project-slug}/` recursively — read all `.md` and `.yaml` files
2. **Answer 8 yes/no questions** based on document content (not assumptions)
3. **Flag failures** with the specific document and gap
4. **Report** in under 60 seconds

## THE 8 QUESTIONS

For each question, answer YES or NO. If NO, specify which document needs work and what is missing.

### 1. Visao: esta claro para quem e qual valor?
- **Check:** `product-vision.md` or `project-context.md` — Does it clearly state the target user and the value proposition?
- **Pass criteria:** At least one persona identified AND a clear problem/value statement present.
- **If NO:** Flag which document is missing or vague.

### 2. Baseline: temos numeros e fonte?
- **Check:** `baseline.md` or `project-context.md` — Are there quantified metrics with data sources?
- **Pass criteria:** At least 2 metrics with numeric values AND source attribution.
- **If NO:** Flag "Baseline metrics missing or not sourced."

### 3. Discovery: ha evidencia (nao so opiniao)?
- **Check:** `project-context.md`, `product-vision.md` — Are decisions backed by evidence (data, research, user quotes) rather than just opinions?
- **Pass criteria:** At least 1 data point, user quote, or research reference.
- **If NO:** Flag "Discovery relies on opinion without supporting evidence."

### 4. OST: oportunidades ligadas ao outcome e com evidencia?
- **Check:** `product-vision.md` (BO-# objectives), `ost.md` if it exists — Are opportunities tied to measurable business outcomes?
- **Pass criteria:** At least 1 BO-# with a measurable target.
- **If NO:** Flag "Business objectives lack measurable outcomes."

### 5. Priorizacao: por que X vem antes de Y esta escrito?
- **Check:** `prd.md` (MoSCoW), `user-stories.md` — Is the prioritization rationale documented?
- **Pass criteria:** Must Have vs. Should Have distinction present with rationale.
- **If NO:** Flag "Prioritization exists but rationale for ordering is missing."

### 6. PRD: da para implementar e testar lendo so ele?
- **Check:** `prd.md` — Can a developer understand what to build and how to test it from the PRD alone?
- **Pass criteria:** Features have acceptance criteria or link to user stories with Given/When/Then.
- **If NO:** Flag "PRD features lack testable acceptance criteria."

### 7. Backlog: toda historia tem aceite verificavel?
- **Check:** `user-stories.md` — Does every US-# have Given/When/Then acceptance criteria?
- **Pass criteria:** 100% of US-# entries have at least one Given/When/Then block.
- **If NO:** Flag "Stories missing acceptance criteria: US-X, US-Y."

### 8. Release: sabemos lancar, monitorar e reverter?
- **Check:** `implementation-plan.md`, `quality-checklist.md`, `release-plan.md` — Is there a launch plan with monitoring and rollback?
- **Pass criteria:** At least deployment strategy AND rollback procedure documented.
- **If NO:** Flag "Release plan incomplete — missing [deployment|monitoring|rollback]."

## OUTPUT FORMAT

```
================================================
  QUICK CHECK — Documentation Quality (60s)
================================================

  1. Visao (para quem / qual valor)     [PASS | FAIL]
  2. Baseline (numeros e fonte)          [PASS | FAIL | N/A]
  3. Discovery (evidencia)               [PASS | FAIL]
  4. OST (outcomes com evidencia)        [PASS | FAIL | N/A]
  5. Priorizacao (rationale)             [PASS | FAIL | N/A]
  6. PRD (implementavel e testavel)      [PASS | FAIL | N/A]
  7. Backlog (aceite verificavel)        [PASS | FAIL | N/A]
  8. Release (lancar, monitorar, reverter) [PASS | FAIL | N/A]

  Result: X/8 PASS | Y FAIL | Z N/A

  --- Failures ---
  [#]: [Document] — [What is missing]
  ...

  --- Recommendation ---
  [Next action to address highest-priority failure]
================================================
```

**N/A** means the document does not exist yet (expected if the project hasn't reached that phase). N/A is NOT a failure — it means that phase hasn't been started.

**FAIL** means the document exists but is missing critical content.

## NOTES

- This check reads documents only — it does NOT modify anything.
- It is designed to complete in under 60 seconds.
- For a deep validation, use `/validate` instead.
- This skill has no upstream dependencies — it can run at any time.
