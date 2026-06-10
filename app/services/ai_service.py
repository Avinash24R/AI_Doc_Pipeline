import requests

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL_NAME = "deepseek-r1:1.5b"

def chunk_text(
    text: str,
    chunk_size: int = 3000
):

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):
        chunks.append(
            text[i:i+chunk_size]
        )

    return chunks
def summarize_large_document(
    text: str
):

    chunks = chunk_text(text)

    summaries = []

    for chunk in chunks:

        summary = generate_summary(chunk)

        summaries.append(summary)

    combined = "\n".join(summaries)

    final_summary = generate_summary(combined)

    return final_summary

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

