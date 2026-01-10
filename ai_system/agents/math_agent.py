import json

from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils.propose_plan_logic import propose_plan


class MathAgent(BaseAgent):
    def propose_agent_plan(self, subject_data):

        client = InferenceClient(model=self.model, token=self.token)
        response = propose_plan(subject_data, "Mathematics", client)

        try:
            return json.loads(response)  # parse right here
        except json.JSONDecodeError:
            return {"raw_response": response}

