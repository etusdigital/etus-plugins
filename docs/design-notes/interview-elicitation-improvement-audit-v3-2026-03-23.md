# Auditoria v3: ETUS PMDocs — Discovery, Brainstorm e Handoff Sem Ambiguidade

**Data:** 2026-03-23  
**Versão do framework analisada:** v5.3  
**Base:** Leitura direta de comandos, skills, templates, validações, hooks e estado + consolidação das versões anteriores da auditoria  
**Objetivo:** Definir como o ETUS deve evoluir para extrair ideias com profundidade, fechar lacunas semânticas no discovery/brainstorm e entregar um handoff verdadeiramente implementável para engenharia

---

## Tese Central

O ETUS PMDocs já tem a arquitetura conceitual correta:

- ideação antes de especificação
- cobertura upstream via actors, JTBDs, journeys, use cases, edge cases e assumptions
- cadeia de rastreabilidade
- SST
- gates por fase
- workflows por modo

Isso coloca o framework acima da maioria das abordagens de documentação de produto.

Mas o principal problema continua sendo este:

> **O ETUS ainda é forte em metodologia declarada e fraco em enforcement operacional.**

Ou seja:

- as perguntas certas ainda dependem demais do agente "se comportar bem"
- a cobertura ainda mede muito mais quantidade do que completude semântica
- a validação ainda é mais política do que mecanismo
- o desenvolvedor ainda recebe informação distribuída demais

O objetivo da v3 é deixar claro que a evolução do ETUS não exige "mais documentos", e sim:

1. um núcleo de entrevista realmente guiado por estado
2. um discovery mais orientado a comportamento real
3. um brainstorm mais disciplinado e menos genérico
4. cobertura semântica em vez de contagem
5. validação executável
6. um pacote final de handoff que não viole SST

---

## Onde Estão As Fases Mais Importantes

Se a pergunta for "onde o ETUS mais precisa ficar excelente em entrevista?", a resposta é:

### Camada 1 — Core Interview Layer

- `ideate`
- `discover`
- `project-context`
- `product-vision`

Esta é a camada mais importante para extração de ideia.

É aqui que o framework precisa:

- entender o problema real
- diferenciar sintoma de causa
- puxar histórias concretas
- extrair restrições e anti-requisitos
- identificar atores, operações e conflitos
- traduzir tudo em oportunidades bem enquadradas

### Camada 2 — Structured Brainstorm Layer

- `brainstorm` dentro de `ideate`
- `solution-discovery`

Esta é a segunda fase mais crítica, mas com uma função diferente:

- não extrair o problema bruto
- e sim transformar evidência em direções testáveis

Se o discovery falha, o brainstorm vira chute.
Se o brainstorm falha, a solução vira fixação prematura.

### Camada 3 — Translation Layer

- `feature-brief`
- `prd`
- `user-stories`
- `feature-spec`

Esta camada não é a principal para entrevista, mas é onde a qualidade do discovery e brainstorm precisa sobreviver sem degradação.

### Camada 4 — Assurance Layer

- `validate-gate`
- `check-traceability`
- `check-sst`
- novos validadores

Esta camada não descobre a ideia, mas precisa impedir que ambiguidades escapem.

### Camada 5 — Change Layer

- `correct-course`
- state/handoffs
- feedback pós-implementação

Esta camada protege o framework da deriva depois que o escopo muda.

---

## O Que Já Funciona Bem e Deve Ser Preservado

### 1. A sequência macro da ideação está certa

A ordem:

- ingest
- problem
- actors
- jobs
- journeys
- cases
- edges
- assumptions
- brainstorm
- synth

é boa e não deve ser descartada.

### 2. O framework já tem sementes de anti-requisito

Existem sinais importantes em:

- `Out-of-Scope`
- `constraints and guardrails`
- perguntas como "o que não fazer"

O problema não é ausência total. O problema é falta de first-class enforcement.

### 3. A infraestrutura de rastreabilidade já é uma vantagem real

O ETUS já pensa melhor que a maioria dos frameworks em:

- upstream/downstream linkage
- ownership por documento
- IDs
- handoff entre fases

Isso deve ser usado como base da próxima evolução, não substituído.

### 4. A validação conceitual já existe

Há boa intenção em:

- 3-layer validation
- adversarial review
- pressure test
- assumption audit

O que falta é torná-la mais executável.

---

## Diagnóstico Refinado

## D1 — O framework ainda é prompt-rich e enforcement-poor

Essa continua sendo a melhor formulação do problema.

O ETUS já contém várias regras boas:

- uma pergunta por mensagem
- aprovação por seção
- rastrear unknowns
- mostrar progresso
- pressure test

Mas essas regras ainda vivem majoritariamente em:

- texto de skill
- instrução para agente
- template

e não em:

- estado persistente
- bloqueios de progressão
- validadores
- artefatos operacionais

### Consequência prática

Uma entrevista aparentemente "boa" ainda pode:

- pular um tipo de pergunta essencial
- aceitar resposta vaga
- marcar cobertura sem suficiência
- avançar por cansaço ou pressa

---

## D2 — A cobertura atual ainda é contábil, não semântica

Hoje o framework sabe bem contar:

- quantos actors
- quantos journeys
- quantos use cases
- quantos edge cases

Mas a pergunta certa para implementação é:

> cobrimos as dimensões certas para este tipo de problema?

Exemplos de dimensões que ainda podem sumir:

- permissões
- side effects
- notificações
- comportamento degradado
- regras de dado
- observabilidade
- política e compliance
- anti-requisitos
- concorrência, retry, idempotência

### Conclusão

`coverage-matrix` precisa evoluir, mas sem virar um monólito de responsabilidades.

Por isso, a v3 propõe separar:

- **coverage** de problema e dimensões
- **interview execution state** da conversa

---

## D3 — Discovery e brainstorm precisam de dinâmicas diferentes

Uma melhoria importante em relação às versões anteriores é deixar isto muito claro:

### Discovery deve otimizar para:

- verdade
- contexto
- comportamento real
- fricção concreta
- impacto
- restrições

### Brainstorm deve otimizar para:

- amplitude de opção
- estrutura
- clusterização
- escolha disciplinada
- explicitação de premissas
- planejamento de teste

Hoje o ETUS já sugere essa separação, mas ainda não a executa com nitidez suficiente.

---

## D4 — Handoff para dev é um problema de empacotamento e não pode violar SST

Sim, ETUS precisa de um artefato consolidado para dev.

Mas a v3 acrescenta uma regra crítica:

> O handoff packet não pode virar um novo source of truth.

Ele precisa ser:

- **derivado**
- **gerado**
- **regenerável**
- **não-editável como autoridade**

Senão o framework troca um problema por outro:

- antes: informação fragmentada
- depois: duplicação e drift entre o packet e os documentos fonte

### Regra de SST para o handoff packet

Cada seção do packet deve apontar sua autoridade:

- rules → feature-spec
- acceptance criteria → user-stories
- contracts → api-spec
- data semantics → data-dictionary
- NFRs → tech-spec

O packet resume e consolida, mas não redefine.

---

## D5 — Mudança de escopo é o ponto mais subdesenvolvido do framework

Essa continua sendo uma assimetria séria.

O framework é relativamente sofisticado para:

- extrair
- estruturar
- gerar
- validar

Mas ainda é fraco para:

- propagar mudanças
- preservar rejeições
- lembrar objeções do usuário
- atualizar docs conectados

Essa é uma área claramente de P1/P0 tardio.

---

## Recomendações v3 (reordenadas)

## R1 — Criar dois artefatos distintos: `coverage-matrix` e `elicitation-state`

### Problema

As versões anteriores empurravam muita responsabilidade para `coverage-matrix.yaml`.

Isso pode criar um artefato confuso, misturando:

- status da entrevista
- suficiência das respostas
- cobertura semântica
- blockers
- rastreabilidade

### Proposta v3

Separar:

### A. `coverage-matrix.yaml`

Responsável por:

- IDs upstream
- dimensões semânticas
- blockers de cobertura
- readiness gate

### B. `elicitation-state.yaml`

Responsável por:

- módulo atual
- pergunta atual
- perguntas já feitas
- qualidade da resposta
- checkpoint de reflexão
- fadiga do usuário
- decisão de continuar ou pausar

### Benefício

Isso mantém o estado operacional da entrevista limpo e a matriz de cobertura semanticamente focada.

**Prioridade:** P0  
**Esforço:** Médio

---

## R2 — Criar um Elicitation Engine compartilhado

Não duplicar lógica de entrevista em todos os agentes.

Criar um mecanismo comum que:

- leia `elicitation-state.yaml`
- saiba onde a entrevista parou
- saiba quando a resposta foi insuficiente
- aplique escalonamento para vagueza
- injete checkpoints de reflexão
- detecte "não sei", fadiga e necessidade de aprofundamento

### Regras mínimas

1. Antes de perguntar, ler o estado
2. Se o módulo já está coberto, resumir em vez de repetir
3. Se a resposta foi vaga, disparar probe obrigatório
4. A cada 3-4 respostas relevantes, executar reflexão
5. Se o usuário demonstrar fadiga, oferecer:
   - continuar
   - aceitar assumptions explícitas
   - pausar com checkpoint persistido

**Prioridade:** P0  
**Esforço:** Médio

---

## R3 — Discovery deve adotar entrevista story-based como default

Baseado na pesquisa externa, essa é uma das mudanças mais importantes.

### Regra

Sempre que possível, discovery deve puxar:

- episódio real
- último caso concreto
- passo a passo do que aconteceu
- por que aquilo importou
- o que a pessoa fez depois

### Exemplos de probes obrigatórios

- "Me conta da última vez que isso aconteceu"
- "Me conduz passo a passo pelo que você fez"
- "O que aconteceu depois?"
- "Por que isso foi importante?"
- "O que você fez para contornar?"

### Benefício

Reduz:

- abstração
- racionalização
- feature request prematuro

**Prioridade:** P0  
**Esforço:** Baixo

---

## R4 — Brainstorm deve virar uma dinâmica estruturada em 5 estágios

### Problema

Hoje brainstorm ainda corre o risco de ser genérico demais.

### Proposta v3

Padronizar brainstorm em:

1. **Target Opportunity**
2. **HMW prompts**
3. **Divergence**
4. **Clustering + selection**
5. **Assumptions + next tests**

### Técnicas iniciais recomendadas

Na v3, para reduzir escopo, eu começaria com 3 técnicas:

- HMW + clustering
- Crazy 8s
- Gut Check

E deixaria como expansão futura:

- mash-ups
- role play
- reverse brainstorming
- six thinking hats

### Benefício

Evita que brainstorm vire uma conversa criativa pouco disciplinada.

**Prioridade:** P0  
**Esforço:** Médio

---

## R5 — Archetype-aware probe packs, mas começando pequeno

As versões anteriores propuseram 6 archetypes.

Na v3, eu recomendo começar com 3 para reduzir risco de manutenção:

### Archetype 1 — Workflow / Approval

Perguntas obrigatórias:

- quais estados existem?
- quais transições são válidas?
- quais transições são proibidas?
- qual SLA/timeout importa?
- existe delegação ou escalação?
- quem é notificado em cada transição?

### Archetype 2 — API / Integration

Perguntas obrigatórias:

- como autentica?
- precisa retry?
- precisa idempotência?
- qual rate limit?
- o que acontece em falha parcial?
- qual contrato de erro?
- existe backward compatibility?

### Archetype 3 — Import / Export

Perguntas obrigatórias:

- formatos aceitos?
- tamanho máximo?
- preview?
- linhas inválidas?
- rollback?
- retomada?
- encoding?
- feedback de progresso?

Depois que esses 3 estiverem estáveis, expandir para:

- billing
- AI/copilot
- CRUD/admin

**Prioridade:** P0  
**Esforço:** Médio

---

## R6 — Cobertura semântica obrigatória por dimensão

Substituir o gate de "quantidade" por um gate que avalia se cobrimos:

- problem clarity
- trigger and preconditions
- core behavior
- success signal
- anti-requirements
- failure modes
- degraded behavior
- actors and permissions
- data mutations
- side effects
- observability

E, quando houver archetype:

- dimensões específicas do archetype

### Regra

Nenhuma dimensão obrigatória pode ficar `false` sem:

- justificativa `not_applicable`
- ou registro explícito como assumption/open question

**Prioridade:** P0  
**Esforço:** Médio

---

## R7 — Anti-requisitos como objetos rastreáveis (`NG-#`)

Essa recomendação se mantém, com uma clarificação:

### O que `NG-#` resolve

Não resolve apenas scope creep.
Resolve também:

- contradições downstream
- redescoberta de decisões rejeitadas
- implementação de "comportamentos óbvios" que nunca foram autorizados

### Campos mínimos

- statement
- reason
- adjacent behavior
- scope: permanent / deferred / conditional
- downstream docs that must respect it

### Integração

- ideation
- feature brief
- PRD
- traceability checks
- `/elicit`

**Prioridade:** P0  
**Esforço:** Baixo-Médio

---

## R8 — Comando `/elicit` como stress-test semântico

Essa continua sendo uma das melhores recomendações.

Mas a v3 propõe posicioná-lo claramente:

### Quando usar

1. Depois de `ideate`, antes de `feature` ou `discover`
2. Depois de `requirements`, antes de `design`
3. Quando o usuário disser: "quero desafiar o que já foi especificado"

### O que ele faz

Não gera novos artefatos de produto.

Ele faz:

- ambiguity review
- contradiction surfacing
- boundary testing
- hidden assumption detection
- developer simulation

### Output

Um relatório de findings e perguntas remanescentes, não um novo source of truth.

**Prioridade:** P0  
**Esforço:** Médio

---

## R9 — Developer Handoff Packet gerado, com regra explícita de derivação

Essa recomendação continua essencial.

### Regra de design

O packet deve ser:

- gerado automaticamente
- derivado das fontes autoritativas
- regenerável
- não autoritativo

### Seções mínimas

- contexto e objetivo
- non-goals
- actors and permissions
- business rules
- acceptance criteria
- error handling matrix
- state machine
- API contracts relevantes
- data mutations e validation rules
- NFRs aplicáveis
- observabilidade
- open blockers
- impl tasks

### Nota importante

O handoff packet deve existir por:

- feature
- ou sprint scope

não necessariamente por projeto inteiro.

**Prioridade:** P0  
**Esforço:** Médio

---

## R10 — Validação executável anti-placeholder e anti-vagueza

Mantida, mas com uma melhoria importante:

### Cuidado com falso positivo

Regex simples não basta.

O validador deve diferenciar:

- placeholder real
- exemplo em template
- texto citado
- docs de referência

### Checks prioritários

- Gherkin placeholder
- NFR sem número + unidade
- vocabulário vago sem métrica
- seção obrigatória vazia
- ausência de cenário de erro mínimo

**Prioridade:** P0  
**Esforço:** Baixo-Médio

---

## R11 — Gate decisions persistence com rationale

Manter não só status:

- pending
- go
- iterate

mas também:

- feedback do usuário
- rationale
- rejected approaches
- iteration count
- unresolved objection

Isso deve alimentar:

- workflow state
- memory
- próximos prompts

**Prioridade:** P1  
**Esforço:** Baixo-Médio

---

## R12 — Diferenciação de "não sei"

Essa recomendação permanece excelente e deve ser formalizada.

### Tipos

- pesquisar
- deferir
- nunca pensei nisso

### Regra

Quando o usuário disser "não sei", ETUS deve classificar antes de seguir.

Isso melhora:

- assumptions
- scope management
- question quality

**Prioridade:** P1  
**Esforço:** Baixo

---

## R13 — Gestão de fadiga do usuário

Essa recomendação é importante e rara.

### Regra proposta

Depois de um certo número de perguntas substantivas, ETUS deve oferecer:

- continuar aprofundando
- pausar e retomar depois
- aceitar assumptions explícitas

### Importante

Essas assumptions precisam ficar claramente marcadas como:

- `assumed_default`
- revisit required

**Prioridade:** P1  
**Esforço:** Baixo

---

## R14 — Feedback loop pós-implementação

Esta recomendação continua ótima, mas eu a colocaria explicitamente como P2 inicial ou P1 tardio.

### Objetivo

Descobrir:

- quais perguntas faltaram
- quais suposições o dev teve que inventar
- em que fase aquilo deveria ter sido capturado

### Valor

Isso é o que transforma archetype packs em ativos que melhoram com o tempo.

**Prioridade:** P1 tardio / P2  
**Esforço:** Médio

---

## Roadmap v3

## Fase 1 — Core Interview Layer

Objetivo: tornar discovery e brainstorm significativamente melhores.

### Entregas

- `elicitation-state.yaml`
- elicitation engine compartilhado
- story-based discovery prompts
- reflection checkpoints
- vague-response escalation
- "não sei" classifier
- fatigue management
- 3 archetype probe packs iniciais

### Benefício esperado

Entrevistas mais precisas, menos perda de contexto, menos respostas vagas aceitas.

---

## Fase 2 — Semantic Coverage Layer

Objetivo: parar de medir cobertura só por contagem.

### Entregas

- semantic dimensions no coverage layer
- archetype-specific dimensions
- NG-# first-class objects
- gate checks baseados em dimensões

### Benefício esperado

O gate começa a barrar ausência de substância, não só ausência de itens.

---

## Fase 3 — Assurance And Handoff Layer

Objetivo: reduzir ambiguidade para engenharia.

### Entregas

- `/elicit`
- anti-placeholder validation
- anti-vagueza validation
- contradiction validator
- developer handoff packet

### Benefício esperado

Menos perguntas abertas para dev, menos inconsistência entre documentos, menos improviso.

---

## Fase 4 — Continuity And Change Layer

Objetivo: impedir drift e aproveitar aprendizado real.

### Entregas

- gate decision persistence
- rationale fields
- correct-course fortalecido
- backpropagation de mudanças de feature
- post-implementation feedback loop

### Benefício esperado

Menos esquecimento de rejeições, menos inconsistência após mudanças, mais evolução contínua do framework.

---

## Métricas de sucesso v3

### Métricas principais

1. **Perguntas que o dev ainda precisou fazer após receber o packet**
   Meta: `< 3` por feature

2. **Cobertura semântica antes do gate**
   Meta: `> 80%` na primeira passagem

3. **Archetype probes respondidos com resposta suficiente**
   Meta: `> 70%`

4. **Vagas escaladas corretamente**
   Meta: `> 90%` das respostas vagas geram probe de follow-up

5. **Iterações por gate**
   Meta: média `< 1.5`

6. **Mudanças rejeitadas reaparecendo downstream**
   Meta: `0`

### Métrica de ouro

> Quantas decisões de produto/comportamento o dev precisou inventar porque a documentação não respondeu?

Essa é provavelmente a melhor métrica de verdade do sistema.

---

## Estimativa mais realista de esforço

As versões anteriores estavam um pouco otimistas.

### Estimativa v3

| Fase | Escopo | Tempo esperado |
|---|---|---|
| Fase 1 | Entrevista e estado | 4-6 dias |
| Fase 2 | Cobertura semântica | 3-5 dias |
| Fase 3 | Validação + handoff | 4-6 dias |
| Fase 4 | Continuidade e change management | 5-8 dias |
| **Total funcional** | Primeira versão boa | **16-25 dias** |

### Nota

Uma primeira versão parcial pode sair antes.

Mas uma versão realmente calibrada, sem muita regra frágil, deve ser tratada como trabalho de 2-4 semanas, não de poucos dias.

---

## Conclusão Final

O ETUS não precisa virar um framework mais "pesado".

Ele precisa virar um framework mais:

- explícito no estado da entrevista
- semântico na cobertura
- disciplinado no brainstorm
- mecânico na validação
- seguro no handoff para dev
- resiliente a mudanças

Se a v1 mostrou o problema e a v2 mostrou a direção, a v3 consolida o caminho:

> **o futuro do ETUS é sair de uma boa metodologia documentada para um sistema operacional de elicitação, decisão e handoff.**
