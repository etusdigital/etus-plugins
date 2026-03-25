---
name: disc-project-context
description: >
  Use when starting a new project, gathering initial project context, or conducting a
  5W2H interview. Also triggers on 'new project', 'project context', 'what are we
  building', 'tell me about the project', or when the discovery-agent begins its
  workflow. This is always the first document in any product documentation effort.
model: opus
version: 1.0.0
argument-hint: "[upstream-context]"
compatibility: "Optional: Slack MCP (pull existing project discussions)"
---

## PURPOSE

The 5W2H interview is the **structural foundation** of Discovery. It captures
essential project context in a repeatable, traceable format that subsequent
phases (Planning, Design, Implementation) depend on. This skill now derives
from the Opportunity Pack instead of re-eliciting the raw idea from scratch,
so project-context.md becomes a structured synthesis of an already-covered
problem space.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — Ideation is now the root
  artifact. project-context derives its structured 5W2H context from the
  already-covered opportunity space.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` — Helps confirm that actors,
  JTBDs, journeys, use cases, and edge cases were actually covered before
  5W2H synthesis.

This skill is the first Discovery synthesis step after ideation.

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information. These patterns exist to create a conversational, collaborative interview experience rather than a form-filling exercise.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. This prevents overwhelming the user and produces more thoughtful, detailed answers. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., scope, product type, deployment model), present 3-4 concrete options with a brief description of each. Highlight your recommendation. Let the user pick before proceeding.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs. Example: "I see two ways to frame the technical context: (A) stack-first — lead with your tech choices, (B) constraint-first — lead with what limits your options. I recommend B because it surfaces risks early."

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section (e.g., Project Identity, then Business Context, then Technical Context), ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Resolve before next phase** — This blocks the handoff. Keep asking until resolved.
   - **Deferred to [phase name]** — Noted and carried forward in Handoff Notes. Won't block progress.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options instead of a single fixed path.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing project-context.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- New product from scratch (greenfield)
- New market segment or unfamiliar domain
- Multiple stakeholders with potentially conflicting priorities

**Use short version when:**
- Adding a feature to a well-documented existing product
- Bug fix or improvement with clear scope
- Even in short version, still include: Project Identity, Problem Statement, Constraints, and Handoff Notes

## PRESSURE TEST

Before generating content, challenge the framing with these questions (ask the most relevant 1-2, not all):

- **Is this the right problem?** — "Before we proceed, let me push back: is [stated problem] the real problem, or is it a symptom of something deeper?"
- **What happens if we do nothing?** — "What's the cost of NOT building this? If the answer is 'not much,' the priority might need rethinking."
- **Is there a better framing?** — "Could we reframe this in a way that solves a bigger problem with similar effort?"
- **Are we building for the right user?** — "You mentioned [user]. Are they the ones who feel the most pain, or is there a higher-leverage audience?"

The goal is to sharpen the problem framing, not to block progress. If the user's framing is solid, acknowledge it and move on quickly. Only dig deeper when genuine misframing signals appear.

## CONTEXT LOADING

Load context in this order of priority:

1. **Opportunity Pack**: Read `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
   first.
2. **Coverage Matrix**: Read `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` if
   it exists.
3. **$ARGUMENTS**: If the user passes `[upstream-context]`, read that file as
   additional context.
4. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for any existing
   project files or prior interview notes.
5. **User Interview**: Fill gaps and refine the 5W2H instead of re-eliciting
   the entire problem space.

## INTERVIEW PROTOCOL

This interview follows a one-question-at-a-time rhythm. Ask the primary question alone in one message, wait for the user's answer, then decide whether to ask a follow-up probe or move to the next 5W2H dimension. This conversational pace helps the user think deeply about each answer rather than rushing through a checklist.

### Step 0: Scope Assessment

Before diving into the 5W2H, ask a single scoping question to calibrate interview depth:

> "Before we dive in, I'd like to understand the scope. Is this:
> **(A) A new product from scratch** — greenfield, no existing codebase or users
> **(B) A new feature in an existing product** — adding capability to something that already exists
> **(C) A bug fix or improvement** — enhancing or fixing something specific
> **(D) Research / exploration** — not sure yet, still figuring it out
>
> I recommend picking the closest fit — we can adjust as we go."

Use the answer to calibrate:
- **(A)** Full-depth interview, all 7 dimensions, probes encouraged
- **(B)** Focus on WHAT, WHO, WHY, HOW. Lighter on WHERE and HOW MUCH (existing product likely has answers)
- **(C)** Abbreviated interview — focus on WHAT and WHY. Other dimensions only if relevant
- **(D)** Exploratory mode — focus on WHY and WHO first, circle back to WHAT once the problem is clearer

### Step 1: WHAT (Project Identity)

**Primary question** (ask alone, one message):
> "What are we building? Describe the product, service, or feature in your own words."

**Follow-up probes** — ask one at a time based on the answer:
- If the description is vague: "Can you give me the elevator pitch — one sentence that captures what this is?"
- If scope is unclear: "Is this a standalone product, a feature within something bigger, or something else?"
- If product type is ambiguous: "Would you call this a tool, a platform, a service, or something else?"

Move to the next dimension once you have a clear picture of WHAT is being built.

### Step 2: WHO (Stakeholders & Users)

**Primary question** (ask alone, one message):
> "Who are the key people involved? Tell me about the end users and the stakeholders or decision-makers."

**Follow-up probes** — ask one at a time based on the answer:
- If only one user type mentioned: "Are there other types of users? For example, admins vs. end users, or internal vs. external?"
- If stakeholders are vague: "Who's making the final decisions on this project? Who has to approve the direction?"
- If user scale is unknown: "How many users are we talking about — tens, hundreds, thousands, millions?"

### Step 3: WHERE (Context & Environment)

**Primary question** (ask alone, one message):
> "Where does this product live? Tell me about the deployment context — cloud, on-prem, browser, mobile, etc."

**Follow-up probes** — ask one at a time based on the answer:
- If infrastructure is unclear: "Is there existing infrastructure we need to integrate with, or are we starting fresh?"
- If deployment is ambiguous: "Which cloud platform, if any? Or is this on-premises?"

Skip deeper probes if scope assessment was (B) or (C) and the user already covered this.

### Step 4: WHEN (Timeline & Urgency)

**Primary question** (ask alone, one message):
> "When does this need to ship? What's driving the timeline?"

**Follow-up probes** — ask one at a time based on the answer:
- If no concrete date: "Is there a hard deadline, or is this more flexible?"
- If deadline exists: "What's driving that deadline — a market window, a contract, a dependency on another team?"
- If phased: "What's the MVP timeline vs. the full product timeline?"

### Step 5: WHY (Business & User Motivation)

**Primary question** (ask alone, one message):
> "Why are we building this? What specific problem does it solve?"

**Follow-up probes** — ask one at a time based on the answer:
- If business case is unclear: "What's the expected business outcome — revenue, cost saving, retention, compliance?"
- If problem is generic: "Can you give me a concrete example of someone experiencing this problem today?"
- If competitive pressure exists: "Is this driven by competitor moves, or by user demand?"

### Step 6: HOW (Approach & Constraints)

**Primary question** (ask alone, one message):
> "How will we approach this? Tell me about the technical and organizational constraints."

**Follow-up probes** — ask one at a time based on the answer:
- If tech stack is missing: "What languages, frameworks, or platforms are we using or considering?"
- If team structure is unclear: "What does the team look like — size, roles, skill gaps?"
- If constraints are light: "Are there any legacy systems, regulatory requirements, or hard technical limits we need to work around?"

### Step 7: HOW MUCH (Budget & Resources)

**Primary question** (ask alone, one message):
> "What resources do we have? Budget, team size, and any external dependencies."

**Follow-up probes** — ask one at a time based on the answer:
- If budget is vague: "Is there a specific budget ceiling, or is it more 'as needed'?"
- If dependencies exist: "Are we waiting on other teams or vendors for anything?"

Skip this dimension entirely for scope (C) or (D) unless the user brings it up.

### Interview Completion

After all relevant dimensions are covered, present a brief synthesis of what you captured and ask: "Does this summary feel complete, or did we miss anything important?"

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/discovery/project-context.md` contains:

- **Project Identity**: Name, one-liner description, type, scope
- **Stakeholders & Users**: Decision makers, user personas, user count estimates
- **Business Context**: Problem statement, business outcome, success criteria
- **Technical Context**: Tech stack, deployment environment, constraints
- **Timeline & Resources**: Deadline, team size, budget, dependencies
- **Interview Date & Interviewer**: Metadata and traceability
- **Handoff Notes**: Any open questions or follow-up items

All answers are tied to the 5W2H framework for easy cross-referencing in Planning and Design phases.

## KNOWLEDGE POINTERS

- Read `references/template.md` for the project-context.md document template and structure.
- Read `references/guide.md` for interview best practices: active listening, clarifying ambiguous answers, capturing constraints without bias.

---

**This skill is the first Discovery synthesis step after ideation.** Upon
completion, present the user with handoff options (see CLOSING SUMMARY) — the
recommended path is product-vision generation via the discovery-agent.

## INPUT VALIDATION

This skill has no upstream document dependencies. Input comes from the user interview.
Aim for substantive answers (not single-word responses) for at least 5 of the 7 5W2H dimensions before generating — this ensures enough context for downstream skills to work effectively.

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] All 7 5W2H sections have substantive content (not placeholders)
- [ ] Tech stack is explicitly listed (languages, frameworks, infra)
- [ ] At least 2 user types/personas identified
- [ ] Timeline includes at least one milestone with date
- [ ] Constraints section has at least 3 explicit constraints
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ project-context.md saved to `docs/ets/projects/{project-slug}/discovery/project-context.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document establishes context, not traceable IDs)
```

Then present these options using AskUserQuestion (or as a numbered list if AskUserQuestion is unavailable):

1. **Proceed to Product Vision (Recommended)** — Start defining vision, business objectives (BO-#), and brainstorm ideas
2. **Refine this document** — Review and improve specific sections before moving on
3. **Pause for now** — Save and return later (the document is already on disk)

Wait for the user to choose before taking any action. Do not auto-proceed to the next skill.

## WORKFLOW

### Step 1: Context Detection
- **Input:** Check `docs/ets/projects/{project-slug}/discovery/` for existing project-context.md
- **Action:** If exists, offer to update rather than regenerate
- **Output:** Decision: create new or update existing

### Step 2: Scope Assessment
- **Input:** User response to scope question (A/B/C/D)
- **Action:** Calibrate interview depth based on scope type
- **Output:** Interview depth setting (full / focused / abbreviated / exploratory)

### Step 3: 5W2H Interview
- **Input:** User responses (interactive, one question per message)
- **Action:** Ask primary question alone, wait for answer, choose follow-up probe or move to next dimension. Respect the interview depth from Step 2.
- **Output:** Raw interview notes (internal)

### Step 4: Section-by-Section Document Generation
- **Input:** Interview notes from Step 3
- **Action:** Generate the document one major section at a time, using the template from `knowledge/template.md`. For each section:
  1. **Propose approach** — Before generating, briefly describe how you plan to frame this section (e.g., "For Technical Context, I'll lead with your constraints since those shape all other choices.")
  2. **Generate the section** — Present it to the user
  3. **Ask for approval** — "Does this capture it well? Anything to adjust?"
  4. **Incorporate feedback** — If the user wants changes, revise and re-present
  5. **Move to next section** — Only after the user approves

  Section order:
  - Project Identity (name, description, type, scope)
  - Stakeholders & Users (decision makers, personas, user estimates)
  - Business Context (problem statement, business outcome, success criteria)
  - Technical Context (stack, deployment, constraints)
  - Timeline & Resources (deadline, team, budget, dependencies)
  - Handoff Notes (open questions, deferred items)
- **Output:** Approved sections assembled into complete project-context.md
- **Integration:** Consumed by product-vision skill (BLOCKS dependency)

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
  1. Verify directory exists: `docs/ets/projects/{project-slug}/discovery/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/discovery/project-context.md` using the Write tool
  3. The document is only saved when written to the filesystem — presenting content in chat is not the same as saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/discovery/project-context.md`) + paths to upstream documents (none — this is the root document)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 9: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/discovery/project-context.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 10: Validation
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT

### Step 11: Handoff Options
- **Action:** Present multiple next-step options (see CLOSING SUMMARY)

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| User provides single-word answers | Medium | Re-ask with specific examples | Accept minimal answer, mark section as thin |
| User refuses to answer a 5W2H question | Low | Skip question, note as "Not provided" | Proceed — downstream skills will ask if needed |
| Existing project-context.md found | Info | Ask: "Update existing or start fresh?" | Default to update |
| Output validation fails | High | Mark as DRAFT, flag specific gaps | Proceed — product-vision will inherit gaps |

## REFLECTION PROTOCOL

Before finalizing the document, run this internal metacognitive check:

### 1. Assumption Audit
- What assumptions am I making about the user's context?
- Am I filling gaps with generic defaults instead of asking?
- Score: LOW / MEDIUM / HIGH confidence in context completeness

### 2. Alternative Perspectives
- Would a different approach make more sense given the constraints?
- Are there objectives or perspectives I haven't considered?
- Have I challenged the user's stated assumptions constructively?

### 3. Completeness Check
- Does every section have substantive content (not placeholders)?
- Are IDs sequential and traceable to upstream documents?
- Would a downstream skill have enough context to work from this document?

### 4. Confidence-Based Decision
| Confidence | Action |
|------------|--------|
| LOW on any section | Ask the user ONE targeted question before finalizing |
| MEDIUM | Flag inline with `<!-- CONFIDENCE: MEDIUM — [reason] -->` and proceed |
| HIGH | Proceed directly to OUTPUT VALIDATION |
