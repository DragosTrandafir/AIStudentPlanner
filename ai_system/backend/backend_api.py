import requests
from typing import Dict, Any, List, Optional


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
        """
        Get the last 2 feedbacks for a user.
        Returns: {
            "current_feedback": feedback from latest schedule,
            "last_feedback": feedback from second latest schedule (if exists)
        }
        """
        url = f"{self.base_url}/users/{user_id}/feedback/latest"
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch latest feedbacks: {response.status_code}")
            
            feedbacks = response.json()  # List of last 2 feedbacks
            
            # Map to orchestrator format
            result = {}
            if feedbacks and len(feedbacks) > 0:
                fb = feedbacks[0]  # Latest feedback
                result["current_feedback"] = {
                    "created_at": fb.get("created_at"),
                    "text": fb.get("comments", ""),
                    "rating": fb.get("rating"),
                }
            
            if feedbacks and len(feedbacks) > 1:
                fb = feedbacks[1]  # Second latest feedback
                result["last_feedback"] = {
                    "created_at": fb.get("created_at"),
                    "text": fb.get("comments", ""),
                    "rating": fb.get("rating"),
                }
            
            return result
        except Exception as e:
            print(f"[BackendAPI] Warning: Could not fetch latest feedback: {e}")
            return {}

    def get_latest_schedule(self, user_id: int) -> Dict[str, Any]:
        """
        Get the entire latest schedule (all plans from latest generation).
        Returns plans in the format expected by the orchestrator.
        """
        url = f"{self.base_url}/users/{user_id}/plans/latest-schedule"
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch latest schedule: {response.status_code}")
            
            plans = response.json()  # List of PlanResponse
            
            # Convert plans to orchestrator calendar format
            calendar = []
            for plan in plans:
                day_entry = {
                    "date": plan["plan_date"],
                    "entries": [],
                    "notes": plan.get("notes", ""),
                }
                
                # Add AI tasks as entries
                for task in plan.get("entries", []):
                    day_entry["entries"].append({
                        "time_allotted": task["time_allotted"],
                        "task_name": task["ai_task_name"],
                        "subject_name/project_name": task["task_name"],
                        "difficulty": task["difficulty"],
                        "priority": task["priority"],
                    })
                
                calendar.append(day_entry)
            
            return {"calendar": calendar}
        except Exception as e:
            print(f"[BackendAPI] Warning: Could not fetch latest schedule: {e}")
            return None

    def get_last_two_schedules(self, user_id: int) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        Get the last two schedules (latest and second latest) with their feedback.
        Returns ({current_schedule, current_feedback}, {last_schedule, last_feedback})
        """
        url = f"{self.base_url}/users/{user_id}/plans/last-two-schedules"
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch schedules: {response.status_code}")
            
            data = response.json()
            
            # Convert first schedule
            current = None
            if data.get("current_schedule"):
                calendar = []
                for plan in data["current_schedule"]["plans"]:
                    day_entry = {
                        "date": plan["plan_date"],
                        "entries": [],
                        "notes": plan.get("notes", ""),
                    }
                    for task in plan.get("entries", []):
                        day_entry["entries"].append({
                            "time_allotted": task["time_allotted"],
                            "task_name": task["ai_task_name"],
                            "subject_name/project_name": task["task_name"],
                            "difficulty": task["difficulty"],
                            "priority": task["priority"],
                        })
                    calendar.append(day_entry)
                
                current = {
                    "calendar": calendar,
                    "feedback": data["current_schedule"].get("feedback"),
                }
            
            # Convert second schedule
            last = None
            if data.get("last_schedule"):
                calendar = []
                for plan in data["last_schedule"]["plans"]:
                    day_entry = {
                        "date": plan["plan_date"],
                        "entries": [],
                        "notes": plan.get("notes", ""),
                    }
                    for task in plan.get("entries", []):
                        day_entry["entries"].append({
                            "time_allotted": task["time_allotted"],
                            "task_name": task["ai_task_name"],
                            "subject_name/project_name": task["task_name"],
                            "difficulty": task["difficulty"],
                            "priority": task["priority"],
                        })
                    calendar.append(day_entry)
                
                last = {
                    "calendar": calendar,
                    "feedback": data["last_schedule"].get("feedback"),
                }
            
            return current, last
        except Exception as e:
            print(f"[BackendAPI] Warning: Could not fetch last two schedules: {e}")
            return None, None
