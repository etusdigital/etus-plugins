---
description: Generate Data Dictionary with field definitions (dict.*) and events (ev.*)
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Data Dictionary

Creating data dictionary for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/design/database-spec.md && echo "✓ database-spec.md exists" || echo "⚠ Missing database spec"`

## Setup

!`mkdir -p docs/data && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/data-chain/knowledge/data-dictionary.md

## Interactive Dictionary Creation

I'll help you document field and event definitions:

### Step 1: Review Database Schema

Read table and column definitions:

@docs/design/database-spec.md

### Step 2: Field Definitions (dict.*)

**For each table and field, create dict.* entries:**

Format: `dict.{table}.{field}`

**Ask the user to provide details for each field:**

**Example: dict.user.email**
1. **Data type**: VARCHAR(255)
2. **Format/Pattern**: Email format (RFC 5322)
3. **Constraints**: NOT NULL, UNIQUE, max 255 chars
4. **Validation rules**: Valid email regex, lowercase only
5. **Business meaning**: User's primary email address for login and communications
6. **Example values**: "user@example.com", "john.doe@company.co"
7. **PII classification**: Yes, PII (GDPR applicable)
8. **Transformation rules**: Lowercase and trim before storage
9. **Related fields**: dict.user.email_verified, dict.user.email_notifications_enabled

[Document dict.* for ALL fields in ALL tables]

**Categories to cover:**
- dict.user.* (all user fields)
- dict.profile.* (all profile fields)
- dict.order.* (all order fields)
- dict.product.* (all product fields)
- dict.order_item.* (all order item fields)
[etc. for all tables]

### Step 3: Event Definitions (ev.*)

**Ask about domain events:**

Format: `ev.{domain}.{action}`

**For each event, document:**

**Example: ev.order.created**
1. **Trigger**: When is this event fired? (Order successfully created)
2. **Payload schema**: What data is included?
   ```json
   {
     "order_id": "uuid",
     "user_id": "uuid",
     "total": "decimal",
     "items": [{"product_id": "uuid", "quantity": "int"}],
     "created_at": "timestamp"
   }
   ```
3. **Consumers**: Who listens to this event?
   - Email service (send confirmation)
   - Analytics service (track conversion)
   - Inventory service (reserve stock)
4. **Retention policy**: How long is event stored? (90 days in event stream)
5. **Replay capability**: Can this event be replayed?
6. **Idempotency**: Can this event be processed multiple times safely?

[Document ev.* for ALL domain events]

**Event domains to cover:**
- ev.user.* (created, updated, deleted, logged_in, logged_out)
- ev.order.* (created, paid, shipped, delivered, cancelled)
- ev.product.* (created, updated, deleted, out_of_stock)
- ev.payment.* (initiated, completed, failed, refunded)
[etc. for all domain events]

### Step 4: Data Lineage

**Ask about data transformations:**

For derived/calculated fields:
1. **Source fields**: Where does this data come from?
2. **Transformation logic**: How is it calculated?
3. **Update frequency**: When is it recalculated?

**Example: dict.order.total**
- Source: SUM(order_items.quantity * order_items.price)
- Transformation: Calculated on order creation, cached in order table
- Update: Recalculated if order items change before payment

### Step 5: Confirm Dictionary

"Here's the data dictionary:

**Field Definitions (dict.*):**
- dict.user.email: VARCHAR(255), UNIQUE, PII, email format
- dict.user.name: VARCHAR(255), NOT NULL, display name
- dict.order.total: DECIMAL(10,2), calculated from items, >= 0
[etc. - hundreds of field definitions]

**Event Definitions (ev.*):**
- ev.user.created: User registration event
  - Payload: {user_id, email, created_at}
  - Consumers: Email, Analytics
- ev.order.paid: Order payment confirmed
  - Payload: {order_id, user_id, total, payment_method}
  - Consumers: Fulfillment, Notification
[etc.]

Is this dictionary complete and accurate?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/data-dictionary.md`.

**Document Structure:**
- Field Definitions (dict.*) - SINGLE SOURCE
  - Organized by table (entity)
  - For each dict.{table}.{field}:
    - Field name
    - Data type and format
    - Constraints
    - Validation rules
    - Business meaning
    - Example values
    - PII classification
    - Transformation rules
    - Related fields
    - Data lineage (if calculated)
- Event Definitions (ev.*) - SINGLE SOURCE
  - Organized by domain
  - For each ev.{domain}.{action}:
    - Event name
    - Trigger condition
    - Payload schema (JSON)
    - Consumers/listeners
    - Retention policy
    - Replay capability
    - Idempotency guarantee
- Cross-Reference Index
  - Fields by PII classification
  - Fields by table
  - Events by domain
  - Event consumers

**CRITICAL**:
- dict.* field definitions ONLY appear in data-dictionary.md (Single Source)
- ev.* event definitions ONLY appear in data-dictionary.md (Single Source)

## Validation

After generation:

!`test -f docs/design/data-dictionary.md && echo "✓ data-dictionary.md created" || echo "✗ Generation failed"`

**Dictionary checklist**:
!`if [ -f docs/design/data-dictionary.md ]; then
  grep -o "dict\.[a-z0-9_]*\.[a-z0-9_]*" docs/design/data-dictionary.md | sort -u | wc -l | xargs echo "Field definitions (dict.*):"
  grep -o "ev\.[a-z0-9_]*\.[a-z0-9_]*" docs/design/data-dictionary.md | sort -u | wc -l | xargs echo "Event definitions (ev.*):"
  grep -ci "pii\|personal.*information" docs/design/data-dictionary.md | xargs echo "PII classifications:"
fi`

## Next Steps

**Create data flow diagram**:
```
/data-flow-diagram
```

**Create data catalog**:
```
/data-catalog
```

**Check SST compliance**:
```
/check-sst
```

---

**Data dictionary generated!** Field definitions (dict.*) and event definitions (ev.*) documented as Single Source of Truth.
