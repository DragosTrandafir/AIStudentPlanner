# Implementation Documentation: AI Prompt Engineering & Heuristics

This document outlines the prompt structures and pedagogical heuristics used to guide the Large Language Models (LLMs) in generating accurate, student-friendly academic plans and schedules.

---

## 1. The Calendar Master Prompt (`CalendarMaster-AI`)

The `generate_calendar_instructions` function creates a high-pressure, deterministic persona responsible for merging multiple agent plans into a single timeline.

### Core Scheduling Constraints
The model is governed by "Essential Constraints" to ensure physical and mental feasibility:
* **Buffer Zones**: Tasks must end $\geq 2$ hours before a deadline and start $\geq 4$ hours after a reference point.
* **Block Limits**: No single study block exceeds 2 hours; tasks longer than this must be split.
* **Break Logic**: 20–30 minute breaks are required after every 2 hours (implicitly handled in time ranges).
* **Workload**: 10–12 hours max per day, primarily between 08:00–22:00.

### Time Pressure Mode
If a deadline is mathematically impossible to meet under normal rules, the prompt allows for:
* Reduced sleep windows.
* "Shallower" coverage of topics (prioritizing breadth over depth).
* Late-night sessions (00:00–06:00).

---

## 2. Subject-Specific Heuristics (CS vs. Math)

The system uses specific estimation rules to ensure that "Practical Exams," "Written Exams," and "Projects" have realistic hour allocations.

### Computer Science (CS) Heuristics
| Task Type | Key Heuristic | Estimated Total Hours |
| :--- | :--- | :--- |
| **Practical Exam** | Focus on Lab/Seminar review and algorithm practice. | 9–12 Hours |
| **Written Exam** | Heavy focus on Lecture review (7–8h) and model solving. | 12–17 Hours |
| **Project** | Focus on Architecture (1h) and Coding (2–4h). Documentation is capped at 1h. | Variable (e.g., 6h) |

### Mathematics Heuristics
| Task Type | Key Heuristic | Estimated Total Hours |
| :--- | :--- | :--- |
| **Practical Exam** | Focused lab review and model solving. | 4–6 Hours |
| **Written Exam** | Intensive seminar and proof review (5–8h). | 15–20 Hours |
| **Project** | Theoretical development and proof writing. | ~5 Hours |

---

## 3. Feedback & Refinement (`CalendarRefiner-AI`)

The `generate_feedback_instructions` function handles iterative updates. It treats user feedback as a **preference** while maintaining the "Global Scheduling Laws."

### The Refinement Logic
1.  **Baseline**: Accepts the `last_schedule` as the current state.
2.  **Context**: Analyzes `last_feedback` (history) vs. `current_feedback` (new request).
3.  **Conflict Resolution**: If user feedback violates a law (e.g., "I want to study 20 hours today"), the agent is instructed to prioritize the **Global Laws** over the user preference to prevent burnout.

---

## 4. Technical Prompt Construction

All prompts are built using a modular approach through these helper functions:

### General Components
* **`get_role_prompt`**: Sets the persona based on the university type.
* **`get_general_heuristics_header`**: Enforces universal rules (e.g., "Total hours must equal the sum of subtasks").
* **`get_input_output_instructions`**: Defines the strict JSON schema to prevent "chatter" or markdown formatting in the LLM response.

### JSON Schema Enforcement
The models are strictly instructed to output a valid JSON object:
```json
{
  "summary": "Overview string",
  "subject_name/project_name": "String",
  "total_estimated_hours": 10,
  "difficulty": 3,
  "tasks": [
    { "task_name": "Part 1", "estimated_hours": 2, "priority": 1 }
  ],
  "deadline": "ISO-8601-Timestamp"
}
```

## 5. Implementation Notes

- Determinism: The prompts use phrases like "STRICTLY adhere" and "Do NOT produce explanations" to minimize tokens and parsing errors.

- Priority Logic: Priorities are strictly sequential (1, 2, 3...) and unique within a single day.

- Task Splitting: The logic enforces naming conventions for split tasks, such as Task Name (part 1).