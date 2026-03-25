# Brainstorm Techniques Reference

This document describes 8 interactive brainstorming techniques available during product vision workshops.
Each technique unlocks different insights about your product idea.

## Table of Contents

- [Overview Table](#overview-table)
- [1. 5 Whys](#1-5-whys)
- [2. SCAMPER](#2-scamper)
- [3. Reverse Brainstorming](#3-reverse-brainstorming)
- [4. Six Thinking Hats](#4-six-thinking-hats)
- [5. Starbursting](#5-starbursting)
- [6. Future State Ideal](#6-future-state-ideal)
- [7. SWOT](#7-swot)
- [8. Mind Mapping](#8-mind-mapping)
- [Selection Pattern](#selection-pattern-during-vision-interview)
- [Tips for Running Techniques Effectively](#tips-for-running-techniques-effectively)
- [Next Steps in Vision Interview](#next-steps-in-vision-interview)

---

## Overview Table

| Technique | Duration | Best For | Output |
|-----------|----------|----------|--------|
| 5 Whys | 10 min | Root cause analysis | Problem tree |
| SCAMPER | 15 min | Feature ideation | 7 solution categories |
| Reverse Brainstorm | 15 min | Risk & mitigation | Inverted solutions |
| Six Thinking Hats | 20 min | Well-rounded analysis | Multi-perspective matrix |
| Starbursting | 15 min | Question generation | W questions matrix |
| Future State Ideal | 15 min | Aspirational design | Idealized spec + constraints |
| SWOT | 15 min | Strategic positioning | 4-quadrant matrix |
| Mind Mapping | 20 min | Visual exploration | Hierarchical concept map |

---

## 1. 5 Whys

### What It Is
Drill down into root causes by asking "Why?" 5 times in sequence. Moves from symptom to underlying cause.

### When to Use
- Exploring why a problem exists (not just what the problem is)
- Validating assumptions before building
- Understanding user pain deeply

### How to Run (5 steps)

1. **State the Problem:** "Freelancers spend 5 hours/week tracking invoice payments."
2. **Ask Why #1:** "Why do they spend so much time?" → "Because invoices are scattered across email, Stripe, PayPal, and spreadsheets."
3. **Ask Why #2:** "Why aren't these centralized?" → "Because they use different payment providers based on client preference."
4. **Ask Why #3:** "Why can't they just pick one provider?" → "Because different clients prefer different payment methods."
5. **Ask Why #4:** "Why do different clients prefer different methods?" → "Because of fees, speed, their banking preferences."
6. **Ask Why #5:** "Why haven't existing tools solved this?" → "Because API access to all providers is complex and providers change constantly."

**Synthesize:** The root cause is fragmented payment provider ecosystem + API integration complexity. Solution: aggregation layer + API abstraction.

### Expected Output Format

```
Problem: [Initial symptom]
  ↓ Why?
Cause 1: [First-level cause]
  ↓ Why?
Cause 2: [Second-level cause]
  ↓ Why?
Cause 3: [Third-level cause]
  ↓ Why?
Root Cause: [Fundamental issue]

Implications for Product:
- Feature 1: [Addresses which cause?]
- Feature 2: [Addresses which cause?]
```

### Duration
10 minutes

---

## 2. SCAMPER

### What It Is
Systematic technique applying 7 creative prompts to your product idea: Substitute, Combine, Adapt, Modify, Put to use, Eliminate, Reverse.

### When to Use
- Generating feature ideas
- Finding product variations
- Breaking conventional thinking

### How to Run (7 steps)

For each prompt, ask: "How might we [prompt] to create better value for [USER]?"

1. **Substitute:** What could we replace?
   - Example: Replace manual CSV upload → automatic API sync
   - Example: Replace email notifications → in-app notifications
   - User answer: [input]

2. **Combine:** What could we merge or integrate?
   - Example: Combine invoice tracking + expense tracking
   - Example: Combine time tracking + invoicing
   - User answer: [input]

3. **Adapt:** What could we borrow from other domains?
   - Example: Adapt Amazon's order tracking → invoice tracking
   - Example: Adapt Slack's notification system → payment reminders
   - User answer: [input]

4. **Modify:** What could we change (scale, shape, attributes)?
   - Example: Modify frequency: daily summary instead of per-transaction
   - Example: Modify scope: track retainer payments in addition to hourly
   - User answer: [input]

5. **Put to Use:** What new uses could this serve?
   - Example: Use for accountants managing multiple freelancer clients
   - Example: Use for agencies tracking sub-contractor payments
   - User answer: [input]

6. **Eliminate:** What could we remove or simplify?
   - Example: Eliminate approval workflows (auto-send on due date)
   - Example: Eliminate dashboard customization (show essentials only)
   - User answer: [input]

7. **Reverse:** What could we flip or rearrange?
   - Example: Instead of reminding freelancers, remind clients of overdue payments
   - Example: Instead of payment tracking, focus on dispute resolution
   - User answer: [input]

### Expected Output Format

```
SCAMPER Analysis for [PRODUCT]:

S (Substitute):
  - [Substitution 1]
  - [Substitution 2]

C (Combine):
  - [Combination 1]
  - [Combination 2]

A (Adapt):
  - [Adaptation 1]
  - [Adaptation 2]

M (Modify):
  - [Modification 1]
  - [Modification 2]

P (Put to Use):
  - [New use 1]
  - [New use 2]

E (Eliminate):
  - [Elimination 1]
  - [Elimination 2]

R (Reverse):
  - [Reversal 1]
  - [Reversal 2]

Top Insights:
- Insight 1 → Potential feature
- Insight 2 → Potential feature
```

### Duration
15 minutes

---

## 3. Reverse Brainstorming

### What It Is
Instead of "How can we solve this?" ask "How can we make this WORSE?" Then invert answers to find safeguards and solutions.

### When to Use
- Identifying risks and failure modes
- Finding non-obvious mitigations
- Stress-testing your product idea

### How to Run (4 steps)

1. **Flip the Goal:** Instead of "How do we help freelancers get paid faster?" ask "How could we ensure freelancers NEVER get paid?"

2. **Brainstorm Failure Modes:** What could go wrong?
   - Payment gateway API fails → invoices aren't synced
   - User authentication breaks → fraudster accesses account
   - Invoice data is corrupted → wrong amounts sent
   - User abandons platform → no ongoing revenue
   - Competitors undercut price → lose to free alternatives

   User answers: [input]

3. **Invert to Solutions:**
   - API failure → Implement redundant payment gateway connections + graceful fallback
   - Auth breach → Implement 2FA, OAuth, IP whitelisting, audit logs
   - Data corruption → Implement checksums, transaction logging, rollback capability
   - User abandonment → Implement onboarding, engagement metrics, win-back campaigns
   - Price undercut → Implement unique value (integrations, compliance, support)

4. **Prioritize Safeguards:** Which mitigations matter most for MVP?

### Expected Output Format

```
Reverse Brainstorm for [PRODUCT]:

How could we ensure [WORST_CASE_SCENARIO]?

Failure Modes:
1. [Failure mode] → Inversion: [Mitigation]
2. [Failure mode] → Inversion: [Mitigation]
3. [Failure mode] → Inversion: [Mitigation]

MVP Safeguards (Priority):
- [ ] Safeguard 1 (High priority)
- [ ] Safeguard 2 (Medium priority)
- [ ] Safeguard 3 (Low priority)

Risks Identified:
- Risk 1: [Scenario] → Plan: [Mitigation]
- Risk 2: [Scenario] → Plan: [Mitigation]
```

### Duration
15 minutes

---

## 4. Six Thinking Hats

### What It Is
Simulate 6 different thinking perspectives simultaneously. Each "hat" represents a thinking mode:
White=Facts, Red=Emotions, Black=Pessimism, Yellow=Optimism, Green=Creativity, Blue=Process.

### When to Use
- Getting well-rounded analysis on your idea
- Understanding stakeholder concerns (finance, product, design, risk)
- Breaking groupthink

### How to Run (6 steps)

For each hat, ask the user to think and speak FROM that perspective:

1. **White Hat (Facts & Data):** "What do we know for certain? What data do we need?"
   - Known facts: [input]
   - Data gaps: [input]

2. **Red Hat (Emotions & Intuition):** "What's your gut feeling about this? What excites or worries you emotionally?"
   - Excitement: [input]
   - Concerns: [input]
   - Intuition: [input]

3. **Black Hat (Pessimism & Risk):** "What could go wrong? What are the weaknesses in this idea?"
   - Risk 1: [input]
   - Risk 2: [input]
   - Weakness 1: [input]

4. **Yellow Hat (Optimism & Benefits):** "What's the best-case scenario? What are the benefits?"
   - Upside 1: [input]
   - Upside 2: [input]
   - Why this could succeed: [input]

5. **Green Hat (Creativity & Alternatives):** "What if we thought about this completely differently? What are alternative approaches?"
   - Alternative 1: [input]
   - Alternative 2: [input]
   - Creative twist: [input]

6. **Blue Hat (Process & Decisions):** "What's our next step? What do we need to decide?"
   - Next step: [input]
   - Decision needed: [input]
   - Who decides?: [input]

### Expected Output Format

```
Six Thinking Hats Analysis for [PRODUCT]:

White Hat (Facts):
- Known fact 1: [fact]
- Data gap 1: [gap]

Red Hat (Emotions):
- Excitement: [feeling]
- Concern: [feeling]

Black Hat (Risks):
- Risk 1: [risk]
- Weakness 1: [weakness]

Yellow Hat (Benefits):
- Upside 1: [benefit]
- Success factor: [factor]

Green Hat (Creativity):
- Alternative approach 1: [idea]
- Creative twist: [idea]

Blue Hat (Process):
- Next step: [action]
- Decision needed: [decision]

Summary:
- Facts support this? [Yes/No] → Data needed: [what]
- Emotions aligned? [Yes/No] → Concerns: [what]
- Risks manageable? [Yes/No] → Mitigations: [what]
- Benefits compelling? [Yes/No] → Value prop: [what]
- Creative alternatives? [Yes/No] → Should explore: [what]
```

### Duration
20 minutes

---

## 5. Starbursting

### What It Is
Generate questions about your idea organized by Who, What, Where, When, Why, How. Uncovers unknowns and gaps.

### When to Use
- Identifying what you don't know
- Planning validation and research
- Surfacing hidden assumptions

### How to Run (6 steps)

For each letter, generate 2-3 questions:

1. **Who?**
   - Who are the users? Who are stakeholders? Who's the competition?
   - User questions: [input]

2. **What?**
   - What is the product? What problem does it solve? What makes it different?
   - User questions: [input]

3. **Where?**
   - Where will it be used? Where is the market? Where are the barriers?
   - User questions: [input]

4. **When?**
   - When will people need this? When will we launch? When is the market right?
   - User questions: [input]

5. **Why?**
   - Why will people buy this? Why now? Why us?
   - User questions: [input]

6. **How?**
   - How will people find us? How will we charge? How will we deliver value?
   - User questions: [input]

### Expected Output Format

```
Starbursting Questions for [PRODUCT]:

Who?
- [Question 1]
- [Question 2]

What?
- [Question 1]
- [Question 2]

Where?
- [Question 1]
- [Question 2]

When?
- [Question 1]
- [Question 2]

Why?
- [Question 1]
- [Question 2]

How?
- [Question 1]
- [Question 2]

Research Priorities:
1. [Most important question to validate]
2. [Second most important]
3. [Third most important]
```

### Duration
15 minutes

---

## 6. Future State Ideal

### What It Is
Imagine perfect world with no constraints. Design ideal product. Then work backward to identify actual constraints and trade-offs.

### When to Use
- Aspirational product design
- Identifying must-haves vs. nice-to-haves
- Understanding trade-offs forced by constraints

### How to Run (3 steps)

1. **Paint Ideal Future:** "It's 2 years from now and there are NO constraints (no budget, no timeline, no technical limitations). What does your ideal product look like? What can it do? What experience does it provide?"
   - Ideal feature 1: [input]
   - Ideal feature 2: [input]
   - Ideal capability 1: [input]
   - Ideal experience: [input]

2. **Describe Ideal Spec:** Capture the full vision (no trade-offs).
   - [Comprehensive spec of perfect product]

3. **Introduce Constraints & Work Backward:**
   - "Now let's be realistic. What constraints are we actually facing?"
   - Budget constraint: $[X] → What cuts?
   - Timeline constraint: [months] → What ships in MVP vs. v2?
   - Technical constraint: [limitation] → What's the workaround?
   - Team constraint: [team size] → What can we reasonably build?

   Trade-offs made:
   - MVP includes: [must-haves]
   - Defer to v2: [nice-to-haves]
   - Never: [out of scope]

### Expected Output Format

```
Future State Ideal for [PRODUCT]:

Ideal World (No Constraints):
- Feature 1: [full description]
- Feature 2: [full description]
- Experience: [full description]
- Capability 1: [full description]

Ideal Specification:
[Complete ideal feature list and spec]

Actual Constraints:
- Budget: $[X] → Cuts: [features]
- Timeline: [months] → MVP: [scope]
- Technical: [limitation] → Workaround: [solution]
- Team: [size] → Feasible build: [scope]

MVP Scope (Constrained):
Must-Have:
- [Feature 1]
- [Feature 2]

Nice-to-Have (v2):
- [Feature 1]
- [Feature 2]

Never (Out of Scope):
- [Feature 1]
```

### Duration
15 minutes

---

## 7. SWOT

### What It Is
Strategic positioning analysis: Strengths, Weaknesses, Opportunities, Threats.

### When to Use
- Strategic positioning
- Competitive analysis
- Risk assessment and opportunity identification

### How to Run (4 steps)

1. **Strengths (Internal, Positive):** "What's our competitive advantage?"
   - Strength 1: [input]
   - Strength 2: [input]

2. **Weaknesses (Internal, Negative):** "What are we bad at or missing?"
   - Weakness 1: [input]
   - Weakness 2: [input]

3. **Opportunities (External, Positive):** "What market tailwinds or trends favor us?"
   - Opportunity 1: [input]
   - Opportunity 2: [input]

4. **Threats (External, Negative):** "What could derail us?"
   - Threat 1: [input]
   - Threat 2: [input]

### Expected Output Format

```
SWOT Analysis for [PRODUCT]:

Strengths (Internal Assets):
- Strength 1: [description]
- Strength 2: [description]

Weaknesses (Internal Gaps):
- Weakness 1: [description]
- Weakness 2: [description]

Opportunities (Market Tailwinds):
- Opportunity 1: [description]
- Opportunity 2: [description]

Threats (Market Headwinds):
- Threat 1: [description]
- Threat 2: [description]

Strategic Implications:
- Leverage: [How to use strengths?]
- Fix: [How to address weaknesses?]
- Seize: [Which opportunities to pursue?]
- Mitigate: [How to defend against threats?]
```

### Duration
15 minutes

---

## 8. Mind Mapping

### What It Is
Visual, hierarchical brainstorming. Start with central idea, branch into subtopics, sub-subtopics. Captures relationships between concepts.

### When to Use
- Comprehensive exploration of product space
- Understanding system complexity
- Capturing everything about your idea

### How to Run (4 steps)

1. **Central Idea:** "Your product is at the center. What's the central node?"
   - Central node: [PRODUCT_NAME]

2. **First-Level Branches:** "What are the 5-7 main categories or dimensions?"
   - Branch 1: Features & Capabilities
   - Branch 2: User Personas
   - Branch 3: Use Cases
   - Branch 4: Technology Stack
   - Branch 5: Competitive Positioning
   - Branch 6: Revenue Model
   - Branch 7: Success Metrics

3. **Second-Level Sub-Branches:** For each branch, ask sub-questions.
   - Example for "Features":
     - Payment sync
     - Invoicing
     - Reporting
     - Integrations
     - Compliance

4. **Visual Representation:** Create text-based or ASCII mind map.

### Expected Output Format

```
Mind Map for [PRODUCT]:

                        [PRODUCT]
                            |
        __________________|_____________________
       |        |       |       |      |       |
    Features  Users   UseCases  Tech Revenue Metrics
       |        |       |       |      |       |
      [F1]    [P1]    [UC1]   [T1]   [R1]   [M1]
      [F2]    [P2]    [UC2]   [T2]   [R2]   [M2]
      [F3]    [P3]    [UC3]   [T3]   [R3]   [M3]

Insights from Mapping:
- Category 1: [Key insight]
- Category 2: [Key insight]
- Relationship: [How X influences Y?]
```

### Duration
20 minutes

---

## Selection Pattern (During Vision Interview)

### Step 1: Agent Proposes
Based on product context, propose 3-4 relevant techniques:

**Example:** "Your product is innovation-focused. I'd recommend:
1. **SCAMPER** — Generate 10+ feature ideas fast
2. **Future State Ideal** — Define the aspirational design
3. **Reverse Brainstorm** — Identify risks before launch
4. **SWOT** — Understand competitive positioning

Which sounds most useful?"

### Step 2: User Chooses
User selects 1 technique.

### Step 3: Agent Executes
Run the chosen technique interactively with user input.

### Step 4: Generate Artifact
Create markdown artifact with technique insights.

### Step 5: Offer Another Technique
"Excellent! I've captured [INSIGHT]. Want to run another technique or stop here?"

**If YES:** Propose remaining 3 techniques, repeat Steps 2-4.
**If NO:** Move to next block.

### Step 6: Consolidate Insights
Integrate all brainstorm artifacts into product-vision.md under "Brainstorm Insights" section.

---

## Tips for Running Techniques Effectively

✅ **Ask open-ended questions:** "What would happen if...?" vs. "Would you...?"

✅ **Record everything:** No judgment, no filtering. Quantity = quality in brainstorming.

✅ **Validate understanding:** "So you mean [interpretation]?" to avoid misunderstanding.

✅ **Use concrete examples:** "For instance, Stripe does..." makes abstract concepts concrete.

✅ **Look for patterns:** After brainstorming, highlight themes and connections.

✅ **Transition smoothly:** "These insights suggest [implication]. Ready for the next block?"

---

## Next Steps in Vision Interview

After brainstorming:
1. User has articulated HMW questions
2. Brainstorm technique has generated insights
3. Integration into product-vision.md begins
4. Move to stress-test and validation block
