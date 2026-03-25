---
name: implementation-plan
description: >
  Use when creating an implementation plan, breaking down tasks, estimating effort,
  or planning sprints. Also triggers on 'how do we build this', 'task breakdown',
  'development roadmap', 'sprint planning', or 'implementation plan'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Optional: external execution adapter integration (for example, a Linear adapter). Use `state/project-status.yaml` + `state/execution-sync.yaml` as the local operational mirror."
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

### Product Mode (default)

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/planning/user-stories.md` — Needed for US-# to decompose into impl-# tasks.
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — Needed for NFR-# targets and technical constraints.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/implementation/api-spec.md` — API design informs implementation sequence.
- `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` — System structure informs task grouping.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `implementation-plan.requires: [user-stories, tech-spec]`
2. Check both required docs exist, non-empty, not DRAFT
3. If missing → auto-invoke upstream skill → wait → continue
4. Check ENRICHES → warn if missing, proceed

### Feature Mode

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/features/{feature-slug}/user-stories.md` — Scoped user stories (FB-# → US-#) to decompose into impl-# tasks.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/design-delta.md` — Technical changes and constraints for this feature. Replaces tech-spec as upstream.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md` — Original feature scope and problem statement.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md` — Chosen solution direction and four-risk assessment for this feature.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-status.md` — Canonical feature state.
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — Broader system constraints (if exists).
- `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` — System structure context (if exists).

**Resolution protocol:**
1. Detect mode: check `docs/ets/projects/{project-slug}/state/project-status.yaml` or infer from `$ARGUMENTS` (if path contains `features/`)
2. Read `dependency-graph.yaml` → Feature mode: `implementation-plan.requires: [features/{feature-slug}/user-stories.md, features/{feature-slug}/design-delta.md]`
3. Check both scoped docs exist, non-empty, not DRAFT
4. If missing → auto-invoke upstream skill → wait → continue
5. Check ENRICHES → warn if missing, proceed

### Mode Detection

Determine mode using this priority:
1. **Explicit:** `$ARGUMENTS` contains a `features/` path → Feature mode
2. **Handoff:** `docs/ets/projects/{project-slug}/state/project-status.yaml` exists with `"mode": "feature"` → Feature mode
3. **Context:** `docs/ets/projects/{project-slug}/features/*/user-stories.md` exists but `docs/ets/projects/{project-slug}/planning/user-stories.md` does not → Feature mode
4. **Default:** Product mode

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- New product build with multiple sprints
- Complex project with cross-team dependencies
- impl-# tasks need formal tracking and estimation

**Use short version when:**
- Single feature with <10 tasks and 1-2 sprint duration
- Adding tasks to an existing implementation plan
- Even in short version, still include: task breakdown with impl-# IDs, sprint assignment, and dependency graph

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing implementation-plan.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

8. **Assess if full process is needed** — If the user's input is already detailed with clear requirements, specific acceptance criteria, and defined scope, don't force the full interview. Confirm understanding briefly and offer to skip directly to document generation. Only run the full interactive process when there's genuine ambiguity to resolve.

### Skill-Specific Interaction

- **Sprint duration:** Propose sprint length with tradeoffs:
  - *1-week sprints* — faster feedback loops, more ceremonies overhead, good for uncertain scope
  - *2-week sprints* — balanced rhythm, industry standard, good for stable teams
  Ask which cadence fits the team.
- **Task decomposition:** Present tasks grouped by user story. For each US-#, show the proposed impl-# breakdown and ask "Does this decomposition make sense? Any tasks missing or too coarse?" before moving to the next story.
- **T-shirt sizing:** For each task, propose a size with 3 options and rationale:
  - *Smaller* (e.g., S) — if the task is straightforward and well-understood
  - *Suggested* (e.g., M) — recommended estimate with rationale
  - *Larger* (e.g., L) — if there are unknowns or integration complexity
  Ask the user to confirm or adjust one task at a time.
- **Risk identification:** Propose 3-4 risks based on the tech stack and scope. For each risk, ask the user to rate severity (High/Medium/Low) before moving to the next risk.
- **Team allocation:** Ask about team capacity one question at a time — first team size, then hours per person per sprint, then any known constraints or vacations.
- **Handoff options:**
  1. Proceed to Sprint Status (Recommended) — initialize sprint tracking from this plan
  2. Refine plan — adjust task decomposition or dependencies
  3. Adjust estimates — recalibrate T-shirt sizes based on feedback
  4. Pause — save current progress and return later

# Implementation Planning

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

Generate a comprehensive **implementation-plan.md** that translates design and architecture documents into an executable development plan. This document decomposes user stories and features into concrete implementation tasks (impl-#), maps dependencies, estimates effort, sequences work across sprints, and identifies risks.

The implementation plan is the bridge between design completion and development execution. It ensures nothing falls through the cracks and provides visibility into what gets built, when, and by whom.

## CONTEXT LOADING (4-level fallback)

### Product Mode

1. **$ARGUMENTS**: If `[upstream-path]` provided, load that document
2. **Handoff**: Check for `docs/ets/projects/{project-slug}/planning/user-stories.md` (stories to implement) and design documents
3. **Scan**: If not found, check `docs/ets/projects/{project-slug}/architecture/tech-spec.md` (architecture tasks), `docs/ets/projects/{project-slug}/implementation/api-spec.md` (API work)
4. **Ask**: If no context available, ask user for project scope, team size, and sprint duration

Load the following sections from upstream:
- User stories (US-#) and acceptance criteria
- Feature specifications (FS-#) if complex features exist
- API endpoints from api-spec.md (API implementation tasks)
- Database schema from database-spec.md (DDL tasks)
- Architecture decisions from tech-spec.md (infrastructure, setup tasks)
- Any identified dependencies or critical paths

### Feature Mode

1. **$ARGUMENTS**: If a `features/` path provided, load that document
2. **Handoff**: Check for `docs/ets/projects/{project-slug}/features/{feature-slug}/user-stories.md` + `docs/ets/projects/{project-slug}/features/{feature-slug}/design-delta.md`
3. **Scan**: If not found, scan `docs/ets/projects/{project-slug}/features/` for matching slug files
4. **Ask**: If no context available, ask user for feature scope, team size, and sprint duration

Load the following sections from upstream:
- Scoped user stories (US-#) from `user-stories.md`
- Technical changes from `design-delta.md` (architecture/data/API deltas)
- Feature brief (FB-#) from `feature-brief.md` for context
- Solution rationale from `solution-discovery.md`
- Existing system constraints from tech-spec.md and architecture-diagram.md (ENRICHES only)

## PROCESS

1. **Strategy Definition**: Determine release approach
   - Big-bang: all features in one release
   - Phased/incremental: MVP first, then additional phases
   - Continuous: rolling releases
2. **Task Decomposition**: Break down stories into concrete tasks
   - Each US-# may yield 1–5 impl-# tasks
   - Group related work (backend, frontend, database, testing)
   - Identify infrastructure/setup tasks (not covered in stories)
   - Create impl-# for:
     - Database schema (DDL, migrations)
     - API endpoints (backend routes)
     - Frontend components (UI implementation)
     - Integration testing
     - Deployment/rollout
3. **Effort Estimation**: Use T-shirt sizing (XS, S, M, L, XL)
   - XS: < 2 hours
   - S: 2–4 hours
   - M: 4–8 hours
   - L: 1–2 days
   - XL: 2+ days (candidate for breakdown)
4. **Dependency Mapping**: Identify blocking relationships
   - What tasks must complete before others start?
   - Which tasks can run in parallel?
   - Critical path (longest dependency chain)
5. **Sprint Planning**: Sequence tasks into sprints
   - Typical sprint: 1–2 weeks
   - Capacity per sprint: team size × hours per person × sprint duration
   - Balance velocity (aim for consistent sprint capacity)
   - Reserve 20% for bugs, tech debt, interruptions
6. **Risk Identification**: Document known risks
   - Technical risks (unfamiliar technology, performance concerns)
   - Resource risks (unavailable team members, skills gaps)
   - Scope risks (creeping features, unclear requirements)
   - Timeline risks (ambitious estimates, external dependencies)
7. **Definition of Done**: Establish task completion criteria
   - Code complete and reviewed
   - Unit tests passing
   - Integrated with related components
   - Documentation updated
   - Deployed to staging

## OUTPUT FORMAT

Document structure:
- **Executive Summary**: Total task count, sprint count, critical path, risk summary
- **Implementation Strategy**: Approach (big-bang, phased, continuous), rationale
- **Task Inventory**: Table with impl-#, description, user story link (US-#), feature link (FS-#), estimate, status
- **Dependency Graph**: Mermaid diagram showing task ordering and critical path
- **Sprint Roadmap**: Sprint-by-sprint breakdown
  - Sprint 1: Tasks (impl-#), estimated capacity, key deliverables
  - Sprint 2: ...
  - Burndown chart (text format)
- **Team & Assignments**: Suggested team roles and task assignments (if applicable)
- **Risk Register**: Table with risk, impact, probability, mitigation, owner
- **Definition of Done**: Checklist for task completion
- **Success Metrics**: How implementation success is measured

## PIPELINE CONTEXT

- **Input**: user-stories.md, api-spec.md, database-spec.md, tech-spec.md, wireframes.md, style-guide.md
- **Output**: implementation-plan.md
- **Feeds**: quality-checklist.md (QA gates). Optional execution projections may mirror impl-# into `state/execution-status.yaml`.
- **Referenced by**: development team, project management

## ID GENERATION

Generate impl-# identifiers for all implementation tasks:
- Numbering: impl-1, impl-2, impl-3, ...
- Format in plan: `impl-1 (Backend: User registration endpoint) → US-3`
- Each impl-# traces back to at least one US-# or FS-#
- Maintain impl-# registry in index/cross-reference section

## KNOWLEDGE POINTER

Refer to `docs/ets/projects/{project-slug}/implementation/template-implementation-plan.md` for:
- Task decomposition examples by story type
- T-shirt sizing guidance with story point equivalents
- Dependency graph Mermaid syntax
- Sprint capacity calculation formulas
- Risk register template with examples
- Definition of Done checklist template

---

**Execution instruction**: Load context, decompose stories into tasks, estimate effort, map dependencies, sequence into sprints, identify risks, establish DoD criteria, and output implementation-plan.md to docs/ets/projects/{project-slug}/implementation/.

## INPUT VALIDATION

### Product Mode

**user-stories.md** (BLOCKS):
- Must contain at least 5 US-# with acceptance criteria
- Must reference PRD-F-# features

**tech-spec.md** (BLOCKS):
- Must contain at least 3 NFR-# with targets
- Must contain at least 1 ADR-#

**api-spec.md** (ENRICHES):
- Should contain endpoint definitions

### Feature Mode

**features/{feature-slug}/user-stories.md** (BLOCKS):
- Must contain at least 1 US-# with acceptance criteria
- Must reference FB-# items

**features/{feature-slug}/design-delta.md** (BLOCKS):
- Must contain at least 1 change section (architecture, data, API, or UI delta)

**features/{feature-slug}/feature-brief.md** (ENRICHES):
- Should contain problem statement and scope definition

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] impl-# tasks cover all Must Have US-# (traceability)
- [ ] Each impl-# has T-shirt size estimate (XS/S/M/L/XL)
- [ ] Dependency graph between impl-# tasks present
- [ ] Sprint roadmap present with task assignments
- [ ] Risk register with at least 3 risks identified
- [ ] impl-# IDs are unique and sequential
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ implementation-plan.md saved to `docs/ets/projects/{project-slug}/implementation/implementation-plan.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list impl-# IDs, e.g., impl-1 through impl-N]

→ Next step: validate or hand off to execution
  Run: /validate or proceed in your chosen execution system
```

Do NOT proceed to the next skill without displaying this summary first.

## EXECUTION ADAPTER PROJECTION (OPTIONAL)

After saving the artifact and displaying the CLOSING SUMMARY, offer optional execution adapter projection:

> "Implementation plan saved with N tasks. Would you like me to project these tasks into an execution adapter?"

**If the user says yes:**

1. Check which `execution_adapter` is active in `state/project-status.yaml`.
2. If `execution_adapter = none`, stop after explaining that execution projection is optional and disabled for this project.

3. If an adapter is active:
   - Read `docs/ets/projects/{project-slug}/state/project-status.yaml`
   - Mirror the execution projection into:
     - `docs/ets/projects/{project-slug}/state/execution-sync.yaml`
     - `docs/ets/projects/{project-slug}/state/execution-status.yaml`
   - If the adapter exposes units/cycles, project them locally
   - If the adapter is Linear, mappings may still be recorded with `memory-write.py linear ...`
   - Display: "Execution projection updated in the ETUS local state."

4. If the user says no, skip silently.

## WORKFLOW

### Step 1: Context Loading

**Product mode:**
- **Input:** `user-stories.md`, `tech-spec.md` (BLOCKS), `api-spec.md`, `architecture-diagram.md` (ENRICHES)
- **Action:** Extract US-#, NFR-#, API endpoints, system structure
- **Output:** Implementation requirements bundle

**Feature mode:**
- **Input:** `features/{feature-slug}/user-stories.md`, `features/{feature-slug}/design-delta.md` (BLOCKS), `features/{feature-slug}/feature-brief.md`, `features/{feature-slug}/solution-discovery.md`, `tech-spec.md` (ENRICHES)
- **Action:** Extract scoped US-#, technical deltas, feature constraints
- **Output:** Feature-scoped implementation requirements bundle

- **Why this matters:** The implementation plan translates all upstream decisions into executable tasks. Loading the full context ensures nothing is missed.

### Step 2: Team & Sprint Configuration (Interactive)
- **Input:** Project context
- **Action:**
  1. Ask about team size (one question)
  2. Ask about hours per person per sprint (one question)
  3. Ask about known constraints or vacations (one question)
  4. Propose sprint duration (1-week vs. 2-week) with tradeoffs. Ask which cadence to use.
- **Output:** Team capacity model and sprint configuration
- **Why this matters:** Capacity determines how many tasks fit in each sprint. Getting this right avoids overcommitting or underutilizing the team.

### Step 3: Task Decomposition (Story-by-Story Approval)
- **Input:** US-# list + team capacity
- **Action:** For each user story:
  1. Present the proposed impl-# breakdown (backend, frontend, database, testing tasks)
  2. For each task, propose T-shirt size with 3 options (smaller/suggested/larger) and rationale
  3. Ask "Does this decomposition make sense? Any tasks missing or too coarse?" before the next story
- **Output:** impl-# task list with approved estimates
- **Integration:** impl-# IDs consumed by `quality-checklist` and may be projected into `state/execution-status.yaml` when an execution adapter is enabled

### Step 4: Dependency Graph
- **Input:** Approved impl-# tasks
- **Action:** Map dependencies between tasks, identify critical path. Present the dependency graph (Mermaid) and ask "Does this ordering make sense? Any dependencies missing?"
- **Output:** Dependency graph + critical path analysis

### Step 5: Risk Identification (Interactive)
- **Input:** Task list + tech stack + scope
- **Action:** Propose 3-4 risks based on the project. For each risk, ask the user to rate severity (High/Medium/Low) before moving to the next.
- **Output:** Risk register with user-validated severity ratings
- **Why this matters:** Risks identified early can be mitigated before they block development. User input on severity ensures the team focuses on what matters most.

### Step 6: Sprint Roadmap
- **Input:** Tasks + dependencies + capacity + risks
- **Action:** Assign tasks to sprints, balance load (reserving 20% for bugs/tech debt). Present the sprint roadmap and ask "Does this sprint sequence work? Any adjustments?"
- **Output:** Approved sprint roadmap table

### Step 7: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is lightweight work and the document has unnecessary sections → trim empty or boilerplate sections
  - If this is complex work and sections are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 8: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline still have to invent if this document is all they get?
  2. Do any sections depend on content claimed to be out of scope?
  3. Are there implicit decisions that should be explicit?
  4. Is there a low-effort addition that would make this significantly more useful for the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 9: Save Artifact
- **Action:**
  - **Product mode:**
    1. Verify directory exists: `docs/ets/projects/{project-slug}/implementation/` — create if missing
    2. Write the complete document to `docs/ets/projects/{project-slug}/implementation/implementation-plan.md` using the Write tool
  - **Feature mode:**
    1. Verify directory exists: `docs/ets/projects/{project-slug}/features/{feature-slug}/` — create if missing
    2. Write the complete document to `docs/ets/projects/{project-slug}/features/{feature-slug}/impl-plan.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 10: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/implementation/implementation-plan.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/planning/user-stories.md`, `docs/ets/projects/{project-slug}/architecture/tech-spec.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 11: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/implementation/implementation-plan.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 12: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT
- **Handoff:** Present next step options:
  1. Proceed to Sprint Status (Recommended)
  2. Refine plan
  3. Adjust estimates
  4. Pause

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing | Critical | Auto-invoke upstream skill | Block execution |
| US-# has no clear implementation path | Medium | Ask user to clarify story | Create placeholder impl-# with TODO |
| Team capacity unknown | Low | Ask user or use default (1 dev, 10pts/sprint) | Note assumption |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
