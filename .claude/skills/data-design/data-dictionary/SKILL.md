---
name: data-dictionary
description: >
  Use when defining field semantics, event definitions, or domain terminology.
  Also triggers on 'data dictionary', 'what does this field mean', 'field
  definitions', 'event catalog', 'enumerated types', or 'domain glossary'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Upstream: docs/ets/projects/{project-slug}/data/erd.md, docs/ets/projects/{project-slug}/data/database-spec.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** `docs/ets/projects/{project-slug}/data/database-spec.md`
- Resolution: Verify existence and CREATE TABLE statements present. If missing, warn and ask to generate upstream first.

**ENRICHES:** None—data dictionary is purely derived from DDL and business semantics.

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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing data-dictionary.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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
- New data model with many entities needing semantic definitions
- Domain with complex business terminology or enumerated types
- Compliance requirements demand field-level documentation

**Use short version when:**
- Adding fields to existing entities
- Defining events for a single new feature
- Even in short version, still include: dict.* definitions for new fields and ev.* definitions for new events

### Skill-Specific Interaction Patterns

- **Field definitions — per entity group:** Present dict.* field definitions one entity group at a time (e.g., all User fields, then all Event fields). Ask "Does this entity group look complete? Anything to adjust?" before moving to the next.
- **Event suggestions:** Suggest events (ev.*) based on user stories and business processes. Ask which events to include and which to skip before documenting.
- **Validation rules:** For each field, propose validation rules with options (e.g., email: RFC 5322 strict vs. loose, max length 254 vs. 320). Let the user choose per field or set a global policy.
- **Handoff options:** At completion, present:
  1. **Proceed to Data Flow Diagram** (Recommended) — Map data flows between components
  2. **Refine dictionary** — Adjust field definitions, add events, change validation rules
  3. **Pause** — Save progress and return later

# Data Dictionary Skill

## PURPOSE

Generate **data-dictionary.md** — the Single Source of Truth for all field definitions (dict.*), event definitions (ev.*), and enumerated types. Documents the semantic meaning, valid values, and business context of every field and event in the data model. No other document may define the meaning of dict.* or ev.* identifiers.

## CONTEXT LOADING

Load context using this 4-level fallback:

1. **$ARGUMENTS** — User provides upstream path: `docs/ets/projects/{project-slug}/data/erd.md` or `docs/ets/projects/{project-slug}/data/database-spec.md`
2. **Handoff** — Receive erd.md + database-spec.md paths from data-agent
3. **Scan** — If no paths given, search `docs/ets/projects/{project-slug}/data/` for both documents
4. **Ask** — If still missing, ask user: "What are the paths to the ERD and database spec?"

Read `references/template.md` for dict.* and ev.* identifier format and definition structure.

## SST RULE

**Why this matters:** All dict.* and ev.* identifier definitions should appear only in data-dictionary.md. Keeping field and event semantics in a single location prevents conflicting definitions and ensures gate approval passes the SST check.

## ID FORMAT

- **Field identifiers:** `dict.[domain].[field_name]` (e.g., `dict.user.email`, `dict.event.timestamp`)
- **Event identifiers:** `ev.[domain].[action]` (e.g., `ev.pageview.view`, `ev.checkout.abandon`)

## PROCESS

1. **Extract Fields from Database Spec**
   - List all columns from CREATE TABLE statements
   - Organize by business domain (user, event, session, etc.)
   - Assign dict.* IDs to each field

2. **Define Field Semantics**
   - Business meaning and use case
   - Data type and valid range/format
   - Enumerated values if applicable
   - Deprecated status and migration notes

3. **Document Events**
   - Identify event types from domain and business process
   - Assign ev.* IDs to each event
   - Document trigger conditions and required fields

4. **Create Reference Tables**
   - Enumeration catalog (status values, categories)
   - Deprecated identifiers and replacement IDs
   - Cross-reference matrix: dict.* → database column mapping

## OUTPUT

Generate `docs/ets/projects/{project-slug}/data/data-dictionary.md` with:

- **Field Definitions** — dict.* identifier, type, business meaning, valid values
- **Event Definitions** — ev.* identifier, trigger condition, required fields
- **Enumerations** — catalog of valid values for status, category, type fields
- **Deprecation Registry** — old identifiers, replacement IDs, sunset date
- **dict.* to Column Mapping** — cross-reference for traceability

## PIPELINE POSITION

**Fourth in data design pipeline**

- ← Upstream: `docs/ets/projects/{project-slug}/data/erd.md` + `docs/ets/projects/{project-slug}/data/database-spec.md`
- → Feeds: `docs/ets/projects/{project-slug}/data/data-flow-diagram.md`, `docs/ets/projects/{project-slug}/data/data-catalog.md`

## INPUT VALIDATION

**From database-spec.md:** Verify CREATE TABLE statements present for ≥5 tables with columns. Extract all column names and types.

## OUTPUT VALIDATION

- [ ] dict.* field identifiers present for all columns (format: dict.[domain].[field_name])
- [ ] ev.* event identifiers present for all events (format: ev.[domain].[action])
- [ ] Field definitions include data type, valid range/format, and business meaning
- [ ] Validation rules per field: required, format/regex, min/max, default, valid example, invalid example, behavior on invalid input
- [ ] Enumeration catalog lists all status/category values per field
- [ ] Deprecation Registry documents old identifiers and replacements
- [ ] dict.* to Column Mapping cross-reference present
- [ ] Source Documents section present at top
- [ ] **SST rule verified:** Field/event definitions appear ONLY here, nowhere else
- [ ] If any check fails → mark document as `<!-- STATUS: DRAFT -->` at top

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ data-dictionary.md saved to `docs/ets/projects/{project-slug}/data/data-dictionary.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list dict.* and ev.* identifiers, e.g., dict.user.email, dict.event.timestamp, ev.pageview.view]

→ Next step: data-flow-diagram — Map data flows between components
  Run: /design or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Extract Fields from Database Spec
- **Input:** database-spec.md CREATE TABLE statements
- **Action:** List all columns by domain (user, event, session, etc.); assign dict.* IDs
- **Output:** dict.* identifier registry by domain
- **Integration:** feeds to data-catalog skill

### Step 2: Define Field Semantics (per entity group)
- **Input:** Column definitions, business requirements, integrity rules
- **Action:** Present dict.* field definitions one entity group at a time (e.g., all User fields, then all Event fields). Include type, valid range/format, business meaning, enumerations.
- **Approval:** Ask "Does this entity group look complete? Anything to adjust?" before moving to the next.
- **Output:** Field Definitions table with dict.* to column mapping
- **Integration:** consumed by data-flow-diagram for schema labeling

### Step 3: Define Validation Rules (per field)
- **Input:** Field definitions + business constraints
- **Action:** For each dict.* field, document:
  - **Required:** yes / no
  - **Format/regex:** validation pattern (e.g., `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` for email)
  - **Min/max:** length or value range (e.g., min: 1, max: 255 for string; min: 0, max: 999999.99 for decimal)
  - **Default value:** what the system uses if no value is provided (e.g., `""`, `0`, `null`, `now()`)
  - **Valid example:** a concrete value that passes validation (e.g., `"user@example.com"`)
  - **Invalid example:** a concrete value that fails validation (e.g., `"user@"`, `""`)
  - **Behavior on invalid input:** what the system does (e.g., "400 Bad Request with field-level error: `{field}: {message}`")
- Propose validation rules with options (e.g., email: RFC 5322 strict vs. loose, max length 254 vs. 320). Let the user choose per field or set a global policy.
- **Approval:** Present rules per entity group and ask for confirmation.

### Step 4: Document Events
- **Input:** Business processes, user journeys, user stories
- **Action:** Suggest events (ev.*) based on user stories and business processes. Present the proposed event list.
- **Approval:** Ask "Which events should we include? Any to add or skip?" before documenting triggers and required fields.
- **Output:** Event Definitions table with ev.* IDs and required fields
- **Integration:** informs SDK event schema and Event Tracker validation

### Step 5: Create Reference Tables
- **Input:** Enumeration values, deprecated fields, cross-references
- **Action:** Build Enumerations catalog and Deprecation Registry
- **Approval:** Present for review.
- **Output:** Reference tables with mappings
- **Integration:** enables query filters and API response validation

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
  2. Write the complete document to `docs/ets/projects/{project-slug}/data/data-dictionary.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/data/data-dictionary.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/data/database-spec.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/data/data-dictionary.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
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
| database-spec.md missing | Critical | Auto-invoke database-spec skill, ask user | Block—cannot generate dict without DDL |
| dict.* ID collision | Medium | Rename duplicates with disambiguating suffix (e.g., dict.event.name_v2) | Mark DRAFT, document collision |
| Field type mismatch | Medium | Cross-check with database-spec column types, correct | Mark DRAFT, document discrepancy |
| Output validation fails | High | Mark DRAFT, document failures, proceed | Continue—data-catalog will consolidate |
