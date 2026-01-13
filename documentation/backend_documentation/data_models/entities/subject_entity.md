# Subject Entity

Represents courses, exams, and projects a user needs to study for.

## Schema

| Column | Type | Constraints | Purpose |
|:---|:---|:---|:---|
| `id` | Integer | PK | Unique identifier |
| `title` | String(255) | NOT NULL | Subject title (e.g., "Linear Algebra") |
| `name` | String(255) | NOT NULL | Subject name |
| `type` | Enum | NOT NULL | WRITTEN, PRACTICAL, or PROJECT |
| `status` | Enum | NOT NULL, DEFAULT=NOT_STARTED | NOT_STARTED, IN_PROGRESS, or COMPLETED |
| `difficulty` | Integer | CHECK [1,5], NOT NULL, DEFAULT=1 | Difficulty rating |
| `start_date` | DateTime | Nullable | When subject starts |
| `end_date` | DateTime | Nullable | When subject ends (deadline) |
| `description` | Text | Nullable | Subject description |
| `student_id` | Integer | FK (User), CASCADE | Owner of the subject |
| `created_at` | DateTime | NOT NULL, DEFAULT=UTC | Creation timestamp |

## Example

```json
{
  "id": 1,
  "user_id": 1,
  "name": "Calculus",
  "exam_date": "2026-02-15",
  "exam_type": "exam",
  "priority": 8,
  "created_at": "2026-01-12T10:00:00Z"
}
```

## Relationships

- Many-to-One: Subject → User
- One-to-Many: Subject → Plan (via AITask)

## Key Properties

- Exam date is required and should be in future
- Priority helps AI prioritize study time allocation
- One subject can have multiple tasks across different plans
