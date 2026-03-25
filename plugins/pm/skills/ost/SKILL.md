---
name: ost
description: >
  Use when structuring discovery findings into an opportunity tree that connects
  outcomes to opportunities to candidate solutions. Also triggers on 'OST',
  'opportunity solution tree', 'opportunity tree', 'where should we focus',
  'which opportunities', or 'structure the discovery'.
model: opus
version: 1.0.0
argument-hint: "[context-path]"
compatibility: "Optional: external issue tracker adapter (for example, Linear) for discovery tickets/evidence, Slack MCP (pull stakeholder discussions)"
---

## PURPOSE

Structure discovery findings into a clear opportunity tree: Outcome (measurable result) → Opportunities (real problems/desires supported by evidence) → Candidate Solutions (high-level directions, not specs) → Assumptions and optional Experiments. The OST reduces the risk of "jumping to features" by forcing structured reasoning: first choose WHERE to attack, then choose HOW. It bridges Discovery and Planning — opportunities selected here become features in the PRD.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Outcome comes from BO-# business objectives.
- `docs/ets/projects/{project-slug}/discovery/baseline.md` — Evidence for opportunities comes from baseline metrics.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Qualitative context improves opportunity framing.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `ost.requires: [product-vision, baseline]`
2. Check: do `docs/ets/projects/{project-slug}/discovery/product-vision.md` and `docs/ets/projects/{project-slug}/discovery/baseline.md` exist, are non-empty, and are not `<!-- STATUS: DRAFT -->`?
3. If product-vision missing → INFORM user → auto-invoke `product-vision` skill → wait → continue
4. If baseline missing → INFORM user → auto-invoke `baseline` skill → wait → continue
5. If either is DRAFT → WARN: "[document] is DRAFT — OST may have weaker evidence foundation" → proceed
6. If project-context.md exists → load for additional qualitative context

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — challenge opportunity framing, push for evidence, flag when solutions are disguised as opportunities, and help the user distinguish outcome from output. OST work is about structured reasoning under uncertainty — these patterns ensure the user builds an honest, evidence-backed tree, not a wish list.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. OST questions require the user to synthesize discovery findings, so give them space. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., outcome framing, opportunity prioritization, experiment design), present 3-4 concrete options with a brief description of each. Highlight your recommendation. Let the user pick before proceeding.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs. Example: "I see three ways to frame this outcome: (A) conversion-focused — increase funnel completion rate, (B) efficiency-focused — reduce time/cost per conversion, (C) quality-focused — improve lead quality while maintaining volume. I recommend A because it directly ties to the baseline's biggest drop-off."

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section (Outcome, then Opportunity list, then each Opportunity detail one by one), ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Resolve before PRD** — This blocks the next phase. Keep asking until resolved.
   - **Deferred to experiment** — Needs validation, not just discussion.
   - **Deferred to [phase name]** — Noted and carried forward.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options instead of a single fixed path.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing ost.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

8. **Assess if full process is needed (right-size check)** — If the user's input already has a clear outcome, well-evidenced opportunities, and candidate solutions, don't force the full interview. Confirm understanding briefly and offer to skip directly to document generation. Only run the full interactive process when there's genuine ambiguity to resolve.

9. **Thinking partner behaviors:**
   - When an opportunity sounds like a solution: "That sounds more like a 'how' than a 'what.' Can we reframe it as the underlying problem or desire?"
   - When evidence is weak: "What data supports this? Can we link to baseline metrics or discovery findings?"
   - When everything is marked critical: "If we had to pick only ONE opportunity to pursue this quarter, which would it be? That's our real P0."
   - When outcome is an output: "That's a deliverable (output), not a result (outcome). What business metric improves if we succeed?"

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

- **Is this outcome or output?** — "Is '[stated outcome]' a measurable result, or is it actually a deliverable? An outcome changes a metric; an output ships a thing."
- **Are these real opportunities or disguised solutions?** — "Review each opportunity: is it describing a problem/desire (good) or describing 'build X' (that's a solution, not an opportunity)?"
- **Is the evidence real?** — "For each opportunity, can we point to specific data from the baseline, a user quote from discovery, or an incident ticket? Assertions without evidence are hypotheses, not opportunities."
- **Would doing nothing be acceptable?** — "What happens to the outcome metric if we invest in NONE of these opportunities? If the answer is 'not much changes,' the outcome may need rethinking."

The goal is to sharpen the tree's quality, not to block progress. If the framing is solid, acknowledge it and move on quickly.

## ANTI-PATTERNS

These anti-patterns come from the team's real experience (KB). Flag them actively during the interview and generation:

1. **Backlog disguised as OST** — The OST is not a list of tickets or user stories. If opportunities read like "implement feature X" or have acceptance criteria, push back: "This looks like a backlog item. What's the underlying problem it solves?"

2. **Opportunities written as solutions** — Opportunities must describe problems or desires, not actions. Bad: "Build a new onboarding flow." Good: "New users abandon before completing first action (68% drop-off at step 3)."

3. **Everything is P0** — If all opportunities are marked critical, the tree is too big or prioritization is missing. Ask: "If you could only pursue ONE of these, which would it be?"

4. **Outcome is output** — Outcome must be a measurable business result, not a deliverable. Bad: "Launch media library." Good: "Increase content creation rate from X to Y per week."

5. **Vague terms without metrics** — "Improve experience" or "make it better" without specifying how to measure improvement. Push for specificity.

6. **No evidence** — Opportunities listed without data, quotes, or incident references. Every opportunity must have at least one evidence point.

## CONTEXT LOADING

Load context in this order of priority:

1. **$ARGUMENTS**: If the user passes `[context-path]`, read that file directly.
2. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for upstream discovery artifacts.
3. **Document Scan**: Scan `docs/ets/projects/{project-slug}/discovery/` for product-vision.md and baseline.md. Load BO-# objectives and baseline metrics.
4. **User Interview**: If nothing found, begin the OST interviews interactively.

## INTERVIEW PROTOCOL

This interview follows a one-question-at-a-time rhythm. Ask each question alone in one message, wait for the user's answer, then decide whether to ask a follow-up or move forward.

### Block 1: Outcome

**Question 1** (ask alone, one message):
> "Qual e o outcome que estamos perseguindo? Lembre: outcome e resultado mensuravel, nao entrega. Exemplo: 'Aumentar taxa de conclusao do funil X de A% para B% mantendo CPL <= Y ate MM/AAAA.'"

Wait for the answer. If the stated outcome is an output, challenge it:
> "Isso parece mais uma entrega (output) do que um resultado (outcome). Qual metrica de negocio melhora se essa entrega for bem-sucedida?"

**Follow-up** (ask alone, one message):
> "Quais sao as metricas principais desse outcome? Para cada uma, qual e o baseline atual (do documento de baseline), a meta, e o periodo?"

Then ask:
> "Quais guardrails nao podem piorar enquanto perseguimos esse outcome? (Ex.: conversao nao pode cair abaixo de X%, p95 nao pode subir acima de Yms)"

### Block 2: Opportunities List

**Question 2** (ask alone, one message):
> "Quais sao as principais oportunidades/problemas que o discovery revelou? Liste 3-7 em uma linha cada. Lembre: oportunidade e problema/dor/desejo real, nao 'fazer X' (isso e solucao)."

Wait for the answer. Review each item against anti-patterns:
- If any sounds like a solution → "O-# parece ser uma solucao, nao uma oportunidade. Qual e o problema subjacente?"
- If more than 7 → "Temos [N] oportunidades — isso pode ser muito. Podemos agrupar ou priorizar para manter 3-7?"

### Block 3: Opportunity Details (one at a time)

For each opportunity from Block 2, ask one at a time:

**Question 3** (ask alone, one message, for each O-#):
> "Vamos detalhar O-[#] — [titulo]. Descreva o problema/oportunidade em 3-6 linhas. Para quem isso importa (persona/area)?"

Wait for the answer. Then ask:

**Question 4** (ask alone, one message):
> "Quais evidencias sustentam O-[#]? Precisamos de pelo menos: (1) um dado com fonte, (2) um relato/quote, (3) um incidente/ticket. O que voce tem?"

Then ask:

**Question 5** (ask alone, one message):
> "Quais solucoes candidatas voce ve para O-[#]? Liste 2-5 direcoes em alto nivel — sem detalhar requisitos, apenas a direcao."

Then ask:

**Question 6** (ask alone, one message):
> "Quais suposicoes (assumptions) precisam ser verdadeiras para essas solucoes funcionarem? O que pode invalidar a abordagem?"

**Optional — ask only if relevant:**
> "Alguma solucao de O-[#] precisa de experimento antes de investir? Se sim: qual experimento, como medir, qual criterio de sucesso, e qual duracao?"

Repeat Block 3 for each opportunity.

### Block 4: Prioritization & Next Steps

**Question 7** (ask alone, one message):
> "Olhando todas as oportunidades juntas: quais sao as mais criticas agora e por que? Quais podem esperar? (Isso nao e a priorizacao oficial — e para sinalizar urgencia relativa.)"

**Question 8** (ask alone, one message):
> "Quais questoes ainda estao em aberto? O que falta validar antes de ir para o PRD?"

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/planning/ost.md` contains:

- **Header**: Title, version, date, owner, contributors, evidence links, horizon
- **1. Outcome**: Measurable outcome statement + main metrics (baseline → target → period) + guardrails
- **2. Oportunidades (lista resumida)**: 3-7 opportunities, one line each, with O-# IDs
- **3. Detalhamento por oportunidade** (repeated block for each O-#):
  - Description (3-6 lines)
  - Who it matters to (persona/area)
  - Evidence (mandatory: data + source, quote/report, incident/ticket)
  - Potential impact (how it affects the outcome)
  - Critical assumptions
  - Candidate solutions (S-#.# IDs, 2-5 high-level directions)
  - Experiments/validations (optional: name, objective, method, success criteria, duration)
- **4. Priorizacao preliminar**: Most critical now + can wait, with 1-2 line justification each
- **5. Questoes em aberto e proximos passos**: Open questions + suggested next steps
- **6. Links e anexos**: Baseline, discovery report, prioritization doc, PRDs, Figma/Miro

**SST Rule:** Structured opportunities and candidate solutions ONLY in this document. No other document should redefine the opportunity tree.

## ID GENERATION

**O-# Pattern**: Opportunities. Format: `O-1`, `O-2`, `O-3`. Each O must:
- Describe a real problem/desire (not a solution)
- Have at least one evidence point (data, quote, or incident)
- Link to the outcome metric it affects

**S-#.# Pattern**: Solution candidates under an opportunity. Format: `S-1.1`, `S-1.2`, `S-2.1`. Each S must:
- Be a high-level direction (not detailed requirements)
- Be under a specific O-# parent
- Be unique and distinguishable from sibling solutions

Downstream traceability: `O-# → selected S-#.# → PRD-F-# features in prd.md`

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the OST document template and structure.

## INPUT VALIDATION

**product-vision.md** (BLOCKS):
- Must contain at least 1 BO-# (Business Objective) with measurable success criterion
- Must have a vision statement

**baseline.md** (BLOCKS):
- Must contain at least 1 metric area (A-D) with baseline data
- Must have Fluxo AS-IS section

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Outcome is a measurable result (not an output/deliverable)
- [ ] Outcome has at least 1 metric with baseline → target → period
- [ ] At least 1 guardrail defined
- [ ] 3-7 opportunities listed with O-# IDs
- [ ] Every opportunity has at least 1 evidence point (data + source)
- [ ] Every opportunity has 2-5 candidate solutions with S-#.# IDs
- [ ] No opportunity reads like a solution (anti-pattern check)
- [ ] Outcome is not an output (anti-pattern check)
- [ ] Assumptions documented for at least the top 3 opportunities
- [ ] Source Documents section present at top referencing product-vision.md and baseline.md

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
ost.md saved to `docs/ets/projects/{project-slug}/planning/ost.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list O-# and S-#.# IDs]
Opportunities: [count] | Solutions: [count] | Experiments: [count]
```

Then present these options using AskUserQuestion (or as a numbered list if AskUserQuestion is unavailable):

1. **Proceed to PRD (Recommended)** — Transform selected opportunities into PRD features (PRD-F-#)
2. **Proceed to Planning Gate** — Validate planning artifacts before Design
3. **Refine this document** — Review and improve specific opportunities or add experiments
4. **Pause for now** — Save and return later (the document is already on disk)

Wait for the user to choose before taking any action. Do not auto-proceed to the next skill.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `product-vision.md` (BLOCKS), `baseline.md` (BLOCKS), optionally `project-context.md` (ENRICHES)
- **Action:** Extract BO-# objectives, baseline metrics, AS-IS flow, pain points. Summarize key points to the user to show you've absorbed the context.
- **Output:** Internal context object

### Step 2: Pressure Test
- **Input:** Step 1 context
- **Action:** Challenge the framing with 1-2 pressure test questions. Verify outcome is truly an outcome, not an output. Check that evidence exists.
- **Output:** Validated/refined framing

### Step 3: OST Interview (one question at a time)
- **Input:** Step 1-2 context + user responses (interactive)
- **Action:** Run the 4-block INTERVIEW PROTOCOL. Ask one question per message, wait for answers. For each opportunity, ensure evidence is present. Flag anti-patterns actively.
- **Output:** Raw interview notes (internal)

### Step 4: Section-by-Section Document Generation
- **Input:** Interview notes from Step 3
- **Action:** Generate the document one major section at a time, using the template from `knowledge/template.md`. For each section:
  1. **Propose approach** — Before generating, briefly describe how you plan to frame this section
  2. **Generate the section** — Present it to the user
  3. **Ask for approval** — "Does this capture it well? Anything to adjust?"
  4. **Incorporate feedback** — If the user wants changes, revise and re-present
  5. **Move to next section** — Only after the user approves

  Section order:
  - Outcome (statement + metrics + guardrails)
  - Oportunidades (summary list)
  - Detalhamento O-1 (description, evidence, solutions, assumptions, experiments)
  - Detalhamento O-2 (repeat)
  - ... (repeat for each O-#)
  - Priorizacao preliminar
  - Questoes em aberto e proximos passos
  - Links e anexos
- **Output:** Approved sections assembled into complete ost.md
- **Integration:** O-# and S-#.# IDs consumed by `prd` skill to generate PRD-F-#

### Step 5: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is a very localized improvement (1 opportunity) → offer "versao curta" with just outcome, 1 opportunity, and candidate solutions
  - If this is complex work and opportunities lack evidence → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 6: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the PRD skill still have to invent if this OST is all they get?
  2. Are there opportunities without evidence?
  3. Are there candidate solutions that are actually fully-specified features (too detailed for OST)?
  4. Is there a low-effort addition (e.g., one more evidence point, one assumption clarification) that would significantly improve the PRD phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 7: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/planning/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/planning/ost.md` using the Write tool
  3. The document is only saved when written to the filesystem — presenting content in chat is not the same as saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review
- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/planning/ost.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/discovery/product-vision.md`, `docs/ets/projects/{project-slug}/discovery/baseline.md`)
  2. The reviewer checks: completeness, evidence quality, anti-pattern compliance, ID consistency, SST compliance
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Output:** Reviewed and approved document

### Step 9: User Review Gate
- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/planning/ost.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
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
| BLOCKS dep missing (product-vision.md) | Critical | Auto-invoke product-vision skill — outcome needs BO-# objectives | Pause until product-vision is available |
| BLOCKS dep missing (baseline.md) | Critical | Auto-invoke baseline skill — evidence needs baseline metrics | Pause until baseline is available |
| BLOCKS dep is DRAFT | Warning | Proceed with available context, noting evidence may be weaker | Add `<!-- ENRICHMENT_MISSING: [doc] is DRAFT -->` |
| User lists >7 opportunities | Medium | Help group/prioritize: "Can we cluster related items or defer some?" | Accept up to 10 if user insists, but flag as complex |
| Opportunity has no evidence | High | Push for at least 1 data point: "What from the baseline or discovery supports this?" | Mark opportunity as `<!-- EVIDENCE: MISSING -->` |
| Outcome is an output | High | Challenge and reframe: "What metric improves if this is delivered?" | Do not proceed until outcome is a measurable result |
| Output validation fails | High | Address gaps, re-present sections to user | Mark as DRAFT |

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

### Invocation

- **Automatic:** Orchestrator invokes Quality Loop for all high-dependency documents
- **Manual:** User can request `--quality-loop` on any skill invocation
- **Skip:** User can pass `--no-quality-loop` to disable (generates once, validates once)
