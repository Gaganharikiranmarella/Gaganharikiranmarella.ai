import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def summarize_transcript(transcript):
    if not transcript.strip():
        return "No content to summarize."
    prompt = (
        "Summarize the following transcript into concise bullet points:\n"
        + transcript
    )
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a summarization assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=data, timeout=15)
        resp.raise_for_status()
        bullets = resp.json()["choices"][0]["message"]["content"]
        return bullets.strip()
    except Exception as e:
        return f"Summarization failed: {e}"
