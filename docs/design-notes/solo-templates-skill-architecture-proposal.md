# Solo-Templates v4: Proposta de Arquitetura de Skills & Agents

**Data:** 2026-03-14
**Versão:** Draft 1.0
**Contexto:** Redesign da arquitetura de skills do solo-templates usando features modernas do Claude Code (skills com frontmatter avançado, subagents com `.claude/agents/`, hooks, `context: fork`, persistent memory, e progressive disclosure)

---

## 1. Diagnóstico: O que Existe Hoje (v3)

### Estrutura Atual

```
.claude/
├── skills/          (7 skills — sem frontmatter avançado)
│   ├── orchestrator/
│   ├── feature-development-chain/
│   ├── architecture-chain/
│   ├── data-chain/
│   ├── ux-chain/
│   ├── api-backend/
│   ├── brand-guidelines/
│   └── skill-master/
├── agents/          (1 agente genérico)
│   └── command-specialist.md
└── commands/        (50+ comandos — muitos obsoletos/duplicados)
    ├── documents/   (30+ — incluindo eliminados: brd, epics, frd, srs, jtbd...)
    ├── workflow/    (discover, define, develop, deliver)
    ├── orchestration/ (start-project)
    ├── validation/  (check-sst, check-traceability, validate-gate)
    ├── iteration/   (init-ids, refine-vision, show-workflow)
    └── utilities/   (list-gates)
```

### Problemas Identificados

| # | Problema | Impacto |
|---|----------|---------|
| 1 | **Skills sem frontmatter moderno** — Nenhuma usa `context: fork`, `agent`, `allowed-tools`, `model`, `hooks`, ou `disable-model-invocation` | Skills rodam inline no contexto principal, consumindo tokens desnecessariamente |
| 2 | **Commands vs Skills duplicados** — 50+ commands antigos coexistem com 7 skills; muitos obsoletos (brd, epics, frd, srs, jtbd, database-schema, etc.) | Confusão sobre qual invocar; sobrecarga de contexto |
| 3 | **Nenhum subagent especializado** — Apenas `command-specialist.md` genérico; skills "chain" rodam no thread principal | Contexto poluído; sem isolamento; sem paralelismo real |
| 4 | **implementation-chain ausente** — CLAUDE.md documenta mas skill não existe | Gap funcional no workflow |
| 5 | **Knowledge/ files obsoletos** — Templates eliminados (frd.md, epics.md, srs.md, etc.) ainda em knowledge/ | Confundem o modelo quando lidos |
| 6 | **Sem hooks** — Zero automação event-driven (validação pós-geração, auto-lint de SST, etc.) | Qualidade depende 100% de instrução manual |
| 7 | **Sem persistent memory** — Nenhum skill/agent usa `memory: project` | Perda de contexto entre sessões; re-entrevistas desnecessárias |
| 8 | **Descriptions genéricas** — Triggering impreciso; skills competem entre si | Claude pode invocar skill errada ou não invocar nenhuma |

---

## 2. Proposta: Arquitetura v4

### Princípio Central

**"Uma skill por documento, um agent por fase, um orchestrator que delega."**

Cada documento dos 21 tem uma skill dedicada (focada, <200 linhas). Cada fase tem um subagent que orquestra suas skills. O orchestrator é o maestro que delega para os subagents.

### 2.1 Nova Estrutura de Diretórios

```
.claude/
├── agents/                          # 7 SUBAGENTS especializados
│   ├── discovery-agent.md           # Fase 1: Entrevista + Visão (Opus)
│   ├── planning-agent.md            # Fase 2: PRD + Stories + Feature Specs (Opus)
│   ├── architecture-agent.md        # Fase 3a: Arch + Tech Spec + NFRs (Sonnet)
│   ├── data-agent.md                # Fase 3b-Data: 6 data design docs (Sonnet)
│   ├── ux-agent.md                  # Fase 3b-UX: 4 UX design docs (Sonnet)
│   ├── api-agent.md                 # Fase 3b-API: api-spec (Sonnet)
│   └── implementation-agent.md      # Fase 4: Impl Plan + Sprint + Quality (Sonnet)
│
├── skills/
│   ├── orchestrator/                # ORCHESTRATOR (único skill inline)
│   │   ├── SKILL.md                 # Orquestração + gates + delegação
│   │   └── knowledge/
│   │       ├── workflow.md          # 4 fases, 3 gates, 21 docs
│   │       ├── ids.yml             # ID registry
│   │       └── checklists.md       # Gate criteria
│   │   (Todas as doc skills: user-invocable: true + disable-model-invocation: true)
│   │
│   ├── discovery/                   # Skills da Fase 1
│   │   ├── project-context/
│   │   │   ├── SKILL.md            # context: fork, agent: discovery-agent
│   │   │   └── knowledge/
│   │   │       └── template.md
│   │   └── product-vision/
│   │       ├── SKILL.md
│   │       └── knowledge/
│   │           └── template.md
│   │
│   ├── planning/                    # Skills da Fase 2
│   │   ├── prd/
│   │   │   ├── SKILL.md
│   │   │   └── knowledge/
│   │   │       └── template.md
│   │   ├── user-stories/
│   │   │   ├── SKILL.md
│   │   │   └── knowledge/
│   │   │       └── template.md
│   │   └── feature-spec/
│   │       ├── SKILL.md
│   │       └── knowledge/
│   │           └── template.md
│   │
│   ├── architecture/                # Skills da Fase 3a
│   │   ├── architecture-diagram/
│   │   │   ├── SKILL.md
│   │   │   └── knowledge/
│   │   │       └── template.md
│   │   └── tech-spec/
│   │       ├── SKILL.md
│   │       └── knowledge/
│   │           └── template.md
│   │
│   ├── data-design/                 # Skills da Fase 3b (Data Track)
│   │   ├── data-requirements/
│   │   ├── erd/
│   │   ├── database-spec/
│   │   ├── data-dictionary/
│   │   ├── data-flow-diagram/
│   │   └── data-catalog/
│   │
│   ├── ux-design/                   # Skills da Fase 3b (UX Track)
│   │   ├── user-journey/
│   │   ├── ux-sitemap/
│   │   ├── wireframes/
│   │   └── style-guide/
│   │
│   ├── api-design/                  # Skills da Fase 3b (API Track)
│   │   └── api-spec/
│   │
│   ├── implementation/              # Skills da Fase 4
│   │   ├── implementation-plan/
│   │   ├── sprint-status/
│   │   └── quality-checklist/
│   │
│   └── validation/                  # Skills utilitárias
│       ├── check-traceability/
│       │   └── SKILL.md
│       ├── check-sst/
│       │   └── SKILL.md
│       └── validate-gate/
│           └── SKILL.md
│
├── hooks/                           # Automação event-driven (NOVO)
│   ├── post-document-save.sh        # Valida SST após Write/Edit em docs/
│   └── pre-gate-validation.sh       # Auto-check antes de gates
│
└── commands/                        # LIMPOS (apenas v3 válidos)
    ├── start-project.md             # Inicializa estrutura
    ├── discover.md                  # Atalho → discovery-agent
    ├── plan.md                      # Atalho → planning-agent
    ├── design.md                    # Atalho → architecture + design agents
    ├── implement.md                 # Atalho → implementation-agent
    └── validate.md                  # Atalho → validation skills
```

### 2.2 Subagents: O Coração da Arquitetura

**Cada fase tem um subagent dedicado** que:
- Roda em contexto isolado (`context: fork` via skill ou invocação direta)
- Tem acesso a skills específicas via `skills:` no frontmatter
- Usa model apropriado para a tarefa
- Tem persistent memory para acumular contexto entre sessões

#### discovery-agent.md

```yaml
---
name: discovery-agent
description: >
  Conduz a entrevista de descoberta usando 5W2H para gerar
  project-context e product-vision. Use proactively quando o
  usuário mencionar um novo produto, ideia, ou quiser iniciar
  documentação do zero.
model: opus
tools: Read, Write, Edit, Glob, Grep
skills:
  - discovery/project-context
  - discovery/product-vision
  - validation/validate-gate
memory: project
---

Você é um Product Discovery Specialist. Sua missão é extrair do
usuário, via entrevista estruturada (5W2H), toda a informação
necessária para gerar 2 documentos:

1. **project-context.md** → docs/discovery/
2. **product-vision.md** → docs/discovery/

## Workflow

1. Leia os templates em knowledge/ de cada skill preloaded
2. Conduza a entrevista: UMA pergunta por vez, em português
3. Confirme entendimento a cada bloco de respostas
4. **CREATIVE EXPLORATION (padrão BMAD):**
   a. Proponha 3-4 técnicas de brainstorm relevantes ao problema
      (5 Whys, Reverse Brainstorm, Estado Futuro Ideal, SCAMPER, etc.)
   b. Usuário ESCOLHE qual técnica rodar
   c. Execute a técnica em sessão interativa
   d. Gere ARTEFATO de brainstorm (Markdown) com insights da técnica
   e. Ofereça: "Quer rodar outra técnica ou parar por aqui?"
   f. Se SIM → proponha técnicas restantes, repita
   g. Se NÃO → consolide insights de todos os artefatos
5. Gere project-context.md → salve em docs/discovery/
6. Gere product-vision.md → salve em docs/discovery/
7. Execute Discovery Gate (GO/NO-GO/ITERATE)

## Regras
- NUNCA gere sem entrevistar
- NUNCA passe o gate automaticamente
- Salve arquivos em docs/discovery/
- Use IDs: BO-# (business objectives)
- Cada técnica de brainstorm gera um artefato para agents downstream
```

#### planning-agent.md

```yaml
---
name: planning-agent
description: >
  Gera documentos de planejamento (PRD, User Stories, Feature Specs)
  via entrevista interativa usando HMW e MoSCoW. Use quando o usuário
  quiser definir requisitos, features, ou histórias de usuário.
model: opus
tools: Read, Write, Edit, Glob, Grep
skills:
  - planning/prd
  - planning/user-stories
  - planning/feature-spec
  - validation/validate-gate
memory: project
---

Você é um Product Planner. Sua missão é transformar a visão do
produto (docs/discovery/product-vision.md) em requisitos acionáveis.

## Pré-requisitos
- docs/discovery/product-vision.md deve existir

## Documentos Gerados
1. prd.md → docs/planning/ (PRD-F-# features)
2. user-stories.md → docs/planning/ (US-# stories)
3. feature-spec-[name].md → docs/planning/feature-specs/ (quando >3 business rules)

## Workflow
1. Leia product-vision.md para contexto
2. Use HMW para transformar problemas em oportunidades
3. Brainstorm features → Priorize com MoSCoW
4. Gere PRD com features priorizadas
5. Detalhe user stories com acceptance criteria (Given/When/Then)
6. Avalie feature-spec-rule para cada feature
7. Execute Planning Gate
```

#### architecture-agent.md

```yaml
---
name: architecture-agent
description: >
  Define arquitetura técnica, NFRs, e decisões de design (ADRs).
  Use quando o usuário quiser definir arquitetura, escolher
  tecnologias, ou definir requisitos não-funcionais.
model: opus
tools: Read, Write, Edit, Glob, Grep, Bash
skills:
  - architecture/architecture-diagram
  - architecture/tech-spec
memory: project
---

Você é um Software Architect. Gera architecture-diagram e tech-spec
baseado nos requisitos de planejamento.

## Pré-requisitos
- docs/planning/user-stories.md deve existir

## Documentos Gerados
1. architecture-diagram.md → docs/design/
2. tech-spec.md → docs/design/ (NFR-#, ADR-#)

## Regras SST
- NFR numeric targets: SOMENTE em tech-spec.md
```

#### data-agent.md

```yaml
---
name: data-agent
description: >
  Gera 6 documentos de data design via entrevista: data-requirements,
  ERD, database-spec, data-dictionary, data-flow-diagram, data-catalog.
  Use quando o usuário quiser modelar dados, definir entidades, ou
  criar esquemas de banco de dados.
model: sonnet
tools: Read, Write, Edit, Glob, Grep
skills:
  - data-design/data-requirements
  - data-design/erd
  - data-design/database-spec
  - data-design/data-dictionary
  - data-design/data-flow-diagram
  - data-design/data-catalog
memory: project
---

Você é um Data Architect. Gera 6 documentos de data design
via entrevista estruturada com o usuário.

## Pré-requisitos
- docs/design/tech-spec.md deve existir (para NFRs de dados)
- docs/planning/user-stories.md (para entidades implícitas)

## Documentos Gerados (em ordem)
1. data-requirements.md → docs/design/
2. erd.md → docs/design/
3. database-spec.md → docs/design/ (DDL — Single Source)
4. data-dictionary.md → docs/design/ (dict.*/ev.* — Single Source)
5. data-flow-diagram.md → docs/design/
6. data-catalog.md → docs/design/

## Regras SST
- dict.*/ev.*: SOMENTE em data-dictionary.md
- DDL (CREATE TABLE): SOMENTE em database-spec.md
- Field definitions: SOMENTE em data-dictionary.md
```

#### ux-agent.md

```yaml
---
name: ux-agent
description: >
  Gera 4 documentos de UX design via Double Diamond: user-journey,
  ux-sitemap, wireframes, style-guide. Use quando o usuário quiser
  definir fluxos de usuário, navegação, layouts, ou tokens de design.
model: sonnet
tools: Read, Write, Edit, Glob, Grep
skills:
  - ux-design/user-journey
  - ux-design/ux-sitemap
  - ux-design/wireframes
  - ux-design/style-guide
memory: project
---

Você é um UX Designer. Gera 4 documentos de UX design
usando a metodologia Double Diamond.

## Pré-requisitos
- docs/planning/prd.md + user-stories.md devem existir

## Documentos Gerados (em ordem)
1. user-journey.md → docs/design/ (DISCOVER)
2. ux-sitemap.md → docs/design/ (DEFINE)
3. wireframes.md → docs/design/ (DEVELOP)
4. style-guide.md → docs/design/ (DELIVER — tok.* Single Source)

## Regras SST
- tok.* (design tokens): SOMENTE em style-guide.md
```

#### api-agent.md

```yaml
---
name: api-agent
description: >
  Gera especificação completa de API backend: endpoints, schemas,
  autenticação, error handling, rate limiting. Use quando o usuário
  quiser definir APIs, contratos de integração, ou endpoints REST/GraphQL.
model: sonnet
tools: Read, Write, Edit, Glob, Grep
skills:
  - api-design/api-spec
memory: project
---

Você é um API Designer. Gera api-spec.md como ponto de
convergência entre arquitetura, dados, e UX.

## Pré-requisitos (CONVERGENCE POINT)
- docs/design/tech-spec.md (NFRs, stack decisions)
- docs/design/database-spec.md (data model)
- docs/planning/user-stories.md (requirements)

## Documentos Gerados
1. api-spec.md → docs/design/

## Regras SST
- API schemas: SOMENTE em api-spec.md
```

#### implementation-agent.md

```yaml
---
name: implementation-agent
description: >
  Gera plano de implementação, status de sprints, e checklist de
  qualidade. Use quando o design estiver completo e o usuário quiser
  planejar a implementação.
model: sonnet
tools: Read, Write, Edit, Glob, Grep
skills:
  - implementation/implementation-plan
  - implementation/sprint-status
  - implementation/quality-checklist
memory: project
---

Você é um Implementation Planner. Transforma os 17 documentos de
design em um plano de implementação acionável.

## Pré-requisitos
- docs/design/ deve ter pelo menos: architecture-diagram, tech-spec, database-spec

## Documentos Gerados
1. implementation-plan.md → implementation/
2. sprint-status.yaml → implementation/
3. quality-checklist.md → implementation/
```

### 2.3 Skills: Uma por Documento

Cada skill segue o mesmo padrão mínimo:

```yaml
---
name: [document-name]
description: [o que gera + quando usar]
user-invocable: false          # Só o agent invoca
disable-model-invocation: true # Não auto-trigger
---

# [Document Name]

## Template
Read the template at [knowledge/template.md](knowledge/template.md)

## Output
Save to: `docs/[phase]/[filename].md`

## Dependencies
- Requires: [upstream docs]
- Feeds: [downstream docs]

## SST Rules
- [What this doc owns exclusively]
- [What it must NOT contain]

## ID Patterns
- [IDs this doc creates/references]
```

**Vantagem:** Cada skill tem <100 linhas. O template pesado fica em `knowledge/template.md` (progressive disclosure). O agent preloada as skills relevantes.

### 2.4 Hooks: Automação Event-Driven

#### PostToolUse Hook: Validação SST

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/post-document-save.sh"
          }
        ]
      }
    ]
  }
}
```

O script verifica se um arquivo em `docs/` foi editado e valida regras SST:
- Given/When/Then aparece fora de user-stories.md? → Warn
- NFR-# definido fora de tech-spec.md? → Warn
- tok.* definido fora de style-guide.md? → Warn

#### SubagentStop Hook: Auto-Gate Check

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "discovery-agent|planning-agent",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify all required documents exist for the gate. Check file existence in docs/. Report what's missing.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 2.5 Persistent Memory

Cada agent usa `memory: project` para manter `.claude/agent-memory/`:

```
.claude/agent-memory/
├── discovery-agent/
│   └── MEMORY.md      # Contexto do produto, decisões do usuário
├── planning-agent/
│   └── MEMORY.md      # Features priorizadas, regras de negócio
├── architecture-agent/
│   └── MEMORY.md      # Stack escolhida, trade-offs, ADRs
├── design-agent/
│   └── MEMORY.md      # Entities descobertas, tokens definidos
└── implementation-agent/
    └── MEMORY.md      # Sprint progress, blockers
```

**Benefício:** Se a sessão cair no meio da entrevista, o agent retoma de onde parou usando sua memória persistente.

### 2.6 Fluxo de Comunicação entre Agents

```
Usuário: "Quero documentar meu produto X"
    │
    ▼
┌──────────────┐
│ Orchestrator  │  (skill inline — decide fase, delega)
│  /orchestrator│
└──────┬───────┘
       │ delega para
       ▼
┌──────────────┐     Gera: project-context.md
│  discovery-  │──────────► product-vision.md
│    agent     │     Gate: Discovery ✓
└──────┬───────┘
       │ resultado volta ao orchestrator
       ▼
┌──────────────┐     Gera: prd.md, user-stories.md
│  planning-   │──────────► feature-spec-*.md
│    agent     │     Gate: Planning ✓
└──────┬───────┘
       │
       ▼
┌──────────────┐     Gera: architecture-diagram.md
│ architecture-│──────────► tech-spec.md
│    agent     │
└──────┬───────┘
       │
       ▼
┌──────────────┐     Data: 6 docs ─┐
│   design-    │     UX: 4 docs   ├──► Gate: Readiness ✓
│    agent     │     API: 1 doc   ─┘
└──────┬───────┘
       │
       ▼
┌──────────────┐     Gera: implementation-plan.md
│implementation│──────────► sprint-status.yaml
│    agent     │──────────► quality-checklist.md
└──────────────┘
```

**Comunicação:** Os agents não se comunicam diretamente. Comunicam via **filesystem** — cada agent lê os docs gerados pelo anterior em `docs/`. O orchestrator coordena a sequência.

### 2.7 Padrão de Agentes Paralelos (Gestão de Contexto)

Agentes paralelos são uma **técnica de gestão de contexto** — não têm relação com o tamanho da equipe. Permitem explorar múltiplas perspectivas sem poluir o contexto principal.

**Quando usar:**
- Brainstorm com múltiplas técnicas simultâneas (discovery-agent)
- Design tracks paralelos: data-agent + ux-agent + api-agent (já no fluxo v4)
- Qualquer momento onde múltiplas análises independentes são possíveis

**Regras obrigatórias para CADA invocação de agente paralelo:**

1. **PROMPT COMPLETO** — O agente nasce sem contexto. O prompt DEVE incluir:
   - Descrição completa do produto/feature
   - Todas as respostas/decisões anteriores relevantes
   - Goals, non-goals, constraints
   - Instruções específicas da tarefa
   - Formato esperado do output

2. **RELATÓRIO OBRIGATÓRIO** — O prompt DEVE instruir: "Gere um RELATÓRIO estruturado contendo: o que foi analisado, técnica/método aplicado, insights descobertos (lista priorizada), riscos/gaps identificados, recomendações."

3. **CONSOLIDAÇÃO** — Após retorno de todos os agentes, o orchestrator/agent principal lê os relatórios, consolida insights únicos, e apresenta ao usuário.

**Exemplo prático — Brainstorm paralelo no discovery-agent:**

O orchestrator despacha 3 subagents simultaneamente:
- Subagent A: aplica "5 Whys" ao problema → relatório
- Subagent B: aplica "Reverse Brainstorm" → relatório
- Subagent C: aplica "SCAMPER" → relatório

Cada um recebe o contexto completo do produto + instrução de gerar relatório. O discovery-agent consolida os 3 relatórios em um único artefato de brainstorm.

**Exemplo prático — Design tracks paralelos (já na arquitetura v4):**

Após architecture-agent, o orchestrator despacha em paralelo:
- data-agent (6 docs) + ux-agent (4 docs) + api-agent (1 doc)

Cada um recebe: PRD, user-stories, tech-spec como contexto. Cada um gera seus documentos + relatório de decisões/trade-offs tomados.

### 2.8 Limpeza: Comandos e Files Obsoletos

**DELETAR** (commands v2 obsoletos):
- `commands/documents/brd.md`
- `commands/documents/epics.md`
- `commands/documents/frd.md`
- `commands/documents/srs.md`
- `commands/documents/jtbd.md`
- `commands/documents/database-schema.md`
- `commands/documents/database-requirements.md`
- `commands/documents/design-requirements.md`
- `commands/documents/frontend-requirements.md`
- `commands/documents/ux-design-decisions.md`
- `commands/documents/ux-docs.md`
- `commands/documents/data-model.md`
- `commands/documents/architecture.md` (duplica architecture-diagram)

**DELETAR** (knowledge/ files obsoletos):
- `orchestrator/knowledge/brd.md`
- `orchestrator/knowledge/epics.md`
- `orchestrator/knowledge/frd.md`
- `orchestrator/knowledge/srs.md`
- `architecture-chain/knowledge/srs.md`
- `data-chain/knowledge/drd.md`
- `data-chain/knowledge/database-schema.md`
- `ux-chain/knowledge/jtbd.md`
- `ux-chain/knowledge/uxdd.md`
- `ux-chain/knowledge/design-requirements.md`
- `ux-chain/knowledge/frontend-requirements.md`

**MANTER como archive** (para referência histórica):
- `_archive/` (já existe)

---

## 3. Comparação: v3 vs v4

| Aspecto | v3 (Atual) | v4 (Proposta) |
|---------|-----------|---------------|
| **Skills** | 7 monolíticas (~700 linhas cada) | 21 focadas (<200 linhas) + 3 validação |
| **Agents** | 1 genérico | 7 especializados por fase/track |
| **Commands** | 50+ (muitos obsoletos) | 6 atalhos limpos |
| **Hooks** | 0 | 2+ (SST validation, gate pre-check) |
| **Memory** | Nenhuma | 7 persistent memory scopes |
| **Context usage** | Tudo inline (token-heavy) | Fork + progressive disclosure |
| **Frontmatter** | Apenas name+description | Completo (context, agent, tools, model, memory, hooks) |
| **Obsolete files** | 20+ acumulados | Limpos/deletados |
| **Implementation chain** | Documentado mas ausente | Implementado |

---

## 4. Plano de Execução

### Fase 1: Foundation (Agents + Orchestrator)
1. Criar 5 subagents em `.claude/agents/`
2. Reescrever `orchestrator/SKILL.md` para delegar via agents
3. Limpar commands obsoletos

### Fase 2: Document Skills (21 skills)
4. Extrair cada skill de dentro das "chain" skills monolíticas
5. Criar structure `skill-name/SKILL.md` + `knowledge/template.md`
6. Manter progressive disclosure (SKILL.md < 200 linhas)

### Fase 3: Implementation Chain (gap fix)
7. Criar `implementation/` skills (plan, sprint-status, quality-checklist)
8. Criar `implementation-agent.md`

### Fase 4: Hooks + Memory
9. Implementar SST validation hook
10. Implementar gate pre-check hook
11. Configurar persistent memory nos agents

### Fase 5: Cleanup + Validation
12. Deletar commands/knowledge obsoletos
13. Rodar evals com skill-creator
14. Otimizar descriptions para triggering

---

## 5. Decisões Tomadas

| # | Decisão | Escolha |
|---|---------|---------|
| 1 | **Design: quantos agents?** | **3 separados** — data-agent, ux-agent, api-agent. Permite paralelismo real e isolamento de contexto. |
| 2 | **Skills invocáveis?** | **Ambos** — `user-invocable: true` + `disable-model-invocation: true`. Usuário pode /prd diretamente OU via agent. |
| 3 | **Model por agent?** | **Opus para Discovery+Planning** (entrevistas criativas), **Sonnet para Design+Implementation** (tarefas estruturadas). |
| 4 | **Hooks?** | **SST + Gate hooks** — PostToolUse valida SST, SubagentStop verifica completude em gates. |

## 6. Fluxo Atualizado (7 Agents)

```
Usuário: "Quero documentar meu produto X"
    │
    ▼
┌──────────────┐
│ Orchestrator  │  (skill inline — decide fase, delega)
│  /orchestrator│
└──────┬───────┘
       │
       ▼
┌──────────────┐  Opus     project-context.md
│  discovery-  │─────────► product-vision.md
│    agent     │           Gate: Discovery ✓
└──────┬───────┘
       ▼
┌──────────────┐  Opus     prd.md, user-stories.md
│  planning-   │─────────► feature-spec-*.md
│    agent     │           Gate: Planning ✓
└──────┬───────┘
       ▼
┌──────────────┐  Sonnet   architecture-diagram.md
│ architecture-│─────────► tech-spec.md
│    agent     │
└──────┬───────┘
       │
       ├────────────────────────────────────┐
       ▼                    ▼               ▼
┌────────────┐   ┌────────────┐   ┌──────────┐
│ data-agent │   │ ux-agent   │   │api-agent │  3 agents Sonnet
│ (6 docs)   │   │ (4 docs)   │   │(1 doc)   │  em paralelo
└──────┬─────┘   └──────┬─────┘   └────┬─────┘
       │                │              │
       └────────────────┴──────────────┘
                        │
                  Gate: Readiness ✓
                        │
                        ▼
              ┌──────────────────┐  Sonnet
              │ implementation-  │─────────► impl-plan + sprint + quality
              │      agent       │
              └──────────────────┘
```

---

## 7. Próximos Passos

### Imediato (esta sessão)
1. Definir test cases para validação da arquitetura
2. Criar a primeira skill + agent como proof-of-concept
3. Rodar evals com skill-creator

### Fase 1: Foundation
4. Criar 7 subagents em `.claude/agents/`
5. Reescrever `orchestrator/SKILL.md` para delegar
6. Limpar commands obsoletos

### Fase 2: Document Skills (21 skills)
7. Extrair skills das "chain" skills monolíticas
8. Criar `skill-name/SKILL.md` + `knowledge/template.md`

### Fase 3: Implementation Chain (gap fix)
9. Criar implementation/ skills + implementation-agent

### Fase 4: Hooks + Memory + Cleanup
10. SST validation hook + gate pre-check hook
11. Persistent memory nos agents
12. Deletar files obsoletos

### Fase 5: Optimize
13. Rodar description optimization via skill-creator
14. Full eval cycle com test cases expandidos

---

*Documento atualizado com decisões do usuário em 2026-03-14.*
