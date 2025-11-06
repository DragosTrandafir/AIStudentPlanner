import json

from huggingface_hub import InferenceClient

from ai_system.agents.base_agent import BaseAgent
from ai_system.utils.custom_agents_prompts_cs import *
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

        client = InferenceClient(model=self.model, token=self.token)

        if type_ == "Practical Exam":
            prompt_practical_exam = (
                get_role_prompt(type_),
                get_general_heuristics_header(),
                get_practical_exam_heuristics(),
                get_input_output_instructions(
                    title, name, start_datetime, end_datetime,
                    type_, difficulty, description, status
                ),
                get_practical_exam_example()
            )

            full_prompt = "\n\n".join(prompt_practical_exam)
            response = make_llm_call(client, full_prompt, self.model)
            print(response)
        elif type_ == "Written Exam":
            prompt_written_exam = (
                get_role_prompt(type_),
                get_general_heuristics_header(),
                get_written_exam_heuristics(),
                get_input_output_instructions(title, name, start_datetime, end_datetime, type_, difficulty, description,
                                              status),
                get_written_exam_example()
            )
            full_prompt = "\n\n".join(prompt_written_exam)
            response = make_llm_call(client, full_prompt, self.model)
            print(response)
