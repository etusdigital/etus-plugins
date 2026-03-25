# Comparação de Artefatos: BMAD vs AIOX vs OpenAI Harness vs Proposta Atual

## TL;DR

| Aspecto             | BMAD                           | AIOX                     | OpenAI Harness              | Nossa Proposta Anterior |
| ------------------- | ------------------------------ | ------------------------ | --------------------------- | ----------------------- |
| **Filosofia**       | Spec-driven, agent-as-code     | Task-first, multi-IDE    | Map-not-encyclopedia        | Doc-layer architecture  |
| **Agentes**         | 9 (analyst→dev+QA)             | 6 (@analyst→@qa)         | Codex (1 modelo)            | N/A (humano+LLM)        |
| **Templates**       | 13+ YAML/MD compiláveis        | Format specs versionados | ExecPlan + QUALITY_SCORE    | Feature Brief + Spec    |
| **Sharding**        | Sim (PRD, Architecture)        | Não (monolítico)         | Não                         | Não                     |
| **Quality Gates**   | 6 checklists + Impl. Readiness | Checklists por fase      | Golden Principles + linters | Nenhum formalizado      |
| **Sprint tracking** | sprint-status.yaml             | Não (externo)            | progress.json               | Não                     |
| **Ponto forte**     | Completude + portabilidade     | Multi-IDE + Squads       | Simplicidade + enforcement  | Semântica de dados      |

---

## 1. BMAD METHOD — Inventário Completo de Artefatos

### 1.1 Agentes (9 + Orchestrator)

| Agente       | Arquivo                  | Responsabilidade                          |
| ------------ | ------------------------ | ----------------------------------------- |
| Analyst      | `analyst.agent.yaml`     | Exploração do problema, produz Brief      |
| PM           | `pm.agent.yaml`          | PRD com FRs/NFRs, MoSCoW                  |
| Architect    | `architect.agent.yaml`   | Architecture doc, ADRs, tech stack        |
| PO           | `po.agent.yaml`          | Alinhamento de docs, sharding             |
| SM           | `sm.agent.yaml`          | Stories hiper-detalhadas, sprint planning |
| Dev          | `dev.agent.yaml`         | Código + testes a partir de stories       |
| TEA          | `tea.agent.yaml`         | Test Architect, QA design                 |
| UX Designer  | `ux-designer.agent.yaml` | UX specs                                  |
| Tech Writer  | `tech-writer.agent.yaml` | Documentação                              |
| Orchestrator | `bmad-orchestrator`      | Coordenação entre agentes                 |

Cada agente é YAML versionável, com: role, tools, success criteria, menu de workflows executáveis. Portável entre IDEs.

### 1.2 Fases e Artefatos

#### Fase 1: DISCOVER (Strategic Foundation)

| Artefato          | Agente  | Formato  | Descrição                                                                                  |
| ----------------- | ------- | -------- | ------------------------------------------------------------------------------------------ |
| **Project Brief** | Analyst | Markdown | Visão, goals, target users, success metrics, constraints. Gerado via brainstorming guiado. |

#### Fase 2: PLAN (Requirements + Architecture)

| Artefato                            | Agente       | Formato                                                            | Descrição                                                                                                              |
| ----------------------------------- | ------------ | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| **PRD**                             | PM           | MD (monolítico ou sharded)                                         | FRs testáveis, NFRs, Epics agrupados, User Stories com acceptance criteria. ~15-25 páginas.                            |
| **PRD Shards**                      | PM/PO        | `docs/prd/index.md` + `01-overview.md`, `02-requirements.md`, etc. | ~650 linhas por shard. Carregamento INDEX_GUIDED ou SELECTIVE_LOAD.                                                    |
| **Architecture**                    | Architect    | MD (monolítico ou sharded)                                         | Tech stack, componentes, data flow, integrações. Inclui ADRs inline.                                                   |
| **Architecture Shards**             | Architect/PO | `docs/architecture/<component>.md`                                 | Um arquivo por componente/módulo.                                                                                      |
| **project-context.md**              | PO/Architect | Markdown                                                           | "Constituição" do projeto: coding standards, constraints, team preferences. Carregado por todos os agentes downstream. |
| **Epics**                           | PM           | `docs/epics/epic-N-<name>.md`                                      | Feature-grouped. Seções: Title, Overview, Features, Tasks, Dependencies.                                               |
| **Implementation Readiness Report** | SM/PO        | Markdown                                                           | Gate: valida completude de PRD + Architecture + Epics. Bloqueia Fase 3 se incompleto.                                  |

#### Fase 3: SOLUTION (Story Development)

| Artefato               | Agente | Formato                     | Descrição                                                                                                                                                                                       |
| ---------------------- | ------ | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stories**            | SM     | `docs/stories/story-<N>.md` | Hiper-detalhadas: contexto arquitetural completo, dependencies, prerequisites (checklist), tasks (max 1 dev-day), subtasks, task→AC mapping, acceptance criteria (Gherkin), testing guidelines. |
| **sprint-status.yaml** | SM     | YAML                        | Status de todos epics/stories, dependency graph, next story. Atualizado conforme progresso.                                                                                                     |

#### Fase 4: BUILD & VERIFY (Implementation)

| Artefato                       | Agente  | Formato             | Descrição                                                                  |
| ------------------------------ | ------- | ------------------- | -------------------------------------------------------------------------- |
| **Feature Branch Code**        | Dev     | Git                 | Implementação de tasks da story.                                           |
| **Implementation Reports**     | Dev     | `_bmad-output/*.md` | Notas, decisões, logs de implementação.                                    |
| **PR + Code Review Checklist** | Dev/TEA | GitHub PR           | Requirements coverage, testes, dead code, security, performance.           |
| **QA Report**                  | TEA     | Markdown            | Pass/Fail por AC, Issues (Blocker/Major/Minor), status: Approved/Rejected. |
| **Test Cases**                 | TEA/Dev | Code + MD           | Unit, integration, edge cases gerados a partir de ACs.                     |

### 1.3 Templates Core (13+)

Localizados em `src/core/templates/`:

1. `prd-template.md` / `prd-tmpl.yaml`
2. `architecture-template.md`
3. `story-template.md` / `story-tmpl.yaml`
4. `epic-template.md` / `epic-tmpl.yaml`
5. `brief-template.md`
6. `ux-spec-template.md`
7. `db-schema-template.md`
8. `project-context-template.md`
9. `sprint-status-template.yaml`
10. `qa-report-template.md`
11. `implementation-readiness-template.md`
12. `code-review-checklist.md`
13. `tech-spec-template.md`

Cada template contém: **Structure** (layout final), **Processing Logic** (como o agente interage com o humano), **Validation Rules** (checklists de completude), **Integration Points** (conexão com artefatos downstream).

### 1.4 Quality Checklists (6+)

- Story validation checklist
- PRD completeness checklist
- Architecture review checklist
- Implementation readiness checklist
- Code review checklist
- QA test coverage checklist

### 1.5 Configuração

| Artefato                 | Formato              | Descrição                                                                  |
| ------------------------ | -------------------- | -------------------------------------------------------------------------- |
| **BMAD Config**          | YAML                 | `prdSharded`, `architectureSharded`, `output_folder`, team preferences     |
| **Workflow Definitions** | YAML (34+)           | Um por workflow: `create-prd`, `create-architecture`, `create-story`, etc. |
| **Agent Definitions**    | YAML (agent-as-code) | Versionados, portáveis, compiláveis para diferentes IDEs                   |

---

## 2. AIOX (Synkra) — Inventário Completo de Artefatos

### 2.1 Agentes (6 core)

| Agente     | Role                           | Produz                      |
| ---------- | ------------------------------ | --------------------------- |
| @analyst   | Research & dependency analysis | Planning Brief              |
| @pm        | Specification writing          | PRD                         |
| @architect | Technical design               | Architecture Document       |
| @sm        | Plan breakdown                 | Development Stories         |
| @dev       | Implementation                 | Source Code                 |
| @qa        | Quality assurance              | QA Review, Violation Report |

### 2.2 Fases e Artefatos

#### Fase 1: PLANNING (Spec Pipeline)

| Artefato                  | Agente     | Formato                                      | Descrição                                                         |
| ------------------------- | ---------- | -------------------------------------------- | ----------------------------------------------------------------- |
| **Planning Brief**        | @analyst   | Markdown                                     | Requirements analysis, dependency research, complexity assessment |
| **PRD**                   | @pm        | Markdown (PRD-FORMAT-SPECIFICATION)          | Product requirements completo                                     |
| **Architecture Document** | @architect | Markdown (ARCHITECTURE-FORMAT-SPECIFICATION) | System components, interactions, infrastructure                   |

#### Fase 2: DEVELOPMENT (Execution Engine)

| Artefato                | Agente | Formato                                          | Descrição                                                           |
| ----------------------- | ------ | ------------------------------------------------ | ------------------------------------------------------------------- |
| **Development Stories** | @sm    | `docs/stories/*.md` (STORY-FORMAT-SPECIFICATION) | Hiper-detalhadas com contexto completo, ACs, implementation details |
| **Source Code**         | @dev   | Language-specific                                | Implementação                                                       |

#### Fase 3: QA

| Artefato                     | Agente | Formato         | Descrição                                       |
| ---------------------------- | ------ | --------------- | ----------------------------------------------- |
| **QA Review / Build Review** | @qa    | Markdown/Report | Validação contra specs                          |
| **Violation Findings**       | @qa    | Report          | Issues de qualidade, input para recovery system |

### 2.3 Configuração Multi-IDE

| IDE         | Localização                        | Formato         |
| ----------- | ---------------------------------- | --------------- |
| Claude Code | `.claude/CLAUDE.md` ou `AGENTS.md` | Markdown        |
| Cursor      | `.cursor/rules/`                   | YAML/Rule       |
| Codex       | `.codex/`                          | AGENTS.md       |
| Gemini      | `.gemini/`                         | Format-specific |

### 2.4 Squad System (extensibilidade por domínio)

Cada Squad contém:

| Componente   | Diretório | Descrição                                                     |
| ------------ | --------- | ------------------------------------------------------------- |
| `squad.yaml` | raiz      | Manifest: metadata, version, dependencies, config inheritance |
| `agents/`    |           | Agentes domain-specific                                       |
| `tasks/`     |           | Task workflows domain-specific                                |
| `workflows/` |           | Multi-step orchestrations                                     |
| `templates/` |           | Document generation templates                                 |
| `tools/`     |           | Custom tool integrations (JS)                                 |
| `scripts/`   |           | Utility automation                                            |
| `data/`      |           | Static config e reference data                                |

**3 níveis de distribuição:** LOCAL (./squads/), PUBLIC (github), MARKETPLACE (api.synkra.dev)

### 2.5 Format Specifications (obrigatórios)

- `TASK-FORMAT-SPECIFICATION-V1` — para tasks
- `PRD-FORMAT-SPECIFICATION` — para PRDs
- `ARCHITECTURE-FORMAT-SPECIFICATION` — para architecture docs
- `STORY-FORMAT-SPECIFICATION` — para development stories

### 2.6 Project Templates

- **default** — Full SDLC pipeline
- **minimal** — Lightweight
- **enterprise** — Extended governance

---

## 3. Comparação Detalhada por Dimensão

### 3.1 Ciclo de Vida do Artefato

```
BMAD:     Brief → PRD (shardable) → Architecture (shardable) → Epics → Impl. Readiness [GATE]
          → Stories → sprint-status.yaml → Code → PR + QA Report [GATE] → Merge

AIOX:     Planning Brief → PRD → Architecture → Stories → Code → QA Review → Working Code
          (+ Recovery System para violações)

OpenAI:   AGENTS.md (mapa) → ExecPlan → Code → Golden Principles + Linters → QUALITY_SCORE.md
          (+ progress.json para handoff entre sessões)

Proposta: AGENTS.md → Feature Brief → Spec → Execution Plan → ADR → Code → (sem gate formal)
```

### 3.2 O que cada framework faz que os outros não fazem

| Capability                        | BMAD                  | AIOX                  | OpenAI                          | Nossa Proposta         |
| --------------------------------- | --------------------- | --------------------- | ------------------------------- | ---------------------- |
| **Sharding de docs grandes**      | ✅ PRD + Architecture | ❌                    | ❌                              | ❌                     |
| **Agent-as-code portável**        | ✅ YAML compilável    | ✅ Multi-IDE          | ❌ (Codex-only)                 | ❌                     |
| **Implementation Readiness gate** | ✅ Workflow dedicado  | ❌                    | ❌                              | ❌                     |
| **sprint-status.yaml**            | ✅                    | ❌                    | progress.json                   | ❌                     |
| **Squad extensibility**           | Módulos (BMM, BMB)    | ✅ Squads marketplace | ❌                              | ❌                     |
| **Quality grades por domínio**    | ❌                    | ❌                    | ✅ QUALITY_SCORE.md             | ❌                     |
| **Enforcement mecânico**          | Husky + lint-staged   | Checklists            | ✅ Linters + testes estruturais | ❌                     |
| **Data & Analytics Contract**     | ❌                    | ❌                    | ❌                              | ✅ (proposta anterior) |
| **Semantic Data Artifacts**       | ❌                    | ❌                    | ❌                              | ✅ (7 artefatos)       |
| **Context cache / pipeline docs** | ❌                    | ❌                    | ❌                              | ✅ (já existem)        |
| **UX Spec dedicado**              | ✅ Template           | ❌                    | ❌                              | ❌                     |
| **Tech Writer agent**             | ✅                    | ❌                    | ❌                              | ❌                     |
| **Recovery System (auto-fix)**    | ❌                    | ✅                    | ❌                              | ❌                     |

### 3.3 Gaps Críticos na Proposta Anterior

1. **Sem gates formais** — BMAD tem Implementation Readiness como gate obrigatório entre Plan e Build. Nós não temos nada equivalente.
2. **Sem sprint tracking** — BMAD tem `sprint-status.yaml`, OpenAI tem `progress.json`. Nós não temos mecanismo de handoff entre sessões de agente.
3. **Sem checklists de validação** — BMAD tem 6+ checklists. Nós temos zero.
4. **Sem Format Specifications** — AIOX define specs obrigatórias para cada tipo de doc (PRD-FORMAT-SPEC, STORY-FORMAT-SPEC). Nós não temos.
5. **Templates são genéricos** — Nossos Feature Brief e Spec são "one size fits all". BMAD tem 13+ templates especializados.
6. **Sem agent definitions** — Tanto BMAD quanto AIOX definem agentes como código versionável. Nós não.
7. **Sem project-context.md** — BMAD tem a "constituição" do projeto que todos os agentes downstream usam. Nós temos CLAUDE.md mas é focado em infra, não em regras de produto.

---

## 4. Proposta Revisada: Padrão de Documentos para ETUS

Baseado nos pontos fortes de cada framework, combinados com nossas necessidades específicas (monorepo multi-produto, pipeline de dados, arbitragem).

### 4.1 Estrutura de Diretórios

```
docs/
├── AGENTS.md                           # Mapa curto (~100 linhas) - OpenAI style
├── project-context.md                  # "Constituição" - BMAD style
│
├── products/                           # Um dir por produto ETUS
│   ├── ets-analytics/
│   │   ├── prd.md                      # PRD do produto
│   │   ├── architecture.md             # Architecture doc
│   │   └── epics/                      # Epics deste produto
│   │       └── epic-N-<name>.md
│   ├── quizmaker/
│   ├── pagemaker/
│   ├── tiktok-tool/
│   ├── dash-v0/
│   └── gam-automations/
│
├── specs/                              # Specs executáveis (features cross-product ou específicas)
│   └── SPEC-NNN-<name>.md
│
├── stories/                            # Stories hiper-detalhadas - BMAD style
│   └── STORY-NNN-<name>.md
│
├── architecture/
│   ├── decisions/                      # ADRs (já existem 39)
│   │   └── ADR-NNN-<name>.md
│   └── system/                         # Architecture docs transversais
│       ├── data-platform.md
│       ├── edge-layer.md
│       └── identity-resolution.md
│
├── data/                               # Semantic Data Artifacts (nosso diferencial)
│   ├── metric-catalog.md
│   ├── entity-model.md
│   ├── field-dictionary.md
│   ├── source-of-truth.md
│   ├── attribution-model.md
│   ├── tracking-plan.md
│   └── source-cost-inventory.md
│
├── quality/                            # Quality gates - inspirado BMAD + OpenAI
│   ├── QUALITY_SCORE.md                # Grades por domínio - OpenAI style
│   ├── checklists/
│   │   ├── prd-checklist.md
│   │   ├── architecture-checklist.md
│   │   ├── story-checklist.md
│   │   ├── implementation-readiness.md
│   │   ├── code-review-checklist.md
│   │   └── data-contract-checklist.md  # Nosso (específico para data pipeline)
│   └── format-specs/                   # Format Specifications - AIOX style
│       ├── PRD-FORMAT-SPEC.md
│       ├── SPEC-FORMAT-SPEC.md
│       ├── STORY-FORMAT-SPEC.md
│       ├── EPIC-FORMAT-SPEC.md
│       ├── ADR-FORMAT-SPEC.md
│       └── DATA-ARTIFACT-FORMAT-SPEC.md
│
├── templates/                          # Templates executáveis - BMAD style
│   ├── prd-template.md
│   ├── spec-template.md
│   ├── story-template.md
│   ├── epic-template.md
│   ├── adr-template.md
│   ├── architecture-template.md
│   ├── data-contract-template.md       # Nosso
│   └── qa-report-template.md
│
├── plans/                              # ExecPlans (work-in-progress) - OpenAI style
│   └── PLAN-YYYY-MM-DD-<name>.md
│
├── progress/                           # Session handoff - BMAD + OpenAI hybrid
│   ├── sprint-status.yaml              # BMAD style
│   └── features.json                   # Anthropic style
│
└── internal/                           # Docs operacionais (já existem)
    ├── data/
    ├── sdlc/
    └── runbooks/
```

### 4.2 Workflow Completo (5 Fases)

```
FASE 1: DISCOVER
  Input:  Ideia, problema, oportunidade
  Output: Product Brief (brainstorming guiado)
  Gate:   Nenhum (exploratório)

FASE 2: PLAN
  Input:  Product Brief
  Output: PRD → Architecture → Epics → project-context.md
  Gate:   ✅ Implementation Readiness Checklist
          (valida: PRD completo? Architecture coerente? Epics cobrem PRD? Data contracts definidos?)

FASE 3: SOLUTION
  Input:  Epics + Architecture + project-context.md
  Output: Stories hiper-detalhadas + sprint-status.yaml
  Gate:   ✅ Story Validation Checklist
          (valida: ACs testáveis? Tasks < 1 dev-day? Dependencies mapeadas?)

FASE 4: BUILD
  Input:  Story + sprint-status.yaml
  Output: Feature branch code + tests
  Gate:   ✅ Code Review Checklist + QA Report
          (valida: ACs cobertos? Testes passam? Data contract implementado?)

FASE 5: VERIFY & LEARN
  Input:  Code merged
  Output: QUALITY_SCORE.md atualizado, sprint-status.yaml atualizado
  Gate:   ✅ Quality Score não degradou
```

### 4.3 Diferencial ETUS: Data Contract Obrigatório

Bloco obrigatório em TODA Spec e Story que toca dados:

````markdown
## Data Contract

### Events

| Event | Properties | Trigger |
| ----- | ---------- | ------- |
| ...   | ...        | ...     |

### Métricas Afetadas

| Métrica | Tabela CH | Query de validação |
| ------- | --------- | ------------------ |
| ...     | ...       | ...                |

### Schema Changes

- [ ] Novos campos no ClickHouse?
- [ ] Novo tópico Redpanda?
- [ ] Atualização no tracking-plan?
- [ ] Atualização no field-dictionary?

### Validação

```sql
-- Query que prova que o data contract está funcionando
SELECT ...
```
````

````

### 4.4 Format Specs (como AIOX)

Cada tipo de documento tem um FORMAT-SPEC que define:

1. **Seções obrigatórias** — o que DEVE existir
2. **Seções opcionais** — o que PODE existir
3. **Validation rules** — critérios de completude
4. **Exemplos** — bom vs ruim
5. **Anti-patterns** — o que NÃO fazer

Isso elimina ambiguidade. Quando um agente (ou humano) cria um PRD, ele segue o PRD-FORMAT-SPEC. Quando revisa, usa o prd-checklist.

### 4.5 Sprint Status (como BMAD)

```yaml
# docs/progress/sprint-status.yaml
sprint: "2026-W11"
goal: "Event Writer dual-insert reliability"
product: "ets-analytics"

epics:
  - id: "epic-3-pipeline-reliability"
    status: "in-progress"
    stories:
      - id: "STORY-042"
        title: "Per-table insert limiters"
        status: "done"
        completed: "2026-02-28"
      - id: "STORY-043"
        title: "DLQ replay mechanism"
        status: "in-progress"
        assignee: "agent"
        blockers: []
      - id: "STORY-044"
        title: "Retention policy automation"
        status: "ready"
        depends_on: ["STORY-043"]

next_story: "STORY-043"
````

---

## 5. Resumo: O Que Pegamos de Cada Framework

| De quem    | O que pegamos                                | Por que                                                                |
| ---------- | -------------------------------------------- | ---------------------------------------------------------------------- |
| **BMAD**   | Stories hiper-detalhadas com task→AC mapping | Agentes precisam de contexto completo para implementar sem ambiguidade |
| **BMAD**   | sprint-status.yaml                           | Handoff entre sessões de agente                                        |
| **BMAD**   | Implementation Readiness gate                | Previne entrar em build com specs incompletas                          |
| **BMAD**   | 13+ templates especializados                 | Consistência. Cada tipo de doc tem sua estrutura                       |
| **BMAD**   | 6+ quality checklists                        | Gates mecânicos > revisão manual                                       |
| **BMAD**   | project-context.md                           | "Constituição" que todos os agentes downstream respeitam               |
| **AIOX**   | Format Specifications por tipo de doc        | Elimina ambiguidade sobre o que é um PRD "completo"                    |
| **AIOX**   | Task-first architecture                      | Workflows definidos como tasks encadeáveis                             |
| **AIOX**   | Squad system (conceito)                      | Extensibilidade por domínio/produto                                    |
| **OpenAI** | AGENTS.md como mapa curto                    | Contexto é recurso escasso                                             |
| **OpenAI** | QUALITY_SCORE.md                             | Grades por domínio, atualizadas automaticamente                        |
| **OpenAI** | ExecPlans                                    | Docs de design autocontidos para features complexas                    |
| **OpenAI** | Enforcement mecânico                         | Linters e testes > instruções em prosa                                 |
| **Nosso**  | Data Contract obrigatório                    | Nenhum framework tem isso. Nós precisamos porque somos data-first      |
| **Nosso**  | 7 Semantic Data Artifacts                    | metric-catalog, entity-model, etc. Específico para analytics           |
| **Nosso**  | Pipeline docs (já existentes)                | event-catalog, column-reference, schema docs                           |
| **Nosso**  | Estrutura products/                          | Multi-produto (Quizmaker, Pagemaker, etc.)                             |

---

## Fontes

- https://github.com/bmad-code-org/BMAD-METHOD
- https://docs.bmad-method.org/reference/workflow-map/
- https://docs.bmad-method.org/tutorials/getting-started/
- https://medium.com/@visrow/bmad-method-and-agent-as-code-scaling-federated-knowledge-architecture-d85e5fe682cb
- https://medium.com/@visrow/what-is-bmad-method-a-simple-guide-to-the-future-of-ai-driven-development-412274f91419
- https://github.com/SynkraAI/aiox-core
- https://github.com/SynkraAI/aios-core/blob/main/docs/guides/squads-overview.md
- https://github.com/SynkraAI/aios-core/blob/main/docs/guides/user-guide.md
- https://github.com/SynkraAI/aios-core/blob/main/docs/FEATURE_PROCESS.md
- https://www.theaistack.dev/p/bmad
- https://buildmode.dev/blog/mastering-bmad-method-2025/
