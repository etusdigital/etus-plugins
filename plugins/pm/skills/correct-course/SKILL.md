---
name: correct-course
description: >
  Use when requirements change mid-sprint, scope needs adjusting, or a significant
  pivot is needed. Generates a Sprint Change Proposal that documents what changed,
  impact analysis, and updates all affected documents. Also triggers on 'change request',
  'scope change', 'pivot', 'requirements changed', 'correct course', or 'mid-sprint change'.
model: opus
version: 1.0.0
argument-hint: "[change description]"
compatibility: "Optional: external execution adapter integration (for example, a Linear adapter). Reads `docs/ets/.memory/linear-mapping.md` and `docs/ets/projects/{project-slug}/state/execution-sync.yaml` when present."
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (at least one must exist — cannot correct course if nothing exists):
- At least one of: `docs/ets/projects/{project-slug}/planning/prd.md`, `docs/ets/projects/{project-slug}/planning/user-stories.md`, `docs/ets/projects/{project-slug}/implementation/implementation-plan.md`
- If none of these exist, there is nothing to change. Halt with: "No existing documents found. Use /start-project or /plan to create documents first."

**ENRICHES** (read if available to assess impact):
- `docs/ets/projects/{project-slug}/planning/prd.md` — Feature definitions (PRD-F-#)
- `docs/ets/projects/{project-slug}/planning/user-stories.md` — Acceptance criteria (US-#)
- `docs/ets/projects/{project-slug}/planning/ost.md` — Opportunity ranking
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — NFRs and ADRs
- `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` — System structure
- `docs/ets/projects/{project-slug}/implementation/implementation-plan.md` — Tasks (impl-#)
- `docs/ets/projects/{project-slug}/state/execution-status.yaml` — Optional execution projection
- `docs/ets/projects/{project-slug}/state/execution-sync.yaml` — Optional adapter sync state, projections, and conflicts
- `docs/ets/.memory/linear-mapping.md` — Human-readable Linear issue mappings

**Resolution protocol:**
1. Scan `docs/ets/projects/{project-slug}/` for all existing documents
2. If zero documents found → halt (nothing to change)
3. Load all found documents to build a complete picture of the current state
4. Check `state/execution-sync.yaml` first, then `.memory/linear-mapping.md`, for execution adapter integration status

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a change navigator — stay factual, analyze impact objectively, and help the user make informed decisions about how to adapt.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Change management requires careful understanding — don't rush through the interview. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., impact scope, recommended approach), present 3-4 concrete options with a brief description of each. Highlight your recommendation.

3. **Present impact analysis before proposing changes** — Before suggesting any document updates, present the full impact analysis and let the user understand the scope of change.

4. **Section-by-section approval** — Present each impact area one at a time. Ask "Does this assessment look right? Anything I'm missing?" before moving to the next.

5. **Track outstanding questions** — If something cannot be answered now, classify it:
   - **Resolve before applying changes** — This blocks the update.
   - **Deferred to next sprint** — Noted and carried forward.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options.

7. **Resume existing work** — Before starting, check if a change proposal already exists for this topic at the expected path. If it does, ask the user: "I found an existing change proposal at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

8. **Assess if full process is needed** — If the user's change description is clear and specific with obvious impact scope, don't force the full interview. Confirm understanding briefly and offer to skip directly to impact analysis. Only run the full interactive process when there's genuine ambiguity to resolve.

## PURPOSE

Navigate mid-sprint or mid-project changes with a structured Sprint Change Proposal. When requirements change, scope shifts, or a pivot is needed, this skill analyzes the impact across all existing ETUS documents, generates a formal change proposal, and — if approved — updates the affected documents. This prevents ad-hoc changes that create inconsistencies between documents and ensures traceability is maintained.

## CONTEXT LOADING

Load context in this order of priority:

1. **$ARGUMENTS**: If the user passes `[change description]`, use it as the initial change context.
2. **Document Scan**: Scan `docs/ets/projects/{project-slug}/` recursively for all existing documents. Build a map of what exists and what IDs are in use.
3. **Execution Adapter Mapping**: Check `docs/ets/projects/{project-slug}/state/execution-sync.yaml` for sync state and `docs/ets/.memory/linear-mapping.md` for readable mappings.
4. **User Interview**: Begin the change assessment interview interactively.

## INTERVIEW PROTOCOL

This interview is short — 3 focused questions asked one at a time.

### Question 1: What Changed

Ask alone, one message:
> "What changed? Describe the change, new requirement, or problem that triggered this."

Wait for the answer. Extract: change description, trigger source (stakeholder request, technical discovery, market shift, etc.), urgency.

If `$ARGUMENTS` was provided and is sufficiently detailed, confirm understanding instead of asking:
> "I understand the change is: [summary]. Is that correct, or should I adjust?"

### Question 2: Criticality

Ask alone, one message:
> "How critical is this change?
> (A) Must change now — blocks current sprint
> (B) Should change soon — affects next sprint
> (C) Can wait — backlog for future"

Wait for the answer. This determines urgency and recommended approach.

### Question 3: Scope of Impact

After reading existing documents, propose 2-3 impact assessments based on what you found:
> "Based on the existing documents, I see the following potential impact areas:
> (A) [assessment 1 — e.g., 'Affects PRD-F-3 and its 4 user stories, plus 6 impl tasks']
> (B) [assessment 2 — e.g., 'Broader: also requires architecture changes to support new auth flow']
> (C) [assessment 3 — e.g., 'Contained: only affects implementation timeline, no design changes']
>
> Which assessment matches your understanding? Or describe a different scope."

## IMPACT ANALYSIS

After the interview, perform automatic impact analysis by reading each existing document.

For each document found in `docs/ets/projects/{project-slug}/`, check if the change affects it:

| Document | Check |
|----------|-------|
| prd.md | Does a PRD-F-# need to change? New feature? Remove feature? |
| user-stories.md | Do US-# acceptance criteria change? New stories needed? |
| ost.md | Does the opportunity ranking change? |
| tech-spec.md | Do NFRs or ADRs change? |
| architecture-diagram.md | Does the architecture change? |
| implementation-plan.md | Do impl-# tasks change? New tasks? Remove tasks? |
| state/execution-status.yaml | Does the current execution projection need re-planning? |
| api-spec.md | Do API endpoints change? |
| database-spec.md | Does the schema change? |
| data-dictionary.md | Do dict.* or ev.* definitions change? |

**For each affected document:**
- Identify WHICH specific IDs are impacted (e.g., PRD-F-3, US-7, US-8, impl-12)
- Describe WHAT changes (old → new)
- Estimate effort (Low/Med/High)

**Present the impact analysis as a table** and ask the user: "Does this impact assessment look right? Any areas I'm missing or over-estimating?"

## OUTPUT FORMAT

The generated Sprint Change Proposal is saved to:
`docs/ets/projects/{project-slug}/implementation/change-proposal-{slug}.md`

Where `{slug}` is a kebab-case version of the change description (e.g., `change-proposal-add-2fa-requirement.md`).

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the Sprint Change Proposal template and structure.

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Change description is clear and specific
- [ ] Criticality is documented (Must/Should/Can wait)
- [ ] Impact analysis covers all existing documents
- [ ] Each affected document has specific IDs listed (PRD-F-#, US-#, impl-#, etc.)
- [ ] Recommended approach is justified with effort/risk assessment
- [ ] Detailed changes section shows old → new for each affected item
- [ ] Decision section has approval checkboxes

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
change-proposal-{slug}.md saved to `docs/ets/projects/{project-slug}/implementation/change-proposal-{slug}.md`

Status: [COMPLETE | DRAFT]
Documents affected: [count] | IDs impacted: [list key IDs]
Criticality: [Must/Should/Can wait]
Recommended approach: [Direct adjustment / Rollback to phase / Re-plan sprint / Accept as tech debt]
```

Then present these options using AskUserQuestion (or as a numbered list if AskUserQuestion is unavailable):

1. **Apply changes to documents (Recommended)** — Update all affected docs automatically, maintaining traceability
2. **Apply changes manually** — User will update docs themselves using the proposal as a guide
3. **Update execution adapter too** — If an execution adapter is active, also update/create/close external items and refresh the local projection
4. **Discard proposal** — Change is not needed, delete the proposal file

Wait for the user to choose before taking any action. Do not auto-proceed.

## WORKFLOW

### Step 1: Context Loading & Existence Check
- **Input:** `$ARGUMENTS` (optional), existing documents in `docs/ets/projects/{project-slug}/`
- **Action:** Scan for all existing ETUS documents. Build a map of document → IDs. Check if at least one of (prd.md, user-stories.md, implementation-plan.md) exists.
- **Output:** Document inventory with ID map
- **Halt condition:** If no documents exist, inform the user and exit.

### Step 2: Change Interview (one question at a time)
- **Input:** User responses (interactive)
- **Action:** Run the 3-question INTERVIEW PROTOCOL. Ask one question per message, wait for answers.
- **Output:** Change description, criticality, scope assessment

### Step 3: Automatic Impact Analysis
- **Input:** Change description + all existing documents
- **Action:** Read each existing document. For each, determine if the change affects it. Identify specific IDs impacted, describe what changes, estimate effort.
- **Output:** Impact analysis table
- **Checkpoint:** Present the table and ask: "Does this impact assessment look right?"

### Step 4: Recommended Approach
- **Input:** Impact analysis + criticality
- **Action:** Based on the scope and criticality, recommend one of:
  - **Direct adjustment** — Modify affected docs within current sprint
  - **Rollback to phase** — Revert to an earlier phase and re-run downstream
  - **Re-plan sprint** — Adjust implementation plan and sprint status
  - **Accept as tech debt** — Document the gap, defer to future sprint
- **Checkpoint:** Present the recommendation with rationale and ask: "Does this approach work for you?"

### Step 5: Detailed Change Proposals
- **Input:** Approved approach + impact analysis
- **Action:** For each affected document, generate specific change proposals showing old → new for each impacted ID. Present section by section.
- **Checkpoint:** For each document's changes, ask: "Do these changes look right?"

### Step 6: Right-Size Check
- **Action:** Before saving, assess whether the proposal's depth matches the change's complexity:
  - If this is a minor change (1-2 docs, low effort) → trim the proposal to essentials
  - If this is a major change (5+ docs, high effort) → ensure all ripple effects are captured
  - A small scope change deserves a short proposal. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 7: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. Would someone reading this proposal understand exactly what to change in each document?
  2. Are there implicit downstream effects not captured (e.g., changing a US-# might affect feature-spec)?
  3. Are there ID conflicts or gaps (e.g., removing US-5 but impl-12 still references it)?
  4. Is there a low-effort addition that would make this significantly more actionable?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 8: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/implementation/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/implementation/change-proposal-{slug}.md` using the Write tool
  3. The document is only saved when written to the filesystem — presenting content in chat is not the same as saving.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review
- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path + paths to all affected upstream documents
  2. The reviewer checks: completeness, consistency, that all impacted IDs are addressed, no orphaned references
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Output:** Reviewed and approved document

### Step 10: User Review Gate
- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Change proposal saved to `docs/ets/projects/{project-slug}/implementation/change-proposal-{slug}.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed after user approval.
- **Output:** User-approved document

### Step 11: Validation & Handoff Options
- **Input:** Approved document
- **Action:** Run OUTPUT VALIDATION checklist. Present CLOSING SUMMARY with handoff options.
- **Output:** Document marked COMPLETE or DRAFT, user chooses next action

### Step 12: Apply Changes (if user chose option 1)
- **Action:** If the user chose "Apply changes to documents":
  1. For each affected document, read the current version
  2. Apply the changes described in the proposal
  3. Re-save each modified document
  4. Update `docs/ets/.memory/decisions.md` with the change decision
  5. Display: "Updated N documents. Changes applied."
- **Output:** All affected documents updated

### Step 13: Linear Sync (if user chose option 3)
- **Action:** If the user chose "Update execution adapter too" and `state/execution-sync.yaml` indicates adapter-backed execution:
  1. Check which adapter is active
  2. For each impacted ETUS ID that has an external mapping:
     - Update the external execution item (title, description, status as needed)
  3. For new IDs created by the change:
     - Create new external execution items
  4. For removed IDs:
     - Close or archive the corresponding external execution items
  5. Update mappings via the adapter bridge
  6. Refresh local sync state in `state/execution-sync.yaml`
  7. If unit composition changed, refresh the local execution projection
  8. Display: "Updated external execution items and refreshed the ETUS local projection."
- **Output:** Execution adapter projection synced

## Reconciliation Phase

After user approves change-proposal:

1. **Extract affected IDs** — List all IDs mentioned in the change (removed PRD-F-#, changed US-#, reversed NG-#, modified EDGE-#, etc.)

2. **Grep project docs** — Search all project documents for these IDs:
   ```
   For each affected ID:
     Search docs/ets/projects/{project-slug}/ recursively
     Record: file path, line number, surrounding context
   ```

3. **List affected documents** — Present to user:
   ```
   The following documents reference affected IDs:
   - user-stories.md (line 45): references PRD-F-3
   - impl-plan.md (line 120): references US-8
   - release-plan.md (line 30): references PRD-F-3
   ```

4. **Generate proposed diffs** — For each affected document:
   - If ID was removed: propose removing the reference
   - If ID was changed: propose updating the wording
   - If priority changed: propose updating priority markers
   - If NG-# was reversed: propose removing the non-goal constraint

5. **Present before/after** — Show each proposed change to user for approval (one doc at a time)

6. **Apply approved changes** — Edit the documents

7. **Update state files** — Update:
   - coverage-matrix.yaml (edge_resolution, semantic_dimensions if affected)
   - workflow-state.yaml (phase status if affected)
   - feature-status.yaml (if feature-mode)
   - ids.yml (if ID sequences affected)

8. **Flag external issues** — If execution adapter is enabled, list which external issues (Linear, etc.) need manual updates

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| No existing documents found | Critical | Halt — nothing to change | Guide user to /start-project or /plan |
| Change description too vague | Medium | Ask for clarification with examples | Proceed with broad impact analysis |
| Document read fails | Medium | Skip that document, note in proposal | Proceed with available documents |
| Execution adapter unavailable | Low | Skip external sync, note in proposal | Manual external update by user |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |

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

### Invocation

- **Automatic:** Orchestrator invokes Quality Loop for all high-dependency documents
- **Manual:** User can request `--quality-loop` on any skill invocation
- **Skip:** User can pass `--no-quality-loop` to disable (generates once, validates once)
