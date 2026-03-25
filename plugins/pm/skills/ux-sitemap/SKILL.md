---
name: ux-sitemap
description: >
  Use when creating a sitemap, defining navigation structure, or planning information
  architecture. Also triggers on 'sitemap', 'how are screens organized', 'page
  hierarchy', 'navigation map', or 'screen structure'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Optional: Figma MCP (import existing sitemaps). Upstream: docs/ets/projects/{project-slug}/ux/user-journey.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/ux/user-journey.md` — Needed for user flows to inform page hierarchy.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/ux/wireframes.md` — Screen details improve sitemap accuracy.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `ux-sitemap.requires: [user-journey]`
2. Check: does `user-journey.md` exist, non-empty, not DRAFT?
3. If missing → auto-invoke `user-journey` skill → wait → continue
4. Check ENRICHES → warn if missing, proceed

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- New product requiring complete information architecture
- Major navigation restructuring or replatforming
- Product with >20 screens across multiple user roles

**Use short version when:**
- Adding screens for a single new feature
- Reorganizing one section of the navigation
- Even in short version, still include: updated hierarchy diagram and page inventory for new screens

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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing ux-sitemap.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

### Skill-Specific Interaction

- **IA approach:** Propose 2-3 navigation structures with tradeoffs before building the hierarchy:
  - *Flat* — all pages at the same level, minimal nesting (good for small apps with few screens)
  - *Hierarchical* — deep parent-child tree (good for content-heavy products with many sections)
  - *Hub-and-spoke* — central dashboard linking to independent sections (good for task-oriented products)
  Ask the user which best fits their product.
- **Page grouping:** Present the proposed hierarchy level by level. Start with top-level categories, ask for approval, then expand each category into child pages for further approval.
- **Complete sitemap review:** Present the full sitemap diagram (Mermaid) for approval before writing the document.
- **Handoff options:**
  1. Proceed to Wireframes (Recommended) — create low-fidelity layouts for each page
  2. Refine sitemap — adjust hierarchy, add missing pages, or reorganize navigation
  3. Pause — save current progress and return later

# Information Architecture and Sitemap Generation

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

Generate a comprehensive **ux-sitemap.md** that defines the hierarchical structure of all pages, screens, and navigation patterns in the product. This document serves as the authoritative reference for how information and functionality are organized, how users navigate between sections, and which access levels apply to each page.

The ux-sitemap is generated after user journeys are mapped and feeds directly into wireframes. It bridges user needs (from journeys) with concrete interaction design (wireframes and API structure).

## CONTEXT LOADING (4-level fallback)

1. **$ARGUMENTS**: If `[upstream-path]` provided, load that document
2. **Handoff**: Check for `docs/ets/projects/{project-slug}/ux/user-journey.md` (touchpoints, journey stages)
3. **Scan**: If not found, check `docs/ets/projects/{project-slug}/planning/user-stories.md` (user flows)
4. **Ask**: If no context available, ask user for journey touchpoints and MVP scope

Load the following sections from upstream:
- Journey stages and touchpoints (which determine page categories)
- User goals by persona (determines page priority)
- Access control requirements
- Any existing page inventory or URL schemes

## PROCESS

1. **Touchpoint Extraction**: Identify all unique touchpoints from user journeys
2. **Page Categorization**: Organize pages into categories
   - Core (product functionality)
   - Discovery (onboarding, marketing)
   - Account (settings, profile, preferences)
   - Support (help, documentation, contact)
   - Admin (if applicable)
3. **Hierarchy Definition**: Map parent-child relationships
   - Root pages (primary entry points)
   - Child pages (sub-sections)
   - Utility pages (error, loading, empty states)
4. **Navigation Pattern Definition**: Document how users move between pages
   - Primary navigation (persistent)
   - Secondary navigation (contextual)
   - Breadcrumbs (location awareness)
   - Footer links (utility and SEO)
5. **Access Control**: Define visibility per user role
   - Public (no auth)
   - Authenticated (logged-in users)
   - Admin (elevated permissions)
   - Specific role-based access
6. **URL Structure**: Establish consistent slug patterns
   - Kebab-case conventions
   - Semantic, RESTful paths
   - Query parameter usage

## OUTPUT FORMAT

Document structure:
- **Executive Summary**: Total page count, structure overview
- **Information Architecture Diagram**: Mermaid flowchart showing hierarchy
- **Page Inventory**: Table with name, path, parent, category, access level, purpose
- **Navigation Patterns**: Primary, secondary, and utility navigation definitions
- **URL Structure**: Naming conventions and examples
- **User Access Matrix**: Pages × Roles (which users see what)
- **Navigation Rules**: Specific rules for breadcrumbs, back buttons, deep linking

## PIPELINE CONTEXT

- **Input**: user-journey.md (touchpoints and stages)
- **Output**: ux-sitemap.md
- **Feeds**: wireframes.md (specifies layouts per page), api-spec.md (routes)
- **Referenced by**: style-guide.md (navigation components)

## SINGLE SOURCE OF TRUTH (SST)

**Site/app hierarchy, page inventory, and navigation structure are ONLY defined here.** Do not replicate page listings or navigation patterns in wireframes.md or style-guide.md. All other documents reference these definitions.

## KNOWLEDGE POINTER

Refer to `docs/ets/projects/{project-slug}/ux/template-ux-sitemap.md` for:
- Page categorization taxonomy
- Information architecture Mermaid syntax
- Page inventory table template
- Navigation pattern examples
- URL structure conventions

---

**Execution instruction**: Load context, extract journey touchpoints, organize into hierarchy, define navigation patterns, establish access control and URL schemes, and output ux-sitemap.md to docs/ets/projects/{project-slug}/ux/.

## INPUT VALIDATION

**user-journey.md** (BLOCKS):
- Must contain at least 2 journey maps
- Must list touchpoints

**wireframes.md** (ENRICHES):
- Should contain screen/page names

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Hierarchical page/screen map present (tree structure)
- [ ] Navigation patterns documented (primary, secondary, utility)
- [ ] All journey touchpoints from user-journey.md represented as pages/screens
- [ ] Information architecture rationale explained
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ ux-sitemap.md saved to `docs/ets/projects/{project-slug}/ux/ux-sitemap.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document defines page hierarchy, not traceable IDs)

→ Next step: wireframes — Create low-fidelity layouts for each page/screen
  Run: /design or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `user-journey.md` (BLOCKS), `wireframes.md` (ENRICHES)
- **Action:** Extract touchpoints, user flows, screen inventory
- **Output:** Page/screen candidate list
- **Why this matters:** Journey touchpoints are the raw material for pages. Starting from real user interactions ensures no important screen is missed.

### Step 2: IA Approach Selection (Interactive)
- **Input:** Page candidates + product type
- **Action:** Propose 2-3 navigation structures (flat, hierarchical, hub-and-spoke) with tradeoffs. Ask the user which best fits the product.
- **Output:** Selected IA pattern
- **Why this matters:** The navigation structure shapes how users discover and access content. Choosing the right pattern early avoids costly restructuring later.

### Step 3: Hierarchy Definition (Level-by-Level Approval)
- **Input:** Page candidates + selected IA pattern
- **Action:** Present the proposed hierarchy level by level:
  1. Top-level categories — present and ask for approval
  2. Second-level pages within each category — present and ask for approval
  3. Utility pages (error, loading, empty states) — present and ask for approval
- **Output:** Sitemap tree (Mermaid or ASCII), approved level by level
- **Integration:** Consumed by `wireframes` skill (BLOCKS)

### Step 4: Navigation Patterns
- **Input:** Approved sitemap tree
- **Action:** Define primary nav, secondary nav, utility nav, breadcrumbs. Present the navigation specification and ask "Does this navigation model work? Anything to adjust?"
- **Output:** Navigation specification

### Step 5: Complete Sitemap Review
- **Input:** Hierarchy + navigation
- **Action:** Present the full sitemap diagram (Mermaid) for final approval before saving. Ask "Does this complete sitemap capture the product structure? Anything to adjust?"
- **Output:** Approved sitemap diagram

### Step 6: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is lightweight work and the document has unnecessary sections → trim empty or boilerplate sections
  - If this is complex work and sections are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 7: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline still have to invent if this document is all they get?
  2. Do any sections depend on content claimed to be out of scope?
  3. Are there implicit decisions that should be explicit?
  4. Is there a low-effort addition that would make this significantly more useful for the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 8: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/ux/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/ux/ux-sitemap.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/ux/ux-sitemap.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/ux/user-journey.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/ux/ux-sitemap.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 11: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT
- **Handoff:** Present next step options:
  1. Proceed to Wireframes (Recommended)
  2. Refine sitemap
  3. Pause

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (user-journey.md) | Critical | Auto-invoke user-journey skill | Block execution |
| Journey maps too sparse | Medium | Ask user about key screens/pages | Proceed with minimal sitemap |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
