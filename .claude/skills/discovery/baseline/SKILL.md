---
name: baseline
description: >
  Use when establishing the current state of metrics, funnels, and data quality
  before a discovery or feature decision. Also triggers on 'baseline', 'current state',
  'dados e contexto', 'funnel metrics', 'what are the numbers today', or 'AS-IS'.
model: opus
version: 1.0.0
argument-hint: "[context-path]"
compatibility: "Optional: Slack MCP (pull metric discussions), external issue tracker adapter (for example, Linear) for incident tickets"
---

## PURPOSE

Establish the quantitative and qualitative "before" picture of a product initiative: current funnels, metric baselines with source and confidence, data quality, operational effort, segmentations, and information gaps. This document prevents "gut-feeling" decisions and guarantees that post-launch impact can be measured objectively (before vs after). It is a reference document, not a requirements document — it captures the current state, not what should change.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Needed to know which product/initiative and which decision this baseline informs.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Metric targets from the vision help focus which baselines to capture.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `baseline.requires: [project-context]`
2. Check: does `docs/ets/projects/{project-slug}/discovery/project-context.md` exist, is non-empty, and is not `<!-- STATUS: DRAFT -->`?
3. If missing → INFORM user → auto-invoke `project-context` skill → wait → continue
4. If DRAFT → WARN: "project-context.md is DRAFT — baseline scope may be less clear" → proceed
5. Check if `product-vision.md` exists → if yes, load metric targets to focus baseline capture → if no, WARN and proceed

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest data sources, challenge confidence levels, propose segmentation angles, and flag when stated numbers may be incomplete or misleading. Baseline work is analytical and evidence-driven — these patterns ensure the user feels supported in building an honest picture, not interrogated.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Baseline questions often require the user to look up data, so give them space. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., which funnel stages to track, which segmentation angles matter, confidence level), present 3-4 concrete options with a brief description of each. Highlight your recommendation. Let the user pick before proceeding.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs. Example: "I see three ways to structure the AS-IS flow: (A) user journey — step by step from the user's perspective, (B) system flow — data movement across systems and integrations, (C) hybrid — user steps with system touchpoints annotated. I recommend C because it captures both the user experience and where data breaks happen."

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section (e.g., AS-IS Flow, then Metrics A, then Metrics B, etc.), ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Tier 1 (blocks)** — This must be resolved before advancing. Add to Lacunas section with responsible + date.
   - **Tier 2 (improves)** — Important but not blocking. Add to Lacunas section.
   - **Deferred to [phase name]** — Noted and carried forward.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options instead of a single fixed path.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing baseline.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

8. **Assess if full process is needed (right-size check)** — If the user's input already has detailed metrics with sources and confidence levels, don't force the full interview. Confirm understanding briefly and offer to skip directly to document generation. Only run the full interactive process when there's genuine ambiguity or missing data to resolve.

9. **Thinking partner behaviors:**
   - When the user shares a metric, ask "Where does this number come from? How confident are you — alta, media, or baixa?"
   - When confidence is baixa, suggest verification methods: "Could we cross-check this against [analytics tool / CRM / logs]?"
   - When a funnel stage is described, probe for drop-off: "What happens to the users who don't make it past this step?"
   - When data is missing, don't just record the gap — propose a collection plan: "To get this, we could [approach A / approach B]."

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

## CONTEXT LOADING

Load context in this order of priority:

1. **$ARGUMENTS**: If the user passes `[context-path]`, read that file directly.
2. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for any upstream discovery artifacts.
3. **Document Scan**: Scan `docs/ets/projects/{project-slug}/discovery/` for existing project-context.md, product-vision.md, or baseline fragments.
4. **User Interview**: If nothing found, begin the baseline interviews interactively.

## INTERVIEW PROTOCOL

This interview follows a one-question-at-a-time rhythm. Ask each question alone in one message, wait for the user's answer, then decide whether to ask a follow-up or move forward.

### Block 1: Scope & Decision

**Question 1** (ask alone, one message):
> "Qual produto/iniciativa estamos documentando e qual decisao este baseline vai informar? (Ex.: priorizar oportunidades, definir escopo de discovery, medir impacto de uma mudanca)"

Wait for the answer. Extract: product name, initiative scope, the decision this baseline serves.

### Block 2: AS-IS Flow

**Question 2** (ask alone, one message):
> "Descreva o fluxo atual (AS-IS) — o que o usuario faz passo a passo hoje? Inclua integracoes e sistemas se souber."

Wait for the answer. Then probe:

**Follow-up probes** — ask one at a time only if needed:
- If integrations unclear: "Quais sistemas/ferramentas estao envolvidos nesse fluxo? (CRM, analytics, APIs, planilhas)"
- If failure points unclear: "Onde esse fluxo quebra ou degrada? Quais sao os pontos de falha conhecidos?"

### Block 3: Metrics Baseline

**Question 3** (ask alone, one message):
> "Quais metricas voce tem hoje para esse fluxo? Vamos cobrir 4 areas: (A) Aquisicao e funil, (B) Qualidade de dados, (C) Performance e confiabilidade, (D) Operacao. Comece pela area que voce tem mais dados."

Wait for the answer. For each metric shared, immediately ask:

**Question 4** (ask for each metric area, one at a time):
> "Para essas metricas: qual o periodo analisado, de onde vem o dado (fonte), e qual a confiabilidade — alta (fonte confiavel, recorte limpo), media (fonte ok mas recorte impreciso), ou baixa (estimativa/achismo)?"

Repeat Q3-Q4 cycle for each of the 4 metric areas (A through D) that apply.

**Every metric field must include:** valor, periodo, fonte, confiabilidade (alta/media/baixa).

### Block 4: Segmentations

**Question 5** (ask alone, one message):
> "Quais segmentacoes sao relevantes para esta analise? Exemplos: por canal (organico/pago/direto), por device (mobile/desktop), por coorte (novo vs recorrente), por tipo de cliente. Quais fazem diferenca nos numeros?"

### Block 5: Constraints & Pain Points

**Question 6** (ask alone, one message):
> "Quais restricoes existem? Pense em 4 dimensoes: (1) Tecnica, (2) Legal/LGPD, (3) Operacao, (4) Time/capacidade. E quais premissas estamos assumindo como verdadeiras?"

Wait for the answer. Then ask:

**Question 7** (ask alone, one message):
> "Quais problemas e dores ja foram observados nesse fluxo? Liste como fatos/observacoes com evidencia — sem propor solucao (isso vem no Discovery/OST)."

### Block 6: Information Gaps

**Question 8** (ask alone, one message):
> "Quais dados faltam que sao criticos para a decisao? Classifique: Tier 1 = bloqueia avanco (precisa antes de seguir), Tier 2 = melhora a analise mas nao bloqueia. Para cada Tier 1, quem vai buscar e quando?"

After the user answers, propose a collection plan:
> "Para coletar os dados faltantes, sugiro: [entrevistas / analytics / logs / CRM / BI]. Faz sentido?"

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/discovery/baseline.md` contains:

- **Header**: Title, version, date, owner, contributors, period analyzed, main sources
- **1. Objetivo do documento**: Which decision this baseline informs (3-5 lines)
- **2. Escopo**: In scope / Out of scope
- **3. Contexto do negocio**: Why now (business pressure, migration, growth, risk, opportunity)
- **4. Fluxo atual (AS-IS)**: 6-12 bullet step-by-step + integrations + failure points
- **5. Baseline de metricas (antes)**:
  - A) Aquisicao e funil (volume, conversion rates, CAC/CPL, RPL)
  - B) Qualidade de dados (valid/invalid leads, duplicates, integration failure rate)
  - C) Performance e confiabilidade (latency p50/p95, error rate, recent incidents)
  - D) Operacao (hours/week rework, manual tasks, operational impacts)
- **6. Segmentacoes relevantes**: By channel, device, cohort, client type
- **7. Restricoes, premissas e dependencias**: Assumptions, constraints (technical, legal/LGPD, operational, capacity), dependencies
- **8. Problemas e dores ja observadas**: Facts/observations with evidence, no proposed solutions
- **9. Lacunas de informacao e plano de coleta**:
  - Tier 1 (blocks advancement) with responsible + date
  - Tier 2 (important but not blocking)
  - Collection plan (interviews, analytics, logs, CRM/BI)
- **10. Links e anexos**: Dashboards, spreadsheets, tickets/incidents, technical docs

**SST Rule:** Baseline metrics (before state) ONLY in this document. No other document should redefine the current state.

**IDs:** No formal IDs. This is a data reference document, not a requirements document.

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the baseline document template and structure.

## INPUT VALIDATION

**project-context.md** (BLOCKS):
- Must contain: `## WHAT`, `## WHO`, `## WHY` sections (or equivalent)
- Minimum length: 40 lines (a real interview, not a stub)
- Must identify the product/initiative being analyzed

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Objetivo do documento states which decision the baseline informs
- [ ] Escopo clearly defines what is in/out of scope
- [ ] Fluxo AS-IS has at least 6 steps with systems/integrations identified
- [ ] At least 2 of the 4 metric areas (A-D) have data with valor + periodo + fonte + confiabilidade
- [ ] Every metric includes confiabilidade rating (alta/media/baixa)
- [ ] At least 1 segmentation dimension documented
- [ ] Restricoes section covers at least 2 of the 4 dimensions (tecnica, legal, operacao, capacidade)
- [ ] Lacunas section separates Tier 1 (blocking) from Tier 2 (non-blocking)
- [ ] Collection plan exists for Tier 1 gaps with responsible + date
- [ ] Source Documents section present at top referencing project-context.md

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
baseline.md saved to `docs/ets/projects/{project-slug}/discovery/baseline.md`

Status: [COMPLETE | DRAFT]
Metric areas covered: [list which of A/B/C/D have data]
Tier 1 gaps: [count] | Tier 2 gaps: [count]
```

Then present these options using AskUserQuestion (or as a numbered list if AskUserQuestion is unavailable):

1. **Proceed to Product Vision (Recommended)** — Use baseline metrics to inform vision targets and guardrails
2. **Proceed to Discovery Gate** — If product-vision already exists, validate discovery artifacts
3. **Refine this document** — Review and improve specific sections (e.g., fill Tier 1 gaps)
4. **Pause for now** — Save and return later (the document is already on disk)

Wait for the user to choose before taking any action. Do not auto-proceed to the next skill.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `project-context.md` (BLOCKS), optionally `product-vision.md` (ENRICHES)
- **Action:** Extract product/initiative scope, stakeholders, constraints, tech stack. If product-vision exists, extract metric targets to focus baseline capture. Summarize key points to the user.
- **Output:** Internal context object

### Step 2: Baseline Interview (one question at a time)
- **Input:** Step 1 context + user responses (interactive)
- **Action:** Run the 6-block INTERVIEW PROTOCOL. Ask one question per message, wait for answers. For every metric, ensure valor + periodo + fonte + confiabilidade are captured.
- **Output:** Raw interview notes (internal)

### Step 3: Section-by-Section Document Generation
- **Input:** Interview notes from Step 2
- **Action:** Generate the document one major section at a time, using the template from `knowledge/template.md`. For each section:
  1. **Propose approach** — Before generating, briefly describe how you plan to frame this section
  2. **Generate the section** — Present it to the user
  3. **Ask for approval** — "Does this capture it well? Anything to adjust?"
  4. **Incorporate feedback** — If the user wants changes, revise and re-present
  5. **Move to next section** — Only after the user approves

  Section order:
  - Objetivo do documento
  - Escopo
  - Contexto do negocio
  - Fluxo atual (AS-IS)
  - Baseline de metricas — A) Aquisicao e funil
  - Baseline de metricas — B) Qualidade de dados
  - Baseline de metricas — C) Performance e confiabilidade
  - Baseline de metricas — D) Operacao
  - Segmentacoes relevantes
  - Restricoes, premissas e dependencias
  - Problemas e dores ja observadas
  - Lacunas de informacao e plano de coleta
  - Links e anexos
- **Output:** Approved sections assembled into complete baseline.md

### Step 4: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is a small/local improvement (P2) and the document has unnecessary sections → trim empty or boilerplate sections, offer "versao curta"
  - If this is a P0/P1 initiative and metric areas are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 5: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline (product-vision or OST) still have to invent if this document is all they get?
  2. Do any metric claims lack source or confidence rating?
  3. Are there Tier 1 gaps without a responsible person and date?
  4. Is there a low-effort addition (e.g., one more segmentation, one more metric source) that would significantly improve the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 6: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/discovery/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/discovery/baseline.md` using the Write tool
  3. The document is only saved when written to the filesystem — presenting content in chat is not the same as saving.
- **Output:** File written to disk at the specified path

### Step 7: Spec Review
- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/discovery/baseline.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/discovery/project-context.md`)
  2. The reviewer checks: completeness, consistency, metric source/confidence coverage, Tier 1 gap accountability, SST compliance
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Output:** Reviewed and approved document

### Step 8: User Review Gate
- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/discovery/baseline.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Output:** User-approved document

### Step 9: Validation
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT

### Step 10: Handoff Options
- **Action:** Present multiple next-step options (see CLOSING SUMMARY)

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (project-context.md) | Critical | Auto-invoke project-context skill — scope context is needed | Pause until project-context is available |
| BLOCKS dep is DRAFT | Warning | Proceed with available context, noting scope may be unclear | Add `<!-- ENRICHMENT_MISSING: project-context is DRAFT -->` |
| ENRICHES dep missing (product-vision.md) | Low | Proceed — baseline can be built without vision targets | Note that baseline may need revision after vision is defined |
| User cannot provide metrics for an area | Medium | Mark area as `[[a coletar]]` with collection plan | Add to Tier 1 gaps if critical, Tier 2 if not |
| All metrics have baixa confidence | High | Escalate: "All metrics are low confidence — consider running a data audit before proceeding" | Mark as DRAFT, add data audit to collection plan |
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
