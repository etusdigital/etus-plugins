---
doc_meta:
  id: per
  display_name: Jobs To Be Done
  pillar: Discover
  owner_role: Product Research
  summary: Captures JTBD job maps, desired outcomes, and adoption forces for personas.
  order: 2
  gate: vision
  requires:
  - vis
  optional: []
  feeds:
  - jour
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
- JTBD
- ETUS
- AI-Templates
ai_template_variables:
- product
- owner
- namespace
---

# Jobs To Be Done — [Job Family Name]

**Author:** [Your Name] · **Date:** [YYYY-MM-DD] · **Context:** SOLO

> Job‑centric profile. No UI details, no acceptance here.  
> **Feeds:** Journey (J# stages), BRD (business outcomes).

---

## 1) Job Map (steps of the job)

1. **Define** → 2. **Locate** → 3. **Prepare** → 4. **Execute** → 5. **Confirm** → 6. **Monitor** → 7. **Modify**  
   _(Adjust steps to your domain; typical maps have 6–12 steps.)_

## 2) Job Stories (primary)

- When [situation/trigger], I want to [motivation], so I can [outcome].
- When […], I want […], so I can […].
- When […], I want […], so I can […].

## 3) Desired Outcomes (ODI‑style)

| Outcome to Optimize            | Direction | Metric | Stage |
| ------------------------------ | --------- | ------ | ----- |
| [e.g., reduce time to X]       | ↓         | min    | J2    |
| [e.g., increase accuracy of Y] | ↑         | %      | J4    |
| [e.g., reduce rework on Z]     | ↓         | %      | J5    |

## 4) Forces of Adoption (Forces Model)

- **Push (current pain):** […]
- **Pull (solution attractions):** […]
- **Anxieties (risks/fears):** […]
- **Habits (lock‑in/friction):** […]

## 5) Constraints & Decision Criteria

- **Constraints:** [compliance, time, budget, device, connectivity]
- **Decision Criteria:** [e.g., TTV < X, cost < Y, risk Z, security policy N]

## 6) Context & Environments

- Devices, connectivity, toolchain, policies, languages/locales

## 7) Links & Trace (IDs)

- **Journey stages:** [J1, J2, …]
- **Stories (US):** [US‑1, US‑2, …]
- **Routes/Views:** [r:/…], [view.…]
- **Events (ev.\*):** [ev.…]

## ✅ JTBD Gate

- [ ] Job map consistent with Journey
- [ ] Outcomes measurable (direction + metric)
- [ ] Forces (push/pull/anxieties/habits) listed
- [ ] Decision criteria clear
- [ ] Trace to J#/US/route/view/event
