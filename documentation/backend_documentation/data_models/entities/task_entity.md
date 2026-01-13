# AITask Entity

Individual study tasks within a plan.

## Schema

| Column | Type | Constraints | Purpose |
|:---|:---|:---|:---|
| `id` | Integer | PK | Unique identifier |
| `ai_task_name` | String(255) | NOT NULL | Task name (e.g., "Lecture Review") |
| `time_allotted` | String(50) | NOT NULL | Time range (e.g., "08:00-10:00") |
| `difficulty` | Integer | CHECK [1,5], NOT NULL | Difficulty rating |
| `priority` | Integer | CHECK [1,10], NOT NULL | Priority ranking |
| `plan_id` | Integer | FK (Plan), CASCADE | Parent plan |
| `task_id` | Integer | FK (Subject), CASCADE | References Subject (actual task) |

## Example

```json
{
  "id": 1,
  "plan_id": 1,
  "subject_id": 1,
  "title": "Chapter 3-4 Practice Problems",
  "description": "Complete exercises 3.1 through 4.5",
  "task_date": "2026-01-13",
  "time_allocated": 120,
  "priority": "high",
  "status": "pending",
  "created_at": "2026-01-12T10:00:00Z"
}
```

## Relationships

- Many-to-One: AITask → Plan
- Many-to-One: AITask → Subject

## Key Properties

- Time allocated in minutes
- Status tracks user's progress (pending → in_progress → completed)
- Priority indicates relative importance among tasks on that day
- Deleting a plan cascades to delete all its AITasks
