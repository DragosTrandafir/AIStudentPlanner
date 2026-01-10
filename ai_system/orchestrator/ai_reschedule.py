import os
from datetime import datetime
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from ai_system.agents.feedback_agent import FeedbackAgent
from ai_system.backend.backend_api import BackendAPI

load_dotenv()

HF_TOKEN_2 = os.getenv("HF_TOKEN_2")
CALENDAR_AGENT_MODEL = os.getenv("CALENDAR_AGENT_MODEL")
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")


class AiRescheduler:
    def __init__(
            self,
            hf_token: Optional[str] = None,
            rescheduler_model_name: Optional[str] = None,
            backend_base_url: Optional[str] = None,
    ):
        self.hf_token = hf_token or HF_TOKEN_2
        self.model = rescheduler_model_name or CALENDAR_AGENT_MODEL
        self.backend = BackendAPI(backend_base_url or BACKEND_BASE_URL)
        self.agent = FeedbackAgent(self.hf_token, self.model, datetime.now())

    def generate_plan_for_user(
            self,
            user_id: int,
            save_to_backend
    ) -> Dict[str, Any]:

        try:
            fb = self.backend.get_current_and_last_feedback(user_id)
        except Exception as e:
            print(f"[AiRescheduler] Warning: Could not fetch feedback: {e}")
            fb = {}

        current_feedback = fb.get("current_feedback") or {
            "current_feedback": fb.get("feedback", "No feedback provided")
        }
        last_feedback = fb.get("last_feedback") or {}


        try:
            latest_schedule = self.backend.get_latest_schedule(user_id)
        except Exception as e:
            print(f"[AiRescheduler] Warning: Could not fetch latest schedule: {e}")
            latest_schedule = {"calendar": []}

        context = {
            "last_feedback": last_feedback,
            "last_schedule": latest_schedule,
            "current_feedback": current_feedback
        }

        new_schedule = self.agent.propose_agent_plan(context)

        return new_schedule


