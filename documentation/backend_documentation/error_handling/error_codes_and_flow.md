# Backend Error Reference

This document is the central repository for all backend error scenarios, validation failures, and error handling patterns.

---

## HTTP Error Status Codes

| HTTP Code | Layer | Cause |
|:---|:---|:---|
| **400** | Service/Database | Business rule violation, constraint violation, validation failure |
| **403** | Service | Authorization/ownership check failed |
| **404** | Route | Resource not found |
| **422** | Pydantic | Invalid request format, wrong type, missing required field |

---

## Error Handling Flow

**Sequential validation chain:**

1. **Pydantic** validates JSON structure, format, types → HTTP 422 if invalid
2. **Service** validates:
   - Resource existence → HTTP 404 if not found
   - Ownership/authorization → HTTP 403 if check fails
   - Business rules, constraints → HTTP 400 if invalid
3. **Database** validates constraints (CHECK, UNIQUE, FK) → HTTP 400 if violated
4. **Unexpected errors** → HTTP 500

---

### Service-Layer Errors

All service errors are raised as `ValueError` and caught by route handlers.

The service layer validates:
- **Existence**: Referenced entities exist (user_id, plan_id, task_id, subject_id) → HTTP 404 if not found
- **Ownership**: User owns the resource they're modifying/accessing (plan, subject) → HTTP 403 if check fails
- **Uniqueness**: Duplicates don't exist (Plan date per user, email, username, Google ID, feedback per user+generation) → HTTP 400 if invalid
- **Range Constraints**: Numeric values within valid ranges (difficulty [1,5], priority [1,10], rating [1,5]) → HTTP 400 if invalid
- **Required Fields**: Non-empty string values (name, email, title, ai_task_name, time_allotted) → HTTP 400 if invalid
- **Date Logic**: Start date not after end date → HTTP 400 if invalid
- **Business Rules**: Either generation_id or plan_id provided, plan has valid generation_id → HTTP 400 if invalid

---

### Database-Level Errors

Constraint violations raise `IntegrityError`, caught by route handlers.

The database layer enforces:
- **Check Constraints**: Numeric fields within valid ranges (difficulty [1,5], priority [1,10]) → HTTP 400 if violated
- **Unique Constraints**: No duplicate values (email, username, google_id, user_id+generation_id for feedback) → HTTP 400 if violated
- **Foreign Key Constraints**: All referenced entities exist (user_id, plan_id, task_id, student_id); cascade delete enforced → HTTP 400 if violated

---

### Pydantic Validation Errors

Validation failures return HTTP 422 Unprocessable Entity with structured validation information.

Pydantic validates:
- **Format**: Date strings in YYYY-MM-DD format, email format, datetime format → HTTP 422 if invalid
- **Type**: Values match declared types (integers for numeric fields, strings for text, dates for date fields) → HTTP 422 if invalid
- **Required Fields**: All mandatory fields provided (user_id, email, plan_date, rating, etc.) → HTTP 422 if missing
- **Enum Values**: Enum fields contain only allowed values (Subject type ∈ {WRITTEN, PRACTICAL, PROJECT}, Subject status ∈ {NOT_STARTED, IN_PROGRESS, COMPLETED}) → HTTP 422 if invalid

---


## Validation Layer Architecture

```
┌─────────────────────────────────────┐
│   Incoming HTTP Request             │
└─────────────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│   FastAPI Route Handler             │
│   (Authentication, basic checks)    │
└─────────────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│   Pydantic Model Validation         │
│   (JSON structure, type validation) │
│   → HTTP 422 if invalid             │
└─────────────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│   Service Layer Validation          │
│   (Business rules, FK checks,       │
│    uniqueness, ownership)           │
│   → HTTP 400/403/404 if invalid     │
└─────────────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│   Database Layer                    │
│   (Check constraints, unique        │
│    constraints, cascades)           │
│   → HTTP 400 if constraint violated │
└─────────────────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│   Database (tables updated)         │
└─────────────────────────────────────┘
```