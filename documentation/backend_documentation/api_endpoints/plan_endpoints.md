# Plan Endpoints

Plan generation, retrieval, and management.

## Endpoints (11 total)

| Method | Endpoint | Description |
|:---|:---|:---|
| POST | `/users/{user_id}/plans` | Create plan |
| POST | `/users/{user_id}/plans/generate` | Generate initial schedule |
| POST | `/users/{user_id}/plans/reschedule` | Submit feedback & regenerate |
| GET | `/users/{user_id}/plans` | List all plans |
| GET | `/users/{user_id}/plans/latest` | Get latest plan |
| GET | `/users/{user_id}/plans/latest-schedule` | Get latest full schedule |
| GET | `/users/{user_id}/plans/history` | Get all generation history |
| GET | `/users/{user_id}/plans/{plan_id}` | Get specific plan |
| GET | `/users/{user_id}/plans/date/{plan_date}` | Get plan by date |
| PUT | `/users/{user_id}/plans/{plan_id}` | Update plan |
| DELETE | `/users/{user_id}/plans/{plan_id}` | Delete plan |

## Key Details

**Create Plan** (`POST /users/{user_id}/plans`)
- Request: `{ "user_id": ..., "plan_date": "YYYY-MM-DD", "notes": "..." }`
- Response: Created plan with id and generation_id
- Creates a single plan for a specific date
- Can be called directly or via generation workflow

**Generate Initial Schedule** (`POST /users/{user_id}/plans/generate`)
- Initiates schedule generation workflow
- Request: `{ "subjects": [...], "time_availability": {...} }`
- Response: Plans for multiple days grouped by `generation_id`
- Calls AI System via BackendAPI wrapper
- Creates generation_id to track this version
- Returns all plans and associated AITasks

**Reschedule** (`POST /users/{user_id}/plans/reschedule`)
- Submits feedback and triggers regeneration
- Request: `{ "feedback_rating": 1-5, "feedback_comments": "..." }`
- Response: New plans from fresh generation_id
- Calls AI Rescheduler system with current + previous feedback
- Deletes old generation plans, creates new ones
- Feedback is preserved for history

**List All Plans** (`GET /users/{user_id}/plans`)
- Returns all plans for the user across all generations
- Optional filters: `?generation_id=...`, `?status=...`
- Includes: plan_id, plan_date, generation_id, created_date
- Ordered by date (newest first)

**Get Latest Plan** (`GET /users/{user_id}/plans/latest`)
- Returns the most recent plan created
- Useful for checking latest generation status
- Includes all associated AITasks

**Get Latest Full Schedule** (`GET /users/{user_id}/plans/latest-schedule`)
- Returns all plans from the latest generation
- Shows complete multi-day schedule
- Ordered by date
- Includes all AITasks for each plan

**Get Plan History** (`GET /users/{user_id}/plans/history`)
- Lists all generations with metadata
- Shows: generation_id, creation_date, plan_count, feedback_count
- Allows user to see previous schedule versions
- Ordered by creation date (newest first)

**Get Specific Plan** (`GET /users/{user_id}/plans/{plan_id}`)
- Returns single plan (one day)
- Includes: plan_date, notes, generation_id, creation_date
- Includes all associated AITasks
- Only accessible to plan owner

**Get Plan by Date** (`GET /users/{user_id}/plans/date/{plan_date}`)
- Returns plan for a specific date (format: YYYY-MM-DD)
- Returns only from latest generation
- If no plan exists for that date, returns 404

**Update Plan** (`PUT /users/{user_id}/plans/{plan_id}`)
- Request: `{ "notes": "..." }`
- Updates plan notes/metadata only
- Does not modify associated AITasks
- Only plan owner can update

**Delete Plan** (`DELETE /users/{user_id}/plans/{plan_id}`)
- Removes plan and cascades delete to all its AITasks
- Does not affect other plans in same generation
- Only plan owner can delete
- Feedback for this generation is preserved
