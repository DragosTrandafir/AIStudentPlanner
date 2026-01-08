import json
from datetime import datetime
from typing import Any, Dict, List, Tuple

from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils.propose_feedback_reschule_logic import (
    propose_feedback_reschedule,
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

        last_feedback: Dict[str, Any] = context.get("last_feedback", {}) or {}
        last_schedule: Dict[str, Any] = context.get("last_schedule", {}) or {}
        current_feedback: Dict[str, Any] = context.get("current_feedback", {}) or {}

        response = propose_feedback_reschedule(
            self.date,
            client,
            last_feedback,
            last_schedule,
            current_feedback
        )

        try:
            return json.loads(response)  # parse right here
        except json.JSONDecodeError:
            return {"raw_response": response}
