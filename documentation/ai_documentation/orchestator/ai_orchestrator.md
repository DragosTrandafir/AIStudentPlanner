# AI Orchestration System: Implementation Documentation

This document serves as the complete technical reference for the AI-driven academic planning system. It details the interaction between the Orchestrator, specialized Domain Agents, Prompt Heuristics, and the Backend API.

---

## 1. System Architecture & Orchestration
The `AiOrchestrator` is the central hub. It manages parallel task execution and routes academic subjects to the appropriate AI experts.

### Key Features
* **Parallel Processing**: Uses `ThreadPoolExecutor` to handle multiple task analyses simultaneously, significantly reducing latency.
* **Intelligent Routing**: Uses keyword analysis to distinguish between Mathematics/Physics tasks and Computer Science tasks.
* **Resilience**: Features a "Soft Fail" mechanism that uses mock data if the Backend API is unreachable.



---

## 2. Agent Definitions
The system utilizes specialized agents that inherit from a `BaseAgent` class. Each agent is responsible for a specific stage of the planning lifecycle.

| Agent Class | Responsibility | Core Logic |
| :--- | :--- | :--- |
| **`CSAgent`** | Analyzes Computer Science tasks. | Applies coding & architecture heuristics. |
| **`MathAgent`** | Analyzes Mathematics/Physics tasks. | Applies proof & theoretical heuristics. |
| **`CalendarAgent`** | Synthesizes plans into a schedule. | Merges task analyses into a daily timeline. |
| **`FeedbackAgent`** | Iterative schedule refinement. | Adjusts calendars based on user performance. |

---

## 3. Prompt Engineering & Heuristics
The system's accuracy relies on domain-specific rules (heuristics) that guide the LLM's estimations.

### Computer Science vs. Mathematics Heuristics
* **CS Projects**: Focus on Implementation (2–4h) and Testing; Documentation is strictly capped at 1h.
* **Math Written Exams**: Heavy focus on Seminar review (5–8h) and proof-solving (15–20h total).
* **Practical Exams**: CS focuses on lab review (3h) and algorithms; Math focuses on model solving (3h).

### The CalendarMaster-AI Persona
The synthesis prompt enforces "Global Scheduling Laws":
* **Buffer Zones**: No tasks 2h before a deadline or 4h after a start date.
* **Human Limits**: Max 10–12h work/day; mandatory 20m breaks every 2h.
* **Task Splitting**: No single block exceeds 2h; longer tasks are split into `(part 1)`, `(part 2)`.



---

## 4. Core Utilities & LLM Logic
The `utils` layer handles the technical communication with Hugging Face and the construction of complex prompts.

### `make_llm_call`
A resilient wrapper that ensures high availability:
1.  **Primary**: Tries `chat_completion` (structured instructions).
2.  **Fallback**: Tries `text_generation` if the chat API is unavailable.

### `propose_plan`
A factory function that assembles a 5-part prompt:
`Role` + `General Heuristics` + `Domain Heuristics` + `Task Data` + `Few-Shot Example`.

---

## 5. Backend Integration (`BackendAPI`)
The system bridges the AI logic with a FastAPI backend using a mapping layer.

* **Data Translation**: Converts DB records into the "Orchestrator Format" (e.g., mapping `SubjectResponse` to `TaskInput`).
* **Feedback Sync**: Retrieves the last two feedback entries to allow the `FeedbackAgent` to perform comparative analysis.
* **Schedule Recovery**: Reconstructs the existing calendar from the database to provide a baseline for rescheduling.

---

## 6. Technical Specifications

### Environmental Variables (ask for the .env file)

- HF_TOKEN_1=your_token_for_domain_agents
- HF_TOKEN_2=your_token_for_calendar_synthesis
- CUSTOM_AGENT_MODEL=openai/gpt-oss-20b
- CALENDAR_AGENT_MODEL=openai/gpt-oss-20b
- BACKEND_BASE_URL=http://localhost:8000