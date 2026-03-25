---
title: "feat: Align skills with ETUS team process (3 new skills + template updates)"
type: feat
status: active
date: 2026-03-17
origin: Google Drive folder — ETUS product team templates and process documentation
---

# Align ETUS PMDocs with Team Process

## Overview

The ETUS product team uses an 8-document process (Visao → Baseline → Discovery → OST → Priorizacao → PRD → Backlog → Release). ETUS PMDocs v5 covers 5 of these 8 well, but is missing 3 critical documents and has gaps in the existing templates. This plan creates the 3 missing skills and updates 4 existing templates to match the team's real workflow.

## Problem Statement

The team has a well-defined, evidence-based process documented in Google Drive. The plugin doesn't match it:
- **Baseline document** (Dados & Contexto) has no skill — the team can't generate their #2 most important document
- **OST** (Opportunity Solution Tree) has no skill — the team can't structure discovery into prioritizable opportunities
- **Release/Rollout plan** has no skill — the team can't document go-live strategy, rollback, and monitoring
- Existing skills (product-vision, prd, user-stories) are close but miss team-specific sections

## Proposed Solution

3 new skills + 4 template updates + workflow integration.

## Acceptance Criteria

- [ ] `baseline` skill generates `docs/ets-docs/discovery/baseline.md` with: funil AS-IS, metricas com fonte/confiabilidade, segmentacoes, lacunas Tier 1/2, plano de coleta
- [ ] `ost` skill generates `docs/ets-docs/planning/ost.md` with: outcome → oportunidades com evidencia → solucoes candidatas → assumptions → experiments
- [ ] `release-plan` skill generates `docs/ets-docs/implementation/release-plan.md` with: estrategia rollout, go/no-go checklist, metricas, rollback, comunicacao, validacao pos-release
- [ ] All 3 new skills follow ETUS v5 patterns (INTERACTION PROTOCOL, ARTIFACT SAVE RULE, spec review, user review gate, CLOSING SUMMARY)
- [ ] `product-vision` template updated with: principios do produto, anti-objetivos, guardrails separados
- [ ] `prd` template updated with: eventos/tracking, rollout alto nivel, requisitos nao-funcionais explicitos
- [ ] `user-stories` template updated with: DoR, DoD, itens de qualidade (observabilidade, tracking, testes)
- [ ] Orchestrator updated: baseline after project-context, OST after discovery report, release-plan after quality-checklist
- [ ] Dependency graph updated with 3 new skills
- [ ] CLAUDE.md updated with new doc count and workflow

---

## Implementation

### Phase 1: Create 3 New Skills

#### 1.1 Baseline Skill (Dados & Contexto)

**Location:** `.claude/skills/discovery/baseline/`

**Files to create:**
- `SKILL.md` — Full skill with INTERACTION PROTOCOL, interviews, section-by-section approval
- `knowledge/template.md` — Based on team's Google Drive template

**Frontmatter:**
```yaml
name: baseline
description: >
  Use when establishing the current state of metrics, funnels, and data quality
  before a discovery or feature decision. Also triggers on 'baseline', 'current state',
  'dados e contexto', 'funnel metrics', 'what are the numbers today', or 'AS-IS'.
model: claude-opus-4
```

**Dependency chain:**
- BLOCKS: `project-context.md` (needs to know what product/initiative we're documenting)
- ENRICHES: `product-vision.md` (metrics targets from vision inform what baseline to capture)
- FEEDS INTO: discovery report (baseline is the foundation for evidence gathering)

**Position in workflow:** After project-context, before product-vision or in parallel with it.

**Key sections from team template:**
1. Objetivo do documento (qual decisao este baseline ajuda a tomar)
2. Escopo (em escopo / fora de escopo)
3. Contexto do negocio (por que agora)
4. Fluxo atual AS-IS (6-12 bullets) + integracoes + pontos de falha
5. Baseline de metricas (antes):
   - A) Aquisicao e funil (volume, taxas de conversao, CAC/CPL, RPL)
   - B) Qualidade de dados (leads validos/invalidos, duplicados, taxa de falha)
   - C) Performance e confiabilidade (latencia, taxa de erro, incidentes)
   - D) Operacao (horas/semana retrabalho, tarefas manuais)
6. Segmentacoes relevantes (canal, device, coorte, tipo de cliente)
7. Restricoes, premissas e dependencias
8. Problemas e dores ja observadas (sem propor solucao)
9. Lacunas de informacao:
   - Tier 1 (bloqueia avanco) com responsavel e data
   - Tier 2 (importante mas nao bloqueia)
   - Plano de coleta (entrevistas, analytics, logs, CRM)

**Interview protocol (1 question at a time):**
- Q1: "Qual produto/iniciativa estamos documentando e qual decisao este baseline vai informar?"
- Q2: "Descreva o fluxo atual (AS-IS) — o que o usuario faz passo a passo hoje?"
- Q3: "Quais metricas voce tem hoje? (conversoes, volumes, performance, qualidade)"
- Q4: "Qual a confiabilidade desses dados? (alta/media/baixa) De onde vem?"
- Q5: "Quais segmentacoes sao relevantes? (canal, device, coorte, tipo de cliente)"
- Q6: "Quais restricoes existem? (tecnica, legal/LGPD, operacao, capacidade)"
- Q7: "Quais dados faltam que sao criticos para decidir? (Tier 1 = bloqueia, Tier 2 = melhora)"

**Every metric field must include:** valor, periodo, fonte, confiabilidade (alta/media/baixa)

**IDs:** Nenhum ID formal. Este documento e referencia de dados, nao de requisitos.

**SST rule:** Baseline de metricas (antes) ONLY neste documento. Nenhum outro doc deve redefinir o "estado atual".

---

#### 1.2 OST Skill (Opportunity Solution Tree)

**Location:** `.claude/skills/planning/ost/`

**Frontmatter:**
```yaml
name: ost
description: >
  Use when structuring discovery findings into an opportunity tree that connects
  outcomes to opportunities to candidate solutions. Also triggers on 'OST',
  'opportunity solution tree', 'opportunity tree', 'where should we focus',
  'which opportunities', or 'structure the discovery'.
model: claude-opus-4
```

**Dependency chain:**
- BLOCKS: `product-vision.md` (outcome comes from BO-# objectives)
- BLOCKS: `baseline.md` (evidence for opportunities comes from baseline)
- ENRICHES: discovery report / project-context (qualitative evidence)
- FEEDS INTO: prd.md (selected opportunities become PRD-F-# features)

**Position in workflow:** After baseline + discovery, before PRD.

**Key sections from team template:**
1. Outcome (topo da arvore):
   - Frase mensuravel (ex: "Aumentar taxa de conclusao do funil X de A% para B%")
   - Metricas principais com baseline → meta → periodo
   - Guardrails (nao pode piorar)
2. Oportunidades (lista resumida, 3-7 itens)
3. Detalhamento por oportunidade (repetir bloco):
   - Descricao do problema/oportunidade (3-6 linhas)
   - Para quem importa (persona/area)
   - Evidencias (obrigatorio: dado + fonte, quote/relato, incidente/ticket)
   - Impacto potencial (como afeta o outcome)
   - Suposicoes criticas (assumptions)
   - Solucoes candidatas (2-5, alto nivel)
   - Experimentos/validacoes (opcional: nome, objetivo, metodo, criterio de sucesso, duracao)
4. Priorizacao preliminar (nao e a oficial; sinaliza urgencia relativa)
5. Questoes em aberto e proximos passos

**Interview protocol:**
- Q1: "Qual e o outcome que estamos perseguindo? (resultado mensuravel, nao entrega)"
- Q2: "Quais sao as principais oportunidades/problemas que o discovery revelou? (liste 3-7)"
- For each opportunity (one at a time):
  - Q3: "Descreva esta oportunidade. Qual a evidencia que a sustenta?"
  - Q4: "Quais solucoes candidatas voce ve para esta oportunidade? (2-5 direcoes)"
  - Q5: "Quais suposicoes precisam ser verdadeiras para essa solucao funcionar?"
- Q6: "Alguma oportunidade precisa de experimento antes de investir? Qual?"

**IDs:** `O-#` (Opportunity), `S-#.#` (Solution candidate under opportunity)

**SST rule:** Oportunidades estruturadas e solucoes candidatas ONLY neste documento.

**Anti-patterns from team KB:**
- Nao transformar em backlog de tickets
- Nao escrever oportunidades como "fazer X" (isso e solucao, nao oportunidade)
- Nao marcar tudo como urgente
- Outcome deve ser resultado, nao entrega

---

#### 1.3 Release Plan Skill

**Location:** `.claude/skills/implementation/release-plan/`

**Frontmatter:**
```yaml
name: release-plan
description: >
  Use when planning a production release with rollout strategy, monitoring,
  rollback plan, and stakeholder communication. Also triggers on 'release plan',
  'rollout plan', 'go-live', 'launch plan', 'how to deploy', 'rollback plan',
  or 'post-release monitoring'.
model: claude-sonnet-4
```

**Dependency chain:**
- BLOCKS: `implementation-plan.md` (need to know what's being released)
- BLOCKS: `quality-checklist.md` (quality gates must be defined before release)
- ENRICHES: `tech-spec.md` (NFR targets inform monitoring thresholds)
- ENRICHES: `prd.md` (success metrics from PRD inform post-release validation)

**Position in workflow:** After quality-checklist, as the FINAL document before execution.

**Key sections from team template:**
1. Resumo do release (o que, para quem, por que, riscos, como medir)
2. Escopo do release (inclui / nao inclui)
3. Estrategia de rollout:
   - Tipo (full/progressivo/canario/beta/feature flag)
   - Configuracao (flag name, segmento inicial, ramp-up %, criterio para avancar)
4. Checklist pre-release (go/no-go):
   - Requisitos tecnicos (build, migracoes, observabilidade, flag, rollback testado)
   - Requisitos de produto (aceite, UX validada, tracking validado)
   - Requisitos operacionais (CS informado, processos atualizados, comunicacao)
   - Decisao go/no-go (data, responsaveis, decisao, justificativa)
5. Metricas e monitoramento:
   - A) Metricas de sucesso (outcome) com baseline → meta → janela
   - B) Guardrails (nao pode piorar) com thresholds
   - C) Metricas operacionais (erro, latencia, tickets, tempo de resposta)
   - Dashboards (links)
6. Plano de monitoramento (24-72h):
   - Ritual (janela intensiva + acompanhamento)
   - Responsaveis (produto, eng, data, ops)
   - Canal (Slack/Teams)
7. Plano de rollback:
   - Gatilhos (queda conversao > X%, erros > Y%, p95 > Zms, tickets > N)
   - Decisores (PM + Tech Lead + backup)
   - Procedimento (4 steps: desabilitar → validar → comunicar → post-mortem)
8. Plano de comunicacao:
   - Interna (publico, canal, mensagem: o que mudou, quem impactado, como agir, onde acompanhar)
   - Externa (se aplicavel: publico, canal, conteudo)
9. Validacao pos-release:
   - Janela de avaliacao (curto + medio prazo)
   - Criterio para "considerar sucesso"
   - Acoes apos release (learnings, bugs, docs, comunicar resultados)

**Interview protocol:**
- Q1: "O que esta sendo released? (escopo e links para PRD/backlog)"
- Q2: "Qual a estrategia de rollout? (propose 3-4 options: full, progressivo, canario, feature flag)"
- Q3: "Quais metricas definem sucesso? E quais guardrails nao podem piorar?"
- Q4: "Quem monitora nas primeiras 24-72h? Qual o canal de comunicacao?"
- Q5: "O que dispara rollback? (thresholds especificos)"
- Q6: "Quem precisa ser comunicado? (interno e externo)"

**IDs:** Nenhum ID formal. Este e um documento operacional, nao de requisitos.

**SST rule:** Estrategia de rollout, plano de rollback e metricas de monitoramento ONLY neste documento.

---

### Phase 2: Update Existing Templates

#### 2.1 Update product-vision template

**File:** `.claude/skills/discovery/product-vision/knowledge/template.md`

Add sections that the team template has and ours doesn't:
- **Principios do Produto** (regras do jogo): 3-5 principios que guiam decisoes
- **Anti-objetivos** (o que nao faremos): trade-offs explicitos com motivo
- **Guardrails** as separate section (currently mixed into success criteria)

#### 2.2 Update prd template

**File:** `.claude/skills/planning/prd/knowledge/template.md`

Add:
- **Eventos e dados (tracking)**: eventos minimos (nome + quando dispara + propriedades), propriedades obrigatorias, destinos/integracoes
- **Requisitos nao-funcionais** as explicit section: performance, confiabilidade, seguranca/LGPD, observabilidade
- **Plano de rollout (alto nivel)**: estrategia, segmento inicial, ramp-up, rollback gatilhos, comunicacao

#### 2.3 Update user-stories template

**File:** `.claude/skills/planning/user-stories/knowledge/template.md`

Add:
- **Definition of Ready (DoR)**: checklist that a story must pass before entering sprint
- **Definition of Done (DoD)**: checklist that a story must pass to be considered complete
- **Itens de qualidade obrigatorios**: observabilidade (logs, metricas, alertas), tracking (eventos conforme PRD), testes (regressao, automatizados), documentacao

#### 2.4 Update user-stories SKILL.md interview

**File:** `.claude/skills/planning/user-stories/SKILL.md`

Add questions:
- After generating stories: "Quais sao os criterios minimos para uma historia entrar na sprint? (DoR)"
- After acceptance criteria: "Quais sao os criterios para considerar uma historia 'pronta'? (DoD)"
- Quality items: "Quais itens de qualidade sao obrigatorios? (observabilidade, tracking, testes)"

---

### Phase 3: Workflow Integration

#### 3.1 Update Orchestrator

**File:** `.claude/skills/orchestrator/SKILL.md`

Update the Product mode workflow to include the 3 new skills:

```
Phase 1: DISCOVERY
  → project-context.md (5W2H)
  → baseline.md (dados & contexto) [NEW — after project-context]
  → product-vision.md (vision + BO-# + BMAD brainstorm)
  → Discovery Gate

Phase 2: PLANNING
  → ost.md (opportunity solution tree) [NEW — before PRD]
  → prd.md (PRD with MoSCoW)
  → user-stories.md + feature-spec-*.md
  → Planning Gate

Phase 3: DESIGN (unchanged)
  → architecture + data + ux + api (parallel)
  → Implementation Readiness Gate

Phase 4: IMPLEMENTATION
  → implementation-plan.md + sprint-status.yaml + quality-checklist.md
  → release-plan.md [NEW — after quality-checklist, as final doc]
```

**New doc count:** 24 (was 21, +baseline, +ost, +release-plan)

#### 3.2 Update Dependency Graph

**File:** `.claude/skills/orchestrator/dependency-graph.yaml`

Add:
```yaml
baseline:
  requires: [project-context]
  enriched-by: [product-vision]
  phase: discovery

ost:
  requires: [product-vision, baseline]
  enriched-by: [project-context]
  phase: planning

release-plan:
  requires: [implementation-plan, quality-checklist]
  enriched-by: [tech-spec, prd]
  phase: implementation
```

Update existing:
- `prd.requires` should include `ost` (opportunities feed into features)
- `product-vision` should be ENRICHED by `baseline` (metrics context improves vision)

#### 3.3 Update CLAUDE.md

- Update doc count: 21 → 24
- Add baseline, OST, release-plan to the output structure
- Update workflow diagram
- Update SST table with new rules

#### 3.4 Update check-sst

**File:** `.claude/skills/validation/check-sst/SKILL.md`

Add 3 new SST rules:
- Baseline metrics (antes) → ONLY in baseline.md
- Structured opportunities + candidate solutions → ONLY in ost.md
- Rollout strategy + rollback plan + monitoring metrics → ONLY in release-plan.md

---

## Dependencies & Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| New skills are too long (>500 lines) | Medium | Low | Use progressive disclosure — details in knowledge/template.md |
| Team process evolves and templates diverge | Medium | Medium | Templates are living docs — update after pilot use |
| OST position between Discovery and Planning creates gate confusion | Low | Medium | OST is part of Planning phase, not a new gate |

## Sources

- Google Drive folder: [ETUS Product Team Templates](https://drive.google.com/drive/folders/1SHhPz0VcH9tThZfvLlyGRIK0kLlxnS7o)
- Team KB: `ETUS_KB_Templates_Produto.md`
- Team README: `README — Documentos Basicos de Produto (ETUS)`
- All 8 team templates read and analyzed
