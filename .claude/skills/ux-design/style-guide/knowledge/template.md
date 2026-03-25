# Style Guide Template

## Responsaveis

- **Owner:** Design Lead
- **Contribuem:** PM, Frontend Dev
- **Aprovacao:** PM + Design Lead

## Table of Contents

1. [Design Tokens Registry](#design-tokens-registry)
   - [Color Palette](#color-palette-tokcolor)
   - [Typography Scale](#typography-scale-tokfont)
   - [Spacing System](#spacing-system-tokspacing)
   - [Border Radius](#border-radius-tokborderradius)
   - [Borders](#borders-tokborder)
   - [Shadows](#shadows-tokshadow)
2. [Component Library](#component-library)
   - [Button Component](#button-component)
   - [Input Component](#input-component)
   - [Card Component](#card-component)
   - [Modal Component](#modal-component)
3. [Responsive Design](#responsive-design)
4. [Accessibility](#accessibility)
5. [Dark Mode](#dark-mode-optional)
6. [Implementation Checklist](#implementation-checklist)

---

## Design Tokens Registry

### Color Palette (tok.color.*)

#### Primary Colors

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `tok.color.primary` | #0066CC | 0, 102, 204 | CTAs, highlights, primary actions |
| `tok.color.primary-50` | #E6F0FF | 230, 240, 255 | Backgrounds, very light |
| `tok.color.primary-100` | #CCE0FF | 204, 224, 255 | Hover backgrounds |
| `tok.color.primary-200` | #99C0FF | 153, 192, 255 | Active, interactive |
| `tok.color.primary-700` | #0052A3 | 0, 82, 163 | Hover state |
| `tok.color.primary-900` | #003D7A | 0, 61, 122 | Pressed, dark mode |

#### Secondary Colors

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `tok.color.secondary` | #7C3AED | 124, 58, 237 | Secondary CTAs, accents |
| `tok.color.secondary-50` | #F5F3FF | 245, 243, 255 | Light backgrounds |
| `tok.color.secondary-600` | #6D28D9 | 109, 40, 217 | Hover state |

#### Neutral Colors (Grays)

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `tok.color.neutral-0` | #FFFFFF | 255, 255, 255 | White background |
| `tok.color.neutral-50` | #FAFAFA | 250, 250, 250 | Subtle backgrounds |
| `tok.color.neutral-100` | #F5F5F5 | 245, 245, 245 | Card backgrounds |
| `tok.color.neutral-200` | #E7E5E4 | 231, 229, 228 | Borders |
| `tok.color.neutral-400` | #A1A1A1 | 161, 161, 161 | Disabled text |
| `tok.color.neutral-600` | #525252 | 82, 82, 82 | Body text |
| `tok.color.neutral-900` | #1A1A1A | 26, 26, 26 | Headings, dark text |

#### Semantic Colors

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `tok.color.success` | #10B981 | 16, 185, 129 | Success states, confirmations |
| `tok.color.success-50` | #ECFDF5 | 236, 253, 245 | Success bg |
| `tok.color.warning` | #F59E0B | 245, 158, 11 | Warnings, cautions |
| `tok.color.warning-50` | #FFFBEB | 255, 251, 235 | Warning bg |
| `tok.color.error` | #EF4444 | 239, 68, 68 | Errors, destructive |
| `tok.color.error-50` | #FEE2E2 | 254, 226, 226 | Error bg |
| `tok.color.info` | #3B82F6 | 59, 130, 246 | Info, notifications |
| `tok.color.info-50` | #EFF6FF | 239, 246, 255 | Info bg |

#### Semantic Text Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `tok.color.text-primary` | tok.color.neutral-900 | Main content |
| `tok.color.text-secondary` | tok.color.neutral-600 | Supporting text |
| `tok.color.text-tertiary` | tok.color.neutral-400 | Disabled, muted |
| `tok.color.text-inverse` | tok.color.neutral-0 | Text on dark backgrounds |

---

### Typography Scale (tok.font.*)

#### Font Families

| Token | Font | Usage |
|-------|------|-------|
| `tok.font.brand` | "Montserrat", sans-serif | Headlines, brand |
| `tok.font.body` | "Inter", sans-serif | Body text, UI |
| `tok.font.mono` | "Fira Code", monospace | Code, technical |

#### Heading Scale

| Token | Size | Weight | Line-Height | Letter-Spacing | Usage |
|-------|------|--------|-------------|---|--------|
| `tok.font.heading.xl` | 48px | 700 | 1.2 | -0.02em | H1 - Page titles |
| `tok.font.heading.lg` | 36px | 700 | 1.25 | -0.01em | H2 - Section headers |
| `tok.font.heading.md` | 28px | 600 | 1.3 | 0 | H3 - Subsections |
| `tok.font.heading.sm` | 24px | 600 | 1.35 | 0 | H4 - Small headers |
| `tok.font.heading.xs` | 20px | 600 | 1.4 | 0 | H5 - Tiny headers |

#### Body Text Scale

| Token | Size | Weight | Line-Height | Usage |
|-------|------|--------|-------------|-------|
| `tok.font.body.lg` | 18px | 400 | 1.6 | Large body, intro text |
| `tok.font.body.md` | 16px | 400 | 1.6 | Default body text |
| `tok.font.body.sm` | 14px | 400 | 1.5 | Small text, captions |
| `tok.font.body.xs` | 12px | 400 | 1.4 | Metadata, footer |

#### Button Text

| Token | Size | Weight | Line-Height | Usage |
|-------|------|--------|-------------|-------|
| `tok.font.button.lg` | 16px | 600 | 1.5 | Large buttons |
| `tok.font.button.md` | 14px | 600 | 1.5 | Standard buttons |
| `tok.font.button.sm` | 12px | 600 | 1.5 | Small buttons |

---

### Spacing System (tok.spacing.*)

**Base unit:** 8px. Scales in multiples of 4.

| Token | Value | Use Cases |
|-------|-------|-----------|
| `tok.spacing.xs` | 4px | Tight spacing, icon gaps |
| `tok.spacing.sm` | 8px | Padding inputs, small gaps |
| `tok.spacing.md` | 16px | Default padding, margins |
| `tok.spacing.lg` | 24px | Section spacing, card padding |
| `tok.spacing.xl` | 32px | Large gaps, header padding |
| `tok.spacing.2xl` | 48px | Hero sections, major spacing |
| `tok.spacing.3xl` | 64px | Page margins, large sections |

---

### Border Radius (tok.border.radius.*)

| Token | Value | Usage |
|-------|-------|-------|
| `tok.border.radius.sm` | 4px | Inputs, small components |
| `tok.border.radius.md` | 8px | Cards, buttons, default |
| `tok.border.radius.lg` | 12px | Large cards, panels |
| `tok.border.radius.full` | 9999px | Circles, pills |

---

### Borders (tok.border.*)

| Token | Value | Usage |
|-------|-------|-------|
| `tok.border.width.sm` | 1px | Default borders |
| `tok.border.width.md` | 2px | Focus borders, active states |
| `tok.border.color.default` | tok.color.neutral-200 | Default borders |
| `tok.border.color.focus` | tok.color.primary | Focus ring |
| `tok.border.color.error` | tok.color.error | Error states |

---

### Shadows (tok.shadow.*)

| Token | CSS | Z-Elevation | Usage |
|-------|-----|-------------|-------|
| `tok.shadow.sm` | 0 1px 2px 0 rgba(0,0,0,0.05) | 1 | Subtle elevation |
| `tok.shadow.md` | 0 4px 6px -1px rgba(0,0,0,0.1) | 2 | Cards, dropdowns |
| `tok.shadow.lg` | 0 10px 15px -3px rgba(0,0,0,0.1) | 3 | Modals, popups |
| `tok.shadow.xl` | 0 20px 25px -5px rgba(0,0,0,0.1) | 4 | Floating panels |

---

## Component Library

### Button Component

#### Variants

**Primary Button**
```
State: default
Background: tok.color.primary
Color: tok.color.neutral-0
Padding: tok.spacing.sm tok.spacing.md
Border-radius: tok.border.radius.md
Font: tok.font.button.md

State: hover
Background: tok.color.primary-700
Cursor: pointer
Shadow: tok.shadow.md

State: active
Background: tok.color.primary-900
Shadow: tok.shadow.sm

State: disabled
Background: tok.color.neutral-200
Color: tok.color.neutral-400
Cursor: not-allowed
```

**Secondary Button**
```
State: default
Background: tok.color.neutral-100
Color: tok.color.primary
Border: tok.border.width.sm tok.border.color.default
Padding: tok.spacing.sm tok.spacing.md
Border-radius: tok.border.radius.md

State: hover
Background: tok.color.neutral-200
```

**Text Button**
```
State: default
Background: transparent
Color: tok.color.primary
Text-decoration: none

State: hover
Color: tok.color.primary-700
Text-decoration: underline
```

#### Sizes

| Size | Padding | Font | Usage |
|------|---------|------|-------|
| **Large** | tok.spacing.md tok.spacing.lg | tok.font.button.lg | Primary CTAs, hero |
| **Medium** | tok.spacing.sm tok.spacing.md | tok.font.button.md | Default, most cases |
| **Small** | 4px tok.spacing.sm | tok.font.button.sm | Compact, tables |

### Input Component

#### Text Input

```
State: default
Border: tok.border.width.sm tok.border.color.default
Border-radius: tok.border.radius.md
Padding: tok.spacing.sm tok.spacing.md
Font: tok.font.body.md
Background: tok.color.neutral-0

State: hover
Border-color: tok.color.neutral-400

State: focus
Border-color: tok.color.primary
Border-width: tok.border.width.md
Outline: 2px solid tok.color.primary-50
Box-shadow: 0 0 0 3px tok.color.primary-50

State: disabled
Background: tok.color.neutral-50
Color: tok.color.text-tertiary
Cursor: not-allowed

State: error
Border-color: tok.color.error
```

#### Label & Help Text

```
Label: tok.font.body.sm, tok.color.text-primary, margin-bottom: tok.spacing.xs
Help text: tok.font.body.xs, tok.color.text-secondary, margin-top: tok.spacing.xs
Error text: tok.font.body.xs, tok.color.error, margin-top: tok.spacing.xs
```

### Card Component

```
Background: tok.color.neutral-0
Border: tok.border.width.sm tok.border.color.default
Border-radius: tok.border.radius.lg
Padding: tok.spacing.lg
Box-shadow: tok.shadow.md

State: hover
Box-shadow: tok.shadow.lg
Transform: translateY(-2px)

Responsive:
- Mobile: margin tok.spacing.md
- Desktop: margin 0
```

### Modal Component

```
Background: tok.color.neutral-0
Border-radius: tok.border.radius.lg
Box-shadow: tok.shadow.xl
Max-width: 500px
Padding: tok.spacing.lg

Title: tok.font.heading.md, tok.color.text-primary
Body: tok.font.body.md, tok.color.text-secondary
Close button: Top-right corner, 32x32px, tok.color.neutral-400

Overlay:
- Background: rgba(0, 0, 0, 0.5)
- Backdrop-filter: blur(2px)
```

---

## Responsive Design

### Breakpoints

| Breakpoint | Width | Devices | Behavior |
|-----------|-------|---------|----------|
| **Mobile** | <640px | Phone | Single column, large touch targets |
| **Tablet** | 640-1024px | Tablet | Two columns, optimized spacing |
| **Desktop** | >1024px | Desktop, Laptop | Full layout, optimal readability |

### Scaling Rules

- **Font sizes:** Base size -2px on mobile
- **Spacing:** 80% of desktop on mobile, 90% on tablet
- **Padding:** Reduce by 25% on mobile
- **Icons:** Min 24x24px on mobile, 16x16px on desktop

---

## Accessibility

### Color Contrast

| Element | Ratio | Standard |
|---------|-------|----------|
| Body text on background | 7:1 | AAA |
| UI components | 4.5:1 | AA |
| Large text (18+px) | 3:1 | AA |

### Focus States

```
All interactive elements:
- Outline: 2px solid tok.color.primary
- Outline-offset: 2px
- No outline-color: transparent in any state
- Visible on keyboard navigation (tab)
```

### Touch Targets

- Minimum: 44x44px
- Recommended: 48x48px
- Spacing: min 8px gap between targets

### Reduced Motion

```
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Dark Mode (Optional)

If implementing dark theme, create tok.* variants:

| Token | Light | Dark | Contrast |
|-------|-------|------|----------|
| `tok.color.bg.primary` | tok.color.neutral-0 | #121212 | Automatic |
| `tok.color.text.primary` | tok.color.neutral-900 | tok.color.neutral-0 | 19:1 |

---

## Implementation Checklist

- [ ] Color palette matches brand guidelines
- [ ] Typography scales work at all breakpoints
- [ ] Spacing system creates clear hierarchy
- [ ] Component states cover all use cases
- [ ] Focus states visible and consistent
- [ ] Contrast ratios meet WCAG AA/AAA
- [ ] Touch targets min 44x44px
- [ ] No color-only information
- [ ] Responsive design tested at 3 breakpoints
- [ ] Design tokens exported for development (Figma, CSS, JSON)

## O que fazer / O que nao fazer

**O que fazer:**
- Definir todos os tokens com tok.* IDs (SST)
- Verificar contraste WCAG AA para todas as combinacoes
- Documentar todos os estados de cada componente
- Incluir valores exatos (hex, px, rem) — nunca vagos

**O que nao fazer:**
- Nao definir tok.* em outro documento (SST e aqui)
- Nao usar cores sem verificar acessibilidade
- Nao criar componentes sem documentar estados
- Nao definir spacing sem base unit consistente

