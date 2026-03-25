---
name: tech-spec-standalone
description: >
  Use when documenting a bug fix, planning a hotfix, or performing root cause
  analysis before implementation. Also triggers on 'bug spec', 'fix plan', 'root
  cause analysis', 'hotfix spec', 'fix this bug', 'debug plan', or 'incident
  report'.
model: sonnet
version: 1.0.0
argument-hint: "[bug description or Linear issue URL]"
compatibility: "Optional: external issue tracker adapter (for example, Linear) for bug details and reproduction steps"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (required — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — Bug mode now starts from a
  failure-understanding ideation package so the fix plan is grounded in
  reproduction, impact, anti-journeys, and fallback understanding.

**ENRICHES** (improves output — use if available):
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` — Helps verify failure states,
  affected actors, and fallback expectations.
- `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` — Helps identify which components are affected.
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — Existing NFRs help assess whether the fix needs to maintain specific targets.
- `docs/ets/projects/{project-slug}/data/database-spec.md` — Helps understand data model when the bug involves data corruption or incorrect queries.
- Any existing source code or error logs the user provides.

**Resolution protocol:**
1. Check ENRICHES: do any architecture docs exist?
2. If yes → load silently for context. This helps identify affected components more accurately.
3. If no → proceed without them. Ask the user to describe the relevant system architecture verbally when needed.

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- Complex bug with multiple affected components
- Root cause spans across services or data layers
- Fix requires schema changes or API modifications

**Use short version when:**
- Simple bug with clear root cause and isolated fix
- Typo-level fixes or configuration changes
- Even in short version, still include: root cause analysis, fix description, and verification steps

## ARTIFACT SAVE RULE

**Why this matters:** A documented fix plan prevents hasty patches that introduce regressions. The tech spec serves as the record of what was wrong, why, and how it was fixed — useful for future debugging and post-mortems.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to `docs/ets/projects/{project-slug}/bugs/tech-spec-{slug}.md`
3. Displaying content in chat is not the same as saving — the file needs to exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only then propose the next step

**If the Write fails:** Report the error to the user and do not proceed.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Bug investigation benefits from methodical questioning — each answer narrows the search space. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When presenting fix approaches, always offer 2-3 alternatives with tradeoffs. Highlight your recommendation based on the risk/effort balance.

3. **Propose approaches before generating** — Before proposing a fix, present 2-3 approaches with pros, cons, effort estimate, and risk level. Let the user choose the direction before documenting the fix plan.

4. **Present output section-by-section** — Present each section (problem, root cause, fix approach, test plan, rollback plan) individually. Ask for approval before moving to the next.

5. **Track outstanding questions** — If something cannot be determined without more investigation:
   - **Resolve before fix** — Blocks implementation (e.g., "need to verify if this affects production data")
   - **Verify during fix** — Can be confirmed during implementation

6. **Multiple handoff options** — At completion, present 3-4 next steps as options (see CLOSING SUMMARY).

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing tech-spec at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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

Create a single-document specification for a bug fix or hotfix. This is the Bug
mode equivalent of the entire Product mode pipeline, but it now derives from an
upstream failure-understanding ideation step rather than a raw symptom-only
conversation.

The tech spec standalone answers five questions:
1. What is broken?
2. Why is it broken? (root cause)
3. How should we fix it? (approach + alternatives)
4. How do we verify the fix? (test plan)
5. How do we undo the fix if it causes problems? (rollback plan)

## CONTEXT LOADING

Load context in this order of priority:

1. **Opportunity Pack**: Read `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
   first.
2. **Coverage Matrix**: Read `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` if
   it exists.
3. **$ARGUMENTS**: If the user passes a bug description or Linear issue URL, use
   it as additional context.
4. **External issue tracker adapter**: If available and an issue URL is provided, import bug
   details, reproduction steps, and any attached logs.
5. **ENRICHES scan**: Check for existing architecture docs to understand the
   system context.
6. **User Interview**: Fill the remaining bug investigation gaps.

## INTERVIEW PROTOCOL

This interview is 5 core questions, asked one at a time. The goal is to build a complete picture of the bug before proposing fixes.

### Question 1: What's the Bug?

> "What's happening that shouldn't be happening? Describe the bug from the user's perspective."

**Follow-up probes** (ask one at a time only if needed):
- If too vague: "Can you show me the error message, screenshot, or log output?"
- If symptoms only: "Is this happening for all users or specific conditions?"

### Question 2: How to Reproduce?

> "How do you reproduce this bug? Walk me through the exact steps."

**Follow-up probes:**
- If inconsistent: "Does it happen every time, or intermittently? If intermittent, how often?"
- If unclear trigger: "What changed recently? New deployment, data migration, config change?"

### Question 3: Expected vs. Actual

> "What should happen (expected behavior) vs. what actually happens (actual behavior)?"

**Follow-up probes:**
- If expected behavior is unclear: "Before this bug existed, what did the user experience?"

### Question 4: Impact Assessment

> "How critical is this? How many users are affected, and what's the business impact?"

Present severity options:
> "Based on what you've described, I'd assess this as:
> 1. **Critical** — System down, data loss, or security vulnerability. Fix immediately.
> 2. **High** — Major feature broken, significant user impact. Fix this sprint.
> 3. **Medium** — Feature partially broken, workaround exists. Fix soon.
> 4. **Low** — Cosmetic or edge case. Fix when convenient.
>
> I'm leaning toward [severity] because [reason]. Does that feel right?"

### Question 5: Context Clues

> "Do you have any clues about the root cause? Suspicious code paths, recent changes, error stack traces?"

**Follow-up probes:**
- If no clues: "When did this start happening? Was there a recent deployment or change?"
- If multiple theories: "Which theory feels most likely? Let's investigate that first."

## ROOT CAUSE ANALYSIS

After the interview, propose a root cause analysis:

1. **Hypothesize** — Based on the interview, propose 1-3 hypotheses for the root cause
2. **Narrow** — For each hypothesis, describe what evidence would confirm or reject it
3. **Conclude** — Present your best assessment of the root cause with confidence level (HIGH/MEDIUM/LOW)

> "Based on what you've described, here's my analysis:
>
> **Most likely root cause:** [description]
> **Confidence:** [HIGH/MEDIUM/LOW]
> **Evidence:** [what supports this]
>
> Does this match your intuition, or should we explore other possibilities?"

## FIX APPROACH PROPOSAL

After root cause is confirmed, propose 2-3 fix approaches:

For each approach, provide:
- **Description:** What the fix does
- **Pros:** Why this approach works well
- **Cons:** Tradeoffs and risks
- **Effort:** Estimated time (hours/days)
- **Risk:** Likelihood of introducing new issues (Low/Medium/High)

Highlight your recommendation and explain why.

> "I see [2-3] ways to fix this:
>
> **Approach A: [Name]** (Recommended)
> [description]
> Pros: [why it's best] | Cons: [tradeoffs] | Effort: [estimate] | Risk: Low
>
> **Approach B: [Name]**
> [description]
> Pros: [advantages] | Cons: [tradeoffs] | Effort: [estimate] | Risk: Medium
>
> I recommend Approach A because [reason]. Which approach do you want to go with?"

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/bugs/tech-spec-{slug}.md` follows the template in `knowledge/template.md`.

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the tech-spec-standalone document template and standard structure.

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Problem description is clear and specific
- [ ] Reproduction steps are documented (or marked "intermittent" with known conditions)
- [ ] Root cause analysis is present with confidence level
- [ ] At least 1 fix approach documented with pros/cons
- [ ] Affected components listed
- [ ] Test plan has at least 2 test cases (reproduce bug + regression test)
- [ ] Rollback plan is documented

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display the summary and offer multiple next steps:

```text
tech-spec-{slug}.md saved to `docs/ets/projects/{project-slug}/bugs/tech-spec-{slug}.md`

Status: [COMPLETE | DRAFT]
Severity: [Critical | High | Medium | Low]
Fix approach: [chosen approach name]

What would you like to do next?

1. Implement the fix (Recommended) — Use /ce:work to start fixing
2. Create a Linear issue — Track this fix in your project management tool
3. Refine this spec — Adjust root cause analysis or fix approach
4. Pause for now — Save and return later
```

Wait for the user's choice before proceeding. Do not auto-advance.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `$ARGUMENTS` or user description + ENRICHES documents (if available)
- **Action:** Load any existing architecture docs for system context. Import from Linear if URL provided.
- **Output:** Internal context (existing docs loaded or none)

### Step 2: Bug Investigation Interview (one question at a time)
- **Input:** Step 1 context + user responses (interactive)
- **Action:** Run the 5-question INTERVIEW PROTOCOL. Ask one question per message, wait for answers, use follow-up probes as needed.
- **Output:** Raw investigation notes (internal)

### Step 3: Root Cause Analysis
- **Input:** Interview data + system context
- **Action:** Propose 1-3 hypotheses, present evidence, conclude with best assessment and confidence level.
- **Checkpoint:** "Here's my root cause analysis. Does this match your intuition?"

### Step 4: Fix Approach Proposal
- **Input:** Confirmed root cause
- **Action:** Propose 2-3 fix approaches with pros, cons, effort, and risk. Highlight recommendation.
- **Checkpoint:** "Which approach do you want to go with?"

### Step 5: Section-by-Section Generation & Approval
- **Input:** All investigation data + chosen fix approach
- **Action:** Generate the spec section by section, presenting each for approval:
  1. **Problem Description** — Present, ask "Does this capture the issue?"
  2. **Reproduction Steps** — Present, confirm accuracy
  3. **Root Cause Analysis** — Present, confirm
  4. **Fix Approach** (chosen + alternatives) — Present, confirm
  5. **Affected Components** — Present, ask if complete
  6. **Test Plan** — Present test cases, ask for additions
  7. **Rollback Plan** — Present, confirm feasibility
  8. **Timeline** — Present estimate, calibrate
- **Checkpoint per section:** "Does this section look right?"

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
  1. Generate slug from bug description (lowercase, hyphens, no special chars)
  2. Verify directory exists: `docs/ets/projects/{project-slug}/bugs/` — create if missing
  3. Write the complete document to `docs/ets/projects/{project-slug}/bugs/tech-spec-{slug}.md` using the Write tool
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/bugs/tech-spec-{slug}.md`) + paths to upstream documents (none — bug specs have no BLOCKS dependencies)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/bugs/tech-spec-{slug}.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 11: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist. Display CLOSING SUMMARY.
- **Handoff:** Present the next-step options. Let the user choose.
- **Output:** Document marked COMPLETE or DRAFT

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| Can't reproduce the bug | Medium | Document known conditions, mark as intermittent | Proceed with best available info |
| Root cause unclear | Medium | Document hypotheses with confidence levels, recommend investigation | Mark root cause as HYPOTHESIS, proceed |
| User has no context about the system | Medium | Ask focused architecture questions inline | Proceed with user-provided info only |
| Output validation fails | High | Mark as DRAFT, flag gaps | Proceed with DRAFT status |
| Multiple bugs discovered during investigation | Medium | Suggest splitting into separate specs | Focus on the primary bug first |

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
