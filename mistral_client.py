import requests
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def generate_with_mistral(prompt, model="mistral:instruct"):
    """
    Calls the Ollama API to generate content using the specified model and prompt.
    Returns the generated text as a string.
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except Exception as e:
        raise RuntimeError(f"Ollama API error: {e}")
