---
name: user-journey
description: >
  Use when mapping user journeys, analyzing touchpoints, or understanding the user
  experience end-to-end. Also triggers on 'user journey', 'journey map', 'user
  flows', 'what is the user experience', 'touchpoint analysis', or 'pain points'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Optional: Figma MCP (import existing journey maps). Upstream: docs/ets/projects/{project-slug}/discovery/product-vision.md, docs/ets/projects/{project-slug}/planning/user-stories.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Needed for personas, BO-#, and value proposition.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/planning/user-stories.md` — User flows and acceptance criteria improve journey accuracy.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `user-journey.requires: [product-vision]`
2. Check: does `product-vision.md` exist, non-empty, not DRAFT?
3. If missing → auto-invoke `product-vision` skill → wait → continue
4. Check ENRICHES → warn if missing, proceed

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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing user-journey.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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
- New product with undefined user flows
- Redesigning the core user experience
- Multiple personas with significantly different journeys

**Use short version when:**
- Adding a journey for a single new feature
- Documenting an alternative path for an existing journey
- Even in short version, still include: JOUR-# with steps table, PRD-F-# links, and edge cases

### Skill-Specific Interaction

- **Journey selection:** After loading context, propose 2-3 key journeys based on user stories and personas. Ask which journey to map first before proceeding.
- **Per-step mapping:** Present each touchpoint with its emotion and pain point. Ask "Does this step capture the experience? Anything to adjust?" before moving to the next step.
- **Alternative paths:** After mapping the primary journeys, suggest 2-3 edge case journeys (error recovery, power user shortcuts, first-time experience). Ask which matter for this product.
- **Handoff options:**
  1. Proceed to UX Sitemap (Recommended) — translate journey touchpoints into page hierarchy
  2. Map another journey — add coverage for additional personas or features
  3. Refine this journey — adjust steps, emotions, or edge cases
  4. Pause — save current progress and return later

# User Journey Map Generation

## PURPOSE

Generate a comprehensive **user-journey.md** that documents how each persona interacts with the product across all lifecycle stages: Awareness → Consideration → Adoption → Goal Completion → Advocacy. This document provides emotional intelligence, identifies friction points, and surfaces opportunities for improvement.

The journey map is the first UX document in the design phase, feeding directly into the ux-sitemap. It ensures that all subsequent UX decisions (information architecture, wireframes, interaction design) are grounded in real user needs and emotional contexts.

## CONTEXT LOADING (4-level fallback)

1. **$ARGUMENTS**: If `[upstream-path]` provided, load that document
2. **Handoff**: Check for `docs/ets/projects/{project-slug}/planning/user-stories.md` (personas, pain points)
3. **Scan**: If not found, check `docs/ets/projects/{project-slug}/discovery/product-vision.md` (vision, users)
4. **Ask**: If no context available, ask user for personas and high-level goals

Load the following sections from upstream:
- Personas (name, role, goals, constraints)
- Identified pain points from user stories
- Desired outcomes or success metrics
- Any existing journey stage definitions

## PROCESS

1. **Persona Extraction**: Identify all unique personas from vision or stories
2. **Stage Mapping**: Define journey stages aligned with product lifecycle
   - Awareness (how users discover)
   - Consideration (evaluation phase)
   - Adoption (first interaction with product)
   - Goal Completion (core use case)
   - Advocacy (retention, referral)
3. **Touchpoint Documentation**: For each stage, document:
   - Key interaction points (UI, messaging, support)
   - Channel used (web, mobile, email, support, community)
   - Expected actions and success signals
4. **Emotional Arc**: Map emotional state across journey
   - High point (moments of delight)
   - Low point (frustration or confusion)
   - Emotional transitions between stages
5. **Pain Points & Opportunities**: At each touchpoint, identify:
   - Current friction (why users struggle)
   - Root cause analysis
   - Opportunity statement ("How might we...")
6. **Success Metrics**: Define how success is measured at each stage

## OUTPUT FORMAT

Document structure:
- **Executive Summary**: Key insights, critical pain points
- **Persona Journey Maps**: One section per primary persona
  - Diagram (Mermaid or ASCII) showing emotional arc and stages
  - Touchpoint table (stage, action, emotion, pain point, opportunity)
  - Voice of the customer quotes where relevant
- **Cross-Persona Insights**: Common patterns, divergences
- **Opportunities Backlog**: Ranked list of HMW statements for design phase
- **Metrics**: How journey success is measured

## PIPELINE CONTEXT

- **Input**: product-vision.md, user-stories.md
- **Output**: user-journey.md
- **Feeds**: ux-sitemap.md (defines screens per journey stage)
- **Referenced by**: wireframes.md, style-guide.md

This is the first UX document generated in the design phase. All subsequent UX work validates and operationalizes this journey.

## JOURNEY ID SYSTEM (JOUR-#)

Every journey in this document receives a unique ID: `JOUR-01`, `JOUR-02`, etc. This enables traceability between journeys and features.

### Per-Journey Structure

Each JOUR-# entry should contain all of the following fields (this ensures downstream skills have the context they need):

```
### JOUR-[NN]: [Journey Name]

**Category:** [Onboarding | Core Task | Recovery | Admin | Edge Case]
**Persona:** [Persona name from product-vision.md]
**Preconditions:** [State that must be true BEFORE the journey starts]
**Postconditions:** [State expected AFTER completing the journey]

#### Steps

| # | Intent | User Interaction | Features (PRD-F-#) | Expected Response | Emotion |
|---|--------|-----------------|---------------------|-------------------|---------|
| 1 | [goal of this step] | [how user interacts with UI] | [PRD-F-1, PRD-F-3] | [what system does] | [positive/neutral/negative] |
| 2 | ... | ... | ... | ... | ... |

#### Edge Cases
- **[Scenario]:** [What could go wrong] → **Recovery:** [How user/system recovers]
- **[Scenario]:** ... → **Recovery:** ...

#### Success Metrics
- [Metric]: [Target] (e.g., "Task completion: <2 minutes")
```

### Why JOUR-# Matters

1. **Traceability:** JOUR-# steps link to PRD-F-# via `Features` column, creating bidirectional traceability (feature → journey, journey → feature)
2. **Coverage check:** Every Must Have PRD-F-# should appear in at least 1 JOUR-# step. Missing features = gap in journey coverage.
3. **Edge case enforcement:** Each JOUR-# requires edge cases, ensuring the team thinks about failure modes early.
4. **Downstream consumption:** `ux-sitemap` uses JOUR-# steps to identify required screens. `wireframes` uses JOUR-# for interaction flows. `quality-checklist` uses JOUR-# edge cases as test scenarios.

### Self-Check Questions (from Neo v0 FJMD)

Before finalizing, ask yourself:
- Am I covering 100% of user-facing features from ALL personas' perspectives?
- Am I covering ALL journey cases, including small details other product managers might omit?
- Are edge cases comprehensive enough that development can proceed without alteration?
- Does every Must Have PRD-F-# appear in at least one JOUR-# step?

## SINGLE SOURCE OF TRUTH (SST)

**User journey maps (JOUR-#), persona journey contexts, touchpoint inventory, and journey edge cases are ONLY defined here.** Do not duplicate in wireframes.md or style-guide.md. Emotional states, pain points, and journey preconditions/postconditions remain the authoritative reference for all UX work.

JOUR-# is the SST for:
- Journey-to-feature mapping (JOUR-# steps → PRD-F-#)
- Edge cases per journey (consumed by quality-checklist for test scenarios)
- Emotional arc per persona (consumed by style-guide for tone/messaging)

## KNOWLEDGE POINTER

Refer to `docs/ets/projects/{project-slug}/ux/template-user-journey.md` for:
- Journey stage definitions (standard template)
- Emotional arc notation
- Touchpoint table structure
- Pain point taxonomy
- Example HMW transformations

---

**Execution instruction**: Load context, extract personas, map journey stages with touchpoints, document emotions and pain points, generate opportunities, and output user-journey.md to docs/ets/projects/{project-slug}/ux/.

## INPUT VALIDATION

**product-vision.md** (BLOCKS):
- Must contain at least 2 personas with goals and pain points
- Must contain at least 1 BO-#

**user-stories.md** (ENRICHES):
- Should contain US-# with Given/When/Then for flow detail

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] At least 2 persona journeys mapped with JOUR-# IDs
- [ ] Each JOUR-# has: preconditions, steps table, postconditions, edge cases
- [ ] Each step links to at least 1 PRD-F-# in Features column
- [ ] Every Must Have PRD-F-# appears in at least 1 JOUR-# step (coverage)
- [ ] Touchpoints include emotional state (positive/neutral/negative)
- [ ] Edge cases documented for each JOUR-# (minimum 2 per journey)
- [ ] Pain points identified with HMW opportunity statements
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ user-journey.md saved to `docs/ets/projects/{project-slug}/ux/user-journey.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list JOUR-# IDs, e.g., JOUR-01, JOUR-02, JOUR-03]

→ Next step: ux-sitemap — Define hierarchical page/screen structure from journey touchpoints
  Run: /design or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `product-vision.md` (BLOCKS), `user-stories.md` (ENRICHES)
- **Action:** Extract personas, goals, pain points, user flows
- **Output:** Persona context bundle
- **Why this matters:** Grounding journeys in real personas and stories ensures the maps reflect actual user needs, not assumptions.

### Step 2: Journey Selection (Interactive)
- **Input:** Persona context + PRD-F-# list from prd.md
- **Action:** Propose 2-3 key journeys based on personas and user stories. Present each with a one-line summary and ask the user which to map first.
- **Output:** Ordered journey priority list
- **Why this matters:** Not all journeys are equally important. Focusing on the highest-impact journey first ensures the most critical user experience is mapped with the most attention.

### Step 3: Journey Mapping with JOUR-# IDs (Section-by-Section)
- **Input:** Selected journey + PRD-F-# features
- **Action:** For each journey:
  1. Present preconditions and postconditions — ask for approval
  2. Present the step table (touchpoints, emotions, features) one section at a time — ask "Does this step capture the experience? Anything to adjust?" before proceeding
  3. Present edge cases — ask which scenarios matter
  4. Coverage check: verify every Must Have PRD-F-# appears in at least 1 JOUR-# step
- **Output:** Numbered JOUR-# journeys with feature traceability, approved section by section

### Step 4: Pain Points & Opportunities
- **Input:** Approved journey maps
- **Action:** Identify friction points, drop-off risks, improvement opportunities. Present the annotated journeys with HMW opportunity statements and ask "Do these pain points and opportunities ring true?"
- **Output:** Annotated journeys with opportunity markers
- **Integration:** Consumed by `ux-sitemap` (BLOCKS) and `wireframes` (indirect)

### Step 5: Alternative Paths (Interactive)
- **Input:** Completed primary journeys
- **Action:** Suggest 2-3 edge case journeys (error recovery, power user shortcuts, first-time experience). Ask which matter for this product.
- **Output:** Additional JOUR-# entries for selected edge cases

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
  1. Verify directory exists: `docs/ets/projects/{project-slug}/ux/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/ux/user-journey.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/ux/user-journey.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/discovery/product-vision.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/ux/user-journey.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 11: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT
- **Handoff:** Present next step options:
  1. Proceed to UX Sitemap (Recommended)
  2. Map another journey
  3. Refine this journey
  4. Pause

## FEATURE JOURNEY MAP MODE

When invoked with a specific feature argument (e.g., `/user-journey checkout` or "map the checkout feature journey"), switch to **feature-centric mode** instead of persona-centric:

### Distinction
- **Persona journey** (default) = one persona's path through the entire product
- **Feature journey** = one feature experienced across ALL relevant personas

### Feature Journey Template

```markdown
## JOUR-[NN]: Feature Journey — [Feature Name] (PRD-F-[NN])

**Category:** Feature Deep-Dive
**Personas Involved:**
- [Persona A] — Goal: X, Pain point: Y
- [Persona B] — Goal: Z, Pain point: W
**Preconditions:** [State required before feature is accessible]
**Postconditions:** [State after successful feature completion]

### Primary Flow
| # | Intent | User Interaction | Features (PRD-F-#) | Expected Response | Persona | Emotion |
|---|--------|-----------------|---------------------|-------------------|---------|---------|
| 1 | [goal] | [how user interacts] | PRD-F-[NN] | [system response] | [who] | [state] |

### Error Flows
| Error Scenario | User Sees | Recovery Path | Fallback | Severity |
|---------------|-----------|---------------|----------|----------|

### Edge Cases
- **[Scenario]:** [description] → **Recovery:** [path]

### Experience Validation
- [ ] All personas can complete primary flow
- [ ] Error flows have recovery paths
- [ ] Every step links to PRD-F-#
- [ ] Emotional arc trends toward satisfaction
- [ ] Accessibility touchpoints verified
```

### When to use Feature Journey Mode
- When a feature has >2 personas interacting with it
- When a feature has complex state transitions
- When a feature spans multiple touchpoints (web, mobile, email)

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (product-vision.md) | Critical | Auto-invoke product-vision skill | Block execution |
| No personas found in product-vision | High | Ask user to define at least 2 personas | Proceed with generic "User A/B" |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
| Feature journey requested but no feature specified | Low | Ask user which feature | Default to persona mode |
