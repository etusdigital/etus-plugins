# Neo v0 Gap Analysis — Round 2 (prompts/core + prompts/chains)

**Data:** 2026-03-15
**Escopo:** Leitura completa de `prompts/core/` (neo.md, orchestration/, templates/) e `prompts/chains/` (chains definition, components/development XML, components/code_quality XML, components/product_management, components/project_planning_management, agent interfaces) + `index.yaml` + `meta-prompt.txt`
**Objetivo:** Identificar lacunas entre Neo v0 e o que foi implementado no ETUS PMDocs v4.1

---

## Resultado: 5 lacunas reais + 3 parciais

Após leitura detalhada de ~50 arquivos do Neo v0, identifiquei:
- **13 padrões já cobertos** (confirmação de que a implementação está sólida)
- **5 lacunas reais** (padrões valiosos que não implementamos)
- **3 coberturas parciais** (implementamos, mas falta profundidade)
- **7 padrões não aplicáveis** (específicos de código/CI/CD, fora do escopo PMDocs)

---

## LACUNAS REAIS (não implementadas)

### GAP-1: Critique Loop com 3 Soluções Comparadas

**Fonte:** `prompts/core/orchestration/follow-up-critque-prompt.md`

**O que é:** Quando encontra um problema no documento, o Neo v0 não apenas corrige — ele gera 3 soluções distintas para cada issue, compara eficiência, escolhe a melhor, e implementa. O loop repete até não haver mais issues.

**O que temos:** Nosso QUALITY LOOP (D1) faz: gerar → avaliar → identificar falhas → melhorar → reavaliar. Mas a melhoria é direta (1 solução), sem comparação de alternativas.

**Padrão Neo v0 (verbatim):**
```
Step 1. For each issue you identify, describe it in detail within <issue> tags.
Step 2. For each <issue>, come up with 3 distinct potential solutions.
Step 3. Compare the efficiency of the 3 <solution>s for each <issue>.
Step 4. Based on the <efficiency_comparison>, choose the best <solution>.
Step 5. Implement the <best_solution> in a step-by-step manner.
Step 6. Repeat Steps 1 through 5, reviewing the <refined_response>.
```

**Impacto:** ALTO — melhora significativa na qualidade dos documentos críticos (product-vision, prd, architecture-diagram)

**Recomendação:** Atualizar o `## QUALITY LOOP` dos 5 skills críticos para incluir a etapa de "3 soluções + comparação de eficiência" no passo de melhoria.

---

### GAP-2: Genius Agent / Adversarial Expert Review

**Fonte:** `prompts/core/orchestration/reasoning.md`

**O que é:** Após produzir um resultado, o Neo v0 ativa um "genius agent" — um especialista que critica ativamente o output procurando falhas, suposições fracas e alternativas não exploradas. O papel é adversarial, não validatório.

**Padrão Neo v0 (verbatim):**
```
Activate a field-specific genius agent based on the query. The agent represents
a 200 IQ-level human expert who critiques your solution from a third-person
perspective. The genius agent must actively challenge your assumptions and find
weaknesses in your reasoning.
```

**O que temos:** O REFLECTION PROTOCOL (D2) faz assumption audit e alternative perspectives, mas é auto-reflexivo (o mesmo agente se avalia). Não há um segundo agente adversarial que desafia.

**Impacto:** ALTO para fase de Design — Architecture Agent produz; Data/UX/API Agents poderiam atuar como adversários especializados que desafiam decisões de arquitetura.

**Recomendação:** Adicionar `## ADVERSARIAL REVIEW` ao orchestrator para a fase de Design: após Architecture Agent produzir tech-spec, os agentes paralelos recebem instrução explícita de "desafiar NFRs e ADRs antes de aceitá-los como premissa". Isso já acontece implicitamente (cada agente lê o tech-spec), mas a instrução adversarial é o diferencial.

---

### GAP-3: Confidence Scoring Numérico (0-1) por Seção

**Fonte:** `prompts/core/orchestration/reasoning.md`

**O que é:** Cada passo do raciocínio recebe um score de confiança de 0 a 1. Se qualquer passo está abaixo de 0.5, o agente revisa antes de prosseguir. O score é reportado no output final.

**O que temos:** O REFLECTION PROTOCOL usa LOW/MEDIUM/HIGH (qualitativo), que é menos preciso. Não há score numérico por seção do documento.

**Padrão Neo v0 (verbatim):**
```
Use confidence grading (C) for every step of your reasoning, from 0 to 1.
Revisit any step with a confidence score below 0.5, and ensure you've explored
alternatives for low-confidence decisions.
```

**Impacto:** MÉDIO — scores numéricos são mais acionáveis que labels qualitativos, mas podem ser over-engineering para documentação de produto.

**Recomendação:** NÃO implementar scoring 0-1 para todos os skills (overhead excessivo). IMPLEMENTAR apenas para product-vision e prd, que são os documentos que mais sofrem com suposições não validadas. Adicionar ao REFLECTION PROTOCOL desses 2 skills: "Score cada seção 0-1. Se alguma seção < 0.5, pergunte ao usuário antes de prosseguir."

---

### GAP-4: Quality Gates com Entry/Exit Criteria Explícitos

**Fonte:** `prompts/core/orchestration/prompt-chain-orchestrator.md`

**O que é:** Cada quality gate tem critérios de ENTRADA (o que precisa existir para iniciar a validação) e SAÍDA (o que precisa ser verdade para aprovar).

**Padrão Neo v0:**
```yaml
quality_gates:
  requirements:
    entry: [stakeholder_sign_off, scope_definition]
    exit: [requirements_completeness, requirements_consistency]
  design:
    entry: [requirements_approval, architecture_standards]
    exit: [design_completeness, technical_feasibility]
```

**O que temos:** Nosso validate-gate faz checklist de completude e roda check-sst + check-traceability, mas não tem entry criteria formais. Um gate pode ser invocado a qualquer momento, mesmo quando os pré-requisitos não estão satisfeitos.

**Impacto:** MÉDIO — entry criteria evitariam invocações prematuras de gate. O validate-gate já valida se os documentos existem, mas não tem uma lista declarativa de entry conditions.

**Recomendação:** Adicionar `entry_criteria` e `exit_criteria` ao dependency-graph.yaml para cada phase transition (não para cada documento individual). Atualizar validate-gate para verificar entry criteria antes de iniciar a validação.

---

### GAP-5: Validação 3-Camadas (Structure → Content → Dependencies)

**Fonte:** `prompts/core/orchestration/prompt-chain-orchestrator.md`

**O que é:** A validação de cada documento usa 3 camadas distintas:
1. **Structure** — seções obrigatórias existem, formatação correta, cross-references válidas
2. **Content** — completude, precisão, consistência
3. **Dependencies** — upstream docs existem, downstream compatibility, traceability

**O que temos:** Nosso OUTPUT VALIDATION combina structure e content numa checklist única. A checagem de dependencies é feita separadamente pelo DEPENDENCY RESOLUTION no início do skill (não no final). Não há uma validação formal de "downstream compatibility" (o documento gerado é compatível com o que os skills downstream esperam?).

**Impacto:** ALTO para validate-gate — a validação 3-camadas torna o gate mais rigoroso e diagnóstico.

**Recomendação:** Reestruturar as checklists do validate-gate para seguir explicitamente as 3 camadas: Structure → Content → Dependencies. Isso é uma reorganização, não uma adição — o conteúdo já está lá mas não está separado.

---

## COBERTURAS PARCIAIS (implementamos, mas falta profundidade)

### PARTIAL-1: State Management com Variáveis Tipadas

**Fonte:** `prompts/chains/components/development/generate-REVISED-project-requirements.xml`

**O que o Neo v0 faz:** Cada prompt chain declara variáveis de estado com tipo e valor inicial:
```xml
<state_management>
  <variables>
    <variable name="requirements_version" type="string" initial_value="1.0.0" />
    <variable name="change_log" type="array" initial_value="[]" />
    <variable name="impact_analysis_complete" type="boolean" initial_value="false" />
  </variables>
</state_management>
```

**O que temos:** O handoff JSON (phase.json) tem estado por fase, mas sem variáveis declarativas por skill. Cada skill gerencia estado implicitamente.

**Recomendação:** DEFER — o handoff JSON já resolve o problema de state entre fases. Variáveis por skill seriam over-engineering para Claude Code, que não tem runtime persistente.

---

### PARTIAL-2: Output Metrics Quantitativos

**Fonte:** `prompts/chains/components/development/generate-REVISED-project-requirements.xml`

**O que o Neo v0 faz:**
```xml
<output_validation>
  <metrics>
    <metric name="change_coverage" type="percentage">
      <threshold>100</threshold>
    </metric>
    <metric name="requirement_consistency" type="percentage">
      <threshold>95</threshold>
    </metric>
    <metric name="traceability_score" type="percentage">
      <threshold>100</threshold>
    </metric>
  </metrics>
</output_validation>
```

**O que temos:** Nosso OUTPUT VALIDATION é um checklist booleano (pass/fail por item) com threshold ≥90% para COMPLETE. Não calculamos percentuais individuais (change_coverage, consistency, traceability separadamente).

**Recomendação:** DEFER para v5 — adicionar métricas quantitativas ao check-sst e check-traceability (e.g., "traceability_coverage: 87%" em vez de "5 orphan IDs found"). Valor alto mas implementação complexa.

---

### PARTIAL-3: Iteration Loop com 4 Termination Conditions

**Fonte:** `prompts/chains/components/code_quality/code_quality_chain.xml`

**O que o Neo v0 faz:** O loop iterativo tem 4 condições de terminação (priorizadas):
```xml
<termination-conditions>
  <condition type="Pass Status" priority="1">All critical quality gates pass</condition>
  <condition type="Quality Threshold" priority="2">Meets target quality metrics</condition>
  <condition type="Max Iterations" priority="3">Maximum iterations reached</condition>
  <condition type="Diminishing Returns" priority="4">Improvements < threshold between iterations</condition>
</termination-conditions>
```

**O que temos:** Nosso QUALITY LOOP tem 3 condições: ≥90% completeness, <5% improvement, max 3 iterations. Falta a condição de "Pass Status" (todos os gates críticos passam).

**Recomendação:** Adicionar "Pass Status" como condição prioritária ao QUALITY LOOP — se todos os itens da OUTPUT VALIDATION passam, sai do loop imediatamente (sem esperar o threshold de 90%).

---

## JÁ COBERTO (confirmação)

| Padrão Neo v0 | Onde implementamos |
|---------------|-------------------|
| Document chains com next-step | dependency-graph.yaml (requires → produces) |
| Artifact dependency tracking | dependency-graph.yaml |
| Quality gates entre fases | validate-gate skill + orchestrator |
| Input validation antes de processar | ## INPUT VALIDATION em todos os 25 skills |
| Chain validation protocol | check-sst + check-traceability |
| Phase transitions com artifact checklist | Handoff JSON protocol no orchestrator |
| Self-reflection 6-step | REFLECTION PROTOCOL em 3 skills Opus |
| Iterative refinement loop | QUALITY LOOP em 5 skills críticos |
| Status tracking (completed/in_progress/pending) | sprint-status.yaml + handoff JSON |
| STOP if dependency missing | BLOCKS protocol + auto-invocation |
| Anti-rationalization rules | 8 regras no orchestrator |
| Source Documents requirement | Template em todos os skills |
| Traceability ID hierarchy (BO→PRD-F→US→FS→impl) | dependency-graph.yaml + check-traceability |

---

## NÃO APLICÁVEL (fora do escopo PMDocs)

| Padrão Neo v0 | Razão |
|---------------|-------|
| Code quality chain (evaluate → improve → rate → generate loop) | PMDocs gera documentos, não código |
| CI/CD pipeline integration | PMDocs não faz deploy |
| Unit test generation | Fora do escopo |
| Git auto-commit em gates | Nice-to-have mas fora do core |
| Screenshot analyzer (multi-agent) | Específico de UI review, não documentação |
| KISS/YAGNI/SOLID scoring | Aplicável a código, não documentos |
| Vector database memory | Claude Code não tem runtime persistente |

---

## PRIORIZAÇÃO DE IMPLEMENTAÇÃO

| # | Gap | Esforço | Impacto | Prioridade |
|---|-----|---------|---------|------------|
| GAP-1 | Critique Loop 3-soluções | Baixo | Alto | **P0** |
| GAP-5 | Validação 3-camadas no validate-gate | Baixo | Alto | **P0** |
| GAP-2 | Adversarial Review no Design | Médio | Alto | **P1** |
| GAP-4 | Entry/Exit Criteria nos Gates | Médio | Médio | **P1** |
| GAP-3 | Confidence scoring 0-1 (product-vision, prd) | Baixo | Médio | **P2** |
| PARTIAL-3 | Pass Status como termination condition | Baixo | Baixo | **P2** |
| PARTIAL-2 | Output metrics quantitativos | Alto | Médio | **v5** |
| PARTIAL-1 | State management com variáveis tipadas | Alto | Baixo | **SKIP** |
