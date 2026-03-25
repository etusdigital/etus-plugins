---
name: arch-delta
description: >
  Use when documenting architecture changes for a specific feature, assessing
  impact, or identifying what needs to be modified. Also triggers on 'design
  delta', 'what changes', 'architecture changes for feature', 'what do we need
  to modify', or 'impact analysis'.
model: sonnet
version: 1.0.0
argument-hint: "[feature-brief path or feature name]"
compatibility: "Upstream: features/{feature-slug}/feature-brief.md. Optional: architecture-diagram.md, tech-spec.md, database-spec.md, api-spec.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (required — must exist):
- `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md` — The design delta documents changes for a specific feature. Without the feature brief, there is no scope to assess impact against.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md` — The chosen solution direction and remaining risks explain why these changes exist.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-status.md` — Canonical feature state for slug, tracking mode, next step, and linked docs.

**ENRICHES** (improves output — use if available):
- `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` — Existing architecture helps identify exactly what components are affected.
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — Existing NFRs and ADRs help assess whether changes violate constraints.
- `docs/ets/projects/{project-slug}/data/database-spec.md` — Existing schema helps define migration changes precisely.
- `docs/ets/projects/{project-slug}/implementation/api-spec.md` — Existing API endpoints help identify modifications vs. new endpoints.

**Resolution protocol:**
1. Check BLOCKS: does `features/{feature-slug}/feature-brief.md` exist?
2. If missing → INFORM user: "I need a feature brief to know what this feature does. Want me to create one first?" → if yes, invoke `feature-brief` skill → wait → continue
3. Check ENRICHES: load any existing architecture/data/api docs for context
4. If no ENRICHES found → proceed, but note that change assessment will be based on the feature brief alone (the user may need to describe the current architecture verbally)

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- Feature requires changes across multiple architectural layers
- Schema migrations or API contract changes are involved
- Impact analysis needs formal documentation for review

**Use short version when:**
- Feature adds logic within a single existing component
- No schema changes, no API changes, no new infrastructure
- Even in short version, still include: affected components list, change description, and risk assessment

## ARTIFACT SAVE RULE

**Why this matters:** The design delta is the bridge between feature scope (feature-brief) and implementation (impl-plan). Developers need this file to understand what to change and what to leave alone.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to `docs/ets/projects/{project-slug}/features/{feature-slug}/design-delta.md`
3. Displaying content in chat is not the same as saving — the file needs to exist on the filesystem for downstream skills to consume it
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only then propose the next step

**If the Write fails:** Report the error to the user and do not proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Design deltas involve technical decisions that benefit from focused discussion. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., migration strategy, API versioning approach), present 3-4 concrete options with tradeoffs. Highlight your recommendation.

3. **Propose approaches before generating** — Before generating any change section, propose the approach. For example: "For the database changes, I see two approaches: (A) add columns to existing table, (B) create a new table with a foreign key. I recommend A because..."

4. **Present output section-by-section** — Present each change section (API, DB, UI, Infra) individually. Ask "Does this capture all the changes? Anything missing?" and only proceed after approval. **Skip sections with no changes** — ask first: "Does this feature require [API/DB/UI/Infra] changes?"

5. **Track outstanding questions** — If a technical decision cannot be made now:
   - **Resolve before implementation** — Blocks the handoff.
   - **Deferred** — Noted with risk assessment.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options (see CLOSING SUMMARY).

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing design-delta at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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

Document ONLY what changes in the architecture for a specific feature — not a full architecture review. This is the Feature mode equivalent of running architecture-diagram + tech-spec + data-* + api-spec in Product mode, but focused exclusively on the delta: what is new, what is modified, what is removed.

The design delta answers three questions:
1. What components are affected by this feature?
2. What specific changes are needed in each component?
3. Is the change backward compatible and reversible?

## CONTEXT LOADING

Load context in this order of priority:

1. **Feature Status**: Read `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-status.md` first.
2. **$ARGUMENTS**: If the user passes `[feature-brief path]`, read that file directly.
3. **Feature Brief scan**: Check `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md`.
4. **Solution Discovery**: Read `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md`.
5. **Architecture scan**: Load existing architecture, tech-spec, database-spec, and api-spec documents for baseline comparison.
6. **User Interview**: If architecture docs don't exist, ask the user to describe the current system.

## CHANGE ASSESSMENT PROTOCOL

For each change category, follow this process:

### 1. Triage — Which sections apply?

Before diving into details, ask the user which areas this feature affects:

> "Based on the feature brief, I think this feature affects: [list]. Does this feature also require changes to any of these areas?
> - API (new or modified endpoints)
> - Database (new tables, columns, indexes)
> - UI (new screens or modified flows)
> - Infrastructure (new services, config, env vars)
>
> I'll skip any sections with no changes."

### 2. Per-Section Deep Dive

For each applicable section, follow the same pattern:

1. **Analyze** the feature brief requirements against existing architecture (if docs available)
2. **Propose** the specific changes with your reasoning
3. **Present** the changes in a structured format
4. **Ask for approval** before moving to the next section
5. **Skip** if the user confirms no changes are needed

### 3. Migration Assessment

After all change sections are approved, assess the overall migration:

- Is the database migration reversible?
- Is the API change backward compatible?
- Is a feature flag needed for gradual rollout?

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/features/{feature-slug}/design-delta.md` follows the template in `knowledge/template.md`.

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the design-delta document template and standard structure.

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] At least 1 change section populated (API, DB, UI, or Infra)
- [ ] Each change has a clear description of what is new vs. modified
- [ ] Migration plan section present with backward compatibility assessment
- [ ] Feature brief reference linked at top
- [ ] Sections with no changes are explicitly marked "No changes required"

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display the summary and offer multiple next steps:

```text
design-delta.md saved to `docs/ets/projects/{project-slug}/features/{feature-slug}/design-delta.md`

Status: [COMPLETE | DRAFT]
Changes documented: [list affected areas, e.g., API (2 new endpoints), DB (1 new table, 1 modified table), UI (1 new screen)]

What would you like to do next?

1. Create Implementation Plan (Recommended) — Break this into tasks with estimates
2. Go straight to implementation — Use /ce:work to start building
3. Refine this design delta — Review and adjust specific sections
4. Pause for now — Save and return later
```

Wait for the user's choice before proceeding. Do not auto-advance to the next skill.

## WORKFLOW

### Step 1: Context Loading
- **Input:** Feature brief (BLOCKS) + architecture docs (ENRICHES)
- **Action:** Read feature brief for scope and acceptance criteria. Load existing architecture docs for baseline.
- **Output:** Internal context with feature requirements and current system state
- **Checkpoint:** "I've loaded the feature brief for [feature name] and [N] existing architecture docs. Let me assess what changes are needed."

### Step 2: Change Triage
- **Input:** Step 1 context
- **Action:** Propose which change sections apply to this feature. Ask the user to confirm or adjust.
- **Output:** List of applicable change sections
- **Checkpoint:** "Based on the feature brief, I think we need changes in: [areas]. Does this sound right, or are there areas I'm missing?"

### Step 3: Section-by-Section Change Documentation
- **Input:** Approved section list + baseline architecture
- **Action:** For each applicable section, one at a time:
  1. **Propose approach** — Before generating, describe 2-3 ways to implement this change
  2. **Generate the change details** — Present structured changes (new, modified, removed)
  3. **Ask for approval** — "Does this capture all the changes for [section]?"
  4. **Incorporate feedback** — Revise if needed
  5. **Move to next section** — Only after approval
- **Output:** Approved change sections

### Step 4: Migration Assessment
- **Input:** All approved change sections
- **Action:** Assess overall migration risk:
  - Database migration reversibility
  - API backward compatibility
  - Feature flag recommendation
- **Checkpoint:** "Here's the migration assessment. Does this risk level feel right?"

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
  1. Use the same slug as the feature brief
  2. Verify directory exists: `docs/ets/projects/{project-slug}/features/{feature-slug}/` — create if missing
  3. Write the complete document to `docs/ets/projects/{project-slug}/features/{feature-slug}/design-delta.md` using the Write tool
- **Output:** File written to disk at the specified path

### Step 8: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/features/{feature-slug}/design-delta.md`) + paths to upstream documents (`docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md`, `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 9: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/features/{feature-slug}/design-delta.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 10: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist. Display CLOSING SUMMARY.
- **Handoff:** Present the next-step options. Let the user choose.
- **Output:** Document marked COMPLETE or DRAFT

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (feature-brief) | Critical | Offer to create feature brief first | Block execution until feature brief exists |
| No ENRICHES docs (no existing architecture) | Medium | Ask user to describe current architecture verbally | Proceed with feature-brief-only context |
| No changes needed in any section | Low | Confirm with user — if truly no changes, document "No architectural changes required" | Write minimal delta doc |
| Output validation fails | High | Mark as DRAFT, flag gaps | Proceed with DRAFT status |
| Slug mismatch with feature brief | Medium | Ask user to confirm the correct slug | Use feature brief slug |

## QUALITY LOOP

This skill supports iterative quality improvement when invoked by the orchestrator or user.

### Cycle

1. **Generate** — Produce initial document following WORKFLOW steps
2. **Self-Evaluate** — Score the output against OUTPUT VALIDATION checklist
   - Calculate: completeness % = (passing checks / total checks) x 100
   - If completeness >= 90% → mark COMPLETE, exit loop
   - If completeness < 90% → proceed to step 3
3. **Identify Issues** — List each failing check with specific gap description
4. **Improve** — Address each issue, regenerate affected sections only
5. **Re-Evaluate** — Score again against OUTPUT VALIDATION
   - If improved by < 5% from previous iteration → diminishing returns, mark DRAFT with notes
   - If completeness >= 90% → mark COMPLETE, exit loop
   - If max iterations (3) reached → mark DRAFT with iteration log
6. **Report** — Log to stdout: iteration count, score progression, remaining gaps if any

### Termination Conditions

| Condition | Action | Document Status |
|-----------|--------|-----------------|
| Completeness >= 90% | Exit loop | COMPLETE |
| Improvement < 5% between iterations | Exit loop (diminishing returns) | DRAFT + notes |
| Max 3 iterations reached | Exit loop | DRAFT + iteration log |
