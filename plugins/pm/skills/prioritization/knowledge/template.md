# Documento de Priorizacao (ICE/RICE) — [Produto/Iniciativa]

<!-- STATUS: DRAFT -->

| Field | Value |
|-------|-------|
| **Versao** | v0.1 |
| **Data** | [AAAA-MM-DD] |
| **Owner** | [nome] |
| **Participantes** | [nomes/areas] |
| **Metodo escolhido** | [ICE ou RICE] |
| **Unidade priorizada** | [Oportunidades / Solucoes / Hipoteses] |
| **Links** | OST [link] / Discovery [link] / Baseline [link] |

**Source Documents:** ost.md, baseline.md (if available), product-vision.md (if available)

---

## 1. Contexto e objetivo

> Principio: sequenciar e escolher.

- [Por que estamos priorizando agora? Qual ciclo/horizonte?]
- [Qual decisao este documento precisa fechar?]
- [5-10 linhas]

---

## 2. Regras do jogo (metodo e escalas)

**Metodo:**
- ICE = (Impacto x Confianca) / Esforco
- _ou_ RICE = (Reach x Impact x Confianca) / Esforco

**Definicoes e escalas (1-5):**

| Dimensao | 1 | 2 | 3 | 4 | 5 |
|----------|---|---|---|---|---|
| **Impacto** | Melhoria marginal | Melhoria perceptivel | Melhoria relevante para metrica | Melhoria significativa e mensuravel | Game-changer para o outcome |
| **Confianca** | Achismo | Poucos sinais | Evidencia parcial (discovery) | Dados + discovery convergem | Dados fortes + validacao |
| **Esforco** | Trivial (<1d) | Pequeno (1-3d) | Medio (1-2 sprints) | Grande (3-4 sprints) | Muito grande (>1 mes) |

(Se RICE)
- **Reach:** alcance estimado no periodo (ex.: usuarios/mes, leads/mes, sessoes/mes)

---

## 3. Lista de itens a priorizar

> Itens vindos da OST, com referencia clara.

- Item 1: [O-1 — titulo]
- Item 2: [O-2 — titulo]
- Item 3: [O-3 — titulo]
- ...

---

## 4. Avaliacao e score (por item)

> Repetir o bloco para cada item.

### Item: [O-1] — [titulo curto]

**a) Impacto (1-5):** [[ ]]

Justificativa do impacto (2-5 linhas):
- [Quais metricas e por que? Baseline → target quando possivel.]

**b) Confianca (1-5):** [[ ]]

Justificativa da confianca (2-5 linhas):
- [Quais evidencias sustentam? Links para discovery/dados.]

**c) Esforco (1-5):** [[ ]]

Justificativa do esforco (2-5 linhas):
- [Estimativa relativa validada com Tech Lead. Principais complexidades.]

**d) Score:**
- ICE: ([I] x [C]) / [E] = [[ ]]
- _ou_ RICE: ([Reach] x [I] x [C]) / [E] = [[ ]]

**e) Dependencias e riscos:**
- Dependencias: [ex.: tracking/eventos, integracao, aprovacoes]
- Riscos: [ex.: LGPD, performance, regressao, adocao]

**f) Prioridade sugerida:** [P0 / P1 / P2]

Racional (2-5 linhas):
- [Por que entra agora ou por que espera.]

---

### Item: [O-2] — [titulo curto]

_(Repetir a mesma estrutura de O-1.)_

---

### Item: [O-3] — [titulo curto]

_(Repetir a mesma estrutura.)_

---

## 5. Ranking final (resumo)

> Escreva em ordem do que sera executado, nao apenas pelo score.

### P0 (neste ciclo)

- [Item] — [1 linha de justificativa]
- [Item] — [...]

### P1 (proximo ciclo / quando houver capacidade)

- [Item] — [...]

### P2 (backlog / avaliar depois)

- [Item] — [...]

---

## 6. Trade-offs e decisoes

**O que ficou de fora e por que:**
- [...]

**Quais riscos estamos aceitando neste ciclo:**
- [...]

**Quais dependencias precisam ser resolvidas primeiro:**
- [...]

---

## 7. Proximos artefatos (o que isso destrava)

A partir dos itens P0, devem ser criados:
- PRD(s): [nome/link a criar]
- Backlog (epicos/historias): [nome/link a criar]
- Plano de Release/Rollout: [nome/link a criar]
- (Opcional) plano de experimento: [nome/link a criar]

---

## O que fazer / o que nao fazer

**O que fazer:**
- Priorizar poucos itens por ciclo (foco).
- Registrar racional escrito (nao apenas numeros).
- Explicitar dependencias e riscos.
- Usar baseline: "de X para Y", sempre que possivel.
- Revisar periodicamente (score muda com novas evidencias).

**O que nao fazer:**
- Nao declarar tudo como P0.
- Nao usar pontuacao como "verdade absoluta" (e ferramenta, nao decisao automatica).
- Nao priorizar sem considerar dependencias (ex.: dashboard sem eventos).
- Nao esconder restricoes (capacidade, legal, integracoes).
- Nao ser apenas tabela sem justificativa.

---

## Responsaveis

- **Owner:** PM da iniciativa/produto.
- **Contribuem:** Tech Lead (esforco e riscos), Data/BI (impacto e baseline), Growth/Operacoes/Design (valor e urgencia).
- **Aprovacao:** Lideranca de Produto + stakeholders do dominio.

---

## Quando usar

Use este template quando:
- houver mais de uma oportunidade/solucao possivel (quase sempre);
- houver restricao de capacidade (time/sprint/trimestre);
- houver disputa de prioridade entre areas;
- voce precisar justificar a ordem de execucao para lideranca.

**Versao curta:** quando houver apenas 1 item claro (mesmo assim registre racional e riscos).
