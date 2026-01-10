# Implementation Documentation: Scheduling & Feedback Agents

This document details the technical implementation of the `CalendarAgent` and `FeedbackAgent`. These agents focus on temporal organization and iterative plan adjustment based on user feedback.

---

## Overview

While subject agents focus on content generation, the Scheduling and Feedback agents manage the **temporal execution** of those plans. They handle the conversion of academic concepts into actionable calendar events and the rescheduling of tasks based on performance feedback.



---

## Class Definitions

### 1. `CalendarAgent`
The `CalendarAgent` is designed to transform high-level study plans into a chronological schedule.

* **Initialization**: Requires a specific `date` context to establish the timeline.
* **Method**: `propose_agent_plan(plans)`
* **Core Logic**: Utilizes the `propose_calendar` utility to map plan items to specific time slots relative to the provided `self.date`.

### 2. `FeedbackAgent`
The `FeedbackAgent` acts as an iterative optimizer. It analyzes past performance and current feedback to suggest schedule adjustments.

* **Initialization**: Requires a `datetime` object representing the "current" reference point.
* **Method**: `propose_agent_plan(context)`
* **Context Extraction**: Processes a dictionary containing:
    * `last_feedback`: Given by the user in the last iteration (can miss).
    * `last_schedule`: The previous iteration of the calendar.
    * `current_feedback`: New input given by the user.

---

## Technical Specifications

### Input/Output Schema

| Agent | Input Parameter | Primary Utility | Expected Output |
| :--- | :--- | :--- | :--- |
| **CalendarAgent** | `plans` (List/Dict) | `propose_calendar` | JSON Calendar Object |
| **FeedbackAgent** | `context` (Dict) | `propose_feedback_reschedule` | JSON Rescheduled Plan |

### Logic Implementation

Both agents follow a robust inference pattern:

1.  **Client Setup**: A `huggingface_hub.InferenceClient` is instantiated per request.
2.  **State Management**: `FeedbackAgent` specifically extracts three distinct layers of state (last feedback, last schedule, and current feedback) to provide the LLM with full context.
3.  **Resilient Parsing**:
    ```python
    try:
        return json.loads(response) 
    except json.JSONDecodeError:
        return {"raw_response": response}
    ```

---

## Data Flow: Feedback & Rescheduling

The `FeedbackAgent` logic facilitates a continuous improvement loop:

1.  **Input**: The agent receives the `context` dictionary.
2.  **Analysis**: The `propose_feedback_reschedule` utility compares "what was planned" vs. "what was achieved."
3.  **Output**: The agent returns a new JSON structure that updates the user's trajectory, which can then be fed back into a `CalendarAgent` for updated time-blocking.



---

## Error Handling

As with the subject agents, these classes implement a fallback mechanism. Since scheduling data is highly structural, a `json.JSONDecodeError` is caught to prevent the system from crashing if the LLM provides a natural language explanation instead of a raw JSON array.

---

## Dependencies
* `datetime`: For precise temporal calculations.
* `typing`: For strict type hinting (`List`, `Dict`, `Any`).
* `huggingface_hub`: For LLM communication.
* `ai_system.utils`: For specialized prompt-logic functions.