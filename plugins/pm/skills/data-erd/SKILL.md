---
name: data-erd
description: >
  Use when creating an ER diagram, mapping entity relationships, or visualizing
  the data model. Also triggers on 'ERD', 'entity relationship diagram', 'how do
  entities relate', 'cardinality mapping', or 'show the data model'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Upstream: docs/ets/projects/{project-slug}/data/data-requirements.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** `docs/ets/projects/{project-slug}/data/data-requirements.md`
- Resolution: Verify existence and ≥5 entities listed. If missing, warn and ask to generate upstream first.

**ENRICHES:** None—ERD is purely derived from requirements.

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT
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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing erd.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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
- New data model from scratch (no existing ERD)
- Significant schema redesign with new entity relationships
- M:N relationships that need junction table resolution

**Use short version when:**
- Adding 1-2 entities to an existing data model
- Modifying attributes on existing entities
- Even in short version, still include: updated Mermaid erDiagram and Relationship Matrix for affected entities

### Skill-Specific Interaction Patterns

- **Relationships — one at a time:** Ask about ONE entity relationship per message. Example: "User and Project: what's the relationship? (A) One user has many projects, (B) Many-to-many through a membership table, (C) One-to-one." Wait for the answer before asking about the next relationship.
- **Key strategy:** Before generating the diagram, propose key strategies (UUID vs. auto-increment vs. composite key) with tradeoffs for this project. Let the user choose.
- **Complete diagram review:** After building the full ERD from approved relationships, present the complete Mermaid diagram for a final review before saving.
- **Handoff options:** At completion, present:
  1. **Proceed to Database Spec** (Recommended) — Generate DDL statements from the ERD
  2. **Refine ERD** — Adjust relationships, add entities, change cardinalities
  3. **Pause** — Save progress and return later

# ERD Skill

## PURPOSE

Generate **erd.md** — the Entity-Relationship Diagram that visually maps all entities, their key attributes, and relationships with cardinalities (1:1, 1:N, M:N). Transforms abstract data requirements into a normalized data model suitable for database implementation.

## CONTEXT LOADING

Load context using this 4-level fallback:

1. **$ARGUMENTS** — User provides upstream path: `docs/ets/projects/{project-slug}/data/data-requirements.md`
2. **Handoff** — Receive data-requirements.md path from data-agent
3. **Scan** — If no path given, search `docs/ets/projects/{project-slug}/data/` for `data-requirements.md`
4. **Ask** — If still missing, ask user: "What is the path to the data requirements document?"

Read `references/template.md` for diagram template and entity attribute format.

## PROCESS

1. **Review Entities and Attributes**
   - Extract all entities from data-requirements.md
   - Identify primary keys, unique identifiers, and key attributes
   - Filter to essential attributes for diagram clarity

2. **Identify Relationships**
   - Scan entity dependencies noted in data-requirements
   - Determine relationship type: identifying (hard) vs. non-identifying (soft)
   - Document relationship semantics

3. **Determine Cardinalities**
   - One-to-One (1:1) — each instance maps to exactly one
   - One-to-Many (1:N) — one parent to multiple children
   - Many-to-Many (M:N) — resolve to junction tables if applicable

4. **Create Mermaid erDiagram**
   - Draw entities with key attributes
   - Add relationship lines with cardinality notation
   - Validate no circular dependencies without resolution

## OUTPUT

Generate `docs/ets/projects/{project-slug}/data/erd.md` with:

- **Mermaid erDiagram** — visual ER model with all entities and relationships
- **Entity Descriptions** — purpose and business meaning of each entity
- **Relationship Matrix** — table mapping source → relationship → target with cardinality
- **Normalization Notes** — any M:N junction tables or denormalization decisions

## PIPELINE POSITION

**Second in data design pipeline**

- ← Upstream: `docs/ets/projects/{project-slug}/data/data-requirements.md`
- → Feeds: `docs/ets/projects/{project-slug}/data/database-spec.md`, `docs/ets/projects/{project-slug}/data/data-dictionary.md`

## INPUT VALIDATION

**From data-requirements.md:** Verify Entity Inventory table with ≥5 entities, business purpose, and primary key columns. Minimum 500 chars.

## OUTPUT VALIDATION

- [ ] Mermaid erDiagram renders without syntax errors
- [ ] All entities from data-requirements present in diagram
- [ ] Cardinalities marked (1:1, 1:N, M:N) on all relationships
- [ ] Relationship Matrix table maps source→relationship→target with semantics
- [ ] Normalization Notes explain any M:N resolution or denormalization
- [ ] Source Documents section present at top
- [ ] If any check fails → mark document as `<!-- STATUS: DRAFT -->` at top

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ erd.md saved to `docs/ets/projects/{project-slug}/data/erd.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document defines entity relationships, not traceable IDs)

→ Next step: database-spec — Generate DDL statements from ERD
  Run: /design or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Extract Entities and Attributes
- **Input:** data-requirements.md Entity Inventory
- **Action:** List all entities with primary keys and key attributes for diagram. Present the attribute list for review.
- **Approval:** Ask "Do these attributes capture the essential fields? Anything to add or remove?"
- **Output:** Confirmed attribute list per entity

### Step 2: Key Strategy Decision
- **Input:** Entity list and project context
- **Action:** Propose key strategies (UUID vs. auto-increment vs. composite key) with tradeoffs for this project. Highlight a recommendation.
- **Approval:** Ask the user to choose the key strategy before generating the diagram.

### Step 3: Determine Relationships (one at a time)
- **Input:** data-requirements.md Dependencies section + business rules
- **Action:** For each entity pair, ask ONE relationship question per message. Example: "User and Project: what's the relationship? (A) One user has many projects, (B) Many-to-many through a membership table, (C) One-to-one."
- **Approval:** Wait for the user's answer before asking about the next relationship. Resolve M:N relationships to junction tables when chosen.
- **Output:** Complete relationship list with cardinalities

### Step 4: Create and Review Mermaid erDiagram
- **Input:** All confirmed entities, attributes, relationships, cardinalities
- **Action:** Draw erDiagram with entities, attributes, and cardinality notation
- **Approval:** Present the complete diagram for a final review. Ask "Does this ERD capture the data model correctly? Anything to adjust?"
- **Output:** Approved Mermaid code block
- **Integration:** feeds to database-spec skill for DDL generation

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
  1. Verify directory exists: `docs/ets/projects/{project-slug}/data/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/data/erd.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/data/erd.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/data/data-requirements.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 9: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/data/erd.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 10: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist. Display CLOSING SUMMARY.
- **Handoff:** Present the 3 next-step options from the Interaction Protocol. Let the user choose.
- **Output:** Document marked COMPLETE or DRAFT

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| data-requirements.md missing | Critical | Auto-invoke data-requirements skill, ask user | Block—cannot generate ERD without entity inventory |
| Mermaid syntax errors | High | Debug erDiagram syntax, validate in Mermaid Live | Mark DRAFT, document error in comment |
| M:N relationship unresolved | Medium | Create explicit junction table, add to diagram | Mark DRAFT, document junction table design needed |
| Output validation fails | High | Mark DRAFT, document failures, proceed | Continue—database-spec will refine |
