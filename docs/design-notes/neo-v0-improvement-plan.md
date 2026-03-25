# ETUS PMDocs v5.0 — Improvement Plan

> Date: 2026-03-14
> Status: DRAFT
> Source: Deep analysis of Neo v0 (280 files, 13 agents, 7 chains), cross-referenced with BMAD, Superpowers, Compound Engineering
> Scope: All improvements to be applied ONLY to `etus-pmdocs` repository (single source of truth)

---

## Executive Summary

After reading 100+ files across Neo v0's architecture, templates, chains, components, and orchestration layers, this plan consolidates every adoptable pattern into 16 concrete improvements organized in 4 categories. Each improvement cites its source, current gap, proposed solution, and implementation effort.

The improvements fall into these categories:

- **A. Dependency & Validation Engine** (7 improvements) — Already detailed in `dependency-enforcement-research.md`, summarized here for completeness
- **B. Skill Enhancement Patterns** (3 improvements + 1 rejected) — New structural patterns per SKILL.md
- **C. New Skills & Document Types** (3 improvements) — Entirely new capabilities inspired by Neo v0
- **D. Orchestration & Quality Loops** (2 improvements) — Process-level improvements

---

## A. Dependency & Validation Engine

> Full detail in `dependency-enforcement-research.md`. Summary of the 7 improvements below.

### A1. Centralized `dependency-graph.yaml`

**Source:** Neo v0 `index.yaml` with `requires`/`generates`
**Gap:** Each SKILL.md maintains its own `## DEPENDENCIES` section — they can diverge.
**Solution:** Single YAML file at `.claude/skills/orchestrator/dependency-graph.yaml` mapping all 21 documents with `requires`, `enriched-by`, `produces`, `skill`, `phase`.
**Effort:** Medium | **Impact:** High | **Priority:** P0

### A2. BLOCKS vs ENRICHES Classification

**Source:** BMAD hard gate + Neo v0 declarative model
**Gap:** Current WARN → SUGGEST → ASK → MARK is too permissive.
**Solution:** Two-tier system. BLOCKS = skill refuses to run. ENRICHES = skill warns but proceeds.
**Effort:** Low | **Impact:** High | **Priority:** P0

### A3. Auto-Invoke Upstream Skill

**Source:** Novel (no framework does this)
**Gap:** All frameworks say "run X first" but none actually invoke X.
**Solution:** Recursive dependency resolution with max depth=5. If BLOCKS dep missing → auto-invoke upstream skill → wait → continue.
**Effort:** High | **Impact:** Very High | **Priority:** P1

### A4. Input Content Validation

**Source:** Neo v0 `<input_validation>` with `min_length`, `required_sections`, `min_items`
**Gap:** We only check file existence, not content structure.
**Solution:** Each SKILL.md gets `## INPUT VALIDATION` section with structural checks (required headings, minimum IDs, minimum length).
**Effort:** Medium | **Impact:** High | **Priority:** P2

### A5. Output Quality Gate per Skill

**Source:** Neo v0 `<output_validation>` metrics + Compound Engineering `.coverage-thresholds.json`
**Gap:** We have phase gates (GO/NO-GO) but no per-skill quality checks.
**Solution:** Each SKILL.md gets `## OUTPUT VALIDATION` checklist. Document marked DRAFT if any check fails. DRAFT status doesn't satisfy BLOCKS dependencies downstream.
**Effort:** Medium | **Impact:** Medium | **Priority:** P2

### A6. Anti-Rationalization Rules

**Source:** Superpowers' 12 rationalization patterns
**Gap:** No defense against AI skipping dependency checks.
**Solution:** Explicit block in orchestrator SKILL.md listing 7+ excuses the AI must never use.
**Effort:** Low | **Impact:** Medium | **Priority:** P1

### A7. Handoff Carries Dependency Status

**Source:** Existing handoff protocol + Neo v0 `blockingIssues`/`pendingDocuments`
**Gap:** Handoff JSON doesn't include document completeness status or ID counts.
**Solution:** Each handoff JSON includes `documents` map with `status: COMPLETE|DRAFT`, `path`, `ids`, and `unresolved_dependencies` array.
**Effort:** Low | **Impact:** Medium | **Priority:** P3

---

## B. Skill Enhancement Patterns

These are structural patterns to add to every SKILL.md, inspired by Neo v0's XML prompts and .meta.md sidecar files.

### B1. Structured Workflow Steps with Integration Points

**Source:** Neo v0 `design_management_workflow.xml` (5-phase workflow with `<integration_points>` listing source/target/data_flow per connection), `user-story-implementation.xml` (4-step workflow with `<dependencies>` tags per step)

**Current gap:** Our SKILL.md files describe WHAT to generate but not HOW to generate it step-by-step. The workflow is embedded in prose without explicit phase boundaries or integration points.

**Proposed solution:** Add `## WORKFLOW` section to every SKILL.md with numbered steps, each step having:
- Step name and purpose
- Inputs consumed (with specific file references)
- Actions taken
- Outputs produced
- Integration point (what other skill/document this connects to)

**Example (for tech-spec skill):**

```markdown
## WORKFLOW

### Step 1: Context Loading
- **Input:** `architecture-diagram.md` (BLOCKS), `prd.md` (ENRICHES), `project-context.md` (ENRICHES)
- **Action:** Extract system components, technology choices, and business constraints
- **Output:** Internal context object (not persisted)
- **Integration:** Reads from architecture-agent output

### Step 2: NFR Extraction
- **Input:** Step 1 context + `user-stories.md` (if available)
- **Action:** Derive quantified NFRs (NFR-#) from context — performance, security, reliability, scalability
- **Output:** NFR table with target values and measurement methods
- **Integration:** NFR-# IDs referenced by `implementation-plan.md` and `quality-checklist.md`

### Step 3: ADR Drafting
- **Input:** Step 1 context + technology constraints
- **Action:** Document Architecture Decision Records (ADR-#) with context, options considered, decision, consequences
- **Output:** ADR entries
- **Integration:** ADR-# IDs referenced by `architecture-diagram.md` (bidirectional)

### Step 4: Validation
- **Input:** Steps 2-3 outputs
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Final `tech-spec.md` marked COMPLETE or DRAFT
- **Integration:** Writes to handoff if phase gate pending
```

**Effort:** Medium (25 skills × 30 min each) | **Impact:** High | **Priority:** P1

### B2. Document References / Source Documents Section

**Source:** Neo v0 templates — every template (BRD, PRD, SRS, UXDD, DRD, DBRD) starts with a `## Document References` or `## Source Documents` section that explicitly lists upstream documents with version and status.

**Current gap:** Generated documents don't cite their upstream sources. A `tech-spec.md` doesn't declare which `architecture-diagram.md` it was built from. This breaks auditability.

**Proposed solution:** Every generated document must include a `## Source Documents` section at the top (after title), listing:
- Document name
- Path
- Status at time of generation (COMPLETE/DRAFT)
- Key IDs consumed (e.g., "PRD-F-1 through PRD-F-8")

**Template to add to each SKILL.md's output format:**

```markdown
## Source Documents

| Document | Path | Status | Key References |
|----------|------|--------|----------------|
| Architecture Diagram | `docs/ets-docs/architecture/architecture-diagram.md` | COMPLETE | C4 Container View, ADR-1 |
| PRD | `docs/ets-docs/planning/prd.md` | COMPLETE | PRD-F-1..PRD-F-8 |
| Project Context | `docs/ets-docs/discovery/project-context.md` | COMPLETE | Tech stack, constraints |
```

**Effort:** Low (template change in each SKILL.md) | **Impact:** Medium | **Priority:** P1

### ~~B3. `.meta.md` Sidecar Files per Skill~~ — REJECTED

> **Decision (2026-03-14):** After researching Claude Code's native progressive disclosure architecture, the sidematter format spec (jlevy), and how BMAD/Superpowers/Compound Engineering handle metadata, this improvement was rejected.
>
> **Reasons:**
> 1. Claude Code already has 3-level progressive disclosure: frontmatter (~100 tokens at startup) → SKILL.md body (on invocation) → `knowledge/` files (on demand). Adding META.md creates a 4th level that the runtime doesn't recognize.
> 2. Everything META.md would contain (Dependencies, Outputs, Success Criteria, Validation) already lives in SKILL.md sections or will live there after improvements A2/A4/A5. Creating META.md would **duplicate** information across two files.
> 3. Neo v0's `.meta.md` files were **human documentation**, not AI instructions — they existed because Cline loaded 132KB monolithically and humans needed navigation aids. In Claude Code's skill model, this need doesn't exist.
> 4. No other major framework (BMAD, Superpowers, Compound Engineering) uses sidecar metadata files for skills.
> 5. The centralized `dependency-graph.yaml` (A1) already serves as the machine-parseable metadata layer — one file for all 21 documents, not 25 separate sidecars.
>
> **Alternative:** The metadata that META.md would have contained is distributed as: dependency info → `dependency-graph.yaml` (A1), validation rules → inline `## INPUT VALIDATION` / `## OUTPUT VALIDATION` in SKILL.md (A4/A5), success criteria → `## OUTPUT VALIDATION` checklist, related skills → `dependency-graph.yaml` edges.

### B3. Error Handling with Typed Recovery Actions

**Source:** Neo v0 `generate-REVISED-project-requirements.xml` — has `<error_handling>` with 4 typed errors, each with severity, recovery_action, and fallback:

```xml
<error_handling>
  <error type="missing_original">
    <severity>critical</severity>
    <recovery_action>Request original requirements document</recovery_action>
    <fallback>Generate new requirements from change requests only</fallback>
  </error>
  <error type="conflicting_changes">
    <severity>high</severity>
    <recovery_action>Flag conflicts for manual resolution</recovery_action>
    <fallback>Apply non-conflicting changes, mark conflicts as TODO</fallback>
  </error>
</error_handling>
```

**Current gap:** Our skills fail silently or with generic warnings. No typed error catalog, no recovery actions, no fallbacks.

**Proposed solution:** Add `## ERROR HANDLING` section to each SKILL.md:

```markdown
## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dependency missing | Critical | Auto-invoke upstream skill | Block execution |
| ENRICHES dependency missing | Warning | Proceed with generic context | Add `<!-- ENRICHMENT_MISSING -->` comment |
| Input validation fails (stub file) | Critical | Re-invoke upstream skill | Block execution |
| Output validation fails | High | Mark document as DRAFT | Flag specific failing checks |
| Circular dependency detected | Critical | Halt with depth=5 error | Report cycle to user |
| Conflicting IDs with existing docs | Medium | Renumber to avoid collision | Append suffix `-alt` |
```

**Effort:** Low-Medium | **Impact:** Medium | **Priority:** P2

---

## C. New Skills & Document Types

These are entirely new capabilities inspired by specific Neo v0 components that have no equivalent in etus-pmdocs.

### C1. Atomic Design System Skill (for `style-guide`)

**Source:** Neo v0 `atomic_design_system.xml` (629 lines) — the most complete design system template found in any framework. Defines a 5-level component hierarchy (atoms → molecules → organisms → templates → pages) with embedded TypeScript design tokens, Shadcn UI integration, theme configuration, and accessibility checklist.

**Current gap:** Our `style-guide` skill generates design tokens (`tok.*`) and basic visual guidelines, but doesn't enforce component hierarchy or provide implementation-ready token definitions.

**Proposed solution:** Enhance the `style-guide` skill with an atomic design system approach:

1. **Component Hierarchy Section** — Define 5 levels with examples:
   - Atoms: buttons, inputs, labels, icons
   - Molecules: search bars, form fields, nav items
   - Organisms: headers, sidebars, card grids
   - Templates: page layouts, dashboard layouts
   - Pages: actual page instances

2. **Design Token Definitions** — TypeScript-ready token objects:
   ```typescript
   // tok.color
   const colors = {
     primary: { 50: '#eff6ff', 500: '#3b82f6', 900: '#1e3a5a' },
     semantic: { success: '#22c55e', warning: '#f59e0b', error: '#ef4444' }
   }

   // tok.typography
   const typography = {
     fontFamily: { sans: 'Inter, system-ui', mono: 'JetBrains Mono' },
     fontSize: { xs: '0.75rem', sm: '0.875rem', base: '1rem', lg: '1.125rem' }
   }

   // tok.spacing
   const spacing = { 1: '0.25rem', 2: '0.5rem', 4: '1rem', 8: '2rem' }

   // tok.breakpoints
   const breakpoints = { sm: '640px', md: '768px', lg: '1024px', xl: '1280px' }
   ```

3. **Accessibility Checklist** (per component level):
   - Color contrast ratios (WCAG AA: 4.5:1 normal, 3:1 large)
   - Keyboard navigation patterns
   - ARIA role requirements per component type
   - Focus management rules

4. **Component Catalog Table**:
   | Component | Level | Tokens Used | ARIA Role | Keyboard | Status |
   |-----------|-------|-------------|-----------|----------|--------|
   | Button | Atom | tok.color.primary, tok.spacing.2 | button | Enter/Space | Spec'd |

**Effort:** High | **Impact:** High | **Priority:** P1

### C2. Feature Journey Map Document (FJMD)

**Source:** Neo v0 `full_feature_journey_map_doc-fjmd.xml` — maps features across 4 journey categories: primary_flows, interaction_points, user_experience, error_handling. Includes user personas with goals/pain_points/expectations.

**Current gap:** Our `user-journey` skill creates journey maps per persona, but doesn't map **feature-level journeys** — how a specific feature is experienced across all touchpoints. The distinction is:
- User journey = persona-centric (Maria's path through the product)
- Feature journey = feature-centric (how "checkout" is experienced across all personas)

**Proposed solution:** Add a `feature-journey-map` option to the `user-journey` skill (not a separate skill, to avoid proliferation). When invoked with a specific feature (e.g., "map the checkout feature journey"), produce:

```markdown
## Feature Journey Map: [Feature Name]

### Personas Involved
- [Persona A] — Goal: X, Pain point: Y
- [Persona B] — Goal: Z, Pain point: W

### Primary Flow
1. Entry point → [trigger/action]
2. Interaction → [what happens]
3. Decision point → [branch logic]
4. Completion → [success state]

### Interaction Points
| Touchpoint | Persona | Action | System Response | Emotion |
|------------|---------|--------|-----------------|---------|

### Error Flows
| Error Scenario | User Sees | Recovery Path | Fallback |
|---------------|-----------|---------------|----------|

### Experience Validation
- [ ] All personas can complete primary flow
- [ ] Error flows have recovery paths
- [ ] Emotional arc trends toward satisfaction
- [ ] Accessibility touchpoints verified
```

**Effort:** Medium | **Impact:** Medium | **Priority:** P2

### C3. Wireframe Validation Rules

**Source:** Neo v0 `wireframe_validation.yaml` — structural validation rules organized by: atomic_components (required elements per level), user_stories (required flows: happy path, error, loading, empty states), data_patterns (CRUD operations with required elements per operation), testing_requirements (visual, functional, accessibility, performance).

**Current gap:** Our `wireframes` skill generates wireframes but has no structural validation to catch missing states (empty state, loading state, error state) or incomplete CRUD patterns.

**Proposed solution:** Add `## WIREFRAME VALIDATION` section to the wireframes SKILL.md:

```markdown
## WIREFRAME VALIDATION

### Required States per Screen
Every screen must show wireframes for these states:
- [ ] **Default/Loaded** — Normal state with data
- [ ] **Empty** — No data yet (first-time experience)
- [ ] **Loading** — Data being fetched
- [ ] **Error** — Something went wrong
- [ ] **Partial** — Some data loaded, some failed

### CRUD Pattern Validation
For each entity with CRUD operations:
- **Create:** Form layout, validation indicators, success/error feedback
- **Read:** List view (with pagination), detail view, search/filter
- **Update:** Edit form, diff view (if applicable), confirmation
- **Delete:** Confirmation dialog, undo option, cascade warning

### Atomic Component Check
- [ ] All atomic components (buttons, inputs, labels) are defined before molecules
- [ ] All molecules are composed of documented atoms
- [ ] No orphan components (used but never defined)

### Accessibility Validation
- [ ] Tab order annotated on every screen
- [ ] Touch targets >= 44x44px on mobile wireframes
- [ ] Screen reader flow annotated (heading hierarchy)
```

**Effort:** Low | **Impact:** Medium | **Priority:** P2

---

## D. Orchestration & Quality Loops

### D1. Iterative Quality Loop (Self-Evaluation → Improvement → Re-Evaluation)

**Source:** Neo v0 `code_quality_chain.xml` (339 lines) — the most sophisticated quality process found. Runs 4 agents in a cycle: evaluator → improver → rater → generator. Each iteration produces a `quality_score`. The loop terminates on 4 conditions:
1. All quality booleans pass (security, performance, reliability, test_coverage, code_style)
2. Quality score ≥ 0.85
3. Max iterations reached
4. Diminishing returns (score improvement < 2% between iterations)

Also inspired by: Neo v0 `follow-up-critique-prompt.md` — iterative refinement where previous response is reviewed, issues identified (3 solutions per issue), best solution selected and implemented, then the refined response is reviewed again until "no more issues."

**Current gap:** Our skills generate a document once and mark it complete. No self-evaluation cycle. The only quality check is the phase gate (GO/NO-GO), which is coarse-grained (per phase, not per document).

**Proposed solution:** Add an optional quality loop to critical skills (those producing documents that many downstream skills depend on). The loop:

```markdown
## QUALITY LOOP (Optional — triggered by orchestrator or user)

### Cycle
1. **Generate** — Produce initial document following WORKFLOW steps
2. **Self-Evaluate** — Score the output against OUTPUT VALIDATION checklist
   - Calculate: completeness % (how many checks pass)
   - If completeness ≥ 90% → mark COMPLETE, exit loop
   - If completeness < 90% → proceed to step 3
3. **Identify Issues** — List each failing check with specific gap description
4. **Improve** — Address each issue, regenerate affected sections
5. **Re-Evaluate** — Score again
   - If improved by < 5% → diminishing returns, mark as DRAFT with notes
   - If completeness ≥ 90% → mark COMPLETE, exit loop
   - If max iterations (3) reached → mark as DRAFT with notes
6. **Report** — Log iteration count, score progression, remaining gaps

### Applicable Skills (high-dependency documents)
- `product-vision` (feeds everything downstream)
- `prd` (feeds all of planning + design)
- `architecture-diagram` (feeds all design agents)
- `user-stories` (feeds implementation)
- `tech-spec` (feeds implementation + quality)
```

**Effort:** High | **Impact:** High | **Priority:** P1

### D2. Self-Reflection & Confidence Grading for Complex Skills

**Source:** Neo v0 `reasoning.md` (super-reasoning-agent with 10-step framework, confidence 0-1 per step, genius-agent critique), `self-reflection-prompt.md` (6-step reflection: Initial Thoughts → Knowledge Assessment → Reasoning → Alternatives → Confidence → Final Response)

**Current gap:** Our skills don't include any metacognitive process. The AI generates directly without evaluating its own confidence or considering alternatives.

**Proposed solution:** Add a `## REFLECTION PROTOCOL` section to the 3 Opus-level skills (project-context, product-vision, prd) where creative/strategic reasoning matters most:

```markdown
## REFLECTION PROTOCOL

Before finalizing the document, run this internal check:

### 1. Assumption Audit
- What assumptions am I making about the user's context?
- Am I filling gaps with generic defaults instead of asking?
- Score: [Low/Medium/High confidence in context completeness]

### 2. Alternative Perspectives
- Would a different product strategy make more sense?
- Are there business objectives I haven't considered?
- Have I challenged the user's stated assumptions constructively?

### 3. Completeness Check
- Does every section have substantive content (not placeholders)?
- Are IDs sequential and traceable?
- Would a downstream skill (e.g., prd reading product-vision) have enough context to work?

### 4. Quality Decision
- If confidence is LOW on any section → ask the user ONE targeted question
- If confidence is MEDIUM → flag it with `<!-- CONFIDENCE: MEDIUM — [reason] -->` inline
- If confidence is HIGH → proceed to OUTPUT VALIDATION
```

**Effort:** Low | **Impact:** Medium | **Priority:** P2

---

## Implementation Roadmap

### Phase 1: Foundation (P0) — 1-2 days

| # | Improvement | Deliverable |
|---|-------------|-------------|
| A1 | Centralized dependency graph | `.claude/skills/orchestrator/dependency-graph.yaml` |
| A2 | BLOCKS vs ENRICHES | Update 25 SKILL.md `## DEPENDENCIES` → `## DEPENDENCY RESOLUTION` |

### Phase 2: Core Engine (P1) — 3-5 days

| # | Improvement | Deliverable |
|---|-------------|-------------|
| A3 | Auto-invoke upstream | Update orchestrator SKILL.md with auto-invocation protocol |
| A6 | Anti-rationalization | Add `## ANTI-RATIONALIZATION RULES` to orchestrator SKILL.md |
| B1 | Workflow steps | Add `## WORKFLOW` to all 25 SKILL.md files |
| B2 | Document References | Add Source Documents template to all SKILL.md output formats |
| C1 | Atomic Design System | Enhance `style-guide` SKILL.md with full atomic hierarchy |
| D1 | Quality Loop | Add `## QUALITY LOOP` to 5 critical skills |

### Phase 3: Depth (P2) — 3-5 days

| # | Improvement | Deliverable |
|---|-------------|-------------|
| A4 | Input validation | Add `## INPUT VALIDATION` to all 25 SKILL.md files |
| A5 | Output quality gate | Add `## OUTPUT VALIDATION` to all 25 SKILL.md files |
| B3 | Error handling | Add `## ERROR HANDLING` to all 25 SKILL.md files |
| C2 | Feature Journey Map | Enhance `user-journey` SKILL.md |
| C3 | Wireframe Validation | Add `## WIREFRAME VALIDATION` to wireframes SKILL.md |
| D2 | Reflection Protocol | Add `## REFLECTION PROTOCOL` to 3 Opus-level skills |

### Phase 4: Polish (P3) — 1 day

| # | Improvement | Deliverable |
|---|-------------|-------------|
| A7 | Handoff dependency status | Update handoff JSON schema in orchestrator and all commands |

---

## Cross-Reference: Neo v0 → ETUS PMDocs Mapping

This table shows which Neo v0 patterns map to which etus-pmdocs improvements:

| Neo v0 Pattern | Source File | ETUS PMDocs Improvement | Status |
|---------------|-------------|------------------------|--------|
| `requires`/`generates` in index.yaml | `neo_prompt/index.yaml` | A1 — dependency-graph.yaml | Planned |
| `<chain-position>` previous/next | All development XMLs | A1 — graph encodes this | Planned |
| `<input_validation>` min_length, required_sections | `generate-REVISED-project-requirements.xml` | A4 — Input Content Validation | Planned |
| `<output_validation>` metrics, pass_fail | `generate-REVISED-project-requirements.xml` | A5 — Output Quality Gate | Planned |
| `<error_handling>` typed errors + recovery | `generate-REVISED-project-requirements.xml` | B4 — Error Handling | Planned |
| `<state_management>` versioned variables | `generate-REVISED-project-requirements.xml` | — (deferred, low ROI) | Deferred |
| Document References section | All templates (BRD, PRD, SRS, UXDD, DRD, DBRD) | B2 — Source Documents | Planned |
| `.meta.md` sidecar files | `atomic_design_system.meta.md`, others | ~~B3 — META.md sidecars~~ | **REJECTED** — info distributed to A1 graph + A4/A5 inline sections |
| Workflow with `<integration_points>` | `design_management_workflow.xml` | B1 — Workflow Steps | Planned |
| Atomic design system (5 levels + tokens) | `atomic_design_system.xml` (629 lines) | C1 — Enhance style-guide | Planned |
| SBVR Business Ontology | `svbr_business_ontology_prompt.xml` | — (consider for data-dictionary) | Deferred |
| Feature Journey Map Document | `full_feature_journey_map_doc-fjmd.xml` | C2 — Enhance user-journey | Planned |
| Wireframe validation YAML | `wireframe_validation.yaml` | C3 — Wireframe Validation | Planned |
| Code quality iteration loop | `code_quality_chain.xml` (339 lines) | D1 — Quality Loop | Planned |
| Confidence grading (0-1) | `reasoning.md` | D2 — Reflection Protocol | Planned |
| Self-reflection 6-step | `self-reflection-prompt.md` | D2 — Reflection Protocol | Planned |
| Follow-up critique (3 solutions/issue) | `follow-up-critque-prompt.md` | D1 — Quality Loop | Planned |
| Prompt chain orchestrator | `prompt-chain-orchestrator.xml` | Already exists (orchestrator skill) | N/A |
| Tech Stack BOM | `generate-tech-stack-BOM.xml` | — (consider for tech-spec) | Deferred |
| Sprint story generation | `generate_next_sprint_user_stories.xml` | Already exists (sprint-status skill) | N/A |
| PlantUML diagrams in templates | `technical_architecture.md` | — (we use Mermaid, keep as-is) | N/A |
| Neo agent `#gen-doc-type` command | `neo_agent.xml` | Already exists (commands/) | N/A |

### Deferred Patterns (Low ROI or Incompatible)

| Pattern | Reason for Deferral |
|---------|-------------------|
| SBVR Business Ontology | Too specialized. Our data-dictionary skill covers field/event definitions without OWL generation overhead. Revisit if a project needs formal ontology. |
| State Management (versioned variables) | Neo v0's `<state_management>` tracked version numbers per document change. Our handoff protocol covers phase-level state. Per-document versioning adds complexity without clear benefit for the LLM workflow. |
| Tech Stack BOM generator | Our tech-spec skill covers technology decisions via ADRs. A separate BOM is useful for enterprise procurement but not for our document pipeline. Revisit if users request it. |
| PlantUML diagrams | We standardized on Mermaid. No benefit to switching. |
| 132KB monolithic YAML loading | Neo v0 loaded everything into context at once. Our skill-per-document architecture is better. This is an anti-pattern we already solved. |

---

## Success Criteria for v5.0

The improvement plan is complete when:

1. **dependency-graph.yaml** exists and all 21 documents are mapped with `requires`/`enriched-by`
2. **All 25 SKILL.md** files have been updated with: DEPENDENCY RESOLUTION, WORKFLOW, INPUT VALIDATION, OUTPUT VALIDATION, ERROR HANDLING sections
3. **5 critical skills** have QUALITY LOOP sections (product-vision, prd, architecture-diagram, user-stories, tech-spec)
4. **3 Opus skills** have REFLECTION PROTOCOL sections (project-context, product-vision, prd)
5. **style-guide** skill includes full atomic design system hierarchy with TypeScript token definitions
6. **wireframes** skill includes wireframe validation rules (states, CRUD, accessibility)
7. **user-journey** skill supports feature journey map variant
8. **Orchestrator** includes anti-rationalization rules and auto-invocation protocol
9. **All generated documents** include Source Documents section at the top

### Verification Method

Run a dry test: invoke the orchestrator for a sample project and verify that:
- Missing dependencies trigger auto-invocation (A3)
- Generated documents include Source Documents section (B2)
- Output validation catches incomplete documents (A5)
- Phase gate handoffs include document status (A7)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-14 | Initial plan based on Neo v0 deep analysis |
