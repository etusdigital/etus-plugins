# Relatorio de Discovery — [Produto/Iniciativa]

<!-- STATUS: DRAFT -->

| Field | Value |
|-------|-------|
| **Versao** | v0.1 |
| **Data** | [AAAA-MM-DD] |
| **Owner** | [nome] |
| **Contribuidores** | [lista] |
| **Periodo do discovery** | [ex.: 2026-01-01 a 2026-01-14] |
| **Links principais** | [dashboards, entrevistas, docs] |

**Source Documents:** baseline.md, project-context.md, product-vision.md (if available)

---

## 1. Objetivo do discovery

> Principio: evidencia antes de decisao.

- [Qual decisao este discovery pretende habilitar?]
- [Quais riscos queremos reduzir?]
- [3-5 linhas descrevendo o proposito]

---

## 2. Perguntas de pesquisa (o que queriamos responder)

- Q1: [...]
- Q2: [...]
- Q3: [...]

---

## 3. Metodo e amostra

### Fontes qualitativas

- Entrevistas: N = [[ ]]
  - Perfis: [[ ]]
  - Duracao media: [[ ]]
  - Como foi conduzido: [[link/script]]
- Shadowing / suporte / vendas / operacao: [[descricao]]

### Fontes quantitativas

- Dados analisados: [[GA4/Amplitude/CRM/BI/Logs/etc.]]
- Periodo: [[ ]]
- Segmentacoes aplicadas: [[canal/device/coorte/etc.]]

### Outras fontes

- Tickets/CS: [[ ]]
- Incidentes/Logs: [[ ]]
- Documentacao tecnica: [[ ]]

---

## 4. Contexto resumido (o cenario antes do discovery)

> Referencia: baseline.md

- [Resumo do baseline e do problema]
- [Principais restricoes e dependencias ja conhecidas]

---

## 5. Evidencias-chave (lista curta e objetiva)

> Use 5-10 itens. Cada item deve ter uma evidencia associada com fonte.

1. **Evidencia 1:** [...]
   Fonte: [link/dashboard/quote/print]

2. **Evidencia 2:** [...]
   Fonte: [...]

3. **Evidencia 3:** [...]
   Fonte: [...]

4. **Evidencia 4:** [...]
   Fonte: [...]

5. **Evidencia 5:** [...]
   Fonte: [...]

---

## 6. Achados e insights (o que aprendemos)

> Organize por temas. Para cada insight: descreva, inclua evidencia e implicacao.
> Diferencie claramente: **fato observado** vs **hipotese** vs **interpretacao**.

### Tema 1 — [ex.: "Visibilidade de funil inexistente"]

- **Insight:** [...]
- **Tipo:** [fato observado | hipotese | interpretacao]
- **Evidencias:**
  - [dado/quote/print + link]
- **Causa provavel (se houver):** [...]
- **Implicacao para produto:** [...]

### Tema 2 — [ex.: "Qualidade de lead e integracao"]

- **Insight:** [...]
- **Tipo:** [fato observado | hipotese | interpretacao]
- **Evidencias:** [...]
- **Causa provavel:** [...]
- **Implicacao:** [...]

### Tema 3 — [...]

_(Repetir para cada tema.)_

---

## 7. Personas/JTBD (quando aplicavel)

### Persona 1: [nome ou perfil]

- **Job principal:** [...]
- **Dor principal:** [...]
- **Criterio de sucesso:** [...]

### Persona 2: [nome ou perfil]

- **Job principal:** [...]
- **Dor principal:** [...]
- **Criterio de sucesso:** [...]

_(Se nao identificamos personas, registrar: "Nenhuma persona distinta emergiu neste discovery.")_

---

## 8. Mapa de dores (sintomas vs causas)

### Sintomas observados

- [sintoma 1]
- [sintoma 2]
- [sintoma 3]

### Causas provaveis (hipoteses fundamentadas com evidencia)

- [causa 1 + evidencia que sustenta]
- [causa 2 + evidencia que sustenta]

---

## 9. Hipoteses emergentes (sem ainda priorizar)

> Use linguagem mensuravel: baseline → target. IDs: H-#
> Nao priorize aqui — priorizacao e o documento seguinte.

- **H-1:** Se [...], entao [...], medido por [...], de [[baseline]] para [[meta]].
- **H-2:** Se [...], entao [...], medido por [...], de [[baseline]] para [[meta]].
- **H-3:** Se [...], entao [...], medido por [...], de [[baseline]] para [[meta]].

---

## 10. Incertezas e lacunas remanescentes

### Tier 1 (bloqueia decisao)

| Lacuna | Responsavel | Data |
|--------|-------------|------|
| [lacuna 1] | [nome] | [AAAA-MM-DD] |
| [lacuna 2] | [nome] | [AAAA-MM-DD] |

### Tier 2 (nao bloqueia, mas melhora qualidade)

- [...]
- [...]

---

## 11. Recomendacoes e proximos passos

- Atualizar OST com oportunidades baseadas nos insights acima.
- Preparar documento de Priorizacao (ICE/RICE) para decidir P0/P1/P2.
- [Acoes adicionais: instrumentacao, coleta de dados, testes, etc.]

---

## 12. Links e anexos

- Planilhas/Dashboards: [...]
- Gravacoes/Transcricoes: [...]
- Prints/Figma: [...]
- Outros docs: [...]

---

## O que fazer / o que nao fazer

**O que fazer:**
- Registrar metodo (quem, quantos, quando, como) para dar credibilidade ao que foi descoberto.
- Apresentar evidencias-chave (dados, quotes curtas, prints, links) junto com cada insight.
- Ser especifico: sempre que possivel, usar baseline e numeros (mesmo aproximados, com fonte).
- Diferenciar claramente: fato observado vs hipotese vs interpretacao.
- Terminar com implicacoes praticas: "isso significa que devemos..."

**O que nao fazer:**
- Nao virar um "dump" de entrevistas ou metricas sem sintese.
- Nao escrever como PRD (nao fecha escopo nem requisitos).
- Nao tentar priorizar tudo aqui (priorizacao e o documento seguinte).
- Nao usar termos vagos ("significativo", "muito", "melhor") sem referencia de medida.

---

## Responsaveis

- **Owner:** PM (ou Researcher, se houver).
- **Contribuem:** Design, Data/BI, Tech Lead, Growth/Ops/CS (dependendo do tema).
- **Aprovacao:** PM + stakeholders diretamente impactados (ex.: Growth Lead para aquisicao).

---

## Quando usar

Use este template quando:
- a iniciativa for P0/P1 ou tiver risco de impacto em receita, aquisicao, retencao, operacao, LGPD ou reputacao;
- houver mais de uma hipotese plausivel ou mais de um caminho de solucao;
- houver necessidade de alinhamento entre multiplas areas (Produto, Growth, Eng, Ops, CS).

**Versao curta:** quando o problema for pequeno e local, mas ainda assim registre: metodo, evidencias-chave e implicacoes.
