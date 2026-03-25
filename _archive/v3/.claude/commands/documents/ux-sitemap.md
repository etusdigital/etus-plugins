---
description: Generate UX Sitemap documenting routes, views, and navigation structure
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate UX Sitemap

Creating UX sitemap for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/design/user-journey.md && echo "✓ user-journey.md exists" || echo "⚠ Missing user journey (recommended to run /user-journey first)"`

## Setup

!`mkdir -p docs/ux && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/ux-chain/knowledge/uxsm.md

## Interactive Sitemap Design

I'll help you design your application's sitemap (routes, views, and navigation):

### Step 1: Identify Key Routes

**Ask the user:**

What are the main routes/pages in your application?

**Typical route categories:**
- Public routes (landing, login, signup)
- Dashboard/home routes
- Feature-specific routes (billing, settings, etc.)
- Detail/nested routes (e.g., /invoices/:id)
- Modal/drawer routes

[List all primary routes with hierarchy]

### Step 2: Define Route Inventory

**For each route, document:**

1. **route_id**: `r:/path/to/route` (e.g., `r:/billing/invoices`)
2. **name**: Human-readable name
3. **parent**: Parent route for breadcrumbs
4. **auth_guard**: `public | user | admin | role:<name>`
5. **feature_flag**: Optional feature flag
6. **params**: Route parameters (e.g., `:invoiceId (uuid)`)
7. **redirect_from**: Legacy URLs if applicable

**Example:**
- `r:/billing/invoices` - Invoices list (parent: `r:/billing`, auth: `user`)
- `r:/billing/invoices/:invoiceId` - Invoice detail (parent: `r:/billing/invoices`, auth: `user`)

### Step 3: Define View Inventory

**For each view, document:**

1. **view_id**: `view.<domain>.<page>` (e.g., `view.billing.invoices-list`)
2. **type**: `page | modal | drawer | layout | partial`
3. **route_id**: Associated route
4. **priority**: `P0 | P1 | P2`
5. **stories**: User story IDs (US-#)
6. **apis**: Backend endpoints used
7. **events**: Analytics events (ev.*)
8. **components**: UI components used (cmp.*)

**Example:**
- `view.billing.invoices-list` (page, `r:/billing/invoices`, P0)
  - Stories: US-7, US-9
  - APIs: GET /api/v1/invoices
  - Events: ev.invoice.list
  - Components: cmp.table.data-grid, cmp.search.bar

### Step 4: Define Required UI States

**For each view, identify required UI states:**

**Standard states:**
- `#default` - Normal display state
- `#loading` - Data loading
- `#empty` - No data to display
- `#error` - Error occurred
- `#success` - Operation succeeded

**Example:**
- `view.billing.invoices-list`: #default, #loading, #empty, #error
- `view.auth.login`: #default, #loading, #error

### Step 5: Navigation Graph

**Map key navigation flows:**

What are the primary navigation paths between routes?

**Example navigation edges:**
- `r:/auth/login` —(success)→ `r:/dashboard`
- `r:/dashboard` —(billing link)→ `r:/billing/invoices`
- `r:/billing/invoices` —(row click)→ `r:/billing/invoices/:invoiceId`
- `r:/billing/invoices/:invoiceId` ↔ (open/close) `view.billing.invoice-send`

[Document all critical navigation paths with triggers]

### Step 6: Traceability Mapping

**Map journey steps to routes and views:**

For each key journey step:
- Journey step (from user-journey.md)
- Associated route_id
- Associated view_id
- User stories (US-#)
- Primary API endpoint

**Example:**
- J1: Login → `r:/auth/login` → `view.auth.login` → US-2 → POST /api/v1/auth/login

### Step 7: Confirm Sitemap

"Here's the sitemap structure:

**Routes (6):**
- r:/ (Home, public)
- r:/auth/login (Login, public)
- r:/dashboard (Dashboard, user)
- r:/billing/invoices (Invoices list, user)
- r:/billing/invoices/:invoiceId (Invoice detail, user)
- r:/settings/profile (Profile, user)

**Views (6):**
- view.auth.login (page, P0)
- view.dashboard.home (page, P0)
- view.billing.invoices-list (page, P0)
- view.billing.invoice-detail (page, P0)
- view.billing.invoice-send (modal, P1)
- view.settings.profile (page, P1)

**Navigation:**
- Login success → Dashboard
- Dashboard → Invoices list
- Invoices list → Invoice detail
- Invoice detail ↔ Send modal

Does this sitemap capture all routes, views, and navigation flows?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/uxsm.md` (UX Sitemap).

**Document Structure:**
- Route Inventory (all routes with auth guards, params)
- View Inventory (all views with stories, APIs, events, components)
- Required UI States per View
- Navigation Graph (high-level flow)
- Traceability (journey → route → view → stories → API)
- Rules & Lint (ID format validation)
- Cross-references (how other docs use this)
- AI Extraction Markers (machine-readable YAML)

## Validation

After generation:

!`test -f docs/design/uxsm.md && echo "✓ uxsm.md created" || echo "✗ Generation failed"`

**Sitemap checklist**:
!`if [ -f docs/design/uxsm.md ]; then
  grep -ci "route_id\|view_id" docs/design/uxsm.md | xargs echo "Routes and views:"
  grep -ci "auth_guard\|public\|user" docs/design/uxsm.md | xargs echo "Auth guards:"
  grep -ci "navigation\|trigger" docs/design/uxsm.md | xargs echo "Navigation flows:"
fi`

## Next Steps

**Create wireframes**:
```
/wireframes
```

**Create design requirements**:
```
/design-requirements
```

Or run complete UX chain:
```
/ux-docs
```

---

**UX sitemap generated!** Routes, views, and navigation structure documented.
