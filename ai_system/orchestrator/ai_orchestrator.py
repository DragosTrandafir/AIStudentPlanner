import os
from datetime import datetime
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
def _run_agent_on_task(agent, task):
    try:
        raw_response = agent.propose_agent_plan(task)
        return raw_response
    except Exception as e:
        print(e)


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

        self.backend = BackendAPI(backend_base_url or BACKEND_BASE_URL)

        self.math_agent = MathAgent(self.hf_token_1, self.custom_model_name)
        self.cs_agent = CSAgent(self.hf_token_1, self.custom_model_name)
        self.general_agent = CalendarAgent(self.hf_token_2, self.calendar_model_name, datetime.now())

    def _process_single_task(self, task: Dict[str, Any]):
        agent = self._select_agent_for_task(task)
        return _run_agent_on_task(agent, task)

    def generate_plan_for_user(self, user_id, save_to_backend) -> Dict[str, Any]:
        try:
            user_data = self.backend.get_user_data(user_id)
        except Exception as e:
            print(f"[AiOrchestrator] Backend unavailable, using mock data. ({e})")
            user_data = {
                "tasks": [
                    {
                        "id": 1,
                        "title": "pde scris",
                        "subject_name/project_name": "Partial Differential Equations",
                        "start_datetime": "2026-01-12T08:00:00",
                        "end_datetime": "2026-01-12T10:00:00",
                        "type": "written",
                        "difficulty": 5,
                        "description": "I did not understand anything during the semester.",
                        "status": "Pending"
                    },
                    {
                        "id": 2,
                        "title": "astronomie scris",
                        "subject_name/project_name": "Astronomy",
                        "start_datetime": "2026-01-26T12:00:00",
                        "end_datetime": "2026-01-26T14:00:00",
                        "type": "written",
                        "difficulty": 5,
                        "description": "I solved everything with ChatGPT, I do not know anything.",
                        "status": "Pending"
                    },
                    {
                        "id": 3,
                        "title": "OOP Final Project",
                        "subject_name/project_name": "Object-Oriented Programming",
                        "start_datetime": "2026-01-25T10:00:00",
                        "end_datetime": "2026-01-31T12:00:00",
                        "type": "project",
                        "difficulty": 4,
                        "description": "Large OOP project with multiple design patterns.",
                        "status": "Pending"
                    },

                    {
                        "id": 4,
                        "title": "ap practic",
                        "subject_name/project_name": "Algorithms and Programming",
                        "start_datetime": "2026-02-02T10:00:00",
                        "end_datetime": "2026-02-02T12:00:00",
                        "type": "practical",
                        "difficulty": 2,
                        "description": "I just need a bit of revise.",
                        "status": "Pending"
                    }
                ]
            }

        tasks_input: List[Dict[str, Any]] = [
            task for task in user_data.get("tasks", [])
            if task.get("status") != "Completed"
        ]

        max_workers = min(8, len(tasks_input))  # safe default for HF APIs
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            plans = list(executor.map(self._process_single_task, tasks_input))

        final_plan = _run_agent_on_task(self.general_agent, plans)

        return final_plan

    def _select_agent_for_task(self, task: Dict[str, Any]):

        text = " ".join([
            task.get("title", ""),
            task.get("subject_name/project_name", ""),
            task.get("description", ""),
            task.get("type", ""),
        ]).lower()

        math_keywords = {
            # Pure mathematics
            "mathematics",
            "math",
            "algebra",
            "analysis",
            "geometry",
            "calculus",
            "statistics",
            "probability",
            "logic",
            "numerical",
            "modeling",

            # Differential equations
            "pde",
            "ode",
            "partial differential equations",
            "differential equations",

            # Applied mathematics / physics
            "astronomy",
            "astrophysics",
            "mechanics",
            "classical mechanics",
            "dynamics",
            "thermodynamics",
            "optics",
            "physics",
        }

        if any(keyword in text for keyword in math_keywords):
            return self.math_agent

        return self.cs_agent


