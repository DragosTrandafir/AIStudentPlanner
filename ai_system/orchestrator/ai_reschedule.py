import os
import json
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
        # `datetime.now()` is the "today" used inside the feedback agent
        self.agent = FeedbackAgent(self.hf_token, self.model, datetime.now())

    def generate_plan_for_user(
        self,
        user_id: str,
        save_to_backend: bool = True,
    ) -> Dict[str, Any]:

        # ------------------ FEEDBACK ------------------
        try:
            fb = self.backend.get_current_and_last_feedback(user_id)
        except Exception:
            fb = {
                "current_feedback": {
                    "created_at": "2025-11-25T10:00:00",
                    "text": "Do not include any learning activity between 13 and 14:30 a.m.",
                    "day_status": "constraint",
                },
                "last_feedback": {
                    "created_at": "2025-11-24T10:00:00",
                    "text": "Make the schedule more efficient",
                    "day_status": "neutral",
                },
            }

        current_feedback = fb.get("current_feedback") or {
            "text": fb.get("feedback", "")
        }
        last_feedback = fb.get("last_feedback", {})

        # ------------------ LAST SCHEDULE ------------------
        try:
            last_schedule = self.backend.get_last_schedule(user_id)
        except Exception:
            last_schedule = {
                "summary": "Previous plan",
                "calendar": [],
            }

        context = {
            "current_feedback": current_feedback,
            "last_feedback": last_feedback,
            "last_schedule": last_schedule,
        }

        new_schedule = self.agent.propose_agent_plan(context)

        print("\n[AiRescheduler] ✅ FINAL RESCHEDULED PLAN")
        print(json.dumps(new_schedule, indent=2, ensure_ascii=False))

        if save_to_backend:
            try:
                self.backend.save_plan(user_id, new_schedule)
            except Exception as e:
                print("[AiRescheduler] Backend save failed:", e)

        return new_schedule


if __name__ == "__main__":
    user = os.getenv("TEST_USER_ID", "demo_user")
    AiRescheduler().generate_plan_for_user(user, save_to_backend=False)
