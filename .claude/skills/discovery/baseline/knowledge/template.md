# Dados & Contexto (Baseline) — [Produto/Iniciativa]

<!-- STATUS: DRAFT -->

| Field | Value |
|-------|-------|
| **Versao** | v0.1 |
| **Data** | [AAAA-MM-DD] |
| **Owner** | [nome] |
| **Contribuidores** | [lista] |
| **Periodo analisado** | [ex.: ultimos 60 dias] |
| **Fontes principais** | [ex.: GA4, Amplitude, CRM/BMS, BigQuery, Logs, Planilhas, etc.] |

**Source Documents:** project-context.md, product-vision.md (if available)

---

## 1. Objetivo do documento

[Qual decisao este baseline ajudara a tomar? Ex.: priorizar oportunidades e definir escopo de discovery.]

- [3-5 linhas descrevendo o proposito]

---

## 2. Escopo

**Em escopo:**
- [funil/fluxo analisado]
- [segmentos incluidos]

**Fora de escopo:**
- [fluxos nao analisados]
- [segmentos excluidos]

---

## 3. Contexto do negocio (por que agora)

- [pressao de meta, migracao de legado, crescimento, risco, oportunidade]
- [impacto se nao fizer nada]

---

## 4. Fluxo atual (AS-IS)

Descreva em 6-12 bullets o fluxo atual, de ponta a ponta:

1. [passo 1]
2. [passo 2]
3. [passo 3]
4. [passo 4]
5. [passo 5]
6. [passo 6]

**Integracoes/sistemas envolvidos:**
- [Sistema A] — papel no fluxo
- [Sistema B] — papel no fluxo

**Pontos de falha conhecidos:**
- [onde quebra, onde degrada, onde gera retrabalho]

---

## 5. Baseline de metricas (antes)

> Preencher sempre com: **valor**, **periodo**, **fonte** e **confiabilidade** (alta/media/baixa).

### A) Aquisicao e funil (produto/negocio)

| Metrica | Valor | Periodo | Fonte | Confiabilidade |
|---------|-------|---------|-------|----------------|
| Volume (trafego/usuarios) | [[ ]] | [[ ]] | [[ ]] | [[alta/media/baixa]] |
| Taxa de inicio do fluxo | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| Taxa de conclusao/resultado principal | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| Conversao etapa A → B | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| Conversao B → C | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| CAC/CPL (se aplicavel) | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| RPL / Receita por lead (se aplicavel) | [[ ]] | [[ ]] | [[ ]] | [[ ]] |

### B) Qualidade de dados (se houver captura/integracao)

| Metrica | Valor | Periodo | Fonte | Confiabilidade |
|---------|-------|---------|-------|----------------|
| % leads validos | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| % leads invalidos | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| % duplicados | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| Taxa de falha de integracao | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| Campos com maior incidencia de erro | [[lista]] | — | [[ ]] | [[ ]] |

### C) Performance e confiabilidade (quando relevante)

| Metrica | Valor | Periodo | Fonte | Confiabilidade |
|---------|-------|---------|-------|----------------|
| Latencia p50 | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| Latencia p95 | [[ ]] | [[ ]] | [[ ]] | [[ ]] |
| Taxa de erro (4xx/5xx ou crash) | [[ ]] | [[ ]] | [[ ]] | [[ ]] |

**Principais incidentes recentes:**
- [incidente + data]

### D) Operacao (processo e esforco manual)

| Metrica | Valor | Periodo | Fonte | Confiabilidade |
|---------|-------|---------|-------|----------------|
| Horas/semana de retrabalho | [[ ]] | [[ ]] | [[ ]] | [[ ]] |

**Principais tarefas manuais:**
- [tarefa 1]
- [tarefa 2]

**Principais impactos operacionais:**
- [ex.: demora, retrabalho, risco de perda]

---

## 6. Segmentacoes relevantes

| Dimensao | Detalhamento |
|----------|-------------|
| Por canal | [[lista + comparativo se houver]] |
| Por device (mobile/desktop) | [[ ]] |
| Por coorte (novo vs recorrente) | [[ ]] |
| Por tipo de campanha/cliente | [[ ]] |

---

## 7. Restricoes, premissas e dependencias

**Premissas (o que estamos assumindo como verdadeiro):**
- [premissa 1]
- [premissa 2]

**Restricoes (limites reais):**
- Tecnica: [...]
- Legal/Compliance (LGPD/consentimento/PII): [...]
- Operacao: [...]
- Time/capacidade: [...]

**Dependencias (o que precisa acontecer ou existir):**
- [time/sistema/fornecedor]
- [aprovacao de area]
- [mudanca em integracao]

---

## 8. Problemas e dores ja observadas

> Liste como fatos/observacoes com evidencia. **Nao proponha solucao aqui** (isso vem no Discovery/OST).

- **Dor 1:** [...] (evidencia: [...])
- **Dor 2:** [...] (evidencia: [...])
- **Dor 3:** [...] (evidencia: [...])

---

## 9. Lacunas de informacao e plano de coleta

### Tier 1 (sem isso nao da para avancar com seguranca)

| Dado faltante | Responsavel | Data limite |
|---------------|-------------|-------------|
| [dado 1] | [nome] | [AAAA-MM-DD] |
| [dado 2] | [nome] | [AAAA-MM-DD] |

### Tier 2 (importante, mas nao bloqueia)

- [dado ou analise]
- [dado ou analise]

### Plano de coleta (como vamos obter)

| Metodo | Quem | Quando |
|--------|------|--------|
| Entrevistas | [quem] | [quando] |
| Analytics | [quem] | [quando] |
| Logs/infra | [quem] | [quando] |
| CRM/BI | [quem] | [quando] |

---

## 10. Links e anexos

- Dashboards: [...]
- Planilhas: [...]
- Tickets/Incidentes: [...]
- Documentos tecnicos relevantes: [...]
