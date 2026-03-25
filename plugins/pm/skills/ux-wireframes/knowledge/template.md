# Wireframes Template

## Responsaveis

- **Owner:** Design Lead
- **Contribuem:** PM, Frontend Dev
- **Aprovacao:** PM + Design Lead

## Table of Contents

1. [Design Notes](#design-notes)
2. [Page: Homepage](#page-homepage)
   - [Wireframe - Desktop](#wireframe---desktop-1024px)
   - [Wireframe - Mobile](#wireframe---mobile-640px)
   - [Component Inventory](#component-inventory)
   - [Interaction Notes](#interaction-notes)
   - [Responsive Behavior](#responsive-behavior)
   - [Accessibility Notes](#accessibility-notes)
3. [Page: Dashboard (/app)](#page-dashboard-app)
   - [Wireframe - Desktop](#wireframe---desktop-1024px-1)
   - [Wireframe - Mobile](#wireframe---mobile-640px-1)
   - [Component Inventory](#component-inventory-1)
   - [Interaction Notes](#interaction-notes-1)
   - [Responsive Behavior](#responsive-behavior-1)
   - [Accessibility Notes](#accessibility-notes-1)
4. [Common Wireframe Patterns](#common-wireframe-patterns)
5. [Implementation Notes](#implementation-notes)

---

## Design Notes

- **Fidelity:** Low — ASCII layouts focused on logical structure
- **Scale:** 1 wireframe = 1 page or complete flow
- **Responsiveness:** Describe mobile/tablet/desktop variations
- **Accessibility:** Include ARIA labels, keyboard navigation, focus states
- **References:** Use tok.* from style-guide for colors/spacing when relevant

---

## Page: Homepage

### Wireframe - Desktop (>1024px)

```
┌────────────────────────────────────────────────────────────────┐
│  Logo              Nav: Product | Blog | Docs    Login | CTA  │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│             ┌─────────────────────────────────────┐             │
│             │    Hero Section                     │             │
│             │  Headline + CTA Button              │             │
│             │  (tok.color.primary background)     │             │
│             └─────────────────────────────────────┘             │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │   Feature 1      │  │   Feature 2      │  │  Feature 3   │ │
│  │   [icon]         │  │   [icon]         │  │  [icon]      │ │
│  │   Description    │  │   Description    │  │  Description │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  CTA Section: Get Started Free                       │    │
│  │  [Primary Button] [Secondary Button]                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│  Footer: Links | Social | Newsletter                           │
└────────────────────────────────────────────────────────────────┘
```

### Wireframe - Mobile (<640px)

```
┌────────────────────┐
│ ☰  Logo   👤  │
├────────────────────┤
│                │
│  Hero          │
│  Headline +    │
│  [CTA Button]  │
│                │
├────────────────────┤
│ Feature 1      │
│ [icon]         │
│ Description    │
├────────────────────┤
│ Feature 2      │
│ [icon]         │
│ Description    │
├────────────────────┤
│ Feature 3      │
│ [icon]         │
│ Description    │
├────────────────────┤
│  [CTA Button]  │
│   Get Started   │
├────────────────────┤
│ Footer links   │
└────────────────────┘
```

### Component Inventory

| Component | Type | Responsibility | States |
|-----------|------|------------------|---------|
| Header | Navigation | Logo, main nav, auth buttons | Default, sticky on scroll |
| Hero | Section | Headline, subheading, CTA | Default |
| Features Grid | Section | 3 feature cards in row | Desktop 3-col, Mobile 1-col |
| Feature Card | Component | Icon, title, description | Hover (lift), Default |
| CTA Section | Section | Call-to-action with buttons | Default |
| Footer | Navigation | Links, social, newsletter | Default |

### Interaction Notes

**Header**
- Logo: `onclick` → navigate to home
- Nav links: `onclick` → navigate to page (smooth scroll if anchor)
- Login: `onclick` → modal login dialog
- CTA button: `onclick` → scroll to pricing / navigate to signup
- Sticky: `onscroll` → header pins when scrolled 100px
- Mobile: `onclick` hamburger → drawer nav slides from left

**Hero Section**
- CTA Button: `onclick` → navigate to /signup
- Button: `onhover` → background darken, shadow increase
- Headline: `onload` → fade-in animation (200ms)

**Feature Cards**
- Card: `onhover` → translateY(-4px), shadow increase (tok.shadow.md)
- Card: `onclick` → navigate to /product#[feature-id]
- Icon: animated SVG on hover (optional, PRD-F-1)

**CTA Section**
- Primary button: `onclick` → navigate to /signup
- Secondary button: `onclick` → scroll to docs
- Buttons: `onhover` → state change (background, text color)

### Responsive Behavior

| Breakpoint | Change | Note |
|-----------|---------|------|
| **Mobile** (<640px) | Stack vertical, full width | Hero text smaller (h2 → h3) |
| **Tablet** (640-1024px) | Hero side-by-side image, features 2-col | Nav expands from hamburger |
| **Desktop** (>1024px) | Hero image right, features 3-col | Standard layout |

### Accessibility Notes

```
ARIA Labels:
- <nav aria-label="Main navigation">
- <button aria-label="Open menu">☰</button>
- <section aria-label="Hero section">
- <section aria-label="Feature highlights">
- <button aria-label="Get started for free">CTA</button>

Keyboard Navigation:
- Tab through: Logo → Nav links → CTA button → Footer links
- Enter: Activate buttons, follow links
- Escape: Close mobile menu if open

Focus States:
- All buttons: 2px outline (tok.color.primary)
- All links: underline or background highlight
- Focus visible on mobile and desktop

Color Contrast:
- Headline: #000 on white (21:1)
- Body text: #444 on white (10:1)
- CTA button: white on tok.color.primary (4.5:1)
```

---

## Page: Dashboard (/app)

### Wireframe - Desktop (>1024px)

```
┌──────────────────────────────────────────────────────┐
│  Logo  [Sidebar Toggle]     User Avatar | Settings   │
├─────────┬────────────────────────────────────────────┤
│ ┌─────┐ │ ┌───────────────────────────────────────┐ │
│ │ D   │ │ │  Dashboard                  [Filters] │ │
│ │ A   │ │ │ ┌──────────┬──────────┬──────────┐   │ │
│ │ S   │ │ │ │ Stat 1   │ Stat 2   │ Stat 3   │   │ │
│ │ H   │ │ │ │ [value]  │ [value]  │ [value]  │   │ │
│ │     │ │ │ └──────────┴──────────┴──────────┘   │ │
│ │ [1] │ │ │                                       │ │
│ │ [2] │ │ │ ┌───────────────────────────────────┐ │ │
│ │ [3] │ │ │ │  Chart / Graph                    │ │ │
│ │     │ │ │ │  [visualization]                  │ │ │
│ │ S   │ │ │ └───────────────────────────────────┘ │ │
│ │ E   │ │ │                                       │ │
│ │ T   │ │ │ ┌───────────────────────────────────┐ │ │
│ │     │ │ │ │  Recent Items / Activity          │ │ │
│ │ [⚙] │ │ │ │  [table or list]                  │ │ │
│ └─────┘ │ └───────────────────────────────────────┘ │
│         │                                           │
└─────────┴───────────────────────────────────────────┘
```

### Wireframe - Mobile (<640px)

```
┌──────────────────────┐
│ ☰ Dashboard     👤   │
├──────────────────────┤
│ ┌──────┬──────┬──┐   │
│ │ S1   │ S2   │S3│   │
│ │ [v]  │ [v]  │[v]│   │
│ └──────┴──────┴──┘   │
├──────────────────────┤
│ Chart                │
│ [visualization]      │
├──────────────────────┤
│ Recent Items         │
│ [item 1]             │
│ [item 2]             │
│ [item 3]             │
├──────────────────────┤
│ ≡ Menu               │
│  Feature 1           │
│  Feature 2           │
│  Reports             │
│  Settings            │
└──────────────────────┘
```

### Component Inventory

| Component | Type | Responsibility | States |
|-----------|------|------------------|---------|
| Sidebar | Navigation | Main menu, quick access | Visible/Collapsed |
| Header | Navigation | Breadcrumb, user menu | Default |
| Stat Cards | Display | KPI values, trends | Default, Loading |
| Chart | Display | Data visualization | Default, Loading, Tooltip |
| Activity Table | Display | Recent items, actions | Default, Hover, Sorting |
| FAB | Component | Floating action button | Default, Hover, Active |

### Interaction Notes

**Sidebar**
- Items: `onclick` → navigate to feature
- Items: `hover` → background highlight (tok.color.gray-100)
- Toggle: `onclick` → collapse/expand sidebar (animation 200ms)
- Mobile: Drawer overlay with backdrop
- Keyboard: Tab through items, Enter to activate

**Header**
- Breadcrumb: `onclick` link → navigate
- Avatar: `onclick` → dropdown menu (Profile, Settings, Logout)
- Dropdown: `onkeydown` Escape → close menu
- Dropdown items: `onclick` → navigate or action

**Stats**
- Card: `onhover` → tooltip with explanation
- Card: `onclick` → navigate to detailed view (optional)
- Values: animated counter on page load (1000ms)

**Chart**
- Hover on data point: tooltip appears (description + value)
- Legend items: `onclick` → toggle series visibility
- Responsive: Scales down on mobile, may stack

**Activity Table**
- Rows: `onclick` → detail view / expand row
- Rows: `onhover` → background highlight, action buttons appear
- Sorting: `onclick` column header → sort asc/desc
- Pagination: `onclick` next/prev → load more items
- Mobile: Collapse to card view (not table)

### Responsive Behavior

| Breakpoint | Change | Note |
|-----------|---------|------|
| **Mobile** | Sidebar → bottom nav or drawer | Stats stack 1-col |
| **Tablet** | Sidebar visible, narrower | Stats 2-col |
| **Desktop** | Standard layout | Stats 3-col |

### Accessibility Notes

```
ARIA Labels:
- <nav aria-label="Main sidebar">
- <button aria-expanded="false" aria-controls="sidebar">Toggle menu</button>
- <section aria-label="Key metrics">
- <table role="grid" aria-label="Recent activity">
- <button aria-label="View details">→</button>

Keyboard Navigation:
- Tab: Sidebar items → Header dropdown → Table cells
- Enter: Activate links/buttons
- Arrow keys: Navigate table rows (optional)
- Escape: Close dropdown menus

Focus States:
- All interactive: 2px outline (tok.color.primary)
- Links: underline + outline
- Table cells: border on focus

Screen Reader:
- Stats: "KPI name: value (trend)"
- Chart: "Chart showing [title] with [description]"
- Table: Row announces [name] [status] [actions]
```

---

## Common Wireframe Patterns

### Form Section

```
┌──────────────────────────────────┐
│ Form Title                       │
├──────────────────────────────────┤
│                                  │
│ [Label]                          │
│ [Input field]    [Validation]   │
│                                  │
│ [Label]                          │
│ [Textarea]                       │
│                                  │
│ [Label] [⊙] Option 1             │
│          [⊙] Option 2             │
│          [⊙] Option 3             │
│                                  │
│ [Label]                          │
│ [Dropdown ▼]                     │
│                                  │
│     [Submit Button] [Cancel]     │
│                                  │
└──────────────────────────────────┘
```

### Modal Dialog

```
┌──────────────────────────────────┐
│ Modal Title              [×]     │
├──────────────────────────────────┤
│ Modal content here               │
│                                  │
│     [Primary Action] [Secondary] │
└──────────────────────────────────┘
```

### Card Component

```
┌───────────────────────┐
│ [Image / Icon]        │
├───────────────────────┤
│ Card Title            │
│ Short description     │
│ • Detail 1            │
│ • Detail 2            │
├───────────────────────┤
│ [Action Button]       │
└───────────────────────┘
```

---

## Implementation Notes

- [ ] Validate wireframes with PMs and design team
- [ ] Create interactive prototype (Figma, Adobe XD)
- [ ] Conduct usability testing with wireframes
- [ ] Get feedback before high-fidelity design
- [ ] Document component variations and states
- [ ] Handoff wireframes to design and development

## O que fazer / O que nao fazer

**O que fazer:**
- Incluir wireframe desktop E mobile para cada tela
- Anotar componentes com nome e tokens (tok.*)
- Documentar estados (default, hover, disabled, error, loading)
- Incluir notas de interacao e acessibilidade

**O que nao fazer:**
- Nao adicionar cor ou estilo visual (isso e style-guide)
- Nao omitir responsive behavior
- Nao criar wireframes sem base no ux-sitemap
- Nao ignorar empty states e estados de carregamento

