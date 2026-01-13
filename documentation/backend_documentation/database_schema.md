# Data Persistence & Schema

The application uses a **Relational Database** via SQLAlchemy. The schema is designed to support the "Parent-Child" relationships required by the AI generation process.

## Entity Relationship Diagram (Abstract)

* **User** `1 : N` **Subject** (A student has many subjects)
* **User** `1 : N` **Plan** (A student has many daily plans)
* **User** `1 : N` **Feedback** (A student provides feedback on generations)
* **Plan** `1 : N` **AITask** (A day consists of many specific tasks)
* **Subject** `1 : N` **AITask** (A task belongs to a subject)

## Key Schema Design Decisions

| Entity | Field | Type | Design Rationale |
| :--- | :--- | :--- | :--- |
| **User** | `password` | `String` | Stored strictly as a Bcrypt Hash. |
| **Plan** | `generation_id` | `UUID String` | Allows grouping multi-day plans (e.g., a "Weekly Schedule") generated in one batch. Critical for the "Reschedule" feature. |
| **Subject** | `type` | `Enum` | Restricted to `written`, `practical`, `project`. Matches the specific AI Agents (`CSAgent` vs `MathAgent`) capabilities. |
| **Feedback** | `generation_id` | `UUID String` | Links feedback to a specific *version* of a schedule, enabling the `FeedbackAgent` to compare "Planned vs Actual". |
| **AITask** | `time_allotted` | `String` | stored as "HH:MM–HH:MM" strings for flexibility in display. |

## Constraints
* **Difficulty:** `CHECK (difficulty >= 1 AND difficulty <= 5)`
* **Priority:** `CHECK (priority >= 1 AND priority <= 10)`
* **Uniqueness:** `UniqueConstraint("user_id", "generation_id")` on Feedback table (One feedback per schedule generation).