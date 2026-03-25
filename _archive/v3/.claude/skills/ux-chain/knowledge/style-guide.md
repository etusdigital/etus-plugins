---
doc_meta:
  id: sty
  display_name: Style Guide
  pillar: Design
  owner_role: Design Lead
  summary: Defines visual tokens, accessibility rules, and cross-platform styling
    standards.
  order: 23
  gate: design
  requires:
  - des
  - wire
  optional: []
  feeds:
  - fe
uuid: <UUID>
version: 0.1.0
status: Draft
owners:
- <owner>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- Style
- Tokens
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Solo Style Guide - [Product Name]

## Problem Context

**Design Requirements:** See des (Design Requirements) for validated design problem analysis.
**Component Specifications:** See wire (Wireframes) for component requirements.
**User Context:** See jour (User Journey) for interaction moments.

## Scope Guard

- **Owns:** Complete design token system, atomic component specifications, primitive UI definitions, implementation patterns
- **Not included here:** Page layouts (see wire), component usage contexts (see des), feature behaviors (see stor)
- **Cross-references:** Links to des for component context, wire for layout integration

## 🎨 Design System Foundation

**Product Name:** [Your tool/app name]
**Design System Architecture:** [Selected atomic design approach with rationale]
**Token Strategy:** [Chosen token naming convention and hierarchy structure]
**Component Philosophy:** [Primitive-based, utility-first, or hybrid approach with reasoning]

## 🌈 Complete Design Token System

### Sub-Atomic Core Tokens

**Global Brand Foundation:**

- **core-primary-500:** `#[hex]` - Brand primary base
- **core-primary-[100-900]:** `#[hex]` - Complete primary scale
- **core-neutral-[50-950]:** `#[hex]` - Complete neutral scale
- **core-semantic-success:** `#[hex]` - Success base
- **core-semantic-warning:** `#[hex]` - Warning base
- **core-semantic-error:** `#[hex]` - Error base
- **core-semantic-info:** `#[hex]` - Info base

> **Developer Context**: Primary colors establish brand recognition and user trust. Semantic colors provide instant feedback reducing cognitive load during user tasks. Use primary for CTAs, semantic for system feedback.

### Semantic Color Tokens

**Context-Aware Color Decisions:**

- **color-text-primary:** `var(--core-neutral-900)` - Primary text content
- **color-text-secondary:** `var(--core-neutral-700)` - Secondary text content
- **color-text-muted:** `var(--core-neutral-500)` - Muted text content
- **color-background-primary:** `var(--core-neutral-50)` - Primary background
- **color-background-elevated:** `var(--core-neutral-0)` - Card/modal backgrounds
- **color-border-default:** `var(--core-neutral-200)` - Default borders
- **color-border-focus:** `var(--core-primary-500)` - Focus states
- **color-action-primary:** `var(--core-primary-500)` - Primary actions
- **color-action-primary-hover:** `var(--core-primary-600)` - Primary hover states
- **color-feedback-success:** `var(--core-semantic-success)` - Success states
- **color-feedback-error:** `var(--core-semantic-error)` - Error states

### Component-Specific Color Tokens

**Atomic Component Color Specifications:**

- **button-primary-bg:** `var(--color-action-primary)` - Primary button background
- **button-primary-text:** `var(--core-neutral-0)` - Primary button text
- **button-secondary-bg:** `transparent` - Secondary button background
- **button-secondary-border:** `var(--color-action-primary)` - Secondary button border
- **input-bg:** `var(--color-background-elevated)` - Input field background
- **input-border:** `var(--color-border-default)` - Input field border
- **input-border-focus:** `var(--color-border-focus)` - Input focus border

## ✏️ Complete Typography Token System

### Typography Foundation Tokens

**Font Family Core Tokens:**

- **font-family-primary:** `[Selected font stack with fallbacks and rationale]`
- **font-family-monospace:** `[Selected monospace stack with fallbacks and rationale]`

**Font Weight Core Tokens:**

- **font-weight-light:** `300` - Light emphasis
- **font-weight-regular:** `400` - Regular content
- **font-weight-medium:** `500` - Medium emphasis
- **font-weight-semibold:** `600` - Strong emphasis
- **font-weight-bold:** `700` - Bold emphasis

> **MVP Priority**: Start with font-weight-regular and font-weight-semibold for 80% of use cases. Add others as interface complexity grows. Typography hierarchy directly impacts user ability to scan and process information.

**Font Size Core Tokens:**

- **font-size-xs:** `0.75rem` (12px) - Micro text
- **font-size-sm:** `0.875rem` (14px) - Small text
- **font-size-base:** `1rem` (16px) - Base text
- **font-size-lg:** `1.125rem` (18px) - Large text
- **font-size-xl:** `1.25rem` (20px) - Extra large
- **font-size-2xl:** `1.5rem` (24px) - Heading small
- **font-size-3xl:** `1.875rem` (30px) - Heading medium
- **font-size-4xl:** `2.25rem` (36px) - Heading large

**Line Height Core Tokens:**

- **line-height-tight:** `1.25` - Tight spacing
- **line-height-normal:** `1.5` - Normal spacing
- **line-height-relaxed:** `1.75` - Relaxed spacing

### Semantic Typography Tokens

**Context-Aware Typography Decisions:**

- **typography-heading-1:** `var(--font-size-4xl)/var(--line-height-tight) var(--font-weight-bold)`
- **typography-heading-2:** `var(--font-size-3xl)/var(--line-height-tight) var(--font-weight-semibold)`
- **typography-heading-3:** `var(--font-size-2xl)/var(--line-height-normal) var(--font-weight-semibold)`
- **typography-body-large:** `var(--font-size-lg)/var(--line-height-relaxed) var(--font-weight-regular)`
- **typography-body:** `var(--font-size-base)/var(--line-height-normal) var(--font-weight-regular)`
- **typography-body-small:** `var(--font-size-sm)/var(--line-height-normal) var(--font-weight-regular)`
- **typography-caption:** `var(--font-size-xs)/var(--line-height-tight) var(--font-weight-medium)`

## 📏 Complete Spatial Token System

### Spacing Foundation Tokens

**Mathematical Spacing Scale:**

- **space-px:** `1px` - Pixel precision
- **space-0:** `0` - No space
- **space-1:** `0.25rem` (4px) - Micro spacing
- **space-2:** `0.5rem` (8px) - Small spacing
- **space-3:** `0.75rem` (12px) - Medium-small
- **space-4:** `1rem` (16px) - Medium spacing **(P0: Critical for MVP)**
- **space-5:** `1.25rem` (20px) - Medium-large
- **space-6:** `1.5rem` (24px) - Large spacing **(P0: Critical for MVP)**
- **space-8:** `2rem` (32px) - Extra large **(P1: Important)**
- **space-10:** `2.5rem` (40px) - Section spacing
- **space-12:** `3rem` (48px) - Large section
- **space-16:** `4rem` (64px) - Page spacing

> **User Impact**: Consistent spacing reduces cognitive load and creates visual rhythm. Start with space-4 and space-6 for 90% of layouts. Poor spacing is the #1 cause of "unprofessional" perception.

### Semantic Spacing Tokens

**Context-Aware Spacing Decisions:**

- **spacing-component-padding-sm:** `var(--space-2)` - Small component internal padding
- **spacing-component-padding:** `var(--space-4)` - Default component internal padding
- **spacing-component-padding-lg:** `var(--space-6)` - Large component internal padding
- **spacing-component-gap:** `var(--space-4)` - Gap between related components
- **spacing-section-gap:** `var(--space-8)` - Gap between sections
- **spacing-page-margin:** `var(--space-6)` - Page edge margins

### Layout System Tokens

**Grid and Container Specifications:**

- **layout-container-sm:** `640px` - Small container max-width
- **layout-container-md:** `768px` - Medium container max-width
- **layout-container-lg:** `1024px` - Large container max-width
- **layout-container-xl:** `1280px` - Extra large container max-width
- **layout-grid-columns:** `12` - Grid column count
- **layout-grid-gap:** `var(--space-6)` - Grid gutter size

### Border Radius & Shadow Tokens

**Visual Enhancement Tokens:**

- **radius-sm:** `0.125rem` (2px) - Small radius
- **radius:** `0.25rem` (4px) - Default radius
- **radius-md:** `0.375rem` (6px) - Medium radius
- **radius-lg:** `0.5rem` (8px) - Large radius
- **radius-xl:** `0.75rem` (12px) - Extra large radius
- **shadow-sm:** `0 1px 2px rgba(0,0,0,0.05)` - Small shadow
- **shadow:** `0 1px 3px rgba(0,0,0,0.1)` - Default shadow
- **shadow-md:** `0 4px 6px rgba(0,0,0,0.1)` - Medium shadow
- **shadow-lg:** `0 10px 15px rgba(0,0,0,0.1)` - Large shadow

## 🧩 Complete Atomic Component System

### Atomic Design Hierarchy

**Atoms - Foundational UI Building Blocks:**

#### Button Atom Specifications

**Primary Button:** **(P0: Critical for MVP)**

- **Background:** `var(--button-primary-bg)`
- **Text:** `var(--button-primary-text)`
- **Padding:** `var(--spacing-component-padding) var(--space-6)`
- **Border Radius:** `var(--radius-md)`
- **Typography:** `var(--typography-body) var(--font-weight-medium)`
- **States:** Default, Hover (+darken 10%), Active (+darken 15%), Disabled (50% opacity), Loading (with spinner)

> **Why This Matters**: Primary buttons drive key user actions. Consistent styling builds user confidence and reduces decision fatigue. Start with Default and Hover states for MVP.

**Secondary Button:**

- **Background:** `transparent`
- **Text:** `var(--color-action-primary)`
- **Border:** `1px solid var(--button-secondary-border)`
- **States:** Default, Hover (bg: primary-50), Active (bg: primary-100), Disabled, Loading

**Icon Button:**

- **Size:** `var(--space-10) × var(--space-10)`
- **Icon Size:** `var(--space-5)`
- **Padding:** `var(--space-2)`
- **Border Radius:** `var(--radius)`

#### Input Atom Specifications

**Text Input:** **(P0: Critical for MVP)**

- **Background:** `var(--input-bg)`
- **Border:** `1px solid var(--input-border)`
- **Border Radius:** `var(--radius)`
- **Padding:** `var(--space-3) var(--space-4)`
- **Typography:** `var(--typography-body)`
- **States:** Default, Focus (border: focus-color + shadow), Error (border: error-color), Disabled (opacity: 60%)

> **User Journey Impact**: Input fields are critical touchpoints in user tasks. Focus states provide immediate feedback, Error states guide users to success. Prioritize Default, Focus, and Error states for MVP.

### Molecules - Component Combinations

**Form Field Molecule:**

- **Composition:** Label Atom + Input Atom + Help Text Atom + Error Message Atom
- **Spacing:** `var(--space-2)` between elements
- **Layout:** Vertical stack

**Search Bar Molecule:**

- **Composition:** Icon Atom + Input Atom + Button Atom
- **Layout:** Horizontal flex with input flex-grow

### Organisms - Complex Components

**Form Organism:**

- **Composition:** Multiple Form Field Molecules + Button Atoms
- **Spacing:** `var(--spacing-component-gap)` between fields
- **Layout:** Vertical stack with submit actions at bottom

**Card Organism:**

- **Background:** `var(--color-background-elevated)`
- **Border:** `1px solid var(--color-border-default)`
- **Border Radius:** `var(--radius-lg)`
- **Padding:** `var(--spacing-component-padding-lg)`
- **Shadow:** `var(--shadow)`
- **Composition:** Header + Content + Footer sections

## 🖼️ Complete Visual Asset System

### Icon System Tokens

**Selected Icon Library:** [Chosen library with selection rationale]
**Icon Style Strategy:** [Outline/solid/duotone with consistency rationale]

**Icon Size Tokens:**

- **icon-size-xs:** `var(--space-3)` (12px) - Micro icons
- **icon-size-sm:** `var(--space-4)` (16px) - Small icons, inline with text
- **icon-size:** `var(--space-5)` (20px) - Default icon size
- **icon-size-md:** `var(--space-6)` (24px) - Medium icons, buttons
- **icon-size-lg:** `var(--space-8)` (32px) - Large icons, prominent display
- **icon-size-xl:** `var(--space-10)` (40px) - Extra large icons

**Icon Semantic Tokens:**

- **icon-color-primary:** `var(--color-text-primary)` - Primary icon color
- **icon-color-secondary:** `var(--color-text-secondary)` - Secondary icon color
- **icon-color-muted:** `var(--color-text-muted)` - Muted icon color
- **icon-color-interactive:** `var(--color-action-primary)` - Interactive icon color
- **icon-stroke-width:** `1.5px` - Consistent stroke width

### Image & Media Tokens

**Aspect Ratio System:**

- **aspect-square:** `1/1` - Profile images, avatars
- **aspect-video:** `16/9` - Video content, hero images
- **aspect-card:** `4/3` - Card images, thumbnails
- **aspect-banner:** `3/1` - Banner images, headers

**Image Size Tokens:**

- **image-size-avatar-sm:** `var(--space-8)` - Small avatar
- **image-size-avatar:** `var(--space-10)` - Default avatar
- **image-size-avatar-lg:** `var(--space-12)` - Large avatar
- **image-size-thumbnail:** `var(--space-16)` - Thumbnail size

## 🎭 Animation & Interaction Tokens

### Animation Duration Tokens **(P2: Enhancement)**

**Timing System:**

- **duration-fast:** `150ms` - Micro-interactions, hover states
- **duration:** `200ms` - Standard transitions
- **duration-slow:** `300ms` - Complex transitions, modals
- **duration-slower:** `500ms` - Page transitions, large animations

> **Implementation Note**: Add animations after core functionality is solid. Users prioritize working features over polish. Start with duration-fast for hover states when ready.

### Animation Easing Tokens

**Easing Curves:**

- **ease-linear:** `linear` - Consistent motion
- **ease-out:** `cubic-bezier(0, 0, 0.2, 1)` - Natural deceleration
- **ease-in:** `cubic-bezier(0.4, 0, 1, 1)` - Natural acceleration
- **ease-in-out:** `cubic-bezier(0.4, 0, 0.2, 1)` - Natural motion
- **ease-bounce:** `cubic-bezier(0.68, -0.55, 0.265, 1.55)` - Playful motion

### Interaction State Tokens

**State Transition Specifications:**

- **transition-default:** `all var(--duration) var(--ease-out)` - Default transitions
- **transition-transform:** `transform var(--duration) var(--ease-out)` - Transform transitions
- **transition-opacity:** `opacity var(--duration-fast) var(--ease-linear)` - Opacity transitions
- **transition-colors:** `color, background-color, border-color var(--duration) var(--ease-out)` - Color transitions

## ♿ Accessibility Token Integration **(P1: Important)**

### Accessibility Compliance Tokens

**Color Contrast Standards:**

- **contrast-ratio-normal:** `4.5:1` - Normal text minimum
- **contrast-ratio-large:** `3:1` - Large text minimum
- **contrast-ratio-ui:** `3:1` - UI elements minimum
- All color tokens maintain required contrast ratios

**Interactive Element Standards:**

- **touch-target-min:** `44px` - Minimum touch target size
- **focus-outline-width:** `2px` - Focus indicator width
- **focus-outline-offset:** `2px` - Focus indicator offset
- **focus-outline-color:** `var(--color-border-focus)` - Focus indicator color

> **Why Critical**: Accessibility isn't optional - it's good UX for everyone. Focus indicators help all users navigate efficiently. Touch targets prevent user frustration on mobile.

**Motion & Animation Accessibility:**

- **reduced-motion:** `@media (prefers-reduced-motion: reduce)` - Respect user preferences
- All animation tokens respect reduced-motion preferences

## 📱 Responsive Design Token System

### Breakpoint Foundation Tokens

**Responsive Breakpoint System:**

- **breakpoint-xs:** `475px` - Extra small devices
- **breakpoint-sm:** `640px` - Small devices
- **breakpoint-md:** `768px` - Medium devices
- **breakpoint-lg:** `1024px` - Large devices
- **breakpoint-xl:** `1280px` - Extra large devices
- **breakpoint-2xl:** `1536px` - 2X large devices

### Device-Specific Token Adaptations

**Touch Interface Tokens:**

- **touch-target-mobile:** `44px` - Mobile touch targets
- **touch-spacing-mobile:** `var(--space-4)` - Mobile touch spacing
- **font-size-mobile-adjust:** `16px` - Mobile font size minimum (prevents zoom)

**Desktop Enhancement Tokens:**

- **hover-enabled:** `@media (hover: hover)` - Hover capability detection
- **focus-visible-enabled:** `:focus-visible` - Keyboard focus detection
- **cursor-pointer:** `pointer` - Interactive cursor state

## 🔧 Implementation Architecture

### Technology-Agnostic Token Export

**CSS Variables Implementation:**

```css
:root {
	/* Core Tokens */
	--core-primary-500: #[hex];
	--space-4: 1rem;
	--font-size-base: 1rem;

	/* Semantic Tokens */
	--color-text-primary: var(--core-neutral-900);
	--typography-body: var(--font-size-base) / var(--line-height-normal);
	--spacing-component-padding: var(--space-4);
}
```

**JSON Token Export:**

```json
{
	"color": {
		"core": {
			"primary": {
				"500": "#[hex]"
			}
		},
		"semantic": {
			"text": {
				"primary": "{color.core.neutral.900}"
			}
		}
	}
}
```

### Framework Integration Patterns

**Implementation Strategy:** [Selected approach - CSS Variables, Styled-Components, Tailwind, etc. with rationale]
**Component Library Integration:** [Chosen component system with token mapping strategy]
**Build Process:** [Token compilation and distribution approach]

## Validation & Discovery Checkpoints

### Design System Validation Process

**User Testing Checkpoints:**

- Test color accessibility with real users (especially color-blind users)
- Validate touch target sizes on actual devices
- Confirm typography readability across age groups
- Measure task completion time with consistent vs. inconsistent spacing

**Developer Feedback Collection:**

- Weekly check: Are design tokens being used correctly?
- Monthly review: Which tokens are unused (candidates for removal)?
- Quarterly assessment: What new tokens are needed based on feature development?

**Iteration Triggers:**

- User complaint about visual inconsistency → Review token usage
- Developer creating custom styles → Missing token identified
- Low task completion rates → Review interaction design tokens
- Accessibility audit failure → Update compliance tokens

## 🔄 Design System Integration

### Cross-Template References

**des Integration:**

- All design tokens support requirements defined in design specifications
- Component tokens align with spatial layout analysis and interaction patterns

**wire Integration:**

- Layout tokens provide foundation for wireframe implementation
- Spacing and sizing tokens support all identified UI patterns

**stor Integration:**

- Design tokens map to specific user journey moments
- Component states support identified user task flows
- Visual hierarchy tokens align with user story priorities

### Discovery-Driven Implementation Roadmap

**Phase 1 - Foundation (Week 1):**

- P0 tokens: Core colors, basic typography, primary spacing
- Test with one key user flow before proceeding

**Phase 2 - Components (Week 2-3):**

- P1 tokens: Form components, feedback states, basic responsive
- Validate with developer team for implementation ease

**Phase 3 - Enhancement (Week 4+):**

- P2 tokens: Animations, advanced states, full accessibility
- Add based on user feedback and feature development needs

### Token Governance

**Version Control:** Semantic versioning for token changes
**Breaking Changes:** Color value updates, spacing scale modifications
**Non-Breaking Changes:** New token additions, semantic token updates
**Documentation:** All tokens include usage guidelines and implementation examples

## Bridge to Implementation

### Next Steps After Style Guide

**Immediate Actions:**

1. **Create User Stories** - Connect design tokens to specific user tasks and pain points
2. **Validate with Wireframes** - Ensure tokens support identified interaction patterns
3. **Implement MVP Tokens** - Start with P0 tokens, test with real users

**Success Metrics:**

- Developer velocity: Time to implement consistent designs
- User satisfaction: Perceived professionalism and ease of use
- Maintenance cost: Reduced design decision overhead
- Consistency score: Automated token usage compliance

**Warning Signs:**

- Developers creating custom styles instead of using tokens
- Users reporting interface feels "cheap" or "inconsistent"
- Long implementation time for simple design changes

---

- Token semantic naming provides clear context for usage and prevents misuse
- Validate design assumptions through user testing and developer feedback
