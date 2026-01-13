# Feedback Entity

User feedback and ratings for schedule generations.

## Schema

| Column | Type | Constraints | Purpose |
|:---|:---|:---|:---|
| `id` | Integer | PK | Unique identifier |
| `user_id` | Integer | FK (User), CASCADE | User providing feedback |
| `generation_id` | String(36) | NOT NULL, UNIQUE (with user_id) | UUID of generation being rated (not FK) |
| `rating` | Integer | NOT NULL | Rating 1-5 (service-level validation) |
| `comments` | Text | Nullable | Optional user comment |
| `created_at` | DateTime | NOT NULL, DEFAULT=UTC | When feedback was submitted |

## Example

```json
{
  "id": 1,
  "user_id": 1,
  "generation_id": "550e8400-e29b-41d4-a716-446655440000",
  "rating": 5,
  "comment": "Too much work on Monday, please redistribute",
  "created_at": "2026-01-13T14:30:00Z"
}
```

## Relationships

- Many-to-One: Feedback → User
- References: generation_id (UUID, not foreign key)

## Key Properties

- Rating must be between 1 and 5
- Comment is optional
- Links feedback to specific generation, enabling regeneration
- Feedback triggers `/plans/reschedule` to generate improved schedule
- All feedback for a generation can be reviewed by user
