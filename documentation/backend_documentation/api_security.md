# API Interface & Security Model

The API follows RESTful standards and implements a stateless security model using JSON Web Tokens (JWT).

## 1. Authentication Mechanism
* **Standard:** OAuth2 with Password Flow.
* **Implementation Details:**
    1.  Client POSTs credentials to `/users/login`.
    2.  Server validates hash and issues a **Access Token**.
    3.  Token is signed using `HS256` algorithm and a server-side `SECRET_KEY`.
    4.  Client must attach header `Authorization: Bearer <token>` to all protected requests.

## 2. Authorization Strategy
The system implements a **Trust-Based Internal Authorization** model optimized for AI interaction.

### Strict Gatekeeping
The `get_current_user_id` dependency is injected into every protected route.
* It decodes the JWT.
* It verifies the expiration (`exp`).
* It extracts the User ID (`sub`).
* **Result:** Invalid or expired tokens are rejected immediately with `401 Unauthorized`.

### Resource Access & AI Trust
Once a user is authenticated via the API Gateway:
1.  **Ownership Check:** Critical routes (like deleting a user or accessing a subject) check `if requested_id == token_id`.
2.  **AI Orchestration Access:** The internal `AiOrchestrator` is trusted to access data for the authenticated user context. This design prevents "Service-to-Service" authentication complexity during the AI generation phase.

## 3. Error Handling Standard
The API implements global exception handling to provide consistent JSON responses:

* **400 Bad Request:** Logic violations (e.g., Duplicate Email, End Date < Start Date).
* **401 Unauthorized:** Missing/Invalid Token.
* **403 Forbidden:** Valid token, but user attempts to modify data they do not own.
* **404 Not Found:** Resource ID does not exist.
* **500 Internal Server Error:** Failures within the AI Orchestrator (caught and wrapped).