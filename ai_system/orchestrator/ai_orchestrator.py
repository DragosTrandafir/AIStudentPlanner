import os
import json
import tempfile
from datetime import datetime, date, time, timedelta
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from ai_system.agents.cs_agent import CSAgent
from ai_system.agents.math_agent import MathAgent
from ai_system.backend.backend_api import BackendAPI

# -----------------------------------------------------------
# Config din .env
# -----------------------------------------------------------

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
CUSTOM_AGENT_MODEL = os.getenv("CUSTOM_AGENT_MODEL")
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

# fallback simplu dacă lipsesc env-urile, ca să nu crape direct
if HF_TOKEN is None:
    print("[AiOrchestrator] WARNING: HF_TOKEN is not set in environment.")
if CUSTOM_AGENT_MODEL is None:
    print("[AiOrchestrator] WARNING: CUSTOM_AGENT_MODEL is not set in environment.")


# -----------------------------------------------------------
# Orchestrator
# -----------------------------------------------------------

class AiOrchestrator:
    """
    Coordonatorul AI:
    - primește de la backend toate task-urile (examene / proiecte)
    - alege agentul corect (Math / CS)
    - cheamă LLM-ul prin agent
    - combină planurile într-un JSON final (inclusiv un pseudo-calendar)
    - trimite planul înapoi la backend
    """

    def __init__(
        self,
        hf_token: Optional[str] = None,
        model_name: Optional[str] = None,
        backend_base_url: Optional[str] = None,
    ) -> None:
        self.hf_token = hf_token or HF_TOKEN
        self.model_name = model_name or CUSTOM_AGENT_MODEL

        if self.hf_token is None or self.model_name is None:
            raise ValueError(
                "[AiOrchestrator] HF_TOKEN or CUSTOM_AGENT_MODEL not configured. "
                "Check your .env file."
            )

        self.backend = BackendAPI(backend_base_url or BACKEND_BASE_URL)

        # inițializăm agenții (deocamdată doar Math și CS)
        self.math_agent = MathAgent(self.hf_token, self.model_name)
        self.cs_agent = CSAgent(self.hf_token, self.model_name)

    # -------------------------------------------------------
    # API public – asta apelează backend-ul
    # -------------------------------------------------------

    def generate_plan_for_user(self, user_id: str, save_to_backend: bool = True) -> Dict[str, Any]:
        """
        Flux principal:
        1) cere la backend toate task-urile pentru user
        2) cere feedback (nu îl folosim încă în mod avansat, doar îl atașăm)
        3) rulează agenții pe fiecare task
        4) combină rezultatele într-un plan unic + blocuri de studiu
        5) opțional, salvează planul în backend
        """

        #user_data = self.backend.get_user_data(user_id)
        #feedback = self.backend.get_feedback(user_id)
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
                        "start_datetime": "2025-09-09T09:00:00",
                        "end_datetime": "2025-09-09T11:00:00",
                        "type": "Practical Exam",
                        "difficulty": 5,
                        "description": "I did not understand anything during the semester.",
                        "status": "Pending"
                    },
                    {
                        "id": 2,
                        "title": "PDE scris",
                        "subject_name/project_name": "Partial Differential Equations",
                        "start_datetime": "2025-09-09T09:00:00",
                        "end_datetime": "2025-09-09T11:00:00",
                        "type": "Written Exam",
                        "difficulty": 5,
                        "description": "I solved everything with ChatGPT.",
                        "status": "Pending"
                    }
                ]
            }

        try:
            feedback = self.backend.get_feedback(user_id)
        except Exception as e:
            print(f"[AiOrchestrator] Backend feedback unavailable, skipping. ({e})")
            feedback = {}

        tasks_input: List[Dict[str, Any]] = (
            user_data.get("tasks")
            or user_data.get("subjects")
            or user_data.get("items")
            or []
        )

        all_items: List[Dict[str, Any]] = []
        all_blocks: List[Dict[str, Any]] = []

        for task in tasks_input:
            agent = self._select_agent_for_task(task)
            agent_plan = self._run_agent_on_task(agent, task)

            # blocuri de studiu (pseudo-calendar) generate din planul agentului
            blocks = self._generate_study_blocks(task, agent_plan)

            all_items.append(
                {
                    "input_task": task,
                    "agent_type": type(agent).__name__,
                    "plan": agent_plan,
                    "study_blocks": blocks,
                }
            )
            all_blocks.extend(blocks)

        final_plan: Dict[str, Any] = {
            "user_id": user_id,
            "generated_at": datetime.utcnow().isoformat(),
            "items": all_items,
            "calendar_blocks": all_blocks,  # toate blocurile la grămadă, pentru UI / Google Calendar
            "feedback_used": feedback,
        }

        if save_to_backend:
            try:
                self.backend.save_plan(user_id, final_plan)
            except Exception as exc:
                # nu omorâm orchestratorul dacă e o problemă de rețea
                print(f"[AiOrchestrator] WARNING: failed to save plan to backend: {exc}")

        return final_plan

    # -------------------------------------------------------
    # Alegerea agentului
    # -------------------------------------------------------

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

        if "math" in text or "algebra" in text or "analysis" in text \
           or "equations" in text or "pde" in text or "ode" in text:
            return self.math_agent

        if "computer" in text or "programming" in text or "cs" in text \
           or "oop" in text or "data structures" in text:
            return self.cs_agent

        # fallback – dacă nu știm, punem la CS (poți schimba la nevoie)
        return self.cs_agent

    # -------------------------------------------------------
    # Rulare agent
    # -------------------------------------------------------

    def _run_agent_on_task(self, agent: Any, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agenții actuali așteaptă un path către un fișier JSON.
        Ca să nu le stricăm API-ul, scriem task-ul într-un fișier temporar.
        """

        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=True) as tmp:
            json.dump(task, tmp)
            tmp.flush()

            raw_response = agent.propose_agent_plan(tmp.name)

        # încercăm să parsăm JSON-ul; dacă nu reușim, îl trimitem ca string brut
        try:
            parsed = json.loads(raw_response)
            return parsed
        except json.JSONDecodeError:
            print("[AiOrchestrator] WARNING: agent returned non-JSON output, keeping raw_response.")
            return {"raw_response": raw_response}

    # -------------------------------------------------------
    # Generare blocuri de studiu (pseudo-calendar)
    # -------------------------------------------------------

    def _generate_study_blocks(
        self,
        input_task: Dict[str, Any],
        agent_plan: Dict[str, Any],
        max_hours_per_day: int = 4,
        default_start_hour: int = 18,
    ) -> List[Dict[str, Any]]:
        """
        Transformă planul agentului (care are 'tasks' cu estimated_hours)
        în blocuri concrete de învățat, distribuite pe zile până la examen.

        Simplificare:
        - pornim de AZI
        - mergem până la deadline (sau cel mult 30 de zile)
        - alocăm max_hours_per_day ore pe zi
        - fiecare subtask devine unul sau mai multe blocuri de învățat
        """

        if not isinstance(agent_plan, dict):
            return []

        sub_tasks = agent_plan.get("tasks", [])
        if not sub_tasks:
            return []

        # determinăm deadline-ul
        deadline_str = agent_plan.get("deadline") or input_task.get("start_datetime")
        try:
            deadline_dt = datetime.fromisoformat(deadline_str)
        except Exception:
            deadline_dt = datetime.now() + timedelta(days=7)

        today = date.today()
        latest_day = min(
            deadline_dt.date(),
            today + timedelta(days=30)  # safety cap
        )

        current_day = today
        hours_used_today = 0
        blocks: List[Dict[str, Any]] = []

        def next_day(d: date) -> date:
            return d + timedelta(days=1)

        for st in sub_tasks:
            task_name = st.get("task_name", "Study session")
            hours_left = int(st.get("estimated_hours", 1))

            while hours_left > 0 and current_day <= latest_day:
                # dacă am umplut ziua curentă, trecem la următoarea
                if hours_used_today >= max_hours_per_day:
                    current_day = next_day(current_day)
                    hours_used_today = 0
                    continue

                # câte ore putem pune în ziua curentă
                available_today = max_hours_per_day - hours_used_today
                chunk = min(hours_left, available_today)

                start_dt = datetime.combine(
                    current_day,
                    time(hour=default_start_hour + hours_used_today, minute=0),
                )
                end_dt = start_dt + timedelta(hours=chunk)

                block = {
                    "date": current_day.isoformat(),
                    "start_datetime": start_dt.isoformat(),
                    "end_datetime": end_dt.isoformat(),
                    "subject_title": input_task.get("title"),
                    "subject_name": input_task.get("subject_name/project_name"),
                    "exam_type": input_task.get("type"),
                    "subtask_name": task_name,
                    "estimated_hours": chunk,
                }
                blocks.append(block)

                hours_left -= chunk
                hours_used_today += chunk

            # dacă am depășit deadline-ul / limita de zile, oprim
            if current_day > latest_day:
                break

        return blocks


# -----------------------------------------------------------
# Script de test / exemplu de folosire
# -----------------------------------------------------------

if __name__ == "__main__":
    """
    Poți rula rapid:
        python -m ai_system.orchestrator.ai_orchestrator
    presupunând că:
      - ai BACKEND_BASE_URL setat
      - backend-ul răspunde la /api/plan/generate etc.
      - ai un user_id de test în DB
    """

    test_user_id = os.getenv("TEST_USER_ID", "demo_user")

    orchestrator = AiOrchestrator()
    plan = orchestrator.generate_plan_for_user(test_user_id, save_to_backend=False)

    print(json.dumps(plan, indent=2))
