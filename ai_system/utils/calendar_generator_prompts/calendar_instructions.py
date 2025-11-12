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
        "Return a single valid JSON object following the structure below:\n\n"
    )

    json_structure = (
        "{\n"
        '  "summary": "One-sentence overview of the overall schedule.",\n'
        '  "calendar": [\n'
        '    {\n'
        '      "date": "year-month-day",\n'
        '      "entries": [\n'
        '        {\n'
        '          "time_allotted": "HH:HH–HH:HH",\n'
        '          "task_name": <string>,\n'
        '          "difficulty": <integer from 1–5>,\n'
        '          "priority": <integer starting from 1>\n'
        '        },...\n'
        '      ],\n'
        '      "notes": "Optional daily note (e.g., breaks, rest, or review)."\n'
        '    }\n'
        '  ]\n'
        "}\n\n"
    )

    rules = (
        "SCHEDULING RULES:\n"
        "- Each plan has a 'deadline' that represents the exam date and time.\n"
        "- Absolutely NO tasks may be scheduled:\n"
        "  • On the same calendar day as the exam after its deadline time.\n"
        "  • Within 2 hours before the exam's deadline time.\n"
        "  • After the deadline date at all.\n"
        "- Example: if the deadline is 2025-11-15T09:00:00, all study tasks for that exam "
        "must end by 07:00 on 2025-11-15 at the latest.\n"
        "- Balance high-difficulty tasks so they are not scheduled back-to-back.\n"
        "- Include breaks after 2 hours of continuous activity (20–30 minutes).\n"
        "- Avoid scheduling multiple complex tasks in a single day unless the deadline compels it.\n"
        "- Spread work evenly, preferring lighter days after demanding ones, if deadlines allow.\n"
        "- Respect task priorities and difficulties in the final schedule.\n"
        "- If possible, do not schedule more than 6 hours of learning a day, try to even out the days.\n"
        "- If possible, ensure that the student does not work between 12 am and 6 am and gets at least 6-7 hours of "
        "sleep per night.\n"

    )

    calendar_prompt = f"{role}\n\n{goal}\n\n{json_structure}\n\n{rules}"
    return calendar_prompt
