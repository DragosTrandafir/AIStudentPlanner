# Task Endpoints

Individual task generation, retrieval, and management within plans.

## Endpoints (5 total)

| Method | Endpoint | Description |
|:---|:---|:---|
| POST | `/plans/{plan_id}/ai-tasks` | Create task |
| GET | `/plans/{plan_id}/ai-tasks` | List tasks in plan |
| GET | `/plans/{plan_id}/ai-tasks/{ai_task_id}` | Get specific task |
| PATCH | `/plans/{plan_id}/ai-tasks/{ai_task_id}` | Update task (partial) |
| DELETE | `/plans/{plan_id}/ai-tasks/{ai_task_id}` | Delete task |

## Key Details

**Create Task** (`POST /plans/{plan_id}/ai-tasks`)
- Request: `{ "ai_task_name": "...", "time_allotted": "HH:MM-HH:MM", "difficulty": 1-5, "priority": 1-10, "task_id": ... }`
- Response: Created AITask with id
- Difficulty must be 1-5, priority must be 1-10
- task_id references the Subject being worked on
- time_allotted is a time range (e.g., "08:00-10:00")
- Only plan owner can create tasks in their plan

**List Tasks in Plan** (`GET /plans/{plan_id}/ai-tasks`)
- Returns all AITasks for a specific plan
- Includes: task_id, ai_task_name, time_allotted, difficulty, priority, subject_name
- Ordered by time_allotted (earliest first)
- Only accessible to plan owner

**Get Specific Task** (`GET /plans/{plan_id}/ai-tasks/{ai_task_id}`)
- Returns full task details
- Includes: associated plan date, subject info, creation date
- Only accessible to task owner

**Update Task** (`PATCH /plans/{plan_id}/ai-tasks/{ai_task_id}`)
- Partial update: `{ "difficulty": ..., "priority": ..., "time_allotted": "..." }`
- Update difficulty (1-5), priority (1-10), or time allocation
- Validation enforced at service layer
- Only task owner can update
- Does not affect other tasks in same plan

**Delete Task** (`DELETE /plans/{plan_id}/ai-tasks/{ai_task_id}`)
- Removes task from plan
- Does not affect the Subject being referenced
- Does not affect other tasks in same plan
- Only task owner can delete
