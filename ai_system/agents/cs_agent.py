import json

from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils import get_response
from ai_system.utils.get_response import make_llm_call


class CSAgent(BaseAgent):
    def propose_agent_plan(self, subject_data):

        with open(subject_data, 'r') as f:
            task = json.load(f)

        title = task['title']
        start_time = task['start_datetime']
        end_time = task['end_datetime']
        type_ = task['type']

        prompt = (f"Print the data I gave you: {title}, {start_time}, {end_time}. "
                  f"Also, tell me a fact about Cluj-Napoca.")

        client = InferenceClient(model=self.model, token=self.token)

        response = make_llm_call(client, prompt, self.model)
        print(response)





