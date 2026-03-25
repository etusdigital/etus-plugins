# Guide: Interactive Interview for PRD

**Objective:** Guide user through brainstorming and feature prioritization to generate high-quality prd.md with clear traceability.

## Table of Contents
1. [Block 1: Vision Confirmation](#block-1-vision-confirmation-2-3-min)
2. [Block 2: Feature Brainstorming with HMW](#block-2-feature-brainstorming-using-hmw-8-12-min)
3. [Block 3: MoSCoW Prioritization](#block-3-moscow-prioritization-5-8-min)
4. [Block 4: Scope Validation](#block-4-scope-validation-3-5-min)
5. [Block 5: Success Criteria](#block-5-success-criteria-5-8-min)
6. [Block 6: PRD Generation](#block-6-prd-generation-automatic)
7. [Block 7: Planning Gate Decision](#block-7-planning-gate-decision-2-3-min)
8. [General Notes](#general-notes)
9. [Quality Checkpoints](#quality-checkpoints)

---

## Block 1: Vision Confirmation (2-3 min)

### Context

User has passed Discovery Gate with validated product-vision.md.

### Questions

1. "Confirming: the product vision is [RESTATE in 1 sentence]? Correct?"
   - If no: "Let's return to product-vision.md to review"
   - If yes: Proceed

2. "What are the 2-3 main problems this product solves?"
   - User lists
   - Confirm: "Are these problems documented as BO-# in product-vision.md?"

3. "Is there any new context since we generated the vision? (market timing, feedback, constraints)"
   - Document changes
   - Assess impact on scope

### Output

- Vision reaffirmed
- Problems mapped to BO-#
- Context updates (if any) registered
- Ready for brainstorm

---

## Block 2: Feature Brainstorming using HMW (8-12 min)

### Context

For EACH BO-# (Business Objective) from product-vision.md, we ask:
"How might we [solve/transform/leverage] [problem/opportunity]?"

### Flow per BO-#

**For each BO-#:**

1. **Present BO-#:** "This BO-# is: [description from product-vision.md]"

2. **Formulate HMW:**
   ```
   "How might we [transform X / solve Y / leverage Z]?"
   ```
   - Let user answer or co-formulate
   - Refine if too vague (ex: "How might we improve UX?" → "How might we reduce onboarding time from 30min to <5min?")

3. **Brainstorm Features:**
   "What features would implement this solution? List 2-5 ideas."
   - User lists (ex: "Onboarding template", "Video tutorial", "Interactive checklist")
   - Don't criticize, just capture

4. **Refine Names:**
   "These features [list]. Is any redundant? Does any deserve to be separated?"
   - Consolidate where there's overlap
   - Name features clearly (ex: "Video Tutorial Onboarding" instead of "Video")

5. **Confirm Coverage:**
   "Is this BO-# well covered by [X features]? Is something missing?"
   - Add features if gap identified
   - Or confirm "Yes, sufficient"

### Result

- List of features grouped by BO-#
- ~2-5 features per typical BO-#
- Total expected: 10-20 initial features (before prioritizing)

### Example Conversation

```
BO-1: "Reduce freelancer administrative time"

Me: "How might we reduce administrative time? What specific activities?"

User: "Invoice creation, sending, client tracking"

Me: "Great. What features would facilitate this?"

User: "1) Pre-filled invoice templates
         2) Automatic email sending
         3) Payment tracking
         4) Status dashboard"

Me: "Are these 4 distinct or is there overlap?"

User: "They are independent"

Me: "Perfect. Is anything missing for this BO-1?"

User: "No, I think it's covered"
```

---

## Block 3: MoSCoW Prioritization (5-8 min)

### Context

Consolidated feature list. Now prioritize using MoSCoW.

### Explain MoSCoW

```
Must Have
  → Features without which product cannot launch
  → Essential for MVP
  → ~30% of features

Should Have
  → Important, but not blockers
  → Competitive differentiator
  → ~50% of features

Could Have
  → Nice-to-have, deferrable to V2
  → ~20% of features

Won't Have
  → Explicitly out of scope
  → Document why not
```

### Prioritization Flow

For EACH feature:

1. **Key Question:**
   "Without this feature, is the product launchable (MVP)?"
   - If NO → "Must Have"
   - If YES → Next question

2. **Question 2:**
   "Does this feature differentiate from competition or is it expected by users?"
   - If differentiates → "Should Have"
   - If expected → "Could Have"
   - If "I don't understand" → Conversation to refine

3. **Question 3 (if Could Have):**
   "Deferrable to V2 without compromising user acceptance?"
   - If YES → "Could Have"
   - If NO → Reclassify to "Should Have"

4. **Won't Have:**
   "Are there features we proposed but definitely won't include? Why?"
   - Capture and document reason

### Distribution Validation

After prioritizing, verify:

```
Expected:
- Must Have: ~25-35% (must be "must", not "everything")
- Should Have: ~40-50%
- Could Have: ~15-25%
- Won't Have: ~5-10% (explicitly rejected)

If distribution unbalanced:
- Too many Must Have (>40%): "Is all this really 'must have'? Should some be 'should'?"
- Few Should Have (<30%): "Missing differentiated features?"
```

### Result

- Each feature has MoSCoW priority
- Distribution validated
- Won't Have features have documented reason

### Example

```
Me: "Invoice Creation - can you launch without this feature?"

User: "No, it's core"

Me: "Must Have then. Next: Stripe Integration - does it differentiate?"

User: "Would be nice, but not required for MVP"

Me: "Should Have then (differentiator). Next: Analytics Dashboard..."
```

---

## Block 4: Scope Validation (3-5 min)

### Context

Features prioritized. Consolidate In-Scope and Out-of-Scope.

### Questions

1. **In-Scope Complete?**
   "Looking at your Must Have and Should Have list: is there any gap?
   Is there something missing to address the vision?"
   - User may identify missing feature
   - Or confirm "It's complete"

2. **Out-of-Scope Clear?**
   "Looking at Could Have and Won't Have:
   is there anything that should be out-of-scope but is in-scope?"
   - Move if necessary
   - Document reason for Won't Have

3. **Timing & Phasing:**
   "Are there features we'd like in the future (V2)?
   Should we document them as Could Have or remove?"
   - If remove: Won't Have with reason "V2"
   - If keep: Leave as Could Have

4. **Scope Approval:**
   "Does this scope [N features in-scope] represent the product you want to launch?"
   - If YES: Ready for next step
   - If NO: "What needs to change?"

### Result

- In/Out scope validated with stakeholder
- Could Have and Won't Have explicit
- Ready to derive user-stories

---

## Block 5: Success Criteria (5-8 min)

### Context

Features defined and prioritized. Now, for EACH feature, define how to measure success.

### General Instructions

Success criteria must answer: **"How do we know this feature was successful?"**

Types of criteria:
- **Quantitative:** Numeric metric (ex: "30% increase in conversion")
- **Qualitative:** User feedback (ex: "Users report less friction")
- **Technical:** Performance/availability (ex: "Latency <200ms, Uptime >99%")

### Flow per Feature

For EACH feature (Must Have + Should Have):

1. **Initial Question:**
   "For [Feature Name], how do we know it was successful?
   What indicator would you look at to validate?"

2. **Capture Answer:**
   User suggests metric
   - If vague ("Users like it"): Refine ("Specifically, how do you measure liking?")
   - If specific ("Upload time <2s"): Capture as is

3. **Validate Measurability:**
   "Can we measure [criterion] with current tools?
   Or does it need new implementation?"
   - Inform user (may impact roadmap)

4. **Multiple Criteria:**
   "Are there other indicators for [Feature]?
   (ex: besides speed, is there expected adoption?)"
   - List 1-3 criteria per typical feature

5. **Could Have Features:**
   "For Could Have, do we need criteria?
   Or just 'if implemented, it will be like this'?"
   - Optional. Capture if user wants.

### Good vs Bad Examples

**Good:**
```
Feature: Invoice Creation
- Metric 1: Create invoice in <2 minutes (measured by analytics)
- Metric 2: Abandonment rate <10% (vs 30% currently)
- Metric 3: NPS +5 points (compared to previous tool)
```

**Bad:**
```
Feature: Invoice Creation
- Metric: Feature is useful
- Metric: Users are happy
- Metric: Works well
```

### Result

- Each Must Have + Should Have has 1-3 success criteria
- Criteria are specific and measurable
- Clear traceability (how to validate ROI)

---

## Block 6: PRD Generation (Automatic)

### Context

Interview complete. Data collected:
- Vision confirmed
- Features by BO-#
- MoSCoW prioritization
- In/Out scope
- Success criteria
- PRD-F-# IDs (auto-generated sequential)

### Generation Process

1. **Internal Validation:**
   - Each PRD-F-# linked to BO-#? ✓
   - Criteria specific (not boilerplate)? ✓
   - MoSCoW distribution OK? ✓
   - No gaps? ✓

2. **Render:**
   - Structure in docs/ets/projects/{project-slug}/planning/prd.md
   - Follow template.md exactly
   - Sequential IDs PRD-F-1, PRD-F-2, ...

3. **Pre-Write Checklist:**
   ```
   Before saving prd.md:
   - [ ] Executive summary linked to vision
   - [ ] In/Out scope disjunct
   - [ ] Features grouped by Must/Should/Could/Won't
   - [ ] Each feature with: description, BO-#, HMW, criteria
   - [ ] Dependencies mapped
   - [ ] Sequential PRD-F-# IDs
   - [ ] ids.yml updated
   - [ ] Statistics calculated
   ```

4. **Result File:**
   ```
   docs/ets/projects/{project-slug}/planning/prd.md
   - [X] lines
   - Ready for user-stories
   ```

### Offer to User

"PRD generated! Options:
1. View in chat (copy manually)
2. Save to docs/ets/projects/{project-slug}/planning/prd.md (automatic)
3. Review before saving (edit in chat)
"

---

## Block 7: Planning Gate Decision (2-3 min)

### Context

PRD generated. Before proceeding to user-stories, gate validation.

### Planning Gate Criteria

```
✓ PRD features cover all BO-# from product-vision?
✓ Scope is realistic for 1-2 sprints?
✓ Must Have is ~30% (not everything critical)?
✓ Success criteria are measurable?
✓ Dependencies are mapped?
```

### Possible Decisions

1. **GO**
   → Next step: user-stories
   → "PRD is ready. Shall we derive user-stories?"

2. **DESCOPE**
   → Remove Could Have features
   → Reclassify Should Have to Could Have
   → "Which feature do we remove to simplify?"

3. **ITERATE**
   → Refine PRD (more HMW, reorganize)
   → "Which aspect of the PRD wants refinement?"

### Result

- Explicit decision made
- Next step clear
- PRD locked in for downstream derivation

---

## General Notes

### Language

- Use English throughout interview
- Be conversational, not formal
- Patterns: "Must have" instead of technical jargon

### Timing

- Total expected: 20-30 minutes for interactive PRD
- Can be faster if user well-prepared
- Can be longer if scope is complex

### Common Errors

| Error | How to Avoid |
|-------|-------------|
| Vague features (ex: "Dashboard") | Refine: "Dashboard of what? For whom?" |
| All Must Have | Question: "Really can't launch without this?" |
| No success criteria | Ask: "How do we know it worked?" |
| PRD without BO-# links | Validate against product-vision.md |
| Non-sequential IDs | Auto-generated, validate before saving |

### Next Steps

After PRD GO decision:
1. Derive user-stories.md (1+ US-# per PRD-F-#)
2. For complex features (>3 business rules), create feature-spec-[name].md
3. Consolidate in Planning Phase output
4. Present Planning Gate (full PRD + user-stories + specs)

---

## Complete Conversation Example (Micro)

```
Me: "Confirming: your vision is 'invoicing platform for freelancers'. Correct?"

User: "Yes, exactly"

Me: "BO-1 is 'Reduce administrative time'. How might we reduce time?"

User: "Quick invoice creation, email sending, payment tracking"

Me: "3 features for BO-1. Done. Next: BO-2 'Cash flow visibility'. How might we?"

User: "Dashboard showing paid vs pending invoices, forecasts"

Me: "2 features. Now prioritization. Invoice Creation - can you launch without it?"

User: "No"

Me: "Must Have then. Dashboard - does it differentiate?"

User: "Would be nice, but not required"

Me: "Should Have. Done. Success criteria for Invoice Creation?"

User: "Create in <2 minutes, no leaving platform"

Me: "Perfect. PRD is ready! Approve?"

User: "Yes!"

Me: "Generating docs/ets/projects/{project-slug}/planning/prd.md. Next: user-stories.md"
```

---

## Quality Checkpoints

| Checkpoint | Validation |
|------------|-----------|
| Post Vision | Vision reaffirmed, BO-# confirmed |
| Post Brainstorm | 10-20 features listed, grouped by BO-# |
| Post MoSCoW | Distribution: M ~30%, S ~50%, C ~20% |
| Post Scope | In/Out explicit, disjunct |
| Post Criteria | Each Must+Should has 1-3 specific criteria |
| Post Generation | Sequential IDs, BO-# links validated |
| Post Gate | Explicit decision (GO/DESCOPE/ITERATE) |
