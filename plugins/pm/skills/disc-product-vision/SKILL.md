---
name: disc-product-vision
description: >
  Use when defining product vision, business objectives, target audience, or
  brainstorming product direction. Also triggers on 'what problem are we solving',
  'who are our users', 'define the vision', 'product vision', 'business objectives',
  or 'value proposition'.
model: opus
version: 1.0.0
argument-hint: "[context-path]"
compatibility: "Optional: Slack MCP (pull product discussions and feedback)"
---

## PURPOSE

Transform the opportunity pack + project context into a strategic vision
document that aligns stakeholders around a unified problem statement, business
objectives, and success metrics. This skill combines structured vision
interviews with the BMAD Creative Intelligence Suite (technique-driven
brainstorming) to surface insights and validate assumptions before moving into
Planning.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — Ensures the problem space,
  actors, JTBDs, journeys, use cases, and edge cases have already been covered
  before strategic framing.
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Needed for business context, stakeholders, constraints, and tech stack to inform vision.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` — Helps validate whether the
  ideation coverage is complete enough before running solution-oriented
  brainstorming.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `product-vision.requires: [project-context]`
2. Check: does `docs/ets/projects/{project-slug}/discovery/project-context.md` exist, is non-empty, and is not `<!-- STATUS: DRAFT -->`?
3. If missing → INFORM user → auto-invoke `project-context` skill → wait → continue
4. If DRAFT → WARN: "project-context.md is DRAFT — vision may be less informed" → proceed

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information. Vision work is inherently creative and strategic — these patterns ensure the user feels like a collaborator, not a form-filler.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Vision questions benefit from reflection time, so give the user space to think. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., brainstorm technique, positioning approach, North Star metric), present 3-4 concrete options with a brief description of each. Highlight your recommendation. Let the user pick before proceeding.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs. Example: "I see three ways to frame this vision: (A) technology-first — lead with the technical innovation, (B) user-outcome-first — lead with the transformation users experience, (C) market-opportunity-first — lead with the gap in the market. I recommend B because it resonates with both investors and users."

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section (e.g., Vision Statement, then Business Objectives, then Personas, then Value Proposition), ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Resolve before next phase** — This blocks the handoff. Keep asking until resolved.
   - **Deferred to [phase name]** — Noted and carried forward as Critical Assumptions. Won't block progress.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options instead of a single fixed path.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing product-vision.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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

## CONTEXT LOADING

Load context in this order of priority:

1. **Opportunity Pack**: Read `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
   first.
2. **Project Context**: Read `docs/ets/projects/{project-slug}/discovery/project-context.md`.
3. **Coverage Matrix**: Read `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` if
   it exists.
4. **$ARGUMENTS**: If the user passes `[context-path]`, read that file as
   additional context.
5. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for any upstream
   discovery artifacts or vision drafts.
6. **User Interview**: Fill strategic gaps rather than rediscovering the raw
   idea.

## VISION INTERVIEW PROTOCOL

This interview follows a one-question-at-a-time rhythm. Ask each question alone in one message, wait for the user's answer, then decide whether to ask a follow-up or move forward. Vision questions are strategic and benefit from space for reflection.

### Block 1: Vision & North Star

**Question 1** (ask alone, one message):
> "Imagine it's 2-3 years from now and this product is wildly successful. What does that future look like? Paint me a picture."

Wait for the answer. Then ask:

**Question 2** (ask alone, one message):
> "Now distill that into one sentence — what is the vision in a single line?"

**Follow-up probes** — ask one at a time only if needed:
- If the vision is too generic: "That's a good start, but it could apply to many products. What makes YOUR vision specific?"
- If no metric mentioned: "What single metric would tell you this vision is being realized? That's your North Star."

### Block 2: Business Objectives

**Question 3** (ask alone, one message):
> "What does success look like for this business? What are the 2-3 most important things you want to achieve?"

Wait for the answer. Then ask:

**Question 4** (ask alone, one message):
> "Now let's get specific. For each of those success factors, what's the metric and the target? Example: 'Hit $100K MRR by month 12' or '10K active users in year 1.'"

Wait for the answer. Then ask:

**Question 5** (ask alone, one message):
> "If you could only hit ONE of these objectives, which would it be? That's your North Star priority."

**Before generating BO-# IDs**, propose 2-3 strategic framings:
> "Based on what you've told me, I see a few ways to structure your business objectives:
> **(A) Growth-first** — Lead with user acquisition and market share, monetization follows
> **(B) Revenue-first** — Lead with revenue and unit economics, growth is a means to that end
> **(C) Impact-first** — Lead with the user/market transformation, business metrics track adoption of that impact
>
> I recommend [X] because [reason]. Which framing feels right for your BO-# structure?"

Only after the user chooses, generate BO-1, BO-2, BO-3... IDs. Business Objectives are exclusively defined in this document.

### Block 3: Target Users

**Question 6** (ask alone, one message):
> "Who are your primary users? Describe them — their role, their challenges, their goals."

Wait for the answer. Then ask:

**Question 7** (ask alone, one message):
> "Are there secondary users who are different from the primary ones? For example, admins vs. end users, or buyers vs. consumers."

**Follow-up probes** — ask one at a time only if needed:
- If Jobs to Be Done are unclear: "When your primary user reaches for this product, what job are they trying to get done?"
- If value is vague: "What specific value do you provide to this persona — not 'better tools' but 'save 5 hours/week' or 'reduce risk by 80%'?"

### Block 4: Value Proposition & Differentiation

**Question 8** (ask alone, one message):
> "What do your users do today instead of using your product? What are the top 2-3 alternatives — competitors, DIY solutions, manual workarounds?"

Wait for the answer. Then ask:

**Question 9** (ask alone, one message):
> "Why would someone choose YOU over those alternatives? What's your unfair advantage?"

**Before generating the differentiation section**, propose 2-3 positioning approaches:
> "I see a few ways to position your competitive advantage:
> **(A) Product differentiation** — Your product does something no one else can do technically
> **(B) Experience differentiation** — Same capabilities, but dramatically better user experience
> **(C) Model differentiation** — Different business model, pricing, or go-to-market that changes the game
>
> Based on what you described, [X] seems strongest because [reason]. Which resonates?"

Wait for the user's choice before writing the competitive landscape section.

## BRAINSTORM PROTOCOL (BMAD CIS)

The BMAD Creative Intelligence Suite offers 8 techniques. Present 3-4 options with brief descriptions and a recommendation tailored to the product context. This helps the user make an informed choice instead of picking blindly.

**Technique Selection:**

Present options using AskUserQuestion (or as a numbered list if AskUserQuestion is unavailable). Tailor the recommendation to the product context from project-context.md.

> "Now let's explore ideas with a brainstorming technique. Based on your product context, I recommend these options:
>
> 1. **SCAMPER** (~15 min) — Apply 7 creative prompts (Substitute, Combine, Adapt, Modify, Put to use, Eliminate, Reverse) to your product idea. Best for: generating feature ideas and finding creative angles.
>
> 2. **Reverse Brainstorming** (~15 min) — 'How could we make this WORSE?' Then invert each answer into a solution. Best for: finding risks, failure modes, and defensive features.
>
> 3. **Six Thinking Hats** (~20 min) — Explore from 6 perspectives (Facts, Emotions, Pessimism, Optimism, Creativity, Process). Best for: well-rounded analysis when stakeholders disagree.
>
> 4. **5 Whys** (~10 min) — Ask 'why' 5 times to drill down to root causes. Best for: validating whether you're solving the real problem.
>
> I recommend **[technique]** because **[reason specific to their product]**. Which sounds most useful right now?"

**Execution:**

Run the selected technique interactively, one prompt at a time:
- Ask one brainstorm question, wait for the answer, then move to the next prompt
- See `references/brainstorm-techniques.md` for full catalog and step-by-step execution guides

**Synthesis:**

After completing the technique, synthesize outputs into key insights and ask: "What surprised you? What's the most valuable insight from this exercise?"

**Offer Next Technique:**

> "Want to run another technique to explore different angles, or shall we move to HMW transformation?"

Honor the user's choice. Brainstorming is valuable but optional — if the user wants to skip or move on, respect that.

## HMW TRANSFORMATION

Transform the top 3 problems (discovered in interview or brainstorm) into "How Might We" opportunity statements. Present each one individually for approval — HMW statements are strategic framing tools, so the wording matters.

**Process (one HMW at a time):**

1. Identify the top problem from the interview or brainstorm
2. Draft an HMW statement: "How might we [action] so that [outcome]?"
3. Present it to the user:
   > "Your first problem is: '[problem]'
   > Here's my HMW reframe: **'How might we [action] so that [outcome]?'**
   > Does this feel right, or would you rephrase it?"
4. Incorporate the user's feedback or approval
5. Move to the next problem

Repeat for problems 2 and 3.

**Example:**
- Problem: "Users churn because onboarding takes 30 minutes"
- HMW: "How might we reduce onboarding to <5 minutes so that users reach value faster?"

HMW statements should feel creative but grounded — they transform complaints into opportunities without prescribing solutions.

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/discovery/product-vision.md` contains:

- **Vision Statement**: Inspiring 2-3 sentence vision of the product's future state
- **Business Objectives**: BO-1, BO-2, BO-3... with measurable success criteria and timeline
- **Target Users**: Primary and secondary personas with Jobs to Be Done
- **Value Proposition**: What/For Whom/How Different
- **Competitive Landscape**: Key competitors and differentiation
- **North Star Metric**: Single primary metric defining success
- **Success Criteria**: Launch criteria + 90-day criteria
- **HMW Questions**: Transformed from top problems
- **Brainstorm Insights**: Artifacts from selected BMAD CIS techniques
- **Critical Assumptions**: Risks and unknowns that feed Planning

All Business Objective IDs (BO-#) are traceable downstream to prd.md features (PRD-F-#) and user stories (US-#).

## ID GENERATION

**BO-# Pattern**: Business Objectives. Format: `BO-1`, `BO-2`, `BO-3`. Each BO must:
- Have a clear measurable success criterion
- Specify a timeline (e.g., "within 6 months", "at launch")
- Link to downstream PRD-F-# features in prd.md
- Be unique and non-overlapping

Maintain traceability: `BO-# → PRD-F-# → US-# → acceptance criteria`

## KNOWLEDGE POINTERS

- Read `references/template.md` for the product-vision.md document template and structure.
- Read `references/guide.md` for vision interview best practices: discovering underlying motivations, validating assumptions without bias, handling conflicting stakeholder views.
- Read `references/brainstorm-techniques.md` for the complete BMAD CIS technique catalog with step-by-step execution guides.

---

**Upon completion, present the user with handoff options (see CLOSING SUMMARY) — the recommended path is the Discovery Gate validation before moving to Planning.**

## INPUT VALIDATION

**project-context.md** (BLOCKS):
- Must contain: `## WHAT`, `## WHO`, `## WHY` sections
- Minimum length: 40 lines (a real interview, not a stub)
- Must list at least 1 persona/user type

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] At least 3 BO-# (Business Objectives) defined with measurable success metrics
- [ ] Problem statement is specific (not generic platitudes)
- [ ] Target users section has at least 2 personas with goals and pain points
- [ ] Value proposition is a single clear sentence
- [ ] Competitive landscape mentions at least 2 alternatives
- [ ] BMAD brainstorm section present (even if user chose to skip techniques)
- [ ] Source Documents section present at top referencing project-context.md

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ product-vision.md saved to `docs/ets/projects/{project-slug}/discovery/product-vision.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list BO-# IDs, e.g., BO-1, BO-2, BO-3]
```

Then present these options using AskUserQuestion (or as a numbered list if AskUserQuestion is unavailable):

1. **Proceed to Discovery Gate (Recommended)** — Validate discovery artifacts before moving to Planning
2. **Run another brainstorm technique** — Explore more angles with BMAD CIS
3. **Refine this document** — Review and improve specific sections before moving on
4. **Pause for now** — Save and return later (the document is already on disk)

Wait for the user to choose before taking any action. Do not auto-proceed to the next skill.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `project-context.md` (BLOCKS)
- **Action:** Extract business context, stakeholders, constraints, tech stack. Summarize key points to the user to show you've absorbed the context.
- **Output:** Internal context object

### Step 2: Vision Interview (one question at a time)
- **Input:** Step 1 context + user responses (interactive)
- **Action:** Run the 4-block VISION INTERVIEW PROTOCOL. Ask one question per message, wait for answers, use follow-up probes as needed.
- **Output:** Raw interview notes (internal)

### Step 3: BMAD Brainstorm
- **Input:** Interview insights + user preference for techniques
- **Action:** Present 3-4 technique options with descriptions and recommendation. Run the selected technique interactively. Offer to run another when done.
- **Output:** Brainstorm insights (internal)

### Step 4: HMW Transformation
- **Input:** Top 3 problems from interview and brainstorm
- **Action:** Draft each HMW statement one at a time, present for approval, refine with user feedback.
- **Output:** 3 approved HMW statements (internal)

### Step 5: Section-by-Section Document Generation
- **Input:** Interview notes, brainstorm insights, HMW statements from Steps 2-4
- **Action:** Generate the document one major section at a time, using the template from `knowledge/template.md`. For each section:
  1. **Propose approach** — Before generating, briefly describe how you plan to frame this section
  2. **Generate the section** — Present it to the user
  3. **Ask for approval** — "Does this capture it well? Anything to adjust?"
  4. **Incorporate feedback** — If the user wants changes, revise and re-present
  5. **Move to next section** — Only after the user approves

  Section order:
  - Vision Statement (2-3 sentence inspiring vision)
  - Business Objectives (BO-# table with metrics and timelines)
  - Target Users (primary and secondary personas with Jobs to Be Done)
  - Value Proposition (What / For Whom / How Different)
  - Competitive Landscape (alternatives and differentiation)
  - North Star Metric and Success Criteria
  - HMW Questions (from Step 4)
  - Brainstorm Insights (from Step 3)
  - Critical Assumptions (risks and unknowns that feed Planning)
- **Output:** Approved sections assembled into complete product-vision.md
- **Integration:** BO-# IDs consumed by `prd` skill to generate PRD-F-#

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
  1. Verify directory exists: `docs/ets/projects/{project-slug}/discovery/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/discovery/product-vision.md` using the Write tool
  3. The document is only saved when written to the filesystem — presenting content in chat is not the same as saving.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/discovery/product-vision.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/discovery/project-context.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/discovery/product-vision.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 11: Validation
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT

### Step 12: Handoff Options
- **Action:** Present multiple next-step options (see CLOSING SUMMARY)

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (project-context.md) | Critical | Auto-invoke project-context skill — this context is needed for informed vision work | Pause until project-context is available |
| BLOCKS dep is DRAFT | Warning | Proceed with available context, noting gaps | Add `<!-- ENRICHMENT_MISSING: project-context is DRAFT -->` |
| User skips BMAD brainstorm | Low | Note "Brainstorm skipped by user" — this is a valid choice | Proceed — brainstorm enriches but is not required |
| Output validation fails (<3 BO-#) | High | Ask user for more objectives — at least 3 are needed for meaningful traceability downstream | Mark as DRAFT |
| Conflicting BO-# IDs with existing doc | Medium | Renumber to avoid collision | Append suffix |

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

Example: If "value proposition lacks specificity" is identified:
- **Solution A:** Refine existing value proposition statement with more concrete differentiators → Effort: Low, Impact: Medium, Risk: Low
- **Solution B:** Conduct user research interviews with target personas to validate differentiation → Effort: High, Impact: High, Risk: Low
- **Solution C:** Add competitive positioning matrix against top 3 alternatives → Effort: Medium, Impact: High, Risk: Medium
- **Selected:** Solution C — high impact with manageable effort, provides concrete comparison for stakeholders

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
