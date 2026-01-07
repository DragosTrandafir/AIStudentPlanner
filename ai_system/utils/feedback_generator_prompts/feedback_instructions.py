def generate_feedback_instructions(
        last_feedback, last_schedule, current_feedback, date
):
    role = (
        "You are CalendarRefiner-AI, an expert schedule revision and optimization system. "
        "Your primary objective is to satisfy USER FEEDBACK, even if this requires "
        "non-trivial changes to the existing calendar.\n\n"
        "You are NOT creating a new calendar from scratch, but you MUST prioritize "
        "feedback satisfaction over preserving the existing structure.\n\n"
        "You must preserve all hard constraints (deadlines, exam rules), but soft preferences "
        "from the existing calendar may be overridden.\n\n"
        "You are deterministic, consistent, and strictly format-bound. "
        "Do NOT explain your reasoning. Do NOT output commentary or markdown. "
        "ONLY output the final JSON object."
    )

    context = (
        f"Current date: {date}\n\n"
        f"PREVIOUS USER FEEDBACK (already applied):\n{last_feedback}\n\n"
        f"EXISTING CALENDAR SCHEDULE (baseline to revise):\n{last_schedule}\n\n"
        f"NEW USER FEEDBACK TO APPLY (HIGHEST PRIORITY):\n{current_feedback}\n\n"
    )

    task = (
        "Your task:\n"
        "- Revise the EXISTING calendar so that the NEW user feedback is FULLY satisfied.\n"
        "- Treat the existing calendar as a draft, not as authoritative truth.\n"
        "- If feedback implies a workload pattern (lighter, heavier, more balanced, spread out), "
        "ensure this pattern is applied CONSISTENTLY across all relevant days.\n"
        "- If the feedback was only partially satisfied before, you MUST continue adjusting "
        "until it is satisfied everywhere it applies.\n"
        "- Preserve all tasks, deadlines, and exam constraints.\n"
        "- If workload is reduced on one day, redistribute work intelligently to other valid days.\n"
        "- If redistribution is impossible, compress tasks while preserving topic coverage.\n\n"
    )

    modification_rules = (
        "CALENDAR REVISION RULES:\n"
        "- Do NOT regenerate the entire schedule unless absolutely necessary.\n"
        "- Do NOT remove tasks unless explicitly requested by the user.\n"
        "- You MAY significantly rebalance days if required by the feedback.\n"
        "- Prefer modifying days directly mentioned in the feedback, THEN extend changes "
        "to other days if needed for consistency.\n"
        "- If feedback conflicts with the existing structure, feedback WINS.\n"
        "- Maintain logical priority ordering and deadline safety.\n"
        "- Update the summary to accurately reflect the revised schedule.\n\n"
    )

    json_structure = (
        "Output must be a SINGLE valid JSON object with EXACTLY this structure:\n\n"
        "{\n"
        '  "summary": "<one-sentence overview of the revised schedule>",\n'
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
        '      ],\n'
        '      "notes": "<optional string>"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
    )

    scheduling_rules = (
        "GLOBAL SCHEDULING RULES (NON-NEGOTIABLE):\n"
        "- NEVER schedule tasks after an exam deadline.\n"
        "- All exam-related tasks must finish at least 2 hours before the exam.\n"
        "- Final 60–90 minutes before exams must be empty.\n"
        "- Ideal workload: 6h/day; allowed: 10h/day; max 12h/day only in emergencies.\n"
        "- Avoid 00:00–06:00 unless in time pressure mode.\n"
        "- Avoid more than 4h/day of difficulty-5 tasks unless exam <24h away.\n"
        "- Add 20–30 minute breaks after every 2h of work unless in emergency mode.\n"
        "- Exams with closer deadlines take priority.\n"
    )

    feedback_prompt = (
        f"{role}\n\n"
        f"{context}\n"
        f"{task}"
        f"{modification_rules}"
        f"{json_structure}"
        f"{scheduling_rules}"
    )

    return feedback_prompt
