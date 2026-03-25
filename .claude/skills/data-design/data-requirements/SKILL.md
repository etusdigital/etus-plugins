---
name: data-requirements
description: >
  Use when starting data modeling, identifying entities, or defining what data the
  system needs. Also triggers on 'data requirements', 'what data do we need',
  'data sources', 'entity inventory', or when the data-agent begins its workflow.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Upstream: docs/ets/projects/{project-slug}/planning/prd.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** `docs/ets/projects/{project-slug}/planning/user-stories.md`
- Resolution: Verify existence. If missing, warn user and ask to generate upstream first or continue with generic output.

**ENRICHES:** `docs/ets/projects/{project-slug}/planning/prd.md`
- Resolution: Optional. If prd.md exists, extract additional features to identify secondary entities.

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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing data-requirements.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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
- New data model from scratch (no existing database)
- Multiple data domains with complex relationships
- Regulatory compliance requirements (PII, data retention)

**Use short version when:**
- Adding entities to an existing data model
- Simple feature with 1-2 new tables
- Even in short version, still include: Entity Inventory, Integrity Rules, and Volume Estimates for new entities

### Skill-Specific Interaction Patterns

- **Entity identification:** Propose an initial entity list derived from user stories and PRD features. Ask "Any entities missing? Any to remove?" before proceeding.
- **Data sources:** For each entity, suggest 2-3 possible source options (SDK, API, external feed, derived) and ask the user to confirm or adjust.
- **Volume calibration:** Propose volume ranges in three tiers (small, medium, large) with concrete numbers. Ask the user to calibrate for their expected scale.
- **Handoff options:** At completion, present:
  1. **Proceed to ERD** (Recommended) — Create Entity-Relationship Diagram from entity inventory
  2. **Refine requirements** — Adjust entities, sources, or volume estimates
  3. **Pause** — Save progress and return later

# Data Requirements Skill

## PURPOSE

Generate **data-requirements.md** — the first document in the data design pipeline. This document establishes the foundation for all subsequent data modeling by inventorying what entities the system must track, where data comes from, what integrity constraints apply, and how much volume the system must handle.

## CONTEXT LOADING

Load context using this 4-level fallback:

1. **$ARGUMENTS** — User provides upstream path: `docs/ets/projects/{project-slug}/planning/prd.md`
2. **Handoff** — Receive explicit upstream document path from planning-agent
3. **Scan** — If no path given, search `.claude/skills/planning/` for latest `prd.md`
4. **Ask** — If still missing, ask user: "What is the path to the PRD or feature spec?"

Read `references/template.md` for the document template and structure.

## PROCESS

1. **Extract Entities from PRD**
   - Review features in `prd.md` (PRD-F-*) and user stories
   - Identify nouns that represent business concepts: User, Event, Session, Domain, etc.
   - List each entity with its business purpose

2. **Identify Data Sources**
   - SDK interactions (frontend events, pageview data)
   - API inputs (batch endpoints, webhooks)
   - External feeds (GeoIP, bot databases)
   - Derived/computed data (analytics aggregates)

3. **Define Integrity Rules**
   - Required fields (NOT NULL constraints)
   - Unique constraints (natural keys, business identifiers)
   - Referential integrity (which entities depend on others)
   - Format/domain rules (email format, IP validation, UUID format)

4. **Estimate Volumes**
   - Events per hour/day
   - Users per account
   - Sessions per user
   - Data retention period (days/years)
   - Peak vs. average throughput

## OUTPUT

Generate `docs/ets/projects/{project-slug}/data/data-requirements.md` with:

- **Entity Inventory** — table of entities, descriptions, primary keys, importance level
- **Data Sources** — table of sources, input format, frequency, volume
- **Integrity Rules** — categorized by type (NOT NULL, UNIQUE, referential, format)
- **Volume Estimates** — throughput, cardinality, retention, peak loads
- **Dependencies** — which entities depend on others

## PIPELINE POSITION

**First in data design pipeline**

- ← Upstream: `docs/ets/projects/{project-slug}/planning/prd.md`
- → Feeds: `docs/ets/projects/{project-slug}/data/erd.md` (erd skill)

## INPUT VALIDATION

**From user-stories.md:** Verify at least 3 user stories present with When/Then clauses. Minimum 500 chars.

**From prd.md (if present):** Verify PRD-F-* IDs and feature descriptions. Use to cross-reference entities.

## OUTPUT VALIDATION

- [ ] Entity Inventory table present with ≥5 entities
- [ ] Data Sources table lists ≥3 sources (SDK, API, external feed)
- [ ] Integrity Rules organized by type (NOT NULL, UNIQUE, referential, format)
- [ ] Volume Estimates include events/hour, users, retention periods, peak throughput
- [ ] Dependencies section maps which entities depend on others
- [ ] Source Documents section present at top
- [ ] If any check fails → mark document as `<!-- STATUS: DRAFT -->` at top

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ data-requirements.md saved to `docs/ets/projects/{project-slug}/data/data-requirements.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document inventories entities, not traceable IDs)

→ Next step: erd — Create Entity-Relationship Diagram from entity inventory
  Run: /design or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Extract Entities from Upstream
- **Input:** user-stories.md When/Then clauses + prd.md features
- **Action:** Propose an initial entity list derived from user stories (nouns representing business concepts: User, Event, Session, Domain, etc.). Include business purpose for each.
- **Approval:** Present the proposed list and ask "Any entities missing? Any to remove?" Only proceed after user confirms.
- **Output:** Confirmed entity list with business purpose
- **Integration:** feeds to ERD skill

### Step 2: Identify Data Sources
- **Input:** Confirmed entity list + feature specs, integration requirements
- **Action:** For each entity, suggest 2-3 source options (SDK, API, webhook, external feed, derived). Present one entity at a time.
- **Approval:** Ask the user to confirm or adjust sources per entity. "Does this look right for [entity]?"
- **Output:** Data Sources table with format, frequency, volume
- **Integration:** informs Event Tracker architecture decisions

### Step 3: Define Integrity Rules
- **Input:** Feature requirements, compliance constraints
- **Action:** Propose integrity rules (NOT NULL, UNIQUE, referential, format) per entity group. Present one entity group at a time.
- **Approval:** Ask "Do these constraints capture the business rules? Anything to add or change?"
- **Output:** Integrity Rules matrix by constraint type
- **Integration:** becomes database-spec CHECK constraints

### Step 4: Estimate Volumes
- **Input:** Market analysis, product roadmap, SLA targets
- **Action:** Propose volume ranges in three tiers (small, medium, large) with concrete numbers for events/day, user cardinality, session duration, retention period.
- **Approval:** Ask the user to calibrate: "Which tier matches your expected scale?"
- **Output:** Volume Estimates with peak/average breakdown
- **Integration:** informs Event Tracker capacity planning

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
  2. Write the complete document to `docs/ets/projects/{project-slug}/data/data-requirements.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/data/data-requirements.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/planning/user-stories.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 9: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/data/data-requirements.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
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
| user-stories.md missing | Critical | Auto-invoke planning/discover, ask user to provide | Generic entities (User, Event, Session, Domain) |
| Entity count <5 | High | Expand with derived/computed entities, ask domain expert | Mark DRAFT, proceed with minimum viable set |
| Volume estimates vague | Medium | Gather from PM/analytics, reference benchmarks | Use order-of-magnitude estimates (e.g., "millions/day") |
| Output validation fails | High | Mark DRAFT, document failures in comment, proceed | Continue—data-agent will refine downstream |
