---
name: ux-wireframes
description: >
  Use when creating wireframes, planning screen layouts, or defining UI structure.
  Also triggers on 'wireframes', 'what does this page look like', 'screen layout',
  'UI structure', 'component placement', or 'low-fidelity mockup'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Optional: Figma MCP (import existing wireframes/mockups). Upstream: docs/ets/projects/{project-slug}/ux/ux-sitemap.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/ux/ux-sitemap.md` — Needed for page hierarchy to wireframe.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/ux/style-guide.md` — Design tokens improve wireframe consistency.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `wireframes.requires: [ux-sitemap]`
2. Check: does `ux-sitemap.md` exist, non-empty, not DRAFT?
3. If missing → auto-invoke `ux-sitemap` skill → wait → continue
4. Check ENRICHES → warn if missing, proceed

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- New product or major UI overhaul
- Complex screens with multiple states and responsive breakpoints
- Screens that require usability testing before development

**Use short version when:**
- Wireframing 1-2 screens for a new feature
- Minor layout adjustments to existing screens
- Even in short version, still include: desktop wireframe, component inventory, and interaction notes per screen

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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing wireframes.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

### Skill-Specific Interaction

- **Per-screen layout:** For each key screen, propose 2-3 layout options with tradeoffs (e.g., single-column vs. sidebar + main, card grid vs. list view). Ask which direction to take before wireframing.
- **Component choices:** When a screen needs a navigation or content pattern, suggest concrete options with tradeoffs:
  - Tabs vs. sidebar navigation (discoverability vs. screen real estate)
  - Cards vs. list rows (visual richness vs. information density)
  - Modal dialog vs. full page (quick action vs. deep editing)
  Ask which pattern fits the use case.
- **Individual wireframe approval:** Present EACH wireframe individually for approval. Do not batch multiple wireframes. Ask "Does this layout work? Anything to adjust?" before the next screen.
- **Responsive strategy:** Ask about breakpoint priorities — mobile-first (start small, scale up) vs. desktop-first (start full, simplify down) — before wireframing any responsive variants.
- **Handoff options:**
  1. Proceed to Style Guide (Recommended) — define design tokens and visual system
  2. Add more wireframes — cover additional screens or states
  3. Refine layouts — adjust component placement or interaction patterns
  4. Pause — save current progress and return later

# Wireframe Generation

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

## PURPOSE

Generate a comprehensive **wireframes.md** that contains low-fidelity, ASCII-based layouts for each page or screen in the product. This document specifies component placement, interaction annotations, responsive behavior, and accessibility requirements without prescribing visual design (colors, typography, spacing — those come from style-guide.md).

Wireframes bridge information architecture and visual design, making concrete the abstract structure defined in the sitemap.

## CONTEXT LOADING (4-level fallback)

1. **$ARGUMENTS**: If `[upstream-path]` provided, load that document
2. **Handoff**: Check for `docs/ets/projects/{project-slug}/ux/ux-sitemap.md` (page inventory and hierarchy)
3. **Scan**: If not found, check `docs/ets/projects/{project-slug}/ux/user-journey.md` (journey touchpoints)
4. **Ask**: If no context available, ask user for page list and layout types

Load the following sections from upstream:
- Page inventory and hierarchy
- Page categories and purposes
- Navigation structure and breadcrumbs
- User personas and their primary tasks

## PROCESS

1. **Page Selection**: Extract priority pages from sitemap (typically top-level + key flows)
2. **Layout Type Definition**: Determine layout pattern for each page
   - Marketing landing (hero, features, CTA)
   - Dashboard (overview, metrics, actions)
   - Form (inputs, validation, submission)
   - Detail view (full record, edit options)
   - List view (table, filters, pagination)
3. **ASCII Wireframing**: Create low-fidelity ASCII layout per page
   - Header/nav area
   - Main content zone (with proportional sizing)
   - Sidebar (if applicable)
   - Footer
4. **Component Annotation**: Document each major component
   - Name and type (button, input, list, card, etc.)
   - Primary interaction (click, focus, hover)
   - States (default, active, disabled, loading, error)
5. **Responsive Design**: Define behavior at 3+ breakpoints
   - Mobile (< 640px): stacked layout
   - Tablet (640–1024px): intermediate layout
   - Desktop (> 1024px): full layout
   - Describe layout changes per breakpoint
6. **Accessibility Requirements**: Document ARIA and keyboard navigation
   - ARIA labels for dynamic content
   - Tab order and focus management
   - Keyboard shortcuts for common actions
   - Error messages and validation feedback
7. **Interaction Documentation**: Detail user interactions
   - Click targets and validation rules
   - Hover states (desktop only)
   - Scroll behavior and lazy loading
   - Modal triggers and dismissal

## OUTPUT FORMAT

Document structure:
- **Executive Summary**: Page count, layout patterns used
- **Wireframe Sections**: One per major page
  - ASCII layout diagram
  - Component inventory (table: component, type, interaction, state)
  - Responsive breakpoints (with description of changes)
  - Accessibility notes (ARIA, keyboard)
  - Related feature references (PRD-F-#)
- **Global Patterns**: Shared navigation, headers, footers
- **Interaction Reference**: Common interaction patterns across all pages

## PIPELINE CONTEXT

- **Input**: ux-sitemap.md (page structure)
- **Output**: wireframes.md
- **Feeds**: style-guide.md (validates component library), implementation-plan.md (feeds dev specs)
- **Referenced by**: api-spec.md (determines data requirements), implementation docs

## SINGLE SOURCE OF TRUTH (SST)

**Page layouts, component structure, and interaction specifications are ONLY defined here.** Do not replicate layouts or interaction details in style-guide.md (which defines design tokens and visual patterns, not layouts). Design token references (tok.*) are permitted but not defined here.

## KNOWLEDGE POINTER

Refer to `docs/ets/projects/{project-slug}/ux/template-wireframes.md` for:
- ASCII wireframe notation and conventions
- Component annotation format
- Responsive breakpoint descriptions
- Accessibility annotation examples
- Common interaction patterns

---

**Execution instruction**: Load context, extract pages from sitemap, create ASCII wireframes per page with component annotations, document responsive behavior and accessibility requirements, validate against journey touchpoints, and output wireframes.md to docs/ets/projects/{project-slug}/ux/.

## INPUT VALIDATION

**ux-sitemap.md** (BLOCKS):
- Must contain a page/screen hierarchy (tree or list)
- Must list at least 3 pages/screens

**style-guide.md** (ENRICHES):
- Should contain design tokens (tok.*)

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] At least 3 screen wireframes present
- [ ] Each wireframe uses ASCII/markdown layout notation
- [ ] Interaction annotations present (click targets, form flows)
- [ ] Responsive breakpoints noted (mobile, tablet, desktop)
- [ ] Accessibility annotations present (tab order, focus)
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ wireframes.md saved to `docs/ets/projects/{project-slug}/ux/wireframes.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document defines screen layouts, not traceable IDs)

→ Next step: style-guide — Define design tokens (tok.*) and component library
  Run: /design or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WIREFRAME VALIDATION

### Required States per Screen
Every screen wireframe must include these states:
- [ ] **Default/Loaded** — Normal state with data
- [ ] **Empty** — No data yet (first-time experience)
- [ ] **Loading** — Data being fetched
- [ ] **Error** — Something went wrong
- [ ] **Partial** — Some data loaded, some failed

### CRUD Pattern Validation
For each entity with CRUD operations, verify:
- **Create:** Form layout, validation indicators, success/error feedback
- **Read:** List view (with pagination wireframe), detail view, search/filter controls
- **Update:** Edit form, diff view (if applicable), confirmation dialog
- **Delete:** Confirmation dialog, undo option, cascade warning indicator

### Atomic Component Check
- [ ] All atomic components (buttons, inputs, labels) are defined before molecules
- [ ] All molecules are composed of documented atoms
- [ ] No orphan components (used in wireframe but never defined)

### Accessibility Validation
- [ ] Tab order annotated on every screen
- [ ] Touch targets >= 44x44px indicated on mobile wireframes
- [ ] Screen reader flow annotated (heading hierarchy H1→H2→H3)
- [ ] Focus indicators shown for interactive elements

## WORKFLOW

### Step 1: Context Loading
- **Input:** `ux-sitemap.md` (BLOCKS), `style-guide.md` (ENRICHES)
- **Action:** Extract page hierarchy, navigation patterns, design tokens
- **Output:** Screen inventory with layout requirements
- **Why this matters:** The sitemap defines which screens exist. Loading it first ensures wireframes cover the full product surface.

### Step 2: Responsive Strategy (Interactive)
- **Input:** Product context and target platforms
- **Action:** Ask about breakpoint priorities — mobile-first (start small, scale up) vs. desktop-first (start full, simplify down). This decision affects every wireframe.
- **Output:** Selected responsive strategy
- **Why this matters:** Mobile-first and desktop-first produce fundamentally different layouts. Deciding upfront keeps all wireframes consistent.

### Step 3: Per-Screen Layout Design (Individual Approval)
- **Input:** Screen inventory + responsive strategy
- **Action:** For each key screen:
  1. Propose 2-3 layout options with tradeoffs (e.g., single-column vs. sidebar + main)
  2. Ask which direction to take
  3. Propose component choices (tabs vs. sidebar, cards vs. list, modal vs. page) with tradeoffs
  4. Present the wireframe with annotations
  5. Ask "Does this layout work? Anything to adjust?" before proceeding to the next screen
- **Output:** Individual approved wireframes
- **Why this matters:** Approving each wireframe individually catches issues early and ensures the user's vision is reflected before investing in more screens.

### Step 4: State Coverage
- **Input:** Approved wireframes
- **Action:** For each screen, present the 5 required states (loaded, empty, loading, error, partial). Ask "Are these state variations complete?"
- **Output:** Complete wireframe set with all states
- **Integration:** Consumed by `style-guide` skill (BLOCKS)

### Step 5: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is lightweight work and the document has unnecessary sections → trim empty or boilerplate sections
  - If this is complex work and sections are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 6: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline still have to invent if this document is all they get?
  2. Do any sections depend on content claimed to be out of scope?
  3. Are there implicit decisions that should be explicit?
  4. Is there a low-effort addition that would make this significantly more useful for the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 7: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/ux/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/ux/wireframes.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/ux/wireframes.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/ux/ux-sitemap.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 9: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/ux/wireframes.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 10: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION + WIREFRAME VALIDATION checklists
- **Output:** Document marked COMPLETE or DRAFT
- **Handoff:** Present next step options:
  1. Proceed to Style Guide (Recommended)
  2. Add more wireframes
  3. Refine layouts
  4. Pause

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (ux-sitemap.md) | Critical | Auto-invoke ux-sitemap skill | Block execution |
| Too many screens to wireframe (>15) | Medium | Prioritize Must Have features, defer others | Wireframe top 10, list remainder |
| Missing states for a screen | Medium | Add minimal state variants | Note missing states in TODO |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
