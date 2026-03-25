---
description: Initialize or update ids.yml registry with namespace and product information
argument-hint: [namespace] [product-name]
allowed-tools: Write, Read, Bash
model: sonnet
---

# Initialize IDs Registry

Initialize or update the `ids.yml` registry file with namespace and product information.

## Overview

The `ids.yml` file is the **central registry** for all IDs used across templates:
- **Namespace**: Your organization/team identifier (e.g., acme, myorg)
- **Product**: Product name (e.g., mobile-app, analytics-platform)
- **ID Types**: Document IDs, item IDs, special formats
- **Cross-references**: How IDs link between documents

## Arguments

- **namespace**: Your organization identifier (lowercase, no spaces)
- **product-name**: Product name (lowercase, hyphen-separated)

Example:
```bash
/init-ids acme mobile-banking-app
```

## Check Current Status

!`if [ -f docs/ids.yml ]; then
  echo "✓ ids.yml exists"
  grep "namespace:" docs/ids.yml
  grep "product:" docs/ids.yml
else
  echo "⚠ ids.yml not found - will create new file"
fi`

## Create/Update ids.yml

Creating registry with namespace **$ARGUMENTS[0]** and product **$ARGUMENTS[1]**...

!`mkdir -p docs && echo "✓ docs/ directory ready"`

Writing ids.yml configuration:

```yaml
# IDs Registry
# Central registry for all IDs used across product documentation

metadata:
  namespace: ${ARGUMENTS[0]:-myorg}
  product: ${ARGUMENTS[1]:-my-product}
  created: $(date +%Y-%m-%d)
  version: "1.0"

# ID Format Rules
id_formats:
  document_ids:
    description: "Lowercase abbreviations for document types"
    pattern: "[a-z]{2,5}"
    examples:
      - vis    # Product Vision
      - brd    # Business Requirements
      - prd    # Product Requirements
      - frd    # Functional Requirements
      - srs    # Software Requirements
      - erd    # Entity Relationship Diagram
      - uxsm   # UX Sitemap
      - uxdd   # UX Design Decisions

  item_ids:
    description: "Prefix + hyphen + number"
    pattern: "[a-z]+-[0-9]+"
    examples:
      - bo-1   # Business Objective
      - prd-f-1  # PRD Feature (Must)
      - us-1   # User Story
      - fs-auth-1  # Feature Spec Requirement
      - nfr-1  # Non-Functional Requirement
      - adr-1  # Architecture Decision Record

  special_formats:
    data_fields:
      pattern: "dict.entity.field"
      examples:
        - dict.user.email
        - dict.order.total_amount

    events:
      pattern: "ev.domain.action"
      examples:
        - ev.user.registered
        - ev.order.completed

    design_tokens:
      pattern: "tok.category.name"
      examples:
        - tok.color.primary
        - tok.spacing.md
        - tok.typography.heading1

    api_endpoints:
      pattern: "api-method-resource"
      examples:
        - api-get-users
        - api-post-orders

    cross_project:
      pattern: "@namespace/id"
      examples:
        - "@auth/user-model"
        - "@payments/checkout-flow"

# Traceability Chains
traceability:
  primary_chain:
    description: "Vision → Requirements → Stories → Implementation"
    flow:
      - vis (Product Vision)
      - bo-# (Business Objectives)
      - prd-f-# (PRD Features - Must/Should/Could)
      - ep-# (Epics)
      - us-# (User Stories)
      - fr-# (Functional Requirements)
      - nfr-# (Non-Functional Requirements)

  data_chain:
    description: "Requirements → Data Model → Implementation"
    flow:
      - fr-# (Functional Requirements)
      - entities (from DRD)
      - tables (from ERD)
      - dict.* (from Data Dictionary)
      - schema DDL (from Database Schema)

  ux_chain:
    description: "Stories → UX Design → Frontend"
    flow:
      - us-# (User Stories)
      - screens (from Wireframes)
      - components (from Design Requirements)
      - tok.* (from Style Guide)
      - frontend specs (Frontend Requirements)

  api_chain:
    description: "Requirements → API → Frontend"
    flow:
      - fr-# (Functional Requirements)
      - endpoints (from Backend Requirements)
      - api-* IDs
      - frontend integration (Frontend Requirements)

# Single Source of Truth (SST) Rules
sst_rules:
  given_when_then:
    location: "user-stories.md ONLY"
    pattern: "Given/When/Then acceptance criteria"
    references: "Other docs reference us-# IDs"

  nfr_targets:
    location: "tech-spec.md ONLY"
    pattern: "NFR-# with quantified targets"
    references: "Other docs reference nfr-# IDs"

  api_schemas:
    location: "api-spec.md ONLY"
    pattern: "Request/response schemas, endpoints"
    references: "Frontend references api-# endpoints"

  design_tokens:
    location: "style-guide.md ONLY"
    pattern: "tok.* definitions with values"
    references: "Other docs reference tok.* tokens"

  data_fields:
    location: "data-dictionary.md ONLY"
    pattern: "dict.* field definitions"
    references: "Other docs reference dict.* fields"

  events:
    location: "data-dictionary.md ONLY"
    pattern: "ev.* event definitions"
    references: "Other docs reference ev.* events"

  database_ddl:
    location: "database-spec.md ONLY"
    pattern: "CREATE TABLE statements"
    references: "Other docs reference table names"

# Gates and Validation
gates:
  discover_gate:
    required_ids:
      - vis (validated)
      - bo-# (3-5 objectives)
    criteria:
      - "5W2H coverage (7/7)"
      - "NSM baseline/target/window"
      - "3-5 Must features identified"

  define_gate:
    required_ids:
      - prd-f-# (Must features)
      - ep-# (epics)
      - us-# (P0 stories)
      - fr-# (functional requirements)
    criteria:
      - "Traceability: bo-# → prd-f-# → ep-# → us-# → fr-#"
      - "Each Must has success criteria"

  develop_gate:
    required_ids:
      - nfr-# (quantified)
      - adr-# (decisions)
    criteria:
      - "C4 diagrams complete"
      - "NFRs have targets and verification"
      - "Deploy targets chosen"

  deliver_gate:
    required_ids:
      - dict.* (data fields)
      - ev.* (events)
      - tok.* (design tokens)
      - api-* (endpoints)
    criteria:
      - "All 3 parallel tracks complete"
      - "Frontend references data/UX/API"
      - "SST rules enforced"

# Document Dependencies
document_flow:
  order_1_3:
    - project-context.md
    - product-vision.md (vis, bo-#)
    - user-journey.md

  order_4_8:
    - prd.md (prd-f-#)
    - user-stories.md (us-#, Given/When/Then)
    - feature-spec-[name].md (FS-[name]-#)
    - architecture-diagram.md (C4)
    - tech-spec.md (nfr-#, adr-#)

  order_9_15:
    - data-requirements.md
    - erd.md
    - database-spec.md (DDL + requirements)
    - data-dictionary.md (dict.*, ev.*)
    - data-flow-diagram.md
    - data-catalog.md

  order_16:
    - api-spec.md (api-*)

  order_17_20:
    - user-journey.md
    - ux-sitemap.md
    - wireframes.md
    - style-guide.md (tok.*)

  order_24_26:
    - implementation-plan.md
    - sprint-status.yaml
    - quality-checklist.md
```

## Validation

After initialization:

!`if [ -f docs/ids.yml ]; then
  echo "✓ ids.yml created/updated"
  wc -l docs/ids.yml | awk '{print "Lines:", $1}'
  grep -c "pattern:" docs/ids.yml | xargs echo "ID patterns defined:"
  grep -c "flow:" docs/ids.yml | xargs echo "Traceability chains:"
else
  echo "✗ Failed to create ids.yml"
fi`

## Next Steps

**Start using the registry**:
```
/start-project     # Uses ids.yml for initialization
```

**Validate ID usage**:
```
/check-traceability  # Verify ID chains
/check-sst          # Verify Single Source of Truth
```

**Generate specific documents**:
```
/vision            # Creates vis, bo-# IDs
/prd               # Creates prd-f-# IDs
```

---

**IDs registry initialized!** All templates will reference this central configuration.
