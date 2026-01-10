# AI Orchestration System: Full Implementation Documentation

This document serves as the comprehensive technical reference for the academic planning system. It covers the architecture, the specialized agent logic, prompt engineering heuristics, and the integration layer.

---

## 1. System Overview
The system is designed to transform abstract academic tasks into concrete, day-by-day study schedules. It utilizes a multi-agent approach where domain experts (Math/CS) analyze content and a central orchestrator/rescheduler manages the workflow.



---

## 2. Orchestration Layer

### 2.1 AI Orchestrator (`AiOrchestrator`)
The "brain" of the system. It handles multi-tasking and parallelizes LLM calls.
* **Agent Routing**: Uses a keyword-based system (e.g., "pde", "calculus", "physics" for Math; "oop", "algorithms" for CS).
* **Parallel Execution**: Uses `ThreadPoolExecutor` to process individual tasks simultaneously.
* **Failover**: Injects mock data if the backend is unreachable.

### 2.2 AI Rescheduler (`AiRescheduler`)
The "feedback loop" controller.
* **Purpose**: Modifies existing calendars based on user feedback.
* **Context Assembly**: Aggregates `last_feedback`, `last_schedule`, and `current_feedback` into a single state for the `FeedbackAgent`.

---

## 3. Specialized Agents

### 3.1 Domain Agents (`CSAgent` & `MathAgent`)
These agents inherit from `BaseAgent` and focus on specific academic disciplines.
* **CSAgent**: Specialized in coding, architecture, and technical projects.
* **MathAgent**: Specialized in proofs, theoretical development, and physics-based modeling.

### 3.2 Synthesis Agents (`CalendarAgent` & `FeedbackAgent`)
* **CalendarAgent**: Merges multiple individual task plans into a single, conflict-free JSON calendar.
* **FeedbackAgent**: Analyzes past vs. present performance to suggest realistic schedule shifts.

---

## 4. Prompt Engineering & Heuristics

### 4.1 Global Scheduling Laws
The system adheres to strict pedagogical and physical constraints:
* **Buffer Zones**: Tasks must finish $\geq 2$ hours before a deadline.
* **Study Blocks**: No block exceeds 2 hours; 20-30 min breaks are mandatory between blocks.
* **Time Pressure Mode**: Allows reduced sleep or shallower coverage only if deadlines are at risk.

### 4.2 Discipline Heuristics
| Discipline | Practical Exam | Written Exam | Project |
| :--- | :--- | :--- | :--- |
| **Computer Science** | 9–12h (Labs/Seminars) | 12–17h (Lectures) | Implementation-heavy; 1h cap on docs. |
| **Mathematics** | 4–6h (Lab review) | 15–20h (Proofs/Seminars) | Proof-heavy; topic review focus. |

---

## 5. Core Utilities & Logic

### 5.1 Communication Wrapper (`make_llm_call`)
Provides resilience via a fallback mechanism:
1. **Primary**: `chat_completion` (for structured instruction following).
2. **Fallback**: `text_generation` (standard completion).

### 5.2 Plan Construction (`propose_plan`)
Constructs a 5-part modular prompt:
`Role` + `General Rules` + `Discipline Heuristics` + `Input Data` + `Few-Shot Example`.

---

## 6. Backend Integration (`BackendAPI`)
A mapping layer that synchronizes the AI system with the FastAPI database.
* **Data Mapping**: Translates DB models (e.g., `SubjectResponse`) into AI-readable Task dictionaries.
* **State Recovery**: Fetches historical feedback and the latest active schedule to provide context for rescheduling.



---

## 7. Technical Specifications

### Environmental Variables

- same as those in ai_orchestrator