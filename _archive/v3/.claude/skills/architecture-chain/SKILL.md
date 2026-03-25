---
name: architecture-chain
description: Generate technical architecture documents (SRS with NFRs, architecture diagrams, technical specifications) using 5W2H for systematic NFR definition and How Might We for constraint-to-opportunity transformation. Use when defining system architecture, non-functional requirements, or technical implementation strategy for solo developers.
---

# Architecture Chain

Generate technical architecture documentation from non-functional requirements through implementation tactics using systematic 5W2H analysis.

## Purpose

This skill guides solo developers through the Develop phase technical foundation by generating:

1. **Software Requirements Spec** (srs) - NFRs with quantified targets
2. **Architecture Diagram** (arch) - C4 models and system design
3. **Technical Spec** (tech) - ADRs, tactics, and validation plans

Each document maintains traceability with lowercase IDs (nfr-#, arch components, adr-#), forming the technical backbone for all implementation work.

## Interactive Architecture Workflow

**This skill is conversation-driven for architectural decisions.**

Architecture requires balancing competing concerns (performance vs cost, scalability vs simplicity, security vs usability). This skill:
1. **Discusses NFR targets** collaboratively before defining requirements
2. **Validates trade-offs** together (not dictating architecture)
3. **Presents architecture options** with pros/cons (monolith vs microservices, SQL vs NoSQL, REST vs GraphQL)
4. **Reviews ADRs** to ensure rationale is clear and alternatives were considered
5. **Confirms technical feasibility** before proceeding to implementation

**Key Principle:** Architecture emerges from constraints, priorities, and trade-offs - all of which must be discussed with the user.

**Do NOT:**
- Generate NFRs based on generic benchmarks without understanding actual requirements
- Choose architecture patterns without discussing trade-offs
- Define performance targets without asking about user expectations
- Select technologies without understanding team capabilities
- Proceed with ADRs without validating alternatives were considered

**Success Criteria:** User understands architectural trade-offs and feels confident in technical decisions.

## When to Use This Skill

Use this skill when:
- Need to define non-functional requirements (performance, security, scalability)
- Designing system architecture for new product or major feature
- Making critical technical decisions that need documentation
- Transitioning from Define gate to Develop phase
- Establishing technical foundation before parallel workstreams

Do NOT use for:
- Functional requirements (use feature-development-chain skill instead)
- UX design (use ux-chain skill instead)
- Data modeling (use data-chain skill instead)
- API specifications (use api-backend skill instead)

**Dependencies:** Requires `user-stories` (docs/planning/user-stories.md) and `feature-specs` (docs/planning/feature-specs/*.md) from feature-development-chain as input.

## Methodology Integration

### 5W2H for NFR Systematic Definition

Apply rigorous questioning to define measurable, testable non-functional requirements:

**WHAT:**
- What quality attributes matter most?
- What performance characteristics are required?
- What security standards must be met?

**WHO:**
- Who is responsible for each NFR?
- Who verifies NFR compliance?
- Who is impacted by NFR failures?

**WHERE:**
- Where in the system do NFRs apply?
- Where are performance bottlenecks likely?
- Where are security boundaries?

**WHEN:**
- When must performance targets be met?
- When should scalability kick in?
- When do we verify NFRs (CI/CD stage)?

**WHY:**
- Why this performance target vs higher/lower?
- Why this security approach vs alternatives?
- Why this availability SLA?

**HOW:**
- How will we achieve this NFR?
- How will we measure/verify it?
- How will we monitor it in production?

**HOW MUCH:**
- How much load must system handle?
- How much downtime is acceptable?
- How much will it cost to achieve?

### How Might We for Technical Constraints

Transform technical constraints into architecture opportunities:

**Example Transformations:**

```
Constraint: Must handle 10k concurrent users with limited budget
↓
HMW: How might we achieve high scalability within budget constraints?
↓
Opportunity: Leverage serverless architecture for auto-scaling, pay-per-use pricing
```

```
Constraint: Legacy database schema can't change
↓
HMW: How might we work with existing schema while enabling new features?
↓
Opportunity: Implement CQRS pattern with read models optimized for new queries
```

```
Constraint: 99.9% uptime required but team is small
↓
HMW: How might we achieve high availability with minimal operational overhead?
↓
Opportunity: Use managed services (RDS, Kubernetes) to reduce operational burden
```

### Double Diamond Mapping

Architecture chain implements the DEVELOP phase convergence:

```
DISCOVER/DEFINE    →    DEVELOP (Converge)    →    DELIVER
      ↓                       ↓                      ↓
    prd/frd            srs/arch/tech          be/fe/data
```

After defining functional requirements, converge on technical approach before diverging into parallel implementation workstreams.

## How to Use This Skill

### Step 1: Technical Specification (tech) - **INTERACTIVE NFR DISCUSSION**

**BEFORE generating tech spec**, conduct NFR target discussion with user (NFR content will be integrated into tech-spec.md):

```
"Let's define your non-functional requirements together. I'll ask about quality attributes that matter for your product:

**Performance Expectations:**
1. What response time do users expect?
   - What feels 'instant' vs 'slow' for your users?
   - Current baseline? (if existing system)
   - Acceptable target? (be specific: P95? P99?)

2. What load must the system handle?
   - How many concurrent users at launch?
   - Growth projection? (6 months? 1 year?)
   - Peak vs average load?

**Scalability Priorities:**
3. How fast do you expect to grow?
   - 2x? 10x? 100x in next 12 months?
   - What triggers scale? (users, data, transactions)
   - Budget constraints for infrastructure?

**Security Requirements:**
4. What security standards must you meet?
   - Industry compliance? (HIPAA, SOC2, GDPR)
   - Data sensitivity level? (PII, financial, public)
   - Authentication needs? (SSO, MFA, OAuth)

**Availability/Reliability:**
5. How much downtime is acceptable?
   - 99.9% (43min/month)? 99.99% (4min/month)?
   - What's cost of downtime? (revenue loss, reputation)
   - Disaster recovery needs? (RPO? RTO?)

**Maintainability:**
6. What's your team's capability?
   - Team size and seniority?
   - Tech stack familiarity?
   - Operational maturity? (Can run Kubernetes? Or need managed services?)"
```

[Wait for user's answers. Probe for quantification when vague.]

**FOLLOW-UP PROBES:**

If user says "fast response time":
```
"How fast exactly? 100ms? 500ms? 2 seconds? What does 'fast' mean for your users in this context?"
```

If user says "needs to scale":
```
"Scale to what level? 10K users? 1M users? What timeline? What's driving this growth?"
```

If user says "must be secure":
```
"What specific threats concern you? What compliance standards apply? What's the impact of a breach?"
```

**STEP 2: Validate NFR Priorities**

After gathering requirements, confirm priorities:

```
"Let me confirm what I've understood about your NFR priorities:

**Performance:** [Restate target] - Is this the right threshold?
**Scalability:** [Restate growth] - Does this match your projections?
**Security:** [Restate standards] - Are these the critical safeguards?
**Availability:** [Restate uptime] - Is this SLA acceptable to your users?
**Team Capability:** [Restate constraints] - Are these the right assumptions about what you can operate?

If you had to rank these, which is MOST critical? Which could you compromise on if needed?"
```

[Wait for confirmation. This informs P0 vs P1 vs P2 NFR prioritization.]

**STEP 3: Discuss NFR Trade-offs**

For conflicting requirements, use HMW to explore solutions:

```
"I see a tension between [Requirement A] and [Requirement B]:
- Achieving [A] typically requires [approach/cost]
- But [B] constrains us to [limitation]

How might we balance these? Let's explore options:

Option 1: [Approach favoring A]
- Pros: [...]
- Cons: [...]
- Cost/Complexity: [...]

Option 2: [Approach favoring B]
- Pros: [...]
- Cons: [...]
- Cost/Complexity: [...]

Option 3: [Compromise approach]
- Pros: [...]
- Cons: [...]
- Cost/Complexity: [...]

Which trade-off makes most sense for your context?"
```

[Document user's decision and rationale for NFR specifications.]

**STEP 4: Generate Tech Spec Document**

Only after confirming NFR targets and priorities, generate the tech spec with NFR definitions using validated requirements.

---

**Now define ALL non-functional requirements using 5W2H systematic analysis:**

#### NFR Categories

**Performance:**
```
Apply 5W2H:
WHAT: Response time, throughput, resource usage
HOW MUCH: API < 200ms p95, DB queries < 50ms p99
WHEN: Under normal load (1000 concurrent users)
HOW: Measure via APM tools (Datadog, New Relic)
WHO: Backend team owns, QA verifies
WHY: User research shows 200ms = "instant"
WHERE: All API endpoints except batch operations
```

**Scalability:**
```
WHAT: System must scale horizontally
HOW MUCH: Support 10k → 100k users within 6 months
WHEN: Auto-scale at 70% CPU utilization
HOW: Stateless services, database read replicas
WHO: DevOps owns, monitored via CloudWatch
WHY: Growth projections show 10x in year 1
HOW MUCH (cost): Budget allows 3x current infrastructure
```

**Security:**
```
WHAT: Data encryption, authentication, authorization
HOW: AES-256 at rest, TLS 1.3 in transit, OAuth 2.0
WHEN: All environments including dev
WHO: Security team owns, audit quarterly
WHY: GDPR compliance + customer trust
WHERE: All personally identifiable information (PII)
HOW MUCH: Zero tolerance for data breaches
```

**Reliability:**
```
WHAT: Availability, fault tolerance, disaster recovery
HOW MUCH: 99.9% uptime (43min downtime/month)
HOW: Multi-AZ deployment, automated failover
WHEN: Measured monthly, reported quarterly
WHO: SRE team owns, CTO accountable
WHY: SLA commitments to enterprise customers
WHERE: Production environment only
```

**Maintainability:**
```
WHAT: Code quality, testability, documentation
HOW MUCH: 80% test coverage, all public APIs documented
HOW: Automated linting, test gates in CI/CD
WHEN: Every PR must pass quality gates
WHO: Engineering team collective ownership
WHY: Enable fast iteration, reduce technical debt
WHERE: All repositories, all languages
```

**Usability:**
```
WHAT: Accessibility, internationalization, user experience
HOW: WCAG 2.1 AA compliance, support 10 languages
WHEN: All new features, existing features by Q2 2026
WHO: Frontend team + accessibility specialist
WHY: Expand market reach, legal compliance
WHERE: All user-facing interfaces
HOW MUCH: Budget for translation service, a11y audits
```

#### NFR Structure (CRITICAL)

Every NFR must include:

```
NFR-#: [NFR ID for traceability]
Category: [Performance|Scalability|Security|Reliability|Maintainability|Usability]
Requirement: [Clear, measurable statement]
Target Value: [Quantified target with units]
Verification Method: [How to test/validate]
Owner: [Person/team responsible]
Acceptance Threshold: [Pass/fail criteria]
Priority: [P0|P1|P2 based on impact]
Rationale: [Why this target was chosen - 5W2H evidence]
```

**Example:**
```
NFR-1: API Response Time
Category: Performance
Requirement: All API endpoints must respond within acceptable latency
Target Value: P95 < 200ms, P99 < 500ms under normal load
Verification Method: Load testing with k6, APM monitoring in production
Owner: Backend team (John Smith)
Acceptance Threshold: P95 < 200ms for 3 consecutive days
Priority: P0 (user-facing, impacts NPS)
Rationale: User research shows 200ms feels "instant", 500ms feels "acceptable",
           >1000ms causes frustration. Competitor benchmarks show 180-250ms average.
```

**Apply HMW to NFR Trade-offs:**
```
Challenge: Achieving <200ms requires expensive caching infrastructure
↓
HMW: How might we achieve target performance within infrastructure budget?
↓
Solutions Explored:
- Edge caching for static content (99% hit rate = big win)
- Database query optimization (50ms → 20ms = free improvement)
- Async processing for non-critical operations (defer work)
Result: Multi-layered approach achieves target at 60% of initial cost estimate
```

**Template Reference:** See `knowledge/tech-spec.md` for complete NFR and tech spec framework

### Step 2: Architecture Diagram (arch) - **INTERACTIVE ARCHITECTURE TRADE-OFFS**

**BEFORE generating architecture diagram**, discuss architectural decisions collaboratively:

```
"Now let's design your system architecture. I'll present options for key architectural decisions:

**Architecture Style:**
Based on your requirements [reference NFRs from Step 1], which architecture makes most sense?

Option A: **Monolith** (single deployable unit)
- Best when: Small team, early stage, rapid iteration, uncertain requirements
- Pros: Simple to develop/deploy/debug, easy to refactor, lower operational overhead
- Cons: Harder to scale different components independently, team can bottleneck
- Cost: Low (single server, simple CI/CD)

Option B: **Modular Monolith** (organized internally but single deploy)
- Best when: Want clear boundaries without operational complexity
- Pros: Clear separation of concerns, can extract services later, easier than microservices
- Cons: Still shares database, single deployment unit
- Cost: Low (same as monolith)

Option C: **Microservices** (multiple independent services)
- Best when: Multiple teams, clear bounded contexts, need independent scaling
- Pros: Team independence, scale components separately, technology flexibility
- Cons: High operational complexity, distributed system challenges, costly
- Cost: High (orchestration, service mesh, monitoring, many deployments)

What fits your team size, product maturity, and operational capability?
```

[Wait for user's decision. Probe reasoning.]

**FOLLOW-UP: Database Architecture**

```
"For your data layer, which approach fits your access patterns?

Option A: **Single Database** (shared by all components)
- Best when: Simple data model, ACID transactions critical, small scale
- Pros: Easy consistency, simple queries, familiar patterns
- Cons: Scaling bottleneck, schema changes impact everything
- Fits: [NFR-#] for transactional consistency

Option B: **Database per Service** (if microservices)
- Best when: Clear bounded contexts, eventual consistency acceptable
- Pros: Independent scaling, service autonomy, technology choice flexibility
- Cons: Complex cross-service queries, distributed transactions, data duplication
- Fits: [NFR-#] for service independence

Option C: **CQRS** (separate read/write models)
- Best when: Read-heavy, complex queries, high scalability needs
- Pros: Optimize reads independently, scalable, flexible read models
- Cons: Eventual consistency, complexity, learning curve
- Fits: [NFR-#] for query performance

Which matches your consistency needs and operational maturity?"
```

[Record user's choice and rationale for ADR.]

**FOLLOW-UP: Integration Patterns**

```
"How should components communicate?

Option A: **Synchronous (REST/GraphQL/gRPC)**
- Best when: Immediate response needed, simple flows, request/reply pattern
- Pros: Easy to reason about, simpler debugging, familiar pattern
- Cons: Tight coupling, cascading failures, slower under load
- Technology Choice:
  - REST: Standard, well-understood, works everywhere
  - GraphQL: Flexible client queries, reduces over-fetching
  - gRPC: High performance, type-safe, streaming support

Option B: **Asynchronous (Message Queue/Event Bus)**
- Best when: Decoupling needed, eventual consistency acceptable, high throughput
- Pros: Loose coupling, better fault tolerance, scalable
- Cons: Harder to debug, eventual consistency, message ordering complexity
- Technology Choice:
  - SQS/RabbitMQ: Queue pattern, guaranteed delivery
  - Kafka/Kinesis: Event streaming, replay capability

Option C: **Hybrid** (sync for user-facing, async for background)
- Best when: Different patterns for different use cases
- Pros: Right tool for each job, balanced approach
- Cons: More complexity, multiple integration patterns to maintain

Which fits your latency requirements and team expertise?"
```

[Wait for decision. This informs Container diagram.]

**STEP 2: Validate Architecture Against NFRs**

```
"Let me confirm this architecture supports your NFRs:

**Architecture Choice:** [Selected: Monolith/Modular/Microservices]
**Database Strategy:** [Selected: Single/Per-Service/CQRS]
**Integration Pattern:** [Selected: Sync/Async/Hybrid]

Checking against your NFRs:
- NFR-1 (Performance [target]): This architecture achieves it by [approach] ✓
- NFR-2 (Scalability [target]): We can scale [component] independently ✓
- NFR-3 (Security [standard]): [Security boundaries/approach] ✓
- NFR-4 (Availability [SLA]): [Redundancy/failover approach] ✓

Are there any NFRs this architecture doesn't adequately support?
What concerns do you have about this design?"
```

[Iterate if gaps identified. Only proceed after validation.]

**STEP 3: Generate C4 Architecture Diagram**

Only after architecture decisions are validated, generate C4 diagrams.

---

**Now document system design using C4 model:**

#### Level 1: Context Diagram
```
System boundary and external dependencies
- What systems/users interact with our system?
- What are the integration points?
- What protocols are used?
```

#### Level 2: Container Diagram
```
Major components and technology choices
- What containers exist? (web app, API, database, cache, queue)
- How do containers communicate?
- What technologies power each container?
```

#### Level 3: Component Diagram
```
Internal structure of key containers
- What components exist within critical containers?
- What are component responsibilities?
- What are component dependencies?
```

#### Level 4: Code Diagram (Optional)
```
Class-level detail for complex components
- Only for architecturally significant areas
- Focus on patterns (factory, strategy, repository)
```

**Apply 5W2H to Architecture Decisions:**
```
WHAT: Microservices vs monolith?
WHY: Microservices chosen for team independence, but adds complexity
HOW: Kubernetes for orchestration, service mesh for communication
HOW MUCH: 5 services to start, budget allows 10 max
WHEN: Monolith first (6mo), break into services after PMF
WHERE: Split at bounded contexts (auth, billing, core product)
WHO: Platform team owns infrastructure, product teams own services
```

**Create HMW for Architecture Constraints:**
```
Constraint: Microservices increase operational complexity
↓
HMW: How might we get microservice benefits with reduced operational overhead?
↓
Solution: Managed Kubernetes (EKS), service mesh (Istio), observability platform (Datadog)
```

**Key Architecture Patterns to Document:**
- Deployment architecture (multi-region, multi-AZ, single-region)
- Data architecture (CQRS, event sourcing, traditional CRUD)
- Integration patterns (sync vs async, REST vs GraphQL vs gRPC)
- Security architecture (zero-trust, defense in depth, principle of least privilege)
- Scalability patterns (horizontal scaling, caching layers, CDN)

**Template Reference:** See `knowledge/architecture-diagram.md` for C4 modeling

### Step 3: Technical Spec (tech)

Document implementation approach with ADRs and tactics:

#### Architecture Decision Records (ADRs)

For every significant technical decision:

```
ADR-#: [Decision Title]
Status: [Proposed|Accepted|Deprecated|Superseded]
Context: What is the issue we're trying to solve? (5W2H context)
Decision: What is the change we're proposing?
Consequences: What becomes easier/harder after this change?
Alternatives Considered: What else did we evaluate?
```

**Example ADR with 5W2H:**
```
ADR-1: Use PostgreSQL for Primary Database

Status: Accepted

Context (5W2H):
WHAT: Need to choose primary database technology
WHY: Product requires complex queries, ACID transactions, JSON flexibility
WHO: Backend team will maintain, DBA will optimize
WHERE: All transactional data, read-heavy workloads
WHEN: Decision needed before schema design (blocking data-chain)
HOW: Evaluated based on query performance, operational maturity, team expertise
HOW MUCH: Budget allows managed service (RDS), not custom infrastructure

Decision:
Choose PostgreSQL (via AWS RDS) as primary database

Consequences:
+ Strong ACID guarantees
+ Rich query capabilities (joins, subqueries, CTEs)
+ JSON support for semi-structured data
+ Mature tooling and monitoring
+ Team has 5 years PostgreSQL experience
- Scaling writes requires sharding (future complexity)
- Managed service costs more than self-hosted
- Vendor lock-in to AWS ecosystem

Alternatives Considered:
- MongoDB: Better for write-heavy, but team unfamiliar, weaker transactions
- MySQL: Familiar but weaker JSON support, community edition limitations
- DynamoDB: Excellent scale but limited query flexibility, higher learning curve
```

#### NFR Implementation Tactics

For each NFR from SRS, document HOW it will be achieved:

```
NFR-1 (API Response Time < 200ms) Implementation Tactics:

Tactic 1: Multi-layer Caching
- Redis for session data (sub-ms lookup)
- CDN for static assets (edge caching)
- Application-level caching (frequently accessed entities)
Owner: Backend team
Timeline: Week 1-2 of implementation

Tactic 2: Database Query Optimization
- Index all foreign keys
- Use connection pooling (pgBouncer)
- Implement read replicas for reporting queries
Owner: DBA
Timeline: Week 2-3

Tactic 3: Async Processing
- Move non-critical work to background jobs
- Use message queue (SQS) for email, notifications
- Immediate response to user, process asynchronously
Owner: Backend team
Timeline: Week 3-4

Verification:
- Load test with k6 (10k requests, 100 concurrent users)
- P95 must be < 200ms for all API endpoints
- Automated test runs nightly in staging
- Production APM monitors continuously
```

**Apply HMW to Implementation Challenges:**
```
Challenge: Caching strategy adds complexity
↓
HMW: How might we implement caching that's easy to reason about and debug?
↓
Solution:
- Cache-aside pattern (simple, well-understood)
- Short TTLs initially (5min), tune based on data
- Cache invalidation via events (clear on update)
- Monitoring shows cache hit rate, makes issues visible
```

**Validation Plan:**
- How will each NFR be tested?
- What tools/frameworks?
- When in development cycle?
- Pass/fail criteria?

**Deployment Strategy:**
- Blue/green deployment for zero downtime
- Feature flags for gradual rollout
- Automated rollback triggers
- Monitoring and alerting setup

**Runbooks:**
- Common failure scenarios
- Debugging procedures
- Recovery steps
- Escalation paths

**Template Reference:** See `knowledge/tech-spec.md` for complete technical specification

## Workflow Sequence

```
1. tech (Technical Spec) — includes NFR definitions
   → Use 5W2H to systematically define all NFRs
   → Each NFR-# has target, verification, owner, threshold
   → Apply HMW to trade-offs and constraints
   ↓

2. arch (Architecture Diagram)
   → C4 model (Context → Container → Component → Code)
   → Document architecture decisions with rationale
   → Create HMW for architecture challenges
   → Validate architecture supports all NFR-# requirements
   ↓

   (Both documents generated together in architecture-chain)
   ↓

✅ DEVELOP GATE (Technical foundation ready for parallel workstreams)
```

## Gate Validation

### Develop Gate Criteria

Before proceeding to parallel implementation workstreams, validate:

- [ ] Every NFR has: target value, verification method, owner, acceptance threshold
- [ ] NFRs cover all categories: performance, scalability, security, reliability, maintainability, usability
- [ ] 5W2H analysis documented for key NFRs (shows rigorous thinking)
- [ ] Architecture diagram has all C4 levels (Context, Container, Component minimum)
- [ ] Architecture supports all NFR-# requirements (no conflicts)
- [ ] ADRs document major decisions with alternatives considered
- [ ] Implementation tactics defined for each P0 NFR
- [ ] Validation plan exists for testing NFRs
- [ ] No architectural debt in critical path (documented if exists elsewhere)
- [ ] HMW statements show constraint-to-opportunity transformations

**Decision:** GO (start parallel workstreams) | REDESIGN (architecture inadequate) | ITERATE (refine NFRs/tactics)

## Output Format

Generate each document in sequence, ensuring:

1. **NFR IDs:** Use nfr-# format for traceability
2. **Quantified Targets:** Every NFR has measurable target with units
3. **5W2H Evidence:** Show systematic analysis in NFR rationale
4. **HMW Transformations:** Document constraint-to-opportunity thinking
5. **ADR Format:** Consistent structure for all decisions
6. **C4 Completeness:** All required diagram levels present
7. **Tactics Linked:** Each NFR-# has corresponding implementation tactics in tech spec

## Quality Checks

After generation, validate:

- **Measurability:** Can every NFR be objectively tested?
- **Ownership:** Does every NFR have a responsible owner?
- **Feasibility:** Do tactics realistically achieve targets?
- **Completeness:** Are all quality attributes covered?
- **Traceability:** Can trace from user stories (US-#) and feature specs (FS-[name]-#) to NFRs to architecture
- **Methodology:** 5W2H and HMW evidence visible in documents

## Knowledge Base

This skill references template files in `knowledge/` directory:

**Core Templates (2 documents):**
- `architecture-diagram.md` - C4 modeling approach
- `tech-spec.md` - Technical specification with NFRs, ADRs, and tactics

**Supporting Resources:**
- `architect-checklist.md` - Architecture review checklist

## Best Practices

1. **Ask Before Generating:** Never assume NFR targets - always discuss with user first
2. **Quantify Everything:** Vague NFRs are untestable (press for numbers with units)
3. **Present Options:** Don't dictate architecture - show trade-offs and let user decide
4. **Document Rationale:** Capture WHY decisions were made (for future reference)
5. **Validate Trade-offs:** Every architecture choice has consequences - discuss them
6. **Confirm Understanding:** Validate NFRs and architecture against user's intent before proceeding
7. **HMW for Constraints:** Transform limitations into creative opportunities collaboratively
8. **Owner Accountability:** Every NFR needs someone responsible (discuss ownership)
9. **Interactive ADRs:** Review alternatives with user, don't assume best choice
10. **Automate Verification:** NFRs should be tested in CI/CD, not manually
11. **Monitor Production:** Architecture assumptions should be validated with real data
12. **Conversation Over Assumptions:** If uncertain about requirements, ask - don't guess

## Common Pitfalls to Avoid

- ❌ Vague NFRs ("system should be fast" → NFR-#: P95 < 200ms)
- ❌ Missing verification method (how will you test it?)
- ❌ No ownership (who is responsible for this NFR?)
- ❌ Skipping 5W2H (leads to incomplete NFR analysis)
- ❌ Architecture doesn't support NFRs (disconnect between SRS and arch)
- ❌ Missing ADR rationale (future team won't understand decisions)
- ❌ No HMW for constraints (missed creative opportunities)
- ❌ Premature optimization (architecting for scale you don't need yet)
- ❌ Resume-driven architecture (choosing tech for learning, not requirements)

## Next Steps After This Skill

After Develop gate passes, launch parallel workstreams:

1. **Data Chain:** Generate data → erd → database-spec → data-dictionary → flow → cat (uses NFRs from tech)
2. **UX Chain:** Generate user-journey → ux-sitemap → wireframes → style-guide (uses NFRs for performance/a11y)
3. **API Backend:** Generate be (uses architecture patterns from arch)

Architecture chain outputs (especially tech and arch) inform all downstream technical work.
