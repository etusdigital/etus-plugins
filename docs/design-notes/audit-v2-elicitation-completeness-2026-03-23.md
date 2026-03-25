# Auditoria v2: ETUS PMDocs — Da Entrevista ao Handoff para Desenvolvedor

**Data:** 2026-03-23
**Versão do framework:** v5.3
**Base:** Leitura completa de 9 agentes, 45 skills, 13 comandos, 5 gates, 6 hooks, state_defaults.py, coverage-matrix.yaml
**Método:** Cruzamento de duas auditorias independentes + leitura direta do código-fonte

---

## Diagnóstico Central

O ETUS PMDocs tem a base certa: ideação antes de especificação, coverage matrix, traceability chain, SST validation, 4 modos, gates entre fases. Isso é melhor que 90% dos frameworks de documentação de produto.

O problema não é falta de metodologia. O problema é que **a qualidade do output depende de prompt discipline, não de enforcement mecânico**.

Na prática, isso significa três coisas:

1. **A entrevista pode terminar "completa" sem cobrir as perguntas certas para o tipo de problema.** O framework pede ">= 2 edge cases" — mas não distingue entre edge cases genéricos e edge cases críticos para o domínio. Um feature de upload com 2 edge cases sobre "nome duplicado" e "campo vazio" passa na validação, mas não cobre "arquivo corrompido", "upload parcial", "limite de tamanho", "vírus".

2. **A validação verifica estrutura, não semântica.** Um user story com `Given [USUARIO], When [AÇÃO], Then [RESULTADO]` passa no check de traceability porque tem formato Given/When/Then. Mas é placeholder.

3. **O desenvolvedor recebe 10+ documentos e precisa montar o puzzle sozinho.** Não existe artefato consolidado que diga: "aqui está tudo que você precisa para implementar esta feature, em um lugar só."

---

## O que já funciona bem (preservar)

Antes das recomendações, é importante fixar o que NÃO deve mudar:

**1. Coverage-first ideation** — A ideate skill já força: problem framing antes de soluções, actors antes de specs, journeys antes de arquitetura. A sequência `ingest → problem → actors → jobs → journeys → cases → edges → assumptions → brainstorm → synth` é correta.

**2. Anti-requisitos existem** — O feature-brief (Q4: "O que está fora de escopo?") e o opportunity-pack (seção "constraints and guardrails") já capturam anti-requisitos. Não são first-class objects rastreáveis, mas existem.

**3. Traceability chain** — `BO-# → PRD-F-# → US-# → FS-# → impl-#` com validação automática via check-traceability. Isso é uma vantagem competitiva real.

**4. Pressure test no feature-brief** — A skill já tem seção "PRESSURE TEST" com 4 perguntas de desafio. Não é enforcement, mas já é instrução de qualidade.

**5. Coverage matrix com IDs rastreáveis** — `ACT-#`, `JTBD-#`, `JOUR-#`, `UC-#`, `EDGE-#`, `ASM-#` com status tracking e downstream linkage. A infraestrutura de rastreamento existe.

**6. Contradiction register na ideation** — "If sources disagree, record the contradiction instead of silently resolving it." Já existe a intenção; falta enforcement.

---

## Recomendações (ordenadas por impacto × esforço)

### R1. Elicitation Engine com estado persistente

**Problema concreto:** A ideate skill tem 11 módulos, mas a progressão entre eles depende do agente "lembrar" onde parou. Se o contexto é perdido (sessão longa, troca de sessão), o agente pode pular módulos ou repetir perguntas.

**Evidência no código:** `coverage-matrix.yaml` tem `step_status` por módulo (not_started/in_progress/covered), mas nenhuma skill verifica esse estado antes de agir. A skill diz "checkpoint after each semantic block" mas a mecânica de checkpoint é: salvar o YAML e esperar que o próximo agente leia.

**O que falta concretamente:**

Cada módulo no coverage-matrix precisa de campos adicionais:

```yaml
step_status:
  actors:
    status: in_progress
    questions_asked: 3
    questions_remaining: 2
    current_question: "Quem bloqueia ou aprova este workflow?"
    answers_quality: sufficient  # insufficient | sufficient | rich
    last_answer_timestamp: "2026-03-23T14:30:00Z"
```

E cada skill precisa de uma regra de entrada:

```
ANTES de perguntar qualquer coisa:
1. Leia coverage-matrix.yaml
2. Encontre o módulo correspondente
3. Se status == "covered" → pule, resuma o que já existe
4. Se status == "in_progress" → continue de current_question
5. Se status == "not_started" → comece do início
```

**Arquivos a alterar:**
- `.claude/skills/discovery/ideate/knowledge/coverage-matrix.yaml` — adicionar campos de estado por step
- `.claude/skills/discovery/ideate/SKILL.md` — adicionar regra de entrada obrigatória
- Cada sub-skill (jtbd-extractor, journey-sweep, edge-case-sweep, use-case-matrix, assumption-audit) — adicionar leitura de estado

**Esforço:** ~80 linhas de YAML + ~30 linhas por sub-skill = ~230 linhas total

---

### R2. Archetype-aware probe packs

**Problema concreto:** A ideate skill pergunta "invalid states?", "dependency failure?", "race condition?" para todo tipo de feature. Essas são categorias genéricas. Um feature de workflow precisa de perguntas sobre estados/transições/SLA/escalação. Um feature de import/export precisa de perguntas sobre formatos/tamanho/rollback/resumabilidade.

**Evidência no código:** `edge-case-sweep/SKILL.md` tem 8 categorias fixas: invalid input, dependency unavailable, race condition, permission mismatch, partial success, abuse, rollback, observability. São boas categorias genéricas, mas não cobrem os gaps específicos de cada tipo de feature.

**O que fazer:**

Criar um passo zero na ideation: classificar o work item em 1-3 archetypes, depois carregar probe packs específicos.

Archetypes propostos (começar com 6, expandir depois):

| Archetype | Probes obrigatórios |
|---|---|
| **CRUD/backoffice** | Roles, permissions, audit trail, bulk operations, soft delete, search/filter, pagination, export |
| **Workflow/approval** | States, transitions, transições inválidas, timeout/SLA, delegação, escalação, reopen, audit trail, notificações por transição |
| **Import/export** | Formatos aceitos, tamanho máximo, linhas malformadas, preview, validação, rollback, resumabilidade, encoding, progresso |
| **API/integration** | Auth, retry, rate limit, idempotency, partial failure, webhook replay, versioning, backward compat, error contract |
| **AI/copilot** | Boundaries de input, risco de hallucination, human override, regras de recusa, critérios de avaliação, fallback, latência aceitável |
| **Billing/subscription** | Ciclo de vida, upgrade/downgrade, prorata, grace period, dunning, refund, invoice, compliance fiscal |

**Formato de cada probe pack:** Um arquivo markdown em `.claude/skills/discovery/elicitation-archetypes/{archetype}.md` com:
- 5-8 perguntas obrigatórias (uma por mensagem)
- Para cada pergunta: o que é "resposta suficiente" vs "precisa aprofundar"
- Anti-patterns específicos do archetype

**Integração:**
1. Após o módulo "Problem Framing" na ideation, perguntar: "Qual desses padrões mais se parece com o que estamos construindo? [lista de archetypes]"
2. Carregar 1-3 probe packs
3. Integrar as perguntas nos módulos existentes (edge-case-sweep herda os probes do archetype)

**Esforço:** ~100 linhas por archetype × 6 = ~600 linhas + ~40 linhas na ideate skill

---

### R3. Semantic coverage dimensions no lugar de contagem

**Problema concreto:** O threshold atual é `>= 3 edge cases` para Product mode. Mas 3 edge cases sobre "campo vazio" valem menos que 1 edge case sobre "o que acontece quando o serviço de pagamento está fora do ar".

**Evidência no código:** `coverage-matrix.yaml` tem `count: 0` e `threshold: 0` por domínio. O gate de ideação checa: `edge_cases_covered: false/true`. Isso é binário e baseado em contagem.

**O que fazer:**

Substituir thresholds de contagem por **dimensões semânticas obrigatórias**. Para cada work item, rastrear se as seguintes dimensões foram cobertas (sim/não/não-aplicável):

```yaml
semantic_dimensions:
  problem_clarity: false          # O problema está descrito independente da solução?
  actor_roles_and_permissions: false  # Quem pode fazer o quê?
  trigger_and_preconditions: false    # O que inicia o fluxo e o que precisa ser verdade antes?
  core_behavior: false            # O que o sistema faz no happy path?
  success_signal: false           # Como o usuário sabe que funcionou?
  explicit_non_goals: false       # O que NÃO deve acontecer?
  failure_modes: false            # O que acontece quando dá errado?
  degraded_behavior: false        # Como o sistema funciona com capacidade reduzida?
  data_mutations: false           # Que dados são criados/alterados/deletados?
  side_effects: false             # Notificações, eventos, webhooks, logs?
  permissions_and_policy: false   # Regras de acesso, compliance, rate limits?
  observability: false            # Logs, métricas, alertas necessários?

  # Dimensões opcionais (ativadas por archetype)
  archetype_dimensions: {}
```

**Regra de gate:** A ideation readiness gate falha se qualquer dimensão obrigatória está `false` sem justificativa `not_applicable`.

**Integração com archetypes:** Cada archetype adiciona dimensões extras em `archetype_dimensions`. Exemplo para workflow: `state_machine: false`, `invalid_transitions: false`, `sla_timeout: false`.

**Arquivos a alterar:**
- `coverage-matrix.yaml` — adicionar `semantic_dimensions`
- `ideate/SKILL.md` — trocar thresholds de contagem por dimensões
- `validate-gate/SKILL.md` — adicionar check de dimensões
- `state_defaults.py` — adicionar dimensões ao default

**Esforço:** ~60 linhas YAML + ~40 linhas em cada skill afetada = ~200 linhas total

---

### R4. Non-goals como objetos rastreáveis (NG-#)

**Problema concreto:** O feature-brief pergunta "O que está fora de escopo?" (Q4), o opportunity-pack tem "constraints and guardrails", mas nenhum desses é rastreável downstream. Se um user story ou impl-plan reintroduz silenciosamente algo que foi declarado fora de escopo, ninguém detecta.

**Evidência no código:** `check-traceability/SKILL.md` rastreia `BO-# → PRD-F-# → US-# → FS-# → impl-#` mas NÃO rastreia non-goals. O `ID_PATTERNS` em `state_defaults.py` não inclui `NG-#`.

**O que fazer:**

1. Adicionar `NG-#` ao `ID_PATTERNS`:
```python
"non_goals": r"\bNG-\d+\b",
```

2. Cada `NG-#` deve ter:
- statement: o que NÃO deve acontecer
- reason: por que foi excluído
- adjacent_behavior: qual funcionalidade válida é vizinha deste non-goal
- scope: `permanent | deferred_to_v2 | conditional`
- downstream_must_respect: lista de docs que não podem contradizer

3. Adicionar check no `check-traceability`:
- Se um doc downstream menciona comportamento que contradiz um `NG-#`, flag como violação

4. Adicionar seção "Non-Goals" no opportunity-pack template e no feature-brief template

**Arquivos a alterar:**
- `state_defaults.py` — adicionar NG-# ao ID_PATTERNS
- `feature_lifecycle.py` — extrair NG-# de docs
- `check-traceability/SKILL.md` — adicionar check de non-goal violation
- `ideate/knowledge/template.md` — adicionar seção NG-#
- `planning/feature-brief/knowledge/template.md` — adicionar seção NG-#

**Esforço:** ~120 linhas total

---

### R5. Comando `/elicit` — Stress-test antes de travar a spec

**Problema concreto:** Não existe uma fase dedicada a "interrogar a spec até eliminar ambiguidade". As peças mais próximas estão espalhadas: pressure test no feature-brief, adversarial review na validate-gate, edge-case-sweep na ideation. Mas nenhuma é focada em "encontrar o que ficou implícito".

**O que fazer:**

Criar `/elicit` como um comando standalone que pode ser executado:
- Depois do `/ideate`, antes do `/feature`
- Depois do `/plan requirements`, antes do `/design`
- A qualquer momento quando o usuário quiser desafiar o que foi documentado

O `/elicit` NÃO cria novos artefatos. Ele interroga os existentes e gera uma lista de findings:

```markdown
# Elicitation Findings

## Ambiguities Found
- EL-1: US-3 diz "notificar o usuário" mas não especifica canal (email? push? in-app?)
- EL-2: feature-brief diz "admin pode editar" mas não define se edição inclui delete

## Contradictions Found
- EL-3: PRD diz "CSV only" (PRD-F-2), api-spec aceita XLSX (endpoint POST /import)
- EL-4: user-story US-5 diz "confirmação síncrona", feature-spec diz "eventual consistency"

## Missing Boundaries
- EL-5: Nenhum documento define o que acontece quando o rate limit é atingido
- EL-6: Permissões de "editor" vs "viewer" nunca formalizadas em matrix

## Hidden Assumptions
- EL-7: Todos os docs assumem single-tenant mas nenhum explicita isso
- EL-8: API spec assume timezone UTC mas frontend pode estar em BRT

## Questions for Developer
- EL-9: "Se eu receber US-3 para implementar, o que eu ainda precisaria perguntar?"
```

**Técnicas de interrogação do `/elicit`:**

1. **Goal vs Non-Goal clash** — Para cada NG-#, verificar se algum doc downstream contradiz
2. **Actor/Permission mismatch** — Para cada actor, verificar se as ações permitidas são consistentes entre docs
3. **Missing lifecycle states** — Para cada entidade com estados, verificar se todas as transições são cobertas
4. **Missing failure handling** — Para cada UC-#, verificar se existe pelo menos 1 EDGE-# correspondente
5. **Developer simulation** — "Se eu fosse implementar [feature], o que eu ainda precisaria saber?"
6. **Vague quantifier check** — Procurar palavras como "rápido", "seguro", "fácil", "muitos", "poucos" sem métricas
7. **Cross-doc consistency** — DB constraints vs data-dictionary vs API schema

**Arquivos a criar:**
- `.claude/commands/elicit.md` — ~60 linhas
- `.claude/skills/validation/elicit/SKILL.md` — ~150 linhas

**Esforço:** ~210 linhas

---

### R6. Implementation Packet — Documento consolidado para o desenvolvedor

**Problema concreto:** O framework gera opportunity-pack, feature-brief, user-stories, design-delta, tech-spec, api-spec, data-dictionary, implementation-plan. O desenvolvedor precisa abrir 8 arquivos e fazer a síntese mental de o que implementar.

**Evidência no código:** O implementation-plan (`SKILL.md`) gera tasks `impl-#` com dependências, mas NÃO consolida business rules, error handling, permissions, data validation em um lugar.

**O que fazer:**

Criar uma skill `implementation-packet` que gera um documento único por feature (ou por sprint):

```markdown
# Implementation Packet: [Feature Name]

## 1. Contexto (2 parágrafos)
Extraído de: feature-brief problem statement + product-vision BO-#

## 2. Non-Goals (NG-#)
Extraído de: feature-brief out-of-scope + NG-# registry

## 3. Actors e Permissions
| Actor | Pode fazer | NÃO pode fazer |
Extraído de: opportunity-pack actor map + tech-spec NFRs

## 4. Business Rules (FB-#, regras de negócio)
Extraído de: feature-brief + feature-spec

## 5. Acceptance Criteria (US-# com Given/When/Then)
Extraído de: user-stories.md

## 6. Error Handling Matrix
| Cenário | Trigger | Resposta do Sistema | Resposta ao Usuário | Retry? |
Extraído de: EDGE-# + user-stories error scenarios + tech-spec NFRs

## 7. State Machine (se aplicável)
Mermaid diagram + transições válidas + transições proibidas
Extraído de: feature-spec

## 8. API Contracts
Endpoints relevantes com request/response schemas + error responses
Extraído de: api-spec.md (filtrado por feature)

## 9. Data Mutations
Quais tabelas/campos são criados/alterados/deletados + validation rules
Extraído de: database-spec + data-dictionary (filtrado por feature)

## 10. Performance Requirements
NFR-# targets aplicáveis a esta feature
Extraído de: tech-spec.md

## 11. Observability
Logs obrigatórios, métricas, alertas, dashboard entries
(NOVO — não existe em nenhum doc hoje)

## 12. Tasks (impl-#)
Sequência de implementação com dependências
Extraído de: implementation-plan.md

## 13. Unresolved Questions
Questões abertas que o dev deve resolver ANTES de implementar
Extraído de: feature-brief outstanding questions + ASM-# open
```

**Regra crítica:** Este documento é GERADO automaticamente, não escrito manualmente. Ele puxa de cada upstream doc e consolida. Se um upstream muda, o packet pode ser regenerado.

**Arquivos a criar:**
- `.claude/skills/implementation/implementation-packet/SKILL.md` — ~200 linhas
- `.claude/skills/implementation/implementation-packet/knowledge/template.md` — ~80 linhas

**Esforço:** ~280 linhas

---

### R7. Validação anti-placeholder e anti-vagueza nos gates

**Problema concreto:** Um user story com `Given [USER], When [ACTION], Then [RESULT]` passa na validação porque tem a estrutura correta. Um NFR com "API should be fast" passa porque tem formato `NFR-#`.

**Evidência no código:** `validate-gate/SKILL.md` Layer 1 (Structure) checa "No unresolved [TODO] or [TBD] placeholders". Mas `[USER]`, `[ACTION]`, `[RESULT]` não são detectados como placeholders. Layer 2 (Content) diz "LLM-based review" mas sem critérios específicos de rejeição.

**O que adicionar:**

1. **Anti-placeholder patterns** — Rejeitar automaticamente:
   - Texto entre colchetes: `[ALGO]`, `[TBD]`, `[TODO]`, `[PLACEHOLDER]`
   - Palavras vagas em NFRs sem número: "fast", "quick", "secure", "easy", "scalable", "reliable"
   - Given/When/Then com menos de 5 palavras por cláusula (indica template não preenchido)

2. **Quantifier check em NFRs** — Todo NFR-# deve ter pelo menos um número (latência em ms, uptime em %, throughput em req/s). Se não tem, flag como `NFR_VAGUE`.

3. **Error path coverage** — Para cada US-# do tipo happy-path, verificar se existe pelo menos 1 US-# ou EDGE-# com cenário de erro correspondente.

**Onde adicionar:**
- `validate-gate/SKILL.md` Layer 1 — adicionar checks anti-placeholder
- `validate-gate/SKILL.md` Layer 2 — adicionar checks de vagueza e error coverage

**Esforço:** ~60 linhas

---

### R8. Checkpoints de reflexão ("O que eu entendi é...")

**Problema concreto:** Os agentes perguntam, o usuário responde, o agente segue. Não há momento de "deixa eu verificar se entendi corretamente". Isso causa dois problemas: o agente pode interpretar errado, e o usuário pode perceber que sua própria resposta foi incompleta.

**Evidência no código:** Nenhum agente ou skill tem instrução de checkpoint de reflexão. O interaction protocol diz "section-by-section approval" para output, mas não para input (respostas do usuário).

**O que adicionar:**

Regra simples em cada agente: **A cada 3-4 respostas do usuário, pausar e resumir:**

```
"Antes de continuar, vou resumir o que entendi até aqui:

1. O problema é [X] porque [Y]
2. O principal afetado é [actor] que hoje faz [workaround]
3. O sucesso seria medido por [metric]
4. Fora de escopo: [NG-1, NG-2]

Isso está correto? Algo que eu interpretei errado ou que falta?"
```

**Onde adicionar:**
- `.claude/agents/discovery-agent.md` — adicionar seção "Reflection Checkpoints"
- `.claude/agents/planning-agent.md` — mesma seção
- `.claude/skills/discovery/ideate/SKILL.md` — adicionar à INTERACTION PROTOCOL
- `.claude/skills/planning/feature-brief/SKILL.md` — adicionar entre Q3 e Q4

**Esforço:** ~40 linhas total (10 por arquivo)

---

### R9. Tabela de escalonamento para respostas vagas

**Problema concreto:** Quando o usuário diz "deve ser rápido", o agente aceita. Deveria escalar com uma pergunta de follow-up específica.

**Evidência no código:** O jtbd-extractor tem "Do not accept 'save time' without specifying where and how" — mas essa é uma instrução, não um mecanismo. Não há tabela de padrões de resposta vaga → follow-up.

**O que adicionar:**

Tabela reusável em um arquivo de conhecimento compartilhado:

```markdown
# .claude/skills/discovery/knowledge/vague-response-escalation.md

| Padrão vago | Follow-up obrigatório |
|---|---|
| "deve ser rápido/performático" | "Rápido significa <200ms? <1s? <5s? Qual é o número que faria o usuário reclamar?" |
| "precisa ser seguro" | "Seguro contra qual ameaça? Qual dado é sensível? Quem NÃO deveria ter acesso?" |
| "fácil de usar" | "Me descreva alguém que teria dificuldade. O que ele tentaria e onde ficaria travado?" |
| "precisa escalar" | "Quantos usuários simultâneos hoje? Quantos em 12 meses? E em 3 anos?" |
| "muitos/poucos/vários" | "Me dá um número. Ordem de grandeza: dezenas, centenas, milhares?" |
| "depois a gente vê/define depois" | "Isso bloqueia implementação? Se sim, preciso de uma decisão agora. Se não, registro como ASM-# open." |
| "tipo o [concorrente]" | "O que exatamente do [concorrente] você quer? O que NÃO quer?" |
| "óbvio/padrão/normal" | "O que é óbvio para você pode não ser para o dev. Me explica o 'óbvio' como se eu nunca tivesse visto." |
```

Referenciado por cada sub-skill de discovery.

**Esforço:** ~40 linhas (arquivo) + ~5 linhas por sub-skill (referência) = ~70 linhas

---

### R10. Gate decisions persistence

**Problema concreto:** Quando o usuário decide "ITERATE" ou "NO-GO" em um gate e explica o motivo, essa informação não é salva. A próxima fase não sabe o que foi rejeitado.

**Evidência no código:** `default_workflow_state()` em `state_defaults.py` tem `gates: { discovery_gate: "pending" }` — status só. Não tem campo para feedback, motivo, ou abordagens rejeitadas.

**O que adicionar:**

Expandir o gate state em `workflow-state.yaml`:

```yaml
gates:
  discovery_gate:
    status: iterate
    feedback: "Visão precisa enfatizar redução de custo, não velocidade"
    timestamp: "2026-03-23T14:30:00Z"
    rejected_approaches:
      - "Foco em velocidade de entrega como proposta de valor"
    iteration_count: 1
```

**Onde alterar:**
- `state_defaults.py` — expandir gates para incluir feedback/rejected
- `validate-gate/SKILL.md` — salvar feedback quando usuário decide ITERATE/NO-GO
- `memory-sync.py` — propagar gate decisions para project-state.md

**Esforço:** ~80 linhas

---

### R11. Feedback loop pós-implementação

**Problema concreto:** Depois que o dev implementa, os gaps que ele encontrou (perguntas que teve que inventar respostas) não retroalimentam o framework. Os archetype probes nunca melhoram com a experiência.

**O que fazer:**

Criar um comando `/retro` que:
1. Pergunta ao dev: "Que perguntas você teve que responder sozinho durante a implementação?"
2. Para cada resposta, classifica: "Isso deveria ter sido perguntado em qual fase? (ideation/planning/design)"
3. Salva como learning em `docs/ets/projects/{project-slug}/learnings/`
4. Se o padrão se repete 2+ vezes, sugere adicionar ao archetype probe pack correspondente

**Esforço:** ~100 linhas (comando + skill)

---

### R12. Diferenciação de "não sei"

**Problema concreto:** Quando o usuário responde "não sei", o framework trata como uma resposta uniforme. Mas existem três tipos de "não sei" com tratamentos diferentes:

| Tipo | Significado | Tratamento correto |
|---|---|---|
| "Não sei e preciso pesquisar" | O usuário tem consciência do gap | Registrar como ASM-# open com owner + deadline |
| "Não sei e está ok não saber agora" | Decisão consciente de defer | Registrar como ASM-# deferred com justificativa |
| "Nunca pensei nisso" | O usuário não sabia que a pergunta existia | Este é o caso mais valioso — aprofundar antes de seguir |

**O que adicionar:**

Instrução nos agentes: quando o usuário diz "não sei", "boa pergunta", "nunca pensei nisso":

```
"Entendi. Me ajuda a classificar isso:
A) Você sabe quem saberia? (vou registrar como pergunta aberta com owner)
B) É seguro deixar para depois? (vou registrar como assumption deferred)
C) Isso pode mudar o escopo do que estamos construindo? (precisamos explorar mais antes de seguir)"
```

**Onde adicionar:**
- `.claude/agents/discovery-agent.md` — seção "Handling Uncertainty"
- `.claude/agents/planning-agent.md` — mesma seção
- `.claude/skills/discovery/assumption-audit/SKILL.md` — expandir AUDIT QUESTIONS

**Esforço:** ~30 linhas

---

### R13. Adaptação à fadiga do usuário

**Problema concreto:** Uma entrevista completa no modo Product pode ter 40+ perguntas. As últimas 10 respostas terão qualidade inferior simplesmente porque o usuário está cansado. Nenhuma análise abordou isso.

**O que fazer:**

1. Ordenar perguntas por criticidade: perguntas que bloqueiam implementação primeiro, perguntas de enriquecimento depois.
2. Após 15 perguntas, oferecer: "Já temos cobertura suficiente para seguir com [X]%. Quer continuar aprofundando ou prefere aceitar defaults para as dimensões restantes?"
3. Para dimensões onde o usuário aceitar defaults, registrar como `ASM-# assumed_default` para revisão posterior.

**Onde adicionar:**
- `.claude/skills/discovery/ideate/SKILL.md` — seção "Fatigue Management"
- Ordem de prioridade nos coverage modules (já estão em ordem boa, mas formalizar)

**Esforço:** ~25 linhas

---

## Roadmap de Implementação

### Fase 1 — Entrevista inteligente (2-3 dias)

| # | O quê | Impacto |
|---|---|---|
| R2 | Archetype-aware probe packs (6 archetypes) | Perguntas certas para o problema certo |
| R8 | Checkpoints de reflexão | Validação de entendimento |
| R9 | Tabela de escalonamento de respostas vagas | Respostas mais específicas |
| R12 | Diferenciação de "não sei" | Unknowns melhor classificados |
| R13 | Adaptação à fadiga | Qualidade consistente |

### Fase 2 — Coverage enforcement (2-3 dias)

| # | O quê | Impacto |
|---|---|---|
| R1 | Elicitation engine com estado persistente | Entrevistas que não perdem progresso |
| R3 | Semantic coverage dimensions | Gates que checam substância, não contagem |
| R4 | Non-goals rastreáveis (NG-#) | Scope creep detectável |
| R7 | Validação anti-placeholder nos gates | Placeholders não passam mais |

### Fase 3 — Handoff para desenvolvedor (2-3 dias)

| # | O quê | Impacto |
|---|---|---|
| R5 | Comando `/elicit` (stress-test) | Ambiguidades encontradas antes da implementação |
| R6 | Implementation Packet | Dev recebe tudo em um documento |
| R10 | Gate decisions persistence | Fases não repropose o que foi rejeitado |

### Fase 4 — Melhoria contínua (1-2 dias)

| # | O quê | Impacto |
|---|---|---|
| R11 | Feedback loop pós-implementação | Framework melhora com o tempo |

---

## Métricas de Sucesso

Como saber se as melhorias funcionaram:

1. **"Perguntas que o dev teve que inventar"** — Pedir ao dev no final de cada feature: quantas decisões ele tomou que não estavam na documentação? Meta: < 3 por feature.

2. **Coverage dimensions atingidas antes do gate** — % de dimensões semânticas cobertas na primeira passagem da ideation. Meta: > 80%.

3. **Archetype probes respondidos** — % das perguntas do archetype que receberam resposta concreta (não vaga, não "não sei"). Meta: > 70%.

4. **Tempo de implementação vs estimativa** — Se a documentação é completa, o desvio entre estimativa e real deve diminuir. Meta: desvio < 30%.

5. **Gate iterations** — Quantas vezes um gate precisa de ITERATE antes de GO. Se as entrevistas melhoram, os gates devem passar mais rápido. Meta: média < 1.5 iterações por gate.

---

## Esforço Total

| Fase | Linhas | Dias |
|---|---|---|
| Fase 1 — Entrevista | ~765 | 2-3 |
| Fase 2 — Coverage | ~550 | 2-3 |
| Fase 3 — Handoff | ~490 | 2-3 |
| Fase 4 — Melhoria contínua | ~100 | 1-2 |
| **Total** | **~1.905** | **7-11** |

---

## Resultado Esperado

| Dimensão | Antes | Depois |
|---|---|---|
| Qualidade da entrevista | 7.5/10 | 9.5/10 |
| Completude para desenvolvedor | 4.5/10 | 9.0/10 |
| Detecção de gaps | 5.5/10 | 9.0/10 |
| Continuidade entre fases | 7.0/10 | 9.0/10 |
| Melhoria contínua | 0/10 | 7.0/10 |

A mudança fundamental: passar de **"coverage sugerida por prompts"** para **"coverage enforced por estado, archetypes, dimensões semânticas, e empacotamento para o dev"**.
