import requests

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL_NAME = "phi3:mini"

def generate_summary(text: str) -> str:
    if not text:
        return ""

    prompt = f"""
    Summarize the following document in 5-10 concise bullet points.

    Document:
    {text[:6000]}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]

