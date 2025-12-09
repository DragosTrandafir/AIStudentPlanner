import requests
from typing import Dict, Any, List


class BackendAPI:
    """
    Wrapper over your FastAPI backend.
    Provides:
      - get_user_data(user_id)
      - get_current_and_last_feedback(user_id)
      - get_last_schedule(user_id)
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_user_data(self, user_id: int) -> Dict[str, Any]:
        """
        Returns user subjects in the format expected by the orchestrator.
        """
        url = f"{self.base_url}/users/{user_id}/subjects"

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(
                f"[BackendAPI] Failed to fetch subjects: {response.status_code} - {response.text}"
            )

        subjects = response.json()  # list of SubjectResponse

        #convert backend subjects → orchestrator tasks format
        tasks = []
        for s in subjects:
            tasks.append({
                "id": s["id"],
                "title": s["title"],
                "subject_name/project_name": s["name"],
                "start_datetime": s["start_date"],
                "end_datetime": s["end_date"],
                "type": s["type"],  # EXAM / PROJECT / etc.
                "difficulty": s["difficulty"],
                "description": s["description"],
                "status": s["status"],  # PENDING / IN_PROGRESS / COMPLETED
            })

        return {"tasks": tasks}

    def get_current_and_last_feedback(self, user_id: int) -> Dict[str, Any]:
        current_feedback = "Do not include any learning activity between 10 and 12 a.m."
        last_feedback = "Make the schedule more efficient"
        return {"feedback": current_feedback, "last_feedback": last_feedback}

    def get_last_schedule(self, user_id: int):
        last_schedule = {
            "calendar": [
                {
                    "date": "2025-11-24",
                    "entries": [
                        {
                            "time_allotted": "18:00–20:00",
                            "task_name": "Lecture review",
                            "subject_name/project_name": "pde",
                            "difficulty": 5,
                            "priority": 1
                        },
                        {
                            "time_allotted": "20:30–22:30",
                            "task_name": "Seminar review",
                            "subject_name/project_name": "OOP",
                            "difficulty": 3,
                            "priority": 1
                        }
                    ],
                    "notes": "High priority tasks for both exams."
                },
                {
                    "date": "2025-11-25",
                    "entries": [
                        {
                            "time_allotted": "09:00–11:00",
                            "task_name": "Seminar review (part 1)",
                            "subject_name/project_name": "pde",
                            "difficulty": 5,
                            "priority": 2
                        },
                        {
                            "time_allotted": "11:30–13:30",
                            "task_name": "Laboratory review",
                            "subject_name/project_name": "OOP",
                            "difficulty": 3,
                            "priority": 2
                        },
                        {
                            "time_allotted": "14:00–16:00",
                            "task_name": "Seminar review (part 2)",
                            "subject_name/project_name": "pde",
                            "difficulty": 5,
                            "priority": 3
                        },
                        {
                            "time_allotted": "16:30–18:30",
                            "task_name": "Algorithm practice",
                            "subject_name/project_name": "OOP",
                            "difficulty": 3,
                            "priority": 3
                        }
                    ],
                    "notes": "Continuing high priority tasks for both exams."
                },
                {
                    "date": "2025-11-26",
                    "entries": [
                        {
                            "time_allotted": "09:00–11:00",
                            "task_name": "Notes and outlines",
                            "subject_name/project_name": "pde",
                            "difficulty": 5,
                            "priority": 4
                        },
                        {
                            "time_allotted": "11:30–13:30",
                            "task_name": "Exam model solving",
                            "subject_name/project_name": "OOP",
                            "difficulty": 3,
                            "priority": 4
                        },
                        {
                            "time_allotted": "14:00–16:00",
                            "task_name": "Exam model solving",
                            "subject_name/project_name": "pde",
                            "difficulty": 5,
                            "priority": 5
                        },
                        {
                            "time_allotted": "16:30–18:30",
                            "task_name": "Additional practice problems",
                            "subject_name/project_name": "pde",
                            "difficulty": 5,
                            "priority": 6
                        }
                    ],
                    "notes": "Final tasks for both exams, ensuring completion before deadlines."
                },
                {
                    "date": "2025-11-27",
                    "entries": [
                        {
                            "time_allotted": "09:00–11:00",
                            "task_name": "Review and finalize",
                            "subject_name/project_name": "pde",
                            "difficulty": 5,
                            "priority": 7
                        }
                    ],
                    "notes": "Final review for PDE exam, ensuring all topics are covered. No tasks after 15:30."
                },
                {
                    "date": "2025-11-28",
                    "entries": [],
                    "notes": "Rest day before OOP exam."
                },
                {
                    "date": "2025-11-29",
                    "entries": [
                        {
                            "time_allotted": "09:00–11:00",
                            "task_name": "Review and finalize",
                            "subject_name/project_name": "OOP",
                            "difficulty": 3,
                            "priority": 5
                        }
                    ],
                    "notes": "Final review for OOP exam, ensuring all topics are covered. No tasks after 07:30."
                }
            ]
        }
        return last_schedule
