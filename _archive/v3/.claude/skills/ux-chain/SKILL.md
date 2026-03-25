---
name: ux-chain
description: Generate complete UX documentation (user journeys, sitemaps, wireframes, style guide) using full Double Diamond methodology and How Might We statements. Use when designing user experiences, creating design systems, or specifying frontend implementation for solo developers.
---

# UX Chain

Generate comprehensive user experience documentation from jobs-to-be-done through frontend implementation specifications using the complete Double Diamond design process.

## Purpose

This skill guides solo developers through the entire UX design process by generating a connected chain of documents **through interactive conversation** spanning all four phases of the Double Diamond:

**DISCOVER (Diverge) → DEFINE (Converge):**
1. **User Journey** (jour) - Current state journey mapping with pain points

**DEFINE (Refine):**
2. **UX Sitemap** (uxs) - Routes, views, and navigation structure

**DEVELOP (Diverge) → DELIVER (Converge):**
3. **Wireframes** (wire) - Layout specifications and responsive breakpoints
4. **Style Guide** (sty) - Visual design tokens (tok.*)

Each document references upstream via lowercase IDs, maintaining traceability from user needs through implementation.

## Interactive UX Workflow

**This skill is conversation-driven, not batch-oriented.**

UX design requires deep understanding of user context, preferences, and constraints. This skill:
1. **Interviews users** about jobs, pain points, and desired outcomes (JTBD method)
2. **Validates journey maps** to ensure accurate current state understanding
3. **Discusses design patterns** collaboratively (not dictating solutions)
4. **Gathers style preferences** before generating design tokens
5. **Reviews wireframes** iteratively with user feedback

**Key Principle:** Design emerges from conversation, not assumptions.

**Do NOT:**
- Generate UX specs based on assumptions about user preferences
- Proceed without validating journey pain points
- Dictate design patterns (present options instead)
- Create style guides without gathering brand/aesthetic input
- Skip accessibility discussions

**Success Criteria:** User feels like they're co-designing with a UX expert, not receiving auto-generated specs.

## When to Use This Skill

Use this skill when:
- Designing user experiences for a new product or feature
- Creating a design system or style guide from scratch
- Need to document UX decisions with clear rationale
- Translating user research into actionable design
- Specifying frontend implementation requirements
- Running the Deliver phase parallel workstream (UX track)

Do NOT use for:
- Backend API design (use api-backend skill instead)
- Data modeling (use data-chain skill instead)
- Business requirements (use feature-development-chain skill instead)

**Dependencies:** Requires `prd` (product requirements) and `user-stories` (docs/planning/user-stories.md) from feature-development-chain skill as input.

## Methodology Integration

### Double Diamond Framework (Reduced Scope)

This skill implements the CORE Double Diamond design process across phases:

```
DISCOVER/DEFINE     DEFINE          DEVELOP/DELIVER
(Converge)       (Refine)         (Converge)

   jour   →    uxs    →    wire/sty
   ↓           ↓             ↓
Journey      Routes/      Wireframes
Mapping      Views        & Tokens
```

**DISCOVER/DEFINE Phase - Understanding & Mapping:**
- Map current state user journeys
- Identify pain points and opportunities

**DEFINE Phase - Synthesizing Insights:**
- Converge on specific UX problems to solve
- Define routes, views, and navigation structure

**DEVELOP/DELIVER Phase - Exploring & Refining:**
- Create wireframes for key screens
- Define design tokens and style guide
- Ensure accessibility and performance standards

### How Might We (HMW) Statements

Transform journey pain points into design opportunities:

**Structure:** "How might we [improve experience] for [user in context] so that [benefit]?"

**Example Transformation:**
```
Pain Point: Users abandon signup at payment step (60% drop-off)
↓
HMW: How might we reduce friction at payment while building trust?
↓
Design Solutions:
- Show security badges and guarantees
- Offer guest checkout option
- Display progress indicator
- Save partial progress automatically
```

**Best Practices for UX HMW:**
- Focus on user emotions and mental models
- Consider accessibility in opportunities
- Frame around desired user outcomes
- Avoid embedding specific UI solutions

### 5W2H Analysis for UX Validation

Apply systematic questioning to validate UX completeness:

**WHAT:**
- What screens/states exist in the system?
- What actions can users take?
- What feedback do users receive?

**WHO:**
- Who are the different user types?
- Who has access to which features?
- Who needs accommodations (accessibility)?

**WHERE:**
- Where do users enter the system?
- Where are the key decision points?
- Where do errors occur most?

**WHEN:**
- When do users need help/guidance?
- When should we show onboarding?
- When do users feel accomplished?

**WHY:**
- Why would users choose this path?
- Why might they abandon flow?
- Why is this pattern better than alternatives?

**HOW:**
- How do users navigate between states?
- How do we communicate status?
- How do we handle errors gracefully?

**HOW MUCH:**
- How much cognitive load per screen?
- How much data to show at once?
- How much friction is acceptable?

## How to Use This Skill

### Phase 1: DISCOVER/DEFINE - Understanding User Needs

#### 1. User Journey (jour)

Map CURRENT STATE journeys (not idealized future):

**Journey Structure Per Stage:**
```
Stage: [Discovery → Consideration → Purchase → Onboarding → Usage → Advocacy]

Current State:
- Actions taken
- Touchpoints used
- Pain points encountered
- Emotions felt

Metrics:
- Time spent
- Abandonment rate
- Support tickets
- Satisfaction score

Paths:
- Happy path (best case)
- Alternative paths (variations)
- Error paths (failure modes)
```

**Create HMW Statements from Pain Points:**
```
Pain: "Users don't understand pricing tiers"
↓
HMW: How might we make pricing transparent and help users self-select the right tier?
```

**Template Reference:** See `knowledge/user-journey.md` for journey mapping structure

### Phase 2: DEFINE - Synthesizing Insights (Convergent)

#### 2. UX Sitemap (uxs)

Define routes, views, and navigation structure:

**Route Structure:**
```
route_id: r:/path/to/route
name: Human-readable name
parent: Parent route (for breadcrumbs)
auth_guard: public | user | admin | role:<name>
params: Route parameters (e.g., :invoiceId)
```

**View Structure:**
```
view_id: view.<domain>.<page>
type: page | modal | drawer | layout
route_id: Associated route
priority: P0 | P1 | P2
stories: User story IDs (US-#)
apis: Backend endpoints used
events: Analytics events (ev.*)
components: UI components (cmp.*)
required_states: #default, #loading, #empty, #error
```

**Example:**
```
route_id: r:/billing/invoices/:invoiceId
name: Invoice Detail
parent: r:/billing/invoices
auth_guard: user
params: :invoiceId (uuid)

view_id: view.billing.invoice-detail
type: page
priority: P0
stories: US-10
apis: GET /api/v1/invoices/:id
events: ev.invoice.view
required_states: #default, #loading, #error
```

**Navigation Graph Example:**
```
r:/auth/login —(success)→ r:/dashboard
r:/dashboard —(billing link)→ r:/billing/invoices
r:/billing/invoices —(row click)→ r:/billing/invoices/:invoiceId
```

**Validation Questions:**
- Are all routes mapped with auth guards?
- Do all views link to user stories (US-#)?
- Are required UI states defined for each view?
- Is the navigation graph complete and logical?

**Template Reference:** See `knowledge/uxsm.md` for complete sitemap patterns

### Phase 3: DEVELOP/DELIVER - Exploring & Refining Solutions

#### 3. Wireframes (wire)

Create layout specifications with responsive breakpoints:

**Wireframe Structure:**
```
Screen: [ScreenName]
Purpose: User goal for this screen
Layout: Grid/flex structure
Components: List of components used
Content Hierarchy: Priority ranking (H1, H2, body)
Responsive Breakpoints:
- Mobile (320-767px): Layout changes
- Tablet (768-1023px): Layout changes
- Desktop (1024px+): Layout changes
```

**Create HMW for Layout Challenges:**
```
Challenge: Too much information on dashboard, users overwhelmed
↓
HMW: How might we prioritize information so users see what matters most first?
↓
Solution: Card-based dashboard with customizable priority, progressive disclosure
```

**Validation:**
- Is content hierarchy clear at each breakpoint?
- Are CTAs prominent and accessible?
- Is navigation intuitive?
- Are error states designed?
- Is loading state handled?

**Template Reference:** See `knowledge/wireframes.md` for wireframe standards

#### 4. Style Guide (sty) - **INTERACTIVE STYLE PREFERENCES**

**STEP 1: Gather Design Preferences**

Ask user before generating tokens:

```
"Let's establish your design system. I'll ask about key style preferences:

**Brand/Aesthetic:**
1. What emotion should your UI convey? (Professional/Playful/Minimal/Bold)
2. Do you have existing brand colors? (If yes, provide hex codes)
3. Font preference? (Sans-serif/Serif/Monospace)

**Accessibility & Density:**
4. Accessibility priority? (Must meet WCAG 2.1 AA? AAA?)
5. Visual density? (Tight/Comfortable/Spacious)
6. Target devices? (Desktop-first/Mobile-first/Both equally)"
```

[Wait for answers. Use responses to generate appropriate tok.* values]

**STEP 2: Generate with User's Preferences**

Define ALL visual design tokens (ONLY place for tok.* definitions):

**Token Categories:**
```
tok.color.primary.500
tok.color.text.body
tok.spacing.md
tok.typography.heading.h1
tok.border.radius.button
tok.shadow.elevation.2
tok.animation.duration.fast
```

**Design Token Structure:**
```
Token: tok.color.primary.500
Value: #3B82F6
Usage: Primary actions, links, focus states
Accessibility: Meets 4.5:1 contrast on white
Do: Use for interactive elements
Don't: Use for large text blocks
```

**Complete Token System:**
- Colors (semantic naming: primary, success, error, warning, info)
- Typography (scales, weights, line heights)
- Spacing (8px scale recommended)
- Borders (radius, width)
- Shadows (elevation levels)
- Animation (durations, easings)
- Breakpoints (mobile, tablet, desktop)
- Z-index (layering system)

**Apply 5W2H to Design System:**
- WHAT tokens are truly needed vs nice-to-have?
- WHERE will each token be used?
- WHY this value vs alternatives?
- HOW MUCH variation is manageable?

**Template Reference:** See `knowledge/style-guide.md` for complete token system

## Workflow Sequence

### Standard Flow (Core Double Diamond)

```
DISCOVER/DEFINE:
1. jour (Journey) → Map current state with pain points
   ↓
   🔹 HMW: Transform pain points into opportunities
   ↓

DEFINE:
2. uxs (Sitemap) → Define routes, views, and navigation
   ↓

DEVELOP/DELIVER:
3. wire (Wireframes) → Create responsive layouts
   ↓
4. sty (Style Guide) → Define all design tokens (tok.*)
   ↓
   ✅ UX TRACK COMPLETE
```

### Parallel Execution Context

The UX chain runs in parallel with:
- **Data Chain** (data → cat): Database and field definitions
- **API Backend** (be): API specifications and contracts

**Frontend implementation** will use:
- UX outputs: jour, wire, sty
- Backend outputs: be (API contracts)
- Data outputs: dict (field definitions, ev.* events)

## Phase Transitions

### Discover/Define → Define Transition

**Criteria to move forward:**
- Current state journeys documented with metrics
- Pain points quantified and prioritized
- HMW statements created for top pain points

### Define → Develop/Deliver Transition

**Criteria to move forward:**
- All routes, views, and navigation flows mapped
- Navigation patterns established

### Develop/Deliver Completion

**Criteria to finalize:**
- Wireframes cover key screens at all breakpoints
- Accessibility requirements defined (WCAG 2.1 AA)
- Style guide has complete token system

## Gate Validation

### UX Track Completion

Before frontend implementation, validate:

- [ ] User journeys mapped with pain points
- [ ] HMW statements created for key opportunities
- [ ] Sitemap covers all routes, views, and navigation flows
- [ ] Wireframes exist for all key screens
- [ ] Responsive breakpoints defined (mobile, tablet, desktop)
- [ ] Complete style guide with all tok.* tokens
- [ ] Accessibility requirements defined (WCAG 2.1 AA)
- [ ] Cross-references to backend API specs (be)
- [ ] Cross-references to data dictionary (dict) for events

## Output Format

Generate each document in sequence, ensuring:

1. **ID Consistency:** Use lowercase IDs (per, jour, uxs, tok.color.primary)
2. **Traceability Links:** Reference upstream documents
3. **HMW Evidence:** Show How Might We transformations
4. **Double Diamond Clarity:** Mark phase transitions
5. **Token Authority:** ALL tok.* definitions ONLY in style-guide
6. **No Duplication:** Other docs reference tok.*, don't redefine

## Quality Checks

After generation, validate:

- **Completeness:** All 8 documents generated
- **HMW Applied:** Pain points transformed into opportunities
- **Tokens Defined:** Style guide has complete tok.* system
- **Responsive Design:** Wireframes cover all breakpoints
- **Accessibility:** WCAG 2.1 AA requirements specified
- **Convergence Ready:** Frontend can reference be + dict + sty

## Knowledge Base

This skill references template files in `knowledge/` directory:

- `user-journey.md` - Journey mapping structure
- `uxsm.md` - UX Sitemap (routes, views, and navigation)
- `wireframes.md` - Layout specifications
- `style-guide.md` - Design token system

## Best Practices

1. **Map Reality:** Journey maps should reflect CURRENT state, not desired future
2. **HMW Everything:** Transform every pain point into design opportunity
3. **Sitemap First:** Define all routes and views before wireframing screens
4. **Accessibility by Default:** Not an afterthought - specify from start
5. **Tokens are Sacred:** ONLY define tok.* in style-guide, others reference
6. **Design with Data:** Use actual content, not lorem ipsum
7. **Responsive from Start:** Don't design desktop-first then "make it mobile"

## Common Pitfalls to Avoid

- ❌ Idealized journeys (map what IS, not what SHOULD be)
- ❌ Missing HMW transformation (pain points don't become opportunities)
- ❌ Defining tok.* outside style-guide (breaks single source of truth)
- ❌ Desktop-only wireframes (mobile is critical)
- ❌ Accessibility as afterthought (should be in wireframes/style-guide)
- ❌ Missing sitemap (leads to incomplete navigation)
- ❌ No error states in wireframes (users will hit errors!)
- ❌ Generic HMW statements (too broad or too solution-specific)

## Next Steps After This Skill

After UX chain completes:

1. **Backend Chain (be):** Validate API contracts support UX needs
2. **Data Chain (dict):** Ensure ev.* events and fields are defined
3. **Frontend Implementation:** Use UX outputs to build UI

The UX chain is one of three parallel workstreams in Deliver phase. Orchestrator coordinates convergence at frontend implementation.
