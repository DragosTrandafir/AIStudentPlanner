import json
import re
from datetime import datetime, date as date_type
from typing import Any, Dict, List, Tuple

from ai_system.utils.get_response import make_llm_call


TimeWindow = Tuple[str, str]  # ("HH:MM", "HH:MM")


def _normalize_time_str(t: str) -> str:
    """
    Normalize things like "13", "13:0", "13.00" to "HH:MM" (24h).
    """
    t = t.strip().replace(".", ":")
    # Keep only first ':' if multiple
    if ":" in t:
        h, m = t.split(":", 1)
    else:
        h, m = t, "00"

    h = h.strip()
    m = m.strip()
    if not h.isdigit():
        return ""
    if not m.isdigit():
        m = "00"

    h_int = max(0, min(23, int(h)))
    m_int = max(0, min(59, int(m)))
    return f"{h_int:02d}:{m_int:02d}"


def extract_forbidden_windows(feedback_text: str) -> List[TimeWindow]:
    """
    Extract forbidden time windows from natural language feedback, e.g.:

    "Do not include any learning activity between 13 and 14:30 a.m."
      -> [("13:00", "14:30")]

    Patterns handled:
      - "between 13 and 14:30"
      - "13 - 14:30"
      - "13:00–14:30"
      - "13 to 14:30"
    """
    if not feedback_text:
        return []

    text = feedback_text.lower()
    text = text.replace("a.m.", "").replace("am", "")
    text = text.replace("p.m.", "").replace("pm", "")

    windows: List[TimeWindow] = []

    # 1) "between X and Y"
    between_pattern = r'between\s+(\d{1,2}(?::\d{1,2})?)\s*and\s*(\d{1,2}(?::\d{1,2})?)'
    for start_raw, end_raw in re.findall(between_pattern, text):
        start = _normalize_time_str(start_raw)
        end = _normalize_time_str(end_raw)
        if not start or not end:
            continue
        s_h, s_m = map(int, start.split(":"))
        e_h, e_m = map(int, end.split(":"))
        if (e_h, e_m) <= (s_h, s_m):
            continue
        windows.append((start, end))

    # 2) Generic ranges: "X - Y", "X–Y", "X to Y"
    range_pattern = r'(\d{1,2}(?::\d{1,2})?)\s*(?:-|–|to)\s*(\d{1,2}(?::\d{1,2})?)'
    for start_raw, end_raw in re.findall(range_pattern, text):
        start = _normalize_time_str(start_raw)
        end = _normalize_time_str(end_raw)
        if not start or not end:
            continue
        s_h, s_m = map(int, start.split(":"))
        e_h, e_m = map(int, end.split(":"))
        if (e_h, e_m) <= (s_h, s_m):
            continue
        # avoid duplicates from the "between" match
        if (start, end) not in windows:
            windows.append((start, end))

    return windows


def _time_to_minutes(t: str) -> int:
    """Convert 'HH:MM' to minutes from midnight."""
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _parse_time_range(time_range: str) -> Tuple[str, str]:
    """
    Parse "HH:MM–HH:MM" or "HH:MM-HH:MM" into ("HH:MM", "HH:MM").
    Returns ("", "") if invalid.
    """
    if not time_range:
        return "", ""
    # Support different dash characters
    parts = re.split(r"\s*[–-]\s*", time_range.strip())
    if len(parts) != 2:
        return "", ""
    start = _normalize_time_str(parts[0])
    end = _normalize_time_str(parts[1])
    if not start or not end:
        return "", ""
    return start, end


def enforce_schedule_constraints(
    plan: Dict[str, Any],
    forbidden_windows: List[TimeWindow],
    today: date_type,
) -> Dict[str, Any]:
    """
    Post-process the LLM-generated plan to guarantee:

    - No study block overlaps any forbidden window.
    - Priorities restart from 1 for each day and have no gaps.

    NOTE:
    - We DO NOT delete blocks just because they are in the past anymore.
      "Never schedule tasks in the past" is enforced at prompt-level by the LLM.
    """
    calendar = plan.get("calendar")
    if not isinstance(calendar, list):
        return plan

    # Pre-compute forbidden intervals in minutes
    forbidden_minutes: List[Tuple[int, int]] = []
    for start, end in forbidden_windows:
        try:
            s = _time_to_minutes(start)
            e = _time_to_minutes(end)
        except Exception:
            continue
        if e <= s:
            continue
        forbidden_minutes.append((s, e))

    def overlaps_forbidden(start_min: int, end_min: int) -> bool:
        for fs, fe in forbidden_minutes:
            # overlap if intervals intersect with non-empty intersection
            if not (end_min <= fs or start_min >= fe):
                return True
        return False

    for day in calendar:
        date_str = day.get("date")
        if not isinstance(date_str, str):
            continue

        # Parse date only to ensure it's valid (we don't drop past days here)
        try:
            _ = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            continue

        entries = day.get("entries", [])
        if not isinstance(entries, list):
            day["entries"] = []
            continue

        cleaned_entries = []
        for entry in entries:
            time_range = entry.get("time_allotted", "")
            start_str, end_str = _parse_time_range(time_range)
            if not start_str or not end_str:
                # invalid time range -> drop this entry
                continue

            start_min = _time_to_minutes(start_str)
            end_min = _time_to_minutes(end_str)
            if end_min <= start_min:
                # invalid or zero-length -> drop
                continue

            if forbidden_minutes and overlaps_forbidden(start_min, end_min):
                # Violates forbidden window -> drop this block
                continue

            cleaned_entries.append(entry)

        # Reassign priorities 1..n for this day
        for idx, e in enumerate(cleaned_entries, start=1):
            e["priority"] = idx

        day["entries"] = cleaned_entries

    return plan


def propose_feedback_reschedule(
    date: datetime,
    client: Any,
    current_feedback: Dict[str, Any],
    last_feedback: Dict[str, Any],
    last_schedule: Dict[str, Any],
) -> str:
    """
    Build the prompt and call the LLM.

    It does NOT parse JSON here; it just returns the raw LLM text.
    JSON parsing + constraint enforcement happens in the agent.
    """
    current_fb_str = json.dumps(current_feedback, indent=2, ensure_ascii=False)
    last_fb_str = json.dumps(last_feedback, indent=2, ensure_ascii=False)
    last_schedule_str = json.dumps(last_schedule, indent=2, ensure_ascii=False)

    feedback_text = current_feedback.get("text", "") or ""
    forbidden_windows = extract_forbidden_windows(feedback_text)
    windows_str = (
        ", ".join([f"{start}–{end}" for start, end in forbidden_windows])
        if forbidden_windows
        else "none detected"
    )

    today_str = date.date().isoformat() if isinstance(date, datetime) else str(date)

    role_and_context = (
        "You are an expert academic planner specialized in rescheduling study plans.\n\n"
        f"TODAY'S DATE: {today_str}\n\n"
        "You receive:\n"
        "1) CURRENT_FEEDBACK (highest priority, MUST be enforced)\n"
        "2) LAST_FEEDBACK (context only)\n"
        "3) LAST_SCHEDULE (base schedule to MODIFY)\n\n"
        f"FORBIDDEN STUDY WINDOWS (24h format, MUST NOT CONTAIN STUDY): {windows_str}\n\n"
        "RAW CURRENT_FEEDBACK TEXT (for understanding the constraint):\n"
        f"{feedback_text}\n\n"
        "CURRENT_FEEDBACK (full object):\n"
        f"{current_fb_str}\n\n"
        "LAST_FEEDBACK:\n"
        f"{last_fb_str}\n\n"
        "LAST_SCHEDULE:\n"
        f"{last_schedule_str}\n\n"
    )

    rules = (
        "YOUR TASK:\n"
        "- Update LAST_SCHEDULE so that it fully respects CURRENT_FEEDBACK.\n"
        "- Apply the FORBIDDEN STUDY WINDOWS strictly.\n\n"

        "HARD CONSTRAINTS:\n"
        "- ONLY use the time intervals explicitly listed in FORBIDDEN STUDY WINDOWS as forbidden.\n"
        "- Do NOT invent or assume any additional forbidden hours.\n"
        "- For every window [START, END] in FORBIDDEN STUDY WINDOWS, "
        "no study block may overlap that interval (even partially).\n"
        "- Any violating block MUST be moved or split.\n"
        "- NEVER schedule tasks in the past relative to TODAY'S DATE.\n"
        "- Respect implied deadlines from task names or dates.\n"
        "- Keep the original structure when possible; change ONLY what is needed.\n\n"

        "WORKLOAD RULES:\n"
        "- Maximum about 6 study hours per day.\n"
        "- Human realistic hours only (07:00–22:00).\n"
        "- Prefer moving existing blocks instead of creating new days.\n\n"

        "PRIORITY RULES:\n"
        "- For EACH DAY, priorities start again at 1.\n"
        "- For each day's entries, priority values must be 1, 2, 3, ... with NO gaps.\n\n"
    )

    json_schema = (
        "OUTPUT FORMAT — STRICT JSON ONLY (no markdown, no extra text):\n\n"
        "{\n"
        '  \"summary\": \"Short explanation of the changes you made.\",\n'
        '  \"calendar\": [\n'
        "    {\n"
        '      \"date\": \"YYYY-MM-DD\",\n'
        '      \"entries\": [\n'
        "        {\n"
        '          \"time_allotted\": \"HH:MM–HH:MM\",\n'
        '          \"task_name\": \"string\",\n'
        '          \"difficulty\": 1,\n'
        '          \"priority\": 1\n'
        "        }\n"
        "      ],\n"
        '      \"notes\": \"string (can be empty)\"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "FINAL CHECK BEFORE YOU ANSWER:\n"
        "1) No study block overlaps any FORBIDDEN STUDY WINDOW.\n"
        "2) No study block is scheduled before TODAY'S DATE.\n"
        "3) Priorities for each day start at 1 and have no gaps.\n"
        "4) The response is VALID JSON and can be parsed directly.\n"
    )

    prompt = role_and_context + rules + json_schema

    return make_llm_call(client, prompt, client.model)
