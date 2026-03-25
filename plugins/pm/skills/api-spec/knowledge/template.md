# API Specification Template

## Responsaveis

- **Owner:** Tech Lead
- **Contribuem:** PM, Frontend Dev, Dev team
- **Aprovacao:** PM + Tech Lead

Use this template as a guide to structure api-spec.md.

## 1. API Overview

```markdown
# API Specification

## Overview

**API Type:** REST | GraphQL | gRPC
**Base URL:** https://api.example.com
**Current Version:** v1

### Design Principles
- RESTful resource-oriented design
- JSON request/response
- Standard HTTP status codes
- Bearer token authentication
```

## 2. Base URL & Versioning

```markdown
## Base URL & Versioning

### URL Structure
```
https://api.example.com/api/v1/...
```

### Versioning Strategy
- Version in URL path: `/api/v1/`, `/api/v2/`
- Sunset policy: Previous version supported for 6 months
```

## 3. Authentication & Authorization

```markdown
## Authentication & Authorization

### Authentication Method: Bearer Token

**Header:**
```
Authorization: Bearer <access_token>
```

**Token Acquisition:**
- POST /auth/login (email, password)
- POST /auth/refresh (refresh_token)
- Returns: { access_token, refresh_token, expires_in }

### Authorization
- Role-based access control (RBAC)
- Roles: admin, editor, viewer
- Validated per endpoint in ACL table
```

## 4. Endpoints (Grouped by Resource)

```markdown
## Endpoints

### Users Resource

#### GET /users
Get all users (paginated)

**Request Parameters:**
- `page` (query, int): Page number (default: 1)
- `limit` (query, int): Items per page (default: 20)

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "user-001",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "editor",
      "created_at": "2026-03-14T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

**Status Codes:**
- `200 OK` — Success
- `401 Unauthorized` — Invalid token
- `403 Forbidden` — Insufficient permissions

**Examples:** curl, JavaScript

---

#### POST /users
Create new user (admin only)

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "name": "Jane Doe",
  "password": "secure-password",
  "role": "editor"
}
```

**Response (201 Created):**
```json
{
  "id": "user-002",
  "email": "newuser@example.com",
  "name": "Jane Doe",
  "role": "editor",
  "created_at": "2026-03-14T10:30:00Z"
}
```

**Status Codes:**
- `201 Created` — User created
- `400 Bad Request` — Invalid input
- `409 Conflict` — Email already exists
```

## 5. Error Handling

```markdown
## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Email is required",
    "status": 400,
    "details": {
      "field": "email",
      "reason": "must_not_be_empty"
    },
    "request_id": "req-12345"
  }
}
```

### Standard Error Codes
- `INVALID_INPUT` (400) — Validation error
- `UNAUTHORIZED` (401) — Missing/invalid token
- `FORBIDDEN` (403) — Insufficient permissions
- `NOT_FOUND` (404) — Resource not found
- `CONFLICT` (409) — Resource already exists
- `INTERNAL_SERVER_ERROR` (500) — Server error
```

## 6. Rate Limiting

```markdown
## Rate Limiting

### Limits
- **Default:** 100 requests/minute per user
- **Burst:** 10 requests/second
- **Admin:** Unlimited

### Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1710406800
```

### Behavior
- Exceeded: HTTP 429 Too Many Requests
- Reset: Per minute, rolling window
```

## 7. Pagination

```markdown
## Pagination

### Strategy: Cursor-based

**Request Parameters:**
```
GET /users?limit=20&cursor=abc123
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "next_cursor": "xyz789",
    "has_more": true
  }
}
```

### Alternative: Offset-based

**Request Parameters:**
```
GET /users?page=2&limit=20
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 500,
    "pages": 25
  }
}
```
```

## 8. Webhook Events

```markdown
## Webhook Events

### Event Subscription
POST /webhooks

**Request:**
```json
{
  "url": "https://your-app.com/webhooks",
  "events": ["ev.user.created", "ev.payment.completed"]
}
```

### Event Payload
```json
{
  "event_id": "evt-12345",
  "event_type": "ev.user.created",
  "timestamp": "2026-03-14T10:00:00Z",
  "data": {
    "user_id": "user-001",
    "email": "user@example.com"
  }
}
```

### Retry Policy
- Maximum 5 retries
- Exponential backoff: 1s, 2s, 4s, 8s, 16s
```

## Notes

- All timestamps are ISO 8601 (UTC)
- All IDs are UUIDs or sequential alphanumeric
- Empty arrays [] instead of null for collections
- Paginated endpoints default to page 1, limit 20

## O que fazer / O que nao fazer

**O que fazer:**
- Definir request/response schema com tipos exatos
- Documentar todos os codigos de erro com mensagem
- Incluir autenticacao e rate limiting por endpoint
- Versionar a API desde o inicio (v1)

**O que nao fazer:**
- Nao duplicar schemas que estao no database-spec (referenciar dict.*)
- Nao criar endpoints sem vincular a US-# ou PRD-F-#
- Nao omitir paginacao em endpoints de listagem
- Nao esquecer de documentar headers obrigatorios

