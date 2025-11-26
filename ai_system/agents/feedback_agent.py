import json

from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils.format_handling.load_json import json_load
from ai_system.utils.propose_feedback_reschule_logic import propose_feedback_reschedule


class FeedbackAgent(BaseAgent):
    def __init__(self, token, model, date,current_feedback,last_feedback,last_schedule):
        super().__init__(token, model)
        self.date=date
        self.current_feedback=current_feedback
        self.last_feedback=last_feedback
        self.last_schedule=last_schedule

    def propose_agent_plan(self, plans):

        client = InferenceClient(model=self.model, token=self.token)
        response = propose_feedback_reschedule(plans, self.date, client,self.current_feedback,self.last_feedback,self.last_schedule)

        try:
            return json.loads(response)  # parse right here
        except json.JSONDecodeError:
            return {"raw_response": response}

