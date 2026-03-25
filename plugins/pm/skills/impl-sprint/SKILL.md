---
name: impl-sprint
description: >
  Legacy compatibility skill for projecting implementation work into an optional
  execution adapter state. Use only when an execution adapter is enabled and a
  local execution projection needs updating.
model: sonnet
version: 1.0.0
argument-hint: "[sprint-number]"
compatibility: "Optional: execution adapter projection. Upstream: docs/ets/projects/{project-slug}/implementation/implementation-plan.md or docs/ets/projects/{project-slug}/features/{feature-slug}/impl-plan.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/implementation/implementation-plan.md` — Needed for Product mode impl-# tasks to track.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/impl-plan.md` — Needed for Feature mode impl-# tasks to track.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/state/project-status.yaml` — Determines whether an execution adapter is enabled.
- `docs/ets/projects/{project-slug}/state/execution-sync.yaml` — Adapter sync context when external execution projection exists.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `sprint-status.requires: [implementation-plan]`
2. Read `docs/ets/projects/{project-slug}/state/project-status.yaml` to detect mode and `execution_adapter`
3. Resolve upstream:
   - Product mode → `implementation/implementation-plan.md`
   - Feature mode → `features/{feature-slug}/impl-plan.md`
4. If missing → auto-invoke `implementation-plan` skill → wait → continue

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- Multi-sprint project requiring formal progress tracking
- Team needs burndown visibility and blocker management
- Stakeholder reporting on sprint-by-sprint progress

**Use short version when:**
- Single sprint with a small task list
- Quick status update for a standup
- Even in short version, still include: task status table, blockers, and sprint velocity

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in YAML STRUCTURE
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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing execution-status.yaml at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

### Skill-Specific Interaction

- **Sprint scope:** Propose a task selection for the first sprint based on priorities, dependencies, and critical path from the implementation plan. Present the proposed sprint backlog and ask "Does this sprint scope look right? Any tasks to add or remove?" before proceeding.
- **Velocity baseline:** Propose a baseline velocity based on team size and sprint duration (e.g., "With 3 developers on 2-week sprints, a conservative baseline is 30 points"). Ask the user to calibrate — is this too aggressive, about right, or too conservative?
- **Per-task assignment:** For each task in the sprint, propose an owner based on task type (backend, frontend, database). Ask "Should [name] own this task?" one at a time.
- **Handoff options:**
  1. Proceed to Quality Checklist (Recommended) — define pre-release quality criteria
  2. Adjust sprint scope — add, remove, or reorder tasks
  3. Pause — save current progress and return later

# Execution Projection Tracking

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

Generate and iteratively update **state/execution-status.yaml**, a living document that tracks optional execution projections for stories, tasks, and execution units. This document is outside the documentation core and exists only when an execution adapter is enabled.

Execution projection is updated only when the project chooses to maintain adapter-aware local state. It never overrides the documentation core.

## CONTEXT LOADING (4-level fallback)

1. **Project Status**: Read `docs/ets/projects/{project-slug}/state/project-status.yaml` first.
2. **$ARGUMENTS**: If `[sprint-number]` provided, load that sprint's current status
3. **State File**: Check for `docs/ets/projects/{project-slug}/state/execution-status.yaml` (existing state to update)
4. **Upstream Plan**:
   - Product mode: `docs/ets/projects/{project-slug}/implementation/implementation-plan.md`
   - Feature mode: `docs/ets/projects/{project-slug}/features/{feature-slug}/impl-plan.md`
5. **Adapter Context**: If `execution_adapter = linear`, also read `docs/ets/projects/{project-slug}/state/execution-sync.yaml`
6. **Ask**: If no context available, ask user for sprint number, current date, and team capacity

Load the following sections from upstream or existing status:
- Sprint definition (start date, end date, capacity)
- Task list (impl-# items assigned to this sprint)
- Current progress (% complete per task)
- Any existing blockers or notes

## PROCESS

### Initial Sprint Setup

1. **Sprint Definition**:
   - Sprint number (1, 2, 3, ...)
   - Start and end dates
   - Team members and capacity (hours/person × sprint duration)
   - Capacity in effort units (estimated hours or story points)

2. **Task Population**: Extracted from implementation-plan.md
   - Assign impl-# tasks to this sprint
   - Copy initial estimates (T-shirt sizes converted to points)
   - Set initial status: todo (not started)
   - Assign owners (if known)

### Ongoing Status Updates (during sprint)

3. **Daily/Weekly Updates**:
   - Update task status: todo → in-progress → done or blocked
   - Record % completion for in-progress tasks
   - Document blockers and mitigation
   - Update actual vs estimated effort
   - Capture learning notes and deviations from plan

4. **Blocker Tracking**:
   - Identify blocking issues (external dependencies, missing information, bugs)
   - Assess severity (high/medium/low)
   - Document resolution plan and owner
   - Track resolution time

5. **Velocity Calculation**:
   - At end of sprint: sum completed effort (story points)
   - Compare to capacity (velocity = actual completed / capacity)
   - Use velocity for future sprint planning

6. **Health Assessment**:
   - On-track: completed velocity >= 80% capacity
   - At-risk: 50–80% capacity
   - Blocked: < 50% capacity
   - Provide mitigation recommendations

## EXECUTION ADAPTER MODES

### `execution_adapter: local`
- `state/execution-status.yaml` may be used as a local execution projection.
- This is optional and never replaces the documentation core.

### `execution_adapter: linear`
- An external execution system remains the operational tracker for assignment, workflow, and execution units.
- `state/execution-status.yaml` becomes the local ETUS projection.
- `state/execution-sync.yaml` stores mappings, conflicts, and sync metadata.

## YAML STRUCTURE

```yaml
schema: etus/execution-status@v1
project_slug: "invoice-saas"
execution_adapter: local
current_unit: sprint-1
updated_at: "2026-03-20T14:30:00Z"

units:
  sprint-1:
    state: active
    start: "2026-03-17"
    end: "2026-03-28"
    capacity: 40
    velocity: 32
    source: local
    stories: ["US-1", "US-2"]
    tasks: ["impl-1", "impl-2"]

story_status:
  US-1:
    state: in_progress
    sprint: sprint-1
    assignee: "alice@example.com"
    percent_complete: 60

task_status:
  impl-1:
    state: done
    sprint: sprint-1
    owner: "alice@example.com"
    estimate: 8
    actual: 9
    blocker: ""
  impl-2:
    state: blocked
    sprint: sprint-1
    owner: "bob@example.com"
    estimate: 13
    actual: 8
    blocker: "Waiting for SMTP credentials"

feature_rollups:
  csv-bulk-import:
    execution_adapter: local
    delivery_state: impl_ready
    release_state: not_released
    next_recommended_step: "/validate"
    story_ids: ["US-1", "US-2"]
    task_ids: ["impl-1", "impl-2"]
```

## UPDATE PROTOCOL

When updating an existing sprint:

1. **Read** the current `state/execution-status.yaml`
2. **Update** only the fields that changed:
   - Task status, % complete, actual effort
   - Blockers (new, resolved, or updated)
   - Notes and learnings
   - Velocity and health assessment (recalculate)
3. **Preserve** task definitions and estimates (if planning changes, update implementation-plan.md instead)
4. **Add** timestamps (updated field) to all modified entries

## PIPELINE CONTEXT

- **Input**: implementation-plan.md or features/{feature-slug}/impl-plan.md (task definitions, sprint assignments)
- **Output**: state/execution-status.yaml (living execution record)
- **Referenced by**: daily standups, sprint reviews, retrospectives, project dashboards
- **Feeds into**: next sprint planning (velocity used for capacity estimation)

## KNOWLEDGE POINTER

Refer to `docs/ets/projects/{project-slug}/state/execution-status.yaml` and `docs/ets/projects/_templates/execution-status.yaml` for:
- YAML schema examples
- Burndown chart calculation (text format)
- Health assessment criteria
- Blocker severity matrix
- Sprint retrospective template
- Velocity trending (multiple sprint comparison)

---

**Execution instruction**: Load `project-status.yaml` first, detect `execution_adapter`, populate or update `state/execution-status.yaml`, and if `execution_adapter = linear`, also reflect mapping/sync notes from `state/execution-sync.yaml`.

## INPUT VALIDATION

**implementation-plan.md** (BLOCKS):
- Must contain at least 3 impl-# tasks
- Must contain sprint roadmap with assignments

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Sprint number and duration specified
- [ ] All assigned impl-# tasks listed with status
- [ ] Progress tracking present (done/in-progress/blocked/todo)
- [ ] Blockers section present (even if empty)
- [ ] Velocity metric present (points completed vs planned)
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ execution-status.yaml saved to `docs/ets/projects/{project-slug}/state/execution-status.yaml`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document tracks impl-# task progress, not new IDs)

→ Next step: quality-checklist — Define pre-release quality criteria and acceptance gates
  Run: /implement or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Context Loading
- **Input:** Product mode `implementation-plan.md` or Feature mode `features/{feature-slug}/impl-plan.md` (BLOCKS), existing `state/execution-status.yaml` (if updating)
- **Action:** Extract impl-# tasks, sprint assignments, previous status
- **Output:** Sprint context
- **Why this matters:** The implementation plan defines what to track. Loading it ensures the sprint covers the right tasks in the right order.

### Step 2: Sprint Scope Selection (Interactive)
- **Input:** impl-# tasks + priorities + dependencies
- **Action:** Propose a task selection for this sprint based on priorities and critical path. Present the proposed sprint backlog and ask "Does this sprint scope look right? Any tasks to add or remove?"
- **Output:** Approved sprint backlog
- **Why this matters:** A well-scoped sprint avoids overcommitting and ensures the team focuses on the highest-impact work.

### Step 3: Velocity Baseline (Interactive)
- **Input:** Team capacity from implementation plan
- **Action:** Propose a baseline velocity based on team size and sprint duration. Ask "Is this baseline too aggressive, about right, or too conservative?"
- **Output:** Calibrated velocity target

### Step 4: Task Assignment (Per-Task Approval)
- **Input:** Approved sprint backlog + team members
- **Action:** For each task, propose an owner based on task type (backend, frontend, database). Ask "Should [name] own this task?" one at a time.
- **Output:** Sprint tasks with approved assignments

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
  1. Verify directory exists: `docs/ets/projects/{project-slug}/state/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/state/execution-status.yaml` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/state/execution-status.yaml`) + paths to upstream documents (`docs/ets/projects/{project-slug}/implementation/implementation-plan.md` or `docs/ets/projects/{project-slug}/features/{feature-slug}/impl-plan.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 9: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/state/execution-status.yaml`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 10: Validation & Handoff
- **Input:** Updated YAML
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT
- **Handoff:** Present next step options:
  1. Proceed to Quality Checklist (Recommended)
  2. Adjust sprint scope
  3. Pause

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (implementation-plan.md) | Critical | Auto-invoke implementation-plan skill | Block execution |
| No impl-# tasks assigned to current sprint | Medium | Ask user to assign tasks | Create empty sprint with note |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
