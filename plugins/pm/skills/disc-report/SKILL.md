---
name: disc-report
description: >
  Use when consolidating discovery findings into an evidence-based report with
  methodology, key evidence, insights by theme, personas/JTBD, testable hypotheses,
  and remaining uncertainties. Also triggers on 'discovery report', 'research findings',
  'what did we learn', 'evidence summary', 'discovery synthesis', or 'sumário de evidências'.
model: opus
version: 1.0.0
argument-hint: "[context-path]"
compatibility: "Optional: Slack MCP (pull stakeholder discussions), external issue tracker adapter (for example, Linear) for discovery tickets and evidence"
---

## PURPOSE

Consolidate what was learned during discovery (qualitative and quantitative) and transform scattered information into actionable insights. This document exists so that product decisions do not depend on memory, opinion, or meetings — and to sustain the OST and prioritization with facts.

This is DIFFERENT from project-context. Project-context captures the 5W2H (what are we building). Discovery Report captures the EVIDENCE gathered during research (what did we learn). It does not close scope (that is the PRD) and does not prioritize (that is the prioritization document).

**Principle:** Evidence before decision.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/baseline.md` — Evidence references baseline metrics; context for the "before" picture.
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Scope context needed to know what initiative the discovery covers.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Vision helps focus the research; BO-# objectives inform which evidence matters most.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `discovery-report.requires: [baseline, project-context]`
2. Check: do `docs/ets/projects/{project-slug}/discovery/baseline.md` and `docs/ets/projects/{project-slug}/discovery/project-context.md` exist, are non-empty, and are not `<!-- STATUS: DRAFT -->`?
3. If baseline missing → INFORM user → auto-invoke `baseline` skill → wait → continue
4. If project-context missing → INFORM user → auto-invoke `project-context` skill → wait → continue
5. If either is DRAFT → WARN: "[document] is DRAFT — discovery report may have weaker evidence foundation" → proceed
6. If product-vision.md exists → load BO-# objectives to focus evidence capture

**Position in workflow:** After baseline, before product-vision OR in parallel with product-vision. The discovery report and product-vision inform each other — evidence shapes vision, vision focuses research.

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — challenge weak evidence, push for specificity, help distinguish facts from hypotheses from interpretations, and flag when insights lack supporting data. Discovery report work is about synthesis and honesty — these patterns ensure the user builds an evidence-based narrative, not a dump of interviews or a wishful interpretation.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Discovery questions often require the user to revisit notes and data, so give them space. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., how to group themes, which personas to highlight, how to frame hypotheses), present 3-4 concrete options with a brief description of each. Highlight your recommendation. Let the user pick before proceeding.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs. Example: "I see three ways to organize the insights: (A) by user journey stage — maps findings to funnel steps, (B) by persona — groups findings by who is affected, (C) by theme — clusters related findings regardless of stage or persona. I recommend C because it best surfaces cross-cutting patterns."

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section (e.g., Objective, then Method, then Evidence, then Insights by Theme, etc.), ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Tier 1 (blocks decision)** — This must be resolved before advancing. Add to Incertezas section with responsible + date.
   - **Tier 2 (improves quality)** — Important but not blocking. Add to Incertezas section.
   - **Deferred to [phase name]** — Noted and carried forward.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options instead of a single fixed path.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing discovery-report.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

8. **Assess if full process is needed (right-size check)** — If the user's input already has well-synthesized evidence with sources, clear insights by theme, and testable hypotheses, don't force the full interview. Confirm understanding briefly and offer to skip directly to document generation. Only run the full interactive process when there's genuine ambiguity or missing synthesis.

9. **Thinking partner behaviors:**
   - When the user shares an insight, ask: "What evidence supports this? Is it a fact observed, a hypothesis, or an interpretation?"
   - When evidence is thin: "We have [N] data points for this theme. Is that enough to act on, or do we need more?"
   - When insights are vague: "Can we make this more specific? What metric or behavior changed, and by how much?"
   - When everything sounds like a solution: "This sounds like what we should build, not what we learned. What's the underlying finding?"
   - When causes are asserted without evidence: "Is this a confirmed cause or a plausible hypothesis? Let's label it accordingly."

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

Before generating content, challenge the evidence quality with these questions (ask the most relevant 1-2, not all):

- **"Do we have enough evidence, or are we interpreting too little data?"** — If the discovery covered <5 users or <1 metric source, flag that conclusions may be premature.
- **"Is the main insight a fact or an opinion?"** — Push for specificity: what was observed, by whom, when, and how?
- **"Are the probable causes supported by data or by intuitive logic?"** — Causes labeled "probable" should have at least one data point or pattern supporting them, not just a plausible narrative.
- **"Are we synthesizing or just listing?"** — A good discovery report transforms raw data into "so what?" implications. If insights don't end with "this means we should consider..." they may be incomplete.

The goal is to sharpen the report's quality, not to block progress. If the evidence is solid, acknowledge it and move on quickly.

## ANTI-PATTERNS

These anti-patterns come from the team's real experience (KB). Flag them actively during the interview and generation:

1. **Interview dump without synthesis** — The report is not a transcript. If sections read like raw interview notes without pattern extraction, push back: "Can we identify the pattern across these responses?"

2. **Writing like a PRD** — Discovery reports do not close scope or define requirements. If sections describe "what we will build," redirect: "This is a decision, not a finding. Let's capture what we learned, and decisions go to the PRD."

3. **Premature prioritization** — The discovery report does not rank or sequence items. If the user tries to assign P0/P1/P2 here, remind them: "Prioritization is the next document. Here we document all findings without ranking."

4. **Vague terms without measurement** — "Significant improvement," "many users complained," "better experience" — always push for specifics: how many, what metric, compared to what baseline.

5. **Confusing fact, hypothesis, and interpretation** — Every claim should be labeled: observed fact (data), hypothesis (testable claim), or interpretation (inference from limited data). Mix-ups erode trust in the report.

## CONTEXT LOADING

Load context in this order of priority:

1. **$ARGUMENTS**: If the user passes `[context-path]`, read that file directly.
2. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for upstream discovery artifacts.
3. **Document Scan**: Scan `docs/ets/projects/{project-slug}/discovery/` for existing baseline.md, project-context.md, product-vision.md. Load baseline metrics and scope context.
4. **User Interview**: If nothing found, begin the discovery report interviews interactively.

## INTERVIEW PROTOCOL

This interview follows a one-question-at-a-time rhythm. Ask each question alone in one message, wait for the user's answer, then decide whether to ask a follow-up or move forward.

### Block 1: Objective

**Question 1** (ask alone, one message):
> "Qual o objetivo deste discovery? Qual decisao ele pretende habilitar? Quais riscos queremos reduzir?"

Wait for the answer. Extract: decision to be enabled, risks to be reduced.

### Block 2: Research Questions

**Question 2** (ask alone, one message):
> "Quais perguntas de pesquisa queriamos responder? Liste como Q1, Q2, Q3..."

Wait for the answer. If fewer than 3 questions, probe: "Ha mais alguma pergunta que o time queria responder?"

### Block 3: Method & Sample

**Question 3** (ask alone, one message):
> "Qual metodo foi usado? Precisamos cobrir: (A) Fontes qualitativas — entrevistas (quantas, perfis, duracao, script), shadowing, suporte; (B) Fontes quantitativas — dados analisados, periodo, segmentacoes; (C) Outras fontes — tickets/CS, incidentes/logs, documentacao tecnica."

Wait for the answer. For each source, immediately probe:
- If qualitative sources are thin: "Quantos entrevistados? Qual o perfil? Isso e representativo do publico?"
- If quantitative sources lack period: "Qual o periodo dos dados? Isso cobre sazonalidade ou eventos atipicos?"

### Block 4: Key Evidence

**Question 4** (ask alone, one message):
> "Quais foram as principais evidencias encontradas? Liste 5-10 items, cada um com a evidencia concreta (dado, quote, print) e a fonte/link."

Wait for the answer. For each evidence item, classify: is it a fact, a pattern, or an outlier?

### Block 5: Insights by Theme

**Question 5** (ask alone, one message):
> "Agrupe os achados por tema. Para cada tema: qual o insight, qual a evidencia que o sustenta, qual a causa provavel, e qual a implicacao para produto?"

Wait for the answer. For each theme:
- If cause is asserted without evidence: "Is this a confirmed cause or a hypothesis?"
- If implication is missing: "So what? What does this mean for the product decision?"

### Block 6: Personas/JTBD

**Question 6** (ask alone, one message):
> "Identificamos personas ou JTBD? Se sim, para cada uma: qual o job principal, qual a dor principal, e qual o criterio de sucesso?"

Wait for the answer. This block is optional — if no personas emerged, note it and move on.

### Block 7: Hypotheses

**Question 7** (ask alone, one message):
> "Quais hipoteses emergiram? Use o formato: 'Se [acao], entao [resultado esperado], medido por [metrica], de [[baseline]] para [[meta]].'"

Wait for the answer. For each hypothesis:
- Ensure it has a measurable target: "What's the baseline for this metric?"
- Ensure it's testable: "How would we know if this hypothesis is wrong?"

### Block 8: Uncertainties

**Question 8** (ask alone, one message):
> "O que ainda e incerto? Classifique: Tier 1 = bloqueia decisao (precisa de responsavel e data), Tier 2 = nao bloqueia mas melhora qualidade."

Wait for the answer. For each Tier 1 uncertainty, ensure there's a responsible person and date.

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/discovery/discovery-report.md` contains:

- **Header**: Title, version, date, owner, contributors, discovery period, main links
- **1. Objetivo do discovery**: Which decision this discovery enables (3-5 lines)
- **2. Perguntas de pesquisa**: Q1, Q2, Q3... (what we wanted to answer)
- **3. Metodo e amostra**:
  - Fontes qualitativas (entrevistas: N, perfis, duracao, script)
  - Fontes quantitativas (dados analisados, periodo, segmentacoes)
  - Outras fontes (tickets/CS, incidentes/logs, docs tecnicos)
- **4. Contexto resumido**: Scenario before discovery (from baseline)
- **5. Evidencias-chave**: 5-10 items, each with fonte/link
- **6. Achados e insights por tema**: Theme N → insight + evidencias + causa provavel + implicacao para produto
- **7. Personas/JTBD** (when applicable): Job principal, dor principal, criterio de sucesso
- **8. Mapa de dores** (sintomas vs causas): Observed symptoms + probable causes (hypotheses with evidence)
- **9. Hipoteses emergentes** (H-# IDs): Se [...], entao [...], medido por [...], de [[baseline]] para [[meta]]
- **10. Incertezas e lacunas remanescentes**: Tier 1 (blocks decision) with responsible + date; Tier 2 (improves quality)
- **11. Recomendacoes e proximos passos**: What this report unlocks
- **12. Links e anexos**: Dashboards, recordings, prints, other docs

**SST Rule:** Discovery evidence, method/sample, and insights by theme ONLY in this document. No other document should redefine the evidence base or insight synthesis.

## ID GENERATION

**H-# Pattern**: Hypotheses. Format: `H-1`, `H-2`, `H-3`. Each H must:
- Follow the format: "Se [action], entao [expected result], medido por [metric], de [baseline] para [target]"
- Be testable and falsifiable
- Reference a baseline metric when possible

Downstream traceability: `H-# → O-# opportunities in ost.md (insights become opportunities)`

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the discovery report document template and structure.

## INPUT VALIDATION

**baseline.md** (BLOCKS):
- Must contain at least 1 metric area (A-D) with baseline data
- Must have Fluxo AS-IS section

**project-context.md** (BLOCKS):
- Must contain: `## WHAT`, `## WHO`, `## WHY` sections (or equivalent)
- Minimum length: 40 lines (a real interview, not a stub)

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Objetivo do discovery states which decision the report enables
- [ ] At least 3 research questions (Q1, Q2, Q3) documented
- [ ] Method and sample section describes at least 1 qualitative OR 1 quantitative source with details
- [ ] At least 5 key evidence items listed with fonte/link
- [ ] At least 2 themes with insights, evidence, and product implications
- [ ] Each insight clearly labeled as fact, hypothesis, or interpretation
- [ ] At least 1 hypothesis (H-#) with measurable baseline → target format
- [ ] Incertezas section separates Tier 1 (blocking) from Tier 2 (non-blocking)
- [ ] Tier 1 uncertainties have responsible person + date
- [ ] Source Documents section present at top referencing baseline.md and project-context.md

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
discovery-report.md saved to `docs/ets/projects/{project-slug}/discovery/discovery-report.md`

Status: [COMPLETE | DRAFT]
Research questions: [count]
Key evidence items: [count]
Themes with insights: [count]
Hypotheses (H-#): [count]
Tier 1 uncertainties: [count] | Tier 2: [count]
```

Then present these options using AskUserQuestion (or as a numbered list if AskUserQuestion is unavailable):

1. **Proceed to Product Vision (Recommended)** — Use evidence to inform vision targets and guardrails (if vision not done yet)
2. **Proceed to OST** — Transform insights into structured opportunities (if vision already exists)
3. **Refine this document** — Review and improve specific sections (e.g., add evidence, clarify hypotheses)
4. **Pause for now** — Save and return later (the document is already on disk)

Wait for the user to choose before taking any action. Do not auto-proceed to the next skill.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `baseline.md` (BLOCKS), `project-context.md` (BLOCKS), optionally `product-vision.md` (ENRICHES)
- **Action:** Extract baseline metrics, scope context, BO-# objectives (if available). Summarize key points to the user to show you've absorbed the context.
- **Output:** Internal context object

### Step 2: Pressure Test
- **Input:** Step 1 context
- **Action:** Challenge the evidence foundation with 1-2 pressure test questions. Verify that discovery has sufficient breadth (sources) and depth (evidence per theme).
- **Output:** Validated/refined framing

### Step 3: Discovery Report Interview (one question at a time)
- **Input:** Step 1-2 context + user responses (interactive)
- **Action:** Run the 8-block INTERVIEW PROTOCOL. Ask one question per message, wait for answers. For each evidence item, ensure source is present. Flag anti-patterns actively.
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
  - Objetivo do discovery
  - Perguntas de pesquisa
  - Metodo e amostra
  - Contexto resumido
  - Evidencias-chave
  - Achados e insights — Tema 1
  - Achados e insights — Tema 2
  - ... (repeat for each theme)
  - Personas/JTBD (if applicable)
  - Mapa de dores
  - Hipoteses emergentes
  - Incertezas e lacunas remanescentes
  - Recomendacoes e proximos passos
  - Links e anexos
- **Output:** Approved sections assembled into complete discovery-report.md

### Step 5: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is a small/local improvement (P2) and the document has unnecessary sections → trim empty or boilerplate sections, offer "versao curta"
  - If this is a P0/P1 initiative and evidence is thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 6: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline (product-vision or OST) still have to invent if this document is all they get?
  2. Do any insight claims lack supporting evidence?
  3. Are there hypotheses without measurable targets?
  4. Is there a low-effort addition (e.g., one more evidence source, one clarification) that would significantly improve the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 7: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/discovery/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/discovery/discovery-report.md` using the Write tool
  3. The document is only saved when written to the filesystem — presenting content in chat is not the same as saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review
- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/discovery/discovery-report.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/discovery/baseline.md`, `docs/ets/projects/{project-slug}/discovery/project-context.md`)
  2. The reviewer checks: completeness, evidence quality, hypothesis measurability, fact/hypothesis/interpretation labeling, SST compliance
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Output:** Reviewed and approved document

### Step 9: User Review Gate
- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/discovery/discovery-report.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
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
| BLOCKS dep missing (baseline.md) | Critical | Auto-invoke baseline skill — evidence needs baseline metrics | Pause until baseline is available |
| BLOCKS dep missing (project-context.md) | Critical | Auto-invoke project-context skill — scope context is needed | Pause until project-context is available |
| BLOCKS dep is DRAFT | Warning | Proceed with available context, noting evidence may be weaker | Add `<!-- ENRICHMENT_MISSING: [doc] is DRAFT -->` |
| ENRICHES dep missing (product-vision.md) | Low | Proceed — report can be built without vision targets | Note that report may need revision after vision is defined |
| User cannot provide evidence for a theme | Medium | Mark theme as `[[evidencia a coletar]]` with collection plan | Add to Tier 1 gaps if critical, Tier 2 if not |
| All evidence is qualitative only | High | Escalate: "All evidence is qualitative — consider adding quantitative data before proceeding to OST" | Mark as DRAFT, add data collection to recommendations |
| Hypotheses lack measurable targets | High | Push for baseline → target format | Mark hypotheses as `<!-- INCOMPLETE: needs baseline/target -->` |
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
