# Interview Guide: Project Context

## Introduction

"I'm going to ask you 12-14 questions across 5 blocks. These questions help me capture your project identity, the problem you're solving, your technical context, and key constraints. This becomes your living reference document for all downstream decisions."

**Duration:** ~25 minutes total
**Output:** project-context.md ready for docs/ets/projects/{project-slug}/discovery/

---

## Block 1: Identity (2 questions)

### Q1: Project Name & Tagline
**Question:** "What is the name of your project, and how would you describe it in 5-10 words?"

**Alternatives if stuck:**
- "What will people call this? What's your internal working title?"
- "If you had to pitch this in one sentence at a coffee shop, what would you say?"

**Record:**
- Project name: [user input]
- Tagline: [user input]

---

### Q2: Elevator Pitch
**Question:** "Now give me a 30-second pitch: What is it, who is it for, and why does it matter?"

**Listen for:** Clarity on who, what, why. Not just features.

**Follow-up if vague:** "What's the problem your users face that this solves?"

**Record:**
- Elevator pitch: [user input]

---

### Q1 Confirmation
> **Confirm Understanding:** "So your project is called [NAME], described as [TAGLINE]. The pitch is: [PITCH]. Is that right?"

If user says NO: "What should I adjust?"

---

## Block 2: Problem (3 questions)

### Q3: The Problem Statement
**Question:** "What is the specific problem you're solving? Be as concrete as possible—not 'people need better tools' but 'X loses Y hours per week doing Z.'"

**Listen for:** Specificity. Quantified impact if possible.

**Anti-pattern:** Vague statements like "improve efficiency" → Push for examples.

**Record:**
- Problem: [user input]

---

### Q4: Current Solution & Friction
**Question:** "How do people solve this problem today? What's broken or painful about their current approach?"

**Listen for:** Existing workflows, tool stack, pain points, workarounds.

**Record:**
- Current solution: [user input]
- Friction points: [user input]

---

### Q5: Who & Why It Matters
**Question:** "Who has this problem? And what's the impact if we don't solve it—lost revenue, wasted time, compliance risk, etc.?"

**Listen for:** Audience clarity + business impact quantification.

**Record:**
- Target audience: [user input]
- Impact/opportunity: [user input]

---

### Q2 Confirmation
> **Confirm Understanding:** "So [AUDIENCE] struggles with [PROBLEM]. Today they [CURRENT_SOLUTION], but the friction is [FRICTION]. The impact is [IMPACT]. Accurate?"

If user says NO: "What should I adjust?"

---

## Block 3: Technical Context (2 questions)

### Q6: Existing Stack & Deployment
**Question:** "What's your current tech stack, and where will this live? (e.g., SaaS, mobile, desktop, embedded, API-only)"

**Listen for:** Frontend, backend, database, deployment platform, monitoring.

**Record:**
- Existing stack: [frontend/backend/db/deployment/monitoring]
- Platform/distribution: [user input]

---

### Q7: Technology Preferences & Constraints
**Question:** "Any tech preferences, languages, frameworks you want to use or avoid? Any legacy system constraints we need to work around?"

**Listen for:** Learning investments, vendor lock-in concerns, integration requirements, skill alignment.

**Record:**
- Tech preferences: [user input]
- Tech constraints: [user input]

---

### Q3 Confirmation
> **Confirm Understanding:** "Your stack is [STACK]. You prefer [PREFERENCES]. Constraints are [CONSTRAINTS]. Right?"

---

## Block 4: Constraints (2 questions)

### Q8: Timeline, Budget & Resources
**Question:** "What are your hard constraints? Timeline (when do you need this?), budget cap, and team size?"

**Listen for:** MVP deadline, budget ceiling, solo vs. team, skill gaps.

**Record:**
- Timeline: [user input]
- Budget: [user input]
- Team size: [user input]
- Skill gaps: [if mentioned, capture]

---

### Q9: Regulatory, Market, Business Constraints
**Question:** "Any regulatory requirements (GDPR, PCI-DSS, SOC 2, etc.), competitive pressures, or business constraints we should know?"

**Listen for:** Compliance, market timing, go-to-market strategy, competitive positioning.

**Record:**
- Regulatory: [user input]
- Market/business constraints: [user input]

---

### Q4 Confirmation
> **Confirm Understanding:** "Timeline is [TIMELINE]. Budget is [BUDGET]. Team is [TEAM_SIZE]. Constraints are [CONSTRAINTS]. Correct?"

---

## Block 5: Validation (1 question)

### Q10: Stress-Test & Critical Assumptions
**Question:** "What's the biggest assumption you're making about this project? What would break your plan if it turned out to be wrong?"

**Listen for:** Risky assumptions, unknowns, validations needed.

**Record:**
- Critical assumption: [user input]
- Risk if wrong: [user input]

---

### Q5 Confirmation & Wrap
> **Confirm Understanding:** "Your biggest risk is [ASSUMPTION]. If that's wrong, [CONSEQUENCE]. Should we document this as a critical assumption to validate?"

---

## After All Blocks: Synthesis

**Present the full context summary:**

"Alright, here's what I'm capturing for your project context:

**Identity:** [NAME] - [TAGLINE]
**Problem:** [PROBLEM] affecting [AUDIENCE]
**Current Pain:** [FRICTION]
**Impact:** [IMPACT]
**Stack:** [STACK]
**Tech Preferences:** [PREFERENCES]
**Timeline:** [TIMELINE]
**Budget:** [BUDGET]
**Team:** [TEAM_SIZE]
**Critical Risk:** [ASSUMPTION] → [CONSEQUENCE]

Does this capture everything accurately?"

---

## Quality Checklist

Before generating the document, verify:

- [ ] Project name and tagline provided?
- [ ] Problem statement is specific (not generic)?
- [ ] Target audience clearly identified?
- [ ] Current solution & friction articulated?
- [ ] Stack and tech preferences documented?
- [ ] Timeline and budget captured?
- [ ] Team size and skill gaps noted?
- [ ] At least one critical assumption identified?
- [ ] All blocks confirmed by user?
- [ ] User ready to generate document?

---

## Anti-Patterns to Avoid

❌ **Batch Questions:** Don't ask all 10 at once. Interview block-by-block.

❌ **Assume Instead of Ask:** If user says "we're a startup," don't assume budget. Ask: "What's your budget cap?"

❌ **Skip Validation:** Always confirm understanding after each block.

❌ **Generate Without Approval:** Show the draft. Ask "Anything to refine?"

---

## Next Steps

Once project-context.md is approved:

1. User acknowledges: "Yes, save this."
2. Write document to `docs/ets/projects/{project-slug}/discovery/project-context.md`
3. Feed context to next skill: **product-vision**
4. Offer: "Ready to define your vision and business objectives?"
