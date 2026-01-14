# Technologies and Frameworks - AI Student Planner

---

# FRAMEWORKS

## 1. Frontend Frameworks

### Web Framework & UI Library
- **Next.js 16.0.1** - Web framework (SSR, SSG, automatic code splitting)
- **React 19.2.0** - UI library

### Styling Framework
- **Tailwind CSS 4.1.17** - Utility-first CSS framework (rapid UI development, pre-built utility classes)

### Calendar Framework
- **FullCalendar 6.1.19** - Calendar component (multiple view options: day grid, week, month)

---

## 2. Backend Framework

### Web Framework
- **FastAPI 0.104.0+** - Web framework (async/await, 100+ requests/second, auto OpenAPI docs)

### ORM Framework
- **SQLAlchemy 2.0.0+** - ORM framework (database-agnostic, relationship management, migrations)

### Data Validation Framework
- **Pydantic 2.0.0+** - Data validation framework (automatic validation, type-safe contracts)

---

## 3. AI Framework

### Multi-Agent System
- **Multi-Agent Architecture (Custom)** - Orchestrates specialized AI agents (Math Agent, CS Agent, General Agent, Feedback Agent) with parallel execution via ThreadPoolExecutor

---

# TECHNOLOGIES

## 1. Frontend Technologies

### Language & Runtime
- **TypeScript 5** - Type safety, IDE support
- **Node.js** - JavaScript runtime

### UI Component Libraries
- **@headlessui/react 2.2.9** - Accessible React components
- **@heroicons/react 2.2.0** - SVG icons
- **lucide-react 0.553.0** - Icon library

### Calendar & Date Libraries
- **date-fns 4.1.0** - Date utilities
- **react-date-range 2.0.1** - Date range picker
- **react-datepicker 8.8.0** - Date picker

### Modal & Interaction Libraries
- **react-modal 3.16.3** - Modal component

### Development Tools
- **ESLint 9** - Code linting
- **eslint-config-next** - Next.js linting config
- **PostCSS 4** - CSS post-processor

---

## 2. Backend Technologies

### Language & Runtime
- **Python** - Backend language

### Web Server
- **Uvicorn 0.24.0+** - ASGI server (async, production-ready)

### Databases
- **SQLite** - Development database (file-based)
- **PostgreSQL** - Production database (ACID, scalable)

### Security & Authentication
- **python-jose[cryptography]** - JWT implementation
- **bcrypt 4.0.1** - Password hashing
- **passlib[bcrypt]** - Password verification

### HTTP & API
- **requests 2.32.5+** - HTTP client
- **CORS Middleware** - Cross-origin support

### Configuration & Environment
- **python-dotenv 1.2.1+** - Environment variables
- **dotenv 0.9.9** - Environment config

### Data Validation
- **email-validator 2.0.0+** - Email validation

---

## 3. AI System Technologies

### LLM & Inference
- **HuggingFace Hub 1.0.1+** - Model repository and inference API
- **openai/gpt-oss-20b** - Open-source LLM (custom agent model; balance between performance and resources)

---

## 4. Development & DevOps Technologies

### Version Control
- **Git** - Version control
- **GitHub** - Repository hosting and collaboration

### Package Management
- **npm/pnpm** - Frontend package manager
- **pip** - Python package manager

### Build & Compilation
- **Next.js Build Tools** - Frontend build system (bundling, minification)
- **TypeScript Compiler** - TypeScript transpilation and type checking

### Environment Management
- **.env Files** - Environment configuration (API keys, DB URLs, model selection)

---

## 5. Database Schema & Data Models

**Entities:**
- **Users** - Student accounts with authentication credentials
- **Subjects** - Academic subjects/courses with difficulty ratings (1-5 scale)
- **Plans** - Calendar days with generated study schedules (grouped by generation_id)
- **AITasks** - Individual study tasks scheduled for specific time slots
- **Feedbacks** - User feedback with rating scores and comments (tied to generation_id)

### Database Schema Diagram

```
                                          USER
                    ┌───────────────┬───────────────┬───────────────┐
                    │               │               │               │
                 (1:N)           (1:N)            (1:N)            (1:N)
                    │               │               │               │
                    ▼               ▼               ▼               ▼
              SUBJECT              PLAN             FEEDBACK          AITASK
              ────────             ────             ────────          ──────
              id (PK)              id (PK)          id (PK)           id (PK)
              title                user_id(FK→User) user_id(FK→User)  time_allotted
              name                 plan_date        generation_id     ai_task_name
              type (E)             notes            rating            difficulty
              status (E)           generation_id    comments          priority
              difficulty           created_at       created_at        plan_id(FK→Plan)
              start_date           updated_at                         task_id(FK→Subject)
              end_date                                                
              description                                             
              student_id(FK→User)
              created_at

Entity Relationships:
- User → Plan (1:N)
- User → Subject (1:N)
- User → Feedback (1:N)
- Plan → AITask (1:N)
- Subject → AITask (1:N)

All relationships have CASCADE DELETE configured.
Note: generation_id (UUID) in Plan entity groups multiple related Plans for each schedule generation.
This is NOT a foreign key to a separate entity, but rather a logical grouping mechanism.
```

---

## 6. Summary by Layer

### Frontend

| Component | Type | Version |
|-----------|------|---------|
| Next.js | Framework | 16.0.1 |
| React | Framework | 19.2.0 |
| TypeScript | Technology | 5 |
| Tailwind CSS | Framework | 4.1.17 |
| FullCalendar | Framework | 6.1.19 |
| date-fns | Technology | 4.1.0 |
| ESLint | Technology | 9 |
| PostCSS | Technology | 4 |

### Backend

| Component | Type | Version |
|-----------|------|---------|
| FastAPI | Framework | 0.104.0+ |
| SQLAlchemy | Framework | 2.0.0+ |
| Pydantic | Framework | 2.0.0+ |
| Uvicorn | Technology | 0.24.0+ |
| Python | Technology | - |
| bcrypt | Technology | 4.0.1 |
| python-jose | Technology | - |
| python-dotenv | Technology | 1.2.1+ |
| email-validator | Technology | 2.0.0+ |

### Database

| Component | Type | Purpose |
|-----------|------|---------|
| SQLite | Technology | Development (file-based) |
| PostgreSQL | Technology | Production (ACID, scalable) |
| SQLAlchemy ORM | Framework | Database abstraction |

### AI System

| Component | Type | Details |
|-----------|------|---------|
| Multi-Agent Architecture | Framework | Math, CS, General, Feedback agents |
| HuggingFace Hub | Technology | 1.0.1+ |
| openai/gpt-oss-20b | Technology | 20B parameter model |

### DevOps & Tools

| Component | Purpose |
|-----------|---------|
| Git | Version control |
| GitHub | Repository hosting |
| npm/pnpm | Frontend packages |
| pip | Python packages |
| Next.js Build Tools | Bundling & optimization |
| TypeScript Compiler | Type checking & transpilation |
| .env Files | Configuration management |
