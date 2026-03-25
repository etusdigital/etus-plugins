---
doc_meta:
  id: opp
  display_name: Opportunity Pack
  pillar: Discovery
  owner_role: Product Lead
  summary: Coverage-driven ideation package that captures the problem space before downstream documentation.
  order: 0
  gate: ideation
  requires: []
  feeds: [ctx, vis, fb, bug, spike]
---

# Opportunity Pack

**Last Updated:** [DATE]
**Owner:** [PRODUCT_LEAD_NAME]
**Status:** [DRAFT | APPROVED]
**Mode:** [product | feature | bug | spike]

---

## Progress & Checkpoints

| Step | Owner Command | Status | Notes |
|---|---|---|---|
| Source Ingestion | `/ideate ingest` | [not_started | in_progress | covered | blocked] | [notes] |
| Problem Framing | `/ideate problem` | [not_started | in_progress | covered | blocked] | [notes] |
| Actor Map | `/ideate actors` | [not_started | in_progress | covered | blocked] | [notes] |
| JTBD Extraction | `/ideate jobs` | [not_started | in_progress | covered | blocked] | [notes] |
| Journey Sweep | `/ideate journeys` | [not_started | in_progress | covered | blocked] | [notes] |
| Use Case Matrix | `/ideate cases` | [not_started | in_progress | covered | blocked] | [notes] |
| Edge Case Sweep | `/ideate edges` | [not_started | in_progress | covered | blocked] | [notes] |
| Assumptions & Unknowns | `/ideate assumptions` | [not_started | in_progress | covered | blocked] | [notes] |
| Solution Direction Brainstorm | `/ideate brainstorm` | [not_started | in_progress | covered | blocked] | [notes] |
| Synthesis & Handoff | `/ideate synth` | [not_started | in_progress | covered | blocked] | [notes] |

**Last Completed Step:** [step]
**Next Recommended Step:** [step or downstream command]

---

## Problem & Context

### Proposed Solution
[What the requester initially asked for]

### Underlying Problem
[Problem described independently from the proposed solution]

### Why Now?
[What changed, why this matters now, what happens if we do nothing]

### Current Alternative
[How users/stakeholders handle this today]

---

## Evidence Register

**Owned by:** `/ideate ingest`

| Type | Source | Summary | Confidence |
|---|---|---|---|
| confirmed_fact | [source] | [summary] | high |
| stakeholder_opinion | [source] | [summary] | medium |
| hypothesis | [source] | [summary] | low |
| prior_decision | [source] | [summary] | high |

### Contradictions Found
- [Contradiction 1]
- [Contradiction 2]

---

## Story Snapshots

### SNAP-1: [descriptive title of the story]
- **Who told it:** [PO / stakeholder / observed user]
- **Context:** [when it happened, what circumstance]
- **What happened:** [narrative in 3-5 sentences]
- **Key quote:** "[most revealing phrase, verbatim]"
- **What went wrong:** [concrete pain point]
- **Current workaround:** [what the person does today]
- **Detected opportunity:** [O-# if applicable]
- **IDs fed:** ACT-#, JTBD-#, JOUR-#, UC-#, EDGE-# extracted from this story

---

## Actor Map

**Owned by:** `/ideate actors`

### ACT-1: [Primary Actor]
- Role:
- Pain:
- Desired outcome:
- Channel/device/context:

### ACT-2: [Secondary Actor]
- Role:
- Pain:
- Desired outcome:
- Channel/device/context:

### Anti-Users / Negative Personas
- [Who should not be optimized for, or who can break the flow]

---

## JTBD Inventory

**Owned by:** `/ideate jobs`

### JTBD-1
- Type: functional | emotional | social
- Actor: ACT-#
- Trigger:
- Situation before:
- Anxiety:
- Progress desired:
- Current alternative:

### JTBD-2
- Type:
- Actor:
- Trigger:
- Situation before:
- Anxiety:
- Progress desired:
- Current alternative:

---

## Journey Inventory

**Owned by:** `/ideate journeys`

### JOUR-1: Happy Path
- Actor:
- Before:
- During:
- After:
- Success signal:

### JOUR-2: Alternate Path
- Actor:
- Before:
- During:
- After:
- Success signal:

### JOUR-3: Failure Path
- Actor:
- Failure trigger:
- Broken state:
- Recovery / fallback:

---

## Use Case Matrix

**Owned by:** `/ideate cases`

| ID | Actor | Trigger | Preconditions | Action | Expected Result |
|---|---|---|---|---|---|
| UC-1 | ACT-# | [trigger] | [preconditions] | [action] | [result] |
| UC-2 | ACT-# | [trigger] | [preconditions] | [action] | [result] |

---

## Edge Case Register

**Owned by:** `/ideate edges`

| ID | Scenario | Risk | Response |
|---|---|---|---|
| EDGE-1 | [invalid or exceptional state] | high | [expected handling] |
| EDGE-2 | [partial failure / abuse / fallback] | medium | [expected handling] |

---

## Constraints & Guardrails

**Owned by:** `/ideate problem` and refined during `/ideate edges`

### Constraints
- Technical:
- Business:
- Legal / compliance:
- Timeline / resource:

### Guardrails
- [Metric or condition that must not degrade]
- [Metric or condition that must not degrade]

---

## Non-Goals Registry

**Owned by:** `/ideate problem` and refined during `/ideate edges`

### NG-1: [What NOT to do]
- **Statement:** [what must NOT happen]
- **Reason:** [why excluded]
- **Scope:** permanent | deferred_to_v2 | conditional
- **Adjacent behavior:** [valid functionality that neighbors this non-goal]
- **Downstream docs that must respect:** [list]

### NG-2: [What NOT to do]
- **Statement:** [what must NOT happen]
- **Reason:** [why excluded]
- **Scope:** permanent | deferred_to_v2 | conditional
- **Adjacent behavior:** [valid functionality that neighbors this non-goal]
- **Downstream docs that must respect:** [list]

---

## Assumptions & Open Questions

**Owned by:** `/ideate assumptions`

### ASM-1
- Statement:
- Evidence:
- Status: assumed | open | resolved
- Validation needed:

### ASM-2
- Statement:
- Evidence:
- Status:
- Validation needed:

---

## Solution Directions

**Owned by:** `/ideate brainstorm`

### Themes (Phase A)

Themes grouped from story snapshots (SNAP-#):

| Theme | Related Snapshots | Summary |
|---|---|---|
| [Theme 1] | SNAP-#, SNAP-# | [one-line summary] |
| [Theme 2] | SNAP-#, SNAP-# | [one-line summary] |

### HMW Statements (Phase B)

Selected How Might We statements (max 3):

1. **HMW-1:** How might we [verb + outcome] without [constraint]?
   - Theme: [theme name]
   - Why selected: [rationale]
2. **HMW-2:** How might we [verb + outcome] without [constraint]?
   - Theme: [theme name]
   - Why selected: [rationale]
3. **HMW-3:** How might we [verb + outcome] without [constraint]?
   - Theme: [theme name]
   - Why selected: [rationale]

### Raw Ideas (Phase C)

Unfiltered ideas per HMW (Crazy 8s — no judgment, quantity over quality):

#### HMW-1 Ideas
1. [idea]
2. [idea]
3. [idea]

#### HMW-2 Ideas
1. [idea]
2. [idea]
3. [idea]

#### HMW-3 Ideas
1. [idea]
2. [idea]
3. [idea]

### Clusters (Phase D)

Ideas grouped by similarity:

| Cluster | Ideas Included | Core Concept |
|---|---|---|
| [Cluster A] | HMW-1 idea 2, HMW-2 idea 1 | [what unifies them] |
| [Cluster B] | HMW-1 idea 3, HMW-3 idea 2 | [what unifies them] |

### Selected Directions (Phase E)

2-3 directions selected for deepening:

#### Direction A: [name]
- **Why it might work:** [rationale]
- **Key tradeoff:** [what you give up]
- **Risks:** [what can go wrong]
- **4-risk evaluation:**
  - Value: [high/medium/low confidence]
  - Usability: [high/medium/low confidence]
  - Viability: [high/medium/low confidence]
  - Feasibility: [high/medium/low confidence]
- **Biggest failure reason:** [answer to "What's the biggest reason this could fail?"]

#### Direction B: [name]
- **Why it might work:** [rationale]
- **Key tradeoff:** [what you give up]
- **Risks:** [what can go wrong]
- **4-risk evaluation:**
  - Value: [high/medium/low confidence]
  - Usability: [high/medium/low confidence]
  - Viability: [high/medium/low confidence]
  - Feasibility: [high/medium/low confidence]
- **Biggest failure reason:** [answer to "What's the biggest reason this could fail?"]

### Assumptions per Direction (Phase F)

| ASM-# | Direction | What needs to be true | Risk Level | Validation Path | Connected to |
|---|---|---|---|---|---|
| ASM-# | Direction A | [assumption statement] | high / medium / low | [how to validate] | solution-discovery |
| ASM-# | Direction B | [assumption statement] | high / medium / low | [how to validate] | solution-discovery |

### Recommended Direction
[Recommendation with rationale, if ready]

---

## Prioritized Handoff

**Owned by:** `/ideate synth`

### For Product Mode
- What must feed project-context:
- What must feed product-vision:

### For Feature Mode
- What must feed feature-brief:

### For Bug Mode
- What must feed tech-spec-standalone:

### For Spike Mode
- What must feed spike:

---

## Blocking Questions Before Planning

**Owned by:** `/ideate synth`

- [Question 1]
- [Question 2]
