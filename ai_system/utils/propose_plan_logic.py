from ai_system.utils.calendar_generator_prompts.calendar_instructions import generate_calendar_instructions
from ai_system.utils.custom_agent_prompts.custom_agents_prompts_cs import (
    get_practical_exam_heuristics_cs,
    get_practical_exam_example_cs,
    get_written_exam_heuristics_cs,
    get_written_exam_example_cs, get_project_heuristics_cs, get_project_example_cs, get_assignment_heuristics_cs,
    get_assignment_example_cs,
)
from ai_system.utils.custom_agent_prompts.custom_agents_prompts_math import (
    get_practical_exam_heuristics_math,
    get_practical_exam_example_math,
    get_written_exam_heuristics_math,
    get_written_exam_example_math, get_project_heuristics_math, get_project_example_math,
    get_assignment_heuristics_math, get_assignment_example_math,
)
from ai_system.utils.custom_agent_prompts.custom_agents_prompts_general import (
    get_role_prompt,
    get_general_heuristics_header,
    get_input_output_instructions,
)
from ai_system.utils.get_response import make_llm_call


def propose_plan(task, general_university_type, client):
    title = task['title']
    name = task['subject_name/project_name']
    start_datetime = task['start_datetime']
    end_datetime = task['end_datetime']
    type_ = task['type'].lower()  # Normalize to lowercase
    difficulty = task['difficulty']
    description = task['description']
    status = task['status']

    # Define a configuration map for all possible (exam type, university type) pairs
    # Keys use lowercase type values to match backend enums: "written", "practical", "project"
    prompt_map = {
        ("practical", "Computer Science"): (
            get_practical_exam_heuristics_cs,
            get_practical_exam_example_cs,
        ),
        ("practical", "Mathematics"): (
            get_practical_exam_heuristics_math,
            get_practical_exam_example_math,
        ),
        ("written", "Computer Science"): (
            get_written_exam_heuristics_cs,
            get_written_exam_example_cs,
        ),
        ("written", "Mathematics"): (
            get_written_exam_heuristics_math,
            get_written_exam_example_math,
        ),
        ("project", "Computer Science"): (
            get_project_heuristics_cs,
            get_project_example_cs,
        ),
        ("project", "Mathematics"): (
            get_project_heuristics_math,
            get_project_example_math,
        ),
        ("assignment", "Computer Science"): (
            get_assignment_heuristics_cs,
            get_assignment_example_cs,
        ),
        ("assignment", "Mathematics"): (
            get_assignment_heuristics_math,
            get_assignment_example_math,
        ),
    }

    # Get the right functions for the given combination
    heuristics_func, example_func = prompt_map.get((type_, general_university_type), (None, None))
    if not heuristics_func:
        raise ValueError(f"Unsupported combination: {type_} + {general_university_type}")

    # Build the full prompt cleanly
    parts = [
        get_role_prompt(type_, general_university_type),
        get_general_heuristics_header(),
        heuristics_func(),
        get_input_output_instructions(
            title, name, start_datetime, end_datetime, type_, difficulty, description, status
        ),
        example_func(),
    ]

    full_prompt = "\n\n".join(parts)
    return make_llm_call(client, full_prompt, client.model)


def propose_calendar(plans_array, date, client):
    prompt = generate_calendar_instructions(plans_array,date)
    return make_llm_call(client, prompt, client.model)
