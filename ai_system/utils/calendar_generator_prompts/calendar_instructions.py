def generate_calendar_instructions(plans_array, date):
    role = (
        f"You are an expert academic planner and coordination agent. "
        f"You have received an array of project analyses from smaller agents. "
        f"Each element in the array contains information in JSON-like form, including: "
        f"a summary, total_estimated_hours, difficulty level, list of tasks, and a deadline. "
        f"Here is the array of small-agent results:\n\n{plans_array}\n\n"
        f"Today’s date is {date}."
    )

    goal = (
        "Your job is to integrate and coordinate all tasks from these plans into a single, unified daily calendar. "
        "Distribute work intelligently across the available days until each plan’s deadline, ensuring a realistic "
        "workload."
        "Return a single valid JSON object following the structure below — "
        "no explanations, no Markdown, no comments, and no trailing commas."
    )

    json_structure = (
        "The JSON must have the following structure:\n\n"
        "{\n"
        '  "summary": "One-sentence overview of the overall schedule.",\n'
        '  "calendar": [\n'
        '    {\n'
        '      "day": "Monday",\n'
        '      "date": "2025-12-11",\n'
        '      "entries": [\n'
        '        {\n'
        '          "time": "10:00–12:00",\n'
        '          "task_name": <string>,\n'
        '          "source_plan": <string>,\n'
        '          "estimated_hours": <integer>,\n'
        '          "difficulty": <integer from 1–5>,\n'
        '          "priority": <integer starting from 1>\n'
        '        }\n'
        '      ],\n'
        '      "notes": "Optional daily note (e.g., breaks, rest, or review)."\n'
        '    }\n'
        '  ]\n'
        "}\n\n"
    )

    rules = (
        "SCHEDULING RULES:\n"
        "- Respect all deadlines in the input array.\n"
        "- Balance high-difficulty tasks so they are not scheduled back-to-back.\n"
        "- Include breaks if daily total exceeds 4 hours; minimum 30 minutes.\n"
        "- Avoid scheduling multiple complex tasks in a single day.\n"
        "- Spread work evenly, preferring lighter days after demanding ones.\n"
        "- Limit to one major task on the day of or immediately before a deadline.\n"
        "- If tasks from different plans overlap, prioritize those with earlier deadlines or higher difficulty.\n"
        "- Output must be only valid JSON according to the schema above — no extra commentary."
    )

    calendar_prompt = f"{role}\n\n{goal}\n\n{json_structure}\n\n{rules}"
    return calendar_prompt
