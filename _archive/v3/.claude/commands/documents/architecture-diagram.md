---
description: Generate Architecture Diagram using C4 Model
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Architecture Diagram

Creating architecture diagram for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/planning/user-stories.md && echo "✓ user-stories.md exists" || echo "⚠ Missing User Stories (recommended)"`
!`test -f docs/planning/feature-specs && echo "✓ feature-specs/ exists (optional)" || echo "ℹ feature-specs/ not found (optional)"`

## Setup

!`mkdir -p docs/design && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/architecture-chain/knowledge/architecture-diagram.md

## Interactive Architecture Design

I'll help you create C4 model architecture diagrams:

### Step 1: Context (Level 1) - System Boundary

**Ask the user:**

1. What is the system name and primary purpose?
2. Who are the external users/actors? (personas, systems)
3. What external systems does it interact with? (APIs, databases, services)
4. What are the key interactions at the system boundary?

[Create Level 1: Context diagram showing system + external actors + external systems]

### Step 2: Container (Level 2) - Major Components

**Ask the user:**

1. What are the major runtime containers? (web app, mobile app, API, databases, message queues)
2. What technology stack for each container? (React, Node.js, PostgreSQL, Redis, etc.)
3. How do containers communicate? (REST, GraphQL, WebSocket, message queue)
4. What data stores exist and what do they hold?

[Create Level 2: Container diagram showing internal architecture]

### Step 3: Component (Level 3) - Internal Structure

**For key containers, ask:**

1. What are the major components within this container?
2. What responsibilities does each component have?
3. How do components interact?
4. What design patterns are used? (MVC, layered, microservices, event-driven)

[Create Level 3: Component diagram for critical containers]

### Step 4: Architecture Patterns

**Ask the user about architecture decisions:**

#### Deployment Architecture
1. Hosting platform? (Cloud provider, on-prem, hybrid)
2. Infrastructure pattern? (Serverless, containers, VMs)
3. Load balancing strategy?
4. CDN requirements?

#### Data Architecture
1. Database choice and why? (SQL vs NoSQL, specific DB)
2. Data partitioning strategy?
3. Caching strategy? (Redis, CDN, in-memory)
4. Data replication approach?

#### Integration Patterns
1. API style? (REST, GraphQL, gRPC)
2. Authentication/authorization pattern?
3. Service-to-service communication?
4. Event-driven architecture?

#### Security Architecture
1. Network security? (VPC, firewall rules, WAF)
2. Encryption strategy? (TLS, at-rest encryption)
3. Secrets management?
4. Identity and access management?

#### Scalability Patterns
1. Horizontal vs vertical scaling?
2. Auto-scaling triggers?
3. Database scaling approach?
4. Stateless design considerations?

### Step 5: Diagram Confirmation

"Here's the architecture I've designed:

**Level 1 (Context):**
- System: [name]
- External actors: [list]
- External systems: [list]

**Level 2 (Container):**
- Web App (React) → API Gateway
- API (Node.js/Express) → PostgreSQL, Redis
- Background Workers → Message Queue
- [etc.]

**Architecture Patterns:**
- Deployment: [approach]
- Data: [strategy]
- Security: [design]
- Scalability: [pattern]

Does this architecture address your requirements and user stories?"

[Wait for confirmation and iterate if needed]

## Generate Document

Generate `docs/design/architecture-diagram.md` using C4 model and Mermaid diagrams.

**Document Structure:**
- Executive Summary
- C4 Level 1: Context Diagram (Mermaid)
  - System boundary
  - External actors
  - External systems
  - Key interactions
- C4 Level 2: Container Diagram (Mermaid)
  - Internal containers
  - Technology choices
  - Container interactions
  - Data flows
- C4 Level 3: Component Diagrams (Mermaid)
  - Component breakdown for key containers
  - Responsibilities
  - Design patterns
- C4 Level 4: Code (Optional)
  - For complex algorithms or critical paths
- Architecture Patterns:
  - Deployment architecture
  - Data architecture
  - Integration patterns
  - Security architecture
  - Scalability patterns

## Validation

After generation:

!`test -f docs/design/architecture-diagram.md && echo "✓ architecture-diagram.md created" || echo "✗ Generation failed"`

**Architecture checklist**:
!`if [ -f docs/design/architecture-diagram.md ]; then
  grep -ci "mermaid\|diagram" docs/design/architecture-diagram.md | xargs echo "Diagrams included:"
  grep -ci "container\|component" docs/design/architecture-diagram.md | xargs echo "C4 levels covered:"
fi`

## Next Steps

**Create technical specification**:
```
/tech-spec
```

Or validate Planning gate:
```
/validate-gate planning
```

---

**Architecture diagram generated!** System structure documented with C4 model and Mermaid diagrams.
