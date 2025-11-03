import json
from ai_system.agents.base_agent import BaseAgent


class MathAgent(BaseAgent):
    def propose_plan(self, subject_data):
        prompt=""
        response = self.model.get_response(prompt)
        return json.load(response)