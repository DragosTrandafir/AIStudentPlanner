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
