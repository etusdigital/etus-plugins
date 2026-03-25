---
description: Generate Data Catalog with asset inventory, lineage, and governance
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Data Catalog

Creating data catalog for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/design/data-dictionary.md && echo "✓ data-dictionary.md exists" || echo "⚠ Missing data dictionary"`
!`test -f docs/design/data-flow-diagram.md && echo "✓ data-flow-diagram.md exists" || echo "⚠ Missing data flow diagram"`

## Setup

!`mkdir -p docs/data && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/data-chain/knowledge/data-catalog.md

## Interactive Catalog Creation

I'll help you build a comprehensive data catalog:

### Step 1: Review Data Assets

Read existing data documentation:

@docs/design/data-dictionary.md
@docs/design/data-flow-diagram.md
@docs/design/database-spec.md

### Step 2: Data Asset Inventory

**For each data asset (table, view, dataset), catalog:**

**Asset metadata:**
1. **Name**: Table/dataset name
2. **Type**: Table, View, Materialized View, External Dataset
3. **Location**: Database, schema, file path
4. **Size**: Row count estimate, storage size
5. **Update frequency**: Real-time, hourly, daily, static
6. **Owner**: Team or person responsible
7. **Description**: What this asset contains
8. **Business purpose**: Why it exists
9. **Quality score**: Data quality rating (1-5)

[Catalog all data assets]

**Example:**
```
Asset: users table
Type: Database table
Location: postgres://prod/public/users
Size: ~500K rows, 50 MB
Update frequency: Real-time (on user actions)
Owner: User Management Team
Description: Core user account information
Business purpose: Authentication, user profile management
Quality score: 5/5 (high quality, well-maintained)
```

### Step 3: Data Lineage

**Ask about data lineage:**

For each asset:
1. **Upstream sources**: Where does this data come from?
   - User input
   - External API
   - Derived from other tables
2. **Transformation logic**: How is data transformed?
3. **Downstream consumers**: Who/what uses this data?
   - Reports
   - Analytics
   - Other services
   - External systems

**Lineage example:**
```
User Registration Form
  ↓
API Validation
  ↓
users table (created)
  ↓ (used by)
  ├─→ Authentication Service
  ├─→ Email Service
  ├─→ Analytics Dashboard
  └─→ CRM Export (daily batch)
```

### Step 4: Data Ownership

**Ask about ownership and stewardship:**

1. **Data domains**: Organize assets by business domain
   - User domain (user, profile, auth tables)
   - Order domain (order, order_item tables)
   - Product domain (product, inventory tables)
2. **Domain owners**: Who owns each domain?
3. **Stewards**: Who maintains data quality?
4. **SLA**: Service level agreements for each asset
   - Uptime requirements
   - Data freshness requirements
   - Query performance requirements

### Step 5: Data Classification

**Classify each asset by sensitivity:**

1. **Public**: Non-sensitive, can be shared openly
2. **Internal**: Internal use only, no PII
3. **Confidential**: Contains PII, restricted access
4. **Restricted**: Highly sensitive (financial, health, auth)

**PII identification:**
- Which assets contain PII? (email, name, address, phone)
- GDPR/CCPA applicability?
- Anonymization requirements?

### Step 6: Data Quality Metrics

**Ask about quality monitoring:**

For each asset:
1. **Completeness**: % of required fields populated
2. **Accuracy**: Error rate, validation failures
3. **Consistency**: Cross-table consistency checks
4. **Timeliness**: Data freshness, lag time
5. **Uniqueness**: Duplicate detection
6. **Validity**: Constraint violations

**Quality dashboards:**
- Real-time quality metrics
- Alerts for quality issues
- Quality trends over time

### Step 7: Access Control

**Document access policies:**

1. **Read access**: Who can query this data?
2. **Write access**: Who can modify this data?
3. **Admin access**: Who can alter schema?
4. **Audit logging**: Track who accesses what?
5. **Data masking**: Mask PII in non-prod environments?

### Step 8: Confirm Catalog

"Here's the data catalog:

**Assets Cataloged:** 15 tables, 3 views

**Key Assets:**
- users (500K rows, Confidential, PII)
  - Owner: User Management Team
  - Quality: 5/5
  - Used by: Auth, Email, Analytics, CRM
- orders (2M rows, Confidential)
  - Owner: Order Management Team
  - Quality: 4/5
  - Used by: Reports, Finance, Fulfillment

**Data Domains:**
- User Domain (users, profiles, auth_tokens)
  - Owner: User Management Team
- Order Domain (orders, order_items, shipments)
  - Owner: Order Management Team
[etc.]

**Classification:**
- 5 assets: Confidential (PII)
- 8 assets: Internal
- 2 assets: Public

Is this catalog complete and accurate?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/data-catalog.md`.

**Document Structure:**
- Data Asset Inventory
  - For each asset:
    - Name, type, location
    - Size and update frequency
    - Owner and description
    - Business purpose
    - Quality score
- Data Lineage
  - Upstream sources
  - Transformation logic
  - Downstream consumers
  - Lineage diagrams (Mermaid)
- Data Ownership
  - Data domains
  - Domain owners
  - Stewards
  - SLAs
- Data Classification
  - Sensitivity levels
  - PII identification
  - Compliance requirements (GDPR, CCPA)
- Data Quality Metrics
  - Quality dimensions
  - Measurement methods
  - Quality dashboards
  - Quality SLAs
- Access Control
  - Read/write/admin policies
  - Audit logging
  - Data masking rules
- Data Governance
  - Change control process
  - Deprecation policy
  - Retention policies
  - Data lifecycle

## Validation

After generation:

!`test -f docs/design/data-catalog.md && echo "✓ data-catalog.md created" || echo "✗ Generation failed"`

**Catalog checklist**:
!`if [ -f docs/design/data-catalog.md ]; then
  grep -ci "asset\|table\|dataset" docs/design/data-catalog.md | xargs echo "Assets cataloged:"
  grep -ci "owner\|steward" docs/design/data-catalog.md | xargs echo "Ownership references:"
  grep -ci "pii\|confidential\|restricted" docs/design/data-catalog.md | xargs echo "Classification mentions:"
  grep -ci "quality\|completeness\|accuracy" docs/design/data-catalog.md | xargs echo "Quality metrics:"
fi`

## Next Steps

**Validate complete data architecture**:
```
/validate-gate deliver
```

**Continue with UX documentation**:
```
/ux-docs
```

Or generate UX documents individually:
```
/jtbd
/user-journey
/ux-sitemap
```

---

**Data catalog generated!** Complete data asset inventory with lineage, ownership, classification, and governance.
