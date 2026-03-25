---
description: Generate Wireframes with screen layouts and navigation flows
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Wireframes

Creating wireframes for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/design/user-journey.md && echo "✓ user-journey.md exists" || echo "⚠ Missing user journey (recommended to run /user-journey first)"`
!`test -f docs/design/ux-sitemap.md && echo "✓ ux-sitemap.md exists" || echo "⚠ Missing UX sitemap"`

## Setup

!`mkdir -p docs/ux && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/ux-chain/knowledge/wireframes.md

## Interactive Wireframe Creation

I'll help you create wireframe specifications:

### Step 1: Review Design Context

Read user journeys and sitemap:

@docs/design/user-journey.md
@docs/design/ux-sitemap.md

### Step 2: Screen Inventory

**Ask the user:**

What screens/views need wireframes?

**Organize by user journey:**

#### Onboarding Journey
- Landing page
- Sign up page
- Welcome/onboarding wizard
- Dashboard (first view)

#### Core Task Journey
- List/index view (invoices, clients, etc.)
- Detail view
- Create/edit form
- Confirmation page

#### Supporting Screens
- Settings page
- Profile page
- Help/support page
- Error pages (404, 500)

[List all screens that need wireframing]

### Step 3: Wireframe Details (Per Screen)

**For each screen, document:**

#### Screen Purpose
- What is this screen for?
- Where does it fit in user journey?
- What user goal does it serve?

#### Layout Structure
- Header (logo, nav, user menu)
- Main content area
- Sidebar (if any)
- Footer

#### Content Blocks
- What sections/regions on page?
- Content hierarchy (most to least important)
- Visual weight (what stands out)

#### Components Used
- Which components from DRD?
- Layout: Grid, flex, fixed positioning
- Spacing: tok.spacing.* values

#### Data Displayed
- What data is shown?
- Data source (API endpoints, local state)
- Empty states (when no data)
- Loading states (while fetching)
- Error states (when fetch fails)

#### User Actions
- What can user do on this screen?
- Primary action (main CTA)
- Secondary actions
- Destructive actions
- Navigation options

#### Responsive Behavior
- Mobile layout (< 640px)
- Tablet layout (641-1024px)
- Desktop layout (> 1024px)
- What changes per breakpoint?

**Example wireframe spec:**

```
Screen: Invoice List (Dashboard)

Purpose: Show all invoices, allow creation and filtering

Layout Structure:
┌─────────────────────────────────────────┐
│ Header (logo, nav, search, user menu)  │
├──────┬──────────────────────────────────┤
│ Side │ Main Content                     │
│ Nav  │ ┌──────────────────────────────┐ │
│      │ │ Page Header                  │ │
│      │ │ "Invoices" + "New Invoice"   │ │
│      │ ├──────────────────────────────┤ │
│      │ │ Filters (status, date range) │ │
│      │ ├──────────────────────────────┤ │
│      │ │ Invoice Table               │ │
│      │ │ [ID | Client | Total | Date]│ │
│      │ │ [Row 1]                     │ │
│      │ │ [Row 2]                     │ │
│      │ │ [Row 3]                     │ │
│      │ ├──────────────────────────────┤ │
│      │ │ Pagination                  │ │
│      │ └──────────────────────────────┘ │
└──────┴──────────────────────────────────┘

Content Blocks:
1. Page header (Invoice count + CTA)
2. Filter bar (status dropdown, date picker)
3. Data table (sortable columns)
4. Pagination controls

Components Used:
- Button (Primary): "New Invoice" CTA
- DataTable: Invoice listing
- Select: Status filter
- DatePicker: Date range
- Pagination: Page controls

Data Displayed:
- Invoice list from GET /api/invoices
- Columns: invoice_id, client_name, total_amount, created_at, status
- Empty state: "No invoices yet. Create your first invoice!"
- Loading: Skeleton rows
- Error: "Failed to load invoices. Retry?"

User Actions:
- Primary: Click "New Invoice" → Create invoice form
- Secondary: Click invoice row → Invoice detail page
- Filter: Select status, date range → Refetch filtered results
- Sort: Click column header → Re-sort table
- Navigate: Click page number → Load page

Responsive:
- Mobile (< 640px):
  - Hide sidebar (hamburger menu)
  - Stack filters vertically
  - Card view instead of table
  - Fewer columns visible
- Tablet (641-1024px):
  - Sidebar collapses to icons only
  - Table with fewer columns
  - Filters in row
- Desktop (> 1024px):
  - Full layout as shown
  - All columns visible
  - Sidebar expanded
```

[Document wireframes for all screens]

### Step 4: Navigation Flows

**Document navigation between screens:**

```
Landing Page
  ├─→ Sign Up → Onboarding → Dashboard
  └─→ Log In → Dashboard

Dashboard
  ├─→ New Invoice → Invoice Form
  │                    └─→ Save → Invoice Detail → Dashboard
  ├─→ Invoice Row → Invoice Detail
  │                    ├─→ Edit → Invoice Form
  │                    └─→ Delete → Dashboard
  └─→ Clients → Client List
                   └─→ Client Detail
```

### Step 5: Annotations

**For each wireframe, add:**

1. **Interaction notes**: Click, hover, drag behaviors
2. **Content notes**: Placeholder vs real content
3. **Design notes**: Visual emphasis, attention flow
4. **Technical notes**: Performance considerations, data loading
5. **Accessibility notes**: Focus order, ARIA labels needed

### Step 6: Confirm Wireframes

"Here are the wireframes:

**Screens Documented:** 12 screens

**Key Wireframes:**
1. Dashboard: Invoice table + filters + CTA
2. Invoice Form: Multi-step form with validation
3. Invoice Detail: View/edit/delete/send actions
4. Client List: Table with search and filters
[etc.]

**Navigation Flow:**
[ASCII flow diagram]

Do these wireframes cover all user journeys and actions?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/wireframes.md`.

**Document Structure:**
- Screen Inventory (all screens listed)
- For each screen:
  - Screen name and purpose
  - User journey context
  - Layout structure (ASCII diagram)
  - Content blocks (prioritized list)
  - Components used (from DRD)
  - Data displayed (sources, states)
  - User actions (primary, secondary, navigation)
  - Responsive behavior (mobile, tablet, desktop)
  - Interaction annotations
  - Accessibility notes
  - Technical notes
- Navigation Flows (screen transitions)
- State Transitions (which screens in which UI states)

## Validation

After generation:

!`test -f docs/design/wireframes.md && echo "✓ wireframes.md created" || echo "✗ Generation failed"`

**Wireframes checklist**:
!`if [ -f docs/design/wireframes.md ]; then
  grep -ci "screen\|page\|view" docs/design/wireframes.md | xargs echo "Screens wireframed:"
  grep -ci "component\|button\|table\|form" docs/design/wireframes.md | xargs echo "Component references:"
  grep -ci "mobile\|tablet\|desktop\|responsive" docs/design/wireframes.md | xargs echo "Responsive considerations:"
fi`

## Next Steps

**Create style guide**:
```
/style-guide
```

**Create style guide**:
```
/style-guide
```

**Validate implementation readiness**:
```
/validate-gate implementation-readiness
```

---

**Wireframes generated!** Screen layouts, navigation flows, and interaction details documented.
