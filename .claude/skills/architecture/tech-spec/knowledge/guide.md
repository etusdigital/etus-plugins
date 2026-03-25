# Tech Spec - Interview Guide

## Table of Contents

1. [Objective](#objective)
2. [Block 1: Preparation & Context](#block-1-preparation--context-5-minutes)
3. [Block 2: Non-Functional Requirements](#block-2-non-functional-requirements-nfrs-30-minutes)
4. [Block 3: Architecture Decision Records](#block-3-architecture-decision-records-adrs-20-minutes)
5. [Block 4: Security Architecture Deep Dive](#block-4-security-architecture-deep-dive-10-minutes)
6. [Block 5: Observability Stack](#block-5-observability-stack-5-minutes)
7. [Block 6: Infrastructure & DevOps + Validation](#block-6-infrastructure--devops--validation-10-minutes)
8. [Expected Timeline](#expected-timeline)
9. [Checklist for the Skill](#checklist-for-the-skill)

---

## Objective

This guide structures questions and interactions to generate the tech-spec.md document in an interactive, conversational, and iterative manner.

It follows 6 thematic blocks to cover all necessary NFRs and ADRs.

---

## Block 1: Preparation & Context (5 minutes)

### Objective

Read and understand the architecture defined in architecture-diagram.md.

### Questions

1. **"I'll review the architecture-diagram.md you generated. Let me confirm I understood..."**
   - Summarize architectural pattern chosen
   - Confirm technology stack (frontend, backend, database, cache, queue)
   - Confirm deployment constraints (cloud, region, budget)

2. **"Does anyone on the team have expertise in quantifying non-functional requirements?"**
   - Response: yes/no/partial
   - If not, warn that I'll help define reasonable values based on patterns

### Confirmation Pattern
```
"So, confirming:
- Architecture: [pattern]
- Stack: [technologies]
- Deployment: [cloud/on-premise, where]
- Team: [size, expertise]

Is that correct?"
```

### Next Step
If confirmed → Block 2. If not → Clarify or go back to architecture-diagram.

---

## Block 2: Non-Functional Requirements (NFRs) (30 minutes)

### Objective

Define and quantify 10-15 non-functional requirements across 6 categories.

Each question creates an NFR-#.

---

### Category 1: Performance (5 min)

#### NFR: Latency for Critical Operations

**Question 1:** "What is the most critical operation in the system? (ex: login, payment, search)"

Expected response: list critical operations

**Question 2:** "What latency is acceptable for this operation?"

Expected response: number in ms (100ms, 200ms, 500ms, 1s, etc.)

**Question 3:** "Are we talking about p50, p95, or p99?"

Expected response: p95 is standard (satisfies 95% of users)

**Synthesize and create:**
```
NFR-1: p95 latency for critical operations ≤ [ms]
- Operations: [list]
- Justification: [based on PRD requirement or user research]
```

#### NFR: API Throughput

**Question 4:** "What RPS (requests per second) is expected at peak?"

Expected response: number (100, 1K, 10K RPS)

**Question 5:** "How do you estimate this number? Based on how many users?"

Expected response: [N users] × [Y requests per user/min]

**Synthesize and create:**
```
NFR-2: API Throughput ≥ [RPS]
- Estimated based on: [N users] × [Y req/min]
- Safety margin: +30% for peaks
```

#### NFR: Heavy Operations Performance

**Question 6:** "Are there heavy operations? (ex: uploads, exports, reports)"

Response: yes/no. If yes → **Question 7**

**Question 7:** "What SLA for these operations? (ex: upload 100MB ≤ 30s)"

Expected response: maximum latency

**Synthesize and create:**
```
NFR-3: Latency of [heavy operation] ≤ [time]
- Maximum size: [MB/GB]
- Requires asynchronous operation? [yes/no]
```

---

### Category 2: Scalability (5 min)

#### NFR: Support Concurrent Users

**Question 8:** "How many concurrent users at peak? (not total, but simultaneous)"

Expected response: number (1K, 10K, 100K simultaneous users)

**Question 9:** "What is the date of this peak? (during beta, after 6 months, 1 year?)"

Expected response: timeline

**Synthesize and create:**
```
NFR-4: Support [N] concurrent users
- Timeline: [date]
- Based on: [%/month] growth projection
```

#### NFR: Horizontal Scalability

**Question 10:** "Does system need to scale horizontally (more machines) or is vertical (bigger machine) OK?"

Expected response: horizontal/vertical/both. Why?

**Synthesize and create:**
```
NFR-5: Scalability [horizontal | vertical | both]
- Reason: [cost, latency, availability]
```

#### NFR: Data Volume

**Question 11:** "How much data will be stored? (MB, GB, TB?)"

Expected response: estimate. If unsure: do projection (N users × Y data per user)

**Synthesize and create:**
```
NFR-6: Data volume ≤ [GB/TB] after [period]
- Growth: [% per month]
- Requires sharding? Backup strategy?
```

---

### Category 3: Reliability (5 min)

#### NFR: Availability (Uptime)

**Question 12:** "What is the expected uptime SLA?"

Expected response: 99%, 99.9%, 99.99%, or "not critical"

**Question 13:** "Why? Does it impact business if it goes down?"

Expected response: reason (critical for sales, etc.)

**Synthesize and create:**
```
NFR-7: Availability ≥ [%] (maximum [X] hours downtime/year)
- Critical because: [business reason]
- Requires multi-region? Load balancer?
```

#### NFR: Recovery Time Objective (RTO)

**Question 14:** "If the system fails in production, what is the maximum acceptable recovery time?"

Expected response: minutes/hours (15 min, 1 hour, 4 hours)

**Synthesize and create:**
```
NFR-8: RTO (Recovery Time Objective) ≤ [time]
- Means: failure → system online in [time]
- Requires: [automatic failover, fast backup, etc.]
```

#### NFR: Recovery Point Objective (RPO)

**Question 15:** "How much data is OK to lose in case of disaster?"

Expected response: hours/days (1 hour, 1 day)

**Synthesize and create:**
```
NFR-9: RPO (Recovery Point Objective) ≤ [time]
- Means: maximum [time] of lost data
- Requires: backup every [frequency]
```

#### NFR: Data Durability

**Question 16:** "What is acceptable risk of data loss? (ex: 1 in 1 billion)"

Expected response: number (or use standard: 99.999999999% = 11 nines)

**Synthesize and create:**
```
NFR-10: Data Durability ≥ [11-nines or percentage]
- Requires: [multi-region replication, checksum, etc.]
```

---

### Category 4: Security (5 min)

#### NFR: Encryption in Transit

**Question 17:** "What is minimum TLS standard?"

Expected response: TLS 1.2, TLS 1.3, etc.

**Synthesize and create:**
```
NFR-11: Encryption in Transit ≥ TLS [version]
- All endpoints HTTPS?
- HSTS header? (Force HTTPS)
```

#### NFR: Encryption at Rest

**Question 18:** "Do sensitive data (PII, payment info) require encryption at rest?"

Response: yes/no. If yes → **Question 19**

**Question 19:** "What algorithm? (AES-256 is standard)"

Expected response: AES-256 (or other)

**Synthesize and create:**
```
NFR-12: Encryption at Rest (AES-256)
- Applies to: [PII, payment info, etc.]
- Key management: [HSM, KMS, env vars]
```

#### NFR: Compliance & Regulatory

**Question 20:** "Any compliance requirements? (GDPR, LGPD, PCI-DSS, HIPAA, SOC2)"

Response: yes/no/list. If yes → **Question 21**

**Question 21:** "What is the impact? (data residency, audit logging, etc.)"

Expected response: specific requirements

**Synthesize and create:**
```
NFR-13: Compliance [GDPR | LGPD | PCI-DSS | etc]
- Data residency: [country/region]
- Audit logging: [yes/no, frequency]
- Regular audits: [yes/no, frequency]
```

#### NFR: Authentication Method

**Question 22:** "What authentication method? (OAuth2, JWT, SAML, custom)"

Response: (should be in architecture-diagram). If not → decide now.

**Synthesize and create:**
```
NFR-14: Authentication [OAuth2 | JWT | SAML]
- MFA required? [yes/no]
- Token expiry: [time]
```

---

### Category 5: Observability (3 min)

#### NFR: Log Retention

**Question 23:** "How long to keep logs?"

Expected response: days (30, 90, 365)

**Synthesize and create:**
```
NFR-15: Log Retention ≥ [days]
- Platform: [ELK, CloudWatch, Datadog, etc.]
- Cost estimate: [$/month]
```

#### NFR: Alert Response Time

**Question 24:** "When a critical alert fires, what is the SLA to respond?"

Expected response: minutes (5, 15, 30)

**Synthesize and create:**
```
NFR-16: Alert Response Time ≤ [minutes]
- On-call rotation: [24/7, business hours, etc.]
- Escalation: [yes/no, after how long]
```

---

### Category 6: Maintainability (2 min)

#### NFR: Code Coverage

**Question 25:** "What is the code coverage target?"

Expected response: percentage (50%, 80%, 90%)

**Synthesize and create:**
```
NFR-17: Code Coverage ≥ [%]
- Tool: [Jest, Coverage.py, etc.]
- Evaluated: [per PR, CI/CD gate]
```

#### NFR: Deploy Frequency

**Question 26:** "How often do you want to deploy?"

Expected response: times per day, week, etc.

**Synthesize and create:**
```
NFR-18: Deploy Frequency ≥ [X deploys/day]
- Requires: [automated testing, CI/CD, canary]
```

---

### NFRs Synthesis Pattern

```
"Great. Summarizing the non-functional requirements we defined:

Performance:
- NFR-1: p95 latency ≤ [ms]
- NFR-2: Throughput ≥ [RPS]

Scalability:
- NFR-3: [N] concurrent users
- NFR-4: Growth of [%/month]

Reliability:
- NFR-5: Uptime ≥ [%]
- NFR-6: RTO ≤ [time]
- NFR-7: RPO ≤ [time]

Security:
- NFR-8: TLS 1.3 + encryption at rest
- NFR-9: [Compliance requirement]

Observability:
- NFR-10: Log retention [days]
- NFR-11: Alert response [minutes]

Maintainability:
- NFR-12: Code coverage ≥ [%]
- NFR-13: Deploy [X times/day]

All correct?"
```

### Next Step
→ Block 3

---

## Block 3: Architecture Decision Records (ADRs) (20 minutes)

### Objective

Document 5-7 architectural decisions with trade-offs.

Follows pattern: Status → Context → Decision → Consequences → Trade-offs

---

### ADR-1: Main Architectural Pattern

**Question 27:** "Which architectural pattern was chosen?"

Response: [Monolith | Microservices | Serverless] (should be in architecture-diagram)

**Question 28:** "Why that choice? What were the trade-offs?"

Expected response: technical and business reasons

**Synthesize:**
```
ADR-1: Main Architectural Pattern

Status: Accepted

Context:
- Team of [N] people
- Scale requirements up to [K users/year]
- Priority: [fast MVP | scalability | operational simplicity]

Decision:
Use [Monolith | Microservices | Serverless] pattern

Consequences:
- Deployment: [frequency, risk]
- Scalability: [limits, how it scales]
- Team dynamics: [how teams work]

Trade-offs:
- Monolith: Simple at start, limited scaling
- Microservices: Scalable, operationally complex
- Serverless: Zero infrastructure, vendor lock-in

Chosen [Monolith] because [specific reasons]
```

---

### ADR-2: Database Pattern

**Question 29:** "Which database pattern was chosen?"

Response: [Relational | NoSQL | Hybrid] (should be in architecture-diagram)

**Question 30:** "Replication and sharding? When do you need to partition?"

Response: replication strategy (master-slave, multi-master), sharding threshold

**Synthesize:**
```
ADR-2: Database Pattern

Status: Accepted

Context:
- Data: [structured | semi-structured | hybrid]
- Queries: [simple | complex]
- Scale: [small | medium | large]
- RPO: [NFR-X]

Decision:
[PostgreSQL | MongoDB | Hybrid] with [type] replication
Sharding at [threshold] records

Consequences:
- Consistency: [ACID | eventual | hybrid]
- Scaling: [how it scales]
- Backup: [strategy, RTO/RPO]

Trade-offs:
- Relational: ACID, complex queries, scaling via replicas
- NoSQL: Flexibility, easier horizontal scaling, eventual consistency

Chosen [PostgreSQL] because [reasons]
```

---

### ADR-3: Communication Pattern

**Question 31:** "Which communication pattern? (REST, gRPC, GraphQL)"

Response: (should be in architecture-diagram)

**Question 32:** "Asynchronous operations? (message queue, event-driven)"

Response: yes/no. If yes → which message broker?

**Synthesize:**
```
ADR-3: Communication Pattern

Status: Accepted

Context:
- Latency critical? [yes/no]
- Coupling acceptable? [yes/no]
- Async operations necessary? [yes/no]

Decision:
Use [REST | gRPC | GraphQL] + [Synchronous | Asynchronous via RabbitMQ/Kafka]

Consequences:
- Latency: [p50, p95 expected]
- Throughput: [RPS capacity]
- Complexity: [dev, operational]

Trade-offs:
- REST: Simple, widely understood, less performant
- gRPC: Fast, type-safe, steeper learning
- GraphQL: Flexible for clients, can over-fetch

Chosen [REST] because [reasons]
```

---

### ADR-4: Security & Authentication

**Question 33:** "Which authentication method was chosen?"

Response: [OAuth2 | JWT | SAML | Custom] (should be in architecture-diagram)

**Question 34:** "Where to store tokens? (HTTP-only cookies, localStorage, session)"

Response: best practice is HTTP-only cookies (secure against XSS)

**Synthesize:**
```
ADR-4: Security & Authentication

Status: Accepted

Context:
- PII data? [yes/no]
- Compliance: [GDPR | LGPD | PCI-DSS | etc] (NFR-X)
- Users: [internal | external | both]

Decision:
- Authentication: [OAuth2 + PKCE]
- Authorization: [RBAC | ABAC]
- Token storage: [HTTP-only cookies]
- Password policy: [requirements]
- MFA: [yes/no]

Consequences:
- User experience: [friction, convenience]
- Security posture: [attack surface, recovery]
- Compliance: [regulatory]

Trade-offs:
- OAuth2: Industry standard, user convenience, complexity
- JWT: Stateless, scalable, less browser support
- SAML: Enterprise, complex, older

Chosen [OAuth2 + PKCE] because [reasons: user convenience, security]
```

---

### ADR-5: Observability & Logging

**Question 35:** "Which logging platform? (ELK, Splunk, CloudWatch, Datadog, etc)"

Response: preference. If unsure → recommend ELK (open-source) or Datadog (managed)

**Question 36:** "Logging levels? ERROR, WARN, INFO, DEBUG?"

Response: which to use in production? (standard: ERROR, WARN, INFO)

**Synthesize:**
```
ADR-5: Observability & Logging

Status: Accepted

Context:
- Log volume: [MB/day]
- Uptime SLA: [%] (NFR-X)
- Debug criticality: [high | medium | low]

Decision:
- Logging platform: [ELK | Datadog | CloudWatch | etc]
- Log levels: [ERROR, WARN, INFO, DEBUG]
- Retention: [30 days] (NFR-X)
- Metrics platform: [Prometheus | CloudWatch | Datadog]
- Tracing: [Jaeger | Datadog APM | None]

Consequences:
- Observability: [debug time reduces]
- Cost: [estimated per month]
- Data privacy: [PII masking?]

Trade-offs:
- Self-hosted (ELK): Control, low cost, operational overhead
- Managed (Datadog): Comfort, high cost, vendor lock-in

Chosen [ELK] because [reasons: cost, control]
```

---

### ADR-6: CI/CD & Deployment Strategy

**Question 37:** "What is the deployment strategy?"

Response: [Blue-Green | Canary | Rolling | Manual]

**Question 38:** "Deploy frequency target? (daily, weekly)"

Expected response: frequency. Influences complexity.

**Synthesize:**
```
ADR-6: CI/CD & Deployment Strategy

Status: Accepted

Context:
- Team size: [N]
- Deploy frequency target: [X times/day] (NFR-X)
- Risk tolerance: [low | medium | high]

Decision:
- CI/CD platform: [GitHub Actions | GitLab CI | Jenkins]
- Deployment strategy: [Blue-Green | Canary | Rolling]
- Approval process: [Automatic | Manual | Code review]
- Rollback: [Automatic on failure | Manual]
- MTTR target: [minutes] (NFR-X)

Consequences:
- Deployment frequency: [increased to X/day]
- MTTR: [reduced to Y minutes]
- Risk: [chance of breaking prod]

Trade-offs:
- Blue-Green: Zero-downtime, but resource-intensive
- Canary: Gradual rollout, detect issues early, more complex
- Rolling: Resource-efficient, gradual, longer downtime

Chosen [Blue-Green] because [reasons: zero-downtime, safety]
```

---

### ADR-7: [Another Important Decision]

If there's another critical decision not covered:
- Cache pattern (cache-aside, write-through, etc.)
- Database partitioning strategy
- Async job processing pattern
- API versioning strategy
- etc.

Follow same pattern: Status → Context → Decision → Consequences → Trade-offs

---

### ADRs Synthesis Pattern

```
"Great. Summarizing the architectural decisions:

ADR-1: Main Pattern [Monolith]
- Reason: [team size, timeline]

ADR-2: Database [PostgreSQL + Master-Slave]
- Reason: [structured data, complex queries]

ADR-3: Communication [REST + RabbitMQ for async]
- Reason: [low latency, decoupling]

ADR-4: Security [OAuth2 + PKCE]
- Reason: [industry standard, security]

ADR-5: Observability [ELK Stack]
- Reason: [open-source, control]

ADR-6: Deployment [Blue-Green]
- Reason: [zero-downtime, safety]

ADR-7: [Other decisions]

Is everything aligned?"
```

### Next Step
→ Block 4

---

## Block 4: Security Architecture Deep Dive (10 minutes)

### Objective

Detail security aspects beyond what was covered in ADR-4.

### Questions

**Question 39:** "Do sensitive data need field-level encryption?"

Response: yes/no. Which fields? (SSN, credit card, address)

**Question 40:** "Data residency requirement?"

Response: [none | specific country | multiple countries]

**Question 41:** "How to manage secrets? (vault, env vars, KMS)"

Response: recommend HashiCorp Vault or AWS KMS

**Question 42:** "Threat model? What are the main risks?"

Response: [unauthorized access, data breach, DDoS, insider threat]

**Synthesize:**
```
## Security Architecture

### Network Security
- VPC configuration: [public/private subnets]
- DDoS protection: [AWS Shield | Cloudflare]
- WAF rules: [OWASP Top 10]

### Data Protection
- Encryption in transit: TLS 1.3 + HSTS (NFR-11)
- Encryption at rest: AES-256 (NFR-12)
- Field-level encryption: [sensitive fields]
- Data masking: [PII in logs/exports]

### Access Control
- Authentication: OAuth2 + PKCE (ADR-4)
- Authorization: RBAC for roles
- Service-to-service: mTLS or API keys
- Secret management: Vault rotation policy

### Compliance
- Regulatory: GDPR | LGPD (NFR-13)
- Data residency: [country]
- Audit logging: [events audited]
- Incident response: [plan/team]

### Threat Model
- Assets: user data, payment info, system reputation
- Threats: [breach, DDoS, insider]
- Mitigations: [per threat]
```

### Next Step
→ Block 5

---

## Block 5: Observability Stack (5 minutes)

### Objective

Specify observability tools and configuration.

### Questions

**Question 43:** "Which logging platform did you choose?"

Response: (should be in ADR-5). If not → decide.

**Question 44:** "Centralized metrics? (Prometheus, CloudWatch, Datadog)"

Response: recommend Prometheus (open-source) or CloudWatch (managed)

**Question 45:** "Distributed tracing? (for microservices)"

Response: yes/no. If microservices → necessary. Options: Jaeger, Datadog, New Relic

**Question 46:** "Alerting platform? (PagerDuty, OpsGenie, Slack)"

Response: preference. Integration with on-call rotation?

**Synthesize:**
```
## Observability Stack

### Logging
- Platform: ELK Stack
- Retention: 30 days (NFR-15)
- Log levels: ERROR, WARN, INFO
- PII masking: Automatic

### Metrics
- Platform: Prometheus
- Collection: 15s interval
- Retention: 30 days
- Critical metrics: CPU, memory, error rate, latency

### Tracing (Distributed)
- Platform: [Jaeger | None] (if monolith)
- Sampling: 10% for cost optimization
- Instrumentation: Automatic (OpenTelemetry)

### Alerting
- Platform: PagerDuty
- Critical alerts: [error rate > 1%, latency > NFR-1 threshold]
- Escalation: 15 minutes
- On-call rotation: 24/7 (engineering team)

### Cost Estimate
- Logging: $[X]/month
- Metrics: $[Y]/month
- Total: $[Z]/month
```

### Next Step
→ Block 6

---

## Block 6: Infrastructure & DevOps + Validation (10 minutes)

### Objective

Detail infrastructure, DevOps, risks and validate complete document.

### Infrastructure & DevOps

**Question 47:** "How do you structure environments?"

Expected response: dev, staging, production. Configuration of each?

**Question 48:** "Infrastructure as Code? (Terraform, CloudFormation)"

Response: yes/no. If yes → which tool?

**Question 49:** "Auto-scaling policy? (for cloud)"

Response: min/max replicas, metrics trigger (CPU%, latency)

**Synthesize:**
```
## Infrastructure & DevOps

### Environments
- Development: Docker Compose local
- Staging: Exact production copy (for testing)
- Production: Multi-region failover

### Infrastructure as Code
- Tool: Terraform
- Version control: Git
- Drift detection: Automated

### Deployment Pipeline
- Stages: Build (2 min) → Test (5 min) → Stage Deploy (3 min) → Approval → Prod Deploy (5 min)
- Total deployment time: ~15 minutes
- Rollback: Blue-Green (instant)

### Scaling
- Horizontal: Auto-scale 2-10 instances based on CPU > 70%
- Vertical: [manual, only if needed]
- Database: Read replicas up to 3, sharding if > 1TB

### Monitoring
- Health checks: Every 30 seconds
- Incident response: PagerDuty alert → on-call response in 5 min
- Maintenance windows: Tuesday 2-4 AM UTC
```

---

### Technical Constraints & Risks

**Question 50:** "What are the main technical risks?"

Expected response: list of 3-5 risks

**Question 51:** "How to mitigate each one?"

Expected response: mitigation strategy

**Synthesize:**
```
## Technical Constraints

| Constraint | Impact |
|---|---|
| Budget: $10K/month | Limits cloud spend, prioritizes cost optimization |
| Compliance: GDPR | Data residency in EU, audit logging |
| Team: 5 backend devs | Monolith better than microservices |

## Technical Risks & Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Database becomes bottleneck at 100K users | High | Read replicas + caching layer |
| Security breach leaks PII | Critical | Encryption + access control + audit logging |
| Cloud costs exceed budget | Medium | Monitoring + auto-scaling tuning |
| Key person leaves | Medium | Documentation + knowledge sharing |
```

---

### Final Validation

**Question 52:** "Shall we review everything together?"

Present:
```
"Summarizing the complete Tech Spec:

NFRs: 13 non-functional requirements quantified
- Performance: latency ≤ [ms], throughput ≥ [RPS]
- Scalability: [N] users, growth [%/month]
- Reliability: uptime ≥ [%], RTO ≤ [time]
- Security: TLS 1.3, encryption at rest, [compliance]
- Observability: ELK, Prometheus, tracing
- Maintainability: code coverage ≥ [%], deploy [X/day]

ADRs: 6 architectural decisions documented
- ADR-1: [Pattern]
- ADR-2: [Database]
- ADR-3: [Communication]
- ADR-4: [Security]
- ADR-5: [Observability]
- ADR-6: [Deployment]

Security Architecture: [detailed]
Observability Stack: [defined]
Infrastructure & DevOps: [planned]
Risks & Mitigations: [identified]

Is it complete and correct?"
```

---

## Expected Timeline

| Block                          | Time | Activity                |
|--------------------------------|------|-------------------------|
| 1. Preparation & Context       | 5 min | Reading + confirmation  |
| 2. Non-Functional Requirements | 30 min| 6 categories, 13+ NFRs  |
| 3. Architecture Decision Records| 20 min| 6-7 ADRs                |
| 4. Security Architecture       | 10 min| Network, data, access   |
| 5. Observability Stack         | 5 min | Logging, metrics, tracing|
| 6. Infra/DevOps + Validation   | 10 min| Risks, checklist        |
|                                |       |                          |
| **Total**                      | **80 min** | **Complete Tech Spec** |

---

## Checklist for the Skill

Before marking as ready:
- [ ] Block 1: Architecture and context confirmed?
- [ ] Block 2: 10-15 NFRs quantified (6 categories)?
- [ ] Block 3: 6-7 ADRs documented with trade-offs?
- [ ] Block 4: Security architecture detailed?
- [ ] Block 5: Observability stack defined?
- [ ] Block 6: Infrastructure planned, risks identified?
- [ ] Document generated in English markdown?
- [ ] IDs (NFR-#, ADR-#) registered in ids.yml?
- [ ] User approved output?

---

**Version:** 1.0
**Language:** English (en-US)
**Model:** Interview-driven NFR + ADR Architecture Decisions
