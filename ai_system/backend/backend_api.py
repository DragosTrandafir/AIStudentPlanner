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

        # Convert backend subjects → orchestrator tasks format
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

        print("--------------------------------------------------------------------------")
        return {"tasks": tasks}


    # def get_feedback(self, user_id: int) -> Dict[str, Any]:
    #     """
    #     Placeholder implementation.
    #     Your backend does not yet support feedback retrieval.
    #     """
    #     print("[BackendAPI] WARNING: Feedback endpoint not implemented yet.")
    #     return {}  # Empty feedback until implemented


    # def save_plan(self, user_id: int, plan: Dict[str, Any]) -> bool:
    #     """
    #     Sends the generated study plan to the backend.
    #     Requires a backend endpoint like:
    #         POST /users/{user_id}/plan
    #     """
    #     url = f"{self.base_url}/users/{user_id}/plan"
    #
    #     response = requests.post(url, json=plan)
    #
    #     if response.status_code not in (200, 201):
    #         raise Exception(
    #             f"[BackendAPI] Failed to save plan: {response.status_code} - {response.text}"
    #         )
    #
    #     return True
