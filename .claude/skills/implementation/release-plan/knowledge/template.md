# Plano de Release/Rollout — [Produto/Iniciativa] — [Nome do PRD]

<!-- STATUS: DRAFT -->

| Field | Value |
|-------|-------|
| **Versao** | v0.1 |
| **Data** | [AAAA-MM-DD] |
| **Owner (PM)** | [nome] |
| **Co-owner (Tech Lead)** | [nome] |
| **Participantes (monitoramento)** | [lista] |
| **Status** | [Draft / Em review / Aprovado / Em execucao / Concluido] |

**Links:**
- PRD: [link]
- Backlog/Epic: [link]
- Dashboards: [link]
- Feature Flag: [link]
- Runbook: [link] (se existir)

**Source Documents:** implementation-plan.md, quality-checklist.md

---

## 1. Resumo do release

> 5-8 linhas cobrindo: o que, para quem, por que, riscos, como medir.

- **O que sera liberado:** [...]
- **Para quem sera liberado:** [...]
- **Por que isso importa:** [...]
- **Riscos principais:** [...]
- **Como saberemos se deu certo:** [metricas]

---

## 2. Escopo do release

**Inclui:**
- [item 1]
- [item 2]
- [item 3]

**Nao inclui (nao-escopo do release):**
- [item A]
- [item B]

---

## 3. Estrategia de rollout

**Tipo:**
- [ ] Full release (100% de uma vez)
- [ ] Progressivo (ramp-up)
- [ ] Canario (grupo pequeno + expansao)
- [ ] Beta (convite/segmento especifico)
- [ ] Feature flag / toggle

**Configuracao do rollout:**

| Campo | Valor |
|-------|-------|
| Feature flag | [nome] — link: [ ] |
| Segmento inicial | [ex.: 5% / clientes internos / canal X / campanha Y] |
| Ramp-up | [ex.: 5% → 20% → 50% → 100%] |
| Criterio para avancar de etapa | [ex.: guardrails estaveis por 2h/24h] |

---

## 4. Checklist pre-release (go/no-go)

### Requisitos tecnicos

- [ ] Build/testes OK
- [ ] Migracoes aplicadas (se aplicavel)
- [ ] Observabilidade minima (logs/metricas/alertas) configurada
- [ ] Feature flag configurada e testada
- [ ] Rollback testado (quando aplicavel)

### Requisitos de produto

- [ ] Criterios de aceite do PRD atendidos
- [ ] Experiencia validada (Design/PM)
- [ ] Tracking validado (eventos/propriedades)

### Requisitos operacionais

- [ ] CS/Suporte informados e preparados
- [ ] Processos atualizados (se necessario)
- [ ] Plano de comunicacao pronto

### Decisao go/no-go

| Campo | Valor |
|-------|-------|
| Data/hora | [[ ]] |
| Responsaveis | [PM + Tech Lead] |
| Decisao | [GO / NO-GO] |
| Justificativa | [...] |

---

## 5. Metricas e monitoramento

### A) Metricas de sucesso (outcome)

| Metrica | Baseline | Meta | Janela |
|---------|----------|------|--------|
| [nome] | [[ ]] | [[ ]] | [[ ]] |
| [nome] | [[ ]] | [[ ]] | [[ ]] |

### B) Guardrails (nao pode piorar)

| Guardrail | Threshold |
|-----------|-----------|
| [ex.: conversao] | [nao pode cair abaixo de X%] |
| [ex.: p95 latencia] | [nao pode subir acima de Xms] |
| [ex.: taxa de erro] | [nao pode subir acima de X%] |

### C) Metricas operacionais (qualidade e suporte)

| Metrica | Threshold |
|---------|-----------|
| Taxa de erro (4xx/5xx/crash) | [[ ]] |
| Latencia p95 | [[ ]] |
| Tickets criticos | [[ ]] |
| Tempo medio de resposta/incidente | [[ ]] |

### Dashboards (links)

- Produto: [link]
- Tecnico/infra: [link]
- Operacao: [link]

---

## 6. Plano de monitoramento (primeiras 24-72h)

**Ritual:**
- Janela intensiva: [ex.: 2-4h pos-release]
- Acompanhamento: [ex.: daily por 3 dias + revisao semanal]

**Responsaveis:**

| Area | Responsavel |
|------|-------------|
| Produto | [nome] |
| Engenharia | [nome] |
| Data | [nome] |
| Operacao/CS | [nome] |

**Canal de acompanhamento:**
- [Slack/Teams] — [link/canal]

---

## 7. Plano de rollback (gatilhos e procedimento)

### Gatilhos (se acontecer, reverter)

| Gatilho | Threshold | Janela |
|---------|-----------|--------|
| Queda de conversao | > [X%] | por [Y horas] |
| Erros | > [X%] ou incidentes criticos | — |
| p95 latencia | > [X ms] | por [Y min] |
| Tickets criticos | > [N] | em [Y horas] |

### Decisores de rollback

- [PM + Tech Lead] (backup: [nomes])

### Procedimento de rollback

1. **Desabilitar** — [desabilitar flag / reverter deploy]
2. **Validar** — [validar estabilizacao das metricas]
3. **Comunicar** — [comunicar stakeholders impactados]
4. **Post-mortem** — [abrir incidente/post-mortem, se necessario]

---

## 8. Plano de comunicacao

### Comunicacao interna (obrigatoria)

| Campo | Valor |
|-------|-------|
| Publico | [CS, Suporte, Growth, Vendas, Ops, Lideranca] |
| Canal | [Slack/Email/Confluence] |

**Mensagem (resumo):**
- **O que mudou:** [...]
- **Quem e impactado:** [...]
- **Como agir se houver problema:** [...]
- **Onde acompanhar metricas:** [link]

### Comunicacao externa (se aplicavel)

| Campo | Valor |
|-------|-------|
| Publico | [usuarios/clientes] |
| Canal | [in-app/email/changelog] |
| Conteudo | [o que mudou + beneficio + suporte] |

---

## 9. Validacao pos-release e encerramento

**Janela de avaliacao:**
- Curto prazo: [24-72h]
- Medio prazo: [1-2 semanas]

**Criterio para "considerar sucesso":**
- [metricas atingidas + guardrails ok]

**Acoes apos o release:**
- [ ] Registrar learnings
- [ ] Abrir melhorias/bugs restantes
- [ ] Atualizar documentacao (PRD/Release Notes/Runbook)
- [ ] Comunicar resultados para stakeholders
