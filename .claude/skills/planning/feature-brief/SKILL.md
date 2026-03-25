---
name: feature-brief
description: >
  Use when documenting a single feature without requiring the full product pipeline.
  Also triggers on 'feature brief', 'document feature', 'new feature', 'add
  feature', or when wanting to spec a standalone feature quickly.
model: opus
version: 1.0.0
argument-hint: "[feature description]"
compatibility: "Optional: external issue tracker adapter (for example, Linear) for feature request context, Slack MCP (pull feature discussions)"
---

## Elicitation Entry Rule

BEFORE asking anything in any module:
1. Read `knowledge/elicitation-state.yaml`
2. Find the corresponding module
3. If status == "covered" → summarize what exists, ask if user wants to go deeper
4. If status == "in_progress" → continue from current_probe
5. If status == "not_started" → start with story probe (see knowledge/story-probes.md)
6. After each question → update elicitation-state.yaml
7. After each story → generate SNAP-# (see Story Snapshots in ideate SKILL.md)

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (required — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — The feature brief now derives
  from the ideation layer instead of raw conversation alone.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md` — Feature definition should only happen after a solution direction is chosen and risks are reduced.
- `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-status.md` — Canonical feature state. Use it to recover slug, tracking mode, next step, and linked upstream docs.

**ENRICHES** (improves output — use if available):
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` — Provides traceable coverage
  for actors, JTBDs, journeys, use cases, edge cases, and assumptions.
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Provides business context, tech stack, and constraints that help frame the feature more accurately.
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — If the product already has a vision doc, BO-# objectives help align the feature with business goals.
- `docs/ets/projects/{project-slug}/planning/prd.md` — If a PRD exists, the feature can reference existing PRD-F-# items and avoid scope overlap.

**Resolution protocol:**
1. Check ENRICHES: do any of the above documents exist?
2. If yes → load them silently for context. Mention to the user: "I found existing docs that provide context — I'll use them to inform this feature brief."
3. If no → proceed without them. Do not ask the user to create upstream docs.

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- Feature touches multiple system components (frontend, backend, data)
- Feature has >3 user stories or complex acceptance criteria
- Feature needs formal design delta analysis

**Use short version when:**
- Small, isolated feature with clear scope and 1-2 stories
- Enhancement to existing functionality with minimal changes
- Even in short version, still include: problem statement, user stories with acceptance criteria, and scope boundaries

## ARTIFACT SAVE RULE

**Why this matters:** The feature brief is the anchor document for Feature mode. Downstream skills (user-stories, design-delta, impl-plan) need this file on disk to read scope and acceptance criteria.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md`
3. Displaying content in chat is not the same as saving — the file needs to exist on the filesystem for downstream skills to consume it
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only then propose the next step

**If the Write fails:** Report the error to the user and do not proceed to the next skill — downstream documents depend on this file existing.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Feature briefs benefit from focused answers. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction, present 3-4 concrete options with a brief description of each. Highlight your recommendation. Let the user pick before proceeding.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs. For example, before defining scope: propose "narrow surgical scope" vs "broader scope with phases" vs "experimental/flagged scope."

4. **Present output section-by-section** — Do not generate the full feature brief at once. Present each major section (problem statement, feature description, target users, acceptance criteria, scope boundaries, design considerations), ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something cannot be answered now, classify it:
   - **Resolve before implementation** — This blocks the handoff to design-delta or impl-plan.
   - **Deferred** — Noted and carried forward in the document's Outstanding Questions section.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options (see CLOSING SUMMARY).

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing feature-brief at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

8. **Assess if full process is needed** — If the user's input is already detailed with clear requirements, specific acceptance criteria, and defined scope, don't force the full interview. Confirm understanding briefly and offer to skip directly to document generation. Only run the full interactive process when there's genuine ambiguity to resolve.

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

Document a single feature within an existing product without requiring the full
Product mode pipeline. This is the lightweight alternative to a full PRD, but
it now derives from the Opportunity Pack so that feature docs inherit actors,
JTBDs, journeys, use cases, edge cases, constraints, and assumptions instead of
rediscovering them from scratch.

Feature briefs are the entry point for Feature mode. They replace the need for project-context + product-vision + prd when the user just wants to spec one feature.

## CONTEXT LOADING

Load context in this order of priority:

1. **Feature Status**: Read `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-status.md` first.
2. **Opportunity Pack**: Read `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
   first.
3. **Solution Discovery**: Read `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md`.
4. **Coverage Matrix**: Read `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` if
   it exists.
5. **$ARGUMENTS**: If the user passes `[feature description]`, use it as
   additional context.
6. **ENRICHES scan**: Check for existing docs (`project-context.md`,
   `product-vision.md`, `prd.md`) to provide context without requiring them.
7. **Execution Adapter Context**: If an execution adapter is active and exposes feature metadata, use it only as optional context enrichment.
8. **User Interview**: Fill feature-specific gaps instead of rediscovering the
   whole problem space.

## INTERVIEW PROTOCOL

This interview is 5 core questions, asked one at a time. Each question builds on the previous answer. Follow-up probes are optional and used only when the answer needs more depth.

### Question 1: What Feature?

> "Tell me about a concrete situation where the user would need this feature. What did they try to do? Where did they get stuck?"

**Follow-up probes** (ask one at a time only if needed):
- If too vague: "Can you walk me through what happened step by step — who was involved and what went wrong?"
- If too broad: "This sounds like it might be multiple features. What's the single most important behavior?"
- Refer to `knowledge/story-probes.md` for additional story-based probes.
- Refer to `knowledge/vague-response-escalation.md` for handling vague or generic answers.

### Question 2: Who Benefits?

> "Who is the primary user of this feature? What's their role, and what frustrates them today?"

**Follow-up probes:**
- If no pain point: "What are they doing today instead? What's broken or slow about that?"
- If multiple personas: "Which persona benefits the most? That's your primary user."

### Question 3: Success Criteria

> "How will you know this feature is working? What does success look like — what should be true that isn't true today?"

**Follow-up probes:**
- If too generic: "Can you make that measurable? For example: 'reduces time from X to Y' or 'eliminates manual step Z'"
- If only one criterion: "What else would tell you this is working well? Think about both the user and the business."

### Question 4: Non-Goals (NG-#)

> "What is this feature explicitly NOT doing? What should we resist adding?"

**Follow-up probes:**
- If "nothing is out of scope": "Every feature has boundaries. What's the adjacent feature you might be tempted to include but shouldn't?"
- For each exclusion identified: "Why is this excluded — is it permanent, deferred to a later version, or conditional on something?"
- For each exclusion: "What's the closest valid behavior that neighbors this non-goal? Where does the boundary lie?"

**Output format:** Each non-goal identified in Q4 MUST be captured as a structured NG-# item:

```markdown
### NG-1: [What NOT to do]
- **Statement:** [what must NOT happen — specific and testable]
- **Reason:** [why excluded]
- **Scope:** permanent | deferred_to_v2 | conditional
- **Adjacent behavior:** [valid functionality that neighbors this non-goal]
- **Downstream docs that must respect:** [user-stories, feature-spec, api-spec, tech-spec, wireframes, impl-plan — whichever apply]
```

Generate one NG-# per exclusion. Minimum 1 NG-# per feature brief. If the user says "nothing is out of scope," push back — every feature has boundaries.

### Question 5: Constraints

> "Are there any constraints — technical, timeline, design, or business — that affect how this should be built?"

**Follow-up probes:**
- If no constraints mentioned: "Does this need to work with existing systems? Any performance requirements? Any deadlines?"

## AUTO-ESCALATION

After completing the interview, assess complexity:

- If **>5 acceptance criteria** or **>3 personas** → suggest escalation:
  > "This feature has significant scope — [N] acceptance criteria and [M] personas. This looks more like a product initiative than a single feature. Want to switch to full Product mode with `/orchestrator`? Or should we continue with the feature brief?"

Honor the user's choice. The suggestion is informational, not blocking.

## ID GENERATION

**FB-# Pattern**: Feature Brief items. Format: `FB-1`, `FB-2`, etc. Each FB-# represents a distinct behavior or capability within the feature.

- FB-# IDs are local to this feature brief (not global across all feature briefs)
- Each FB-# should have a clear name and description
- Typically 1-4 FB-# items per feature brief (more suggests escalation to Product mode)

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md` follows the template in `knowledge/template.md`.

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the feature-brief document template and standard structure.
- Read `knowledge/story-probes.md` for story-based elicitation probes.
- Read `knowledge/vague-response-escalation.md` for vague-response patterns and escalation questions.

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Problem statement describes a specific problem (not generic)
- [ ] At least 1 persona identified with pain point
- [ ] At least 2 acceptance criteria defined (specific and testable)
- [ ] Scope boundaries defined (in-scope and out-of-scope sections populated)
- [ ] At least 1 NG-# defined with statement, reason, scope, adjacent behavior, and downstream docs
- [ ] At least 1 FB-# item defined with description
- [ ] At least 1 JTBD-#, 1 UC-#, and 1 EDGE-# from ideation are referenced or explicitly marked not applicable

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display the summary and offer multiple next steps:

```text
feature-brief.md saved to `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list FB-# IDs, e.g., FB-1, FB-2]

What would you like to do next?

1. Create User Stories (Recommended) — Decompose this feature into testable stories (US-#)
2. Create Design Delta — Document what changes in the architecture for this feature
3. Go straight to implementation — Use /ce:work to start building
4. Refine this feature brief — Review and improve specific sections
5. Pause for now — Save and return later
```

Wait for the user's choice before proceeding. Do not auto-advance to the next skill.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `$ARGUMENTS` or user description + ENRICHES documents (if available)
- **Action:** Check for existing project docs. Load silently if found. Summarize any relevant context to the user.
- **Output:** Internal context (existing docs loaded or none)
- **Checkpoint:** If ENRICHES found: "I found existing project docs — I'll use them for context. Let's focus on your feature."

### Step 2: Feature Interview (one question at a time)
- **Input:** Step 1 context + user responses (interactive)
- **Action:** Run the 5-question INTERVIEW PROTOCOL. Ask one question per message, wait for answers, use follow-up probes as needed.
- **Output:** Raw interview notes (internal)

### Step 3: Complexity Assessment
- **Input:** Interview responses
- **Action:** Count acceptance criteria and personas. If thresholds exceeded, run AUTO-ESCALATION check.
- **Output:** Decision to continue or escalate

### Step 4: Approach Proposal
- **Input:** Interview data
- **Action:** Before generating content, propose 2-3 approaches for how to frame this feature brief:
  - **Narrow and surgical** — Minimal scope, fastest to implement, lowest risk
  - **Balanced** — Core feature with key edge cases covered
  - **Comprehensive** — Full feature with all considerations documented
- **Checkpoint:** Ask the user which approach feels right.

### Step 5: Section-by-Section Generation & Approval
- **Input:** All interview data + chosen approach
- **Action:** Generate the feature brief section by section, presenting each for approval:
  1. **Problem Statement** — Present, ask "Does this capture the problem well?"
  2. **Feature Description (FB-# items)** — Present, ask for adjustments
  3. **Target Users** — Present persona(s), confirm
  4. **Acceptance Criteria** — Present each, refine
  5. **Scope Boundaries** — Present in-scope / out-of-scope, confirm
  6. **Design Considerations** — Present, ask what's missing
  7. **Dependencies & Outstanding Questions** — Present, confirm
- **Checkpoint per section:** "Does this section look right? Anything to adjust before we move on?"

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
  1. Generate slug from feature name (lowercase, hyphens, no special chars)
  2. Verify directory exists: `docs/ets/projects/{project-slug}/features/{feature-slug}/` — create if missing
  3. Write the complete document to `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md` using the Write tool
  4. The document needs to exist on the filesystem for downstream skills to consume it — presenting content in chat is not sufficient.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md`) + paths to upstream documents (`docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md`, `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/features/{feature-slug}/feature-brief.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
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
| No ENRICHES docs found | Low | Proceed without context — this is expected in Feature mode | None needed |
| User can't define acceptance criteria | Medium | Suggest 2-3 criteria based on the feature description | Proceed with user-confirmed suggestions |
| Auto-escalation threshold hit | Low | Suggest Product mode, honor user's choice | Continue with feature brief |
| Output validation fails | High | Mark as DRAFT, flag gaps | Proceed with DRAFT status |
| Slug collision (file already exists) | Medium | Ask user: overwrite or create new version? | Append -v2 suffix |

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
