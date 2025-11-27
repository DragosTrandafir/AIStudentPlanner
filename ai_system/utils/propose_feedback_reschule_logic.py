from ai_system.utils.get_response import make_llm_call


def propose_feedback_reschedule(date, client,current_feedback,last_feedback,last_schedule):
    prompt = "" # prompts for reschuling
    return make_llm_call(client, prompt, client.model)

