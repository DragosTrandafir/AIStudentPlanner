# AI Orchestration Integration

A specific architectural pattern was implemented in `plan_routes.py` to facilitate communication between the stateless REST API and the heavy, synchronous AI Orchestrator.

## The Problem: Database Locking
The application uses SQLite for development. SQLite allows only one writer at a time.
1.  **The API Route** opens a DB Session to fetch user data.
2.  **The AI Orchestrator** (called inside the route) attempts to open a *new* DB Session to fetch the same data.
3.  **Result:** Deadlock / "Database is locked" error.

## The Solution: The "Session Sandwich" Pattern

To prevent the API Route and the AI Orchestrator from fighting over the database connection, the `generate_plan` endpoint follows a strict three-step execution flow:

### Phase 1: Data Pre-Fetch (Session A)
* **Action:** Open DB Session.
* **Logic:** Fetch User and Subject data using Repositories.
* **Transformation:** Convert SQLAlchemy models to pure Python Dictionaries (JSON-serializable).
* **CRITICAL:** Close DB Session immediately. (Lock Released).

### Phase 2: AI Execution (No Lock)
* **Action:** Initialize `AiOrchestrator`.
* **Injection:** We use a `DirectDataConnector` to inject the pre-fetched dictionaries into the AI.
* **Execution:** The AI performs heavy computation (LLM calls via HuggingFace) without holding any database connection open. This ensures the API remains responsive.

### Phase 3: Persistence (Session B)
* **Action:** Open a **New** DB Session.
* **Logic:** Receive JSON output from AI.
* **Mapping:** Map JSON entries to `Plan` and `AITask` database models.
* **Commit:** Save the generated schedule to the database.

## Direct Data Connector
A helper class (`DirectDataConnector`) acts as an adapter. It mocks the internal API calls the Orchestrator usually makes, allowing the AI logic to remain unchanged while optimizing performance within the backend.