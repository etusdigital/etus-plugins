---
description: Generate Data Flow Diagram showing data sources, transformations, and flows
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Data Flow Diagram

Creating data flow diagram for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/design/data-dictionary.md && echo "✓ data-dictionary.md exists" || echo "⚠ Missing data dictionary"`

## Setup

!`mkdir -p docs/data && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/data-chain/knowledge/data-flow-diagram.md

## Interactive Data Flow Design

I'll help you map data flows:

### Step 1: Review Data Dictionary

Read field and event definitions:

@docs/design/data-dictionary.md

### Step 2: Data Sources

**Ask about external data sources:**

1. **User input sources**:
   - Web forms
   - Mobile apps
   - API clients
2. **External system sources**:
   - Payment gateways (Stripe, PayPal)
   - Email providers (SendGrid, Mailgun)
   - Analytics platforms (Google Analytics, Mixpanel)
   - Third-party APIs
3. **Internal sources**:
   - Background jobs
   - Scheduled tasks
   - Administrative tools

[List all data entry points]

### Step 3: Data Transformations

**Ask about data processing:**

1. **Where does data get transformed?**
   - Input validation
   - Business logic layer
   - Database triggers
   - Background workers
   - ETL pipelines
2. **What transformations occur?**
   - Format conversions
   - Calculations
   - Aggregations
   - Enrichment (adding context)
   - Normalization

**Example flows:**
- User submits order → Validate items → Calculate total → Reserve inventory → Create order record → Emit ev.order.created
- Payment webhook → Verify signature → Update order status → Emit ev.order.paid → Trigger fulfillment

[Document transformation steps]

### Step 4: Data Sinks (Outputs)

**Ask about where data flows to:**

1. **Storage destinations**:
   - Primary database
   - Cache (Redis)
   - Object storage (S3)
   - Search index (Elasticsearch)
2. **External systems**:
   - Email service
   - SMS provider
   - Analytics platforms
   - Data warehouse
3. **Event streams**:
   - Message queue
   - Event bus
   - Webhooks to clients

[List all data exit points]

### Step 5: Event Flows

**Ask about event-driven flows:**

Using ev.* definitions from data dictionary:

**For each event:**
1. **Event source**: What triggers this event?
2. **Event propagation**: How does event travel? (direct call, queue, pub/sub)
3. **Event consumers**: Who processes this event?
4. **Downstream events**: Does this event trigger other events?

**Example:**
```
ev.order.created
  ↓ (via message queue)
  → Email Service → Sends confirmation email
  → Analytics Service → Tracks conversion
  → Inventory Service → Reserves stock
    ↓
    ev.inventory.reserved
      ↓
      → Fulfillment Service
```

### Step 6: Batch vs Real-time

**Ask about processing patterns:**

1. **Real-time flows**: Data processed immediately
   - User actions (orders, updates)
   - Payment processing
   - Notifications
2. **Near real-time flows**: Processed within minutes
   - Analytics ingestion
   - Search index updates
3. **Batch flows**: Processed on schedule
   - Daily reports
   - Data exports
   - Cleanup jobs
   - Backups

### Step 7: Confirm Data Flows

"Here are the data flows:

**Sources:**
- User web app → API → Database
- Payment webhook → Payment processor → Database
- Admin tool → API → Database

**Transformations:**
- Order validation (API layer)
- Total calculation (business logic)
- Email formatting (email service)

**Sinks:**
- PostgreSQL (primary storage)
- Redis (cache)
- S3 (file uploads)
- SendGrid (emails)

**Event Flows:**
1. User creates order
   → ev.order.created
   → [Email, Analytics, Inventory]
2. Payment confirmed
   → ev.order.paid
   → [Fulfillment, Notification]

Does this capture all data flows?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/data-flow-diagram.md` with Mermaid flow diagrams.

**Document Structure:**
- Data Sources (External and Internal)
- Data Transformations (Processing Steps)
- Data Sinks (Storage and External Systems)
- Event Flows (using ev.* definitions)
  - Event propagation patterns
  - Event consumers
  - Downstream events
- Processing Patterns
  - Real-time flows
  - Near real-time flows
  - Batch flows
- Mermaid Flow Diagrams
  ```mermaid
  flowchart TD
    User[User Web App] --> API[API Gateway]
    API --> Valid{Validate}
    Valid -->|Valid| Proc[Process Order]
    Valid -->|Invalid| Err[Return Error]
    Proc --> DB[(Database)]
    Proc --> Queue[Message Queue]
    Queue --> Email[Email Service]
    Queue --> Analytics[Analytics]
    Queue --> Inventory[Inventory Service]
  ```
- Data Lineage
  - Source → Transformation → Destination
  - Field-level lineage (where possible)

## Validation

After generation:

!`test -f docs/design/data-flow-diagram.md && echo "✓ data-flow-diagram.md created" || echo "✗ Generation failed"`

**Flow diagram checklist**:
!`if [ -f docs/design/data-flow-diagram.md ]; then
  grep -ci "source\|input\|external" docs/design/data-flow-diagram.md | xargs echo "Data sources:"
  grep -ci "transformation\|processing\|etl" docs/design/data-flow-diagram.md | xargs echo "Transformations:"
  grep -o "ev\.[a-z0-9_]*\.[a-z0-9_]*" docs/design/data-flow-diagram.md | sort -u | wc -l | xargs echo "Events referenced:"
  grep -ci "mermaid" docs/design/data-flow-diagram.md | xargs echo "Flow diagrams:"
fi`

## Next Steps

**Create data catalog**:
```
/data-catalog
```

**Validate data architecture**:
```
/validate-gate deliver
```

---

**Data flow diagram generated!** Data sources, transformations, event flows, and sinks documented with Mermaid diagrams.
