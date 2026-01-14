# Authentication Security Documentation

## 1. Security Overview
This implementation handles user identity through secure password hashing and stateless **JWT** (JSON Web Token) authentication.



### Password Hashing
* **Algorithm:** `bcrypt` via Passlib.
* **Logic:** Passwords are salted and hashed before database insertion. Plaintext is never stored.
* **Verification:** Uses `pwd_context.verify` to prevent timing attacks during login.



### JWT Configuration
* **Algorithm:** `HS256`.
* **Expiration:** 60 minutes.
* **Identifier:** User ID is stored in the `sub` (subject) claim of the token.

---

## 2. Implementation Flow

### Registration & Login
1.  **User Creation:** `get_password_hash()` is called in the route before saving to the DB.
2.  **Login:** `UserService.login_user()` validates credentials.
3.  **Token Issuance:** `create_access_token()` generates a signed JWT for the client.

### Route Protection
The `get_current_user_id` dependency acts as a security guard:
* Extracts the **Bearer Token** from the Authorization header.
* Decodes and validates the token signature using the `SECRET_KEY`.
* Injects the authenticated `user_id` directly into the route function.

---

## 3. Best Practices Applied
* **Statelessness:** No session data is stored on the server.
* **Dependency Injection:** Route protection is reusable and decoupled from business logic.
* **Integrity:** Unique constraints on `email`, `username`, and `google_id` prevent account shadowing.

---

## 4. Environment Requirements
* **SECRET_KEY:** Must be a 32-byte hex string in production.
* **HTTPS:** Required to protect tokens from man-in-the-middle (MITM) attacks.