# Avaliação Crítica: Solo-Templates vs BMAD vs Superpowers

**Data:** 2026-03-13
**Objetivo:** Identificar o que é excessivo, o que falta, e propor uma lista definitiva de documentos com QUANDO e POR QUE.

---

## 1. Diagnóstico Honesto do Solo-Templates

### O que funciona bem

| Aspecto                         | Valor Real                                            |
| ------------------------------- | ----------------------------------------------------- |
| ids.yml com regex + lint rules  | Rastreabilidade forte (BO→PRD-F→ep→US→FR→NFR)         |
| SST enforcement                 | Evita duplicação de definições (dict._, tok._, ev.\*) |
| Gate reviews (GO/NO-GO/ITERATE) | Força decisão explícita antes de avançar              |
| 5W2H no Discovery               | Estrutura sistemática para explorar o problema        |
| HMW + MoSCoW no Define          | Transforma problemas em features priorizadas          |
| Bash validation nos commands    | Verificação automatizada (grep-based)                 |

### O que está over-engineered

| Problema                           | Evidência                                                                                                                | Impacto                                                                               |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| **44 comandos para um dev solo**   | 26 individuais + 6 grouped + 3 validation + 4 utility + 4 workflow + 1 orchestrator                                      | Paralisia de escolha. BMAD tem ~13 templates e já é considerado completo              |
| **25+ documentos obrigatórios**    | Mais que equipes de 10 pessoas produzem                                                                                  | Um dev solo vai gastar mais tempo documentando do que construindo                     |
| **7 documentos de Data separados** | data-requirements, erd, database-requirements, database-schema, data-dictionary, data-flow-diagram, data-catalog         | Para um MVP, 2-3 bastam (ERD + schema + dictionary). O resto é overhead de enterprise |
| **8 documentos de UX separados**   | jtbd, user-journey, ux-sitemap, ux-design-decisions, design-requirements, wireframes, style-guide, frontend-requirements | Metade destes pode ser seção de um doc maior                                          |
| **Orchestrator de 54KB**           | SKILL.md do orchestrator é enorme                                                                                        | Complexidade que dificulta manutenção e debug                                         |
| **5 gates formais**                | Discover, Define, Develop, Deliver, Release                                                                              | 3 seriam suficientes para solo dev (Discovery, Planning, Implementation Readiness)    |
| **IDs separados para tudo**        | ep-#, US-#, FR-#, NFR-#, ADR-#, be-ep-#, dict._, ev._, tok._, cmp._, view.\*, r:/                                        | Manter 12+ namespaces de IDs é trabalho de registrar, não de construir                |

### O que está faltando (gaps críticos)

| Gap                                     | O que BMAD faz                                                   | O que Superpowers faz                                                          | Solo-Templates                                                           |
| --------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| **Behavioral enforcement**              | Checklists obrigatórios por fase                                 | TDD enforcement (RED→GREEN→REFACTOR), 2-stage review, "no code without design" | Zero. Gera docs mas não garante que sejam seguidos                       |
| **project-context.md ("constituição")** | Documento central que todo agente consulta antes de agir         | N/A (usa spec como base)                                                       | Não existe. Cada skill opera com conhecimento parcial                    |
| **PRD sharding**                        | Divide PRD em shards de ~650 linhas para caber no context window | N/A                                                                            | PRD monolítico. Em projetos grandes, estoura o contexto                  |
| **Sprint/iteration tracking**           | sprint-status.yaml com estado de cada story                      | Subagent dispatch com progresso por task                                       | Nenhum tracking de execução. Docs gerados = fim do ciclo                 |
| **Implementation Readiness gate**       | Gate específico entre planning e coding com checklist técnico    | Spec approval obrigatório antes de qualquer código                             | Não tem. O "Develop Gate" é sobre docs, não sobre readiness para codar   |
| **Subagent dispatch**                   | N/A                                                              | Cada task roda em contexto limpo (worktree isolado)                            | N/A. Tudo roda no mesmo contexto                                         |
| **Spec-as-conversation**                | Entrevista interativa para extrair requisitos                    | Brainstorm→Plan→Implement→Complete com aprovação em cada passo                 | Tem 5W2H, mas falta a disciplina de "não avança sem aprovação explícita" |
| **Code quality enforcement**            | TEA agent com checklists                                         | 2-stage review (spec compliance + code quality)                                | Zero. O sistema termina quando os docs estão prontos                     |
| **Rollback/iteration protocol**         | Pode voltar a qualquer fase                                      | Task pode ser rejeitada e refeita                                              | Gates permitem ITERATE mas sem protocolo claro de o que mudar            |
| **Task decomposition**                  | Stories com tasks e AC mapeados                                  | ExecPlans com steps numerados e critérios de done                              | Stories têm Given/When/Then mas sem decomposição em tasks                |
| **Living document updates**             | sprint-status.yaml evolui a cada sprint                          | progress.json atualizado por task                                              | Docs são gerados uma vez e ficam estáticos                               |

---

## 2. Análise por Documento: Manter, Fundir ou Eliminar

### Legenda de decisão

- **MANTER** = documento essencial, vale a complexidade
- **FUNDIR** = conteúdo válido, mas deve ser seção de outro doc
- **ELIMINAR** = baixo ROI para dev solo, gera mais overhead que valor
- **ADICIONAR** = não existe no Solo-Templates, precisa ser criado

### Discovery Phase (atualmente 2 docs)

| #   | Documento             | Decisão         | Justificativa                                                                                          |
| --- | --------------------- | --------------- | ------------------------------------------------------------------------------------------------------ |
| 1   | **product-vision.md** | MANTER          | Fundamental. 5W2H + NSM + kill criteria. É o "norte" do projeto                                        |
| 2   | **brd.md**            | FUNDIR → vision | Para solo dev, business objectives (BO-#) podem ser seção da vision. BRD formal é artefato corporativo |

**Resultado: 1 documento (vision com seção de business case)**

### Define Phase (atualmente 4 docs)

| #   | Documento           | Decisão                              | Justificativa                                                                                                                                                                                                                                                                     |
| --- | ------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 3   | **prd.md**          | MANTER (com sharding)                | Core do sistema. Adotar sharding do BMAD (~650 linhas por shard) para projetos grandes                                                                                                                                                                                            |
| 4   | **epics.md**        | FUNDIR → prd                         | Epics são seção do PRD, não documento separado. BMAD e AIOX fazem isso                                                                                                                                                                                                            |
| 5   | **user-stories.md** | MANTER (com tasks)                   | Essencial. Mas adicionar decomposição em tasks + AC mapping como BMAD faz                                                                                                                                                                                                         |
| 6   | **frd.md**          | EVOLUIR → **feature-spec-[nome].md** | O conceito é válido: features complexas precisam de spec individual com business rules, state machines, edge cases e integrations. Renomear de "FRD" (corporativo) para "feature-spec" (indústria). 1 doc por feature, gerado sob demanda — não obrigatório para features simples |

**Resultado: 3 documentos (PRD com epics, User Stories com tasks, Feature Specs por feature)**

> **Feature Spec vs User Story — quando usar cada um:**
>
> - **User Story** = O que o usuário quer + como validamos (Given/When/Then). Foco no comportamento observável.
> - **Feature Spec** = Business rules, state machines, error handling, edge cases, integrations. Foco na lógica de domínio.
> - **Regra prática:** se a feature tem >3 business rules ou um state machine, merece um feature-spec. Se é CRUD simples, a story basta.
> - **Exemplo ETS:** "Context Merge" tem 200K entry cache, TTL 5min, 4 instâncias paralelas, 15 campos CWV — claramente merece um feature-spec. "Exibir lista de domínios no Admin" — story basta.

### Develop Phase (atualmente 3 docs)

| #   | Documento                   | Decisão              | Justificativa                                                                              |
| --- | --------------------------- | -------------------- | ------------------------------------------------------------------------------------------ |
| 7   | **srs.md**                  | FUNDIR → tech-spec   | NFRs são seção do tech spec, não documento separado. Um solo dev não precisa de SRS formal |
| 8   | **architecture-diagram.md** | MANTER               | C4 diagrams são referência visual essencial                                                |
| 9   | **tech-spec.md**            | MANTER (absorve SRS) | Documento técnico central: stack + NFRs + ADRs + deployment                                |

**Resultado: 2 documentos (architecture + tech-spec com NFRs)**

### Data Phase (atualmente 7 docs)

> **Contexto crítico:** Para a ETUS, dados são o produto. O ETS processa milhões de eventos/dia, tem 868 colunas em 5 tabelas ClickHouse, pipeline de 8 estágios, 17 tópicos Redpanda e 148 eventos catalogados. Cortar docs de data de um produto data-intensive seria como cortar docs de API de uma API company.

| #   | Documento                    | Decisão                       | Justificativa                                                                                                                                                                                                  |
| --- | ---------------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 10  | **data-requirements.md**     | MANTER                        | No ETS, requisitos de dados **são** requisitos de produto: quais eventos coletar, qual granularidade, latência aceitável, campos obrigatórios, quality thresholds. Não está no PRD                             |
| 11  | **erd.md**                   | MANTER                        | Modelo ER das 5 tabelas + relações entre entidades. Referência visual indispensável                                                                                                                            |
| 12  | **database-requirements.md** | FUNDIR → **database-spec.md** | Para ClickHouse, constraints de performance são críticos (ORDER BY keys, TTLs, ReplacingMergeTree, partition strategy). Mas não precisa ser separado do schema — fundir DDL + constraints + performance config |
| 13  | **database-schema.md**       | FUNDIR → **database-spec.md** | DDL + constraints em um doc só. SST para schema físico                                                                                                                                                         |
| 14  | **data-dictionary.md**       | MANTER                        | 868 colunas precisam de definição formal. dict._ (fields) + ev._ (events) + PII classification                                                                                                                 |
| 15  | **data-flow-diagram.md**     | MANTER                        | Com 8 estágios de pipeline e 17 tópicos, o DFD é a documentação mais consultada no dia a dia. Complexo demais para ser seção de outro doc                                                                      |
| 16  | **data-catalog.md**          | MANTER                        | 148 eventos, 69 ativos, status por módulo (OK/Not Yet/Planned). O `event-catalog-complete.md` existente prova o valor — é referência contínua                                                                  |

**Resultado: 6 documentos (data-requirements + ERD + database-spec + dictionary + DFD + catalog)**

### UX Phase (atualmente 8 docs)

| #   | Documento                    | Decisão            | Justificativa                                                       |
| --- | ---------------------------- | ------------------ | ------------------------------------------------------------------- |
| 17  | **jtbd.md**                  | FUNDIR → vision    | Personas e JTBD são seção do product-vision                         |
| 18  | **user-journey.md**          | MANTER             | Journey maps revelam gaps que nenhum outro doc captura              |
| 19  | **ux-sitemap.md**            | MANTER             | Inventário de rotas e views é essencial para frontend               |
| 20  | **ux-design-decisions.md**   | ELIMINAR           | Decisões de UX ficam melhor como ADRs no tech-spec (UXDD-# → ADR-#) |
| 21  | **design-requirements.md**   | ELIMINAR           | Component specs são parte do style-guide ou frontend-req            |
| 22  | **wireframes.md**            | MANTER             | ASCII wireframes são referência rápida para implementação           |
| 23  | **style-guide.md**           | MANTER             | tok.\* são Single Source. Design tokens são referência contínua     |
| 24  | **frontend-requirements.md** | FUNDIR → tech-spec | Reqs de frontend são seção do tech-spec (stack, routing, state)     |

**Resultado: 4 documentos (journey + sitemap + wireframes + style-guide)**

### Backend (atualmente 1 doc)

| #   | Documento                   | Decisão                      | Justificativa                                         |
| --- | --------------------------- | ---------------------------- | ----------------------------------------------------- |
| 25  | **backend-requirements.md** | MANTER (renomear → api-spec) | Endpoints, auth, errors. Essencial para implementação |

**Resultado: 1 documento (api-spec)**

### Novos Documentos (inspirados em BMAD + Superpowers)

| #   | Documento                  | Fonte                     | QUANDO                                                    | POR QUE                                                                                                                                                      |
| --- | -------------------------- | ------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| N1  | **project-context.md**     | BMAD                      | Antes de tudo. Atualizado continuamente                   | "Constituição" do projeto. Todo agente/skill consulta antes de agir. Contém: visão em 1 frase, stack decidido, constraints, glossário, decisões-chave        |
| N2  | **feature-spec-[nome].md** | Solo-Templates (evoluído) | Quando uma feature tem >3 business rules ou state machine | Spec individual por feature complexa: business rules, states, edge cases, integrations. Equivale ao PRD shard do BMAD. Não obrigatório para features simples |
| N3  | **implementation-plan.md** | Superpowers + BMAD        | Após tech-spec, antes de codar                            | Decompõe stories em tasks ordenadas com critérios de done. Equivale ao ExecPlan do OpenAI Harness. Sem isso, não começa implementação                        |
| N4  | **sprint-status.yaml**     | BMAD                      | Durante implementação                                     | Tracking de progresso por story/task. Status: not-started/in-progress/blocked/done. Evolui a cada sessão                                                     |
| N5  | **quality-checklist.md**   | BMAD + Superpowers        | Pré-merge/deploy                                          | Checklist de qualidade: spec compliance, tests passando, a11y, perf budget, security basics. Sem check = não mergeia                                         |

---

## 3. Lista Definitiva: 22 Documentos

De 25+ para 22. Redução cirúrgica que preserva profundidade em dados (core da ETUS) e adiciona feature-specs + enforcement behavioral.

### Setup (1 doc)

| #   | Documento              | QUANDO gerar                                 | POR QUE ter                                                                                                                          | Complexidade |
| --- | ---------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| 1   | **project-context.md** | Primeiro documento. Atualizado continuamente | "Constituição" do projeto. Todo agente/skill consulta antes de agir. Visão em 1 frase, stack, constraints, glossário, decisões-chave | Simples      |

### Discovery (1 doc)

| #   | Documento             | QUANDO gerar                      | POR QUE ter                                                                                                               | Complexidade |
| --- | --------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------ |
| 2   | **product-vision.md** | Quando surge uma ideia de produto | Define o problema, público, mercado, métricas. Inclui JTBD, business case (BO-#), kill criteria. Absorve brd.md e jtbd.md | Médio        |

### Planning (3 docs + N feature-specs)

| #   | Documento                  | QUANDO gerar                                          | POR QUE ter                                                                                                                                                              | Complexidade |
| --- | -------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| 3   | **prd.md** (com sharding)  | Após vision aprovada                                  | Features priorizadas (MoSCoW), HMW statements, epics embutidos. Shard quando >650 linhas                                                                                 | Complexo     |
| 4   | **user-stories.md**        | Após PRD aprovado                                     | Stories com Given/When/Then + decomposição em tasks + AC mapping. SST para acceptance criteria                                                                           | Complexo     |
| 5   | **feature-spec-[nome].md** | Quando feature tem >3 business rules ou state machine | Spec individual por feature complexa: business rules, states, edge cases, error handling, integrations. 1 por feature, sob demanda. Features simples (CRUD) não precisam | Complexo     |

> **Quantos feature-specs?** Depende do projeto. ETS provavelmente teria ~8-10 (Context Merge, Event Tracker, Interceptor, Bot Detection, Normalizer, Enricher, Projector, Writer, Raw Archiver). Um app CRUD simples pode ter zero.

### Design (2 docs)

| #   | Documento                   | QUANDO gerar           | POR QUE ter                                                                                 | Complexidade |
| --- | --------------------------- | ---------------------- | ------------------------------------------------------------------------------------------- | ------------ |
| 6   | **architecture-diagram.md** | Após stories definidas | C4 diagrams + deployment diagram. Referência visual para arquitetura                        | Médio        |
| 7   | **tech-spec.md**            | Junto com architecture | Stack, NFRs com targets (absorve srs.md), ADRs, deployment strategy, frontend/backend split | Complexo     |

### Data (6 docs)

| #   | Documento                | QUANDO gerar                           | POR QUE ter                                                                                                                                     | Complexidade |
| --- | ------------------------ | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| 8   | **data-requirements.md** | Quando dados são parte core do produto | Quais dados coletar, latência aceitável, granularidade, quality thresholds, campos obrigatórios. Para a ETUS isso é tão importante quanto o PRD | Médio        |
| 9   | **erd.md**               | Quando domínio tem >3 entidades        | Modelo ER com relacionamentos. Referência visual indispensável                                                                                  | Médio        |
| 10  | **database-spec.md**     | Após ERD aprovado                      | DDL + ORDER BY + TTLs + partitioning + constraints. Fusão de schema + requirements. SST para schema físico                                      | Médio        |
| 11  | **data-dictionary.md**   | Junto com database-spec                | dict._ (868 field definitions) + ev._ (148 event definitions) + PII classification                                                              | Médio        |
| 12  | **data-flow-diagram.md** | Quando pipeline tem >2 estágios        | Pipeline visual: quem produz → tópico → transformação → quem consome. Com 8 estágios no ETS, é o doc mais consultado                            | Médio        |
| 13  | **data-catalog.md**      | Quando tem >20 eventos/métricas        | Inventário de eventos com status (OK/Not Yet/Planned), módulo, trigger. O event-catalog-complete.md do ETS já prova o valor                     | Médio        |

### UX (4 docs)

| #   | Documento           | QUANDO gerar                     | POR QUE ter                                                                 | Complexidade |
| --- | ------------------- | -------------------------------- | --------------------------------------------------------------------------- | ------------ |
| 14  | **user-journey.md** | Após vision, antes de wireframes | Journey maps com pain points e oportunidades. Revela gaps invisíveis no PRD | Médio        |
| 15  | **ux-sitemap.md**   | Após PRD + stories               | Inventário de rotas, views, estados de UI. Mapa de navegação                | Médio        |
| 16  | **wireframes.md**   | Após sitemap                     | Layouts ASCII por tela. Referência rápida para implementação                | Médio        |
| 17  | **style-guide.md**  | Antes de implementar frontend    | Design tokens (tok.\*). SST para cores, tipografia, espaçamento             | Médio        |

### Implementation (2 docs)

| #   | Documento                  | QUANDO gerar                   | POR QUE ter                                                                                           | Complexidade |
| --- | -------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------- | ------------ |
| 18  | **api-spec.md**            | Após tech-spec + database-spec | Endpoints com request/response, auth, errors, rate limits                                             | Complexo     |
| 19  | **implementation-plan.md** | Após todos os docs de design   | Tasks ordenadas com critérios de done. Gate de Implementation Readiness. Sem plan aprovado = não coda | Médio        |

### Execution (2 docs)

| #   | Documento                | QUANDO gerar              | POR QUE ter                                                                                       | Complexidade |
| --- | ------------------------ | ------------------------- | ------------------------------------------------------------------------------------------------- | ------------ |
| 20  | **sprint-status.yaml**   | Ao iniciar implementação  | Tracking de progresso por story/task. Atualizado a cada sessão de trabalho                        | Simples      |
| 21  | **quality-checklist.md** | Pré-merge de cada feature | Spec compliance + tests + a11y + perf + security. Enforcement behavioral. Sem check = não mergeia | Simples      |

### O que foi cortado (6 documentos eliminados ou fundidos)

| Documento                | Destino                                                |
| ------------------------ | ------------------------------------------------------ |
| brd.md                   | Absorvido pela product-vision.md (seção Business Case) |
| epics.md                 | Absorvido pelo prd.md (seção Epics)                    |
| srs.md                   | Absorvido pelo tech-spec.md (seção NFRs)               |
| jtbd.md                  | Absorvido pela product-vision.md (seção JTBD)          |
| database-requirements.md | Fundido com database-schema → database-spec.md         |
| database-schema.md       | Fundido com database-requirements → database-spec.md   |
| ux-design-decisions.md   | Decisões UX viram ADRs no tech-spec                    |
| design-requirements.md   | Specs de componentes vão no style-guide                |
| frontend-requirements.md | Reqs frontend são seção do tech-spec                   |

---

## 4. Mudanças Estruturais (Além dos Documentos)

### 4.1 Gates: de 5 para 3

| Gate                         | QUANDO                         | O que valida                                                                            |
| ---------------------------- | ------------------------------ | --------------------------------------------------------------------------------------- |
| **Discovery Gate**           | Após vision                    | Problema claro? Público definido? Métricas identificadas? Kill criteria? Vale investir? |
| **Planning Gate**            | Após PRD + stories + tech-spec | Requirements completos? Traceability ok? Architecture sound? Scope achievable?          |
| **Implementation Readiness** | Após implementation-plan       | Tasks decompostas? Critérios de done claros? Quality checklist definido? Pode codar?    |

**Eliminados:** Deliver Gate (subsumed pelo Planning Gate) e Release Gate (substituído pelo quality-checklist contínuo).

### 4.2 IDs: de 12+ namespaces para 8

| ID          | Formato               | Onde vive              |
| ----------- | --------------------- | ---------------------- |
| BO-#        | Business Objective    | product-vision.md      |
| PRD-F-#     | Feature               | prd.md                 |
| US-#        | User Story            | user-stories.md        |
| FS-[nome]-# | Feature Spec Rule     | feature-spec-[nome].md |
| NFR-#       | Non-Functional Req    | tech-spec.md           |
| ADR-#       | Architecture Decision | tech-spec.md           |
| dict.\*     | Field Definition      | data-dictionary.md     |
| ev.\*       | Event Definition      | data-dictionary.md     |

**Eliminados:** ep-# (epics são seção do PRD), FR-# (redundante com US + feature-specs), be-ep-# (endpoints no api-spec sem ID formal), tok._ (design tokens usam nomes CSS nativos), cmp._/view.\*/r:/ (overhead de registrar componentes/rotas como IDs formais).

### 4.3 Commands: de 44 para ~15

Princípio: cada documento = 1 comando. Mais 3-4 de workflow/validation.

```
# Workflow (3)
/discover [idea]       → Gera project-context + vision
/plan                  → Gera PRD + stories + architecture + tech-spec
/design                → Gera data docs + UX docs + api-spec

# Individual (14 — só quando precisa de 1 doc isolado)
/vision, /prd, /stories, /feature-spec [nome], /architecture, /tech-spec
/data-reqs, /erd, /db-spec, /dictionary, /dfd, /catalog
/api-spec, /wireframes

# Execution (2)
/implementation-plan   → Gera plan com tasks
/sprint-status         → Atualiza tracking

# Validation (2)
/validate [gate-name]  → Gate review
/check-quality         → Quality checklist
```

### 4.4 Behavioral Enforcement (o gap mais crítico)

O que Superpowers prova: **documentos sem enforcement são sugestões, não regras.**

Adicionar ao sistema:

1. **"No code without approved spec"** — implementation-plan.md deve existir e estar aprovado antes de qualquer código
2. **Quality gate por PR** — quality-checklist.md é obrigatório antes de merge. Não é sugestão
3. **Sprint tracking vivo** — sprint-status.yaml atualizado a cada sessão. Se está desatualizado >2 sessões, o sistema avisa
4. **Spec compliance review** — ao terminar uma task, verificar se o código implementa o que a story especificou (Given/When/Then)

---

## 5. Resumo Executivo

### Antes (Solo-Templates)

- 25+ documentos fixos
- 44 comandos
- 5 gates
- 12+ namespaces de IDs
- 7 skills + 1 orchestrator
- Zero enforcement behavioral
- Zero tracking de execução
- FRD com nome corporativo

### Depois (Proposta)

- **21 documentos base + N feature-specs sob demanda** (redução de ~16% em base, mas com profundidade onde importa)
- **~21 comandos** (redução de 52%)
- **3 gates** (redução de 40%)
- **8 namespaces de IDs** (redução de 33%)
- **4 regras de enforcement** (de zero)
- **Sprint tracking vivo** (de zero)
- **project-context.md** como constituição (de zero)
- **Feature-specs** para features complexas (evolução do FRD)
- **6 docs de Data** preservados (core business da ETUS)

### O que mudou em relação à v1 desta avaliação

| Mudança                                                    | Motivo                                                                                                                                    |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| FRD evoluiu para feature-spec-[nome].md                    | Conceito válido — features complexas precisam de spec individual com business rules/states/edge cases. Renomeado para padrão da indústria |
| Data docs restaurados (3 → 6)                              | Para a ETUS, dados são o produto. Cortar docs de data seria como cortar docs de API de uma API company                                    |
| database-requirements + database-schema → database-spec.md | Única fusão mantida nos docs de data — DDL e constraints vivem juntos na prática                                                          |
| Lista final: 17 → 21 + N feature-specs                     | Menos cortes radicais, mais cortes cirúrgicos. Profundidade onde o negócio exige                                                          |

### O insight central

O Solo-Templates é um **sistema de geração de documentos**. O que falta é ser um **sistema de gestão de produto**.

A diferença:

- Geração = cria documentos bonitos uma vez
- Gestão = mantém documentos vivos, enforcement discipline durante execução, tracking de progresso, quality gates reais

O BMAD entende isso (sprint-status.yaml, project-context.md, Implementation Readiness gate). O Superpowers entende isso ainda melhor ("no code without design", 2-stage review, TDD enforcement).

O caminho é: **menos docs onde não importa, profundidade onde o negócio exige, e disciplina de execução que hoje não existe.**
