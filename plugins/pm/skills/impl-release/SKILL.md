---
name: impl-release
description: >
  Use when planning a production release with rollout strategy, monitoring,
  rollback plan, and stakeholder communication. Also triggers on 'release plan',
  'rollout plan', 'go-live', 'launch plan', 'how to deploy', 'rollback plan',
  or 'post-release monitoring'.
model: sonnet
version: 1.0.0
argument-hint: "[context-path]"
compatibility: "Optional: external issue tracker adapter (for example, Linear) for release ticket context, Slack MCP (coordinate communication channels)"
---

## PURPOSE

Plan a safe, measurable production release: rollout strategy (full/progressive/canary/beta/feature flag), go/no-go checklist, success and guardrail metrics with dashboards, monitoring ritual (who watches for how long), rollback plan with specific triggers and procedure, stakeholder communication (internal + external), and post-release validation. This document ensures that "launching" is not just "deploying" — it is operating with intention. It reduces regression risk and guarantees objective impact reading.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/implementation/implementation-plan.md` — Need to know what is being released (scope, stories, timeline).
- `docs/ets/projects/{project-slug}/implementation/quality-checklist.md` — Quality gates must be defined before release.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — NFR targets inform monitoring thresholds.
- `docs/ets/projects/{project-slug}/planning/prd.md` — Success metrics from PRD inform post-release validation.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `release-plan.requires: [implementation-plan, quality-checklist]`
2. Check: do `docs/ets/projects/{project-slug}/implementation/implementation-plan.md` and `docs/ets/projects/{project-slug}/implementation/quality-checklist.md` exist, are non-empty, and are not `<!-- STATUS: DRAFT -->`?
3. If implementation-plan missing → INFORM user → auto-invoke `implementation-plan` skill → wait → continue
4. If quality-checklist missing → INFORM user → auto-invoke `quality-checklist` skill → wait → continue
5. If either is DRAFT → WARN: "[document] is DRAFT — release plan may have gaps in scope or quality criteria" → proceed
6. If tech-spec.md exists → load NFR targets for monitoring thresholds
7. If prd.md exists → load success metrics for post-release validation

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest rollout strategies based on risk profile, propose monitoring thresholds from NFR targets, challenge weak rollback plans, and help the user think through communication needs. Release planning is operational and risk-driven — these patterns ensure the user builds a plan that can actually be executed, not a checkbox document.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Release questions often require coordination with engineering and ops, so give the user space. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., rollout strategy, monitoring duration, rollback triggers), present 3-4 concrete options with a brief description of each. Highlight your recommendation based on the risk profile. Let the user pick before proceeding.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs. Example: "Based on the risk profile (P0 initiative, integration changes, funnel impact), I see three rollout strategies: (A) Feature flag with 5% → 20% → 50% → 100% ramp — safest, slower feedback, (B) Canary with 10% for 24h then full — faster, needs good monitoring, (C) Full release with kill switch — fastest, riskiest. I recommend A because of the integration changes."

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section (Rollout Strategy, then Go/No-Go Checklist, then Metrics, etc.), ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Resolve before go-live** — This blocks the release. Keep asking until resolved.
   - **Deferred to post-release** — Can be addressed after launch.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options instead of a single fixed path.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing release-plan.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

8. **Assess if full process is needed (right-size check)** — If the release is low-risk (small change, no integrations, no funnel impact), don't force the full interview. Offer a "versao curta" with just: scope, basic metrics, simple rollback, and communication. Only run the full interactive process for P0/P1 releases with meaningful risk.

9. **Thinking partner behaviors:**
   - When rollout strategy is "full release" for a risky change: "This change touches [integrations/funnel/data]. Are you sure full release is the right strategy? A progressive rollout with feature flags would give us an escape hatch."
   - When rollback plan is vague: "If something goes wrong at 2 AM, who does what? Let's make this executable: step 1 disable flag, step 2 verify, step 3 communicate."
   - When metrics lack thresholds: "At what point do we consider this a problem? Let's set specific numbers: conversion drops >X%, errors >Y%, latency p95 >Zms."
   - When communication plan is missing: "Who will be surprised if this goes live without warning? Those are the people we need to communicate to."

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
2. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for upstream implementation artifacts.
3. **Document Scan**: Scan `docs/ets/projects/{project-slug}/implementation/` for implementation-plan.md and quality-checklist.md. Scan `docs/ets/projects/{project-slug}/architecture/` for tech-spec.md. Scan `docs/ets/projects/{project-slug}/planning/` for prd.md.
4. **User Interview**: If nothing found, begin the release plan interviews interactively.

## INTERVIEW PROTOCOL

This interview follows a one-question-at-a-time rhythm. Ask each question alone in one message, wait for the user's answer, then decide whether to ask a follow-up or move forward.

### Block 1: Release Scope

**Question 1** (ask alone, one message):
> "O que esta sendo released? Descreva o escopo (o que inclui e o que NAO inclui) e compartilhe links para PRD/backlog/epico."

Wait for the answer. Extract: scope, links, risk profile.

**Follow-up** (ask alone, one message, if risk is unclear):
> "Qual o nivel de risco deste release? Considere: (1) impacto em funil/conversao/receita, (2) mudancas em integracoes, (3) alteracoes de schema/dados, (4) impacto operacional. Isso nos ajuda a escolher a estrategia de rollout."

### Block 2: Rollout Strategy

**Question 2** (ask alone, one message):
> "Qual a estrategia de rollout? Baseado no perfil de risco, sugiro estas opcoes:
>
> 1. **Full release** — 100% de uma vez. Mais rapido, maior risco. Bom para mudancas de baixo risco.
> 2. **Progressivo (ramp-up)** — 5% → 20% → 50% → 100%. Mais seguro, feedback gradual. Bom para mudancas de medio risco.
> 3. **Canario** — Grupo pequeno (5-10%) por 24h, depois expandir. Bom para validar estabilidade.
> 4. **Feature flag** — Toggle configuravel, ramp-up por segmento. Mais controle, rollback instantaneo. Bom para mudancas de alto risco.
>
> Recomendo **[opcao]** porque **[razao baseada no risco]**. Qual prefere?"

Wait for the answer. Then ask configuration details:
> "Para a estrategia escolhida: qual o nome da feature flag (se aplicavel)? Qual segmento inicial? Qual criterio para avancar de etapa?"

### Block 3: Metrics & Monitoring

**Question 3** (ask alone, one message):
> "Quais metricas definem sucesso para este release? Pense em 3 categorias:
> (A) **Metricas de sucesso (outcome)** — o que esperamos melhorar (baseline → meta → janela)
> (B) **Guardrails** — o que NAO pode piorar (com threshold especifico)
> (C) **Metricas operacionais** — erros, latencia, tickets"

Wait for the answer. Then ask:

**Question 4** (ask alone, one message):
> "Quem monitora nas primeiras 24-72h? Precisamos de: responsavel de Produto, Engenharia, Data, e Operacao/CS. Qual o canal de comunicacao (Slack/Teams) e qual o ritual (janela intensiva + acompanhamento diario)?"

### Block 4: Rollback

**Question 5** (ask alone, one message):
> "O que dispara rollback? Vamos definir gatilhos especificos:
> - Queda de conversao > [X%] por [Y horas]?
> - Erros > [X%] ou incidentes criticos?
> - p95 > [X ms] por [Y min]?
> - Tickets criticos > [N] em [Y horas]?
>
> Quem decide o rollback? (PM + Tech Lead + backup)"

Wait for the answer. Then ask:
> "Qual o procedimento de rollback? Sugiro 4 passos: (1) desabilitar flag/reverter deploy, (2) validar estabilizacao, (3) comunicar stakeholders, (4) abrir incidente/post-mortem. Faz sentido ou precisa ajustar?"

### Block 5: Communication

**Question 6** (ask alone, one message):
> "Quem precisa ser comunicado sobre este release?
> **Interno:** CS, Suporte, Growth, Vendas, Ops, Lideranca — quais se aplicam?
> **Externo (se aplicavel):** usuarios/clientes via in-app, email, changelog?
>
> Para cada publico, precisamos definir: o que mudou, quem e impactado, como agir se houver problema, onde acompanhar metricas."

### Block 6: Post-Release Validation

**Question 7** (ask alone, one message):
> "Como validamos o sucesso apos o release?
> - **Curto prazo (24-72h):** o que olhamos?
> - **Medio prazo (1-2 semanas):** o que confirma sucesso?
> - **Criterio para 'considerar sucesso':** quais metricas precisam estar ok?
> - **Acoes apos release:** learnings, bugs, docs, comunicar resultados"

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/implementation/release-plan.md` contains:

- **Header**: Title, version, date, owner (PM), co-owner (Tech Lead), monitoring participants, status, links (PRD, backlog, dashboards, feature flag, runbook)
- **1. Resumo do release**: What, for whom, why, main risks, how we measure success (5-8 lines)
- **2. Escopo do release**: Includes / Does not include
- **3. Estrategia de rollout**: Type (full/progressive/canary/beta/feature flag) + configuration (flag name, initial segment, ramp-up %, advancement criteria)
- **4. Checklist pre-release (go/no-go)**:
  - Technical requirements (build, migrations, observability, flag, rollback tested)
  - Product requirements (acceptance criteria, UX validated, tracking validated)
  - Operational requirements (CS informed, processes updated, communication ready)
  - Go/no-go decision (date, responsible, decision, justification)
- **5. Metricas e monitoramento**:
  - A) Success metrics (outcome) with baseline → target → window
  - B) Guardrails (cannot worsen) with thresholds
  - C) Operational metrics (error rate, latency, tickets, response time)
  - Dashboards (links)
- **6. Plano de monitoramento (24-72h)**: Ritual (intensive window + daily follow-up), responsible (product, eng, data, ops), channel (Slack/Teams)
- **7. Plano de rollback**: Triggers (specific thresholds), decision-makers (PM + Tech Lead + backup), procedure (4 steps: disable → verify → communicate → post-mortem)
- **8. Plano de comunicacao**: Internal (audience, channel, message: what changed, who impacted, how to act, where to track) + External (if applicable: audience, channel, content)
- **9. Validacao pos-release e encerramento**: Evaluation window (short + medium term), success criteria, post-release actions (learnings, bugs, docs, communicate results)

**SST Rule:** Rollout strategy, rollback plan, and monitoring metrics ONLY in this document. No other document should redefine release operations.

**IDs:** No formal IDs. This is an operational document, not a requirements document.

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the release plan document template and structure.

## INPUT VALIDATION

**implementation-plan.md** (BLOCKS):
- Must contain: release scope or sprint plan with stories
- Must identify what is being released

**quality-checklist.md** (BLOCKS):
- Must contain: quality gates or acceptance criteria checklist
- Must have at least 3 checklist items

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Resumo do release describes what, for whom, why, risks, and success metrics
- [ ] Escopo clearly defines what is included and not included
- [ ] Rollout strategy is explicit (type + configuration)
- [ ] Go/no-go checklist has at least 3 technical, 2 product, and 2 operational items
- [ ] At least 2 success metrics with baseline → target → window
- [ ] At least 1 guardrail with specific threshold
- [ ] Monitoring plan names responsible people and specifies ritual duration
- [ ] Rollback triggers have specific numeric thresholds (not vague "if something goes wrong")
- [ ] Rollback procedure has at least 3 actionable steps
- [ ] Communication plan identifies at least internal audiences
- [ ] Post-release validation defines evaluation windows and success criteria
- [ ] Source Documents section present at top referencing implementation-plan.md and quality-checklist.md

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
release-plan.md saved to `docs/ets/projects/{project-slug}/implementation/release-plan.md`

Status: [COMPLETE | DRAFT]
Rollout strategy: [type]
Go/no-go items: [count]
Rollback triggers: [count]
```

Then present these options using AskUserQuestion (or as a numbered list if AskUserQuestion is unavailable):

1. **Execute go/no-go review** — Walk through the checklist with the team to make the GO/NO-GO decision
2. **Refine this document** — Review and improve specific sections (e.g., add more rollback triggers, refine communication)
3. **Return to quality-checklist** — If quality gates need updating before release
4. **Pause for now** — Save and return later (the document is already on disk)

Wait for the user to choose before taking any action. Do not auto-proceed to the next skill.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `implementation-plan.md` (BLOCKS), `quality-checklist.md` (BLOCKS), optionally `tech-spec.md` (ENRICHES), `prd.md` (ENRICHES)
- **Action:** Extract release scope, quality gates, NFR targets, success metrics. Assess risk profile. Summarize key points to the user.
- **Output:** Internal context object with risk assessment

### Step 2: Release Interview (one question at a time)
- **Input:** Step 1 context + user responses (interactive)
- **Action:** Run the 6-block INTERVIEW PROTOCOL. Ask one question per message, wait for answers. For rollout strategy, propose options based on risk profile. For rollback, insist on specific thresholds.
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
  - Resumo do release
  - Escopo do release
  - Estrategia de rollout
  - Checklist pre-release (go/no-go)
  - Metricas e monitoramento
  - Plano de monitoramento (24-72h)
  - Plano de rollback
  - Plano de comunicacao
  - Validacao pos-release e encerramento
- **Output:** Approved sections assembled into complete release-plan.md

### Step 4: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the release's risk:
  - If this is a low-risk release (small change, no integrations) → offer "versao curta" with just: scope, basic metrics, simple rollback, and communication
  - If this is a P0/P1 release with integration changes → ensure all sections are thorough
  - Low-risk releases deserve a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 5: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. Could an on-call engineer execute the rollback procedure at 2 AM with just this document?
  2. Are all rollback triggers numeric and actionable (not "if something goes wrong")?
  3. Is every stakeholder who would be surprised by this release included in the communication plan?
  4. Are dashboards linked (not just mentioned)?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 6: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/implementation/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/implementation/release-plan.md` using the Write tool
  3. The document is only saved when written to the filesystem — presenting content in chat is not the same as saving.
- **Output:** File written to disk at the specified path

### Step 7: Spec Review
- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/implementation/release-plan.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/implementation/implementation-plan.md`, `docs/ets/projects/{project-slug}/implementation/quality-checklist.md`)
  2. The reviewer checks: completeness, rollback executability, threshold specificity, communication coverage, SST compliance
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Output:** Reviewed and approved document

### Step 8: User Review Gate
- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/implementation/release-plan.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
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
| BLOCKS dep missing (implementation-plan.md) | Critical | Auto-invoke implementation-plan skill — need to know what's being released | Pause until implementation-plan is available |
| BLOCKS dep missing (quality-checklist.md) | Critical | Auto-invoke quality-checklist skill — quality gates must exist before release | Pause until quality-checklist is available |
| BLOCKS dep is DRAFT | Warning | Proceed with available context, noting scope/quality gaps | Add `<!-- ENRICHMENT_MISSING: [doc] is DRAFT -->` |
| ENRICHES dep missing (tech-spec.md) | Low | Proceed — ask user for NFR targets directly | Note that monitoring thresholds may need revision |
| ENRICHES dep missing (prd.md) | Low | Proceed — ask user for success metrics directly | Note that post-release validation may need revision |
| Rollback triggers are vague | High | Push for specific numbers: "At exactly what threshold do we rollback?" | Do not proceed until at least 2 triggers have numeric thresholds |
| No monitoring responsible named | High | Push: "Who watches the dashboards after go-live? We need names, not roles." | Mark as DRAFT until people are assigned |
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
