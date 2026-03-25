# Análise: Discovery & Brainstorm — BMAD vs Superpowers vs Double Diamond

**Objetivo:** Extrair as melhores práticas de cada framework para enriquecer o contexto dos agents e skills de Discovery e Planning do Solo-Templates v4.

---

## 1. Superpowers — Brainstorming Skill

### O que faz bem

O Superpowers tem a skill de brainstorm mais **rigorosa** dos três. Funciona como um gate-keeper que impede qualquer implementação antes de um design aprovado.

### Processo Completo (9 Steps)

```
1. EXPLORE PROJECT CONTEXT
   → Lê arquivos, docs, commits recentes
   → Entende o que já existe antes de perguntar

2. OFFER VISUAL COMPANION (opcional)
   → "Quer que eu mostre mockups/diagramas enquanto discutimos?"
   → Browser para: wireframes, mockups, layouts
   → Terminal para: requisitos, trade-offs, escopo

3. ASK CLARIFYING QUESTIONS (Socratic)
   → UMA pergunta por vez
   → Foco em: propósito, restrições, critérios de sucesso
   → Preferência por multiple-choice sobre open-ended
   → Não assume — questiona

4. PROPOSE 2-3 APPROACHES
   → Com trade-offs explícitos
   → Com recomendação clara
   → Usuário escolhe antes de avançar

5. PRESENT DESIGN
   → Em seções dimensionadas pela complexidade
   → Aprovação por seção (não tudo de uma vez)
   → Chunks curtos o bastante para ler e digerir

6. WRITE DESIGN DOC
   → Salva em docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md
   → Commit no git

7. SPEC REVIEW LOOP
   → Despacha spec-document-reviewer subagent
   → Máximo 5 iterações de refinamento

8. USER REVIEWS WRITTEN SPEC
   → Gate: usuário DEVE aprovar antes de prosseguir

9. TRANSITION TO IMPLEMENTATION
   → Invoca writing-plans skill (e NADA MAIS)
```

### Princípios-Chave

| Princípio | Detalhe |
|-----------|---------|
| **Uma pergunta por mensagem** | Evita overwhelm; mantém foco |
| **Multiple-choice > open-ended** | Reduz carga cognitiva do usuário |
| **YAGNI ruthlessly** | Remove features desnecessárias proativamente |
| **Sempre propor alternativas** | Nunca settla na primeira ideia |
| **Validação incremental** | Aprovação por seção, não em bloco |
| **Anti-pattern explícito** | "Projetos simples são onde assunções não examinadas causam mais desperdício" |
| **Hard gate** | "NÃO invoque nenhuma skill de implementação até design aprovado" |

### O que Podemos Extrair

1. **Gate anti-implementação** — O discovery-agent NÃO deve gerar documentos antes de completar a entrevista
2. **Uma pergunta por vez** — Padrão que já usamos, mas devemos enforçar no agent prompt
3. **2-3 abordagens com trade-offs** — Antes de definir visão, apresentar alternativas
4. **Aprovação por seção** — Não mostrar o doc inteiro; apresentar em blocos
5. **Spec review subagent** — Despachar um reviewer após geração (validação cruzada)

---

## 2. BMAD — Analyst Agent + Creative Intelligence Suite

### O que faz bem

BMAD tem o fluxo de discovery mais **estruturado** dos três, com agentes especializados e técnicas de brainstorming formais. A separação Analyst → Product Manager → Architect é clara.

### Analyst Agent (Mary) — Workflow

```
FASE 1: ANALYSIS

  Command 1: /brainstorm
  ├── Explora espaço de ideias
  ├── Faz perguntas clarificadoras para descobrir:
  │   • Goals e non-goals
  │   • Constraints (technical, business, compliance)
  │   • Risks e assumptions
  │   • Open questions para pesquisa posterior
  │   • Immediate next steps
  ├── Aplica 3 técnicas de brainstorm:
  │   • "O que poderia dar errado?" (risk-first)
  │   • "Estado futuro ideal" (vision-first)
  │   • "Reverse brainstorming" (anti-pattern discovery)
  └── Output: brainstorming document (Markdown table format)

  Command 3: /create-project-brief
  ├── Duas modalidades:
  │   • Interactive Mode (recomendado) — trabalha seção por seção
  │   • YOLO Mode — gera draft completo de uma vez
  ├── Seções do Project Brief:
  │   • Market analysis
  │   • User personas
  │   • Competitive insights
  │   • Success criteria
  │   • Goals/Non-goals
  │   • Constraints
  │   • Risks
  └── Output: Product Brief (10-15 páginas, "source of truth")

  Command 5: /elicit (Advanced Elicitation)
  ├── Stress-test do plano/brief
  ├── Ações de elicitação:
  │   • Expand sections with more details
  │   • Validate against similar products
  │   • Stress test assumptions
  │   • Explore alternative approaches
  │   • Analyze resource/constraint trade-offs
  │   • Generate risk mitigation strategies
  │   • Challenge scope from MVP minimalist view
  │   • Brainstorm creative feature possibilities
  └── Output: Brief refinado e validado

  Command 7: /research-prompt
  └── Gera prompts de pesquisa para ferramentas externas de AI
```

### Creative Intelligence Suite (CIS) — 8 Técnicas

| # | Técnica | O que faz |
|---|---------|-----------|
| 1 | **5 Whys** | Descende até a root cause perguntando "por quê?" 5x |
| 2 | **SCAMPER** | Substitute, Combine, Adapt, Modify, Put to use, Eliminate, Reverse |
| 3 | **Mind Mapping** | Ramificação visual de conceitos |
| 4 | **Reverse Brainstorming** | "Como podemos PIORAR isso?" → inverte para soluções |
| 5 | **Six Thinking Hats** | Fatos(W), Emoções(R), Pessimismo(B), Otimismo(Y), Criatividade(G), Processo(B) |
| 6 | **Starbursting** | Gera perguntas (Who/What/Where/When/Why/How) sobre cada feature |
| 7 | **Brainwriting** | Ideias escritas → iteração silenciosa (3-6 agents paralelos) |
| 8 | **SWOT** | Strengths, Weaknesses, Opportunities, Threats |

**Padrão de uso principal (interativo):** Agent propõe técnicas → usuário escolhe → roda uma por vez → gera artefato → oferece rodar outra ou parar.

**Padrão alternativo (paralelo para gestão de contexto):** 2-3 subagents aplicam técnicas diferentes ao MESMO problema simultaneamente. Cada subagent recebe prompt com contexto COMPLETO e DEVE gerar relatório estruturado. Orchestrator consolida.

### Transição Analyst → Product Manager

```
Analyst (Mary)                    Product Manager (James)
─────────────                     ─────────────────────
Product Brief (source of truth)
        │
        ▼
                                  /create-prd
                                  ├── Lê Product Brief
                                  ├── Transforma em PRD com:
                                  │   • Functional requirements
                                  │   • Non-functional requirements
                                  │   • User stories
                                  │   • Feature prioritization
                                  └── Output: PRD formal
```

### O que Podemos Extrair

1. **3 comandos de discovery** — brainstorm, create-brief, elicit são fases distintas (não um blob)
2. **Interactive vs YOLO mode** — Oferecer ao usuário escolha de velocidade
3. **Elicitation como stress-test** — Fase separada APÓS o brief, para desafiar assunções
4. **CIS técnicas selecionáveis** — Agent propõe, usuário escolhe, roda uma por vez (ou paralelo para gestão de contexto)
5. **Goals + Non-goals** — Sempre documentar o que NÃO é escopo
6. **Brainstorm table format** — Estrutura tabular para organizar ideias

---

## 3. Double Diamond — Framework Teórico

### O que faz bem

O Double Diamond fornece o **modelo mental** que amarra tudo: divergir → convergir, duas vezes.

### Os 4 Ds Mapeados

```
Diamond 1: PROBLEMA CERTO
┌─────────────────────────────────────────────┐
│                                             │
│  DISCOVER (diverge)     DEFINE (converge)   │
│                                             │
│  • User interviews      • Affinity diagrams │
│  • Market research      • Root-cause (5Why) │
│  • Competitor analysis  • Problem statement │
│  • Service safari       • HMW questions     │
│  • Analytics review     • User personas     │
│  • Stakeholder talks    • Priority matrix   │
│                                             │
│  "Entender o problema"  "Definir o problema"│
└─────────────────────────────────────────────┘

Diamond 2: SOLUÇÃO CERTA
┌─────────────────────────────────────────────┐
│                                             │
│  DEVELOP (diverge)      DELIVER (converge)  │
│                                             │
│  • Brainstorm features  • User stories      │
│  • Prototype concepts   • Feature specs     │
│  • Explore alternatives • Architecture      │
│  • Test assumptions     • Tech spec + NFRs  │
│  • HMW → features       • Data/UX/API design│
│  • MoSCoW priority      • Implementation    │
│                                             │
│  "Explorar soluções"   "Entregar solução"   │
└─────────────────────────────────────────────┘
```

### Mapeamento para Solo-Templates v4

| Double Diamond | Solo-Templates Fase | Agent | Docs |
|---------------|-------------------|-------|------|
| **DISCOVER** (diverge) | Discovery | discovery-agent | project-context |
| **DEFINE** (converge) | Discovery | discovery-agent | product-vision |
| **DEVELOP** (diverge) | Planning | planning-agent | prd, user-stories |
| **DELIVER** (converge) | Design + Implementation | architecture/data/ux/api/impl agents | 15 docs restantes |

---

## 4. Síntese: Proposta de Enriquecimento para v4

### 4.1 Discovery Agent — Workflow Enriquecido

O discovery-agent deve incorporar os melhores elementos de cada framework:

```
FASE DISCOVER (Divergente) — "Entender o Problema"
═══════════════════════════════════════════════════

Step 1: CONTEXT SCAN (Superpowers)
  → Lê arquivos existentes, docs/, CLAUDE.md
  → "Já existe algo construído? Qual o estado atual?"

Step 2: PROBLEM INTERVIEW (5W2H + BMAD clarifying)
  → Uma pergunta por vez (Superpowers)
  → Multiple-choice quando possível (Superpowers)
  → Cobre: What, Who, Where, When, Why, How, How Much
  → Documenta Goals + Non-goals (BMAD)
  → Documenta Constraints + Assumptions (BMAD)

Step 3: CREATIVE EXPLORATION (BMAD CIS - seleção pelo usuário)
  → Agent PROPÕE 3-4 técnicas de brainstorm relevantes ao problema:
    • "Estado futuro ideal" — como seria perfeito?
    • "O que poderia dar errado?" — reverse brainstorm
    • "5 Whys" — descende até a root cause
    • "SCAMPER" — substituir, combinar, adaptar...
    • "Six Thinking Hats" — múltiplas perspectivas
  → USUÁRIO ESCOLHE qual técnica rodar
  → Agent EXECUTA a técnica escolhida em sessão interativa
  → Agent GERA ARTEFATO de brainstorm (Markdown) com insights da técnica
  → Agent OFERECE: "Quer rodar outra técnica ou parar por aqui?"
    • Se SIM → propõe técnicas restantes, repete ciclo
    • Se NÃO → consolida insights de todos os artefatos gerados
  → Cada artefato fica disponível para agents downstream

  ALTERNATIVA: Agentes Paralelos (gestão de contexto)
  → Para explorar múltiplas técnicas simultaneamente:
    • Orchestrator despacha 2-3 subagents, cada um com UMA técnica
    • CADA subagent recebe prompt completo com TODO o contexto
      (produto, respostas da entrevista, goals, constraints)
    • CADA subagent DEVE gerar um RELATÓRIO estruturado do que fez
    • Orchestrator consolida os relatórios em insights únicos
  → Nota: agentes paralelos são uma técnica de GESTÃO DE CONTEXTO,
    não relacionada ao tamanho da equipe

Step 4: ALTERNATIVE APPROACHES (Superpowers)
  → Propõe 2-3 abordagens para o produto
  → Com trade-offs explícitos
  → Com recomendação
  → Usuário escolhe antes de avançar

═══ OUTPUT: project-context.md (docs/discovery/) ═══
     Contém: 5W2H, goals/non-goals, constraints,
     assumptions, risks, creative insights


FASE DEFINE (Convergente) — "Definir o Problema"
═══════════════════════════════════════════════════

Step 5: VISION SYNTHESIS
  → Destila tudo em problem statement claro
  → Define business objectives (BO-#)
  → Aplica HMW (How Might We) para transformar
    problemas em oportunidades

Step 6: VISION PRESENTATION (Superpowers)
  → Apresenta em seções, não tudo de uma vez
  → Aprovação por seção
  → Chunks digeríveis

Step 7: ELICITATION / STRESS-TEST (BMAD)
  → Desafia assunções da visão:
    • "Existem produtos similares? Como se diferenciar?"
    • "Qual o MVP mínimo absoluto?" (YAGNI)
    • "Quais os maiores riscos?"
    • "Isso resolve o problema real do usuário?"

═══ OUTPUT: product-vision.md (docs/discovery/) ═══
     Contém: Problem statement, BO-#, target users,
     value proposition, success criteria, risks

═══ GATE: Discovery (GO / NO-GO / ITERATE) ═══
```

### 4.2 Planning Agent — Workflow Enriquecido

```
FASE DEVELOP (Divergente) — "Explorar Soluções"
═══════════════════════════════════════════════════

Step 1: PRD FEATURES (HMW → Features)
  → Lê product-vision.md
  → Transforma HMW questions em features concretas
  → Brainstorm aberto de features possíveis

Step 2: FEATURE PRIORITIZATION (MoSCoW)
  → Must have / Should have / Could have / Won't have
  → Valida com usuário: "Concorda com essa priorização?"

Step 3: INTERACTIVE vs FAST MODE (BMAD)
  → Oferece escolha:
    • Interactive: trabalha feature por feature
    • Fast: gera PRD draft completo, depois refina

═══ OUTPUT: prd.md (docs/planning/) ═══
     Contém: PRD-F-# features priorizadas por MoSCoW


FASE DEVELOP cont. (Convergente) — "Detalhar Soluções"
═══════════════════════════════════════════════════

Step 4: USER STORIES
  → Para cada PRD-F-#, gera US-# stories
  → Given/When/Then acceptance criteria
  → Single Source of Truth para Gherkin

Step 5: FEATURE SPEC EVALUATION
  → Para cada feature: ">3 business rules?"
    • SIM → gera feature-spec-[name].md
    • NÃO → stories são suficientes

Step 6: SPEC REVIEW (Superpowers)
  → Auto-review: traceability check
  → "Cada US-# referencia um PRD-F-#?"
  → "Cada FS-# referencia US-# corretos?"

═══ OUTPUT: user-stories.md + feature-spec-*.md ═══
═══ GATE: Planning (GO / DESCOPE / ITERATE) ═══
```

### 4.3 Técnicas Específicas por Skill

| Skill | Técnica Principal | Fonte |
|-------|------------------|-------|
| `project-context` | 5W2H + Clarifying Questions | Solo-Templates + BMAD |
| `product-vision` | HMW + Elicitation Stress-Test | Solo-Templates + BMAD |
| `prd` | MoSCoW + Feature Brainstorm | Solo-Templates |
| `user-stories` | Given/When/Then + Story Mapping | Solo-Templates |
| `feature-spec` | Business Rule Decomposition | Solo-Templates |
| `architecture-diagram` | C4 Model + Trade-off Analysis | Standard |
| `tech-spec` | NFR Framework + ADR Pattern | Standard |
| `data-*` (6 docs) | Entity Discovery + ERD | Standard |
| `ux-*` (4 docs) | Double Diamond Develop/Deliver | Double Diamond |
| `api-spec` | Contract-First Design | Standard |
| `implementation-*` | Sprint Decomposition | Agile |

### 4.4 Knowledge Files Adicionais para Skills

Cada skill de discovery/planning deve ter um `knowledge/guide.md` adicional com:

```markdown
# Interview Guide — [Document Name]

## Questions to Ask (in order)

### Block 1: Context [2-3 questions]
1. [Question - multiple choice when possible]
   Options: A) ..., B) ..., C) ..., D) Other
2. ...

### Block 2: Deep Dive [3-4 questions]
3. [Open-ended but focused]
4. ...

### Block 3: Validation [2 questions]
5. "Confirme se entendi corretamente: [summary]"
6. "Tem algo que eu deveria ter perguntado mas não perguntei?"

## Techniques to Apply
- [Technique name]: [When to use]
- ...

## Anti-Patterns to Avoid
- ❌ Gerar sem entrevistar
- ❌ Fazer todas as perguntas de uma vez
- ❌ Assumir ao invés de perguntar
- ❌ Pular a fase de alternativas

## Quality Criteria
- [ ] Todas as seções do template preenchidas
- [ ] Goals E non-goals documentados
- [ ] Constraints identificadas
- [ ] Risks listados
- [ ] Usuário aprovou cada seção
```

### 4.5 Padrão de Agentes Paralelos (Gestão de Contexto)

Agentes paralelos são uma **técnica de gestão de contexto** do Claude Code — não têm relação com tamanho de equipe. Use quando precisar explorar múltiplas perspectivas sem poluir o contexto principal.

**Regras obrigatórias para qualquer invocação de agente paralelo:**

```
1. PROMPT COMPLETO
   O agente nasce SEM contexto. O prompt DEVE conter:
   - Descrição completa do produto/feature
   - Respostas da entrevista até o momento
   - Goals, non-goals, constraints
   - Instruções específicas da técnica a executar
   - Formato esperado do output

2. RELATÓRIO OBRIGATÓRIO
   O prompt DEVE instruir o agente a gerar um RELATÓRIO estruturado:
   - O que foi analisado
   - Técnica aplicada
   - Insights descobertos (lista priorizada)
   - Riscos ou gaps identificados
   - Recomendações

3. CONSOLIDAÇÃO
   Após todos os agentes retornarem, o orchestrator/agent principal:
   - Lê todos os relatórios
   - Consolida insights únicos (remove duplicatas)
   - Apresenta ao usuário para validação
```

**Exemplo de prompt para agente paralelo de brainstorm:**

```
Você é um analista aplicando a técnica [TÉCNICA] ao seguinte produto:

## Contexto do Produto
[Colar project-context completo ou respostas da entrevista]

## Goals
[Goals do produto]

## Non-goals
[Non-goals]

## Sua Tarefa
Aplique a técnica [TÉCNICA] ao problema descrito acima.

## Output Esperado
Gere um RELATÓRIO em Markdown com:
1. Técnica aplicada e como foi usada
2. Insights descobertos (mínimo 5, máximo 10)
3. Riscos ou pontos cegos identificados
4. Top 3 recomendações
```

### 4.6 Hard Gates (do Superpowers)

Adicionar em cada agent prompt:

```
## GATES (non-negotiable)

❌ NÃO gere documentos antes de completar a entrevista
❌ NÃO pule seções do template
❌ NÃO passe gates automaticamente — SEMPRE peça aprovação
❌ NÃO avance para próxima fase sem gate GO
✅ SEMPRE apresente em seções digeríveis
✅ SEMPRE ofereça 2-3 alternativas antes de decidir
✅ SEMPRE documente o que NÃO está no escopo
✅ SEMPRE faça stress-test das assunções antes do gate
```

---

## 5. Comparação Resumida

| Aspecto | Superpowers | BMAD | Double Diamond | Solo-Templates v4 |
|---------|-------------|------|---------------|-------------------|
| **Foco** | Software dev | Software dev | Design thinking | Product documentation |
| **Discovery** | Socratic Q&A | Analyst agent + CIS | Discover → Define | 5W2H + HMW + Elicit |
| **Brainstorm** | Clarifying Qs → Approaches | 8 técnicas (user seleciona) | Diverge → Converge | Técnicas selecionáveis + artefatos |
| **Gate** | Design approval | Brief → PRD handoff | Diamond transitions | 3 gates explícitos |
| **Pergunta** | 1 por mensagem | Multiple per block | N/A (conceitual) | 1 por mensagem |
| **Alternativas** | 2-3 com trade-offs | Via CIS techniques | Via divergent phase | 2-3 com trade-offs |
| **Stress-test** | Spec review subagent | /elicit command | N/A | Elicitation step |
| **Non-goals** | YAGNI principle | Goals + Non-goals | N/A | Goals + Non-goals |
| **Output** | Design doc | Product Brief | Problem statement | project-context + vision |

---

*Análise gerada para informar o design das skills v4 do Solo-Templates.*
