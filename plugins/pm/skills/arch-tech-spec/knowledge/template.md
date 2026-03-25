# Tech Spec Template

## Responsaveis

- **Owner:** Tech Lead
- **Contribuem:** PM, Dev team, DevOps, Security
- **Aprovacao:** PM + Tech Lead

## Table of Contents

1. [Expected Sections](#expected-sections)
2. [1. Technical Overview](#1-technical-overview)
3. [2. Non-Functional Requirements](#2-non-functional-requirements-nfrs)
4. [3. Architecture Decision Records](#3-architecture-decision-records-adrs)
5. [4. Security Architecture](#4-security-architecture)
6. [5. Observability Stack](#5-observability-stack)
7. [6. Infrastructure & DevOps](#6-infrastructure--devops)
8. [7. Technical Constraints](#7-technical-constraints)
9. [8. Technical Risks & Mitigations](#8-technical-risks--mitigations)
10. [Completeness Checklist](#checklist-of-completeness)
11. [Example Final Structure](#example-of-final-structure)

---

## Expected Sections

This document captures all quantified non-functional requirements and architectural decisions. It is the Single Source of Truth for technical requirements.

### 1. Technical Overview

**Description:** Executive summary of technical decisions.
- System name
- Chosen architectural pattern
- Main stack (language, framework, database)
- Performance/scalability target in one line
- Security strategy in summary

**Example:**
```
# Tech Spec - [System Name]

System [Name] uses **[Monolith | Microservices | Serverless]** pattern
with [summarized stack: Node.js + Express + PostgreSQL + Redis].

**Target:** p95 latency ≤ [ms], supports [K users/year], uptime [%].

**Security:** [Encryption type], [auth method], [compliance].
```

---

## 2. Non-Functional Requirements (NFRs)

**Description:** Complete table of quantified non-functional requirements.

**Table Format:**

| ID    | Category        | Requirement                                      | Metric              | Target                    | Priority | Justification                         |
|-------|------------------|------------------------------------------------|----------------------|---------------------------|------------|---------------------------------------|
| NFR-1 | Performance      | Latency for critical operations                | p95 latency          | ≤ 200 ms                  | Critical   | UX requirement, user research showed |
| NFR-2 | Performance      | API Throughput                                 | RPS (requests/sec)   | ≥ 1,000 RPS               | High       | Year 1 scale                         |
| NFR-3 | Performance      | Response time for downloads                    | Download latency     | ≤ 5s for 10MB             | High       | User expectation                      |
| NFR-4 | Scalability      | Support concurrent users                       | Concurrent users     | ≥ 10,000 users            | High       | Expected production peak             |
| NFR-5 | Scalability      | Data growth                                    | Data retention       | ≤ 500 GB/year             | Medium     | 3-year projection                    |
| NFR-6 | Reliability      | System availability                            | Uptime               | ≥ 99.9% (9h downtime/year) | Critical   | Customer SLA                         |
| NFR-7 | Reliability      | Recovery Time Objective (RTO)                  | Recovery time        | ≤ 15 minutes              | High       | Business cannot be down             |
| NFR-8 | Reliability      | Recovery Point Objective (RPO)                 | Maximum data loss    | ≤ 1 hour                  | High       | Daily backup + replication          |
| NFR-9 | Security         | Encryption in transit                          | Protocol             | TLS 1.3 + HSTS            | Critical   | Compliance + security best practice |
| NFR-10| Security         | Encryption at rest                             | Algorithm            | AES-256                   | Critical   | PII sensitivity                      |
| NFR-11| Security         | Authentication method                          | Protocol             | OAuth2 + PKCE             | Critical   | Industry standard, user convenience |
| NFR-12| Observability    | Log retention                                  | Days                 | ≥ 30 days                 | Medium     | Troubleshooting + compliance        |
| NFR-13| Observability    | Alert response time                            | Minutes              | ≤ 5 minutes               | High       | Production incident response        |
| NFR-14| Maintainability  | Code coverage                                  | Percentage           | ≥ 80%                     | Medium     | Quality assurance                    |
| NFR-15| Maintainability  | Deploy frequency                               | Times/week           | ≥ 1 deployment/day        | Medium     | CI/CD pipeline efficiency           |

**Expected output:**
- Minimum 10-15 NFRs covered
- Each with: ID, category, quantified metric, clear target
- Justification based on PRD, user research, or business requirements

---

## 3. Architecture Decision Records (ADRs)

**Description:** Architectural decisions documented with trade-offs.

**Format for each ADR:**

#### ADR-1: [Title of Decision]

**Status:** Accepted | Pending | Rejected | Superseded

**Context:**
[Why was this decision necessary? What problem does it solve? What constraints motivated it?]

**Decision:**
[What was decided? Which pattern/technology/approach was chosen?]

**Consequences:**
[What are the implications of this decision? Positive and negative.]

**Trade-offs vs Alternatives:**
- **Option A (chosen):** [Advantages] vs [Disadvantages]
- **Option B (rejected):** Why not? [Technical or business reasons]
- **Option C (rejected):** Why not? [Technical or business reasons]

**Implementation Notes:**
[Technical details for implementation, if relevant]

**Related ADRs:**
[If there are related ADRs, list them]

---

#### ADR-2: Main Architectural Pattern

**Status:** Accepted

**Context:**
Team of [N] people, scale requirements up to [K users/year],
deadline [time]. Needs to support [multiple domains | simple logic].

**Decision:**
**[Monolith | Microservices | Serverless]** architecture.

**Consequences:**
- **Scalability:** [How it scales? Limits?]
- **Deployments:** [Frequency, risks, complexity]
- **Testing:** [Unit, integration, E2E]
- **Team Dynamics:** [How teams work with this pattern]

**Trade-offs vs Alternatives:**
- **Monolith:** Simple at start, limited scalability, monolithic deploy
- **Microservices:** Scalable, operationally complex, independent teams
- **Serverless:** Zero infrastructure, vendor lock-in, cold start latency

**Chosen:** [Monolith] because [project-specific reasons]

---

#### ADR-3: Database Pattern

**Status:** Accepted

**Context:**
Data [structured | semi-structured | hybrid], queries [simple | complex],
scale [small | medium | large].

**Decision:**
[Relational | NoSQL | Hybrid] with [PostgreSQL | MongoDB | etc].

Replication: [None | Master-Slave | Multi-Master]
Partitioning: [None | Range | Hash] (threshold: [number]K records)

**Consequences:**
- **Consistency:** [ACID, eventual consistency, hybrid]
- **Scaling:** [How it scales? Sharding limits?]
- **Backup:** [Strategy, frequency, RTO/RPO]

**Trade-offs vs Alternatives:**
- **PostgreSQL (Relational):** ACID compliance, complex queries, scaling via read replicas
- **MongoDB (NoSQL):** Schema flexibility, easier horizontal scaling, less consistency
- **Hybrid:** Relational + cache (Redis) + message queue

**Chosen:** [PostgreSQL] because [project-specific reasons]

---

#### ADR-4: Communication Pattern

**Status:** Accepted

**Context:**
Latency critical? [Yes | No], coupling OK? [Yes | No],
async operations necessary? [Yes | No].

**Decision:**
[REST | gRPC | GraphQL] + [Synchronous | Asynchronous via message queue]

**Consequences:**
- **Latency:** [p50, p95, p99 expected]
- **Throughput:** [Estimated RPS]
- **Complexity:** [Operational, development]

**Trade-offs vs Alternatives:**
- **REST:** Simple, widely understood, less performant at scale
- **gRPC:** Fast, type-safe, steeper learning curve
- **GraphQL:** Flexible for clients, can over-fetch, learning curve

**Chosen:** [REST] because [project-specific reasons]

---

#### ADR-5: Security & Authentication

**Status:** Accepted

**Context:**
PII data? [Yes | No], compliance [GDPR | LGPD | PCI-DSS | None],
users [internal | external | both].

**Decision:**
- **Authentication:** [OAuth2 | JWT | SAML | Custom]
- **Authorization:** [RBAC | ABAC | Attribute-based]
- **Password Policy:** [Complexity, rotation, MFA]
- **Token Storage:** [HTTP-only cookies | localStorage | session]

**Consequences:**
- **User Experience:** [Friction, convenience]
- **Security Posture:** [Attack surface, recovery]
- **Compliance:** [Regulatory, audit]

**Trade-offs vs Alternatives:**
[Document rejected options and why]

**Chosen:** [OAuth2 + PKCE + HTTP-only cookies] because [reasons]

---

#### ADR-6: Observability & Logging

**Status:** Accepted

**Context:**
Log volume [MB/day], uptime SLA [%], debug criticality [High | Medium | Low].

**Decision:**
- **Logging Platform:** [Centralized (ELK, Splunk) | Managed (CloudWatch, Datadog)]
- **Log Levels:** ERROR, WARN, INFO [, DEBUG]
- **Retention:** [30 days | 90 days | custom]
- **Metrics Platform:** [Prometheus | CloudWatch | Datadog]
- **Tracing:** [Jaeger | Datadog APM | None]
- **Alerting:** [PagerDuty | OpsGenie | Native (CloudWatch)]

**Consequences:**
- **Operational Visibility:** [Debug time reduces from X to Y]
- **Cost:** [Estimated per month]
- **Data Privacy:** [Do logs contain PII? How to mask?]

**Trade-offs vs Alternatives:**
[Document self-hosted vs managed, retention levels]

**Chosen:** [ELK Stack self-hosted] because [reasons: cost, control, etc]

---

#### ADR-7: CI/CD & Deployment Strategy

**Status:** Accepted

**Context:**
Team size, deploy frequency [daily | weekly], risk tolerance [low | medium | high].

**Decision:**
- **CI/CD Platform:** [GitHub Actions | GitLab CI | Jenkins]
- **Deployment Strategy:** [Blue-Green | Canary | Rolling | Manual]
- **Environments:** [dev | staging | production]
- **Approval Process:** [Automatic | Manual | Code review]
- **Rollback:** [Automatic on failure | Manual | Gradual]

**Consequences:**
- **Deployment Frequency:** [Capacity for X deploys/day]
- **MTTR (Mean Time To Recovery):** [Minutes for rollback]
- **Risk:** [Chance of breaking production]

**Trade-offs vs Alternatives:**
[Document Blue-Green vs Canary vs Rolling]

**Chosen:** [Blue-Green] because [reasons: zero-downtime, safety, etc]

---

## 4. Security Architecture

**Description:** Deep dive into security.

#### Network Security
- VPC configuration (public/private subnets, NACLs, security groups)
- DDoS protection (AWS Shield, Cloudflare, etc.)
- WAF rules (OWASP Top 10)
- Firewall rules

#### Data Protection
- Encryption at rest (AES-256, encryption key rotation)
- Encryption in transit (TLS 1.3, HSTS, pinning)
- Field-level encryption (PII, sensitive fields)
- Data masking (logs, exports)

#### Access Control
- Authentication method (OAuth2, JWT, SAML, MFA)
- Authorization model (RBAC, ABAC)
- Service-to-service auth (mTLS, API keys)
- Secret management (vault, env vars, rotation)

#### Compliance
- Regulatory requirements (GDPR, LGPD, PCI-DSS, HIPAA, SOC2)
- Data residency (which countries)
- Audit logging (what, who, when)
- Incident response plan (who, how, timeline)

#### Threat Model
- Assets: data, infrastructure, reputation
- Threats: unauthorized access, data breach, DDoS, insider threat
- Mitigations: per threat

---

## 5. Observability Stack

**Description:** Which tools are used.

#### Logging
- **Platform:** [ELK, Splunk, CloudWatch, Datadog, etc]
- **Aggregation:** Which logs are collected? Format? Structured?
- **Retention:** How many days kept?
- **Search:** Which query language?
- **Cost:** Estimated per month/year

#### Metrics
- **Platform:** [Prometheus, CloudWatch, Datadog, Grafana, etc]
- **Collection Interval:** 15s, 30s, 1m?
- **Retention:** How many days kept?
- **Cardinality Limits:** [If Prometheus, what series limit?]
- **Dashboards:** Which metrics are critical (CPU, memory, errors, latency)?

#### Tracing (Distributed)
- **Platform:** [Jaeger, Datadog APM, New Relic, Zipkin, etc]
- **Sampling:** 100% or sampling? If sampling, what %?
- **Trace Context:** How propagated between services? (W3C Trace Context, B3, etc.)
- **Instrumentation:** Automatic or manual?

#### Alerting
- **Platform:** [PagerDuty, OpsGenie, Slack, VictorOps]
- **Critical Alerts:** [List of alerts that trigger on-call]
- **Alert Thresholds:** (ex: error rate > 1%, latency p95 > 1s)
- **Escalation Policy:** How long before escalating?
- **On-Call Schedule:** Who is on-call? How does it rotate?

#### Cost Tracking
- **Platform:** [CloudWatch, Datadog, native cloud provider]
- **Alerts:** [Budget exceeded alerts]
- **Monthly Cost:** [Estimated]

---

## 6. Infrastructure & DevOps

**Description:** How system is operationalized.

#### Environments
- **Development:** Local machines? Docker Compose? Dev cluster?
- **Staging:** Exact production copy? Or reduced version?
- **Production:** Region, multi-region, failover strategy
- **Disaster Recovery:** Backup location, RTO/RPO, drill frequency

#### Infrastructure as Code
- **Tool:** [Terraform, CloudFormation, Helm, etc]
- **Version Control:** Code stored in git? Reviewed?
- **Drift Detection:** How to detect manual changes in prod?

#### Container Registry
- **Platform:** [Docker Hub, ECR, GCR, private registry]
- **Image Retention:** How many versions kept?
- **Scanning:** Automatic vulnerability scanning?

#### Deployment Pipeline
- **Stages:** Build → Test → Stage → Prod
- **Build:** How long does it take? Caching?
- **Tests:** Unit (in build), integration (in stage), E2E (in stage)?
- **Approval:** Manual approval before prod?
- **Deployment:** Expected time? Blue-green, canary?
- **Health Checks:** How long for health check post-deploy?

#### Scaling
- **Horizontal:** Auto-scaling policy? Min/max replicas? Metrics trigger?
- **Vertical:** When to increase instance size? Manual or auto?
- **Database Scaling:** Read replicas? Sharding?

#### Monitoring & Alerting
- **Health Checks:** Who monitors systems? Frequency?
- **Incident Response:** Who responds? SLA? Post-mortem process?
- **Maintenance Windows:** When do deployments happen? Frequency?

---

## 7. Technical Constraints

**Description:** Inherited or imposed technical limitations.

| Constraint              | Description                                  | Impact                                |
|-------------------------|-----------------------------------------------|---------------------------------------|
| Budget                  | [Maximum infrastructure budget/month]        | Limits cloud spend, self-hosting?     |
| Compliance              | [GDPR, LGPD, PCI-DSS, etc]                  | Data residency, encryption, audit    |
| Legacy Systems          | [Integration with existing system?]          | API contracts, data formats           |
| Team Skills             | [Available expertise: Node, Python, etc]     | Influences language, frameworks       |
| Vendor Choices          | [Company uses AWS? Google Cloud preferred?]  | Limits cloud options                  |
| Timeline                | [MVP in X months]                            | Prioritizes simplicity vs scaling     |

---

## 8. Technical Risks & Mitigations

| Risk                                    | Severity | Probability | Mitigation                                              |
|----------------------------------------|----------|-------------|--------------------------------------------------------|
| Database becomes bottleneck at 100K users | High   | Medium      | Read replicas + caching layer (Redis) + monitoring     |
| Security breach leaks PII              | Critical | Low         | Encryption + access control + audit logging + training |
| Cloud costs exceed budget               | Medium   | High        | Monitoring + alerts + auto-scaling tuning              |
| Key employee leaves with critical knowledge | Medium | Low        | Documentation + knowledge sharing sessions             |
| Third-party API rate limit hits        | Medium   | Medium      | Caching + retry strategy + contact vendor              |

---

## Checklist of Completeness

Before marking as complete:
- [ ] Technical overview section exists?
- [ ] NFRs table is complete (at least 10 NFRs)?
- [ ] Each NFR has: category, metric, target, priority, justification?
- [ ] ADRs documented (at least 5)?
- [ ] Each ADR has: status, context, decision, consequences, trade-offs?
- [ ] Security Architecture section details: network, data, access, compliance, threat model?
- [ ] Observability Stack specifies: logging, metrics, tracing, alerting, cost?
- [ ] Infrastructure & DevOps covers: environments, IaC, registry, pipeline, scaling, monitoring?
- [ ] Technical Constraints identified?
- [ ] Risks & Mitigations documented (3-5 risks)?
- [ ] IDs (NFR-#, ADR-#) registered in ids.yml?
- [ ] Document in English?
- [ ] User confirmed satisfaction?

## Example of Final Structure

```
# Tech Spec - [System]

## 1. Technical Overview
[Summary, pattern, performance/scale/uptime target]

## 2. Non-Functional Requirements (NFRs)
[Table NFR-1 through NFR-N]

## 3. Architecture Decision Records (ADRs)
### ADR-1: Main Architectural Pattern
[Status, context, decision, consequences, trade-offs]

### ADR-2: Database
[...]

### ADR-3: Communication
[...]

### ADR-4: Security & Authentication
[...]

### ADR-5: Observability
[...]

### ADR-6: CI/CD & Deployment
[...]

### ADR-7: [Another important decision]
[...]

## 4. Security Architecture
[Network, data, access, compliance, threat model]

## 5. Observability Stack
[Logging, metrics, tracing, alerting, cost]

## 6. Infrastructure & DevOps
[Environments, IaC, registry, pipeline, scaling, monitoring]

## 7. Technical Constraints
[Constraints table]

## 8. Technical Risks & Mitigations
[Risks table]
```

---

**Version:** 1.0
**Language:** English (en-US)
**Model:** NFR-centric + ADR Architecture Decision Records
**SST:** NFRs and ADRs ONLY in this document

## O que fazer / O que nao fazer

**O que fazer:**
- Quantificar todo NFR com metrica e alvo (< 200ms p95, nao "rapido")
- Documentar alternativas consideradas em cada ADR
- Incluir metodo de verificacao para cada NFR
- Manter NFR-# e ADR-# como IDs imutaveis

**O que nao fazer:**
- Nao usar linguagem subjetiva ("bom", "seguro", "escalavel")
- Nao definir NFR sem metodo de medicao
- Nao duplicar NFR-# ou ADR-# em outros documentos
- Nao incluir pseudo-codigo ou detalhes de implementacao

