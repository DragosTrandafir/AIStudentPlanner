# Backend Architecture Overview

![](documentation/Architecture diagram/architecture.png)

## System Abstract
The Backend serves as the **Single Source of Truth** for the AI Student Planner. It acts as the mediator between the React Frontend and the AI Orchestration layer.

## Technology Stack
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (High-performance, async-ready Python web framework)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (Database abstraction and SQL toolkit)
* **Validation:** [Pydantic](https://docs.pydantic.dev/) (Data schema enforcement and serialization)
* **Security:** OAuth2 with JWT (JSON Web Tokens) & Bcrypt password hashing.
* **Database:** SQLite (Development) / PostgreSQL (Production ready).

## Architectural Pattern: CSR (Controller-Service-Repository)
The application follows a strict separation of concerns to ensure maintainability and testability:

1.  **Controller/Router Layer (`/routes`)**:
    * Handles HTTP Requests/Responses.
    * Manages Authentication/Authorization dependencies.
    * **No business logic allowed here.**

2.  **Service Layer (`/service`)**:
    * Contains the core business rules (e.g., "Start date must be before End date").
    * Orchestrates multiple repositories if needed.
    * Agnostic of the HTTP context (doesn't know about JSON or HTML).

3.  **Repository Layer (`/repository`)**:
    * Direct interface with the Database.
    * Executes CRUD (Create, Read, Update, Delete) operations.
    * Maps SQL rows to Python Objects.

4.  **Domain Layer (`/domain`)**:
    * Defines the core business objects (entities and value objects) that map to database tables.
    * Encapsulates business rules directly on the data they belong to.
    * Independent of HTTP and infrastructure concerns.
    * Used by repositories to persist and load data.