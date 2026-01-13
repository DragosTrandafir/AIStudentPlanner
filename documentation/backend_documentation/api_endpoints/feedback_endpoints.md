# Feedback Endpoints

User feedback submission and retrieval.

## Endpoints (3 total)

| Method | Endpoint | Description |
|:---|:---|:---|
| POST | `/users/{user_id}/feedback` | Submit feedback for current generation |
| GET | `/users/{user_id}/feedback/history` | Get feedback history |
| GET | `/users/{user_id}/feedback/latest` | Get last 2 feedbacks |

## Key Details

**Submit Feedback** (`POST /users/{user_id}/feedback`)
- Request: `{ "generation_id": "...", "rating": 1-5, "comments": "..." }`
- Response: Created feedback record with id
- Rating must be 1-5 (service-level validation)
- Comments field is optional
- Only one feedback allowed per (user, generation_id) pair
- Used by `/plans/reschedule` to trigger AI Rescheduler
- Returns: feedback_id, user_id, generation_id, rating, created_date

**Get Feedback History** (`GET /users/{user_id}/feedback/history`)
- Returns all feedback submitted by user
- Shows: feedback_id, generation_id, rating, comments, created_date
- Ordered by date (newest first)
- Includes feedback from all generations
- Useful for tracking user satisfaction trends

**Get Latest Feedbacks** (`GET /users/{user_id}/feedback/latest`)
- Returns last 2 feedback records submitted by user
- Shows: feedback_id, generation_id, rating, comments, created_date
- Useful for checking most recent feedback before regeneration
- Ordered by creation date (newest first)
