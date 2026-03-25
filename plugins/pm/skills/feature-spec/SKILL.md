---
name: feature-spec
description: >
  Use when a feature has complex business logic, multiple state transitions, or
  intricate validation rules that need detailed specification. Also triggers on
  'feature specification', 'this feature needs a detailed spec', 'complex feature',
  'state machine', or 'business rules'.
model: opus
version: 1.0.0
argument-hint: "[feature-name]"
compatibility: "Optional: external issue tracker adapter (for example, Linear) for issue details and acceptance criteria"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (required — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/planning/prd.md` — Provides the PRD-F-# feature definition and priority. Without it, the spec has no scope anchor.
- `docs/ets/projects/{project-slug}/planning/user-stories.md` — Provides US-# acceptance criteria that the spec elaborates on. The spec adds business rules and state logic on top of what the stories define.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Business context and personas help ground business rules in real user scenarios.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `feature-spec.requires: [prd, user-stories]`
2. Check both required docs exist, non-empty, not DRAFT
3. If either missing → auto-invoke the missing skill → wait → continue
4. Check ENRICHES → warn if missing, proceed

## ARTIFACT SAVE RULE

**Why this matters:** Feature specs contain the detailed business rules (FS-#) that architecture and implementation skills reference. If the spec only exists in chat, the tech-spec cannot incorporate ADRs for complex logic, and the implementation plan cannot reference FS-# rule IDs.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in FEATURE SPEC FORMAT
3. Displaying content in chat is not the same as saving — the file needs to exist on the filesystem for downstream skills to reference FS-# IDs
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only then propose the next step

**If the Write fails:** Report the error to the user and do not proceed — downstream documents depend on FS-# references in this file.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Use the AskUserQuestion tool when available for structured choices. Complex features have many rules; exploring them one at a time prevents missed edge cases.

2. **3-4 suggestions for choices** — When the user needs to choose between state models, error handling strategies, or validation approaches, present 3-4 concrete options with tradeoffs. Highlight your recommendation.

3. **Present business rules one at a time** — Present each FS-# rule individually with its description, trigger condition, and expected result. Ask "Does this rule capture it correctly? Anything to adjust?" before moving to the next rule.

4. **Propose state machines visually before committing** — If the feature has state transitions, propose 2-3 state model options using Mermaid diagrams. Let the user choose the right model before detailing transitions.

5. **Suggest edge cases per rule** — For each business rule, suggest 2-3 edge cases the user may not have considered. Ask which are relevant before including them.

6. **Propose validation options per field** — For validation rules, present 2-3 options per field (strict vs. lenient, client-side vs. server-side, etc.) and ask which approach fits.

7. **Track outstanding questions** — If something cannot be answered now, classify it:
   - **Resolve before next phase** — This blocks the handoff to Design.
   - **Deferred to [phase name]** — Noted and carried forward.

8. **Multiple handoff options** — At completion, present 3-4 next steps as options (see CLOSING SUMMARY).

9. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing feature-spec at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

10. **Assess if full process is needed** — If the user's input is already detailed with clear requirements, specific acceptance criteria, and defined scope, don't force the full interview. Confirm understanding briefly and offer to skip directly to document generation. Only run the full interactive process when there's genuine ambiguity to resolve.

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
- Feature has >3 business rules or complex state transitions
- Multiple error recovery paths that need explicit documentation
- Business logic has conditional branching (discounts, tiers, permissions)

**Use short version when:**
- Feature has 3-4 clear rules with no state machine
- Linear workflow with simple validation
- Even in short version, still include: Overview, Business Rules (FS-# IDs), and Edge Cases

## PURPOSE

Provide a deep-dive specification for complex features that exceed the user-story threshold. A feature-spec is **not always needed** — it's created on-demand only when a feature has >3 business rules, state transitions, or intricate validation logic. This keeps user-stories.md lean while providing implementation teams with detailed logic maps for complex workflows.

## CONTEXT LOADING

Load context in this order of priority:

1. **$ARGUMENTS**: If the user passes `[feature-name]`, identify that feature in the current project context.
2. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for prior feature analysis or complexity assessments.
3. **Document Scan**: Scan `docs/ets/projects/{project-slug}/planning/` for user-stories.md to find US-# that reference this feature.
4. **User Interview**: If nothing found, interview the user about the feature's complexity.

## COMPLEXITY THRESHOLD

A feature-spec is created when a feature meets at least one of these criteria (the goal is to keep user-stories.md lean while giving implementation teams detailed logic maps for complex workflows):

**1. More than 3 business rules**
- Example: "Duplicate Invoice" feature
  - Rule 1: Copy all line items from original
  - Rule 2: Reset due date to 30 days from today
  - Rule 3: Mark as "Duplicated from #123" in audit trail
  - Rule 4: Notify client if the duplicate is sent within 24h
  - Rule 5: Prevent duplication if original invoice status is not "Final"
  - → 5 rules exceeds threshold → **Create feature-spec**

**2. State machine / multiple state transitions**
- Example: "Invoice lifecycle" has states: Draft → Saved → Sent → Paid, with alternative paths like Draft → Deleted or Sent → Overdue
  - → Multiple states + transitions → **Create feature-spec**

**3. Intricate validation logic**
- Example: "Apply volume-based discount" with rules:
  - 5+ items: 5% discount
  - Total >$1000: 10% discount
  - Repeat customer: +2% bonus
  - Discounts don't stack; use maximum of the three
  - → Complex conditional logic → **Create feature-spec**

**4. Elaborate error handling & recovery**
- Example: "Send invoice via email" with multiple failure paths:
  - Invalid email → Prompt user to correct
  - SMTP failure → Auto-retry 3 times, then notify
  - Customer blocked → Display reason
  - → Multiple error paths → **Create feature-spec**

**When NOT to create feature-spec (stay with user-stories):**
- Simple CRUD (create, read, update, delete with basic validation)
- Linear workflows with no branching
- Fewer than 3 business rules
- Behavior fully expressible in Given/When/Then

## ON-DEMAND PATTERN

This skill is invoked after user-stories.md is complete, because stories need to exist before we can assess which features exceed the complexity threshold. During user-stories planning:

1. Each US-# is evaluated: "Does this story exceed 3 business rules or have state complexity?"
2. If YES → Flag with note: "Candidate for feature-spec-[kebab-name].md"
3. If NO → Leave as user-story only

Then, for each flagged story, invoke this skill to generate the feature-spec.

## FEATURE SPEC FORMAT

The generated `docs/ets/projects/{project-slug}/planning/feature-spec-[kebab-name].md` contains:

- **Feature Overview**: Name, linked US-#, problem statement
- **Business Rules** (numbered FS-[kebab-name]-1, FS-[kebab-name]-2, ...): Each rule explicit and testable
- **State Machine Diagram** (if applicable, using Mermaid): All states, transitions, and conditions
- **Validation Rules**: Input constraints, edge cases, boundary conditions
- **Error Handling Matrix**: Structured EDGE-# scenario handling with system response and user message
- **Error Handling & Recovery**: Failure paths, retry logic, user prompts
- **State Machine** (mandatory if feature has >2 states): Mermaid diagram, valid transitions, forbidden transitions
- **Permission Matrix**: Action-by-role access control table
- **Data Transformations**: Formulas, calculations, data flow
- **Edge Cases & Assumptions**: Non-obvious scenarios the implementation must handle

Example sections:

```
## Business Rules

FS-checkout-1: Cart total calculated as sum of all line items after discounts and taxes
FS-checkout-2: If user has active coupon, apply before tax calculation
FS-checkout-3: Coupon expires at end of UTC day; validate before applying
FS-checkout-4: If coupon reduces total below $5, show warning "Order may incur small-order fee"

## State Machine

[Mermaid diagram showing: Empty Cart → Items Added → Coupon Applied → Checkout → Payment Processing → Complete]

## Validation Rules

- Cart items: 1-100 items per order
- Coupon code: 6-16 alphanumeric, case-insensitive
- If coupon expired: show error "This code has expired. Try another."
```

## ID GENERATION

**FS-[kebab-name]-# Pattern**: Feature Spec rules. Format: `FS-checkout-1`, `FS-checkout-2`, etc.

- Kebab-name: Slug of the feature name (e.g., "payment-processing", "user-onboarding")
- Number: Sequential within the spec (FS-checkout-1, FS-checkout-2...)
- Each rule is explicitly numbered and traceable

Maintain traceability: `US-# → feature-spec-[kebab-name].md → FS-[kebab-name]-#`

## KNOWLEDGE POINTERS

- Read `references/template.md` for the feature-spec-[name].md document template and standard sections.
- Read `references/guide.md` for best practices on detailing business rules, drawing state machines with Mermaid, and capturing edge cases without over-specifying implementation.

---

**This skill is on-demand and invoked after user-stories.md is complete. Create a feature-spec for each flagged feature that exceeds the complexity threshold. Present handoff options to the user after each spec (see CLOSING SUMMARY). The architecture-agent will incorporate completed specs into tech-spec and ADRs during the Design phase.**

## INPUT VALIDATION

**prd.md** (BLOCKS):
- Needs to contain the specific PRD-F-# being expanded — the spec must trace back to a defined feature
- Feature should have MoSCoW priority — this determines how much detail is warranted

**user-stories.md** (BLOCKS):
- Needs at least 1 US-# referencing the target PRD-F-# — the spec elaborates on stories, so at least one story must exist

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Feature name matches PRD-F-# from prd.md
- [ ] All US-# for this feature are referenced
- [ ] Business rules documented (>3 rules for complex features)
- [ ] State machine or workflow diagram present (if stateful, mandatory if >2 states)
- [ ] Error handling matrix present with EDGE-# references
- [ ] Permission matrix present with role-based access for all actions
- [ ] Edge cases listed with expected behavior
- [ ] FS-{name}-# IDs are unique and sequential
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display the summary and offer multiple next steps:

```text
feature-spec-[name].md saved to `docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-[name].md`

Status: [COMPLETE | DRAFT]
IDs generated: [list FS-{name}-# IDs, e.g., FS-checkout-1, FS-checkout-2, FS-checkout-3]

What would you like to do next?

1. Create next Feature Spec — If more features need detailed specs
2. Proceed to Planning Gate (Recommended) — Validate planning artifacts before Design phase
3. Refine this spec — Review and improve specific sections
4. Pause for now — Save and return later
```

Wait for the user's choice before proceeding. Do not auto-advance to the next skill.

## WORKFLOW

### Step 1: Feature Identification & Confirmation
- **Input:** PRD-F-# from prd.md, US-# from user-stories.md
- **Action:** Load feature definition, acceptance criteria, priority
- **Output:** Feature context bundle
- **Checkpoint:** Present the feature overview and ask: "Is this the right feature to detail? Does the complexity reason (>3 rules / state machine / validation) match?"

### Step 2: Business Rules — One Rule at a Time
- **Input:** Feature context + user input
- **Action:** For each business rule:
  1. Present the rule as FS-[name]-# with description, trigger condition, and expected result
  2. Ask: "Does this rule capture it correctly? Anything to adjust?"
  3. After the user approves, suggest 2-3 edge cases for this rule
  4. Ask: "Are any of these edge cases relevant?"
  5. Only after approval, move to the next rule
- **Output:** Business rules table with FS-{name}-# IDs, approved one by one
- **Checkpoint:** After all rules are listed, present the complete rules table and ask: "Is this the full set of rules, or is anything missing?"

### Step 3: State Machine (if applicable) — Propose Options
- **Input:** Business rules from Step 2
- **Action:**
  1. Propose 2-3 state model options using Mermaid diagrams (e.g., minimal states vs. full lifecycle vs. with error states)
  2. Ask: "Which model best represents this feature?"
  3. After the user chooses, detail each transition one at a time
  4. Ask about forbidden transitions: "Are there transitions that should be explicitly blocked?"
- **Output:** Approved state machine diagram
- **Checkpoint:** Present the final diagram and ask: "Does this cover all states and transitions?"

### Step 4: Validation Rules — Propose Options per Field
- **Input:** Business rules + state machine
- **Action:** For each field that needs validation:
  1. Present 2-3 validation approaches (e.g., strict vs. lenient, client vs. server, format options)
  2. Ask: "Which approach fits for this field?"
  3. Ask for the exact error message the user should see
- **Output:** Validation rules table with conditions, error messages, and affected fields
- **Checkpoint:** Present the complete validation table and ask: "Does this cover all the validation needs?"

### Step 5: Error Handling Matrix
- **Input:** All rules, states, and validations + EDGE-# from upstream opportunity-pack or edge-case sweep
- **Action:**
  1. For each EDGE-# relevant to this feature, document the handling in a structured matrix:
     | EDGE-# | Scenario | Trigger | System Response | User Message | Retry? | Rollback? |
  2. Present each error scenario individually with condition, user message, and recovery strategy
  3. Ask: "Is this the right behavior for this error?"
  4. Suggest 2-3 additional edge cases the user may not have considered
  5. Ask: "Are any of these relevant?"
- **Output:** Error handling matrix and edge case list

### Step 5b: Permission Matrix
- **Input:** Actor map from upstream, business rules
- **Action:**
  1. Identify all actions in the feature
  2. Build a permission matrix mapping actions to roles:
     | Action | Public | User | Editor | Admin | Superadmin |
  3. Ask: "Does this permission model match your requirements? Any actions missing?"
- **Output:** Approved permission matrix

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
  1. Verify directory exists: `docs/ets/projects/{project-slug}/planning/feature-specs/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-[name].md` using the Write tool (where [name] is the kebab-case feature name)
  3. The document needs to exist on the filesystem for downstream skills — presenting content in chat is not sufficient.
- **Output:** File written to disk at the specified path

### Step 9: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-[name].md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/planning/prd.md`, `docs/ets/projects/{project-slug}/planning/user-stories.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 10: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-[name].md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
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
| BLOCKS dep missing | Critical | Auto-invoke upstream skill | Block execution |
| PRD-F-# not found in prd.md | Critical | Ask user which feature to expand | Block — can't spec unknown feature |
| Feature has <3 business rules | Low | Proceed — not all features are complex | Note: "Feature may not need a spec" |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
