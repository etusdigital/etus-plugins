---
doc_meta:
  id: be
  display_name: Backend Requirements
  pillar: Build
  owner_role: Backend Lead
  summary: Defines API endpoints, schemas, auth, and integration contracts for services.
  order: 18
  gate: technical
  requires:
  - frd
  - srs
  - stor
  - data
  - erd
  - sql
  optional:
  - dict
  feeds:
  - dict
uuid: <UUID>
version: 0.1.0
status: Draft
owners:
- <owner>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- Backend
- API
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Solo Backend Requirements - [Service Name]

**Author:** [Your Name]  
**Date:** [YYYY-MM-DD]  
**Context:** SOLO - Single developer project

---

## Document Control

- **Version:** 1.0
- **Status:** [Draft/Review/Approved]
- **API Version:** [v1]
- **References:** prd, us-#, fr-#, nfr-#
- **ID Pattern:** Each endpoint gets be-ep-# for traceability (be-ep-1, be-ep-2, etc.)

## API Context

**Service Purpose:** [What this backend service accomplishes]
**Upstream Dependencies:** References PRD features, User Stories (us-#), Functional Requirements (fr-#)
**Downstream Consumers:** Frontend applications, mobile apps, third-party integrations

## 🎯 Problem Statement

**Core Problem:** [What user/business problem does this backend solve?]
**Impact if Unsolved:** [Consequences of not having this backend]
**Success Metrics:** [How we measure problem resolution]

- Metric 1: [Specific measurable outcome]
- Metric 2: [User behavior change expected]
- Metric 3: [Business impact measurement]

## 🔍 Backend Discovery Checklist

### Data Operations Analysis

□ All CRUD operations identified per entity
□ Batch vs single operations defined
□ Real-time vs async operations classified
□ Transaction boundaries established
□ Pagination strategies selected
□ Search/filter requirements captured

### Integration Requirements

□ All external APIs identified with vendors
□ Authentication methods documented (OAuth2, API keys, etc.)
□ Rate limits and quotas recorded
□ Webhook endpoints defined
□ Fallback strategies specified
□ Circuit breaker patterns identified

### Security & Compliance

□ Authentication pattern selected (JWT, session, etc.)
□ Authorization model defined (RBAC, ABAC, etc.)
□ PII fields identified for encryption
□ Audit trail requirements specified
□ Compliance needs documented (GDPR, CCPA, etc.)
□ API key rotation strategy defined

### Performance & Scale

□ Expected request volumes estimated
□ Peak traffic patterns identified
□ Caching strategies defined
□ Database connection pooling configured
□ Response time targets set (reference SRS)
□ Concurrent user limits established

### Often Missed Requirements

□ Idempotency keys for critical operations
□ Soft delete vs hard delete strategy
□ Timezone handling for all timestamps
□ File upload size limits and types
□ Background job processing needs
□ Email/notification triggers per action
□ Data export formats required
□ Bulk operation limits
□ Concurrent update conflict resolution
□ Session management strategy

## 🗺️ User Journey to Backend Mapping

| Journey Step | User Intent       | Triggers          | API Call            | Data Change       | Next State           |
| ------------ | ----------------- | ----------------- | ------------------- | ----------------- | -------------------- |
| [Step name]  | [What user wants] | [Action]          | [Endpoint]          | [CRUD op]         | [Result]             |
| Registration | Create account    | Submit form       | POST /auth/register | Create user       | Verification pending |
| Login        | Access app        | Enter credentials | POST /auth/login    | Update last_login | Authenticated        |
| View list    | Browse items      | Page load         | GET /resources      | Read only         | Items displayed      |
| Create item  | Add new content   | Click save        | POST /resources     | Insert record     | Item created         |

## 🎯 API Endpoint Specifications (MoSCoW Priority)

### Priority Matrix

#### Must Have (P0 - MVP Critical)

- Authentication endpoints (login, logout, refresh)
- Core entity CRUD operations
- Essential search/filter endpoints
- Critical integration webhooks

#### Should Have (P1 - Important)

- Batch operations endpoints
- Advanced search capabilities
- Secondary integration points
- Export/import endpoints

#### Could Have (P2 - Enhancement)

- Analytics endpoints
- Reporting capabilities
- Nice-to-have integrations

#### Won't Have (P3 - Future)

- [Document for roadmap visibility]

### API Endpoints

#### Authentication & Authorization

**POST /api/v1/auth/login**

- **Endpoint ID:** be-ep-1
- **Priority:** P0 (Must Have)
- **Purpose:** User authentication
- **Request Body:** `{email, password}`
- **Response:** `{token, user, expires_at}`
- **Tracking:** Event ev.auth.login (see Data Dictionary)
- **Errors:** 401 (invalid credentials), 429 (rate limited)

**POST /api/v1/auth/refresh**

- **Endpoint ID:** be-ep-2
- **Priority:** P0 (Must Have)
- **Purpose:** Token refresh
- **Headers:** `Authorization: Bearer <refresh_token>`
- **Response:** `{token, expires_at}`
- **Tracking:** Event ev.auth.token_refresh

#### [Resource Group Name]

**GET /api/v1/[resources]**

- **Endpoint ID:** be-ep-3
- **Priority:** [P0/P1/P2]
- **Purpose:** List resources with pagination
- **Query Params:** `page, limit, sort, filter`
- **Response:** `{data: [], meta: {total, page, limit}}`
- **Tracking:** Event ev.[resource].list
- **Cache:** [TTL if applicable]

**POST /api/v1/[resources]**

- **Endpoint ID:** be-ep-4
- **Priority:** [P0/P1/P2]
- **Purpose:** Create new resource
- **Request Body:** [Reference entity schema]
- **Response:** Created resource with ID
- **Tracking:** Event ev.[resource].create
- **Validation:** [Reference fr-# for business rules]

## 📊 Analytics & Telemetry Requirements

### API Event Tracking

Each endpoint must emit telemetry events for marketing analytics:

| Endpoint         | Event ID             | Payload                    | Marketing Use       |
| ---------------- | -------------------- | -------------------------- | ------------------- |
| POST /auth/login | ev.auth.login        | user_id, timestamp, source | Conversion tracking |
| GET /[resource]  | ev.[resource].view   | resource_id, user_id       | Engagement metrics  |
| POST /[resource] | ev.[resource].create | resource_id, user_id       | Feature adoption    |

### Conversion Funnel Events

**Registration Funnel:**

1. ev.auth.signup_start → 2. ev.auth.email_verify → 3. ev.auth.onboard_complete

**Core Action Funnel:**

1. ev.[feature].initiate → 2. ev.[feature].complete → 3. ev.[feature].share

### Performance Metrics

- **Response Time:** Track metrics per nfr-5 performance requirements
- **Error Rates:** Track by error code and endpoint
- **Usage Patterns:** Track requests per user segment
- **Attribution:** Capture UTM parameters, referrer on entry points

## 🔌 External Integrations

### Integration Architecture Strategy

**Integration Selection Criteria:**

- **Business Requirements:** [What external capabilities are needed]
- **Data Flow Requirements:** [How data flows between systems]
- **Reliability Requirements:** [Uptime and failure handling needs]
- **Security Requirements:** [Authentication and data protection needs]

**Integration Patterns:**

- **Synchronous Integration:** [Real-time data exchange requirements]
- **Asynchronous Integration:** [Background processing and queue-based needs]
- **Event-Driven Integration:** [Event publishing and subscription patterns]

### Required External Services

**[Service Category 1]: [Service Purpose]**

- **Selected Service:** [Chosen service with rationale]
- **Integration Pattern:** [How integration is implemented]
- **Protocol:** [Communication protocol with rationale]
- **Authentication Strategy:** [Authentication method with rationale]
- **Data Exchange Format:** [Data format and schema requirements]
- **Error Handling Strategy:** [Failure modes and recovery patterns]
- **Rate Limiting:** [Request limits and backoff strategies]
- **Monitoring Requirements:** [Health checks and performance metrics]

**[Service Category 2]: [Service Purpose]**

- **Selected Service:** [Chosen service with rationale]
- **Integration Pattern:** [How integration is implemented]
- **Protocol:** [Communication protocol with rationale]
- **Authentication Strategy:** [Authentication method with rationale]
- **Data Exchange Format:** [Data format and schema requirements]
- **Error Handling Strategy:** [Failure modes and recovery patterns]
- **Rate Limiting:** [Request limits and backoff strategies]
- **Monitoring Requirements:** [Health checks and performance metrics]

### Webhook Endpoints

**POST /api/v1/webhooks/[provider]**

- **Authentication:** [Signature verification method]
- **Retry Policy:** [How provider retries failed deliveries]
- **Event Types:** [List of events we handle]
- **Processing:** [Async/sync, queue strategy]

## 📐 Business Logic & Validation Rules

### Validation Rules per Entity

**[Entity Name]:**

- **Field Validations:** [List specific rules - email format, string length, etc.]
- **Cross-field Validations:** [Dependencies between fields]
- **State Transitions:** [Valid state changes - draft→published, etc.]
- **Business Constraints:** [Domain-specific rules]

**User Entity Example:**

- **Field Validations:**
  - email: valid format, unique in database
  - password: min 8 chars, requires uppercase, number
  - age: must be >= 13
- **Cross-field Validations:**
  - If role='admin', must have verified_email=true
- **State Transitions:**
  - pending → active (after email verification)
  - active → suspended (by admin only)
  - suspended → active (by admin only)
- **Business Constraints:**
  - Cannot delete user with active subscriptions
  - Cannot have more than 3 active sessions

## 🚨 Error Handling

### Standard Error Response

```json
{
	"error": {
		"code": "ERROR_CODE",
		"message": "User-friendly message",
		"field": "field_name (if applicable)",
		"request_id": "uuid"
	}
}
```

### Error Codes

| Code               | HTTP | Description              | User Action      |
| ------------------ | ---- | ------------------------ | ---------------- |
| AUTH_REQUIRED      | 401  | Missing authentication   | Login required   |
| PERMISSION_DENIED  | 403  | Insufficient permissions | Contact admin    |
| VALIDATION_ERROR   | 400  | Invalid input            | Fix field errors |
| RATE_LIMITED       | 429  | Too many requests        | Wait and retry   |
| RESOURCE_NOT_FOUND | 404  | Entity doesn't exist     | Check ID         |
| CONFLICT           | 409  | Duplicate or conflict    | Resolve conflict |
| SERVICE_ERROR      | 503  | External service down    | Retry later      |

## 📋 Traceability Matrix

| User Story | Endpoints                  | Priority | Status |
| ---------- | -------------------------- | -------- | ------ |
| us-#       | POST /api/v1/[resource]    | P0       | [ ]    |
| us-#       | GET /api/v1/[resource]     | P0       | [ ]    |
| us-#       | PUT /api/v1/[resource]/:id | P1       | [ ]    |

## Implementation Checklist

### Pre-Development

□ All P0 endpoints identified
□ External API credentials obtained
□ Rate limits documented
□ Error codes standardized

### Development

□ Authentication implemented
□ P0 endpoints complete
□ Telemetry events integrated
□ Error handling consistent

### Pre-Launch

□ All integrations tested
□ Webhooks verified
□ Performance targets met (see SRS)
□ Security scan passed
