# Subject Endpoints

Subject generation, retrieval, and management.

## Endpoints (5 total)

| Method | Endpoint | Description |
|:---|:---|:---|
| POST | `/users/{user_id}/subjects` | Create subject |
| GET | `/users/{user_id}/subjects` | List user's subjects |
| GET | `/users/{user_id}/subjects/{subject_id}` | Get subject details |
| PUT | `/users/{user_id}/subjects/{subject_id}` | Update subject |
| DELETE | `/users/{user_id}/subjects/{subject_id}` | Delete subject |

## Key Details

**Create Subject** (`POST /users/{user_id}/subjects`)
- Request: `{ "title": "...", "name": "...", "type": "WRITTEN|PRACTICAL|PROJECT", "difficulty": 1-5, "status": "NOT_STARTED|IN_PROGRESS|COMPLETED" }`
- Response: Created subject with id
- Type must be one of: WRITTEN, PRACTICAL, PROJECT
- Status defaults to NOT_STARTED
- Difficulty defaults to 1, ranges 1-5
- Optional: start_date, end_date, description
- Only user can create subjects for themselves

**List User Subjects** (`GET /users/{user_id}/subjects`)
- Returns all subjects for the authenticated user
- Shows: subject_id, title, name, type, status, difficulty, created_date
- Optional filters: `?type=WRITTEN`, `?status=IN_PROGRESS`
- Ordered by creation date (newest first)

**Get Subject Details** (`GET /users/{user_id}/subjects/{subject_id}`)
- Returns full subject information
- Includes: title, name, type, status, difficulty, start_date, end_date, description, created_date
- Shows associated AITasks that reference this subject
- Only accessible to subject owner

**Update Subject** (`PUT /users/{user_id}/subjects/{subject_id}`)
- Request: `{ "title": "...", "status": "...", "difficulty": ..., "description": "..." }`
- Update subject metadata: title, status, difficulty, description, dates
- Status must be one of: NOT_STARTED, IN_PROGRESS, COMPLETED
- Difficulty must be 1-5
- Only subject owner can update
- Does not affect existing AITasks referencing this subject

**Delete Subject** (`DELETE /users/{user_id}/subjects/{subject_id}`)
- Deletes subject and cascades delete to all AITasks referencing it
- Cascading deletes only affect AITasks, not Plans
- Only subject owner can delete
- This is a destructive operation (cascades to tasks)
