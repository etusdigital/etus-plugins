---
name: spike
description: >
  Use when conducting research, evaluating feasibility, or exploring options before
  committing to a direction. Also triggers on 'spike', 'research', 'investigate',
  'feasibility', 'POC', 'proof of concept', 'brainstorm', 'explore options', or
  'compare alternatives'.
model: opus
version: 1.0.0
argument-hint: "[research question or topic]"
compatibility: "Optional: WebSearch (for market/technology research), external issue tracker adapter (for example, Linear) to link the spike"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (required — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — Spikes now start from an
  explicit question-framing package so the research is grounded in actors,
  hypotheses, use cases, and open questions.

**ENRICHES** (improves output — use if available):
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` — Helps verify that the question
  was framed with enough coverage before research begins.
- Any existing project documents that provide context for the research question.
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Business context may inform which options are viable.
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Vision alignment helps evaluate options against strategic goals.

**Resolution protocol:**
1. Check ENRICHES: do any project docs exist?
2. If yes → load silently for context. This helps frame the research within the product context.
3. If no → proceed without them. Spikes often happen before any docs exist.

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- Research question affects a major architecture or technology decision
- Multiple viable options need formal comparison with tradeoffs
- Spike results will be referenced by future ADRs or NFRs

**Use short version when:**
- Quick feasibility check for a single technology or approach
- Time-boxed exploration (< 1 day)
- Even in short version, still include: research question, options evaluated, recommendation, and evidence

## ARTIFACT SAVE RULE

**Why this matters:** Research findings are valuable beyond the immediate decision. A documented spike saves future teams from repeating the same investigation and captures the reasoning behind strategic choices.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to `docs/ets/projects/{project-slug}/spikes/spike-{slug}.md`
3. Displaying content in chat is not the same as saving — the file needs to exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only then propose the next step

**If the Write fails:** Report the error to the user and do not proceed.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Research questions benefit from deliberate exploration. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a research methodology, brainstorm technique, or direction to explore, present 3-4 concrete options with descriptions. Highlight your recommendation.

3. **Propose approaches before generating** — Before starting research, propose 2-3 research methodologies with tradeoffs. For example: "desk research" vs. "prototyping" vs. "expert interview" vs. "competitive analysis."

4. **Present output section-by-section** — Present findings, options, and recommendation individually. Ask "Does this capture the key finding?" and only proceed after approval.

5. **Track outstanding questions** — If research reveals new questions:
   - **Critical for decision** — Must be answered before recommending.
   - **Future investigation** — Noted for follow-up spikes or research.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options (see CLOSING SUMMARY).

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing spike document at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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

## PURPOSE

Document a research investigation, feasibility study, or brainstorm. Spikes
still answer the question "Should we?" before committing to "How do we?", but
they now start from a question-framing ideation package rather than ad-hoc
conversation alone.

Spikes are the entry point for Spike/Research mode. They can feed into any other mode:
- Spike concludes "build a feature" → Feature mode
- Spike concludes "build a product" → Product mode
- Spike concludes "not worth pursuing" → Decision documented, move on

## CONTEXT LOADING

Load context in this order of priority:

1. **Opportunity Pack**: Read `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
   first.
2. **Coverage Matrix**: Read `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` if
   it exists.
3. **$ARGUMENTS**: If the user passes `[research question]`, use it as
   additional context.
4. **ENRICHES scan**: Check for existing project docs to provide context for the
   research.
5. **External issue tracker adapter**: If available, check if there's an existing spike issue with
   context.
6. **User Interview**: Begin the research scoping interview interactively.

## INTERVIEW PROTOCOL

This interview is 4 core questions, asked one at a time. The goal is to scope the research before diving in.

### Question 1: The Question

> "What question are you trying to answer? Be as specific as possible."

**Follow-up probes** (ask one at a time only if needed):
- If too broad: "Can you narrow this to a specific decision you need to make?"
- If multiple questions: "Which question is most important to answer first? Let's focus there."

### Question 2: The Context

> "What's the context? Why does this matter now — what triggered this investigation?"

**Follow-up probes:**
- If no trigger: "Is this exploratory curiosity, or is there a decision that's blocked waiting for this answer?"
- If deadline pressure: "When do you need this answer by? That helps me scope the research depth."

### Question 3: Success Criteria

> "What would a good answer look like? What level of confidence do you need — a quick directional signal, or a thorough analysis?"

Present research depth options:
> "I see three levels of research depth:
> 1. **Quick scan** (~30 min) — High-level comparison, enough for a directional decision
> 2. **Thorough analysis** (~2 hours) — Detailed comparison with evidence, sufficient for a confident recommendation
> 3. **Deep investigation** (~4+ hours) — Exhaustive research with prototyping or experimentation
>
> Based on your timeline, I'd suggest [level]. Which fits your needs?"

### Question 4: Constraints

> "Are there any constraints — budget, technology, team skills, timeline — that would rule out certain options upfront?"

**Follow-up probes:**
- If no constraints: "Is there anything you've already tried or ruled out?"

## BRAINSTORM PROTOCOL (BMAD CIS)

When the research question benefits from creative exploration, offer BMAD CIS techniques. This is the same brainstorm toolkit available in the `product-vision` skill.

**Technique Selection:**

Present options tailored to the research context:

> "This research question could benefit from a structured brainstorming technique. Here are some options:
>
> 1. **SCAMPER** (~15 min) — Apply 7 creative prompts (Substitute, Combine, Adapt, Modify, Put to use, Eliminate, Reverse) to explore alternatives. Best for: finding creative solutions to a known problem.
>
> 2. **Reverse Brainstorming** (~15 min) — 'How could we make this WORSE?' Then invert each answer. Best for: identifying risks and failure modes in proposed solutions.
>
> 3. **Six Thinking Hats** (~20 min) — Explore from 6 perspectives (Facts, Emotions, Pessimism, Optimism, Creativity, Process). Best for: evaluating options when stakeholders have different concerns.
>
> 4. **5 Whys** (~10 min) — Ask 'why' 5 times to drill down to root causes. Best for: validating whether you're researching the right question.
>
> I recommend **[technique]** because **[reason specific to their question]**. Want to try one, or jump straight to evaluating options?"

**Execution:**

Run the selected technique interactively, one prompt at a time. See `.claude/skills/discovery/product-vision/knowledge/brainstorm-techniques.md` for full catalog and step-by-step execution guides.

**Synthesis:**

After completing the technique, synthesize outputs into key insights and ask: "What surprised you? What's the most valuable insight?"

Honor the user's choice — brainstorming enriches the spike but is not required.

## RESEARCH METHODOLOGY

After scoping, propose 2-3 research methodologies:

> "For this question, I'd recommend these research approaches:
>
> **A. Desk research** — Analyze existing documentation, competitor products, industry benchmarks
> **B. Prototyping/POC** — Build a minimal proof of concept to test feasibility
> **C. Expert consultation** — Leverage domain expertise (yours, team's, or external)
>
> I recommend [A/B/C] because [reason]. Which approach do you want to take?"

## OPTION EVALUATION

For each option discovered during research, document:

1. **Description** — What is this option?
2. **Pros** — Advantages and benefits
3. **Cons** — Disadvantages and risks
4. **Effort** — T-shirt size (XS/S/M/L/XL)
5. **Risk** — Low/Medium/High
6. **Fit** — How well does this align with constraints and goals?

Present options in a structured comparison, then propose a recommendation with rationale.

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/spikes/spike-{slug}.md` follows the template in `knowledge/template.md`.

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the spike document template and standard structure.
- Read `.claude/skills/discovery/product-vision/knowledge/brainstorm-techniques.md` for the complete BMAD CIS technique catalog (shared with product-vision skill).

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Research question is clearly stated and specific
- [ ] Context explains why this matters now
- [ ] At least 2 options evaluated with pros/cons
- [ ] Each option has effort and risk assessment
- [ ] Recommendation is present with rationale (or explicit "no recommendation yet" with what's needed to decide)
- [ ] Decision section documents whether a decision was made

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display the summary and offer multiple next steps:

```text
spike-{slug}.md saved to `docs/ets/projects/{project-slug}/spikes/spike-{slug}.md`

Status: [COMPLETE | DRAFT]
Research question: [the question]
Recommendation: [recommended option or "needs more research"]
Decision: [Made / Pending]

What would you like to do next?

1. Create a Feature Brief — Turn this recommendation into a feature spec
2. Start a Product — This is big enough for full Product mode with /orchestrator
3. Share findings — Review the spike with stakeholders
4. Run another spike — Investigate a follow-up question
5. Pause for now — Save and return later
```

Wait for the user's choice before proceeding. Do not auto-advance.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `$ARGUMENTS` or user description + ENRICHES documents (if available)
- **Action:** Check for existing project docs. Load silently if found.
- **Output:** Internal context (existing docs loaded or none)

### Step 2: Research Scoping Interview (one question at a time)
- **Input:** Step 1 context + user responses (interactive)
- **Action:** Run the 4-question INTERVIEW PROTOCOL. Ask one question per message, wait for answers.
- **Output:** Scoped research question with depth and constraints

### Step 3: Methodology Selection
- **Input:** Scoped question + constraints
- **Action:** Propose 2-3 research methodologies. Ask the user which approach to take.
- **Output:** Chosen methodology

### Step 4: Brainstorm (Optional)
- **Input:** Research question + user preference
- **Action:** If the user wants brainstorming, present BMAD CIS technique options. Run the selected technique interactively. If the user wants to skip, proceed to findings.
- **Output:** Brainstorm insights (if run) or skip

### Step 5: Research & Findings
- **Input:** Methodology + brainstorm insights (if any)
- **Action:** Conduct research (desk research, analysis, prototyping guidance). Present each key finding one at a time for discussion.
- **Checkpoint per finding:** "Here's what I found about [topic]. Does this match your understanding?"

### Step 6: Option Evaluation
- **Input:** All findings
- **Action:** Structure findings into options with pros/cons/effort/risk. Present options for comparison.
- **Checkpoint:** "Here are the [N] options. Does this capture all the viable paths?"

### Step 7: Recommendation & Decision
- **Input:** Evaluated options + user discussion
- **Action:** Propose a recommendation with rationale. Ask if a decision can be made now or if more research is needed.
- **Checkpoint:** "Based on the research, I recommend [option] because [reason]. Ready to make a decision, or need more information?"

### Step 8: Section-by-Section Document Generation
- **Input:** All research data, findings, evaluation, decision
- **Action:** Generate the spike document section by section, presenting each for approval:
  1. **Research Question** — Confirm framing
  2. **Context** — Present, ask if complete
  3. **Methodology** — Present what was done
  4. **Findings** — Present key findings
  5. **Options Evaluated** — Present comparison
  6. **Recommendation** — Present with rationale
  7. **Decision** — Document outcome
  8. **Brainstorm Insights** — If BMAD CIS was used
- **Checkpoint per section:** "Does this section look right?"

### Step 9: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is lightweight work and the document has unnecessary sections → trim empty or boilerplate sections
  - If this is complex work and sections are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 10: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline still have to invent if this document is all they get?
  2. Do any sections depend on content claimed to be out of scope?
  3. Are there implicit decisions that should be explicit?
  4. Is there a low-effort addition that would make this significantly more useful for the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 11: Save Artifact
- **Action:**
  1. Generate slug from research question (lowercase, hyphens, no special chars)
  2. Verify directory exists: `docs/ets/projects/{project-slug}/spikes/` — create if missing
  3. Write the complete document to `docs/ets/projects/{project-slug}/spikes/spike-{slug}.md` using the Write tool
- **Output:** File written to disk at the specified path

### Step 12: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/spikes/spike-{slug}.md`) + paths to upstream documents (none — spikes have no BLOCKS dependencies)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 13: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/spikes/spike-{slug}.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 14: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist. Display CLOSING SUMMARY.
- **Handoff:** Present the next-step options. Let the user choose.
- **Output:** Document marked COMPLETE or DRAFT

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| Research question too broad | Medium | Ask user to narrow down — "What specific decision are you trying to make?" | Proceed with broader question, note limitation |
| No viable options found | Medium | Document why all options were rejected, suggest new research direction | Mark as DRAFT with "inconclusive" status |
| User can't decide between options | Low | Suggest criteria-based scoring or time-boxed decision | Document as "decision pending" with what's needed |
| BMAD technique doesn't yield insights | Low | Note "technique completed, no breakthrough insights" and move on | Proceed to option evaluation |
| Output validation fails | High | Mark as DRAFT, flag gaps | Proceed with DRAFT status |

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
