import os
import json
import tempfile
from datetime import datetime, date, time, timedelta
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from ai_system.agents.cs_agent import CSAgent
from ai_system.agents.general_agent import CalendarAgent
from ai_system.agents.math_agent import MathAgent
from ai_system.backend.backend_api import BackendAPI

from concurrent.futures import ThreadPoolExecutor


# Config din .env
load_dotenv()

HF_TOKEN_1 = os.getenv("HF_TOKEN_1")
HF_TOKEN_2 = os.getenv("HF_TOKEN_2")
CUSTOM_AGENT_MODEL = os.getenv("CUSTOM_AGENT_MODEL")
CALENDAR_AGENT_MODEL = os.getenv("CALENDAR_AGENT_MODEL")
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")


# Orchestrator
class AiOrchestrator:
    def __init__(
            self,
            hf_token: Optional[str] = None,
            custom_model_name: Optional[str] = None,
            calendar_model_name: Optional[str] = None,
            backend_base_url: Optional[str] = None,
    ) -> None:
        self.hf_token_1 = hf_token or HF_TOKEN_1
        self.hf_token_2 = hf_token or HF_TOKEN_2
        self.custom_model_name = custom_model_name or CUSTOM_AGENT_MODEL
        self.calendar_model_name = calendar_model_name or CALENDAR_AGENT_MODEL

        if self.hf_token_1 is None or self.custom_model_name is None:
            raise ValueError(
                "[AiOrchestrator] HF_TOKEN or CUSTOM_AGENT_MODEL not configured. "
                "Check your .env file."
            )

        self.backend = BackendAPI(backend_base_url or BACKEND_BASE_URL)

        self.math_agent = MathAgent(self.hf_token_1, self.custom_model_name)
        self.cs_agent = CSAgent(self.hf_token_1, self.custom_model_name)
        self.general_agent = CalendarAgent(self.hf_token_2, self.calendar_model_name, datetime.now())

    def _process_single_task(self, task: Dict[str, Any]):
        agent = self._select_agent_for_task(task)
        return self._run_agent_on_task(agent, task)

    def generate_plan_for_user(self, user_id, save_to_backend: bool = True) -> Dict[str, Any]:
        try:
            user_data = self.backend.get_user_data(user_id)
        except Exception as e:
            print(f"[AiOrchestrator] Backend unavailable, using mock data. ({e})")
            user_data = {
                "tasks": [
                    {
                        "id": 1,
                        "title": "OOP practic",
                        "subject_name/project_name": "Object-Oriented Programming",
                        "start_datetime": "2026-01-23T09:00:00",
                        "end_datetime": "2026-01-23T11:00:00",
                        "type": "Practical Exam",
                        "difficulty": 5,
                        "description": "I did not understand anything during the semester.",
                        "status": "Pending"
                    },
                    {
                        "id": 2,
                        "title": "PDE scris",
                        "subject_name/project_name": "Partial Differential Equations",
                        "start_datetime": "2026-01-19T12:00:00",
                        "end_datetime": "2026-01-19T15:00:00",
                        "type": "Written Exam",
                        "difficulty": 5,
                        "description": "I solved everything with ChatGPT.",
                        "status": "Pending"
                    },
                    {
                        "id": 3,
                        "title": "OOP Final Project",
                        "subject_name/project_name": "Object-Oriented Programming",
                        "start_datetime": "2026-01-25T10:00:00",
                        "end_datetime": "2026-01-27T12:00:00",
                        "type": "Project",
                        "difficulty": 4,
                        "description": "Large OOP project with multiple design patterns.",
                        "status": "Pending"
                    },

                    {
                        "id": 4,
                        "title": "PDE Project",
                        "subject_name/project_name": "Partial Differential Equations",
                        "start_datetime": "2026-01-20T10:00:00",
                        "end_datetime": "2026-01-22T12:00:00",
                        "type": "Project",
                        "difficulty": 3,
                        "description": "Short mathematics project on PDEs with a few problems and a small report.",
                        "status": "Pending"
                    }
                ]
            }

        tasks_input: List[Dict[str, Any]] = (
            user_data.get("tasks")
        )

        max_workers = min(8, len(tasks_input))  # safe default for HF APIs
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            plans = list(executor.map(self._process_single_task, tasks_input))

        print(plans)

        final_plan = self._run_agent_on_task(self.general_agent, plans)

        print(f"Plan final: {final_plan}")

        if save_to_backend:
            try:
                self.backend.save_plan(user_id, final_plan)
            except Exception as exc:
                print(f"[AiOrchestrator] WARNING: failed to save plan to backend: {exc}")

        return final_plan

    # Alegerea agentului
    def _select_agent_for_task(self, task: Dict[str, Any]) -> Any:
        """
        Heuristic simplu:
        - dacă există câmp 'domain' / 'category', folosim asta
        - altfel, încercăm să ghicim după numele materiei
        - default: CSAgent
        """
        domain = (
                task.get("domain")
                or task.get("category")
                or task.get("faculty")
                or ""
        ).lower()

        subject_name = task.get("subject_name/project_name", "").lower()
        title = task.get("title", "").lower()
        text = f"{domain} {subject_name} {title}"
        print(f"Selected agent :{text}")

        if "math" in text or "algebra" in text or "analysis" in text \
                or "equations" in text or "pde" in text or "ode" in text:
            return self.math_agent

        if "computer" in text or "programming" in text or "cs" in text \
                or "oop" in text or "data structures" in text:
            return self.cs_agent

        return self.cs_agent

    # Rulare agent
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

    orchestrator = AiOrchestrator()
    plan = orchestrator.generate_plan_for_user(test_user_id, save_to_backend=False)

    print(json.dumps(plan, indent=2))
