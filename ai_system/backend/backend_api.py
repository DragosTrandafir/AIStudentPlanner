import requests


class BackendAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    # get user data for planning
    def get_user_data(self, user_id: str):
        """
        Fetches all user-specific planning data from backend.
        Includes: subjects, projects with their attributes
        """
        url = f"{self.base_url}/api/plan/generate"
        response = requests.get(url, params={"user_id": user_id})
        #response.raise_for_status()
        return response.json()

    # get latest feedback
    def get_feedback(self, user_id: str):
        """
        Retrieves recent user feedback related to the plan (e.g. 'too much', 'missed today').
        """
        url = f"{self.base_url}/api/plan/feedback"
        response = requests.get(url, params={"user_id": user_id})
        # response.raise_for_status()
        return response.json()

    # save generated plan in DB
    def save_plan(self, user_id: str, plan: dict):
        """
        Sends the new JSON plan to the backend for storage in the DB.
        """
        url = f"{self.base_url}/api/plan/save"
        response = requests.post(url, json={"user_id": user_id, "plan": plan})
        # response.raise_for_status()
        return response.json()

    # get last plan from DB
    def get_last_plan(self, user_id: str):
        """
        Retrieves last stored plan (for recovery or consistency check).
        """
        url = f"{self.base_url}/api/plan/last"
        response = requests.get(url, params={"user_id": user_id})
        # response.raise_for_status()
        return response.json()
