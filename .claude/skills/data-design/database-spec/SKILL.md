---
name: database-spec
description: >
  Use when defining database schema, creating table definitions, or planning
  migrations. Also triggers on 'database spec', 'create the tables', 'DDL',
  'migration strategy', 'index strategy', or 'database schema'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Upstream: docs/ets/projects/{project-slug}/data/erd.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** `docs/ets/projects/{project-slug}/data/erd.md`
- Resolution: Verify existence and Mermaid diagram renders. If missing, warn and ask to generate upstream first.

**ENRICHES:** `docs/ets/projects/{project-slug}/architecture/tech-spec.md`
- Resolution: Optional. If tech-spec exists, extract NFR-* targets for performance, indexing strategy, and storage constraints.

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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing database-spec.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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
- New database with no existing schema
- Major migration (e.g., changing database engine or restructuring tables)
- Schema with >10 tables and complex constraints

**Use short version when:**
- Adding 1-3 tables to an existing schema
- Adding columns or indexes to existing tables
- Even in short version, still include: CREATE TABLE DDL, Index Strategy, and Migration Plan for new/changed tables

### Skill-Specific Interaction Patterns

- **Database engine:** Before generating DDL, propose 3-4 engine options (e.g., PostgreSQL, MySQL, SQLite, MongoDB) with tradeoffs for this project's scale, query patterns, and team expertise. Let the user choose.
- **Per-table DDL:** Present the CREATE TABLE statement for each table individually. Ask "Does this table look correct? Anything to adjust?" before moving to the next table.
- **Index strategy:** After each table's DDL is approved, propose indexes for that table with rationale (query patterns, cardinality, expected performance). Let the user confirm.
- **Soft vs. hard delete:** For each relevant entity, propose soft delete (with `deleted_at` column) vs. hard delete with tradeoffs. Ask the user's preference per entity or globally.
- **Handoff options:** At completion, present:
  1. **Proceed to Data Dictionary** (Recommended) — Define dict.* and ev.* field/event identifiers
  2. **Refine DDL** — Adjust table definitions, constraints, or indexes
  3. **Pause** — Save progress and return later

# Database Spec Skill

## PURPOSE

Generate **database-spec.md** — the Single Source of Truth for all CREATE TABLE statements, column definitions, indexes, constraints, and migration strategies. This is the only document where DDL appears; no other document may contain CREATE TABLE, ALTER TABLE, or index definitions.

## CONTEXT LOADING

Load context using this 4-level fallback:

1. **$ARGUMENTS** — User provides upstream path: `docs/ets/projects/{project-slug}/data/erd.md`
2. **Handoff** — Receive erd.md path from data-agent
3. **Scan** — If no path given, search `docs/ets/projects/{project-slug}/data/` for `erd.md`
4. **Ask** — If still missing, ask user: "What is the path to the ERD document?"

Read `references/template.md` for DDL formatting and migration script template.

## SST RULE

**Why this matters:** All CREATE TABLE, ALTER TABLE, and DDL statements should appear only in database-spec.md. Keeping DDL in a single location prevents conflicting schemas and ensures gate approval passes the SST check.

## PROCESS

1. **Translate ERD to DDL**
   - Convert each entity to a CREATE TABLE statement
   - Map attributes to typed columns (INT, VARCHAR, TIMESTAMP, UUID, etc.)
   - Add primary keys and unique constraints from ERD

2. **Define Indexes**
   - Identify indexed columns: primary keys, foreign keys, frequent filters
   - Specify index type (B-tree, Hash, BRIN as applicable)
   - Estimate index size and query performance impact

3. **Plan Migrations**
   - Version migration scripts (V001_initial_schema.sql, V002_add_column.sql)
   - Document rollback procedures
   - Identify backward-compatible sequences

## OUTPUT

Generate `docs/ets/projects/{project-slug}/data/database-spec.md` with:

- **DDL Statements** — CREATE TABLE for all entities with typed columns
- **Constraints** — PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL
- **Index Strategy** — indexed columns, types, rationale
- **Migration Plan** — versioned scripts, dependencies, rollback procedures

## PIPELINE POSITION

**Third in data design pipeline**

- ← Upstream: `docs/ets/projects/{project-slug}/data/erd.md`
- → Feeds: `docs/ets/projects/{project-slug}/data/data-dictionary.md`, `docs/ets/projects/{project-slug}/data/data-flow-diagram.md`

## INPUT VALIDATION

**From erd.md:** Verify Mermaid diagram present, all entities with cardinalities. Minimum 500 chars.

**From tech-spec (if present):** Verify NFR-* IDs for performance targets, storage constraints.

## OUTPUT VALIDATION

- [ ] CREATE TABLE DDL present for all entities from ERD
- [ ] All columns typed (INT, VARCHAR, UUID, TIMESTAMP, JSONB, etc.)
- [ ] PRIMARY KEY and FOREIGN KEY constraints defined
- [ ] UNIQUE and CHECK constraints specified per requirements
- [ ] Index strategy documented (B-tree, Hash, BRIN)
- [ ] Migration plan with version numbering (V001, V002, etc.)
- [ ] Source Documents section present at top
- [ ] **SST rule verified:** DDL appears ONLY here, nowhere else in codebase
- [ ] If any check fails → mark document as `<!-- STATUS: DRAFT -->` at top

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ database-spec.md saved to `docs/ets/projects/{project-slug}/data/database-spec.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document defines DDL/schema, not traceable IDs)

→ Next step: data-dictionary — Define dict.* and ev.* field/event identifiers
  Run: /design or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Database Engine Decision
- **Input:** Project context, tech-spec NFRs, team expertise
- **Action:** Propose 3-4 database engine options (e.g., PostgreSQL, MySQL, SQLite, MongoDB) with tradeoffs for this project's scale, query patterns, and team expertise. Highlight a recommendation.
- **Approval:** Ask the user to choose the engine before generating any DDL.

### Step 2: Soft vs. Hard Delete Policy
- **Input:** Business requirements, compliance constraints
- **Action:** For each relevant entity (or globally), propose soft delete (with `deleted_at` column) vs. hard delete with tradeoffs. Present the options clearly.
- **Approval:** Ask the user's preference per entity or as a global policy.

### Step 3: Translate ERD to DDL (one table at a time)
- **Input:** erd.md entities and attributes + chosen engine + delete policy
- **Action:** Convert each entity to CREATE TABLE with typed columns. Present ONE table's DDL at a time including PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL constraints.
- **Approval:** Ask "Does this table look correct? Anything to adjust?" before moving to the next table.
- **Output:** Approved CREATE TABLE statements for all entities
- **Integration:** feeds to data-dictionary skill

### Step 4: Index Strategy (per table)
- **Input:** Approved DDL + query patterns, cardinality estimates
- **Action:** After each table's DDL is approved, propose indexes for that table with rationale (query patterns, cardinality, expected performance). Specify index type (B-tree, Hash, BRIN).
- **Approval:** Ask the user to confirm indexes per table.
- **Output:** Index definitions with rationale
- **Integration:** informs Event Writer query optimization

### Step 5: Create Migration Plan
- **Input:** Current schema (if exists), new schema
- **Action:** Version migration scripts (V001_initial.sql, V002_add_column.sql); document rollback procedures.
- **Approval:** Present the migration plan for review.
- **Output:** Versioned migration scripts with dependencies
- **Integration:** deployment checklist for DevOps

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
  1. Verify directory exists: `docs/ets/projects/{project-slug}/data/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/data/database-spec.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/data/database-spec.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/data/erd.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/data/database-spec.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 11: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist. Display CLOSING SUMMARY.
- **Handoff:** Present the 3 next-step options from the Interaction Protocol. Let the user choose.
- **Output:** Document marked COMPLETE or DRAFT

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| erd.md missing | Critical | Auto-invoke erd skill, ask user | Block—cannot generate DDL without ERD |
| DDL syntax invalid | High | Validate against target database (ClickHouse/Postgres), fix syntax | Mark DRAFT, document syntax error |
| Missing foreign keys | Medium | Cross-reference ERD relationships, add FK constraints | Mark DRAFT, document missing constraints |
| Output validation fails | High | Mark DRAFT, document failures, proceed | Continue—downstream skills will refine |
