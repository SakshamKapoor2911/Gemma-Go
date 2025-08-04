import ollama

def get_empathy_feedback(text_to_analyze):
    """Sends transcribed text to the locally running Ollama model."""
    prompt = f"""
    You are an expert empathy and communication coach. Your task is to analyze the following text and provide gentle, constructive feedback.
    Analyze the text from three perspectives:
    1.  **Clarity:** How clear is the user's message?
    2.  **Sentiment:** What is the underlying emotion (e.g., frustrated, nervous, confident)?
    3.  **Empathy:** Does the message consider the other person's feelings?

    After your analysis, provide one single, actionable tip in a "Suggestion:" section to help the user communicate more effectively. Keep the feedback concise and encouraging.

    Text to analyze: "{text_to_analyze}"
    """
    try:
        response = ollama.chat(
            model='gemma3n:e2b',
            messages=[{'role': 'user', 'content': prompt}],
        )
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama: {e}"
