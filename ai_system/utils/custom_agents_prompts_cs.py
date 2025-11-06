# general prompts
def get_role_prompt(type_):
    role_prompt = (f"You are a specialized planner for Computer Science university {type_}s. "
                   f"Analyze the following {type_} task and propose a structured work plan in JSON format. "
                   f"The plan will be used by a scheduling coordinator, so focus on concrete, schedulable data.\n\n")
    return role_prompt


def get_input_output_instructions(title, name, start_datetime, end_datetime, type_, difficulty, description, status):
    input_output_instructions = (
        f"Base your estimates on these heuristics."
        f"Keep total hours realistic and consistent across runs.\n\n"


        f"Here is the task data:\n"
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

        f"Output fields:\n"
        f"- summary: brief overview of the task\n"
        f"- total_estimated_hours: integer, total hours required\n"
        f'- difficulty: consider the input difficulty, but make an average with your estimated difficulty given '
        f'all the information\n'
        f"- tasks: list of subtasks, each with task_name, estimated_hours, and priority (1 = first)\n"
        f"- deadline: copy <start_datetime> from input if available\n\n"

        f"Please output ONLY valid JSON in EXACTLY this structure — "
        f"do NOT include any explanations, reasoning, or extra text before or after the JSON.\n\n")
    return input_output_instructions


# special prompts

# CS

# Practical Exam heuristics
def get_practical_exam_heuristics():
    return (f"Use the following heuristics for estimating hours, difficulty and tasks:\n"
            f"- We have 7 or 14 seminaries"
            f"- We have 7 or 14 laboratories"
            f"- Each laboratory review = ???????\n"
            f"- Each seminary review = ???????\n"
            f"- Additional review algorithms and coding problems = 15-30 minutes each, depending on difficulty.\n"
            f"- Practical exams typically require 6–10 total preparation hours. ??????\n")


# Practical Exam example
def get_practical_exam_example():
    return (f"Example format (for reference only):\n"
            f"{{\n"
            f'  "summary": "Short sentence describing the overall goal.",\n'
            f'  "total_estimated_hours": 12,\n'
            f'  "difficulty": 4,\n'
            f'  "tasks": [\n'
            f'    {{ "task_name": "Seminars review (part 1)", "estimated_hours": 3, "priority": 1 }},\n'
            f'    {{ "task_name": "Seminars review (part 2)", "estimated_hours": 5, "priority": 2 }},\n'
            f'    {{ "task_name": "Laboratories review", "estimated_hours": 4, "priority": 3 }}\n'
            f'    {{ "task_name": "Algorithms", "estimated_hours": 2, "priority": 4 }}\n'
            f'  ],\n'
            f'  "deadline": "2025-11-10T09:00:00"\n'
            f"}}")


# Written Exam heuristics
def get_written_exam_heuristics():
    return (f"Use the following heuristics for estimating hours, difficulty and tasks:\n"
            f"- We have 14 lectures"
            f"- Each lecture review = ???????\n"
            f"- Additional notes, outlines and summaries = ?????.\n"
            f"- Written exams typically require 6–10 total preparation hours. ??????\n")


# Written Exam example
def get_written_exam_example():
    return (f"Example format (for reference only):\n"
            f"{{\n"
            f'  "summary": "Short sentence describing the overall goal.",\n'
            f'  "total_estimated_hours": 12,\n'
            f'  "difficulty": 4,\n'
            f'  "tasks": [\n'
            f'    {{ "task_name": "Seminars review (part 1)", "estimated_hours": 3, "priority": 1 }},\n'
            f'    {{ "task_name": "Seminars review (part 2)", "estimated_hours": 5, "priority": 2 }},\n'
            f'    {{ "task_name": "Laboratories review", "estimated_hours": 4, "priority": 3 }}\n'
            f'    {{ "task_name": "Algorithms", "estimated_hours": 2, "priority": 4 }}\n'
            f'  ],\n'
            f'  "deadline": "2025-11-10T09:00:00"\n'
            f"}}")
