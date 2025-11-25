# special prompts

# CS

# Practical Exam heuristics
def get_practical_exam_heuristics_cs():
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
def get_practical_exam_example_cs():
    return (
        "Example JSON (for reference only — adapt details as needed):\n"
        "{\n"
        '  "summary": "Preparation for practical exam of medium difficulty (you can include also description info)",\n'
        '  "subject_name/project_name": "Object-Oriented Programming",\n'
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
def get_written_exam_heuristics_cs():
    return (
        "Heuristics for Written Exams:\n"
        "- Usually consist of around 14 lectures and possibly a few seminars.\n"
        "- Lecture review: 7–8 hours total.\n"
        "- Seminar review: 0–1 hours (optional or minor component).\n"
        "- Creating additional notes, outlines, and summaries: 2–4 hours.\n"
        "- Solving past written exam models: 3–4 hours.\n"
        "- Typical total preparation time: 12–17 hours.\n\n"
        "Adjust the distribution of time and difficulty according to task details and "
        "difficulty level."
    )


# Written Exam example
def get_written_exam_example_cs():
    return (
        "Example JSON (for reference only — adapt details as needed):\n"
        "{\n"
        '  "summary": "Preparation for a medium-difficulty Data Structures written exam.",\n'
        '  "subject_name/project_name": "Computer Architecture",\n'
        '  "total_estimated_hours": 14,\n'
        '  "difficulty": 3,\n'
        '  "tasks": [\n'
        '    { "task_name": "Lecture review (part 1)", "estimated_hours": 4, "priority": 1 },\n'
        '    { "task_name": "Lecture review (part 2)", "estimated_hours": 3, "priority": 2 },\n'
        '    { "task_name": "Notes and outlines", "estimated_hours": 3, "priority": 3 },\n'
        '    { "task_name": "Exam model solving", "estimated_hours": 4, "priority": 4 }\n'
        '  ],\n'
        '  "deadline": "2025-11-10T09:00:00"\n'
        "}"
    )


# Project heuristics
def get_project_heuristics_cs():
    return (
        "Heuristics for CS Projects:\n"
        "- CS projects usually involve coding tasks, research, design, and debugging.\n"
        "- Typical phases: planning, implementation, testing, documentation.\n"
        "- Planning / Architecture: 0.5–1 hour.\n"
        "- Implementation (coding): the main workload, 2–4 hours depending on difficulty.\n"
        "- Testing & debugging: usually under 1 hour.\n"
        "- Documentation + Additional notes MUST NOT exceed a combined total of 1 hour.\n"
        "- Example: Documentation = 0.5h and Additional notes = 0.5h.\n"
        "- If the difficulty is high, increase only the implementation/testing time—not documentation.\n"
        "- Subtasks MUST NOT exceed 4 hours — split into logical parts (part 1, part 2, ...).\n"
        "- Ensure total_estimated_hours equals the sum of all subtask hours.\n"
    )

# Project example
def get_project_example_cs():
    return (
        "Example JSON (for reference only — adapt details as needed):\n"
        "{\n"
        '  "summary": "Work plan for a medium-difficulty CS project involving coding and testing.",\n'
        '  "total_estimated_hours": 6,\n'
        '  "difficulty": 3,\n'
        '  "tasks": [\n'
        '    { "task_name": "Project planning & architecture", "estimated_hours": 1, "priority": 1 },\n'
        '    { "task_name": "Core implementation (part 1)", "estimated_hours": 2, "priority": 2 },\n'
        '    { "task_name": "Core implementation (part 2)", "estimated_hours": 1, "priority": 3 },\n'
        '    { "task_name": "Testing & debugging", "estimated_hours": 1, "priority": 4 },\n'
        '    { "task_name": "Documentation", "estimated_hours": 0.5, "priority": 5 },\n'
        '    { "task_name": "Additional notes", "estimated_hours": 0.5, "priority": 6 }\n'
        '  ],\n'
        '  "deadline": "2025-11-28T09:00:00"\n'
        "}"
    )





# Assignment heuristics
def get_assignment_heuristics_cs():
    return (
        ""
    )


# Assignment example
def get_assignment_example_cs():
    return (
        ""
    )
