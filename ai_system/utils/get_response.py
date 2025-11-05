# flask
def make_llm_call(client,prompt,model_name):
    # Attempt chat_completion
    try:
        reply = client.chat_completion(messages=[{"role": "user", "content": prompt}],
                                       temperature=0.6)
        # Ensure the content extraction is correct based on the client type
        response = getattr(reply.choices[0].message, 'content', str(reply.choices[0].message))
    # Fallback to text_generation
    except Exception as e_chat:
        print(f"Chat completion failed for {model_name}: {e_chat}")
        try:
            reply = client.text_generation(prompt, temperature=0.6)
            response = reply
        except Exception as e_text:
            print(f"Text generation failed for {model_name}: {e_text}")
            response = "Could not complete response."
    return response
