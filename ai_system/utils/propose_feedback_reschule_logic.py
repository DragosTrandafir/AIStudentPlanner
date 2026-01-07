from typing import Any, Dict

from ai_system.utils.feedback_generator_prompts.feedback_instructions import generate_feedback_instructions
from ai_system.utils.get_response import make_llm_call


def propose_feedback_reschedule(
        date,
        client: Any,
        current_feedback: Dict[str, Any],
        last_feedback: Dict[str, Any],
        last_schedule: Dict[str, Any],
) -> str:
    prompt = generate_feedback_instructions(last_feedback, last_schedule, current_feedback, date)
    return make_llm_call(client, prompt, client.model)
