from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils.format_handling.load_json import json_load
from ai_system.utils.propose_plan_logic import propose_plan


class CSAgent(BaseAgent):
    def propose_agent_plan(self, subject_data):
        task = json_load(subject_data)

        client = InferenceClient(model=self.model, token=self.token)
        response = propose_plan(task, "Computer Science", client)
        return response
