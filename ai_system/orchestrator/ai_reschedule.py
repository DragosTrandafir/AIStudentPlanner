import os
import json
import tempfile
from datetime import datetime, date, time, timedelta
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from ai_system.agents.cs_agent import CSAgent
from ai_system.agents.feedback_agent import FeedbackAgent
from ai_system.agents.general_agent import CalendarAgent
from ai_system.agents.math_agent import MathAgent
from ai_system.backend.backend_api import BackendAPI

# -----------------------------------------------------------
# Config din .env
# -----------------------------------------------------------

load_dotenv()

HF_TOKEN_2 = os.getenv("HF_TOKEN_2")
CALENDAR_AGENT_MODEL = os.getenv("CALENDAR_AGENT_MODEL")
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")


class AiRescheduler:
    """
    Coordonatorul AI:
    - primește de la backend last_feedback, current_feedback si last_schedule
    - combină planurile într-un JSON final (inclusiv un pseudo-calendar)
    - trimite planul înapoi la backend
    """

    def __init__(
            self,
            hf_token: Optional[str] = None,
            rescheduler_model_name: Optional[str] = None,
            backend_base_url: Optional[str] = None,
    ) -> None:
        self.hf_token = hf_token or HF_TOKEN_2
        self.rescheduler_model_name = rescheduler_model_name or CALENDAR_AGENT_MODEL

        if self.hf_token is None or self.rescheduler_model_name is None:
            raise ValueError(
                "[AiOrchestrator] HF_TOKEN or rescheduler_model_name not configured. "
                "Check your .env file."
            )

        self.backend = BackendAPI(backend_base_url or BACKEND_BASE_URL)
        self.rescheduler_agent = FeedbackAgent(self.hf_token, self.rescheduler_model_name, datetime.now())

    def generate_plan_for_user(self, user_id, save_to_backend: bool = True):

        try:
            feedbacks = self.backend.get_current_and_last_feedback(user_id)
            print(feedbacks)
        except Exception as e:
            print(f"[AiOrchestrator] Backend feedback unavailable, skipping. ({e})")

        try:
            last_schedule = self.backend.get_last_schedule(user_id)
            print(last_schedule)
        except Exception as e:
            print(f"[AiOrchestrator] Backend feedback unavailable, skipping. ({e})")



    def _run_agent_on_task(self, agent, task):
        try:
            raw_response = agent.propose_agent_plan(task)
            return raw_response
        except Exception as e:
            print(e)


# -----------------------------------------------------------
# Script de test / exemplu de folosire
# -----------------------------------------------------------

if __name__ == "__main__":
    test_user_id = os.getenv("TEST_USER_ID", "demo_user")

    rescheduler = AiRescheduler()
    rescheduler.generate_plan_for_user(test_user_id, save_to_backend=False)

    # print(json.dumps(plan, indent=2))
