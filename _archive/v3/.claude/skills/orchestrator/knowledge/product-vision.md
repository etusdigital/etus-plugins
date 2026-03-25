---
doc_meta:
  id: vis
  display_name: Product Vision
  pillar: Define
  owner_role: Product Lead
  summary: Defines one-line vision, North Star Metric, and must-have outcomes.
  order: 1
  gate: vision
  requires: []
  optional: []
  feeds:
  - per
  - brd
uuid: <UUID>
version: 1.0.0
status: Draft
owners:
- <owner>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- ETUS
- AI-Templates
- Vision
ai_template_variables:
- product
- owner
- namespace
---

# Product Vision — [Tool Name]

**Author:** [Your Name] · **Date:** [YYYY-MM-DD] · **Context:** SOLO

> **Scope:** problem‑only (Discover). No journey mapping, no feature lists, no acceptance.
> **Feeds:** `prd.md` (product requirements).

---

## 1) Problem Statement (one line)

[Describe the core problem without embedding a solution.]

## 2) How Might We (problem framings)

- **Primary HMW:** [How might we …?]
- **Alt HMW 1:** […]
- **Alt HMW 2:** […]

## 3) 5W2H — Problem Map

- **WHO:** [Primary user] | [Secondary] | [Extreme]
- **WHAT:** [Core problem] | [Users can’t …] | [Success looks like …]
- **WHERE:** [Contexts/Platforms]
- **WHEN:** [Triggers] | [Frequency] | [Critical moments]
- **WHY:** [Root cause] | [Why now] | [Why previous solutions failed]
- **HOW (Workarounds):** [How they cope today] | [Pain 1–10]
- **HOW MUCH:** [Time lost] | [Money wasted] | [Opportunity cost]

## 4) Problem North Star

- **Metric:** […]
- **Baseline:** […] · **Target:** […] · **Timeline:** […]
- **Leading signals:** […, …]
- **Lagging signals:** […, …]

## 5) Anti‑Goals (explicit problem boundaries)

- […]
- […]
- […]

## 6) CSD — Certainties / Suppositions / Doubts

| CSD | Item | Evidence / Source | Impact if wrong | Next action | Experiment | Kill criteria       |
| --- | ---- | ----------------- | --------------- | ----------- | ---------- | ------------------- |
| C   | […]  | […]               | —               | Use premise | —          | —                   |
| S   | […]  | Weak/Moderate     | High            | Define test | […]        | If < X → stop/pivot |
| D   | […]  | —                 | Medium          | Discovery   | […]        | Revisit in N days   |

## 7) Evidence & Severity

- **Evidence:** [links, data, quotes]
- **Severity:** [X h/month], [R$], [Y% rate], [qualitative signal]

## 8) Critical Assumptions & Validation

| Assumption (S‑#) | Risk | Method | Success | Stop/Pivot |
| ---------------- | ---- | ------ | ------- | ---------- |
| S‑1              | High | […]    | […]     | […]        |
| S‑2              | Med  | […]    | […]     | […]        |

## 9) Stakeholders & Decision Rights (RACI‑lite)

| Role | Name     | Decision Rights               | Input Required |
| ---- | -------- | ----------------------------- | -------------- |
| D    | PM       | Go/No‑Go on Discover → Define | HMW/5W2H/CSD   |
| A    | Founder  | Scope boundaries              | Anti‑Goals     |
| C    | Eng Lead | Feasibility signals           | Evidence       |
| I    | Data     | Measurement feasibility       | North Star     |

## 10) References

- Benchmarks / prior research: […]
- Upstream notes: […]
- Downstream: `prd.md`, `user-journey.md`

## ✅ Vision Gate (Problem‑only)

- [ ] Clear, solution‑free problem statement
- [ ] HMW + 5W2H with numbers
- [ ] North Star with baseline/target/timeline
- [ ] Anti‑Goals set
- [ ] CSD prioritized; assumptions have method + kill criteria
- [ ] Evidence & severity captured
- [ ] Stakeholders aligned to move to **JTBD / Journey / BRD**
