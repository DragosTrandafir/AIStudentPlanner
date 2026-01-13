# Backend Flow Overview

-------- User Authentication & Profile --------

1️⃣ Frontend sends username/password -> Backend Auth Endpoint

2️⃣ Backend:
- Validates credentials (bcrypt hash comparison)
- Creates JWT token
- Returns token to Frontend

3️⃣ Frontend stores token for future requests

-------- Initial Schedule Generation --------

1️⃣ Frontend sends user subjects + exam dates -> Backend `/plans/generate` endpoint

2️⃣ Backend:
- Validates user exists & subjects exist
- Validates input format
- Creates `generation_id` (UUID) to track this generation

3️⃣ Backend invokes AI System (via AiOrchestrator):
- Sends user data to AI System
- AI System processes and returns optimized schedule
- (See [ai_documentation/orchestator/ai_orchestrator.md](../../ai_documentation/orchestator/ai_orchestrator.md) for AI processing details)

4️⃣ Backend validates & stores results:
- Validates response has expected `{"calendar": [...]}` structure
- Stores Plan records (one per day)
- Stores AITask records (individual tasks)
- Links all records with same `generation_id`

5️⃣ Backend returns GeneratedPlanResponse to Frontend

-------- Reschedule with Feedback --------

1️⃣ User submits feedback (rating [1-5] + comments) -> Backend `/feedback` endpoint

2️⃣ Backend (Feedback):
- Validates user exists
- Validates rating is in range [1,5]
- Prevents duplicate feedback for same generation
- Stores feedback record

3️⃣ User requests reschedule -> Backend `/plans/reschedule` endpoint

4️⃣ Backend (Reschedule):
- Validates user exists & subjects exist
- Validates input format
- Retrieves context: last feedback, current feedback, latest schedule from database

5️⃣ Backend invokes AI System (via AiRescheduler):
- Sends context (previous plan + feedback) to AI System
- AI System processes and returns refined schedule
- (See [ai_documentation/orchestator/ai_reschedule.md](../../ai_documentation/orchestator/ai_reschedule.md) for AI rescheduling logic)

6️⃣ Backend validates & stores results:
- Validates response has expected `{"calendar": [...]}` structure (raises 400/500 if invalid)
- Creates new `generation_id` for this refined schedule
- Stores Plan & AITask records (refined schedule)
- Previous generation remains in database (history preserved)

7️⃣ Backend returns GeneratedPlanResponse to Frontend

-------- Data Persistence --------

- **User**: Registration, authentication, profile
- **Subject**: User's courses/exams
- **Plan**: Daily schedule (grouped by `generation_id`)
- **AITask**: Individual tasks within plans
- **Feedback**: User ratings/comments for schedules

All user data is isolated - users can only access their own schedules, tasks, feedback.

-------- Detailed Documentation --------

See dedicated folders for backend-specific details:
- `api_endpoints/` - REST endpoint specifications (one file per entity)
- `authentication/` - JWT & access control details
- `data_models/` - Entity schemas (one file per entity)
- `ai_integration/` - Backend-AI System handoff points and communication
- `error_handling/` - Validation layers and HTTP status codes

AI System internals (orchestrator logic, agent processing, prompt engineering) are documented in [ai_documentation/](../../ai_documentation/) folder.
