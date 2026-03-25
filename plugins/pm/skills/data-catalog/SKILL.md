---
name: data-catalog
description: >
  Use when creating a data catalog, documenting data ownership, or tracking data
  lineage. Also triggers on 'data catalog', 'asset inventory', 'data governance',
  'data lineage', 'retention policies', or 'who owns this data'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Upstream: docs/ets/projects/{project-slug}/data/data-dictionary.md, docs/ets/projects/{project-slug}/data/data-flow-diagram.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** `docs/ets/projects/{project-slug}/data/database-spec.md`, `docs/ets/projects/{project-slug}/data/data-dictionary.md`, `docs/ets/projects/{project-slug}/data/data-flow-diagram.md`
- Resolution: Verify all three exist with content. If any missing, warn and ask to generate upstream first.

**ENRICHES:** None—data catalog is the consolidation of all data-design outputs.

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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing data-catalog.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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
- First data catalog creation (consolidating all data assets)
- Data governance audit or compliance review
- Organization needs formal data ownership and lineage mapping

**Use short version when:**
- Adding new assets from a recently created table or service
- Updating classification or retention for existing assets
- Even in short version, still include: Asset Registry entry, Classification, and Retention for new assets

### Skill-Specific Interaction Patterns

- **Data classification:** Propose a sensitivity classification per entity (PII, sensitive, internal, public) with reasoning for each. Ask the user to confirm or adjust per entity.
- **Retention policy:** For each data type, propose 3 retention options (e.g., 30 days, 1 year, indefinite) with compliance and cost tradeoffs. Let the user choose per data type or set a global default.
- **Ownership assignment:** Ask ownership questions per dataset — "Who owns User data? Who owns Event data?" — one at a time.
- **Handoff options:** At completion, present:
  1. **Design phase complete — proceed to gate** (Recommended) — Run Implementation Readiness Gate validation
  2. **Refine catalog** — Adjust classification, retention, or ownership
  3. **Pause** — Save progress and return later

# Data Catalog Skill

## PURPOSE

Generate **data-catalog.md** — the final and comprehensive inventory of all data assets across the system. Consolidates data definitions, classifications, ownership, lineage, and governance policies into a searchable registry. This is the end of the data design pipeline and the authoritative reference for data governance.

## CONTEXT LOADING

Load context using this 4-level fallback:

1. **$ARGUMENTS** — User provides upstream paths: `docs/ets/projects/{project-slug}/data/data-dictionary.md` and `docs/ets/projects/{project-slug}/data/data-flow-diagram.md`
2. **Handoff** — Receive both document paths from data-agent
3. **Scan** — If no paths given, search `docs/ets/projects/{project-slug}/data/` for both documents
4. **Ask** — If still missing, ask user: "What are the paths to the data dictionary and data flow diagram?"

Read `references/template.md` for asset registry format and governance policy template.

## PROCESS

1. **Compile Asset Inventory**
   - Extract all tables from database-spec
   - Extract all fields (dict.*) and events (ev.*) from data-dictionary
   - Add computed views, caches, and external data feeds

2. **Classify Sensitivity**
   - Identify PII fields (email, phone, IP, location)
   - Classify by sensitivity tier: public, internal, confidential, restricted
   - Document encryption/masking requirements

3. **Assign Ownership**
   - Data owner (accountable for quality and governance)
   - Steward (operational management)
   - Contact for access requests and incidents

4. **Trace Lineage**
   - Source system for each asset (SDK, API, external feed)
   - Transformation path (process that creates/modifies it)
   - Downstream consumers (processes, reports, exports)

5. **Define Retention**
   - Data retention period (days/months/years)
   - Archival policy (move to cold storage, delete, anonymize)
   - Compliance requirements (GDPR, CCPA, regional regulations)

## OUTPUT

Generate `docs/ets/projects/{project-slug}/data/data-catalog.md` with:

- **Asset Registry** — table of all assets (tables, fields, events) with owner and sensitivity
- **Classification Matrix** — assets grouped by sensitivity, lineage, and retention
- **Lineage Graph** — source → transformation → consumer relationships
- **Retention Schedule** — asset name, retention period, archival action, compliance basis
- **Governance Policies** — access controls, encryption requirements, incident procedures

## PIPELINE POSITION

**Final in data design pipeline**

- ← Upstream: `docs/ets/projects/{project-slug}/data/data-dictionary.md` + `docs/ets/projects/{project-slug}/data/data-flow-diagram.md`
- → End of data pipeline: no downstream data-design skills

## INPUT VALIDATION

**From database-spec.md:** Verify CREATE TABLE statements for ≥5 tables. Minimum 500 chars.

**From data-dictionary.md:** Verify dict.* and ev.* identifiers with ≥10 field definitions. Minimum 500 chars.

**From data-flow-diagram.md:** Verify Mermaid flowchart and process descriptions present. Minimum 500 chars.

## OUTPUT VALIDATION

- [ ] Asset Registry table lists all tables from database-spec with owner and sensitivity tier
- [ ] Classification Matrix groups assets by sensitivity (public, internal, confidential, restricted)
- [ ] Lineage Graph shows source→transformation→consumer relationships from data-flow-diagram
- [ ] All tables from database-spec mapped to asset entries
- [ ] All dict.* and ev.* identifiers mapped to asset ownership
- [ ] Retention Schedule specifies retention period, archival action, and compliance basis
- [ ] Governance Policies document access controls, encryption, incident procedures
- [ ] Source Documents section present at top
- [ ] If any check fails → mark document as `<!-- STATUS: DRAFT -->` at top

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ data-catalog.md saved to `docs/ets/projects/{project-slug}/data/data-catalog.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document consolidates data assets, not traceable IDs)

→ Next step: validate-gate (Design Gate) or parallel completion — Data pipeline complete
  Run: /validate or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Compile Asset Inventory
- **Input:** database-spec.md (tables), data-dictionary.md (fields, events)
- **Action:** Extract all tables from DDL and all dict.*, ev.* identifiers from dictionary. Present the complete asset list.
- **Approval:** Ask "Is this inventory complete? Any assets missing?"
- **Output:** Confirmed asset list with type (table, field, event, view, cache)
- **Integration:** foundation for registry

### Step 2: Classify Sensitivity (per entity)
- **Input:** Business requirements, compliance constraints (GDPR, CCPA)
- **Action:** Propose a sensitivity classification per entity (PII, sensitive, internal, public) with reasoning for each. Present per-entity classifications.
- **Approval:** Ask "Does this classification look right for [entity]?" per entity or in groups.
- **Output:** Sensitivity Classification table with encryption/masking requirements
- **Integration:** informs access control policies

### Step 3: Assign Ownership (per dataset)
- **Input:** Organizational structure, domain responsibilities
- **Action:** Ask ownership questions per dataset — "Who owns User data? Who owns Event data?" — one dataset at a time.
- **Approval:** Wait for the user's answer before asking about the next dataset.
- **Output:** Ownership Registry with owner name, contact, responsibilities
- **Integration:** enables data governance and incident response

### Step 4: Trace Lineage
- **Input:** data-flow-diagram.md flows, database-spec.md tables, data-dictionary.md definitions
- **Action:** Map source system to transformation to consumer for each asset; document transformation logic.
- **Approval:** Present the lineage graph for review.
- **Output:** Lineage Graph with source, process, and downstream consumer relationships
- **Integration:** enables impact analysis for schema changes

### Step 5: Define Retention (per data type)
- **Input:** Business policy, compliance requirements (GDPR Article 5, CCPA)
- **Action:** For each data type, propose 3 retention options (e.g., 30 days, 1 year, indefinite) with compliance and cost tradeoffs. Let the user choose per data type or set a global default.
- **Approval:** Ask per data type or present grouped for efficiency.
- **Output:** Retention Schedule and Governance Policies tables
- **Integration:** informs data lifecycle management and audit procedures

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
  2. Write the complete document to `docs/ets/projects/{project-slug}/data/data-catalog.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/data/data-catalog.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/data/database-spec.md`, `docs/ets/projects/{project-slug}/data/data-dictionary.md`, `docs/ets/projects/{project-slug}/data/data-flow-diagram.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/data/data-catalog.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
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
| Any upstream document missing | Critical | Auto-invoke missing upstream skills | Block—cannot consolidate without all inputs |
| Asset count <5 tables | High | Review database-spec for completeness, expand if needed | Mark DRAFT, document minimum viable set |
| Ownership missing for asset | Medium | Ask domain expert or PM to assign owner | Mark DRAFT, document ownership gaps |
| Output validation fails | High | Mark DRAFT, document failures, proceed | Publish as DRAFT—governance team reviews |
