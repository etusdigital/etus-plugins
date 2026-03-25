---
name: style-guide
description: >
  Use when defining a style guide, design tokens, or visual design system. Also
  triggers on 'style guide', 'design tokens', 'what colors/fonts', 'brand
  guidelines', 'component library', 'typography', or 'color palette'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Optional: Figma MCP (import design tokens and styles from Figma). Upstream: docs/ets/projects/{project-slug}/ux/wireframes.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/ux/wireframes.md` — Needed for component inventory to define tokens.

**ENRICHES** (improves output — warn if missing):
- None.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `style-guide.requires: [wireframes]`
2. Check: does `wireframes.md` exist, non-empty, not DRAFT?
3. If missing → auto-invoke `wireframes` skill → wait → continue

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Never batch multiple questions. Ask one, wait for the answer, then ask the next. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction, present 3-4 concrete options with a brief description of each. Highlight your recommendation.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs and a recommendation.

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section, ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Resolve before next phase** — Blocks the handoff.
   - **Deferred to [phase name]** — Noted and carried forward.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing style-guide.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

## MEMORY PROTOCOL

This skill reads and writes persistent memory to maintain context across sessions.

**On start (before any interaction):**
1. Read `docs/ets/.memory/project-state.md` — know where the project is
2. Read `docs/ets/.memory/decisions.md` — don't re-question closed decisions
3. Read `docs/ets/.memory/preferences.md` — apply user/team preferences silently
4. Read `docs/ets/.memory/patterns.md` — apply discovered patterns
5. If any memory file doesn't exist, create it with the default template

**On finish (after saving artifact, before CLOSING SUMMARY):**
1. `project-state.md` is updated **automatically** by the PostToolUse hook — do NOT edit it manually.
2. If the user chose between approaches during this skill → run via Bash:
   `python3 .claude/hooks/memory-write.py decision "<decision>" "<rationale>" "<this-skill-name>" "<phase>" "<tag1,tag2>"`
3. If the user expressed a preference → run via Bash:
   `python3 .claude/hooks/memory-write.py preference "<preference>" "<this-skill-name>" "<category>"`
4. If a recurring pattern was identified → run via Bash:
   `python3 .claude/hooks/memory-write.py pattern "<pattern>" "<this-skill-name>" "<applies_to>"`

**The `.memory/*.md` files are read-only views** generated automatically from `memory.db`. Never edit them directly.

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- New product with no existing design system
- Brand refresh or visual redesign
- Building a shared component library for multiple products

**Use short version when:**
- Adding tokens for a new component to an existing design system
- Minor palette or typography adjustments
- Even in short version, still include: tok.* definitions for new tokens and component state documentation

### Skill-Specific Interaction

- **Color palette:** Propose 3-4 palette options with mood and rationale (e.g., "Corporate trust — blues/grays", "Energetic startup — vibrant gradients", "Minimal elegance — monochrome with accent", "Nature/wellness — earth tones"). Ask the user which direction to explore.
- **Typography:** Propose 2-3 font combinations with character descriptions:
  - *Sans-serif modern* — clean, tech-forward (e.g., Inter + JetBrains Mono)
  - *Serif traditional* — authoritative, editorial (e.g., Merriweather + Source Sans Pro)
  - *Mixed personality* — serif headings + sans body for contrast and hierarchy
  Ask which combination fits the product's voice.
- **Spacing system:** Propose base unit with rationale — 4px (fine-grained control, more tokens) vs. 8px (cleaner scale, fewer decisions). Ask which approach to use.
- **Design tokens per category:** Present tokens category by category for approval: first colors, then typography, then spacing, then components. Wait for approval on each category before moving to the next.
- **Handoff options:**
  1. Design phase complete — proceed to Implementation Readiness Gate (Recommended)
  2. Refine guide — adjust tokens, colors, or typography
  3. Add more components — expand the component library
  4. Pause — save current progress and return later

# Design System and Style Guide Generation

## PURPOSE

Generate a comprehensive **style-guide.md** that serves as the authoritative Single Source of Truth for all design tokens and visual system decisions. This document defines design token identifiers (tok.*), typography, color palettes, spacing systems, shadow hierarchy, and component specifications with all state variations.

The style guide is the final UX document in the design phase. It consolidates all visual decisions and provides frontend teams with a complete reference for implementation.

## CRITICAL SST RULE

**All design tokens (tok.*) are defined ONLY in style-guide.md.** No other document may define or redefine tok.* identifiers. Other documents reference but do not create tokens.

## CONTEXT LOADING (4-level fallback)

1. **$ARGUMENTS**: If `[upstream-path]` provided, load that document
2. **Handoff**: Check for `docs/ets/projects/{project-slug}/ux/wireframes.md` (component needs)
3. **Scan**: If not found, check `docs/ets/projects/{project-slug}/ux/user-journey.md` or product-vision.md (brand context)
4. **Ask**: If no context available, ask user for brand colors, typography preferences, and component inventory

Load the following sections from upstream:
- Component list from wireframes
- Layout patterns and spacing needs
- Accessibility requirements (WCAG contrast ratios)
- Brand guidelines or existing design system references

## PROCESS

1. **Brand & Tone Extraction**: Identify brand personality and color associations
2. **Color Palette Definition**: Create semantic color system
   - Primary colors (brand-defining)
   - Secondary colors (supporting)
   - Neutral colors (grayscale, backgrounds)
   - Semantic colors (success green, error red, warning orange, info blue)
   - Each with 5–9 shades (50, 100, 200, ... 900)
3. **Typography System**: Define type hierarchy
   - Heading fonts (2–3 options: serif, sans, display)
   - Body font (primary reading font)
   - Monospace font (code, technical content)
   - Font sizes, weights, line heights for each role (H1–H6, body, caption)
4. **Spacing System**: Establish base unit (8px or 4px) and multiples
   - xs, sm, md, lg, xl, 2xl (8, 16, 24, 32, 48, 64px typical)
5. **Border & Corner Radius**: Define 3–4 levels (sm, md, lg)
6. **Shadow System**: Define elevation levels (sm, md, lg, xl)
7. **Component Library**: Document all reusable components
   - Button (primary, secondary, tertiary, danger variants)
   - Input fields (text, email, password, select, checkbox, radio)
   - Cards, modals, alerts, badges, chips
   - Lists, tables, pagination
   - For each: states (default, hover, active, disabled, focus, error, loading)
8. **Accessibility Validation**: Confirm WCAG AA contrast ratios, focus states
9. **Token Naming**: Generate tok.* identifiers following strict format

## TOKEN FORMAT (CRITICAL)

Format: `tok.[category].[subcategory].[name]`

**Categories:**
- `tok.color.[semantic].[shade]` — e.g., `tok.color.primary.500`, `tok.color.error.100`
- `tok.font.[role].[property]` — e.g., `tok.font.heading.lg`, `tok.font.body.regular`
- `tok.spacing.[size]` — e.g., `tok.spacing.md`, `tok.spacing.2xl`
- `tok.border.[property].[size]` — e.g., `tok.border.radius.md`, `tok.border.width.sm`
- `tok.shadow.[level]` — e.g., `tok.shadow.md`, `tok.shadow.lg`

**Examples:**
- `tok.color.primary.500` — Primary brand color
- `tok.color.error.100` — Light error background
- `tok.font.heading.xl` — Large heading (H1)
- `tok.font.body.regular` — Regular body text
- `tok.spacing.md` — Medium padding/margin (16px)
- `tok.border.radius.md` — Medium corner radius (8px)
- `tok.shadow.lg` — Large elevation shadow

## OUTPUT FORMAT

Document structure:
- **Executive Summary**: Design system overview, design principles
- **Color System**: Palette with hex values, semantic usage, accessibility notes
- **Typography System**: Font families, sizes, weights, line heights, usage guidelines
- **Spacing System**: Base unit, scale, and application examples
- **Elevation & Shadows**: Shadow definitions for each level
- **Component Library**: One section per component type
  - Visual description (ASCII or reference)
  - All state variations (default, hover, active, disabled, focus, error, loading)
  - Token references (tok.* IDs)
  - Implementation notes (CSS class patterns, recommended variants)
- **Accessibility Guidelines**: Contrast ratios, focus indicators, keyboard navigation
- **Usage Guidelines**: When to use which tokens, component composition rules

## PIPELINE CONTEXT

- **Input**: wireframes.md (component requirements)
- **Output**: style-guide.md
- **Feeds**: implementation-plan.md (dev specifications), referenced by all other design docs
- **Convergence point**: All visual decisions finalize here

## SINGLE SOURCE OF TRUTH (SST)

**Design tokens (tok.*), typography definitions, color palette, spacing scale, and component specifications are EXCLUSIVELY defined here.** No other document may define, redefine, or override any tok.* identifier or visual specification. All references to design decisions in other documents must point to style-guide.md.

## KNOWLEDGE POINTER

Refer to `docs/ets/projects/{project-slug}/ux/template-style-guide.md` for:
- Token naming conventions and best practices
- Color palette template with semantic mapping
- Typography system examples
- Spacing scale generation
- Component state variation patterns
- Accessibility checklist (WCAG AA)

---

**Execution instruction**: Load context, extract component and token requirements, define color and typography systems, establish spacing and elevation scales, document all component patterns with state variations, validate accessibility, and output style-guide.md to docs/ets/projects/{project-slug}/ux/.

## INPUT VALIDATION

**wireframes.md** (BLOCKS):
- Must contain at least 3 screen wireframes
- Must use component annotations (buttons, inputs, labels)

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] tok.color tokens defined (primary, secondary, semantic)
- [ ] tok.typography tokens defined (font families, sizes, weights)
- [ ] tok.spacing tokens defined (scale system)
- [ ] tok.breakpoints tokens defined (responsive breakpoints)
- [ ] Atomic component hierarchy present (atoms → molecules → organisms)
- [ ] At least 5 atoms documented with tokens used
- [ ] Accessibility color contrast ratios noted (WCAG AA)
- [ ] SST rule verified: tok.* defined ONLY here
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ style-guide.md saved to `docs/ets/projects/{project-slug}/ux/style-guide.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list tok.* token categories, e.g., tok.color.*, tok.font.*, tok.spacing.*, tok.border.*, tok.shadow.*]

→ Next step: validate-gate (Design Gate) or parallel completion — UX pipeline complete
  Run: /validate or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## ATOMIC DESIGN SYSTEM

This skill generates design tokens AND a component hierarchy using Atomic Design methodology.

### Component Hierarchy (5 Levels)

**Atoms** — Smallest UI elements, cannot be decomposed further:
- Buttons, inputs, labels, icons, badges, dividers, avatars
- Each atom references tok.* tokens for styling

**Molecules** — Groups of atoms working together:
- Search bars (input atom + button atom + icon atom)
- Form fields (label atom + input atom + validation message atom)
- Navigation items (icon atom + label atom + badge atom)

**Organisms** — Complex components made of molecules:
- Headers (logo + nav molecules + search molecule + user menu)
- Sidebars (nav items + section dividers + collapse control)
- Card grids (card organisms in responsive grid layout)

**Templates** — Page-level layouts defining content areas:
- Dashboard layout (header + sidebar + main content + footer)
- Form layout (header + form sections + action bar)
- List layout (header + filters + list + pagination)

**Pages** — Actual page instances with real content:
- Specific implementations of templates with data

### Design Token Definitions

Generate implementation-ready token objects:

```typescript
// tok.color
const colors = {
  primary: { 50: '#value', 100: '#value', ..., 900: '#value' },
  secondary: { 50: '#value', ..., 900: '#value' },
  neutral: { 50: '#value', ..., 900: '#value' },
  semantic: { success: '#value', warning: '#value', error: '#value', info: '#value' }
}

// tok.typography
const typography = {
  fontFamily: { sans: 'Inter, system-ui, sans-serif', mono: 'JetBrains Mono, monospace' },
  fontSize: { xs: '0.75rem', sm: '0.875rem', base: '1rem', lg: '1.125rem', xl: '1.25rem', '2xl': '1.5rem' },
  fontWeight: { normal: 400, medium: 500, semibold: 600, bold: 700 },
  lineHeight: { tight: 1.25, normal: 1.5, relaxed: 1.75 }
}

// tok.spacing
const spacing = { 0.5: '0.125rem', 1: '0.25rem', 2: '0.5rem', 3: '0.75rem', 4: '1rem', 6: '1.5rem', 8: '2rem', 12: '3rem', 16: '4rem' }

// tok.breakpoints
const breakpoints = { sm: '640px', md: '768px', lg: '1024px', xl: '1280px', '2xl': '1536px' }

// tok.radius
const borderRadius = { sm: '0.25rem', md: '0.375rem', lg: '0.5rem', xl: '0.75rem', full: '9999px' }

// tok.shadow
const boxShadow = { sm: '0 1px 2px rgba(0,0,0,0.05)', md: '0 4px 6px rgba(0,0,0,0.1)', lg: '0 10px 15px rgba(0,0,0,0.1)' }
```

### Component Catalog Table

For each documented component:

| Component | Level | Tokens Used | ARIA Role | Keyboard | States | Status |
|-----------|-------|-------------|-----------|----------|--------|--------|
| Button | Atom | tok.color.primary, tok.spacing.2, tok.radius.md | button | Enter/Space | default, hover, active, disabled, loading | Spec'd |
| Input | Atom | tok.color.neutral, tok.spacing.2, tok.radius.md | textbox | Tab, typing | default, focus, error, disabled | Spec'd |
| SearchBar | Molecule | (uses Button + Input atoms) | search | Enter to submit | empty, typing, loading, results | Spec'd |

### Accessibility Checklist (per level)

**Atoms:**
- [ ] Color contrast ≥ 4.5:1 (normal text) or ≥ 3:1 (large text) — WCAG AA
- [ ] Interactive atoms have focus indicators (visible ring/outline)
- [ ] Touch targets ≥ 44x44px on mobile

**Molecules:**
- [ ] Tab order is logical within the molecule
- [ ] ARIA labels on composite components

**Organisms:**
- [ ] Keyboard navigation covers all interactive elements
- [ ] Screen reader can traverse organism content meaningfully
- [ ] Skip-to-content links for repeated organisms (e.g., header)

## WORKFLOW

### Step 1: Context Loading
- **Input:** `wireframes.md` (BLOCKS)
- **Action:** Extract component inventory, layout patterns, visual annotations
- **Output:** Component list with usage context
- **Why this matters:** The wireframes define which components exist. Starting from the actual component inventory ensures the design system covers everything the product needs.

### Step 2: Color Palette (Interactive)
- **Input:** Brand context + component list
- **Action:** Propose 3-4 palette options with mood and rationale. Ask the user which direction to explore. After selection, present the full color system (primary, secondary, neutral, semantic shades) for approval.
- **Output:** Approved tok.color.* tokens
- **Why this matters:** Color sets the emotional tone of the entire product. Getting this right first guides typography and component decisions.

### Step 3: Typography (Interactive)
- **Input:** Approved colors + product voice
- **Action:** Propose 2-3 font combinations with character descriptions. After selection, present the full typography scale (sizes, weights, line heights) for approval.
- **Output:** Approved tok.font.* tokens

### Step 4: Spacing & Layout Tokens (Interactive)
- **Input:** Typography decisions
- **Action:** Propose base unit (4px vs. 8px) with rationale. Present the complete spacing scale, border radius, and shadow system for approval.
- **Output:** Approved tok.spacing.*, tok.border.*, tok.shadow.* tokens
- **Why this matters:** Consistent spacing creates visual harmony. The base unit decision affects every component in the system.

### Step 5: Atomic Hierarchy (Section-by-Section)
- **Input:** All approved tokens + component list
- **Action:** Classify components into atoms/molecules/organisms/templates/pages. Present each level for approval:
  1. Atoms — present each with tokens used and states, ask for approval
  2. Molecules — present composition from atoms, ask for approval
  3. Organisms — present complex components, ask for approval
- **Output:** Component catalog table with ARIA roles and keyboard patterns

### Step 6: Accessibility Audit
- **Input:** Component catalog
- **Action:** Verify contrast ratios, focus management, ARIA compliance per level. Present results and ask "Do these accessibility standards meet your requirements?"
- **Output:** Accessibility checklist results

### Step 7: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is lightweight work and the document has unnecessary sections → trim empty or boilerplate sections
  - If this is complex work and sections are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 8: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline still have to invent if this document is all they get?
  2. Do any sections depend on content claimed to be out of scope?
  3. Are there implicit decisions that should be explicit?
  4. Is there a low-effort addition that would make this significantly more useful for the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 9: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/ux/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/ux/style-guide.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 10: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/ux/style-guide.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/ux/wireframes.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 11: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/ux/style-guide.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 12: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT
- **Integration:** tok.* IDs are SST — no other document may define design tokens
- **Handoff:** Present next step options:
  1. Design phase complete — proceed to Implementation Readiness Gate (Recommended)
  2. Refine guide
  3. Add more components
  4. Pause

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (wireframes.md) | Critical | Auto-invoke wireframes skill | Block execution |
| No components in wireframes | Medium | Ask user for component list | Define minimal atom set |
| Color contrast fails WCAG AA | High | Suggest adjusted colors | Flag failing combinations |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
| tok.* conflict with existing doc | Critical | This is SST — report violation | Only style-guide defines tok.* |
