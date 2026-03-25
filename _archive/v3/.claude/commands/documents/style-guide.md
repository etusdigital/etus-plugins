---
description: Generate Style Guide with design tokens and component styles
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Style Guide

Creating style guide for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/design/wireframes.md && echo "✓ wireframes.md exists" || echo "⚠ Missing wireframes (recommended to run /wireframes first)"`
!`test -f docs/design/user-journey.md && echo "✓ user-journey.md exists" || echo "ℹ User journey context"`

## Setup

!`mkdir -p docs/ux && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/ux-chain/knowledge/style-guide.md

## Interactive Style Guide Creation

I'll help you create a comprehensive style guide:

### Step 1: Review Design Requirements

Read wireframes and user journey context:

@docs/design/wireframes.md
@docs/design/user-journey.md

### Step 2: Color System (tok.color.*)

**Ask about color palette:**

#### Primary Colors
1. **Brand color**: Main brand color (e.g., blue)
2. **Shades**: Generate 50-900 scale (lighter to darker)
   - 50: Very light (backgrounds)
   - 100-200: Light (hover states, borders)
   - 300-500: Medium (text on dark, icons)
   - 600-700: Main (primary actions, links)
   - 800-900: Dark (text, emphasis)

**Example:**
```
tok.color.primary.50: #EFF6FF   (lightest blue)
tok.color.primary.100: #DBEAFE
tok.color.primary.200: #BFDBFE
tok.color.primary.300: #93C5FD
tok.color.primary.400: #60A5FA
tok.color.primary.500: #3B82F6
tok.color.primary.600: #2563EB  (main brand blue)
tok.color.primary.700: #1D4ED8
tok.color.primary.800: #1E40AF
tok.color.primary.900: #1E3A8A  (darkest blue)
```

#### Neutral Colors (Grays)
- tok.color.neutral.50 through tok.color.neutral.900
- Used for backgrounds, text, borders

#### Semantic Colors
- tok.color.success.* (green for positive actions)
- tok.color.warning.* (yellow/orange for caution)
- tok.color.error.* (red for errors)
- tok.color.info.* (blue for informational)

#### Special Colors
- tok.color.background.light / dark
- tok.color.text.primary / secondary / disabled
- tok.color.border.light / medium / strong

[Define complete color palette]

### Step 3: Typography (tok.font.*)

**Ask about typography system:**

#### Font Families
- tok.font.family.heading: "Inter, system-ui, sans-serif"
- tok.font.family.body: "Inter, system-ui, sans-serif"
- tok.font.family.mono: "Monaco, monospace"

#### Font Sizes
```
tok.font.size.xs: 12px
tok.font.size.sm: 14px
tok.font.size.md: 16px (base)
tok.font.size.lg: 18px
tok.font.size.xl: 20px
tok.font.size.2xl: 24px
tok.font.size.3xl: 30px
tok.font.size.4xl: 36px
tok.font.size.5xl: 48px
```

#### Font Weights
```
tok.font.weight.light: 300
tok.font.weight.regular: 400
tok.font.weight.medium: 500
tok.font.weight.semibold: 600
tok.font.weight.bold: 700
```

#### Line Heights
```
tok.font.lineheight.tight: 1.25
tok.font.lineheight.normal: 1.5
tok.font.lineheight.relaxed: 1.75
tok.font.lineheight.loose: 2
```

#### Typography Scale
Define heading and body text styles:
```
Heading 1: tok.font.size.4xl, tok.font.weight.bold, tok.font.lineheight.tight
Heading 2: tok.font.size.3xl, tok.font.weight.semibold, tok.font.lineheight.tight
Heading 3: tok.font.size.2xl, tok.font.weight.semibold, tok.font.lineheight.normal
Body: tok.font.size.md, tok.font.weight.regular, tok.font.lineheight.normal
Small: tok.font.size.sm, tok.font.weight.regular, tok.font.lineheight.normal
```

### Step 4: Spacing System (tok.spacing.*)

**Define spacing scale:**

```
tok.spacing.0: 0px
tok.spacing.1: 4px
tok.spacing.2: 8px
tok.spacing.3: 12px
tok.spacing.4: 16px
tok.spacing.5: 20px
tok.spacing.6: 24px
tok.spacing.8: 32px
tok.spacing.10: 40px
tok.spacing.12: 48px
tok.spacing.16: 64px
tok.spacing.20: 80px
tok.spacing.24: 96px
```

**Usage:**
- Padding, margins, gaps
- Component internal spacing
- Layout spacing

### Step 5: Effects (tok.shadow.*, tok.radius.*, tok.transition.*)

**Shadow System:**
```
tok.shadow.none: none
tok.shadow.sm: 0 1px 2px 0 rgba(0,0,0,0.05)
tok.shadow.md: 0 4px 6px -1px rgba(0,0,0,0.1)
tok.shadow.lg: 0 10px 15px -3px rgba(0,0,0,0.1)
tok.shadow.xl: 0 20px 25px -5px rgba(0,0,0,0.1)
```

**Border Radius:**
```
tok.radius.none: 0px
tok.radius.sm: 4px
tok.radius.md: 6px
tok.radius.lg: 8px
tok.radius.xl: 12px
tok.radius.full: 9999px (pill shape)
```

**Transitions:**
```
tok.transition.fast: 100ms ease-in-out
tok.transition.normal: 200ms ease-in-out
tok.transition.slow: 400ms ease-in-out
```

### Step 6: Component Styles

**For each component, define styles using tokens:**

**Example: Primary Button**
```css
.button-primary {
  /* Layout */
  padding: tok.spacing.3 tok.spacing.6;
  border-radius: tok.radius.md;

  /* Typography */
  font-size: tok.font.size.md;
  font-weight: tok.font.weight.medium;
  font-family: tok.font.family.body;

  /* Colors */
  background-color: tok.color.primary.600;
  color: tok.color.neutral.50;
  border: none;

  /* Effects */
  box-shadow: tok.shadow.sm;
  transition: tok.transition.normal;
  cursor: pointer;
}

.button-primary:hover {
  background-color: tok.color.primary.700;
  box-shadow: tok.shadow.md;
}

.button-primary:disabled {
  background-color: tok.color.neutral.300;
  cursor: not-allowed;
}
```

[Define styles for all components]

### Step 7: Layout & Grid

**Define layout tokens:**

```
tok.layout.container.sm: 640px
tok.layout.container.md: 768px
tok.layout.container.lg: 1024px
tok.layout.container.xl: 1280px

tok.layout.grid.cols: 12
tok.layout.grid.gap: tok.spacing.6

tok.layout.breakpoint.sm: 640px
tok.layout.breakpoint.md: 768px
tok.layout.breakpoint.lg: 1024px
tok.layout.breakpoint.xl: 1280px
```

### Step 8: Iconography

**Define icon system:**

1. **Icon library**: Lucide, Heroicons, FontAwesome?
2. **Icon sizes**:
   - tok.icon.size.sm: 16px
   - tok.icon.size.md: 20px
   - tok.icon.size.lg: 24px
   - tok.icon.size.xl: 32px
3. **Icon style**: Outlined, filled, or both?
4. **Icon usage**: When to use icons vs text

### Step 9: Confirm Style Guide

"Here's the complete style guide:

**Color System:**
- Primary: 10 shades (50-900)
- Neutral: 10 shades
- Semantic: success, warning, error, info
- Total tokens: ~60 color tokens

**Typography:**
- Fonts: Inter (heading + body)
- Sizes: 9 scales (xs to 5xl)
- Weights: 5 weights
- Line heights: 4 options

**Spacing:**
- 13 spacing tokens (0 to 24)
- Consistent 4px base unit

**Effects:**
- Shadows: 5 levels
- Radius: 6 options
- Transitions: 3 speeds

**Components:**
- [List of styled components]

**Total Design Tokens:** ~150 tokens

Is this style guide complete and consistent?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/style-guide.md`.

**Document Structure:**
- Design Token Catalog (SINGLE SOURCE OF TRUTH)
  - Color Tokens (tok.color.*)
    - Primary palette with hex values
    - Neutral palette
    - Semantic colors
    - Usage guidelines
  - Typography Tokens (tok.font.*)
    - Font families
    - Font sizes
    - Font weights
    - Line heights
    - Typography scale (H1-H6, body, small)
  - Spacing Tokens (tok.spacing.*)
    - Spacing scale
    - Usage guidelines
  - Effect Tokens
    - Shadows (tok.shadow.*)
    - Border radius (tok.radius.*)
    - Transitions (tok.transition.*)
  - Layout Tokens (tok.layout.*)
    - Container widths
    - Grid system
    - Breakpoints
  - Icon Tokens (tok.icon.*)
    - Icon sizes
    - Icon library
- Component Styles (using tokens)
  - CSS for each component
  - States (hover, active, disabled)
  - Variants (sizes, colors)
  - Examples with code
- Usage Guidelines
  - When to use which tokens
  - Color accessibility (contrast ratios)
  - Typography hierarchy
  - Spacing consistency
  - Component composition
- Dark Mode (if applicable)
  - Dark mode token mappings
  - Color adjustments

**CRITICAL**: Design tokens (tok.*) ONLY defined in style-guide.md (Single Source of Truth)

## Validation

After generation:

!`test -f docs/design/style-guide.md && echo "✓ style-guide.md created" || echo "✗ Generation failed"`

**Style guide checklist**:
!`if [ -f docs/design/style-guide.md ]; then
  grep -o "tok\.[a-z]*\.[a-z0-9-]*" docs/design/style-guide.md | sort -u | wc -l | xargs echo "Design tokens defined:"
  grep -ci "color.*#[0-9A-F]" docs/design/style-guide.md | xargs echo "Color definitions:"
  grep -ci "font\|typography" docs/design/style-guide.md | xargs echo "Typography references:"
fi`

## Next Steps

**Validate implementation readiness**:
```
/validate-gate implementation-readiness
```

**Check SST compliance**:
```
/check-sst
```

---

**Style guide generated!** Complete design token system (tok.*) documented as Single Source of Truth.
