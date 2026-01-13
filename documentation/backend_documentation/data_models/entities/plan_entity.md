# Plan Entity

Represents a single day's study plan.

## Schema

| Column | Type | Constraints | Purpose |
|:---|:---|:---|:---|
| `id` | Integer | PK | Unique identifier |
| `user_id` | Integer | FK (User), CASCADE | Owner of the plan |
| `plan_date` | Date | NOT NULL | Day this plan is for |
| `notes` | Text | Nullable | User's notes |
| `generation_id` | String(36) | Nullable | UUID grouping plans from same generation |
| `created_at` | DateTime | NOT NULL, DEFAULT=UTC | When plan was created |
| `updated_at` | DateTime | NOT NULL, DEFAULT=UTC | Last update time |

## Example

```json
{
  "id": 1,
  "user_id": 1,
  "generation_id": "550e8400-e29b-41d4-a716-446655440000",
  "plan_date": "2026-01-13",
  "created_at": "2026-01-12T10:00:00Z"
}
```

## Relationships

- Many-to-One: Plan → User
- One-to-Many: Plan → AITask (cascade delete)
- Grouped-by: generation_id

## Key Properties

- One plan per day per generation
- All plans with same `generation_id` form a complete schedule
- New generation (e.g., after feedback) creates new `generation_id` with new Plan records
- Previous generation plans remain for history
