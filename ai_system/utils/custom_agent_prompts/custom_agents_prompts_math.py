# special prompts

# Math

# Practical Exam heuristics
def get_practical_exam_heuristics_math():
    return (
        "Heuristics for Practical Exams:\n"
        "- Typically 7 or 14 laboratories.\n"
        "- Laboratories review: 2-3 hours.\n"
        "- Solving past exam models: 2-3 hours.\n"
        "- Typical total: 4-6 preparation hours.\n\n"
        "Adjust values based on task description realism."
    )


# Practical Exam example
def get_practical_exam_example_math():
    return (
        "Example JSON (for reference only — adapt details as needed):\n"
        "{\n"
        '  "summary": "Preparation for practical exam of medium difficulty (you can include also description info)",\n'
        '  "subject_name/project_name": "Differential Equations",\n'
        '  "total_estimated_hours": 5,\n'
        '  "difficulty": 3,\n'
        '  "tasks": [\n'
        '    { "task_name": "Laboratory review", "estimated_hours": 2, "priority": 1 },\n'
        '    { "task_name": "Exam model solving", "estimated_hours": 3, "priority": 2 },\n'
        '  ],\n'
        '  "deadline": "2025-11-10T09:00:00"\n'
        "}"
    )


# Written Exam heuristics
def get_written_exam_heuristics_math():
    return (
        "Heuristics for Written Exams:\n"
        "- Usually consist of around 14 lectures and 7 or 14 seminars.\n"
        "- Lecture review: ~5 hours total.\n"
        "- Seminar review: 5-8 hours.\n"
        "- Creating additional notes, outlines, and summaries: ~2 hours.\n"
        "- Solving past written exam models: 3–5 hours.\n"
        "- Typical total preparation time: 15–20 hours.\n\n"
        "Adjust the distribution of time and difficulty according to task details and "
        "difficulty level."
    )


# Written Exam example
def get_written_exam_example_math():
    return (
        "Example JSON (for reference only — adapt details as needed):\n"
        "{\n"
        '  "summary": "Preparation for Real Analysis Exam (you can include also description info)",\n'
        '  "subject_name/project_name": "Real Analysis",\n'
        '  "total_estimated_hours": 17,\n'
        '  "difficulty": 3,\n'
        '  "tasks": [\n'
        '    { "task_name": "Lecture review", "estimated_hours": 5, "priority": 1 },\n'
        '    { "task_name": "Seminar review (part 1)", "estimated_hours": 4, "priority": 3 },\n'
        '    { "task_name": "Seminar review (part 2)", "estimated_hours": 2, "priority": 4 },\n'
        '    { "task_name": "Notes and outlines", "estimated_hours": 2, "priority": 5 },\n'
        '    { "task_name": "Exam model solving", "estimated_hours": 4, "priority": 6 }\n'
        '  ],\n'
        '  "deadline": "2025-11-10T09:00:00"\n'
        "}"
    )


# Project heuristics
def get_project_heuristics_math():
    return (
        "Heuristics for Math Projects:\n"
        "- Math projects are usually theoretical, involving proofs, problem sets, small research tasks, or structured reports.\n"
        "- Typical phases: topic review, theoretical development, solving exercises/proofs, writing the report.\n"
        "- Topic review: 0.5–1 hour depending on complexity.\n"
        "- Solving exercises / writing proofs: main workload, typically 1–3 hours depending on difficulty.\n"
        "- Report writing: 0.5–1 hour.\n"
        "- Optional: presentation preparation (0.5 hours) if required.\n"
        "- Subtasks SHOULD NOT exceed 3 hours — split into (part 1), (part 2), etc.\n"
        "- Difficulty mainly affects the number and depth of proofs/problems.\n"
        "- Ensure total_estimated_hours equals the sum of all subtask hours.\n"
        "Adjust the distribution of time and difficulty according to task details and "
        "difficulty level."
    )



# Project example
def get_project_example_math():
    return (
        "Example JSON (for reference only — adapt details as needed):\n"
        "{\n"
        '  "summary": "Work plan for a medium-difficulty math project involving proofs and a short written report.",\n'
        '  "total_estimated_hours": 5,\n'
        '  "difficulty": 3,\n'
        '  "tasks": [\n'
        '    { "task_name": "Topic review", "estimated_hours": 1, "priority": 1 },\n'
        '    { "task_name": "Proof writing (part 1)", "estimated_hours": 2, "priority": 2 },\n'
        '    { "task_name": "Proof writing (part 2)", "estimated_hours": 1, "priority": 3 },\n'
        '    { "task_name": "Report writing", "estimated_hours": 1, "priority": 4 }\n'
        '  ],\n'
        '  "deadline": "2025-11-28T09:00:00"\n'
        "}"
    )



# Assignment heuristics
def get_assignment_heuristics_math():
    return (
        ""
    )


# Assignment example
def get_assignment_example_math():
    return (
        ""
    )
