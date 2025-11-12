# general prompts
def get_role_prompt(type_, general_university_type):
    role_prompt = (
        f"You are an expert academic planner specializing in {general_university_type} university {type_}s. "
        f"Your role is to analyze each {type_} and generate a structured, schedulable work plan in pure JSON format. "
        f"The plan must be actionable, realistic, and suitable for direct import into a scheduling system.\n\n"
    )
    return role_prompt


def get_input_output_instructions(title, name, start_datetime, end_datetime, type_, difficulty, description, status):
    input_output_instructions = (
        f"Below is the data for a {type_} task. "
        f"Use it to estimate workload, difficulty, and subtasks using the given heuristics.\n\n"

        f"Task data:\n"
        f"{{\n"
        f'  "title": "{title}",\n'
        f'  "name": "{name}",\n'
        f'  "start_datetime": "{start_datetime}",\n'
        f'  "end_datetime": "{end_datetime}",\n'
        f'  "type": "{type_}",\n'
        f'  "difficulty": "{difficulty}",\n'
        f'  "description": "{description}",\n'
        f'  "status": "{status}"\n'
        f"}}\n\n"

        f"Expected output (JSON only (DO NOT INCLUDE extra text, no trailing commas, no Markdown, no explanations)):\n"
        f"{{\n"
        f'  "summary": "Brief 1-sentence overview of the task.",\n'
        f'  "total_estimated_hours": <integer>,\n'
        f'  "difficulty": <integer from 1–5, balanced between input and your estimate>,\n'
        f'  "tasks": [\n'
        f'    {{ "task_name": <string>, "estimated_hours": <integer>, "priority": <integer starting from 1> }}\n'
        f'  ],\n'
        f'  "deadline": "{start_datetime}"\n'
        f"}}\n\n"

        f"Output rules:\n"
        f"- Output MUST be valid JSON only (no extra text, no trailing commas, no Markdown, no explanations).\n"
        f"- Use realistic and coherent time estimates consistent with heuristics.\n"
        f"- Priorities must start at 1 and increase sequentially.\n"
    )
    return input_output_instructions


def get_general_heuristics_header():
    return (
        "General estimation principles:\n"
        "- Adjust total hours based on difficulty and task type.\n"
        "- Keep total hours consistent with both heuristics and input difficulty.\n"
        "- Make sure total hours = the sum of all subtask hours.\n"
        "- Subtasks SHOULD NOT exceed 5 hours (split them in parts: (part 1), (part 2), ...).\n"
        "- Use action-oriented subtask names appropriate to the subtask type "
        "(e.g.,'Solve Model Problems', 'Additional notes', ...).\n"
    )
