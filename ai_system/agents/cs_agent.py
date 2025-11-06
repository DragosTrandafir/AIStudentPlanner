import json

from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils.custom_agents_prompts import *
from ai_system.utils.get_response import make_llm_call


class CSAgent(BaseAgent):
    def propose_agent_plan(self, subject_data):
        with open(subject_data, 'r') as f:
            task = json.load(f)

        title = task['title']
        name = task['subject_name/project_name']
        start_datetime = task['start_datetime']
        end_datetime = task['end_datetime']
        type_ = task['type']
        difficulty = task['difficulty']
        description = task['description']
        status = task['status']

        prompt_practical_exam = (
            get_role_prompt(type_),

            get_practical_exam_heuristics(),

            get_input_output_instructions(title,name,start_datetime,end_datetime,type_, difficulty,description,status),

            get_practical_exam_example()
        )

        client = InferenceClient(model=self.model, token=self.token)

        print(type_)

        if type_ == "Practical Exam":
            full_prompt = "\n\n".join(prompt_practical_exam)
            response = make_llm_call(client, full_prompt, self.model)
            print(response)
