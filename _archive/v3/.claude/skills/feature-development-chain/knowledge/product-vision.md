---
doc_meta:
  id: vis
  display_name: Product Vision
  pillar: Discover
  owner_role: Product Lead
  summary: Defines problem statement, North Star metric, critical assumptions, and problem boundaries using 5W2H systematic analysis.
  order: 1
  gate: discovery
  requires: []
  optional:
  - project-context
  feeds:
  - prd
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
- Vision
- Problem Discovery
ai_template_variables:
- product
- owner
- namespace
---

# Product Vision — [Tool Name]

**Author:** [Your Name] · **Date:** [YYYY-MM-DD] · **Context:** SOLO

> **Scope:** Problem-only (Discover phase). No feature lists, no journey mapping, no acceptance criteria.
> **Feeds:** `prd.md` (scope & features).

---

## 1) Problem Statement (one line)

[Describe the core problem without embedding a solution. Focus on customer pain, not on your idea to fix it.]

**Example:** "Freelancers waste 5 hours per week chasing late invoice payments."

---

## 2) How Might We (problem framings)

Transform problem statement into opportunity framings:

- **Primary HMW:** [How might we …?]
  - **Opportunity:** [What becomes possible if we solve this?]

- **Alt HMW 1:** [Alternative framing]
  - **Opportunity:** […]

- **Alt HMW 2:** [Third framing]
  - **Opportunity:** […]

**Guidance:** Each HMW reframes the problem differently, opening new solution spaces. Don't lock into one framing.

---

## 3) 5W2H — Problem Map

Systematic questioning that deeply understands the problem:

### WHO
- **Primary user:** [Type of person experiencing problem]
  - Demographics, role, context
  - How many? (if knowable)

- **Secondary users:** [Other groups affected]
  - Do they experience same problem or related one?

- **Extreme users:** [Users we might not have considered]
  - Power users? Rare edge cases? New market segment?

### WHAT
- **Core problem:** [What is fundamentally broken?]
  - Not "how to fix" but "what's wrong"

- **Users can't …:** [Specific capability they lack]
  - What are they trying to accomplish?
  - What stops them?

- **Success looks like …:** [What would solving this enable?]
  - Concrete outcome, not abstract benefit

### WHERE
- **Contexts/Platforms:** [Where does problem manifest?]
  - On web? Mobile? Desktop?
  - At work? At home? On the go?
  - Specific tools or workflows?

- **Geographic scope:** [Any regional specificity?]

### WHEN
- **Triggers:** [What causes problem to surface?]
  - Specific moments or events
  - Recurring patterns

- **Frequency:** [How often does this occur?]
  - Daily? Weekly? Quarterly?
  - Escalating or steady?

- **Critical moments:** [High-stakes times when problem is most acute?]

### WHY
- **Root cause:** [Why does this problem exist?]
  - Not surface symptom but underlying cause
  - What systemic issue enables the problem?

- **Why now:** [Why is this problem urgent now?]
  - Market shift? Technology change? New regulation?
  - Why didn't anyone solve this sooner?

- **Why previous solutions failed:** [What did competitors/predecessors miss?]
  - Technical limitation? Business model? UX?

### HOW (Workarounds)
- **Current workarounds:** [How do people cope today?]
  - What manual process replaces solution?
  - What tools do they stitch together?

- **Pain level:** [How bad are workarounds? 1-10]
  - 1 = minor inconvenience
  - 10 = extremely painful

- **Time cost:** [How much time is wasted?]
  - Per day/week/month?
  - Total across user base?

### HOW MUCH
- **Time wasted:** [Hours/days per user per period]
  - Freelancer example: 5 hours/week × 50K users = 250K hours/week

- **Money lost:** [Direct revenue impact or opportunity cost]
  - Lost productivity value?
  - Delayed cash flow?

- **Opportunity cost:** [What could users do with recovered time?]
  - Growth activities? Creative work? Time with family?

---

## 4) Problem North Star

Define what success looks like and how to measure it:

### Metric
[What single metric best measures if we've solved the problem?]

**Example:** "Average days-to-payment for freelancer invoices"

### Baseline & Target
- **Baseline:** [Current state of metric]
  - Example: "Freelancers average 37 days to get paid"

- **Target:** [Goal state]
  - Example: "Reduce to 14 days average"

- **Timeline:** [When should we achieve target?]
  - Example: "Within 12 months of launch"

### Leading Signals
[Metrics that predict success before lagging signals are visible]

- Example: "Automation adoption rate" (people enabling automatic follow-ups)
- Example: "Days to first payment" (early adopters getting paid faster)
- Track these for early validation of solution direction

### Lagging Signals
[Metrics that confirm success but appear later]

- Example: "NPS score" (overall satisfaction)
- Example: "Revenue per freelancer" (economic impact)
- Example: "Churn rate" (retention)

---

## 5) Anti-Goals (explicit problem boundaries)

Explicitly state what you are NOT solving:

- [What's explicitly out of scope for this problem?]
  - Example: "We are not solving invoice creation - that works fine"
  - Example: "We are not building an accounting system - just payment tracking"

- [What would be nice but not core to problem?]
  - Example: "We could integrate with 50 payment processors, but starting with PayPal/Stripe"

- [What past attempts failed at?]
  - Example: "Previous solution was too complex - we won't repeat that"

---

## 6) CSD — Certainties / Suppositions / Doubts

Risk assessment matrix: What do we know vs assume vs need to validate?

| CSD | Item | Evidence / Source | Confidence | Impact if wrong | Next action | Validation Method | Kill Criteria |
| --- | ---- | --------- | ---------- | --------------- | ----------- | ---------- | ------------------- |
| C | [Known fact backed by evidence] | [Source/link/data] | High | — | Use as premise | — | — |
| S | [Assumption: weak evidence] | [Source, if any] | Medium | [High/Medium/Low] | [Define test] | [Experiment design] | [Stop if X] |
| D | [Doubt: no evidence] | [Gap description] | Low | [High/Medium/Low] | [Discovery work] | [Research plan] | [Revisit in N days] |

**Examples:**

| CSD | Item | Evidence | Confidence | Impact | Next | Validation | Kill |
| --- | ---- | -------- | ---------- | ------ | ---- | ---------- | ---- |
| C | Freelancers experience payment delays | Customer interviews (12 people), industry report | High | — | Proceed | — | — |
| S | Freelancers will pay $X/month | Competitor pricing research | Medium | High | Validate willingness-to-pay | Survey 50 freelancers | If <30% say "yes" |
| D | Automated reminders reduce days-to-payment by >50% | No data yet | Low | High | MVp test | A/B test reminder strategy | If improvement <30% |

---

## 7) Evidence & Severity

Back up problem claim with data:

### Evidence
- **Customer interviews:** [# people, quote examples]
  - Example: "12 freelancers interviewed, 11/12 cited payment delays as top 3 pain point"

- **Data/metrics:** [Quantified signal]
  - Example: "40% of SaaS freelancers report payment delays >30 days (industry survey)"

- **Market research:** [Reports, benchmarks, competitor data]
  - Example: "Stripe report: SMBs lose $X to late payments annually"

- **Support tickets:** [Frequency, sentiment]
  - Example: "Payment tracking is #3 support request (25% of tickets)"

### Severity
- **Time impact:** [X hours/month/year lost per user]

- **Financial impact:** [$ lost or opportunity cost]

- **Emotional/qualitative:** [Stress, frustration, trust erosion]

- **Market impact:** [# of users affected, market size]

---

## 8) Critical Assumptions & Validation

For each assumption, define how to validate or disprove it:

| Assumption | Risk | Validation Method | Success Criteria | Stop/Pivot |
| ---------- | ---- | ------ | ------- | ---------- |
| S-1: Freelancers will actively use payment tracking tool | High | Early user testing (5-10 power users) | >70% adoption among beta users | If <40% use it regularly |
| S-2: Payment delays are caused by forgotten invoices (not cash flow) | Medium | Customer survey (20+ freelancers) | >60% cite "forgotten" as reason | If <40% cite forgetting |
| S-3: Automated reminders won't annoy customers | High | A/B test reminder frequency | >80% positive feedback on frequency | If >30% report annoyance |

---

## 9) Stakeholders & Decision Rights (RACI-lite)

Who needs to approve, input, and consult?

| Role | Name | Decision Authority | Input Required | Consulted |
| ---- | ---- | --------- | --------------- | ---------- |
| D (Decision) | [PM Name] | Go/No-Go on problem framing | 5W2H answers | — |
| A (Approve) | [Founder/CEO Name] | Scope boundaries (do we solve full problem?) | Anti-goals | [Eng Lead, Data] |
| C (Consult) | [Eng Lead] | Feasibility signals (is solution buildable?) | Evidence/severity | — |
| I (Inform) | [Data Lead] | Metric feasibility (can we track North Star?) | North Star definition | — |

---

## 10) References

### Upstream
- [Project context document, if any]
- [Market research or industry reports]
- [Customer interview notes]
- [Competitive analysis]

### Downstream
- `prd.md` - Product requirements (features that solve this problem)
- `user-stories.md` - User stories (acceptance criteria for features)
- `feature-spec-*.md` - Detailed specs (for complex features)

---

## ✅ Discovery Gate (Problem-only)

Validate that problem is well-understood before defining solution:

- [ ] Clear, solution-free problem statement
- [ ] 5W2H with specific answers (no vague dimensions)
- [ ] North Star metric with baseline/target/timeline
- [ ] Anti-goals set (explicit scope boundaries)
- [ ] CSD prioritized; suppositions/doubts have validation method + kill criteria
- [ ] Evidence cited (data, interviews, research - not speculation)
- [ ] Severity quantified (time/money/market impact)
- [ ] Stakeholders aligned and decision rights clear
- [ ] HMW statements show multiple opportunity angles
- [ ] Confidence level: Could you pitch this problem to investors?

---

**End of Product Vision**
