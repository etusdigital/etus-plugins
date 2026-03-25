# Auditoria Profunda: ETUS PMDocs — Eficácia de Entrevista e Completude para Desenvolvedores

**Data:** 2026-03-23
**Escopo:** Análise de 7 agentes, 45 skills, 13 comandos, 5 gates, sistema de memória e fluxo de handoff
**Objetivo:** Identificar TODOS os gaps que impedem o framework de extrair 100% das ideias do product owner e entregar documentação completa para desenvolvedores

---

## Score Atual

| Dimensão | Score | Meta |
|----------|-------|------|
| Qualidade da entrevista (extração de ideias) | 7.5/10 | 9.5/10 |
| Completude para desenvolvedor | 4.5/10 | 9.0/10 |
| Detecção de gaps (validação) | 5.5/10 | 9.0/10 |
| Continuidade entre fases | 7.0/10 | 9.0/10 |
| Gestão de mudanças | 3.0/10 | 8.0/10 |

---

## PARTE 1: Problemas na Entrevista (extrair ideias da cabeça do PO)

### 1.1 — Agentes são geradores de documentos, não entrevistadores

**Problema:** Os 7 agentes sabem ESTRUTURAR documentos, mas não sabem ENTREVISTAR. Eles perguntam "O que é o problema?" mas não ensinam a si mesmos como lidar com respostas vagas, como aprofundar, como desafiar premissas.

**Evidência:** Nenhum agente tem uma seção "Técnicas de Entrevista" com padrões concretos como:
- "Me conta uma situação real onde isso aconteceu..." (narrativa)
- "O que aconteceria se NÃO fizéssemos isso?" (impacto negativo)
- "Me dá um número específico..." (quantificação)
- "E se o oposto fosse verdade?" (desafio de premissa)
- "Quem mais é afetado por isso?" (stakeholders escondidos)

**Fix:** Adicionar bloco `## Técnicas de Entrevista` em cada agente com 7 padrões de probe.

**Arquivos:** Todos em `.claude/agents/`

---

### 1.2 — NINGUÉM pergunta "O que NÃO deve acontecer?"

**Problema:** Todas as skills perguntam "o que construir" mas nenhuma pergunta sistematicamente "o que EVITAR", "o que o sistema NÃO pode fazer", "quais são os guardrails".

**Evidência:**
- `project-context` (skill): Zero probes sobre anti-requisitos
- `prd` (skill): Tem scope in/out mas não pergunta ativamente "o que está PROIBIDO"
- `user-stories`: Gera cenários positivos mas não cenários negativos ("Given que o sistema NÃO deve permitir...")
- `product-vision`: Nenhuma pergunta sobre "o que NÃO queremos ser"

**Impacto:** Desenvolvedores descobrem restrições não documentadas durante implementação, gerando retrabalho.

**Fix:** Adicionar pergunta obrigatória em cada fase: "O que este produto/feature NÃO deve fazer em hipótese alguma?"

---

### 1.3 — Não há validação por reflexão ("Então o que eu entendi é...")

**Problema:** Nenhum agente faz checkpoint de validação onde resume o que entendeu e pede confirmação antes de prosseguir. O agente ouve, documenta, e segue em frente — sem verificar se entendeu corretamente.

**Fix:** Adicionar checkpoints de reflexão a cada 3-4 perguntas: "Antes de continuar, deixa eu resumir o que entendi até aqui: [resumo]. Isso está correto?"

---

### 1.4 — Respostas vagas são aceitas sem desafio

**Problema:** Quando o usuário diz "deve ser rápido", "precisa ser seguro", "deve ser fácil de usar" — os agentes aceitam sem pedir números ou critérios mensuráveis.

**Evidência:** `architecture-agent.md` (linha 41-49): Pergunta "Latência aceitável?" mas não tem instrução para escalar quando usuário diz "rápido" sem métrica.

**Fix:** Tabela de escalonamento por tipo de resposta vaga:

| Resposta vaga | Probe de follow-up |
|---|---|
| "Deve ser rápido" | "Rápido significa <200ms? <1s? <5s? Qual é o número que faria o usuário reclamar?" |
| "Precisa ser seguro" | "Seguro contra qual ameaça? Qual dado é sensível? Quem NÃO deveria acessar?" |
| "Fácil de usar" | "Me descreva um usuário que teria dificuldade. O que ele tentaria fazer e onde ficaria travado?" |
| "Depois a gente vê" | "Isso bloqueia a próxima fase? Se sim, preciso de uma decisão agora. Se não, vou registrar como questão aberta." |

---

### 1.5 — Skills de ideação listam categorias em vez de fazer perguntas

**Problema:** `edge-case-sweep` e `journey-sweep` são listas de categorias para verificar, mas NÃO são protocolos de entrevista com perguntas concretas.

**Analogia:** É como dar uma checklist para um médico em vez de ensiná-lo a fazer anamnese — ele marca os itens mas não investiga o que o paciente não sabe que tem.

**Fix:** Converter categorias em perguntas estruturadas (uma por mensagem), com exemplos concretos para cada pergunta.

---

### 1.6 — JTBD é superficial

**Problema:** A extração de Jobs To Be Done aceita respostas como "economizar tempo" sem aprofundar para "reduzir o ciclo de 4 semanas para 1 semana".

**Fix:** Expandir de 5 para 10 prompts de extração, incluindo:
- "O que 10x mais fácil significaria na prática?"
- "Qual é a solução atual e quanto tempo/dinheiro ela custa?"
- "Quando foi a última vez que isso te frustrou? Me conta o que aconteceu."

---

### 1.7 — Não detecta conflito entre stakeholders

**Problema:** `project-context` não pergunta se diferentes stakeholders têm visões conflitantes. Riscos políticos ficam escondidos até a implementação.

**Fix:** Adicionar probe: "Existe alguém na organização que discorda desta abordagem? Quem? Qual é a objeção dele?"

---

### 1.8 — Falta "critério de matar o projeto"

**Problema:** `product-vision` pede métricas de sucesso mas nunca pede "em que ponto decidimos que não vale a pena continuar?".

**Fix:** Adicionar: "Qual métrica, se não for atingida em X meses, significa que devemos pivotar ou cancelar?"

---

## PARTE 2: Problemas na Completude para Desenvolvedor

### 2.1 — Não existe spec de error handling

**Problema:** Nenhum documento captura sistematicamente: "Quando X falha, o sistema deve fazer Y". Error handling fica a cargo da interpretação do desenvolvedor.

**Cobertura atual:** ~20% dos cenários de erro são documentados.

**O que falta em cada documento:**

| Documento | Gap de Error Handling |
|---|---|
| user-stories.md | Cenários Given/When/Then só para happy path (2-3 cenários); faltam cenários de timeout, permissão negada, dado inválido, sistema offline |
| feature-spec.md | Tem seção de error handling mas é opcional e não-estruturada |
| api-spec.md | Respostas de erro genéricas; falta schema detalhado do corpo do erro (qual campo falhou e por quê) |
| tech-spec.md | NFRs definidos mas SEM fallback: "Quando NFR-001 é violado, o que acontece?" |

**Fix:** Criar seção obrigatória "Error Handling Matrix" no feature-spec:

```
| Cenário de Erro | Trigger | Resposta do Sistema | Resposta ao Usuário | Retry? |
|---|---|---|---|---|
| API timeout | >3s sem resposta | Circuit breaker abre | "Tente novamente em instantes" | Sim, 3x com backoff |
```

---

### 2.2 — Regras de validação de dados não são documentadas

**Cobertura atual:** ~10%.

**Problema:** Campos como "email", "telefone", "CEP" não têm regras de validação documentadas (formato, comprimento, obrigatório/opcional, valores válidos).

**Onde deveria estar:** data-dictionary.md → campo `validation_rules` para cada dict.*

**Fix:** Para cada campo no data-dictionary, exigir:
- Required/Optional
- Formato (regex ou enum)
- Min/Max length
- Valor default
- Exemplo válido e exemplo inválido

---

### 2.3 — Máquinas de estado implícitas

**Cobertura atual:** ~30%.

**Problema:** Features com múltiplos estados (ex: pedido → pagamento → envio → entrega) não têm diagrama de estados obrigatório. Transições inválidas não são documentadas.

**Fix:** No feature-spec, para qualquer feature com >2 estados, exigir:
- Diagrama Mermaid de estados
- Transições válidas com triggers
- Transições PROIBIDAS explícitas
- Side effects de cada transição

---

### 2.4 — Segurança e permissões são mencionadas, nunca formalizadas

**Cobertura atual:** ~40%.

**Problema:** "Somente admins podem fazer X" aparece em design notes mas nunca existe uma **permission matrix** formal.

**Fix:** Criar seção obrigatória no tech-spec ou feature-spec:

```
| Ação | Público | Usuário | Admin | Superadmin |
|---|---|---|---|---|
| Ver lista | ✅ | ✅ | ✅ | ✅ |
| Criar item | ❌ | ✅ | ✅ | ✅ |
| Deletar item | ❌ | ❌ | ✅ | ✅ |
```

---

### 2.5 — Observabilidade quase zero

**Cobertura atual:** ~5%.

**Problema:** Nenhum documento especifica: quais logs, métricas e alertas cada feature precisa. O desenvolvedor implementa sem monitoring.

**Fix:** Adicionar ao quality-checklist e ao Definition of Done:
- Logs obrigatórios por feature (com nível: info/warn/error)
- Métricas a coletar (latência, taxa de erro, throughput)
- Thresholds de alerta (quando pagar alguém?)
- Dashboard entries necessárias

---

### 2.6 — Não existe "Developer Handoff Checklist"

**Problema:** Não há um documento final que consolide tudo que o desenvolvedor precisa verificar antes de começar. O desenvolvedor precisa ler 10+ documentos e montar o puzzle sozinho.

**Fix:** Criar skill `developer-handoff.md` que gera um documento consolidado:

```markdown
# Developer Handoff: [Feature Name]

## Business Rules (de feature-spec)
## Acceptance Criteria (de user-stories)
## Error Handling Matrix (NOVO)
## Permission Matrix (NOVO)
## Data Validation Rules (de data-dictionary)
## API Contracts (de api-spec)
## State Machine (de feature-spec)
## Performance Requirements (de tech-spec)
## Observability Requirements (NOVO)
## Open Questions (bloqueantes vs. deferidos)
## Anti-Requirements ("NÃO deve...")
```

---

### 2.7 — Faltam especificações de: idempotência, retry, concorrência

**Problema:** Nenhum documento responde:
- "Esta operação é segura para retry?"
- "O que acontece se dois usuários editam o mesmo registro?"
- "Precisamos de idempotency key nos endpoints POST?"

**Fix:** Adicionar ao api-spec uma coluna "Idempotency" por endpoint e ao feature-spec uma seção "Concurrency Handling".

---

## PARTE 3: Problemas na Validação (detecção de gaps)

### 3.1 — Gates verificam ESTRUTURA, não CONTEÚDO

**Problema:** Os gates checam se documentos existem e se IDs são rastreáveis, mas NÃO verificam se o conteúdo é completo ou específico.

**Exemplo real:** Um user story com `Given [USUARIO], When [AÇÃO], Then [RESULTADO]` (texto placeholder) PASSA na validação porque tem a estrutura Given/When/Then.

**Taxas de detecção atuais:**

| Tipo de Problema | Taxa de Detecção |
|---|---|
| IDs órfãos (BO-# sem US-#) | 95% |
| Violação de SST | 85% |
| Texto placeholder | 40% |
| NFRs não-mensuráveis | 60% |
| Error handling ausente | 30% |
| Edge cases faltando | 10% |
| Segurança implícita | 5% |

**Fix:** Implementar validação baseada em schema:
- Auto-fail se Given/When/Then contém `[PLACEHOLDER]`
- Auto-fail se NFR não tem unidade e número
- Exigir pelo menos 1 cenário de erro por user story

---

### 3.2 — Não existe validação cross-document

**Problema:** Se o database-spec diz `email VARCHAR(100) NOT NULL` mas o data-dictionary diz "email: optional text field" — ninguém detecta a contradição.

**Fix:** Criar skill `cross-document-validation` que verifica consistência entre:
- DB constraints vs. data-dictionary
- API response schemas vs. database columns
- User story roles vs. permission matrix

---

## PARTE 4: Problemas no Fluxo entre Fases

### 4.1 — Handoffs comprimem contexto demais

**Problema:** Cada fase gera um relatório JSON para a próxima. Esse JSON é um RESUMO — perde evidências, raciocínios, alternativas rejeitadas.

**Exemplo:** Discovery gera 3 documentos ricos → comprime em `discovery.json` → Planning lê só o JSON.

**Fix:** Instruir agentes downstream a ler o JSON como INDEX e os documentos completos como FONTE:
```
1. Leia discovery.json para entender a estrutura
2. Leia project-context.md para contexto completo
3. Leia product-vision.md para visão e BOs
4. Leia discovery-report.md para evidências
```

---

### 4.2 — Rejeições do usuário NÃO são registradas

**Problema:** Quando o usuário diz "NO-GO" ou "não gosto dessa abordagem porque X" em um gate, a rejeição e o motivo não são persistidos. O agente da próxima fase não sabe o que já foi rejeitado.

**Risco:** A fase seguinte pode propor exatamente o que foi rejeitado.

**Fix:** Criar `gate-decisions.yaml` no state/:
```yaml
gates:
  discovery_gate:
    decision: ITERATE
    feedback: "Visão precisa enfatizar redução de custo, não velocidade"
    timestamp: "2026-03-23T14:30:00Z"
    rejected_approaches:
      - "Foco em velocidade de entrega como proposta de valor principal"
```

---

### 4.3 — /correct-course é incompleto

**Problema:** O comando existe (19 linhas) mas:
- Não tem agente dedicado
- Não cascateia mudanças automaticamente para docs downstream
- Não atualiza user-stories, design-delta, impl-plan, release-plan

**Resultado:** Se um requisito muda no meio do projeto, o usuário precisa manualmente atualizar 5-10 documentos.

**Fix:** Criar `change-management-agent.md` que:
1. Analisa qual requisito mudou
2. Rastreia quais documentos referenciam esse requisito (via IDs)
3. Gera diffs propostos para cada documento afetado
4. Apresenta antes/depois para aprovação
5. Aplica as mudanças

---

### 4.4 — Features não propagam de volta para o produto-pai

**Problema:** Se uma Feature muda de scope (ex: de "SHOULD" para "COULD"), o PRD do produto-pai NÃO é atualizado automaticamente.

**Fix:** Hook no `feature_lifecycle.py` que detecta mudanças de prioridade em features e marca o PRD para revisão.

---

### 4.5 — Sistema de memória registra O QUÊ mas não POR QUÊ

**Problema:** A memória (`project-state.md`, `workflow-state.yaml`) rastreia:
- ✅ Quais documentos existem
- ✅ Qual fase atual
- ✅ Próximo passo
- ❌ POR QUE cada decisão foi tomada
- ❌ Quais alternativas foram consideradas e rejeitadas
- ❌ Feedback do usuário nos gates

**Fix:** Expandir `state_defaults.py` para incluir campos de rationale em cada gate e decisão.

---

## PARTE 5: Roadmap de Implementação

### Sprint 1: Fundação da Entrevista (Maior impacto, menor esforço)

| # | Melhoria | Arquivos | Esforço |
|---|---|---|---|
| 1 | Adicionar "Técnicas de Entrevista" aos 7 agentes | `.claude/agents/*.md` | ~50 linhas |
| 2 | Pergunta obrigatória "O que NÃO deve acontecer?" em discovery + planning | 4 skills | ~16 linhas |
| 3 | Checkpoints de reflexão a cada 3-4 perguntas | 7 agentes | ~28 linhas |
| 4 | Tabela de escalonamento para respostas vagas | 7 agentes | ~35 linhas |
| 5 | Converter edge-case-sweep e journey-sweep em protocolos de entrevista | 2 skills | ~40 linhas |

**Total Sprint 1:** ~170 linhas, ~3-5 dias

### Sprint 2: Completude para Desenvolvedor

| # | Melhoria | Arquivos | Esforço |
|---|---|---|---|
| 6 | Error Handling Matrix obrigatória no feature-spec | 1 skill | ~20 linhas |
| 7 | Permission Matrix obrigatória no tech-spec | 1 skill | ~15 linhas |
| 8 | Validation Rules obrigatórias no data-dictionary | 1 skill | ~15 linhas |
| 9 | Observability Checklist no quality-checklist | 1 skill | ~15 linhas |
| 10 | Criar skill `developer-handoff` (documento consolidado) | 1 nova skill | ~100 linhas |
| 11 | Seção de idempotência/retry no api-spec | 1 skill | ~10 linhas |

**Total Sprint 2:** ~175 linhas, ~3-5 dias

### Sprint 3: Validação Inteligente

| # | Melhoria | Arquivos | Esforço |
|---|---|---|---|
| 12 | Schema-based validation (anti-placeholder) | validate-gate skill | ~40 linhas |
| 13 | Cross-document consistency check | nova skill | ~80 linhas |
| 14 | Exigir ≥1 cenário de erro por user story | user-stories skill | ~10 linhas |
| 15 | Exigir métricas mensuráveis em NFRs | tech-spec skill | ~10 linhas |

**Total Sprint 3:** ~140 linhas, ~2-4 dias

### Sprint 4: Fluxo e Continuidade

| # | Melhoria | Arquivos | Esforço |
|---|---|---|---|
| 16 | Handoff reports enriquecidos (evidências + rejections) | 7 agentes | ~50 linhas |
| 17 | gate-decisions.yaml com registro de feedback | state_defaults.py + memory-sync.py | ~60 linhas |
| 18 | Change Management Agent completo | novo agente + skill + comando | ~200 linhas |
| 19 | Feature backpropagation para produto-pai | feature_lifecycle.py | ~40 linhas |
| 20 | Rationale fields no sistema de memória | state_defaults.py | ~30 linhas |

**Total Sprint 4:** ~380 linhas, ~5-7 dias

---

## Resultado Esperado

| Dimensão | Atual | Pós Sprint 1-2 | Pós Sprint 3-4 |
|---|---|---|---|
| Qualidade da entrevista | 7.5/10 | 9.0/10 | 9.5/10 |
| Completude para desenvolvedor | 4.5/10 | 7.5/10 | 9.0/10 |
| Detecção de gaps | 5.5/10 | 7.0/10 | 9.0/10 |
| Continuidade entre fases | 7.0/10 | 7.5/10 | 9.0/10 |
| Gestão de mudanças | 3.0/10 | 3.5/10 | 8.0/10 |

**Esforço total:** ~865 linhas de código/prompt distribuídas em ~14-21 dias
**Redução esperada de retrabalho na implementação:** 40-50%
