import json

from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils.format_handling.load_json import json_load
from ai_system.utils.propose_feedback_reschule_logic import propose_feedback_reschedule


class FeedbackAgent(BaseAgent):
    def __init__(self, token, model, date):
        super().__init__(token, model)
        self.date=date

    def propose_agent_plan(self, context):

        client = InferenceClient(model=self.model, token=self.token)

        current_feedback=context['current_feedback']
        last_feedback=context[
            'last_feedback'
        ]
        last_schedule=context['last_schedule']

        response = propose_feedback_reschedule(self.date, client,current_feedback,last_feedback,last_schedule)

        try:
            return json.loads(response)  # parse right here
        except json.JSONDecodeError:
            return {"raw_response": response}

