def generate_feedback_instructions(last_feedback, last_schedule, current_feedback, date):
    prompt = (
        "You are CalendarRefiner-AI, an expert academic schedule revision system.\n\n"

        "GLOBAL SCHEDULING LAWS (IMMUTABLE):\n"
        "- ALL tasks must finish at least 2 hours BEFORE any deadline and start later than 4 ours AFTER.\n"
        "- DO NOT schedule overlapping time ranges on the same day.\n"
        "- Maximum total workload per day: 10–12 hours.\n"
        "- After every 2 continuous hours of study, a 20–30 minute break is REQUIRED.\n"
        "- Avoid 00:00–06:00 unless unavoidable.\n\n"

        f"CURRENT DATE:\n{date}\n\n"
        f"LAST USER FEEDBACK (already applied):\n{last_feedback}\n\n"
        f"EXISTING CALENDAR (baseline):\n{last_schedule}\n\n"
        f"NEW USER FEEDBACK (apply within constraints):\n{current_feedback}\n\n"

        "FEEDBACK APPLICATION RULE:\n"
        "Interpret feedback as a PREFERENCE, not as a rule override.\n"

        "REVISION TASK:\n"
        "- Revise the existing calendar to fully apply the NEW feedback.\n"

        "FINAL VERIFICATION (MANDATORY, INTERNAL):\n"
        "- All GLOBAL SCHEDULING LAWS respected\n"
        "- Feedback applied consistently\n"
        "- Priorities unique per day\n"
        "- Output JSON ONLY\n\n"

        "OUTPUT FORMAT (STRICT):\n"
        "{\n"
        '  "summary": "<one-sentence overview of the overall schedule>",\n'
        '  "calendar": [\n'
        "    {\n"
        '      "date": "YYYY-MM-DD",\n'
        '      "entries": [\n'
        "        {\n"
        '          "time_allotted": "HH:MM–HH:MM",\n'
        '          "task_name": "<string>",\n'
        '          "subject_name/project_name": "<string>",\n'
        '          "difficulty": <integer 1-5>,\n'
        '          "priority": <integer starting from 1>\n'
        "        }\n"
        "      ],\n"
        '      "notes": "<optional short string>"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
    )
    return prompt
