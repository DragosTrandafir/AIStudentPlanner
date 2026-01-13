# User Entity

Represents user accounts and profiles.

## Schema

| Column | Type | Constraints | Purpose |
|:---|:---|:---|:---|
| `id` | Integer | PK | Unique identifier |
| `name` | String(255) | NOT NULL | User's full name |
| `username` | String(255) | UNIQUE, NOT NULL | Unique username for login |
| `email` | String(255) | UNIQUE, NOT NULL | Unique email for login |
| `password` | String(255) | NOT NULL | Hashed password (bcrypt) |
| `major` | String(255) | Nullable | User's academic major |
| `google_id` | String(255) | UNIQUE, Nullable | Google OAuth ID |
| `created_at` | DateTime | NOT NULL, DEFAULT=UTC | Account creation timestamp |

## Example

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2026-01-12T10:00:00Z",
  "updated_at": "2026-01-12T10:00:00Z"
}
```

## Relationships

- One-to-Many: User → Subject
- One-to-Many: User → Plan
- One-to-Many: User → Feedback

## Key Properties

- Username and email are case-insensitive but stored as-is
- Password is never returned in API responses
- All timestamps are UTC
