import json
from datetime import datetime
from typing import Any, Dict, List, Tuple

from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils.propose_feedback_reschule_logic import (
    propose_feedback_reschedule,
    extract_forbidden_windows,
    enforce_schedule_constraints,
)
from ai_system.utils.llm_json import extract_json_from_llm


class FeedbackAgent(BaseAgent):
    def __init__(self, token: str, model: str, date: datetime):
        super().__init__(token, model)
        self.date = date  # datetime representing "today" for this agent

    def propose_agent_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point:
        - Builds prompt and calls LLM.
        - Parses JSON.
        - Enforces hard constraints (forbidden windows, priorities).
        - Normalizes the summary so it reflects the actual forbidden windows.
        """
        client = InferenceClient(model=self.model, token=self.token)

        current_feedback: Dict[str, Any] = context.get("current_feedback", {}) or {}
        last_feedback: Dict[str, Any] = context.get("last_feedback", {}) or {}
        last_schedule: Dict[str, Any] = context.get("last_schedule", {}) or {}

        # 1) Call LLM
        response_text = propose_feedback_reschedule(
            self.date,
            client,
            current_feedback,
            last_feedback,
            last_schedule,
        )

        # 2) Try to parse JSON from the LLM output
        try:
            plan = extract_json_from_llm(response_text)
        except Exception as e:
            # If JSON is invalid, return error payload with raw text for debugging.
            return {
                "summary": "LLM returned invalid JSON",
                "error": str(e),
                "raw_response": response_text,
            }

        # 3) Enforce constraints locally for guaranteed correctness
        feedback_text = current_feedback.get("text", "") or ""
        forbidden_windows = extract_forbidden_windows(feedback_text)

        plan = enforce_schedule_constraints(
            plan,
            forbidden_windows,
            today=self.date.date(),
        )

        # 4) Normalize summary so it always reflects the *real* forbidden windows
        if forbidden_windows:
            windows_str = ", ".join([f"{start}–{end}" for start, end in forbidden_windows])
            base_summary = plan.get("summary") or "Adjusted the study schedule based on feedback."
            # Strip any trailing sentence that might mention wrong hours; keep first sentence.
            first_sentence = base_summary.split(".")[0].strip()
            plan["summary"] = (
                f"{first_sentence}. "
                f"Forbidden study window(s) enforced: {windows_str}."
            )
        else:
            # No forbidden windows detected; keep summary as is or provide a default.
            if "summary" not in plan:
                plan["summary"] = "Updated the schedule based on feedback."

        return plan
