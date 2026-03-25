---
name: retro-project
description: >
  Use when finishing a project, reflecting after a sprint, or capturing lessons
  learned. Also triggers on 'retro', 'retrospective', 'lessons learned', 'what
  did we learn', 'post-mortem', or 'what worked and what did not'.
model: opus
version: 1.0.0
argument-hint: "[project-slug]"
---

# Project Retrospective Skill

## PURPOSE

This skill captures organizational knowledge that would otherwise be lost between projects. By conducting a structured retrospective interview, it produces a lessons-learned document that future discovery phases can reference. The goal is to compound knowledge: each project makes the next one better by surfacing patterns, anti-patterns, and decision outcomes.

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- End of a multi-sprint project or major release
- Significant lessons learned that should compound into future projects
- Team wants to formally review decision outcomes (ADRs, technology choices)

**Use short version when:**
- End of a single sprint or minor feature delivery
- Quick team reflection (30 minutes or less)
- Even in short version, still include: what worked, what did not work, and 2-3 actionable improvements

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- None. Retrospectives can run at any time — after a project, after a sprint, or after a feature.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Provides project name and scope for context
- `docs/ets/projects/{project-slug}/planning/prd.md` — Provides feature list for decision-outcome mapping
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — Provides ADRs for architectural decision review

If upstream documents exist, read them to pre-populate context and ask more targeted questions. If they don't exist, the interview still works — it just relies more on user memory.

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information. The retrospective interview is intentionally reflective — give the user space to think. These are not rapid-fire questions.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Retrospectives benefit from slow, thoughtful responses.

2. **3-4 suggestions for choices** — When asking about patterns or categories, present concrete examples to help the user think. Example: "What kind of pattern was this? (A) Process pattern — how the team worked, (B) Technical pattern — an architecture or code approach, (C) Communication pattern — how decisions were made and shared, (D) Something else."

3. **Propose approaches before generating** — Before writing each section, briefly describe your framing: "For the 'What Didn't Work' section, I'll focus on systemic issues rather than individual blame. Does that approach work for you?"

4. **Present output section-by-section** — Present each section for approval before moving on.

5. **Track outstanding questions** — If something can't be answered now, note it as a follow-up item in the retrospective.

6. **Multiple handoff options** — At completion, present next steps.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing retrospective at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

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

## INTERVIEW PROTOCOL

Conduct the retrospective as a reflective conversation. Ask one question at a time, listen carefully, and follow up where the user's answer reveals something worth exploring deeper.

### Step 0: Context Loading

Before starting the interview:
1. Check if `docs/ets/projects/{project-slug}/discovery/project-context.md` exists — read for project name and scope
2. Check if `docs/ets/projects/{project-slug}/planning/prd.md` exists — read for feature list
3. Check if `docs/ets/projects/{project-slug}/architecture/tech-spec.md` exists — read for ADR list
4. Check if any prior retrospectives exist in `docs/ets/projects/{project-slug}/learnings/` — read to avoid asking about already-captured learnings

If documents exist, use them to ask more specific questions (e.g., "ADR-3 chose PostgreSQL over MongoDB — how did that decision play out?").

### Step 1: What Went Well?

**Primary question** (ask alone, one message):
> "Looking back at this project, what went well? What are you proud of?"

**Follow-up probes** — ask one at a time based on the answer:
- If the answer is generic: "Can you give me a specific example — a moment where things clicked?"
- If only technical wins mentioned: "What about the process or team dynamics — anything that worked well there?"
- If only one item: "What else? Try to think of 2-3 more things."

### Step 2: What Didn't Go Well?

**Primary question** (ask alone, one message):
> "What didn't go well? What was frustrating or harder than expected?"

**Follow-up probes** — ask one at a time based on the answer:
- If blame-oriented: "Setting aside who — what systemic issue caused that?"
- If only one item: "What else? Even small things count — they often reveal patterns."
- If vague: "Can you walk me through a specific incident where this problem showed up?"

### Step 3: What Patterns Did We Discover?

**Primary question** (ask alone, one message):
> "Did you notice any recurring patterns — things that kept coming up, either positively or negatively?"

**Follow-up probes** — ask one at a time based on the answer:
- If unclear: "For example: 'Every time we skipped code review, we had a bug the next day' — anything like that?"
- If patterns mentioned: "Would you say this is specific to this project, or something that would apply to future projects too?"
- Classify each pattern: Process, Technical, Communication, or Other

### Step 4: What Decisions Paid Off? Which Backfired?

**Primary question** (ask alone, one message):
> "Think about the key decisions made during this project — which ones paid off, and which ones backfired?"

**Follow-up probes** — ask one at a time based on the answer:
- If upstream docs exist: "I see ADR-# decisions in tech-spec.md — how did [specific ADR] play out?"
- If only technical decisions mentioned: "What about non-technical decisions — scope, timeline, team structure, communication?"
- For each decision: "Knowing what you know now, would you make the same choice?"

### Step 5: What Would We Do Differently?

**Primary question** (ask alone, one message):
> "If you could go back to the start of this project with everything you know now, what would you do differently?"

**Follow-up probes** — ask one at a time based on the answer:
- If the answer is broad: "Can you narrow it to the one single change that would have had the biggest impact?"
- If only process changes: "Any technical decisions you'd revisit?"
- If only technical changes: "Any process or communication changes?"

### Interview Completion

After all 5 questions, present a brief synthesis of the key learnings and ask: "Does this capture the most important lessons? Anything I missed?"

## ID SYSTEM

Each learning gets a unique ID:

- `LEARN-#` — Sequential learning ID (LEARN-1, LEARN-2, LEARN-3...)
- Each LEARN-# gets one or more tags from: `architecture`, `data`, `ux`, `api`, `process`, `communication`, `testing`, `deployment`, `scope`, `estimation`, `tooling`

Example:
```
LEARN-1 [architecture, process]: PostgreSQL was the right choice for our relational data model, but we should have set up read replicas from the start.
LEARN-2 [estimation, scope]: Feature X took 3x longer than estimated because we underestimated the authentication complexity.
```

## OUTPUT FORMAT

**Path:** `docs/ets/projects/{project-slug}/learnings/retro-{slug}.md`

Where `{slug}` is derived from:
- The project name if available (from project-context.md)
- Or from user input if asked
- Or from the current date (retro-2026-03-17)

The document follows the template in `knowledge/template.md`.

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the retrospective document template and structure.

## INPUT VALIDATION

This skill has no strict upstream dependencies. It works best with existing project documents but can run purely from interview data.

If upstream documents exist:
- [ ] Read project-context.md for project name and scope
- [ ] Read prd.md for feature list (map decisions to features)
- [ ] Read tech-spec.md for ADR list (review architectural decisions)

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] At least 3 items in "What Worked" section
- [ ] At least 3 items in "What Didn't Work" section
- [ ] At least 2 patterns identified with classification tags
- [ ] At least 3 decision outcomes documented (paid off or backfired)
- [ ] At least 3 recommendations for future projects
- [ ] All LEARN-# IDs are sequential and tagged
- [ ] Document has interview date and participants

If any check fails, mark as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## WORKFLOW — PRE-SAVE CHECKS

### Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is lightweight work and the document has unnecessary sections → trim empty or boilerplate sections
  - If this is complex work and sections are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline still have to invent if this document is all they get?
  2. Do any sections depend on content claimed to be out of scope?
  3. Are there implicit decisions that should be explicit?
  4. Is there a low-effort addition that would make this significantly more useful for the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/learnings/retro-{slug}.md`) + paths to upstream documents (none — retrospectives have no BLOCKS dependencies)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/learnings/retro-{slug}.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

## CLOSING SUMMARY

After saving and validating, display:

```text
Retrospective saved to `docs/ets/projects/{project-slug}/learnings/retro-{slug}.md`

Status: [COMPLETE | DRAFT]
Learnings captured: LEARN-1 through LEARN-N
Tags covered: [list of unique tags]
```

Then present these options:

1. **Start a new project (Recommended if between projects)** — Apply these learnings in a fresh `/start-project`
2. **Refine this retrospective** — Add more detail or revisit specific sections
3. **Run another retrospective** — For a different project or sprint
4. **Pause for now** — The document is saved and will be available for future discovery phases

Wait for the user to choose before taking any action.

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| No upstream documents found | Info | Run interview from user memory only | Proceed — learnings are still valuable |
| User provides very short answers | Medium | Ask follow-up probes | Accept minimal input, mark as DRAFT |
| Prior retrospective exists for same project | Low | Ask: "Update existing or create new?" | Default to create new with date suffix |
| Output validation fails | Medium | Mark as DRAFT, flag thin sections | Proceed — partial learnings are better than none |
