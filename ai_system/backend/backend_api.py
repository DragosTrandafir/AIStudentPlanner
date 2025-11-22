import requests
from typing import Dict, Any, List


class BackendAPI:
    """
    Wrapper over your FastAPI backend.
    Provides:
      - get_user_data(user_id)
      - get_feedback(user_id)    (placeholder)
      - save_plan(user_id, plan)
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
                "type": s["type"],            # EXAM / PROJECT / etc.
                "difficulty": s["difficulty"],
                "description": s["description"],
                "status": s["status"],        # PENDING / IN_PROGRESS / COMPLETED
            })

        return {"tasks": tasks}


