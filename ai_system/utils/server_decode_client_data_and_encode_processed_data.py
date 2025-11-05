import json
from huggingface_hub import InferenceClient
from get_response import make_llm_call


def decode_encode(data_to_decode, token):
    decoded = json.loads(data_to_decode.decode("utf-8"))
    prompt = decoded[1]
    model_name = decoded[2]

    client = InferenceClient(model=model_name, token=token)
    response = make_llm_call(client, prompt, model_name)
    response_encoded = response.encode("utf-8")

    return response_encoded
