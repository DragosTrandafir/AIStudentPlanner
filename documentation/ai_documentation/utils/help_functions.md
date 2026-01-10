# Implementation Documentation: Core Utilities & LLM Logic

This document details the utility functions and prompt-generation logic within `ai_system.utils`. These components serve as the engine for the high-level agents, handling everything from raw LLM communication to complex prompt engineering.

---

## 1. LLM Communication: `make_llm_call`

The `make_llm_call` function is the centralized gateway for all model interactions. It is designed to be resilient, offering a fallback mechanism between different Hugging Face inference methods.

### Resilience Strategy
The function attempts to communicate with the model using two distinct methods to ensure high availability:

| Attempt | Method | Description |
| :--- | :--- | :--- |
| **Primary** | `chat_completion` | Uses the structured Chat API (`messages` list). Ideal for instructional following. |
| **Fallback** | `text_generation` | Uses the standard completion API. Triggered automatically if `chat_completion` fails or is unsupported. |

### Error Handling
* **Graceful Degradation**: If both methods fail, it logs the specific error to the console and returns the string: `"Could not complete response."`
* **Attribute Safety**: Uses `getattr` to safely extract content from the Chat Completion choice object.

---

## 2. Planning Logic: `propose_plan`

The `propose_plan` function is a specialized factory that assembles complex prompts based on the specific type of academic task and university subject.

### Prompt Configuration Map
The function uses a configuration mapping to pair **Task Types** (Practical, Written, Project, Assignment) with **Subject Domains** (CS, Math).



### Assembly Pipeline
The final prompt is built by joining five distinct segments to ensure the LLM has complete context:
1.  **Role Prompt**: Sets the persona (e.g., "You are a CS Professor").
2.  **General Heuristics**: Global rules for plan generation.
3.  **Specific Heuristics**: Domain-specific constraints (e.g., CS practical exam logic).
4.  **Input/Output Instructions**: Detailed task parameters (title, dates, difficulty).
5.  **Few-Shot Example**: A concrete example of the expected output format.

---

## 3. Scheduling & Feedback Logic

### `propose_calendar`
This utility acts as a bridge between high-level plans and a concrete timeline.
* **Input**: An array of generated plans and a reference `date`.
* **Output**: A raw string (intended to be JSON) representing a structured calendar.
* **Function**: It delegates prompt creation to `generate_calendar_instructions`.

### `propose_feedback_reschedule`
Handles the logic for adjusting existing schedules based on user progress.
* **State Management**: It takes three layers of data (`last_feedback`, `last_schedule`, `current_feedback`) to provide the LLM with a comprehensive view of the user's trajectory.
* **Context**: Incorporates the current `date` to ensure rescheduling occurs in the future, not the past.

---

## Summary Table: Utility Responsibilities

| Function | Primary Responsibility | Key Dependency |
| :--- | :--- | :--- |
| **`make_llm_call`** | API communication & Error Handling | `huggingface_hub.InferenceClient` |
| **`propose_plan`** | Multi-domain prompt assembly | `custom_agent_prompts` |
| **`propose_calendar`** | Temporal mapping of tasks | `calendar_generator_prompts` |
| **`propose_feedback_reschedule`** | Iterative schedule optimization | `feedback_generator_prompts` |

---

## Technical Constants & Flow
The system relies on a strict directory structure for prompt snippets:
* `utils/custom_agent_prompts/`: Contains subject-specific heuristics (CS vs. Math).
* `utils/feedback_generator_prompts/`: Instructions for rescheduling logic.
* `utils/calendar_generator_prompts/`: Logic for time-blocking and event creation.