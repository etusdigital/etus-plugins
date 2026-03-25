---
name: data-flow
description: >
  Use when mapping data flows, understanding how data moves through the system, or
  documenting ETL processes. Also triggers on 'data flow diagram', 'how does data
  move', 'ETL flows', 'integration paths', or 'process-to-storage mapping'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Upstream: docs/ets/projects/{project-slug}/architecture/architecture-diagram.md, docs/ets/projects/{project-slug}/data/database-spec.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** `docs/ets/projects/{project-slug}/data/erd.md`, `docs/ets/projects/{project-slug}/data/data-dictionary.md`
- Resolution: Verify both exist. If either missing, warn and ask to generate upstream first.

**ENRICHES:** `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md`
- Resolution: Optional. If architecture diagram exists, align process names and component boundaries.

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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing data-flow-diagram.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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
- New system with multiple data pipelines (ETL, streaming, batch)
- Complex integration with external systems (webhooks, feeds, APIs)
- Data flows through >3 processing stages

**Use short version when:**
- Adding a single new data flow to existing diagram
- Documenting a simple request-response API path
- Even in short version, still include: updated Mermaid flowchart and Process Description for the new flow

### Skill-Specific Interaction Patterns

- **Flow identification:** Propose the set of data flows derived from the architecture diagram and user stories. Ask "Are these the right flows? Any missing or unnecessary?" before diagramming.
- **Timing per flow:** For each data flow, ask whether it should be real-time or batch, and present the tradeoffs (latency vs. throughput, cost vs. freshness). One flow at a time.
- **Diagram review:** After building the complete Mermaid flowchart from approved flows, present the full diagram for review before saving.
- **Handoff options:** At completion, present:
  1. **Proceed to Data Catalog** (Recommended) — Compile asset inventory with classification and lineage
  2. **Refine flows** — Adjust data paths, timing, or volume annotations
  3. **Pause** — Save progress and return later

# Data Flow Diagram Skill

## PURPOSE

Generate **data-flow-diagram.md** — a visual map of how data flows between system components, processes, and storage systems. Shows ingestion paths, transformation pipelines, and output destinations. Bridges architecture and data design by showing data movement end-to-end.

## CONTEXT LOADING

Load context using this 4-level fallback:

1. **$ARGUMENTS** — User provides upstream paths: `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` and `docs/ets/projects/{project-slug}/data/database-spec.md`
2. **Handoff** — Receive architecture-diagram.md and database-spec.md paths from architecture-agent + data-agent
3. **Scan** — If no paths given, search `docs/ets/projects/{project-slug}/` for both documents
4. **Ask** — If still missing, ask user: "What are the paths to the architecture diagram and database spec?"

Read `references/template.md` for data flow diagram Mermaid format and process notation.

## PROCESS

1. **Map Data Sources**
   - Identify all data input points (SDKs, APIs, webhooks, external feeds)
   - Document ingestion format and frequency
   - Note any pre-processing at source

2. **Trace Processing Paths**
   - Identify transformation processes from architecture (normalizer, enricher, etc.)
   - Document each step's input and output data shape
   - Note filtering, aggregation, or enrichment rules

3. **Connect to Storage**
   - Map processes to database tables from database-spec
   - Identify real-time vs. batch ingestion
   - Document archival paths (data lake, cold storage)

4. **Draw Mermaid Flowchart**
   - Source → Process → Store relationships
   - Parallel and conditional flows
   - Data volume and frequency annotations

## OUTPUT

Generate `docs/ets/projects/{project-slug}/data/data-flow-diagram.md` with:

- **Mermaid Flowchart** — data flows from sources through processes to stores
- **Process Descriptions** — purpose and transformation logic of each process
- **Data Transformations** — input schema → output schema for each step
- **Volume & Frequency** — throughput estimates for each flow segment

## PIPELINE POSITION

**Fifth in data design pipeline**

- ← Upstream: `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` + `docs/ets/projects/{project-slug}/data/database-spec.md`
- → Feeds: `docs/ets/projects/{project-slug}/data/data-catalog.md`

## INPUT VALIDATION

**From erd.md:** Verify entities present and Mermaid diagram renders. Minimum 500 chars.

**From data-dictionary.md:** Verify dict.* field identifiers and field definitions present. Minimum 500 chars.

**From architecture-diagram.md (if present):** Verify component names for process alignment.

## OUTPUT VALIDATION

- [ ] Mermaid flowchart renders without syntax errors
- [ ] All entities from ERD appear as storage nodes (database, cache, file)
- [ ] Data sources labeled (SDK, API, webhook, external feed)
- [ ] Data sinks labeled (ClickHouse, R2, data lake, cold storage)
- [ ] Processes labeled with transformation logic (Normalizer, Enricher, etc.)
- [ ] Data flows labeled with dict.* field names or entity names
- [ ] Volume & Frequency annotations present on flows
- [ ] Source Documents section present at top
- [ ] If any check fails → mark document as `<!-- STATUS: DRAFT -->` at top

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ data-flow-diagram.md saved to `docs/ets/projects/{project-slug}/data/data-flow-diagram.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document maps data flows, not traceable IDs)

→ Next step: data-catalog — Compile asset inventory with classification and lineage
  Run: /design or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Propose Data Flows
- **Input:** architecture-diagram.md + user-stories.md + data-dictionary.md
- **Action:** Propose the set of data flows derived from the architecture and user stories. List each flow with source, destination, and purpose.
- **Approval:** Ask "Are these the right flows? Any missing or unnecessary?" before proceeding.
- **Output:** Confirmed flow list

### Step 2: Timing Decisions (per flow)
- **Input:** Confirmed flow list + NFR targets
- **Action:** For each data flow, ask whether it should be real-time or batch. Present the tradeoffs (latency vs. throughput, cost vs. freshness) for this specific flow. One flow at a time.
- **Approval:** Wait for the user's answer before asking about the next flow.
- **Output:** Flow list with timing annotations

### Step 3: Map Data Sources
- **Input:** Feature specs, integration requirements, architecture diagram
- **Action:** Enumerate all input points (SDK events, batch API, webhooks, GeoIP feeds); note format and frequency.
- **Approval:** Present the sources table for review.
- **Output:** Data Sources table with ingestion method, format, frequency, volume
- **Integration:** informs Event Tracker endpoint design

### Step 4: Trace Processing Paths
- **Input:** architecture-diagram.md services, domain logic from prd
- **Action:** Map transformation processes (Normalizer, Enricher, Projector); document input/output schemas.
- **Approval:** Present the process flow and ask "Does this processing pipeline look right?"
- **Output:** Process flow with schema transformations labeled
- **Integration:** validates architecture components against data model

### Step 5: Draw and Review Mermaid Flowchart
- **Input:** All confirmed sources, processes, storage, flows with labels and volume
- **Action:** Create Mermaid flowchart with source-to-process-to-store relationships; annotate volumes and timing.
- **Approval:** Present the full diagram for review. Ask "Does this diagram capture the data flows correctly? Anything to adjust?"
- **Output:** Approved Mermaid diagram
- **Integration:** feeds to data-catalog for lineage documentation

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
  2. Write the complete document to `docs/ets/projects/{project-slug}/data/data-flow-diagram.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/data/data-flow-diagram.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/data/erd.md`, `docs/ets/projects/{project-slug}/data/data-dictionary.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/data/data-flow-diagram.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
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
| erd.md or data-dictionary.md missing | Critical | Auto-invoke missing upstream skills | Block—cannot generate flows without entity/field definitions |
| Mermaid syntax errors | High | Debug flowchart syntax, validate in Mermaid Live | Mark DRAFT, document syntax error |
| Process not in architecture diagram | Medium | Add process to both architecture and flow diagram or document discrepancy | Mark DRAFT, note alignment gap |
| Output validation fails | High | Mark DRAFT, document failures, proceed | Continue—data-catalog will consolidate lineage |
