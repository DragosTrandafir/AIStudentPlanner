# Implementation Documentation: Subject-Specific Agents

This document provides the technical specification and implementation details for the `CSAgent` and `MathAgent` classes. These agents are designed to generate structured academic plans using Large Language Models (LLMs) via the Hugging Face Hub.

---

## Overview

The agents are specialized components within the `ai_system` architecture. They leverage a shared base class and a centralized logic utility to ensure consistency while maintaining domain-specific focuses.



---

## Class Definitions

### 1. `CSAgent`
The `CSAgent` is responsible for generating plans related to **Computer Science**. 

* **Logic**: It passes the string `"Computer Science"` as the domain identifier to the underlying logic utility.
* **Usage**: Ideal for curriculum development, coding project roadmaps, and technical skill assessments.

### 2. `MathAgent`
The `MathAgent` is responsible for generating plans related to **Mathematics**.

* **Logic**: It passes the string `"Mathematics"` as the domain identifier.
* **Usage**: Ideal for theorem exploration, pedagogical sequences, and mathematical modeling plans.

---

## Core Method: `propose_agent_plan`

Both agents implement the `propose_agent_plan` method. This method follows a specific execution pipeline:

### Execution Pipeline

| Step | Action | Description |
| :--- | :--- | :--- |
| **1** | **Client Init** | Initializes an `InferenceClient` using the agent's internal `model` and `token`. |
| **2** | **Utility Call** | Calls the `propose_plan` function with the subject data and domain name. |
| **3** | **Parsing** | Attempts to convert the model's string response into a Python dictionary. |
| **4** | **Fallback** | If JSON parsing fails, returns the raw text in a structured dictionary. |

---

## Technical Implementation

The implementation utilizes the `huggingface_hub` library for model interaction and the `json` library for data structured handling.

### Implementation Logic Snippet

```python
# Common logic shared by both agents
client = InferenceClient(model=self.model, token=self.token)
response = propose_plan(subject_data, "Subject Name", client)

try:
    return json.loads(response)  # Success: returns structured data
except json.JSONDecodeError:
    return {"raw_response": response}  # Error: returns raw string
```

## Dependencies

- json: Standard library for data parsing.

- huggingface_hub.InferenceClient: Used for API-based LLM inference.

- ai_system.agents.base_agent: The parent class providing configuration.

- ai_system.utils.propose_plan_logic: The core prompt-engineering utility.