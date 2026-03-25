---
doc_meta:
  id: checks
  display_name: Checklist Library
  pillar: Operate
  owner_role: Enablement Lead
  summary: Maintains reusable readiness, QA, and review checklists for the documentation flow.
  order: 0.9
  gate: meta
  requires: []
  optional: []
  feeds: []
uuid: <UUID>
version: 3.0.0
status: Guide
owners:
- <owners>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- Checklists
- Gates
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Checklists — 3 Gates

**Recommended path:** `docs/implementation/quality-checklist.md`

---

## Gate 1: Discovery Gate (after project-context + product-vision)

- [ ] Problem Statement sem solução embutida
- [ ] 5W2H com números (Who/What/Where/When/Why/How/How Much)
- [ ] HMW (How Might We) com oportunidades priorizadas
- [ ] CSD priorizada + **kill criteria** por suposição
- [ ] BO-# com baseline → target → timeline
- [ ] North Star Metric definida com baseline e target
- [ ] Anti-goals documentados (o que NÃO fazer)
- [ ] Project context atualizado (stack, constraints, glossary)

---

## Gate 2: Planning Gate (after PRD + user-stories + feature-specs)

- [ ] PRD-F-# com Success Criteria + out-of-scope
- [ ] MoSCoW priorização (Must/Should/Could/Won't)
- [ ] US-# com ≥3 cenários (Happy/Alt/Error) + DoD
- [ ] Given/When/Then acceptance criteria para cada US
- [ ] Feature specs criados para features complexas (>3 business rules ou state machine)
- [ ] FS-[name]-# com inputs/outputs tipados, business rules categorizadas, state transitions
- [ ] Traceability: BO-# → PRD-F-# → US-# → FS-[name]-# (cadeia completa)
- [ ] Scope achievable para solo dev / small team

---

## Gate 3: Implementation Readiness (after design phase complete)

### Architecture & Tech
- [ ] Tech Spec: NFR-# com alvo numérico + verificação + owner
- [ ] Arquitetura: C4 + deployment + integrações documentadas
- [ ] ADRs documentados para decisões técnicas chave
- [ ] Táticas de NFR com code patterns

### Data
- [ ] Data requirements definidos com entidades e relacionamentos
- [ ] ERD completo com todas entidades e cardinalidades
- [ ] Database spec: DDL, indexes, constraints, migration strategy
- [ ] Data dictionary: `dict.*` para todos os campos
- [ ] Data catalog: `ev.*` para todos os eventos
- [ ] Data flow diagram com fontes, transformações e destinos

### UX
- [ ] User journeys documentados (happy/alt/error paths)
- [ ] UX sitemap com navegação completa
- [ ] Wireframes para todas as telas core
- [ ] Style guide com design tokens `tok.*`

### API & Implementation
- [ ] API spec completo com endpoints, auth, error envelope
- [ ] Implementation plan com sprints e tarefas
- [ ] Quality checklist preenchido
- [ ] Sprint-status.yaml inicializado

### Cross-Cutting
- [ ] Todos os 21 documentos gerados
- [ ] Traceability chain completa (sem IDs órfãos)
- [ ] Single Source of Truth respeitada (sem definições duplicadas)
- [ ] Nenhuma referência quebrada entre documentos
