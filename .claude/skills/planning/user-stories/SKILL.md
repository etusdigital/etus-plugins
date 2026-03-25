---
name: user-stories
description: >
  Use when writing user stories, defining acceptance criteria, or specifying user
  behaviors. Also triggers on 'user stories', 'as a user I want', 'acceptance
  criteria', 'Given/When/Then', 'BDD scenarios', or 'behavioral specifications'.
model: opus
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Optional: external execution adapter integration (for example, a Linear adapter). Use `state/project-status.yaml` + `state/execution-sync.yaml` as the local operational mirror."
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

### Product Mode (default)

**BLOCKS** (required — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/planning/prd.md` — Provides the PRD-F-# features to decompose into stories. Without features, there is nothing to write stories for.
- `docs/ets/projects/{project-slug}/planning/solution-discovery.md` — Stories should derive from the selected solution direction, not only from the abstract requirement list.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Personas and BO-# context makes stories more specific and grounded in real user needs.
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — Upstream actors, JTBDs,
  journeys, use cases, and edge cases should be reflected in story coverage.
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` — Helps ensure stories do not
  skip critical scenarios already identified during ideation.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `user-stories.requires: [prd]`
2. Check: does `prd.md` exist, non-empty, not DRAFT?
3. If missing → auto-invoke `prd` skill → wait → continue
4. Check ENRICHES: `product-vision.md` → warn if missing, proceed

### Feature Mode

**BLOCKS** (required — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md` — Provides the FB-# items to decompose into stories. Replaces prd.md as upstream in Feature mode.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md` — Feature-mode stories should trace back to the chosen solution direction.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-status.md` — Canonical feature state for slug, tracking mode, next step, and linked docs.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Personas and BO-# context.
- `docs/ets/projects/{project-slug}/planning/prd.md` — If exists, provides broader product context.
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — Source of upstream feature
  problem-space coverage.
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` — Source of upstream feature
  coverage commitments.

**Resolution protocol:**
1. Detect mode: check `docs/ets/projects/{project-slug}/state/project-status.yaml` or infer from `$ARGUMENTS` (if path contains `features/` and `feature-brief.md`)
2. Read `dependency-graph.yaml` → Feature mode: `user-stories.requires: [feature-brief]`
3. Check: does `features/{feature-slug}/feature-brief.md` exist, non-empty, not DRAFT?
4. If missing → auto-invoke `feature-brief` skill → wait → continue
5. Check ENRICHES → warn if missing, proceed

### Mode Detection

Determine mode using this priority:
1. **Explicit:** `$ARGUMENTS` contains a `features/` path or a `feature-status.md` path → Feature mode
2. **Handoff:** `docs/ets/projects/{project-slug}/state/project-status.yaml` exists with `"mode": "feature"` → Feature mode
3. **Context:** `docs/ets/projects/{project-slug}/features/*/feature-brief.md` exists but `docs/ets/projects/{project-slug}/planning/prd.md` does not → Feature mode
4. **Default:** Product mode

## ARTIFACT SAVE RULE

**Why this matters:** user-stories.md is the Single Source of Truth for all Given/When/Then acceptance criteria. If it only exists in chat, QA teams cannot generate BDD tests, and the feature-spec and implementation skills cannot reference US-# IDs.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is not the same as saving — the file needs to exist on the filesystem for downstream skills and BDD test generation
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only then propose the next step

**If the Write fails:** Report the error to the user and do not proceed — downstream documents depend on US-# references in this file.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Use the AskUserQuestion tool when available for structured choices. Batching questions leads to shallow stories with generic acceptance criteria.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., which scenarios to include, story point estimate), present 3-4 concrete options with a brief description of each. Highlight your recommendation.

3. **Generate stories one at a time** — Present each US-# with its story statement and acceptance criteria. Ask "Does this capture the behavior correctly? Anything to adjust?" before generating the next story.

4. **Propose Given/When/Then scenarios before writing** — For each story, propose 2-3 scenarios (happy path, edge case, error case) and ask which to include. Then write the approved scenarios.

5. **Track outstanding questions** — If something cannot be answered now, classify it:
   - **Resolve before next phase** — This blocks the handoff to feature-spec or Design.
   - **Deferred to [phase name]** — Noted and carried forward in the handoff JSON.

6. **Present story groups for approval** — After completing all stories for one PRD-F-#, present the group summary and ask for approval before moving to the next feature.

7. **Multiple handoff options** — At completion, present 3-4 next steps as options (see CLOSING SUMMARY).

8. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing user-stories.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

9. **Assess if full process is needed** — If the user's input is already detailed with clear requirements, specific acceptance criteria, and defined scope, don't force the full interview. Confirm understanding briefly and offer to skip directly to document generation. Only run the full interactive process when there's genuine ambiguity to resolve.

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

## PRESSURE TEST

Before generating content, challenge the framing with these questions (ask the most relevant 1-2, not all):

- **Is this the right problem?** — "Before we proceed, let me push back: is [stated problem] the real problem, or is it a symptom of something deeper?"
- **What happens if we do nothing?** — "What's the cost of NOT building this? If the answer is 'not much,' the priority might need rethinking."
- **Is there a better framing?** — "Could we reframe this in a way that solves a bigger problem with similar effort?"
- **Are we building for the right user?** — "You mentioned [user]. Are they the ones who feel the most pain, or is there a higher-leverage audience?"

The goal is to sharpen the problem framing, not to block progress. If the user's framing is solid, acknowledge it and move on quickly. Only dig deeper when genuine misframing signals appear.

## PURPOSE

Translate features into testable user stories with acceptance criteria in
Gherkin Given/When/Then format. This is the **Single Source of Truth** for all
behavioral specifications. If an actor, journey, use case, or edge case mattered
upstream during ideation, it should either appear here or be explicitly
deferred.

- **Product mode:** Translate each PRD feature (PRD-F-#) into stories.
- **Feature mode:** Translate each feature-brief item (FB-#) into stories. Scoped to the single feature.

## CONTEXT LOADING

### Product Mode

Load context in this order of priority:

1. **Solution Discovery**: Read `docs/ets/projects/{project-slug}/planning/solution-discovery.md` first.
2. **$ARGUMENTS**: If the user passes `[upstream-path]`, read that file directly (typically prd.md).
3. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for any upstream planning artifacts.
4. **Document Scan**: Scan `docs/ets/projects/{project-slug}/planning/` for existing prd.md to extract PRD-F-#.
5. **User Interview**: If nothing found, begin the user story interviews interactively.

### Feature Mode

Load context in this order of priority:

1. **Feature Status**: Read `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-status.md` first.
2. **Solution Discovery**: Read `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md` first.
3. **$ARGUMENTS**: If the user passes a `features/{feature-slug}/feature-brief.md` path, read that file directly.
4. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/project-status.yaml` for Feature mode context and slug.
5. **Document Scan**: Scan `docs/ets/projects/{project-slug}/features/` for existing `feature-brief.md` files to extract FB-#.
5. **Existing Product Docs (ENRICHES)**: If `prd.md` or `product-vision.md` exist, read them for broader context but do NOT require them.
6. **User Interview**: If nothing found, begin the user story interviews interactively.

## STORY FORMAT

Each user story follows a simple template:

```
As a [persona], I want [action], so that [benefit/motivation]
```

Example:
- As a freelancer, I want to create an invoice in <2 minutes, so that I can focus on billable work instead of admin.

Validate with user: "Is this persona correct? Does the action match the benefit?"

### Story Depth Guidelines

Each US-# must go beyond the basic story statement. The difference between a shallow story and a production-ready story:

**Shallow (insufficient):**
> US-1: As a user, I want to log in, so that I can access my account.
> Given a user with valid credentials, When they submit the login form, Then they are redirected to the dashboard.

**Production-ready (target depth):**
> US-1: As a freelancer with an existing account, I want to log in with email/password or Google SSO, so that I can access my invoicing dashboard within 3 seconds.
>
> Given a freelancer with valid email/password credentials
> When they submit the login form
> Then they are redirected to the invoicing dashboard within 3 seconds
> And their last-viewed client is pre-selected
>
> Given a freelancer clicking "Sign in with Google"
> When Google OAuth completes successfully
> Then their account is linked (first time) or they are logged in (returning)
> And session persists for 30 days with "Remember me" checked
>
> Given 3 consecutive failed login attempts
> When the freelancer tries a 4th attempt
> Then the account is temporarily locked for 15 minutes
> And an email notification is sent to the account owner
>
> **Dependencies:** Upstream: PRD-F-2 (Authentication). Downstream: None (simple).
> **Technical Notes:** Requires OAuth 2.0 with Google. Rate limiting on login endpoint. Session management via JWT with 30-day refresh token.
> **Design Notes:** Login page with email/password + Google SSO button. Error states: invalid credentials, locked account, network error. Mobile-responsive (min 320px).

## ACCEPTANCE CRITERIA FORMAT

Each story has 1-3 acceptance criteria in Gherkin Given/When/Then format:

```
Given [pre-conditions / initial state]
When [user action]
Then [expected result]
```

Example:
```
Given a freelancer logged in with previous clients
When clicking "New Invoice"
Then they see a pre-filled form with the most recent client selected
And suggested line items from previous invoices appear

Given a draft invoice unsaved for >5 minutes
When the user navigates away
Then they see a prompt "Discard unsaved changes?"

Given an invoice overdue by >30 days
When freelancer views the dashboard
Then the invoice is highlighted in red with "Overdue" label
```

**Quality Guidelines for Given/When/Then:**
- **Given**: Be specific (not "a user", but "a freelancer with >3 past invoices"). State the setup clearly.
- **When**: Use a single action (not "user creates and saves"; use two scenarios instead). Be concrete ("clicks button" not "interacts").
- **Then**: Describe the observable outcome (not "system works", but "form displays with fields X, Y, Z pre-filled").
- **Avoid boilerplate**: Each scenario must be testable and meaningful.

## SST RULE

**Given/When/Then acceptance criteria live only in this document.**

Why this matters: if acceptance criteria are scattered across user-stories.md, feature-spec files, and implementation plans, QA teams get conflicting definitions of "done" and BDD tests diverge from the actual spec. By keeping all Given/When/Then here, there is exactly one place to look for behavioral expectations.

This is the Single Source of Truth for:
- Definition of Done (QA acceptance)
- BDD test generation (Cucumber/Gherkin automation)
- Behavioral specification (shared understanding between dev and design)

Downstream documents (feature-spec-*.md, implementation-plan.md) may elaborate on business rules and logic but should not modify or override the Given/When/Then scenarios defined here.

## ID GENERATION

**US-# Pattern**: User Stories. Format: `US-1`, `US-2`, etc. Each US-# must:
- Reference which upstream item it implements:
  - **Product mode:** PRD-F-# (traceability back to PRD scope)
  - **Feature mode:** FB-# (traceability back to feature-brief scope)
- Have one clear persona and action
- Include 1-3 Given/When/Then acceptance criteria
- Link to downstream feature-spec-*.md if story triggers >3 business rules threshold (Product mode only)
- Be unique and testable

Maintain traceability:
- **Product mode:** `BO-# → PRD-F-# → US-# → acceptance criteria`
- **Feature mode:** `ACT/JTBD/JOUR/UC/EDGE -> FB-# → US-# → impl-#`

## OUTPUT FORMAT

### Product Mode

The generated `docs/ets/projects/{project-slug}/planning/user-stories.md` contains:

- **Source Documents**: Table of upstream documents consumed
- **Index**: Table of PRD-F-# with US-# count under each
- **Grouped by PRD-F-#**: Stories organized by feature they implement

### Feature Mode

The generated `docs/ets/projects/{project-slug}/features/{feature-slug}/user-stories.md` contains:

  - **Source Documents**: Table listing `feature-brief.md` and `solution-discovery.md` as primary upstream
- **Index**: Table of FB-# with US-# count under each
- **Grouped by FB-#**: Stories organized by feature-brief item they implement
- Same per-US-# structure as Product mode, but with `FB-#` replacing `PRD-F-#` in the Feature field

### Common Structure (both modes)

Both modes share the same per-US-# structure:
- **Per US-#** (each story contains ALL of these fields):

```markdown
### US-[NN]: [Descriptive Title]

**Feature:** PRD-F-[NN] — [Feature name]
**Persona:** [Persona name]
**Priority:** [Must/Should/Could — inherited from PRD-F-#]
**Story Points:** [S/M/L/XL — relative effort estimate]

> As a [persona], I want [action], so that [benefit/motivation].

#### Acceptance Criteria

```gherkin
Given [specific pre-condition with context]
When [single concrete user action]
Then [observable, testable outcome]

Given [another scenario]
When [action]
Then [result]
```

#### Dependencies
- **Upstream:** [PRD-F-# and any other US-# this depends on]
- **Downstream:** [FS-{name}-# if complexity threshold met, or "None"]

#### Technical Notes
- [Key technical consideration — e.g., "Requires OAuth 2.0 integration"]
- [Performance constraint — e.g., "Must respond in <200ms"]
- [Data dependency — e.g., "Reads from user_profiles table"]

#### Design Notes
- [UI requirement — e.g., "Modal dialog with form validation"]
- [UX constraint — e.g., "Must work on mobile viewport (320px)"]
- [Accessibility — e.g., "ARIA labels for all form inputs"]
```

- **Coverage Matrix**:
  - **Product mode:** Table showing PRD-F-# × US-# mapping
  - **Feature mode:** Table showing FB-# × US-# mapping
- **Statistics**: Total US-#, breakdown by priority (Must/Should/Could), by story points
- **Traceability**:
  - **Product mode:** Visual chain: BO-# → PRD-F-# → US-# → [FS-# if applicable]
  - **Feature mode:** Visual chain: FB-# → US-# → impl-#

## COMPLEXITY THRESHOLD

After writing a user story, check: Does this feature have >3 business rules, state transitions, or intricate validation?

If YES → Flag for feature-spec-[name].md creation. The feature-spec will detail the complex logic while user-stories.md remains the SST for acceptance criteria.

If NO → Leave as-is. Simple user story is sufficient.

## KNOWLEDGE POINTERS

- Read `references/template.md` for the user-stories.md document template and structure.
- Read `references/guide.md` for story writing best practices: writing from user perspective, avoiding vagueness, making Given/When/Then specific and executable.

---

**Upon completion, evaluate each US-# for the complexity threshold. Flag features exceeding 3 business rules for feature-spec creation. Then present handoff options to the user (see CLOSING SUMMARY). Planning Gate validation: All PRD-F-# covered by US-# and feature-specs? Scope achievable in estimated time?**

## INPUT VALIDATION

### Product Mode

**prd.md** (BLOCKS):
- Needs at least 3 `PRD-F-#` identifiers — fewer than 3 features suggests the PRD is incomplete
- Needs a `## Features` section — this is where PRD-F-# definitions live
- Each PRD-F-# should have a MoSCoW priority — stories inherit priority from their parent feature

**product-vision.md** (ENRICHES):
- Should contain personas with goals — these drive the "As a [persona]" part of each story

### Feature Mode

**features/{feature-slug}/feature-brief.md** (BLOCKS):
- Needs at least 1 `FB-#` identifier — the items to decompose into stories
- Needs a clear problem statement and scope definition
- Each FB-# should have priority/importance indication

**prd.md** (ENRICHES):
- If exists, provides broader product context and existing PRD-F-# for cross-reference

**product-vision.md** (ENRICHES):
- If exists, provides personas and BO-# context

## OUTPUT VALIDATION

Before marking this document as COMPLETE:

### Common checks (both modes)
- [ ] Each US-# has 1-3 Given/When/Then acceptance criteria (not boilerplate)
- [ ] All Given/When/Then are specific and testable (concrete personas, measurable outcomes)
- [ ] Each US-# includes Dependencies section (upstream/downstream)
- [ ] Each US-# includes Technical Notes (at least 1 technical consideration)
- [ ] Each US-# includes Design Notes (at least 1 UI/UX requirement)
- [ ] Source Documents section present at top

### Product Mode checks
- [ ] At least 1 US-# per Must Have PRD-F-# (coverage)
- [ ] Each US-# references which PRD-F-# it implements (traceability)
- [ ] No orphan US-# without PRD-F-# reference
- [ ] Coverage matrix present (PRD-F-# × US-# table)

### Feature Mode checks
- [ ] At least 1 US-# per FB-# item (coverage)
- [ ] Each US-# references which FB-# it implements (traceability)
- [ ] No orphan US-# without FB-# reference
- [ ] Coverage matrix present (FB-# × US-# table)

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display the summary and offer multiple next steps:

```text
user-stories.md saved to `docs/ets/projects/{project-slug}/planning/user-stories.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list US-# IDs, e.g., US-1, US-2, US-3, ... US-N]
Features flagged for detailed spec: [list any, or "None"]

What would you like to do next?

1. Proceed to Feature Specs (Recommended if features were flagged) — Detail complex features with >3 business rules
2. Skip Feature Specs, proceed to Planning Gate — If no features need detailed specs
3. Refine these stories — Review and improve specific stories
4. Pause for now — Save and return later
```

Wait for the user's choice before proceeding. Do not auto-advance to the next skill.

## WORKFLOW

### Step 1: Context Loading & Confirmation

**Product mode:**
- **Input:** `prd.md` (BLOCKS), `product-vision.md` (ENRICHES)
- **Action:** Extract PRD-F-# features, personas, priorities
- **Output:** Feature list with priorities
- **Checkpoint:** Present the feature list and ask: "I found [N] features. Should we write stories for Must Have + Should Have, or include Could Have too?"

**Feature mode:**
- **Input:** `features/{feature-slug}/feature-brief.md` (BLOCKS), `product-vision.md` (ENRICHES if exists)
- **Action:** Extract FB-# items, scope, personas from feature-brief
- **Output:** Feature-brief item list with priorities
- **Checkpoint:** Present the FB-# list and ask: "I found [N] items in the feature brief. Should we write stories for all of them?"

### Step 2: Story Generation — One Story at a Time, One Feature at a Time

For each PRD-F-# (Must Have first, then Should Have):

**2a. Feature introduction:**
- Present the feature name, description, and priority from prd.md
- Ask: "What are the main ways users interact with this feature?" (one question, wait for answer)

**2b. Story drafting (one US-# per turn):**
- Draft the story statement (As a / I want / So that) and present it
- Ask: "Does this capture the right persona, action, and benefit?"
- Only after approval, proceed to acceptance criteria

**2c. Acceptance criteria — propose scenarios before writing:**
- Propose 2-3 Given/When/Then scenarios for this story:
  - Happy path scenario
  - Edge case or alternative path (suggest 2-3 options, ask which matter)
  - Error case (if applicable)
- Ask: "Which of these scenarios should we include? Any others?"
- Write the approved scenarios in Gherkin format

**2d. Edge case suggestions for Must Have stories:**
- For each Must Have story, suggest 2-3 edge cases the user may not have considered
- Ask: "Are any of these relevant for this story?"
- Include approved edge cases as additional Given/When/Then scenarios

**2e. Story completion:**
- Present the complete US-# with all fields (story, criteria, dependencies, technical notes, design notes)
- Ask: "Does this look right? Anything to adjust?"
- Only after approval, ask: "Any more stories for this feature, or move to the next one?"

**2f. Feature group approval:**
- After all stories for one PRD-F-# are done, present the group summary
- Ask: "Here are all [N] stories for PRD-F-#. Does this cover the feature well?"
- Only after approval, move to the next PRD-F-#

### Step 3: Definition of Ready, Done & Quality Items
- **Input:** Completed stories
- **Action:** After all stories are generated, ask the user about team-level quality definitions:
  1. **DoR:** "What are the minimum criteria for a story to enter a sprint? (e.g., clear description, acceptance criteria defined, dependencies mapped, design available, tracking defined, estimated, prioritized)"
  2. **DoD:** "What are the criteria to consider a story 'done'? (e.g., acceptance met, tests passed, tracking validated, logs configured, docs updated, PM/QA approved)"
  3. **Quality items:** "Which quality items are mandatory for every story? (e.g., observability: logs/metrics/alerts, tracking: events per PRD, tests: regression/automated, documentation)"
- **Checkpoint:** Present the DoR, DoD, and quality items sections for approval before proceeding.
- **Note:** If the user has no custom definitions, use the defaults from the template.

### Step 4: Complexity Assessment
- **Input:** Completed stories
- **Action:** For each feature, assess the complexity threshold (>3 business rules, state machines, intricate validation)
- **Checkpoint:** Present which features are candidates for feature-spec and ask: "Do you agree these need detailed specs?"

### Step 5: Coverage & Statistics
- **Input:** All stories
- **Action:** Generate coverage matrix (PRD-F-# x US-#), statistics, and traceability chain
- **Checkpoint:** Present the summary and ask: "Does the coverage look complete?"

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
  - **Product mode:**
    1. Verify directory exists: `docs/ets/projects/{project-slug}/planning/` — create if missing
    2. Write the complete document to `docs/ets/projects/{project-slug}/planning/user-stories.md` using the Write tool
  - **Feature mode:**
    1. Verify directory exists: `docs/ets/projects/{project-slug}/features/{feature-slug}/` — create if missing
    2. Write the complete document to `docs/ets/projects/{project-slug}/features/{feature-slug}/user-stories.md` using the Write tool
  3. The document needs to exist on the filesystem for downstream skills — presenting content in chat is not sufficient.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/planning/user-stories.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/planning/prd.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/planning/user-stories.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 11: Validation
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (prd.md) | Critical | Auto-invoke prd skill | Block execution |
| prd.md has no PRD-F-# | Critical | Re-invoke prd with feedback | Block — stories need features |
| Feature too vague for stories | Medium | Ask user to clarify feature scope | Generate generic story with TODO |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |

## QUALITY LOOP

This skill supports iterative quality improvement when invoked by the orchestrator or user.

### Cycle

1. **Generate** — Produce initial document following WORKFLOW steps
2. **Self-Evaluate** — Score the output against OUTPUT VALIDATION checklist
   - Calculate: completeness % = (passing checks / total checks) × 100
   - If completeness ≥ 90% → mark COMPLETE, exit loop
   - If completeness < 90% → proceed to step 3
3. **Identify Issues** — List each failing check with specific gap description
4. **Improve** — Address each issue, regenerate affected sections only
5. **Re-Evaluate** — Score again against OUTPUT VALIDATION
   - If improved by < 5% from previous iteration → diminishing returns, mark DRAFT with notes
   - If completeness ≥ 90% → mark COMPLETE, exit loop
   - If max iterations (3) reached → mark DRAFT with iteration log
6. **Report** — Log to stdout: iteration count, score progression (e.g., 65% → 82% → 91%), remaining gaps if any

### Termination Conditions

| Condition | Action | Document Status |
|-----------|--------|-----------------|
| Completeness ≥ 90% | Exit loop | COMPLETE |
| Improvement < 5% between iterations | Exit loop (diminishing returns) | DRAFT + notes |
| Max 3 iterations reached | Exit loop | DRAFT + iteration log |

### Invocation

- **Automatic:** Orchestrator invokes Quality Loop for all high-dependency documents
- **Manual:** User can request `--quality-loop` on any skill invocation
- **Skip:** User can pass `--no-quality-loop` to disable (generates once, validates once)

### 3-Solution Critique

When the self-evaluation identifies a weakness (score < 7/10 on any criterion):

1. **Generate 3 distinct solutions** — each must use a fundamentally different approach (not variations of the same idea)
2. **Compare efficiency** — for each solution, rate:
   - Effort to implement (Low/Medium/High)
   - Impact on document quality (Low/Medium/High)
   - Risk of introducing new issues (Low/Medium/High)
3. **Select and apply** — choose the solution with the best effort-to-impact ratio and lowest risk
4. **Document the decision** — add a brief note in the output explaining which solution was chosen and why

Example: If "acceptance criteria lack edge cases" is identified:
- **Solution A:** Add edge cases to existing criteria → Effort: Low, Impact: Medium, Risk: Low
- **Solution B:** Create dedicated edge case section per US-# → Effort: Medium, Impact: High, Risk: Low
- **Solution C:** Restructure all criteria into happy/sad/edge path format → Effort: High, Impact: High, Risk: Medium
- **Selected:** Solution B — best impact with manageable effort, provides explicit edge case coverage for QA

## EXECUTION ADAPTER PROJECTION (OPTIONAL)

After saving the artifact and displaying the CLOSING SUMMARY, offer optional execution adapter projection:

> "User stories saved. Would you like me to project these stories into an execution adapter?"

**If the user says yes:**

1. Check which `execution_adapter` is active in `state/project-status.yaml`.
2. If `execution_adapter = none`, explain that projection is optional and disabled for this project.

3. If an adapter is active:
   - Project story IDs into `docs/ets/projects/{project-slug}/state/execution-status.yaml`
   - Update `docs/ets/projects/{project-slug}/state/execution-sync.yaml`
   - If the adapter is Linear, mappings may still be recorded with `python3 .claude/hooks/memory-write.py linear ...`
   - Display: "Execution projection updated in the ETUS local state."

4. If the user says no, skip silently and proceed to handoff options.

**Linear mapping layers**:

```markdown
# Linear Issue Mapping

| ETUS ID | Linear ID | Title | Status |
|---------|-----------|-------|--------|
| US-1 | LIN-123 | [title] | created |
```

- `docs/ets/.memory/linear-mapping.md` — human-readable memory view
- `docs/ets/projects/{project-slug}/state/execution-sync.yaml` — operational sync state and local projection

Together they bridge ETUS docs and the chosen execution adapter without losing the ETUS documentation core.

## REFLECTION PROTOCOL
