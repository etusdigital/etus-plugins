# Auditoria v3: ETUS PMDocs — Elicitation, Coverage, e Developer Handoff

**Data:** 2026-03-23
**Versão do framework:** v5.3
**Base:** Leitura completa do código-fonte (9 agentes, 45 skills, 13 comandos, 5 gates, 6 hooks, state_defaults.py, coverage-matrix.yaml, todos os templates) + duas auditorias externas + pesquisa de best practices (GOV.UK, NNGroup, IDEO, Product Talk, Google Design Sprint)
**Objetivo:** Tornar o ETUS excepcionalmente eficaz em extrair ideias de produto da cabeça do PO sem deixar lacunas, e produzir documentação que permita ao desenvolvedor implementar sem adivinhar.

---

## Diagnóstico Central

O ETUS tem a base certa. Ideação antes de spec, coverage matrix com IDs rastreáveis, SST, traceability chain, 4 modos, gates entre fases. É melhor que a maioria dos frameworks de documentação de produto.

O problema está em três camadas:

**Camada 1 — Método de extração errado.** O framework faz perguntas abstratas ("Qual é o problema?", "Quem são os usuários?") quando deveria extrair histórias concretas do passado ("Me conta da última vez que isso aconteceu", "O que aconteceu depois?"). Perguntas abstratas produzem respostas genéricas. Narrativas do passado produzem contexto, detalhes, e revelam o que o PO nem sabia que era relevante.

**Camada 2 — Coverage medida por contagem, não por substância.** O gate de ideação pede ">= 2 edge cases". Mas 2 edge cases genéricos sobre "campo vazio" não valem 1 edge case sobre "o que acontece quando o serviço de pagamento cai durante uma transação". A validação não distingue edge cases genéricos de edge cases relevantes para o tipo de feature.

**Camada 3 — O desenvolvedor recebe 10+ documentos e monta o puzzle sozinho.** Não existe artefato consolidado que diga: "aqui está tudo que você precisa para implementar esta feature, em um lugar".

---

## O Que Já Funciona (Preservar)

**1. Sequência de ideation correta.** `ingest → problem → actors → jobs → journeys → cases → edges → assumptions → brainstorm → synth` é a ordem certa. Cobertura antes de criatividade.

**2. Anti-requisitos existem.** O feature-brief (Q4: "O que está fora de escopo?") e o opportunity-pack (seção "Constraints & Guardrails") já capturam o que NÃO fazer. Falta rastreabilidade, não intenção.

**3. Traceability chain funciona.** `BO-# → PRD-F-# → US-# → FS-# → impl-#` com validação automática. É vantagem competitiva real.

**4. Pressure test no feature-brief.** 4 perguntas de desafio: "Is this the right problem?", "What happens if we do nothing?", "Is there a better framing?", "Are we building for the right user?". Bom instinto, precisa de mais enforcement.

**5. Coverage matrix com IDs rastreáveis.** `ACT-#`, `JTBD-#`, `JOUR-#`, `UC-#`, `EDGE-#`, `ASM-#` com status tracking e downstream linkage. A infraestrutura existe.

**6. Contradiction register.** "If sources disagree, record the contradiction instead of silently resolving it." Intenção certa. Falta mecânica.

**7. Solution discovery com 4 riscos.** Value, Usability, Viability, Feasibility — framework correto para avaliar soluções antes de commitar com requirements.

**8. Validate-gate 3-layer.** Structure → Content → Dependencies. Arquitetura certa. Precisa de critérios mais fortes na Layer 2.

---

## Recomendações

### R1. Story-based interviewing como método primário de discovery

**O que existe hoje:**

A ideate skill pergunta (módulo Problem Framing): "What is the proposed solution?", "What is the underlying problem?", "What happens if we do nothing?". O discovery-agent faz 5W2H: "What is the problem/opportunity?", "Who are the users/stakeholders?". O feature-brief pergunta: "What feature are you documenting?"

Todas são perguntas abstratas que pedem opinião e hipótese.

**O que a pesquisa mostra:**

Product Talk, NNGroup e GOV.UK convergem: as melhores entrevistas de discovery são **story-based e past-focused**. Em vez de perguntar "Qual é o problema?", perguntar "Me conta da última vez que isso aconteceu. O que aconteceu? Quem estava envolvido? O que deu errado? O que você fez depois?"

Respostas sobre o passado são mais concretas, mais detalhadas, e revelam contexto que perguntas abstratas não capturam. Quando alguém conta uma história real, aparecem: os workarounds, os atores escondidos, os pontos de dor que o PO nem sabia que importavam.

**Analogia:** Perguntar "Qual é o problema?" é como um médico perguntar "O que você tem?". Perguntar "Me conta o que aconteceu" é como perguntar "Quando começou? O que você sentiu? O que fez?" — a segunda abordagem produz diagnóstico melhor.

**O que fazer concretamente:**

Reescrever os prompts de extração em 4 skills para usar story-first:

| Skill | Prompt atual | Prompt story-based |
|---|---|---|
| ideate (Problem Framing) | "What is the underlying problem?" | "Me conta da última vez que esse problema aconteceu. O que aconteceu? Quem estava envolvido? O que deu errado?" |
| ideate (Actor Map) | "Who feels the pain directly?" | "Na história que você me contou, quem mais estava envolvido? Quem aprovava? Quem era afetado mesmo sem participar?" |
| jtbd-extractor | "What job is this person trying to get done?" | "Antes de pensar na solução: o que essa pessoa estava tentando fazer naquele momento? O que a faria dizer 'valeu a pena'?" |
| feature-brief (Q1) | "What feature are you documenting?" | "Me conta uma situação concreta onde o usuário precisaria dessa feature. O que ele tentou fazer? Onde travou?" |

Adicionar 5 story probes reusáveis como knowledge file compartilhado:

```markdown
# .claude/skills/discovery/knowledge/story-probes.md

## Core Story Probes (use um por vez, na ordem)

1. "Me conta da última vez que isso aconteceu."
   - Suficiente quando: resposta inclui quem, o quê, quando, e resultado
   - Insuficiente quando: resposta é genérica ou hipotética

2. "Me conduz passo a passo pelo que aconteceu."
   - Suficiente quando: passos são concretos e sequenciais
   - Insuficiente quando: pula etapas ou generaliza

3. "O que aconteceu depois?"
   - Usar quando: a história parou no meio

4. "Pode me dar outro exemplo?"
   - Usar quando: precisa de padrão (1 história = anedota, 2+ = padrão)

5. "Por que isso foi importante para você?"
   - Usar no final da história, não no início
```

**Arquivos a alterar:**
- `.claude/skills/discovery/ideate/SKILL.md` — reescrever módulos 2, 3, 4 para story-first
- `.claude/skills/discovery/jtbd-extractor/SKILL.md` — reescrever EXTRACTION PROMPTS
- `.claude/skills/planning/feature-brief/SKILL.md` — reescrever Q1-Q3
- `.claude/agents/discovery-agent.md` — reescrever seção "Problem Interview"
- Criar `.claude/skills/discovery/knowledge/story-probes.md` (novo)

**Esforço:** ~150 linhas (reescrita) + ~30 linhas (novo arquivo) = ~180 linhas

---

### R2. Interview Snapshot — Micro-artefato de síntese imediata

**O que existe hoje:**

A ideação captura informação diretamente no opportunity-pack.md. Toda a conversa é destilada em um único documento no final. Detalhes, citações e contexto se perdem entre a conversa e a síntese.

**O que a pesquisa mostra:**

IDEO recomenda "download your learnings" imediatamente após cada entrevista. Product Talk recomenda "interview snapshots" que capturam: contexto-chave, citação memorável, mapa de experiência, oportunidades, e insights — logo depois de cada história, não no final do processo.

**O que fazer:**

Criar um micro-artefato **Interview Snapshot** — um bloco estruturado gerado DURANTE a ideação, depois de cada história significativa extraída. Não é um documento separado; é uma entrada no opportunity-pack.

Adicionar ao template do opportunity-pack uma nova seção entre "Evidence Register" e "Actor Map":

```markdown
## Story Snapshots

### SNAP-1: [título descritivo da história]
- **Quem contou:** [PO / stakeholder / usuário observado]
- **Contexto:** [quando aconteceu, que circunstância]
- **O que aconteceu:** [narrativa em 3-5 frases]
- **Citação-chave:** "[frase mais reveladora, verbatim]"
- **O que deu errado:** [ponto de dor concreto]
- **Workaround atual:** [o que a pessoa faz hoje]
- **Oportunidade detectada:** [O-# se aplicável]
- **IDs alimentados:** ACT-#, JTBD-#, JOUR-#, UC-#, EDGE-# extraídos desta história
```

**Regra de operação:** Após cada história extraída (R1), o agente gera o snapshot e pergunta: "Esse resumo captura o que você me contou? Algo que eu interpretei errado?"

Esse é o checkpoint de reflexão — não arbitrário a cada N perguntas, mas ancorado em cada unidade de informação (história).

**Arquivos a alterar:**
- `.claude/skills/discovery/ideate/knowledge/template.md` — adicionar seção Story Snapshots
- `.claude/skills/discovery/ideate/SKILL.md` — adicionar instrução de gerar snapshot após cada história
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml` — adicionar `snapshots: []` com IDs SNAP-#

**Esforço:** ~60 linhas

---

### R3. Archetype-aware probe packs como checklist pós-história

**O que existe hoje:**

O `edge-case-sweep/SKILL.md` tem 8 categorias genéricas: invalid input, dependency unavailable, race condition, permission mismatch, partial success, abuse, rollback, observability. São bons defaults, mas não cobrem os gaps específicos de cada tipo de feature.

**Sequência correta (insight da pesquisa):**

Stories (R1) → Snapshot (R2) → **Archetype checklist** (R3) para verificar o que as histórias não revelaram.

Os probes de archetype NÃO são o método primário de extração. São uma rede de segurança que roda DEPOIS das histórias, para encontrar o que o PO não contou porque não pensou nisso.

**Archetypes propostos (6 iniciais):**

```markdown
# .claude/skills/discovery/elicitation-archetypes/workflow-approval.md

## Archetype: Workflow / Approval

### Probes obrigatórios (perguntar um por vez)
1. "Quais são os estados possíveis? Me lista todos."
   - Suficiente: lista com 3+ estados e nomes claros
   - Insuficiente: "pendente e aprovado" (falta rejeitado, expirado, cancelado)

2. "Quando alguém rejeita, o que acontece? Volta para quem? O requerente é notificado?"
   - Suficiente: fluxo de rejeição claro com próximo passo
   - Insuficiente: "a pessoa corrige e manda de novo" (sem detalhe)

3. "Se ninguém aprovar em X dias, o que deveria acontecer?"
   - Suficiente: timeout com ação automática ou escalação
   - Insuficiente: "não sei" → registrar como ASM-# open

4. "Alguém pode delegar a aprovação? O delegado tem os mesmos poderes?"

5. "Existe audit trail? Quem precisa ver o histórico de aprovações?"

6. "É possível reabrir algo já aprovado? Em que condições?"

### Anti-patterns deste archetype
- Estados implícitos (ex: "em revisão" que ninguém definiu)
- Transições impossíveis não documentadas
- SLA sem consequência
```

**6 archetypes iniciais:**

| Archetype | Arquivo | Probes |
|---|---|---|
| CRUD / Backoffice | `crud-backoffice.md` | Roles, bulk ops, soft delete, search/filter, audit, export |
| Workflow / Approval | `workflow-approval.md` | States, transitions, timeout, delegation, reopen, audit |
| Import / Export | `import-export.md` | Formatos, tamanho, malformed rows, preview, rollback, resumo |
| API / Integration | `api-integration.md` | Auth, retry, rate limit, idempotency, partial failure, versioning |
| AI / Copilot | `ai-copilot.md` | Input boundaries, hallucination, human override, recusa, eval, latência |
| Billing / Subscription | `billing-subscription.md` | Ciclo, upgrade/downgrade, prorata, dunning, refund, compliance |

**Integração:** Após os módulos "Actor Map" e "Journey Sweep" na ideation, o agente pergunta: "Com base no que discutimos, esse trabalho se parece mais com [lista de archetypes]. Qual deles melhor descreve o que estamos construindo?" → Carrega 1-3 probe packs → Roda probes como checklist sobre o que as histórias não cobriram.

**Arquivos a criar:**
- `.claude/skills/discovery/elicitation-archetypes/` (diretório)
- 6 arquivos `.md`, um por archetype (~80 linhas cada)
- Referência em `.claude/skills/discovery/ideate/SKILL.md`

**Esforço:** ~480 linhas (6 × 80) + ~30 linhas (integração na ideate) = ~510 linhas

---

### R4. Separar divergência e convergência no brainstorm

**O que existe hoje:**

O módulo "Solution Direction Brainstorm" na ideate skill diz: "BMAD technique selection → candidate solution directions → risk discovery → stress test of the preferred direction". É um fluxo que mistura geração de ideias com avaliação imediata.

O discovery-agent oferece 4 técnicas (Mind Mapping, HMW, Scenario Planning, JTBD) e pede que o usuário escolha uma.

**O que a pesquisa mostra:**

IDEO e Design Sprint são claros: divergência e convergência são modos diferentes que não devem se misturar. Quando você critica ideias enquanto gera, mata a geração. A sequência correta é:

1. **Themes** — Agrupar insights das histórias
2. **HMW** — Reformular cada insight como "How Might We...?"
3. **Diverge** — Gerar muitas opções sem julgar (quantidade > qualidade)
4. **Cluster** — Agrupar ideias similares
5. **Select** — Escolher 2-3 direções
6. **Stress test** — Testar cada direção contra riscos
7. **Assumptions** — Listar o que precisa ser verdade para cada direção funcionar

**O que está errado no ETUS:** O passo de HMW está no lugar errado. Hoje, HMW é mencionado no PRD como técnica de priorização (correto para lá) e no discovery-agent como opção de brainstorm. Mas não é usado como **ponte entre discovery e brainstorm** — que é seu uso mais forte segundo a pesquisa.

**O que fazer:**

Reescrever o módulo "brainstorm" na ideate skill com fases explícitas:

```markdown
### 10. Solution Direction Brainstorm

#### Pré-requisito
Brainstorm é BLOQUEADO até:
- Problem defined
- >= 1 actor
- >= 1 JTBD
- >= 1 journey
- >= 3 story snapshots

#### Fase A: Themes (convergência sobre evidência)
- Agrupar story snapshots por tema
- Apresentar agrupamento ao usuário: "Vejo 3 temas: [X], [Y], [Z]. Faz sentido?"

#### Fase B: HMW Bridge
- Para cada tema, gerar 2-3 HMW statements
- Ex: "Como poderíamos [reduzir o tempo de aprovação] sem [comprometer o audit trail]?"
- Usuário seleciona os HMWs mais relevantes

#### Fase C: Diverge (sem julgamento)
- Para cada HMW selecionado, gerar 3-5 opções
- Regra: NÃO criticar, NÃO avaliar, NÃO dizer "mas"
- Construir sobre ideias ("e se também...", "e se em vez disso...")

#### Fase D: Cluster & Select
- Agrupar ideias similares
- Usuário seleciona 2-3 direções para aprofundar

#### Fase E: Stress Test (convergência)
- Para cada direção: tradeoffs, riscos, o que pode dar errado
- Avaliar contra os 4 riscos: value, usability, viability, feasibility

#### Fase F: Assumptions
- Para cada direção: "O que precisa ser verdade para isso funcionar?"
- Registrar como ASM-# com risk level e validation path
- Conectar a solution-discovery downstream
```

**Arquivos a alterar:**
- `.claude/skills/discovery/ideate/SKILL.md` — reescrever módulo 10
- `.claude/agents/discovery-agent.md` — reescrever seção "Creative Exploration"
- `.claude/skills/discovery/ideate/knowledge/template.md` — expandir "Solution Directions" para incluir themes, HMWs, ideias brutas, cluster, assumptions

**Esforço:** ~120 linhas (reescrita) + ~40 linhas (template) = ~160 linhas

---

### R5. Semantic coverage dimensions no lugar de contagem

**O que existe hoje:**

Thresholds: `actors >= 2, jtbd >= 2, journeys >= 2, use_cases >= 4, edge_cases >= 3, assumptions >= 3` para Product mode. O readiness gate checa booleans: `problem_defined: false`, `actors_identified: false`, etc.

**O problema:**

3 edge cases sobre "campo vazio" valem menos que 1 edge case sobre "o que acontece quando o pagamento falha no meio da transação". A contagem passa, a substância não.

**O que fazer:**

Manter contagem como floor mínimo, mas adicionar **dimensões semânticas obrigatórias** ao coverage-matrix:

```yaml
semantic_dimensions:
  # Obrigatórias (gate falha se false sem justificativa)
  problem_independent_of_solution: false
  actor_roles_and_permissions: false
  trigger_and_preconditions: false
  core_behavior_described: false
  success_signal_defined: false
  explicit_non_goals: false
  failure_modes_covered: false
  data_mutations_identified: false

  # Recomendadas (warning se false, não falha)
  degraded_behavior: false
  side_effects_and_notifications: false
  observability_needs: false
  permissions_and_policy: false

  # Ativadas por archetype
  archetype_dimensions: {}
```

**Regra de gate:** Ideation Readiness Gate falha se qualquer dimensão obrigatória é `false` sem uma justificativa `not_applicable` com razão.

**Cada archetype (R3) adiciona dimensões extras.** Exemplo para workflow: `state_machine_defined: false`, `invalid_transitions_documented: false`, `sla_timeout_defined: false`.

**Arquivos a alterar:**
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml` — adicionar `semantic_dimensions`
- `.claude/skills/discovery/ideate/SKILL.md` — adicionar check de dimensões no readiness gate
- `.claude/skills/validation/validate-gate/SKILL.md` — adicionar check de dimensões na Layer 2
- `.claude/hooks/state_defaults.py` — adicionar dimensões ao default se necessário

**Esforço:** ~100 linhas

---

### R6. Non-goals como objetos rastreáveis (NG-#)

**O que existe hoje:**

O feature-brief (Q4) pergunta "What is this feature explicitly NOT doing?". O opportunity-pack tem seção "Constraints & Guardrails" com "what must NOT get worse". Mas nenhum é rastreável downstream — se um user story ou impl-plan reintroduz algo declarado fora de escopo, ninguém detecta.

`check-traceability/SKILL.md` rastreia `BO-# → PRD-F-# → US-# → FS-# → impl-#` mas NÃO rastreia non-goals. `ID_PATTERNS` em `state_defaults.py` não inclui `NG-#`.

**O que fazer:**

1. Adicionar `NG-#` ao `ID_PATTERNS`:
```python
"non_goals": r"\bNG-\d+\b",
```

2. Para cada `NG-#`:
- statement: o que NÃO deve acontecer
- reason: por que foi excluído
- scope: `permanent | deferred_to_v2 | conditional`
- downstream_must_respect: lista de docs que não podem contradizer

3. Adicionar check no `check-traceability`: se doc downstream menciona comportamento que contradiz `NG-#`, flag como violação.

4. Adicionar seção no template do opportunity-pack (entre "Constraints & Guardrails" e "Assumptions"):

```markdown
## Non-Goals Registry

### NG-1: [O que NÃO fazer]
- Reason: [por que está excluído]
- Scope: permanent | deferred_to_v2 | conditional
- Adjacent behavior: [funcionalidade válida que é vizinha deste non-goal]
```

**Arquivos a alterar:**
- `state_defaults.py` — adicionar NG-# ao ID_PATTERNS
- `feature_lifecycle.py` — extrair NG-# de docs
- `check-traceability/SKILL.md` — adicionar check de violação de NG-#
- Template do opportunity-pack — adicionar seção
- Template do feature-brief — adicionar seção

**Esforço:** ~120 linhas

---

### R7. Elicitation engine com estado persistente

**O que existe hoje:**

O `coverage-matrix.yaml` tem `step_status` por módulo: `not_started | in_progress | covered`. Mas nenhuma skill lê esse estado antes de agir. Se a sessão reinicia, o agente não sabe em qual pergunta parou dentro de um módulo.

**O que fazer:**

Separar explicitamente **estado de cobertura** de **estado operacional da entrevista**.

O `coverage-matrix.yaml` deve continuar dono de:

- IDs rastreáveis
- dimensões semânticas
- blockers
- readiness gate

Criar um novo arquivo `elicitation-state.yaml` para guardar o andamento da conversa:

```yaml
modules:
  actors:
    status: in_progress
    stories_collected: 2
    archetype_probes_done: false
    dimension_coverage:
      actor_roles_and_permissions: true
      trigger_and_preconditions: false
    current_probe: "Quem bloqueia ou aprova este workflow?"
    last_activity: "2026-03-23T14:30:00Z"
    fatigue_score: low
    reflection_checkpoint_due: false
```

Regra de entrada obrigatória para cada sub-skill:

```
ANTES de perguntar qualquer coisa:
1. Leia elicitation-state.yaml
2. Encontre o módulo correspondente
3. Se status == "covered" → resuma o que existe, pergunte se quer aprofundar
4. Se status == "in_progress" → continue de current_probe
5. Se status == "not_started" → comece com story probe
```

**Arquivos a alterar:**
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml` — manter coverage e semantic dimensions
- criar `docs/ets/projects/{project-slug}/state/elicitation-state.yaml` (ou template equivalente)
- `.claude/skills/discovery/ideate/SKILL.md` — adicionar regra de entrada
- `.claude/hooks/state_defaults.py` — adicionar estado default do `elicitation-state`
- Cada sub-skill (jtbd-extractor, journey-sweep, edge-case-sweep, use-case-matrix, assumption-audit) — adicionar leitura de estado

**Esforço:** ~230 linhas

---

### R8. Validação anti-placeholder e anti-vagueza

**O que existe hoje:**

`validate-gate/SKILL.md` Layer 1 checa "No unresolved [TODO] or [TBD] placeholders". Layer 2 checa "User stories follow Given/When/Then with specific values (not placeholders)" e "Technical specs have quantified NFRs (numbers, not 'fast' or 'scalable')".

Layer 2 está certa na intenção, mas é LLM-dependent — não há critérios de rejeição mecânicos.

**O que adicionar:**

Anti-patterns concretos para Layer 1 (fast-fail, não depende de LLM):

```markdown
### Anti-Placeholder Patterns (Layer 1 extension)
Reject automatically if found in required sections:
- Text inside brackets: [ALGO], [USER], [ACTION], [RESULT], [VALOR]
- NFR-# without a number: "fast", "quick", "scalable", "secure", "reliable" without metric
- Given/When/Then with < 5 words per clause
- Empty table cells in required tables
- "TBD", "TODO", "to be defined", "a definir" in any form
```

Anti-vagueza para Layer 2:

```markdown
### Vagueness Checks (Layer 2)
- Every NFR-# must contain at least one number (ms, %, req/s, etc.)
- Every US-# happy-path must have at least 1 US-# or EDGE-# error-path sibling
- Every permission claim ("only admin can...") must trace to a formal role definition
```

**Arquivos a alterar:**
- `.claude/skills/validation/validate-gate/SKILL.md` — expandir Layer 1 e Layer 2

**Esforço:** ~50 linhas

---

### R9. Comando `/elicit` — Stress-test de ambiguidade

**O que existe hoje:**

Peças espalhadas: pressure test no feature-brief (4 perguntas), adversarial review language no validate-gate, edge-case-sweep na ideation. Nenhuma é focada em "encontrar o que ficou implícito nos documentos existentes".

**O que fazer:**

Criar `/elicit` como stress-test que roda sobre documentação existente e gera findings:

```markdown
# Elicitation Findings: [Feature/Project Name]

## Ambiguities (EL-A-#)
- EL-A-1: US-3 diz "notificar o usuário" mas não especifica canal

## Contradictions (EL-C-#)
- EL-C-1: PRD diz "CSV only", api-spec aceita XLSX

## Missing Boundaries (EL-B-#)
- EL-B-1: Nenhum doc define o que acontece quando rate limit é atingido

## Hidden Assumptions (EL-H-#)
- EL-H-1: Todos os docs assumem single-tenant sem explicitar

## Developer Questions (EL-D-#)
- EL-D-1: "Se eu implementar US-3, qual canal de notificação uso?"
```

**Técnicas do `/elicit`:**

1. **Developer simulation** — "Se eu fosse implementar [feature], o que eu precisaria perguntar?"
2. **Cross-doc consistency** — DB constraints vs data-dictionary vs API schema
3. **Vague quantifier scan** — "rápido", "seguro", "muitos" sem métrica
4. **NG-# violation scan** — Docs downstream contradizem non-goals?
5. **Missing error siblings** — Para cada happy-path UC-#, existe error-path correspondente?
6. **Permission matrix gap** — Claims de permissão sem role definition formal?
7. **State machine completeness** — Para entidades com estados, todas as transições documentadas?

**Arquivos a criar:**
- `.claude/commands/elicit.md` (~50 linhas)
- `.claude/skills/validation/elicit/SKILL.md` (~150 linhas)

**Esforço:** ~200 linhas

---

### R10. Implementation Packet — Documento consolidado para o dev

**O que existe hoje:**

O implementation-plan gera tasks `impl-#` com dependências. O dev precisa navegar opportunity-pack, feature-brief, user-stories, design-delta, tech-spec, api-spec, data-dictionary para montar o quadro completo.

**O que fazer:**

Criar skill que gera um documento único por feature, **consolidado automaticamente** dos upstream docs:

```markdown
# Implementation Packet: [Feature Name]

## 1. Context & Non-Goals
De: feature-brief + NG-# registry

## 2. Actors & Permissions
| Actor | Pode | NÃO pode |
De: opportunity-pack actor map + permission claims

## 3. Business Rules
De: feature-brief FB-# + feature-spec

## 4. Acceptance Criteria (Given/When/Then)
De: user-stories.md (filtrado por feature)

## 5. Error Handling Matrix
| Cenário | Trigger | Resposta Sistema | Resposta Usuário | Retry? |
De: EDGE-# + user-stories error scenarios

## 6. State Machine (se archetype = workflow)
Mermaid + transições válidas + transições proibidas
De: feature-spec

## 7. API Contracts
Endpoints com request/response + error responses
De: api-spec (filtrado por feature)

## 8. Data Mutations & Validation
Tabelas/campos criados/alterados + regras de validação
De: database-spec + data-dictionary

## 9. Performance Requirements
NFR-# aplicáveis
De: tech-spec

## 10. Observability
Logs, métricas, alertas
(NOVO — não existe hoje)

## 11. Tasks (impl-#)
Sequência com dependências
De: implementation-plan

## 12. Open Questions
O que resolver ANTES de implementar
De: ASM-# open + feature-brief outstanding questions
```

**Regras críticas:**

1. Este documento é **GERADO, não escrito manualmente**. Puxa de cada upstream. Se um upstream muda, pode ser regenerado.
2. Este documento **NÃO é source of truth**. Ele consolida e aponta para as fontes autoritativas.
3. Cada seção do packet deve declarar sua autoridade:
   - Business Rules → `feature-spec` / `feature-brief`
   - Acceptance Criteria → `user-stories`
   - API Contracts → `api-spec`
   - Data Mutations & Validation → `database-spec` + `data-dictionary`
   - Performance Requirements → `tech-spec`
4. O packet pode resumir, agrupar e filtrar. Ele **não pode redefinir** comportamento, schema, NFR ou critério de aceite.

**Arquivos a criar:**
- `.claude/skills/implementation/implementation-packet/SKILL.md` (~180 linhas)
- `.claude/skills/implementation/implementation-packet/knowledge/template.md` (~80 linhas)

**Esforço:** ~260 linhas

---

### R11. Diferenciação de "não sei"

**O que existe hoje:**

O assumption-audit tem: "status: resolved | assumed | open". Mas não diferencia entre os três tipos de "não sei":

| Tipo | Significado | Tratamento |
|---|---|---|
| "Não sei e preciso pesquisar" | Gap consciente | ASM-# open com owner + deadline |
| "Não sei e tá ok não saber" | Defer consciente | ASM-# deferred com justificativa |
| "Nunca pensei nisso" | Gap inconsciente | Aprofundar ANTES de seguir — este é o caso mais valioso |

**O que fazer:**

Adicionar instrução nos agentes de discovery e planning:

```markdown
## Handling "Não Sei"

Quando o usuário responde "não sei", "boa pergunta", "nunca pensei nisso":

Pergunte: "Me ajuda a classificar isso:
A) Você sabe quem saberia? → registro como ASM-# open com owner
B) É seguro deixar para depois? → registro como ASM-# deferred
C) Isso pode mudar o que estamos construindo? → preciso explorar mais"

Se a resposta é C, NÃO siga em frente. Faça mais 2-3 perguntas sobre o tema
antes de mover para o próximo módulo.
```

**Arquivos a alterar:**
- `.claude/agents/discovery-agent.md` — seção "Handling Uncertainty"
- `.claude/agents/planning-agent.md` — mesma seção
- `.claude/skills/discovery/assumption-audit/SKILL.md` — expandir status options

**Esforço:** ~40 linhas

---

### R12. Escalonamento de respostas vagas

**O que existe hoje:**

O jtbd-extractor diz "Do not accept 'save time' without specifying where and how". Boa intenção, sem mecânica.

**Contexto da pesquisa:** Com story-based interviewing (R1), respostas vagas acontecem com menos frequência porque narrativas concretas produzem detalhes naturalmente. Mas quando acontecem, o agente precisa saber como reagir.

**O que fazer:**

Criar tabela de escalonamento como knowledge file compartilhado:

```markdown
# .claude/skills/discovery/knowledge/vague-response-escalation.md

| Padrão vago | Reação |
|---|---|
| "deve ser rápido" | "Na história que você me contou, quanto tempo levava? Quanto deveria levar para o usuário não reclamar?" |
| "precisa ser seguro" | "Seguro contra quê? Na última vez que deu problema, o que aconteceu?" |
| "muitos/poucos/vários" | "Me dá um número. Ordem de grandeza: dezenas, centenas, milhares?" |
| "depois a gente vê" | "Isso bloqueia implementação? Se sim, preciso de decisão. Se não, registro como ASM-# deferred." |
| "tipo o [concorrente]" | "O que exatamente? Me mostra ou me descreve a parte que você quer." |
| "óbvio/padrão" | "Me explica o 'óbvio' como se eu nunca tivesse visto o sistema." |
```

**Arquivos a criar:**
- `.claude/skills/discovery/knowledge/vague-response-escalation.md` (novo)
- Referenciado por: ideate, jtbd-extractor, feature-brief, assumption-audit

**Esforço:** ~50 linhas

---

### R13. Gate decisions persistence

**O que existe hoje:**

`default_workflow_state()` em `state_defaults.py` tem `gates: { discovery_gate: "pending" }`. Só status. Não tem feedback, motivo, ou abordagens rejeitadas.

Se o usuário diz "ITERATE porque a visão precisa enfatizar redução de custo", a próxima fase não sabe disso.

**O que fazer:**

Expandir gate state em workflow-state.yaml:

```yaml
gates:
  discovery_gate:
    status: iterate
    feedback: "Visão precisa enfatizar redução de custo, não velocidade"
    timestamp: "2026-03-23T14:30:00Z"
    rejected_approaches:
      - "Foco em velocidade como proposta de valor"
    iteration_count: 1
```

**Arquivos a alterar:**
- `state_defaults.py` — expandir gates
- `validate-gate/SKILL.md` — salvar feedback em ITERATE/NO-GO
- `memory-sync.py` — propagar gate decisions

**Esforço:** ~80 linhas

---

### R14. Adaptação à fadiga do usuário

**O que existe hoje:**

Nada. Uma entrevista completa no Product mode pode ter 40+ perguntas.

**O que fazer:**

1. Ordenar perguntas por criticidade: bloqueantes de implementação primeiro, enriquecimento depois.
2. Após 15 perguntas (ou 30 minutos de conversa), oferecer: "Já temos cobertura de [X]% nas dimensões obrigatórias. Quer continuar aprofundando ou aceitar defaults para o resto?"
3. Para dimensões com default aceito: registrar como `ASM-# assumed_default`.

**Onde adicionar:**
- `.claude/skills/discovery/ideate/SKILL.md` — seção "Fatigue Management"

**Esforço:** ~25 linhas

---

### R15. Feedback loop pós-implementação

**O que existe hoje:**

Nada. Gaps encontrados pelo dev durante implementação não retroalimentam o framework.

**O que fazer:**

Criar `/retro` que:
1. Pergunta ao dev: "Que decisões você tomou sozinho durante a implementação?"
2. Classifica cada gap: em qual fase deveria ter sido perguntado?
3. Salva como learning em `docs/ets/projects/{slug}/learnings/`
4. Se padrão se repete 2+ vezes em projetos diferentes, sugere adicionar ao archetype probe correspondente

**Esforço:** ~100 linhas (comando + skill)

---

## Roadmap de Implementação

### Fase 1 — Método de entrevista (3-4 dias)

| # | Melhoria | Impacto | Esforço |
|---|---|---|---|
| R1 | Story-based interviewing | Extração 3x mais rica | ~180 linhas |
| R2 | Interview Snapshots | Síntese sem perda de contexto | ~60 linhas |
| R4 | Brainstorm divergência/convergência + HMW bridge | Ideação mais disciplinada | ~160 linhas |
| R11 | Diferenciação de "não sei" | Unknowns melhor classificados | ~40 linhas |
| R12 | Escalonamento de respostas vagas | Respostas mais específicas | ~50 linhas |
| R14 | Adaptação à fadiga | Qualidade consistente | ~25 linhas |
| **Total Fase 1** | | | **~515 linhas** |

### Fase 2 — Coverage enforcement (3-4 dias)

| # | Melhoria | Impacto | Esforço |
|---|---|---|---|
| R3 | Archetype probe packs (6) | Perguntas certas para o tipo de problema | ~510 linhas |
| R5 | Semantic coverage dimensions | Gates que checam substância | ~100 linhas |
| R6 | Non-goals rastreáveis (NG-#) | Scope creep detectável | ~120 linhas |
| R7 | Elicitation engine com estado | Entrevistas sem perda de progresso | ~200 linhas |
| R8 | Validação anti-placeholder | Placeholders não passam | ~50 linhas |
| **Total Fase 2** | | | **~980 linhas** |

### Fase 3 — Handoff para desenvolvedor (2-3 dias)

| # | Melhoria | Impacto | Esforço |
|---|---|---|---|
| R9 | Comando `/elicit` (stress-test) | Ambiguidades detectadas antes do código | ~200 linhas |
| R10 | Implementation Packet | Dev recebe tudo em 1 documento | ~260 linhas |
| R13 | Gate decisions persistence | Fases não repropose o que foi rejeitado | ~80 linhas |
| **Total Fase 3** | | | **~540 linhas** |

### Fase 4 — Melhoria contínua (1-2 dias)

| # | Melhoria | Impacto | Esforço |
|---|---|---|---|
| R15 | Feedback loop pós-implementação | Framework aprende com a experiência | ~100 linhas |
| **Total Fase 4** | | | **~100 linhas** |

---

## Esforço Total

| Fase | Linhas | Dias (MVP funcional) |
|---|---|---|
| Fase 1 — Método de entrevista | ~515 | 3-4 |
| Fase 2 — Coverage enforcement | ~980 | 3-4 |
| Fase 3 — Handoff para dev | ~540 | 2-3 |
| Fase 4 — Melhoria contínua | ~100 | 1-2 |
| **Total** | **~2.135** | **9-13** |

**Leitura correta dessa estimativa:**

- `9-13 dias` = primeira versão funcional, com MVP operacional das principais ideias
- `16-25 dias` = versão calibrada e estável, já ajustada depois da integração entre skills, hooks, estado e validação

O risco aqui não está só em "escrever linhas", mas em:

- coordenar mudanças entre múltiplos skills
- calibrar os critérios de gate
- evitar falso positivo em validações
- ajustar a convivência entre SST, handoff packet e novos estados de elicitação

---

## Como Saber se Funcionou

| Métrica | Como medir | Meta |
|---|---|---|
| Perguntas inventadas pelo dev | Perguntar ao dev no final de cada feature | < 3 por feature |
| Dimensões semânticas cobertas no 1º pass | % de dimensões obrigatórias = true antes do gate | > 80% |
| Archetype probes respondidos | % de probes com resposta concreta | > 70% |
| Gate iterations | Média de ITERATEs antes de GO | < 1.5 |
| Stories extraídas vs. perguntas abstratas | Ratio de SNAP-# vs. respostas genéricas | > 60% story-based |
| Tempo de implementação vs. estimativa | Desvio real/estimado | < 30% |

---

## Diferenças da v2 para a v3

| Aspecto | v2 | v3 |
|---|---|---|
| Método primário de extração | Perguntas abstratas com follow-up | Story-based interviewing |
| Checkpoint de reflexão | A cada 3-4 perguntas (arbitrário) | A cada história extraída (ancorado em unidade de informação) |
| Archetype probes | Método primário de extração | Checklist pós-história (rede de segurança) |
| Brainstorm | Não abordado | Separação divergência/convergência + HMW bridge |
| Interview Snapshot | Não existia | Micro-artefato intermediário |
| Escalonamento de respostas vagas | Tabela reativa standalone | Ancorado em story probes ("Na história que você contou...") |
| Ordem do roadmap | Archetype probes na Fase 1 | Story-based na Fase 1, archetypes na Fase 2 |

A mudança fundamental da v3: **extrair primeiro, verificar depois**. Histórias concretas produzem 80% da cobertura naturalmente. Archetypes, dimensões semânticas e `/elicit` capturam os 20% restantes que as histórias não revelaram.
