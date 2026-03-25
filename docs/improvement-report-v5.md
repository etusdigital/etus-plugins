# ETUS PMDocs v5 — Relatório de Sugestões de Melhorias

**Data:** 2026-03-17
**Baseado em:** Análise profunda de 3 repositórios clonados (Superpowers v5.0.4, Compound Engineering v2.40, BMAD v6), leitura de todas as skills/agents/workflows de cada um, e pesquisa de frameworks de marketing de performance.

---

## Sumário Executivo

O ETUS PMDocs v4.1 é o framework mais completo para **documentação de produto** (21 docs, rastreabilidade BO→impl, SST). Porém, ao compará-lo com os 3 frameworks concorrentes e considerar os casos de uso de marketing de performance, identificamos **4 categorias de melhorias**:

1. **Melhorias estruturais** — Inspiradas nos 3 frameworks (Quick Flow, Knowledge Capture, Anti-Rationalization)
2. **Novos agentes e skills de marketing** — Cobertura de performance marketing
3. **Skills de execução pós-documentação** — Ponte entre documentação e código
4. **Melhorias de DX** — Developer experience e usabilidade do framework

---

## PARTE 1: Melhorias Estruturais (Inspiradas nos Concorrentes)

### 1.1 Quick Flow Track (Inspirado: BMAD)

**O que é:** Track simplificado para documentar features pequenas, bug fixes, ou campanhas rápidas sem passar pelas 4 fases completas.

**Como funciona no BMAD:** `bmad-quick-spec` gera um tech-spec direto, `bmad-quick-dev` implementa. Se o escopo cresce, escala automaticamente para o fluxo completo.

**Implementação sugerida:**
- Novo comando: `/quick-doc [tipo]`
- Gera 1 documento único (quick-spec.md) com seções condensadas de Discovery + Planning
- Sem gates formais — apenas checklist inline
- Auto-detecção de escopo: se >3 features ou >5 user stories → sugere escalar para fluxo completo

**Resultado esperado:** Redução de 70min → 10min para documentar features simples. Elimina a barreira de entrada do framework para tarefas menores.

---

### 1.2 Knowledge Capture / Compound Loop (Inspirado: Compound Engineering)

**O que é:** Documentar soluções, decisões e aprendizados de cada projeto para reusar em projetos futuros.

**Como funciona no Compound:** `/ce:compound` lança 6 sub-agentes paralelos que extraem padrões de bugs corrigidos, decisões arquiteturais e preferências de código. Salva em `docs/solutions/` com YAML frontmatter pesquisável. O `learnings-researcher` depois consulta essas soluções em novos projetos.

**Implementação sugerida:**
- Nova Fase 5: **Retrospective** (pós-implementação)
- Novo skill: `project-retrospective.md` → Documenta lições aprendidas, padrões descobertos, decisões que funcionaram/falharam
- Novo diretório: `docs/ets-docs/learnings/`
- Novo agente: `learnings-researcher` (consulta retrospectivas passadas durante Phase 1)
- IDs: `LEARN-#` (Aprendizado) com tags categorizadas

**Resultado esperado:** Cada projeto torna o próximo mais rápido. Padrões de arquitetura, decisões de UX, e métricas de marketing que funcionaram são reutilizados automaticamente.

---

### 1.3 Anti-Rationalization Reforçado (Inspirado: Superpowers)

**O que é:** Técnicas de persuasão (Cialdini) para impedir que o agente pule etapas, mesmo sob pressão do usuário.

**Como funciona no Superpowers:** A meta-skill `using-superpowers` usa linguagem imperativa ("YOU MUST", "This is not negotiable") e tabelas de racionalização com contra-argumentos para cada desculpa possível.

**Implementação sugerida:**
- Adicionar ao orchestrator SKILL.md uma seção `## RED FLAGS` com sintomas de quando o agente está prestes a pular uma fase
- Expandir a seção `ANTI-RATIONALIZATION RULES` existente com tabela Excuse→Reality (como no Superpowers)
- Adicionar ao validate-gate um "adversarial review mode" (inspirado BMAD) que força a encontrar problemas antes de aprovar

**Resultado esperado:** Documentos de maior qualidade. Redução de 40% em problemas encontrados em fases posteriores por informação insuficiente em fases anteriores.

---

### 1.4 Adversarial Review (Inspirado: BMAD)

**O que é:** Revisão forçada onde o reviewer DEVE encontrar problemas. Zero findings = re-análise obrigatória.

**Como funciona no BMAD:** Qualquer artefato pode passar por adversarial review. O reviewer adota postura cínica e retorna findings com severidade (HIGH/MEDIUM/LOW).

**Implementação sugerida:**
- Novo skill de validação: `adversarial-review.md`
- Invocado automaticamente pelo orchestrator antes de cada gate
- Retorna lista de findings com severidade
- HIGH findings bloqueiam GO; MEDIUM viram tech debt; LOW são informativos
- Integrar na Phase 3 (Design) onde já existe adversarial review parcial

**Resultado esperado:** Documentos mais robustos. Captura de edge cases e contradições que passariam despercebidos na validação padrão.

---

### 1.5 Agentes Nomeados com Personalidade (Inspirado: BMAD)

**O que é:** Dar nomes e personalidades aos agentes para melhorar a experiência interativa.

**Como funciona no BMAD:** Mary (Analyst), John (PM), Winston (Architect), Bob (Scrum Master), Sally (UX Designer), etc. Cada um tem `identity`, `communicationStyle`, e `principles`.

**Implementação sugerida:**
- Adicionar YAML frontmatter com `displayName`, `identity`, e `communicationStyle` aos 7 agentes
- Exemplos: discovery-agent → "Luna" (curiosa, investigativa), planning-agent → "Atlas" (estruturado, priorizador), architecture-agent → "Blueprint" (técnico, pragmático)

**Resultado esperado:** Experiência mais engajante. Usuário lembra qual agente faz o quê. Melhora a interatividade durante entrevistas de Discovery e Planning.

---

### 1.6 Pesquisa Automatizada Paralela (Inspirado: Compound Engineering)

**O que é:** Lançar múltiplos agentes de pesquisa em paralelo durante o planejamento para enriquecer o contexto.

**Como funciona no Compound:** `/ce:plan` lança 4 agentes: `framework-docs-researcher`, `best-practices-researcher`, `git-history-analyzer`, `repo-research-analyst`. `/deepen-plan` lança 20-40 agentes.

**Implementação sugerida:**
- Novo skill: `deepen-discovery.md` — Após Discovery, lança 3-5 agentes paralelos de pesquisa:
  - `market-researcher` (pesquisa concorrentes via web)
  - `tech-researcher` (pesquisa frameworks/libs via Context7 MCP)
  - `audience-researcher` (pesquisa personas e comportamento)
- Resultados consolidados como input para Phase 2

**Resultado esperado:** Discovery mais rica com dados de mercado reais em vez de apenas entrevista com o usuário. PRDs com benchmarks competitivos.

---

## PARTE 2: Novos Agentes e Skills de Marketing de Performance

### 2.1 Novo Agente: marketing-agent (Opus)

**Propósito:** Especialista em documentação de marketing de performance. Gera documentos de campanha, funil, criativos e métricas.

**Skills gerados:**

#### 2.1.1 `growth-strategy.md` (Estratégia de Crescimento)
- Framework AARRR (Acquisition → Activation → Retention → Revenue → Referral) com métricas por estágio
- Growth Loops documentados (viral: k-factor, content: SEO→signup→dados→conteúdo, paid: revenue→reinvestimento)
- Bullseye Framework (19 canais → rank → test top 3 → focus no que funciona)
- Priorização ICE (Impact × Confidence × Ease) ou RICE (Reach × Impact × Confidence / Effort)
- Marketing OKRs por trimestre (ex: "Reduzir CAC em 20%, atingir ROAS 4:1, LTV:CAC ≥ 3:1")
- IDs: `GS-#` (Growth Strategy items), `MKT-OBJ-#` (Marketing Objectives)
- **SST:** Métricas de crescimento e AARRR targets ONLY aqui

#### 2.1.2 `campaign-brief.md` (Brief de Campanha)
- Objetivo (awareness/consideration/conversion)
- Público-alvo (Custom Audiences, Lookalikes, interesse) com `SEG-#` segments
- Canais (Meta, Google, TikTok, programmatic) com budget allocation %
- Media Plan: alocação de budget por canal, timeline de veiculação, KPIs por canal
- KPIs target (CAC, ROAS, CTR, CPA, CPL) com valores numéricos
- UTM naming convention: `{source}_{medium}_{campaign-type}_{name}_{audience}_{YYYYMM}`
  - Ex: `google_cpc_leadgen_data-quality-ebook_mid-market_202603`
  - Regra: tudo lowercase, sem espaços, hífens dentro de segmentos, underscores entre segmentos
- Ad Set naming: `[Audiência]_[Parâmetros]_[Budget]` (ex: `LAL-1%-Purchasers-$75`)
- Ad naming: `[TipoCriativo]_[Hook]_[Versão]` (ex: `Video-TestimonialHook-V1`)
- IDs: `CAMP-#` (Campaign), `SEG-#` (Audience Segment)
- **SST:** Briefs de campanha, UTM conventions e segmentos ONLY aqui
- Nota: Campanhas com KPIs definidos têm 80% melhor ROI (HubSpot 2025)

#### 2.1.3 `funnel-spec.md` (Especificação de Funil)
- TOFU (Top of Funnel): Awareness → canais, criativos, métricas (impressions, reach, CPM)
- MOFU (Middle of Funnel): Consideration → retargeting, lead magnets, métricas (CTR, leads, CPL)
- BOFU (Bottom of Funnel): Conversion → ofertas, urgência, métricas (CVR, CPA, ROAS)
- Pontos de conversão entre estágios
- Mapeia para user-journey.md (JOUR-# steps)
- IDs: `FUN-#` (Funnel steps)
- **SST:** Funil de conversão ONLY aqui

#### 2.1.4 `creative-strategy.md` (Estratégia de Criativos)
- Framework de 5 passos: Research (Ad Library, Creative Center) → Brief → Ideação/Script → Produção → Feedback Loop
- Método 3:2:2 (3 criativos × 2 textos × 2 CTAs) + Dynamic Creative Testing (DCT) para Meta
- Angles de hook (pain point, curiosity, social proof, UGC, authority, testimonial)
- Formatos por plataforma (9:16 vertical para Reels/TikTok, 1:1 para feed, 16:9 para YouTube)
- Scoring system: Hook Rate (>30% 3s views), Hold Rate (25-50%), CTR (>1% cold traffic)
- Creative fatigue tracking (frequência vs. performance decay)
- Referência a style-guide.md (tok.* design tokens) e brand voice
- IDs: `CRV-#` (Creative Variant) com naming: `[TipoCriativo]_[Hook]_[Versão]`
- **SST:** Criativos, variações e scoring ONLY aqui
- Nota: Criativos contribuem até 70% da performance (Meta 2026 — AI faz targeting, criativo é o diferencial)

#### 2.1.5 `experiment-log.md` (Log de Experimentos / A/B Tests)
- Hipótese (formato: "Se [variável], então [resultado] porque [razão]")
- Variantes (control vs. treatment)
- Métricas primária/secundárias
- Tamanho de amostra e duração
- Critério de sucesso (significância estatística)
- Resultados e aprendizados
- IDs: `EXP-#` (Experiment)
- **SST:** Resultados de experimentos ONLY aqui

#### 2.1.6 `metrics-dashboard.md` (Dashboard de Métricas)
- 3 camadas de dashboards:
  - Executive (C-level): Revenue impact, CAC, LTV, ROAS, ROI
  - Operational (marketing team): Tráfego por canal, conversion rate, CPA
  - Campaign (managers): Performance diária, ad-level, real-time
- Métricas fundamentais com fórmulas:
  - CAC = Total spend / novos clientes (target: varia por indústria)
  - LTV = Revenue esperada ao longo do tempo (target: LTV:CAC ≥ 3:1)
  - ROAS = Revenue / ad spend (target: >3x para DTC)
  - MER = Total revenue / total marketing spend (target: >3x)
  - Payback Period = CAC / monthly revenue per customer (target: <12 meses)
- Cadência: Daily (issues), Weekly (trends), Monthly (ROI deep-dive), Quarterly (strategic review)
- Attribution models: Last-Click, First-Click, Linear, Time-Decay, U-Shaped (40/20/40), Data-Driven (ML)
  - 67% dos times B2B ainda usam last-touch → oportunidade de melhoria
  - Empresas reportam 14-36% melhora em CPA com multi-touch attribution
- Alertas real-time (ex: "CVR caiu abaixo de 2%", "CPA subiu 15% acima da média")
- IDs: `MET-#` (Metric definitions), `DASH-#` (Dashboard specs), `ATTR-#` (Attribution rules)
- **SST:** Definições de métricas, fórmulas, dashboards e attribution ONLY aqui

#### 2.1.7 `landing-page-spec.md` (Especificação de Landing Page)
- URL e UTM pattern
- Headline, subheadline, CTA
- Seções (hero, social proof, features, FAQ, CTA final)
- Formulário (campos, validação)
- SEO (title, meta description, H1, schema markup)
- Performance targets (load time <3s, LCP <2.5s, CLS <0.1)
- Referência a wireframes.md e style-guide.md
- IDs: `LP-#` (Landing Page)
- **SST:** Specs de landing pages ONLY aqui

#### 2.1.8 `email-sequence.md` (Sequência de Email/Push)
- Trigger (signup, abandonment, purchase, inactivity)
- Sequência de emails (D+0, D+1, D+3, D+7...)
- Subject line, preview text, body template
- Segmentação por comportamento
- Métricas (open rate, click rate, unsubscribe)
- IDs: `SEQ-#` (Sequence steps)
- **SST:** Sequências de email ONLY aqui

---

#### 2.1.9 `content-strategy.md` (Estratégia de Conteúdo + SEO)
- 7 frameworks: Pillars (temas centrais), Clusters (topic/subtopic), PESO (Paid/Earned/Shared/Owned), Editorial Calendar, Customer Journey content, Repurposing, Voice/Tone
- Editorial Calendar com campos: título, persona, keyword, formato, pilar, autor, deadlines, canais, status
- SEO PRD: Project Summary, Goals/KPIs, User Stories (incluindo crawlers como "usuários"), Technical Requirements (URL structure, SSR/SSG, schema markup JSON-LD), Acceptance Criteria
- 4 pilares SEO 2026: Estrutura Técnica, Sistemas de Conteúdo, Construção de Autoridade, UX
- IDs: `CON-#` (Content pieces), `SEO-#` (SEO requirements)
- **SST:** Pilares de conteúdo, editorial calendar e SEO specs ONLY aqui

#### 2.1.10 `brand-voice.md` (Brand Voice & Guidelines para Campanhas)
- Tom de voz da marca (com exemplos de uso correto/incorreto)
- Ad Copy Patterns: Headline (benefit-driven), Body (problema→solução→prova), CTA (action-oriented)
- Estilo visual por canal (cores para urgência, CTAs, trust signals)
- Do's and Don'ts com exemplos concretos
- Referência a style-guide.md (tok.* tokens) para consistência cross-channel
- IDs: nenhum (referência, não rastreável)
- **SST:** Brand voice para marketing ONLY aqui (tok.* continua no style-guide.md)

---

### 2.2 Sistema de IDs para Marketing

Extensão da cadeia de rastreabilidade:

```
BO-# (Business Objective)
  ↓
PRD-F-# (Feature)        GS-# (Growth Strategy)
  ↓                         ↓
US-# (User Story)        CAMP-# (Campaign)
  ↓                         ↓
FS-# (Feature Spec)     FUN-# (Funnel Step) + CRV-# (Creative)
  ↓                         ↓
impl-# (Task)           EXP-# (Experiment) + LP-# (Landing Page)
                            ↓
                         MET-# (Metric) + SEQ-# (Email Sequence)
```

**Rastreabilidade bidirecional:** Cada CAMP-# referencia um ou mais BO-#. Cada EXP-# referencia um CAMP-# e um CRV-#.

---

### 2.3 Nova Fase: Marketing Phase (entre Design e Implementation)

```
Phase 1: DISCOVERY → Phase 2: PLANNING → Phase 3: DESIGN
  → Phase 3.5: MARKETING (novo, marketing-agent, Opus)
    → growth-strategy.md, campaign-brief.md, funnel-spec.md,
      creative-strategy.md, landing-page-spec.md, email-sequence.md
    → Marketing Readiness Gate (GO/ITERATE/DESCOPE)
  → Phase 4: IMPLEMENTATION
    → experiment-log.md, metrics-dashboard.md (adicionados ao impl-plan)
```

**Gate:** Marketing Readiness Gate
- Funil completo? (TOFU → MOFU → BOFU mapeado)
- UTM naming convention definida?
- Criativos planejados? (mín. 3 variantes)
- KPIs target definidos? (CAC, ROAS, CTR com valores numéricos)
- Landing pages especificadas?
- Experimentos planejados?

---

## PARTE 3: Skills de Execução Pós-Documentação

### 3.1 Document Review Subagent (Inspirado: Superpowers + Compound)

**O que é:** Subagente que revisa cada documento gerado antes de declarar completo.

**Implementação:** Após cada skill gerar um documento, um `doc-reviewer` (Haiku, para custo baixo) revisa estrutura, completude e SST.

**Resultado esperado:** Documentos sem seções vazias ou [TODO]. Validação inline economiza tempo no gate.

---

### 3.2 Multi-Model Optimization (Inspirado: Superpowers v5)

**O que é:** Usar o modelo mais barato capaz para cada tarefa.

**Implementação:**
- Phase 1-2: Opus (requer entrevista interativa complexa)
- Phase 3 (Data/UX/API agents): Sonnet (já está assim)
- Validation (check-sst, check-traceability): Haiku (read-only, pattern matching)
- doc-reviewer: Haiku
- Phase Marketing: Sonnet (geração estruturada)

**Resultado esperado:** Redução de ~30% no custo de tokens sem perda de qualidade.

---

### 3.3 Context7 MCP Integration (Inspirado: Compound Engineering)

**O que é:** Integrar documentação de frameworks via Context7 MCP para enriquecer tech-spec e architecture decisions.

**Implementação:** Adicionar `Context7 MCP` como integração opcional. Quando o architecture-agent escolher um framework (e.g., Next.js, Rails), consultar Context7 para documentação atualizada.

**Resultado esperado:** Tech specs com referências à documentação oficial e patterns recomendados dos frameworks escolhidos.

---

## PARTE 4: Melhorias de DX (Developer Experience)

### 4.1 `bmad-help` Style Helper (Inspirado: BMAD)

**O que é:** Skill inteligente que detecta o estado do projeto e recomenda o próximo passo.

**Implementação:** Novo skill `etus-help.md` que lê `.handoff/phase.json` e `docs/ets-docs/` para sugerir:
- "Você está na Phase 2 (Planning). PRD completo, user stories incompletas. Rode `/plan` para continuar."
- "Nenhum projeto encontrado. Rode `/start-project` para começar."

**Resultado esperado:** Onboarding mais fácil. Usuário nunca fica perdido sobre o que fazer em seguida.

---

### 4.2 Plugin Marketplace Compatibility

**O que é:** Empacotar ETUS PMDocs como plugin do Claude Code marketplace.

**Implementação:** Criar `.claude-plugin/plugin.json` seguindo o formato do Compound Engineering. Publicar no marketplace oficial.

**Resultado esperado:** Instalação com um comando: `/plugin install etus-pmdocs`. Auto-update. Alcance massivo.

---

### 4.3 Multi-Platform Support (Inspirado: Compound + Superpowers)

**O que é:** Suporte a Cursor, Codex, Gemini CLI além de Claude Code.

**Implementação:** Criar shims para cada plataforma (como o Superpowers faz com scripts de conversão).

**Resultado esperado:** Alcance 5-10x maior. Não fica preso ao ecossistema Anthropic.

---

## Resumo de Impacto

| Melhoria | Complexidade | Impacto | Prioridade |
|----------|-------------|---------|------------|
| Quick Flow Track | Média | Alto (remove barreira de entrada) | P0 |
| Marketing Agent (8 skills) | Alta | Crítico (novo mercado) | P0 |
| Knowledge Capture | Média | Alto (efeito composto) | P1 |
| Adversarial Review | Baixa | Médio (qualidade) | P1 |
| Anti-Rationalization Reforçado | Baixa | Médio (qualidade) | P1 |
| Document Review Subagent | Baixa | Médio (qualidade) | P1 |
| Pesquisa Paralela (deepen) | Média | Alto (contexto) | P1 |
| Agentes Nomeados | Baixa | Baixo (UX) | P2 |
| Multi-Model Optimization | Baixa | Médio (custo) | P2 |
| Context7 MCP Integration | Baixa | Médio (contexto) | P2 |
| etus-help Skill | Baixa | Médio (DX) | P2 |
| Plugin Marketplace | Média | Alto (distribuição) | P2 |
| Multi-Platform Support | Alta | Alto (alcance) | P3 |

---

## Números do v5 Projetado

| Métrica | v4.1 (atual) | v5 (proposto) |
|---------|-------------|--------------|
| Agentes | 7 | 10 (+marketing-agent, +analytics-agent, +learnings-researcher) |
| Skills | 25 | 40 (+10 marketing, +2 analytics, +3 structural) |
| Documentos | 21 | 34 (+12 marketing/analytics, +1 retrospective) |
| Gates | 3 | 4 (+Marketing Readiness Gate) |
| Fases | 4 | 5.5 (+Marketing Phase, +Retrospective) |
| IDs rastreáveis | 11 tipos | 22 tipos (+11 marketing/analytics IDs) |
| SST Rules | 7 | 19 (+12 marketing SST rules) |

---

## Próximos Passos

1. **Implementar Quick Flow** — Menor esforço, maior impacto imediato
2. **Criar marketing-agent + 8 skills** — Abre novo mercado (PM + Growth Marketing)
3. **Adicionar Knowledge Capture** — Efeito composto a longo prazo
4. **Publicar no Marketplace** — Distribuição e visibilidade

---

---

## PARTE 5: Técnicas Específicas a Incorporar (Da Análise Profunda dos Repos)

### 5.1 Do Superpowers — Two-Stage Review System

O Superpowers usa revisão em 2 estágios para cada task:
1. **Spec Compliance Review** — "O agente construiu o que foi pedido? Nada a mais, nada a menos?"
2. **Code Quality Review** — "O que foi construído está bem feito?"

A ordem é crucial: construir a coisa errada com qualidade = desperdício. Construir a coisa certa com baixa qualidade = corrigível.

**Aplicação no ETUS:** Após cada skill gerar um documento, um `doc-spec-reviewer` verifica se o conteúdo alinha com o upstream (BLOCKS deps). Depois, um `doc-quality-reviewer` verifica completude e profundidade.

---

### 5.2 Do Superpowers — CSO (Claude Search Optimization)

Descoberta crítica: o Superpowers descobriu que colocar resumo do workflow na `description` do SKILL.md faz o Claude seguir a description em vez de ler o skill completo.

**Regra:** Description = APENAS "Use when [condições de trigger]", NUNCA resumo do que o skill faz.

**Aplicação no ETUS:** Revisar todas as 25 descriptions dos SKILL.md para garantir que são triggers, não resumos.

---

### 5.3 Do Compound — Origin Document Traceability

O `/ce:plan` do Compound carrega decisões do brainstorm com referências explícitas:
```markdown
Decision: Use PostgreSQL (see origin: docs/brainstorms/2026-01-15-auth-requirements.md)
```

Se o brainstorm tem perguntas não resolvidas ("Resolve Before Planning"), o plan **se recusa a rodar**.

**Aplicação no ETUS:** Adicionar `(see origin: docs/ets-docs/discovery/product-vision.md#BO-3)` nas decisões do PRD, tech-spec, e implementation-plan.

---

### 5.4 Do Compound — Conditional Agent Pattern

O `/ce:review` detecta o tipo de conteúdo no PR e aciona agentes condicionalmente:
- PR tem migrações? → `schema-drift-detector` + `data-migration-expert` + `deployment-verification-agent`
- PR tem frontend? → `julik-frontend-races-reviewer`
- PR tem segurança? → `security-sentinel`

**Aplicação no ETUS:** No validate-gate, detectar o tipo de conteúdo gerado:
- Design tem banco? → Acionar validação extra de DDL/ERD
- Design tem API? → Acionar validação de schemas
- Design tem UX? → Acionar validação de acessibilidade (WCAG)

---

### 5.5 Do Compound — Deepen Plan (20-40 Agentes Paralelos)

O `/deepen-plan` descobre TODAS as skills disponíveis (projeto + usuário + plugins instalados), spawna 1 sub-agente por skill, e deixa CADA agente decidir se é relevante.

**Regra:** "Do NOT filter by relevance — let agents decide applicability."

**Aplicação no ETUS:** Criar `/deepen-discovery` que lança agentes paralelos por cada aspecto: mercado, tecnologia, audiência, concorrentes, regulação.

---

### 5.6 Do BMAD — Step-File Architecture

Cada workflow do BMAD é dividido em step files sequenciais:
```
workflows/create-prd/
├── workflow.md (master control)
├── steps/
│   ├── step-01-init.md
│   ├── step-02-interview.md
│   ├── step-03-requirements.md
│   └── step-04-output.md
└── prd.template.md
```

Com frontmatter tracking: `stepsCompleted: [step-01, step-02]`

**Benefícios:** Execução determinística, recovery de falhas (sabe último step completo), menus param para decisão humana.

**Aplicação no ETUS:** Converter os 7 SKILL.md maiores (orchestrator, prd, user-stories, tech-spec, etc.) para step-file architecture.

---

### 5.7 Do BMAD — Party Mode (Multi-Agent Discussion)

O BMAD traz 2-3 agentes simultaneamente em uma sessão para debater. Exemplo:

```
User: "Devemos usar monolito ou microservices?"

Architect (Winston): "Para 10K users iniciais, monolito. ADR-1 documenta isso."
Dev (Amelia): "Concordo, mas precisamos de um clean boundary para auth — isso
              facilita extrair depois."
PM (John): "Ambos estão certos. Mas o PRD-F-3 (multi-tenant) pode forçar a
           separação mais cedo. Precisamos do feedback do data-agent."
```

**Aplicação no ETUS:** Criar `/party-mode` que carrega 2-3 agentes relevantes e facilita cross-talk. Útil para: decisões de arquitetura, review de PRD, post-mortems.

---

### 5.8 Do BMAD — Project Context "Constitution"

O `project-context.md` do BMAD é carregado automaticamente por TODOS os workflows de implementação. Contém: tech stack, regras de código, convenções, testing patterns.

**Diferente do nosso `project-context.md`:** O do BMAD foca em regras de implementação para agentes (não contexto de projeto). É uma "constituição" que todos os agentes obedecem.

**Aplicação no ETUS:** Adicionar uma seção `## Implementation Rules` ao nosso project-context.md que é lida por todos os agentes na Phase 3-4.

---

### 5.9 Do BMAD — Adversarial Review Forçado (Findings Mínimos)

Regra do BMAD: o reviewer **DEVE encontrar no mínimo 10 issues**. Zero findings = re-análise obrigatória.

O reviewer assume postura cínica: "problemas existem, encontre-os". Busca especificamente o que FALTA (não apenas o que está errado).

**Filtro humano:** Como o AI é instruído a encontrar problemas, haverá falsos positivos. O humano decide o que é real.

**Aplicação no ETUS:** Adicionar ao `validate-gate` um modo `--adversarial` que exige minimum 5 findings antes de recomendar GO. Severity HIGH bloqueia GO.

---

### 5.10 Do BMAD — Scale-Adaptive Tracks com Escalation Guards

O BMAD detecta automaticamente se o escopo cresceu além do Quick Flow:
- Menções multi-componente → sugere Quick Spec primeiro
- Linguagem de sistema → sugere PRD completo
- Incerteza no approach → sugere Discovery

**Aplicação no ETUS:** Implementar no `/quick-doc` (proposto na Parte 1) detecção de escopo com auto-escalação:
- Se >3 features → "Escopo grande detectado. Recomendo `/orchestrator` para workflow completo."
- Se tiver banco de dados → "Necessita data design. Recomendo Phase 3 completa."
- Trabalho feito no quick-doc é preservado e migrado para o fluxo completo.

---

## PARTE 6: Roadmap de Implementação Sugerido

### Sprint 1 (1 semana) — Quick Wins
- [ ] Revisar todas as 25 descriptions de SKILL.md para CSO (trigger-only, sem resumo)
- [ ] Estender product-vision.md com seção "Go-to-Market Strategy"
- [ ] Estender prd.md com seção "Marketing Requirements"
- [ ] Adicionar marketing metrics ao data-dictionary template (dict.campaign.*, dict.funnel.*)
- [ ] Adicionar brand voice/ad copy patterns ao style-guide template

### Sprint 2 (1 semana) — Quick Flow + Help
- [ ] Criar `/quick-doc` skill com escopo detection + auto-escalation
- [ ] Criar `etus-help` skill (detecta estado do projeto, recomenda próximo passo)
- [ ] Adicionar origin traceability (`see origin:`) ao PRD e tech-spec templates

### Sprint 3 (2 semanas) — Marketing Agent + Skills
- [ ] Criar marketing-agent.md (Opus)
- [ ] Criar 4 skills prioritários: campaign-brief, funnel-spec, creative-strategy, metrics-dashboard
- [ ] Criar sistema de IDs marketing: CAMP-#, FUN-#, CRV-#, MET-#
- [ ] Criar Marketing Readiness Gate no validate-gate skill
- [ ] Estender dependency-graph.yaml com marketing skills

### Sprint 4 (2 semanas) — Marketing Skills Complementares + Analytics
- [ ] Criar 4 skills restantes: landing-page-spec, email-sequence, experiment-log, growth-strategy
- [ ] Criar analytics-agent.md (Sonnet) com event-tracking-spec + attribution-model skills
- [ ] Criar IDs: LP-#, SEQ-#, EXP-#, GS-#
- [ ] Estender handoff protocol com marketing_artifacts

### Sprint 5 (1 semana) — Knowledge Capture + Review
- [ ] Criar Phase 5: Retrospective com project-retrospective skill
- [ ] Criar docs/ets-docs/learnings/ structure
- [ ] Implementar adversarial review mode no validate-gate (--adversarial flag)
- [ ] Criar doc-spec-reviewer + doc-quality-reviewer (2-stage review)

### Sprint 6 (1 semana) — Advanced Features
- [ ] Implementar Party Mode (/party-mode) para multi-agent discussions
- [ ] Criar /deepen-discovery para pesquisa paralela automatizada
- [ ] Implementar step-file architecture para os 3 skills maiores (orchestrator, prd, tech-spec)
- [ ] Criar .customize.yaml support para personalização de agentes

### Sprint 7 (1 semana) — Distribution
- [ ] Criar .claude-plugin/plugin.json para marketplace
- [ ] Testar instalação via `/plugin install`
- [ ] Documentar README público
- [ ] Publicar v5.0

---

*Relatório gerado com análise profunda de 3 repositórios clonados (14 skills Superpowers, 46 skills + 28 agentes Compound Engineering, 34+ workflows + 12 agentes BMAD), leitura completa de todos os SKILL.md/agents/workflows, e pesquisa de 15+ fontes de frameworks de marketing de performance.*
