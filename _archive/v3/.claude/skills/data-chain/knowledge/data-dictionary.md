---
doc_meta:
  id: dict
  display_name: Data Dictionary
  pillar: Data
  owner_role: Data Steward
  summary: Defines canonical field semantics, telemetry payloads, and validation constraints.
  order: 15
  gate: technical
  requires:
  - sql
  optional: []
  feeds:
  - cat
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
- Dictionary
- Telemetry
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Solo Data Dictionary - [System Name]

**Author:** [Your Name]  
**Date:** [YYYY-MM-DD]  
**Context:** SOLO - Single developer project

## Scope Guard

- Owns: field and telemetry payload definitions (names, types, meanings, constraints) for API/UI/analytics.
- Not included here: DDL, page/component behavior, endpoint shape ownership.

## 🔍 Problem Discovery

### What Problem Does This Solve? (WHY)

- **Data Confusion:** [What misunderstandings occur without clear definitions?]
- **Developer Pain:** [How does unclear data slow development?]
- **Business Impact:** [Cost of data misinterpretation]

### Who Needs This? (WHO)

- **Developers:** Need to understand field meanings for implementation
- **Product Team:** Need to verify data captures requirements
- **Analytics Team:** Need consistent definitions for tracking

## 🚀 MVP Data Elements (MoSCoW)

### Must Have (P0) - Core Business Logic

| Field Name | Type      | Meaning                | Constraint          | Tracks What         |
| ---------- | --------- | ---------------------- | ------------------- | ------------------- |
| user_id    | UUID      | Unique user identifier | Required, Immutable | User identity       |
| email      | string    | User email address     | RFC 5322, Unique    | Contact/login       |
| created_at | timestamp | Account creation time  | Auto-set, Immutable | User acquisition    |
| [field]    | [type]    | [business meaning]     | [validation]        | [analytics purpose] |

### Should Have (P1) - Enhanced Features

| Field Name  | Type      | Meaning            | When Introduced  | Tracks What |
| ----------- | --------- | ------------------ | ---------------- | ----------- |
| last_active | timestamp | Last user activity | After MVP launch | Engagement  |
| [field]     | [type]    | [meaning]          | [sprint/phase]   | [metric]    |

### Could Have (P2) - Future Enhancements

| Field Name  | Type   | Meaning       | Validation Trigger  | Future Use      |
| ----------- | ------ | ------------- | ------------------- | --------------- |
| preferences | json   | User settings | When features added | Personalization |
| [field]     | [type] | [meaning]     | [when to add]       | [potential]     |

## 📊 Analytics Tracking Dictionary

### Core Event Payloads

| Event Name        | Payload Fields                           | Purpose           | Marketing KPI             |
| ----------------- | ---------------------------------------- | ----------------- | ------------------------- |
| user_signup       | {user_id, source, timestamp, method}     | Track acquisition | CAC, Conversion Rate      |
| feature_used      | {user_id, feature_id, context, duration} | Track engagement  | DAU/MAU, Feature Adoption |
| purchase_complete | {user_id, amount, items, currency}       | Track revenue     | LTV, AOV, Revenue         |
| session_start     | {session_id, user_id, entry_point}       | Track visits      | Sessions, Bounce Rate     |

### Attribution Fields

| Field        | Type   | Captures          | Example                       |
| ------------ | ------ | ----------------- | ----------------------------- |
| utm_source   | string | Traffic source    | "google", "facebook", "email" |
| utm_medium   | string | Marketing medium  | "cpc", "organic", "referral"  |
| utm_campaign | string | Campaign name     | "summer_sale_2024"            |
| referrer_id  | UUID   | Referral tracking | User who referred             |
| device_type  | string | User device       | "mobile", "desktop", "tablet" |

## 🗺️ Data Through User Journey

### Discovery Stage

| Field        | Created When    | Used For               |
| ------------ | --------------- | ---------------------- |
| session_id   | First page view | Track discovery path   |
| landing_page | Initial visit   | Understand entry point |
| referrer_url | Page load       | Track traffic source   |

### Activation Stage

| Field            | Created When      | Used For              |
| ---------------- | ----------------- | --------------------- |
| signup_method    | Registration      | Optimize onboarding   |
| activation_event | First key action  | Measure time-to-value |
| onboarding_step  | Progress tracking | Identify drop-offs    |

### Retention Stage

| Field            | Created When      | Used For            |
| ---------------- | ----------------- | ------------------- |
| last_active      | Each interaction  | Identify churn risk |
| feature_adoption | Feature use       | Track stickiness    |
| engagement_score | Daily calculation | Predict retention   |

## 📊 Telemetry Events (ev.\*)

### Authentication Events

- **ev.auth.login**: User login (user_id, timestamp, source)
- **ev.auth.signup_start**: User starts signup (user_id, timestamp)
- **ev.auth.email_verify**: Email verification (user_id, timestamp)
- **ev.auth.token_refresh**: Token refresh (user_id, timestamp)
- **ev.auth.onboard_complete**: Onboarding complete (user_id, timestamp)

### Core Feature Events

- **ev.[feature].initiate**: Feature started (feature_id, user_id, timestamp)
- **ev.[feature].complete**: Feature completed (feature_id, user_id, timestamp)
- **ev.[feature].share**: Feature shared (feature_id, user_id, timestamp)

### Resource Events

- **ev.[resource].view**: Resource viewed (resource_id, user_id, timestamp)
- **ev.[resource].create**: Resource created (resource_id, user_id, timestamp)
- **ev.[resource].list**: Resource list viewed (user_id, timestamp, count)

## ✅ Field Validation Rules

### Format Validations

- **email:** RFC 5322 format → "Invalid email format"
- **phone:** E.164 format (+1234567890) → "Use international format"
- **currency:** 2 decimal places → "Invalid amount format"
- **url:** Valid URL format → "Invalid URL"
- **date:** ISO 8601 → "Use YYYY-MM-DD format"

### Business Rules

- **age:** Must be 13+ → "User must be 13 or older"
- **username:** 3-30 chars, alphanumeric → "Username must be 3-30 characters"
- **password:** Min 8 chars, 1 uppercase, 1 number → "Password too weak"
- **discount:** 0-100 range → "Invalid discount percentage"

### Cross-Field Validations

- **end_date > start_date** → "End date must be after start date"
- **quantity \* price = total** → "Total calculation mismatch"
- **role requires permissions** → "Role missing required permissions"

## 💻 Implementation Reference

### TypeScript Interface

```typescript
interface UserData {
	user_id: string; // UUID v4
	email: string; // RFC 5322
	created_at: Date; // ISO 8601
	last_active?: Date; // Optional, ISO 8601
}
```

### Validation Example

```javascript
const validateEmail = (email) =>
	/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? null : "Invalid email format";
```

### Analytics Event

```javascript
track("user_signup", {
	user_id: user.id,
	source: getUTMSource(),
	method: "email", // or 'google', 'facebook'
	timestamp: new Date().toISOString(),
});
```

### API Response Format

```json
{
	"data": {
		"user_id": "123e4567-e89b-12d3",
		"email": "user@example.com",
		"created_at": "2024-01-01T10:00:00Z"
	}
}
```

---
