---
description: Generate User Journey Map documenting user experience flows
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate User Journey Map

Creating user journey for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/discovery/product-vision.md && echo "✓ product-vision.md exists" || echo "⚠ Missing product vision (recommended to run /vision first)"`

## Setup

!`mkdir -p docs/design && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/ux-chain/knowledge/user-journey.md

## Interactive Journey Mapping

I'll help you map user journeys:

### Step 1: Review Vision

Read product vision and objectives:

@docs/discovery/product-vision.md

### Step 2: Identify Key Journeys

**Ask the user:**

For each primary persona, what are the key journeys to map?

**Common journey types:**
- Onboarding journey (first-time user experience)
- Core task journey (main job to be done)
- Recovery journey (error handling, support)
- Re-engagement journey (bringing back inactive users)

**Example journeys:**
- "Sarah creates her first invoice"
- "Sarah checks payment status"
- "Sarah handles overdue payment"

[Identify 3-5 key journeys to map]

### Step 3: Journey Stages

**For each journey, ask about stages:**

Map the journey in stages (typically 5-8 stages):

**Example: "Sarah creates her first invoice"**

1. **Awareness/Entry**: How does the journey start?
2. **Consideration**: What does the user evaluate?
3. **Action/Task**: What does the user do?
4. **Completion**: How does the task finish?
5. **Follow-up**: What happens after?

[Define stages for each journey]

### Step 4: Journey Details (Per Stage)

**For each stage, document:**

#### User Actions
- What does the user do?
- What decisions do they make?
- What inputs do they provide?

#### User Thoughts
- What is the user thinking?
- What questions do they have?
- What are they trying to understand?

#### User Emotions
- How does the user feel? (excited, confused, frustrated, confident)
- Emotion rating (1-5, negative to positive)

#### Touchpoints
- What UI screens/pages?
- What interactions (clicks, form fills, reads)?
- What channels (web, mobile, email)?

#### Pain Points
- What frustrations exist?
- What causes friction?
- What might go wrong?

#### Opportunities
- How can we improve this stage?
- What delighters could we add?
- How can we reduce friction?

#### Systems Involved
- What backend systems?
- What integrations?
- What data is accessed/modified?

### Step 5: Example Journey Map

**Confirm journey structure:**

"Here's the journey map for 'Sarah creates her first invoice':

**Stage 1: Awareness (Emotion: Curious 😊 +3)**
- Actions: Signs up, logs in first time
- Thoughts: 'Where do I start? Is this easy to use?'
- Touchpoints: Sign-up page, welcome email, dashboard
- Pain points: Overwhelming dashboard, too many options
- Opportunities: Guided onboarding, clear CTA for 'Create Invoice'
- Systems: Auth service, user database

**Stage 2: Invoice Creation (Emotion: Focused 😐 +1)**
- Actions: Clicks 'New Invoice', fills client details, adds line items
- Thoughts: 'Do I have all the info I need? Are taxes calculated automatically?'
- Touchpoints: Invoice form, client autocomplete, line item editor
- Pain points: Not sure about tax calculation, tedious line item entry
- Opportunities: Saved client templates, smart defaults, bulk import
- Systems: Invoice service, client database, tax calculator

**Stage 3: Review (Emotion: Anxious 😟 -1)**
- Actions: Previews invoice PDF, checks calculations, reviews terms
- Thoughts: 'Does this look professional? Did I miss anything?'
- Touchpoints: PDF preview, edit mode, calculation summary
- Pain points: Worried about errors, can't easily compare to previous invoices
- Opportunities: Comparison view, confidence indicators, professional templates
- Systems: PDF generator, template engine

**Stage 4: Send (Emotion: Relieved 😌 +2)**
- Actions: Adds client email, customizes message, clicks 'Send'
- Thoughts: 'Will the client receive this? When will they pay?'
- Touchpoints: Email composer, send confirmation, tracking dashboard
- Pain points: No delivery confirmation, unclear payment timeline
- Opportunities: Email tracking, payment reminders, status updates
- Systems: Email service, notification system, payment tracker

**Stage 5: Follow-up (Emotion: Satisfied 😊 +4)**
- Actions: Checks invoice status, sees payment received, marks complete
- Thoughts: 'Great! Payment received. Easy to track.'
- Touchpoints: Dashboard, payment notification, invoice archive
- Pain points: None (happy path)
- Opportunities: Thank you automation, review request, upsell
- Systems: Payment gateway, notification system, analytics

Does this journey map accurately capture the user experience?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/user-journey.md` with journey maps.

**Document Structure:**
- Journey Overview (which personas, which journeys)
- For each journey:
  - Journey title and persona
  - Journey goal (what user wants to accomplish)
  - Journey stages (5-8 stages)
  - For each stage:
    - Stage name
    - User actions
    - User thoughts (internal dialogue)
    - User emotions (rating and emoji)
    - Touchpoints (screens, interactions, channels)
    - Pain points (frustrations, friction)
    - Opportunities (improvements, delighters)
    - Systems involved (backend, integrations)
  - Journey metrics:
    - Overall sentiment trend (emotion graph)
    - Critical pain points to address
    - High-impact opportunities
    - Drop-off risk points
  - Mermaid journey diagram
  ```mermaid
  journey
    title Sarah Creates First Invoice
    section Awareness
      Sign up: 5: Sarah
      First login: 4: Sarah
    section Creation
      New invoice: 3: Sarah
      Fill details: 2: Sarah
    section Review
      Preview PDF: 3: Sarah
    section Send
      Send invoice: 4: Sarah
    section Follow-up
      Payment received: 5: Sarah
  ```

## Validation

After generation:

!`test -f docs/design/user-journey.md && echo "✓ user-journey.md created" || echo "✗ Generation failed"`

**Journey map checklist**:
!`if [ -f docs/design/user-journey.md ]; then
  grep -ci "journey\|stage" docs/design/user-journey.md | xargs echo "Journey stages:"
  grep -ci "pain point\|friction" docs/design/user-journey.md | xargs echo "Pain points identified:"
  grep -ci "opportunity\|improvement" docs/design/user-journey.md | xargs echo "Opportunities:"
  grep -ci "emotion\|feel" docs/design/user-journey.md | xargs echo "Emotional insights:"
fi`

## Next Steps

**Create UX sitemap**:
```
/ux-sitemap
```

**Create UX design decisions**:
```
/ux-design-decisions
```

Or run complete UX chain:
```
/ux-docs
```

---

**User journey map generated!** User experience flows documented with emotions, pain points, and opportunities.
