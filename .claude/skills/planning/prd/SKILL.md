---
name: prd
description: >
  Use when creating a PRD, defining features, prioritizing requirements, or scoping
  an MVP. Also triggers on 'product requirements', 'feature list', 'what should we
  build first', 'MoSCoW', 'prioritize features', or 'define the product scope'.
model: opus
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Optional: external issue tracker adapter (for example, Linear) for roadmap context, Slack MCP (pull feature discussions)"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (required — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Provides the BO-# business objectives that get transformed into features. Without these, there is nothing to prioritize.
- `docs/ets/projects/{project-slug}/planning/prioritization.md` — Opportunity ranking determines which problems deserve delivery scope.
- `docs/ets/projects/{project-slug}/planning/solution-discovery.md` — Delivery requirements should only be written after the chosen solution direction is explicit.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Tech stack and constraints help assess feature feasibility more accurately.
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — Provides the full
  problem-space coverage that should be converted into structured requirements.
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` — Helps verify that actors,
  JTBDs, journeys, use cases, edge cases, and assumptions are represented in
  the PRD scope.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `prd.requires: [product-vision]`
2. Check: does `product-vision.md` exist, non-empty, not DRAFT?
3. If missing → auto-invoke `product-vision` skill → wait → continue
4. Check ENRICHES: `project-context.md` → warn if missing, proceed regardless

## ARTIFACT SAVE RULE

**Why this matters:** The PRD is the single source of truth for scope and priorities. If it only exists in chat, downstream skills (user-stories, feature-spec, architecture) cannot read it, and traceability breaks.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is not the same as saving — the file needs to exist on the filesystem for downstream skills to consume it
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only then propose the next step

**If the Write fails:** Report the error to the user and do not proceed to the next skill — downstream documents depend on this file existing.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Use the AskUserQuestion tool when available for structured choices. Batching multiple questions overwhelms the user and leads to shallow answers.

2. **3-4 suggestions for choices** — When the user needs to choose a direction, present 3-4 concrete options with a brief description of each. Highlight your recommendation. Let the user pick before proceeding.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs and a recommendation. For example, before the feature list: propose "minimal MVP" vs "balanced" vs "ambitious" scope approaches.

4. **Present output section-by-section** — Do not generate the full PRD at once. Present each major section (executive summary, feature list, scope boundaries, success criteria, etc.), ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something cannot be answered now, classify it:
   - **Resolve before next phase** — This blocks the handoff to user-stories.
   - **Deferred to [phase name]** — Noted and carried forward in the handoff JSON.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options (see CLOSING SUMMARY).

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing prd.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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

Transform product vision into prioritized, traceable requirements. This skill
bridges Discovery (what we're building) and Design (how we'll build it) by
identifying all features, prioritizing them through MoSCoW, and establishing
scope boundaries. It now assumes ideation has already mapped the covered
problem space, so the PRD should convert that coverage into requirements rather
than discover it from scratch.

## CONTEXT LOADING

Load context in this order of priority:

1. **Solution Discovery**: Read `docs/ets/projects/{project-slug}/planning/solution-discovery.md` first.
2. **$ARGUMENTS**: If the user passes `[upstream-path]`, read that file directly (typically product-vision.md).
3. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for any upstream planning artifacts or feature lists.
4. **Document Scan**: Scan `docs/ets/projects/{project-slug}/discovery/` for existing product-vision.md to extract BO-#.
5. **User Interview**: If nothing found, begin the PRD creation interviews interactively.

## HMW PROCESS

Transform each Business Objective (BO-#) into features using How Might We — one BO at a time, one feature at a time:

1. **Present one BO-#**: Show the business objective and ask "How might we achieve [BO description]?" Wait for the user's response before continuing.
2. **Brainstorm features one at a time**: For each idea the user proposes, explore it:
   - "What value does this deliver toward BO-#?"
   - "Is this a single feature or should we split it?"
   - Only after the user confirms this feature, ask: "Any other feature for this BO-#?"
3. **Confirm coverage per BO**: After the user says "that's all for this one," summarize the features for that BO-# and ask: "Does this cover BO-#, or is something missing?"
4. **Move to next BO-#**: Only proceed to the next business objective after the current one is confirmed.
5. **Consolidate**: After all BO-# are covered, present the full feature list and ask about duplicates or clusters.

Result: A comprehensive feature list (typically 10-25 features for MVP scope), built collaboratively one feature at a time.

## MOSCOW PRIORITIZATION

Classify each feature into one of four buckets — presenting each feature individually for prioritization:

- **Must Have**: Required for MVP launch. No MVP without it. Business-critical or user expectation.
- **Should Have**: Important for success but not blocking MVP. High value, moderate complexity.
- **Could Have**: Nice-to-have, differentiator. Lower priority, can be deferred post-launch.
- **Won't Have**: Out of scope for this release cycle. Explicitly documented for future.

**Prioritization flow — one feature at a time:**

1. Present the feature with its name, description, and which BO-# it serves.
2. Offer the 4 MoSCoW options with your recommendation and a brief rationale:
   - "I'd suggest **Must Have** because [reason]. What do you think? Must / Should / Could / Won't?"
3. Wait for the user's choice before moving to the next feature.
4. After all features are prioritized, present the distribution summary (e.g., "5 Must, 4 Should, 3 Could, 2 Won't") and check if the balance feels right.

**Healthy distribution guideline** (share with user if distribution is skewed):
- Must Have: ~25-35% — if higher, ask "Is everything here truly a launch blocker?"
- Should Have: ~40-50%
- Could Have: ~15-25%
- Won't Have: ~5-10%

## ID GENERATION

**PRD-F-# Pattern**: Product Requirements Features. Format: `PRD-F-1`, `PRD-F-2`, etc. Each PRD-F-# must:
- Reference which BO-# it serves (traceability back to vision)
- Have a clear name and description
- Include success criteria or acceptance thresholds
- Link to downstream US-# when user stories are created
- Be unique and non-overlapping in scope

Maintain traceability: `BO-# → PRD-F-# → US-# → acceptance criteria (Given/When/Then)`

## SST RULE

**Feature definitions and MoSCoW priorities live only in prd.md.**

Why: if priorities are scattered across documents, teams get conflicting instructions and scope creep goes undetected. By keeping scope decisions here, any change is visible in one place. Downstream documents (user-stories.md, feature-spec-*.md, api-spec.md, implementation-plan.md) reference PRD-F-# but rely on this document for priority and scope definitions.

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/planning/prd.md` contains:

- **Executive Summary**: Bridge from vision → features (1 paragraph, references BO-#)
- **Scope Statement**: What's in/out with justification
- **Feature List**: Each PRD-F-# with:
  - Feature name and one-liner
  - Problem/value statement
  - Which BO-# it serves
  - MoSCoW priority (Must/Should/Could/Won't)
  - Success criteria (metric or threshold)
- **Scope Boundaries**: Explicit out-of-scope items (prevents creep)
- **Dependencies & Assumptions**: Inter-feature dependencies, team/resource assumptions
- **Release Criteria**: When is this PRD "done"? (all Must Have features designed? all Should Have estimated?)

## KNOWLEDGE POINTERS

- Read `references/template.md` for the prd.md document template and standard structure.
- Read `references/guide.md` for feature brainstorming and prioritization best practices.

---

**Upon completion, present handoff options to the user (see CLOSING SUMMARY). Validate PRD-F-# to BO-# traceability before proceeding.**

## INPUT VALIDATION

**product-vision.md** (BLOCKS):
- Needs at least 1 `BO-#` identifier — without business objectives there is nothing to decompose into features
- Needs sections: `## Business Objectives`, `## Target Users` — these drive the HMW brainstorm
- Minimum length: 50 lines — shorter documents likely lack the detail needed for feature generation

**project-context.md** (ENRICHES):
- Should contain: `## WHAT`, `## WHY` — provides constraints that improve feature feasibility assessment

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] At least 5 PRD-F-# features defined
- [ ] Each PRD-F-# references a BO-# (traceability)
- [ ] MoSCoW priority assigned to every feature (Must/Should/Could/Won't)
- [ ] MVP boundary explicitly defined (which features are Must Have)
- [ ] At least 1 Must Have and 1 Won't Have feature (scope is bounded)
- [ ] Success criteria defined for each Must Have feature
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display the summary and offer multiple next steps:

```text
prd.md saved to `docs/ets/projects/{project-slug}/planning/prd.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list PRD-F-# IDs, e.g., PRD-F-1, PRD-F-2, PRD-F-3]

What would you like to do next?

1. Proceed to User Stories (Recommended) — Start decomposing features into testable stories (US-#)
2. Refine this PRD — Review and improve specific sections
3. Run Discovery Gate first — Validate discovery artifacts before continuing
4. Pause for now — Save and return later
```

Wait for the user's choice before proceeding. Do not auto-advance to the next skill.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `product-vision.md` (BLOCKS), `project-context.md` (ENRICHES)
- **Action:** Extract BO-# objectives, personas, constraints
- **Output:** Internal context with BO-# list
- **Checkpoint:** Summarize what was loaded and ask the user to confirm: "I found [N] business objectives. Is this the right starting point?"

### Step 2: Scope Approach Proposal
- **Input:** BO-# list from Step 1
- **Action:** Before brainstorming features, propose 2-3 scope approaches with tradeoffs:
  - **Minimal MVP** — Focus on the 2-3 most critical BO-#s. Faster to market, but may miss differentiators.
  - **Balanced** — Cover all BO-#s with Must Have + key Should Have features. Recommended default.
  - **Ambitious** — Full coverage including Could Have features for competitive edge. Longer timeline.
- **Checkpoint:** Ask the user which approach resonates before generating any features.

### Step 3: HMW Feature Generation (one BO at a time)
- **Input:** BO-# list + chosen scope approach
- **Action:** For each BO-#, one at a time:
  1. Present the BO-# and ask "How might we achieve [objective]?"
  2. Explore features one by one with the user
  3. Confirm coverage for this BO-# before moving to the next
- **Output:** Raw feature list built collaboratively
- **Checkpoint per BO:** "Here are the [N] features for BO-#. Does this cover it?"

### Step 4: MoSCoW Prioritization (one feature at a time)
- **Input:** Feature list from Step 3
- **Action:** Present each feature individually with 4 options (Must/Should/Could/Won't) plus your recommendation and rationale. Wait for the user's choice before presenting the next feature.
- **Output:** Prioritized feature table with PRD-F-# IDs
- **Checkpoint:** After all features are prioritized, present the distribution summary and ask if the balance feels right.
- **Integration:** PRD-F-# IDs consumed by `user-stories` skill

### Step 5: Section-by-Section Generation & Approval
- **Input:** All interview data collected so far
- **Action:** Generate the PRD section by section, presenting each for approval:
  1. **Executive Summary** — Present, ask "Does this capture it well?"
  2. **Feature List** (grouped by priority) — Present, ask for adjustments
  3. **Scope Boundaries** (in-scope / out-of-scope) — Present, confirm
  4. **Success Criteria** (per Must Have feature) — Present each, refine
  5. **Dependencies & Assumptions** — Present, ask what's missing
  6. **Release Criteria** — Present, confirm
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
  1. Verify directory exists: `docs/ets/projects/{project-slug}/planning/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/planning/prd.md` using the Write tool
  3. The document needs to exist on the filesystem for downstream skills to consume it — presenting content in chat is not sufficient.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/planning/prd.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/discovery/product-vision.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/planning/prd.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
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
| BLOCKS dep missing (product-vision.md) | Critical | Auto-invoke product-vision skill | Block execution |
| product-vision.md has no BO-# | Critical | Re-invoke product-vision with feedback | Block — PRD cannot trace without BO-# |
| User can't prioritize features | Medium | Suggest default: all Could Have except first 3 Must | Proceed with tentative priorities |
| Output validation fails | High | Mark as DRAFT, flag gaps | Proceed with DRAFT status |
| Conflicting PRD-F-# IDs | Medium | Renumber starting from max+1 | Append suffix |

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

Example: If "MVP boundary not clearly defined" is identified:
- **Solution A:** Add explicit "What's in MVP" vs "What's post-launch" table → Effort: Low, Impact: Medium, Risk: Low
- **Solution B:** Conduct scope negotiation interview with stakeholders to prioritize across all features → Effort: High, Impact: High, Risk: Medium
- **Solution C:** Use effort-based cut-off (must-haves must be completable in N weeks) → Effort: Medium, Impact: High, Risk: Low
- **Selected:** Solution C — high impact with manageable effort, provides objective prioritization criteria

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
