# general prompts
def get_role_prompt(type_):
    role_prompt = (
        f"You are an expert academic planner specializing in Computer Science university {type_}s. "
        f"Your role is to analyze each {type_} and generate a structured, schedulable work plan in pure JSON format. "
        f"The plan must be actionable, realistic, and suitable for direct import into a scheduling system.\n\n"
        f"Do NOT explain your reasoning or include any text outside the JSON."
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

        f"Expected output (JSON only):\n"
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
        "- Always produce practical, schedulable subtasks (no vague items like 'study a bit').\n"
        "- Adjust total hours based on difficulty and task type.\n"
        "- Keep total hours consistent with both heuristics and input difficulty.\n"
        "- Make sure total hours = the sum of all subtask hours.\n"
        "- Subtasks should not exceed 5 hours each unless clearly justified.\n"
        "- Use action-oriented task names appropriate to the task type "
        "(e.g., 'Review Seminar Material', 'Revise Code Exercises', 'Solve Model Problems').\n"
    )


# special prompts

# CS

# Practical Exam heuristics
def get_practical_exam_heuristics():
    return (
        "Heuristics for Practical Exams:\n"
        "- Typically 7 or 14 seminars and laboratories.\n"
        "- Laboratories review: 2–3 hours.\n"
        "- Seminars review: ~2 hours.\n"
        "- Additional review (algorithms/coding problems): 1–2 hours.\n"
        "- Solving past exam models: 4–5 hours.\n"
        "- Typical total: 9–12 preparation hours.\n\n"
        "Adjust values based on task description realism."
    )


# Practical Exam example
def get_practical_exam_example():
    return (
        "Example JSON (for reference only — do not copy verbatim):\n"
        "{\n"
        '  "summary": "Preparation for practical exam of medium difficulty (you can include also description info)",\n'
        '  "total_estimated_hours": 11,\n'
        '  "difficulty": 3,\n'
        '  "tasks": [\n'
        '    { "task_name": "Seminar review (part 1)", "estimated_hours": 1, "priority": 1 },\n'
        '    { "task_name": "Seminar review (part 2)", "estimated_hours": 1, "priority": 2 },\n'
        '    { "task_name": "Laboratory review", "estimated_hours": 3, "priority": 3 },\n'
        '    { "task_name": "Algorithm practice", "estimated_hours": 2, "priority": 4 },\n'
        '    { "task_name": "Exam model solving", "estimated_hours": 4, "priority": 5 }\n'
        '  ],\n'
        '  "deadline": "2025-11-10T09:00:00"\n'
        "}"
    )


# Written Exam heuristics
def get_written_exam_heuristics():
    return (
        "Heuristics for Written Exams:\n"
        "- Usually consist of around 14 lectures and possibly a few seminars.\n"
        "- Lecture review: 7–8 hours total.\n"
        "- Seminar review: 0–1 hours (optional or minor component).\n"
        "- Creating additional notes, outlines, and summaries: 2–4 hours.\n"
        "- Solving past written exam models: 3–4 hours.\n"
        "- Typical total preparation time: 12–17 hours.\n\n"
        "Adjust the distribution of time and difficulty according to task details, "
        "difficulty level, and available preparation window."
    )


# Written Exam example
def get_written_exam_example():
    return (
        "Example JSON (for reference only — do not copy verbatim):\n"
        "{\n"
        '  "summary": "Comprehensive review of lecture material, summaries, and exam models.",\n'
        '  "total_estimated_hours": 16,\n'
        '  "difficulty": 4,\n'
        '  "tasks": [\n'
        '    { "task_name": "Lecture review (part 1)", "estimated_hours": 4, "priority": 1 },\n'
        '    { "task_name": "Lecture review (part 2)", "estimated_hours": 4, "priority": 2 },\n'
        '    { "task_name": "Seminar review", "estimated_hours": 1, "priority": 3 },\n'
        '    { "task_name": "Notes and outlines (part 1)", "estimated_hours": 2, "priority": 4 },\n'
        '    { "task_name": "Notes and outlines (part 2)", "estimated_hours": 2, "priority": 5 },\n'
        '    { "task_name": "Exam model solving", "estimated_hours": 3, "priority": 6 }\n'
        '  ],\n'
        '  "deadline": "2025-11-10T09:00:00"\n'
        "}"
    )
