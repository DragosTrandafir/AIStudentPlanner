import json

from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils.propose_plan_logic import propose_calendar


class CalendarAgent(BaseAgent):
    def __init__(self, token, model, date):
        super().__init__(token, model)
        self.date=date

    def propose_agent_plan(self, plans):

        client = InferenceClient(model=self.model, token=self.token)
        response = propose_calendar(plans, self.date, client) # functie similara cu response = propose_plan(subject_data, "Mathematics", client) din ceilalti agenti, dar cu alte prompturi

        try:
            return json.loads(response)  # parse right here
        except json.JSONDecodeError:
            return {"raw_response": response}

