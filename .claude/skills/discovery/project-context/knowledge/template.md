---
doc_meta:
  id: ctx
  display_name: Project Context
  pillar: Discovery
  owner_role: Product Lead
  summary: Living document capturing project identity, team context, technology stack decisions, and constraints.
  order: 0
  gate: discovery
  requires: []
  feeds: [vis, prd, arch, tech]
---

# Project Context

**Last Updated:** [DATE]
**Owner:** [PRODUCT_LEAD_NAME]
**Status:** [DRAFT | APPROVED]

---
## Responsaveis

- **Owner:** PM (Product Manager)
- **Contribuem:** Design Lead, Growth, Tech Lead
- **Aprovacao:** Lideranca de Produto


## Project Identity

### Project Name
[Name of the project]

### Tagline
[One-line descriptive tagline - 5-10 words]

### Elevator Pitch
[30-second description: What is it, for whom, why does it matter?]

---

## Problem Statement

### The Problem
[Clear, specific problem statement. Not "people need better tools" but "solo freelancers lose 5-10 hours/week tracking invoice payments across email, Stripe, and spreadsheets"]

### Who Has This Problem
[Target audience segment. Example: "Freelancers billing $30K-$200K/year"]

### Current Solution
[How do they solve it today? What's the friction?]

### Why It Matters
[Business or user impact. Quantified if possible. Example: "Lost invoice follow-ups cost freelancers ~$500/month in average outstanding balance"]

---

## 5W2H Analysis

### What?
[What are you building? What will it do?]

### Who?
[Who are the primary users? Who are stakeholders?]

### Where?
[Where will this be used? (SaaS, mobile app, embedded, etc.)]

### When?
[When does this need to exist? Launch timeline?]

### Why?
[Why build this? Strategic rationale beyond problem statement?]

### How?
[How will you build it? Broad approach.]

### How Much?
[Budget, resources, timeline, scope limits?]

---

## Goals & Non-Goals

### Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

### Non-Goals (Explicit Out of Scope)
- [ ] Non-goal 1
- [ ] Non-goal 2

---

## Constraints

### Technical Constraints
- [Existing infrastructure limitations, preferred tech stack, platform decisions]

### Business Constraints
- [Budget cap, timeline pressure, regulatory requirements]

### Team Constraints
- [Skill gaps, availability, team size, solo vs. team]

### Market Constraints
- [Competitive landscape, go-to-market limitations, distribution channels]

---

## Assumptions & Risks

### Critical Assumptions
1. [Assumption 1 - e.g., "Users will adopt if invoice sync reduces manual entry by 80%"]
2. [Assumption 2]
3. [Assumption 3]

### Key Risks
1. [Risk 1 - e.g., "Stripe API rate limits may limit real-time sync"] → Mitigation: [Plan to address]
2. [Risk 2] → Mitigation: [Plan to address]

---

## Team Context

### Team Structure
- Team Size: [Solo | 2-3 | 4-8 | 8+]
- Roles & Responsibilities:
  - [Role]: [Name] ([availability])
  - [Role]: [Name] ([availability])

### Skills & Experience
- [Skill area]: [expertise level, e.g., "5 years React frontend"]
- [Skill area]: [expertise level]
- Skill Gaps: [What's missing? How will you address?]

---

## Technology Context

### Existing Stack
- Frontend: [e.g., React 19, Vue 3, vanilla JS]
- Backend: [e.g., Node.js, Go, Python, None]
- Database: [e.g., PostgreSQL, MongoDB, None yet]
- Deployment: [e.g., Vercel, AWS, Hetzner, On-premise]
- Monitoring: [e.g., Datadog, New Relic, None]

### Technology Preferences
- [Preferred frameworks, languages, architectural patterns]
- [Why? Learning investment, team expertise, vendor lock-in concerns]

### Technology Constraints
- [Any platforms off-limits? Legacy system requirements?]

---

## Success Criteria (Launch)

### MVP Launch Criteria
- [ ] Criterion 1 (e.g., "Can sync invoices from 3 payment gateways")
- [ ] Criterion 2 (e.g., "Page load < 2s")
- [ ] Criterion 3

### 90-Day Goals Post-Launch
- [Goal 1 - e.g., "1,000 active users"]
- [Goal 2 - e.g., "NPS > 50"]

---

## Document Metadata

**Document ID:** ctx
**Version:** 1.0
**Last Reviewed:** [DATE]
**Next Review:** [DATE]
**Approval Chain:** [Who approved this?]

---


## O que fazer / O que nao fazer

**O que fazer:**
- Ser claro, curto e verificavel
- Registrar restricoes reais (tecnicas, legais, operacionais)
- Explicitar o que esta fora de escopo
- Incluir metricas de sucesso com numero e prazo

**O que nao fazer:**
- Nao propor solucoes aqui (isso e Discovery/Vision)
- Nao virar roadmap ou cronograma
- Nao usar termos vagos sem metrica ("melhorar performance")
- Nao misturar problema com solucao no Problem Statement

## Related Documents

- Feeds into: [product-vision.md](../product-vision.md)
- Referenced by: [prd.md](../../planning/prd.md), [architecture-diagram.md](../../design/architecture-diagram.md), [tech-spec.md](../../design/tech-spec.md)
