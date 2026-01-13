# User Endpoints

User authentication, registration, and profile management.

## Endpoints (6 total)

| Method | Endpoint | Description |
|:---|:---|:---|
| POST | `/users/login` | User login - returns JWT token |
| POST | `/users` | Create new user account |
| GET | `/users` | List all users |
| GET | `/users/{user_id}` | Get user profile |
| PUT | `/users/{user_id}` | Update user profile |
| DELETE | `/users/{user_id}` | Delete user account |

## Key Details

**Login** (`POST /users/login`)
- Request: `{ "email": "...", "password": "..." }`
- Response: `{ "access_token": "...", "token_type": "bearer" }`
- JWT token used in Authorization header for subsequent requests
- Token includes user_id and expiration
- Invalid credentials return 401 Unauthorized

**Create User** (`POST /users`)
- Request: `{ "email": "...", "password": "..." }`
- Response: `{ "id": ..., "email": "...", "created_at": "..." }`
- Email must be unique (enforced at DB level)
- Password is hashed with bcrypt before storage
- Returns 400 if email already exists

**List All Users** (`GET /users`)
- Returns all user accounts in system
- Shows: user_id, email, created_date
- May require admin role (check implementation)

**Get User Profile** (`GET /users/{user_id}`)
- Returns user info: id, email, created_date
- Only accessible by the user themselves or admin
- Returns 403 Forbidden if not authorized

**Update User Profile** (`PUT /users/{user_id}`)
- Request: `{ "email": "...", "password": "..." }`
- Update email and/or password
- Requires valid JWT token for the user
- New email must be unique if changed
- Password is hashed before storage
- Returns 403 if user is not authorized

**Delete User Account** (`DELETE /users/{user_id}`)
- Deletes user and cascades to all plans, subjects, and feedback
- Requires valid JWT token for the user
- Returns 403 if user is not authorized
- This is a destructive operation and cannot be undone
