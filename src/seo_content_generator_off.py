import os
import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama's local API

def build_prompt(keyword: str) -> str:
    return f"""
You are a professional SEO content writer. Write a fully optimized SEO landing page in Markdown about: "{keyword}"

Include:
1. SEO Title
2. Meta description (max 160 characters)
3. Intro paragraph
4. Three structured subheadings with 3–5 sentences each
5. A strong call to action
Return only the Markdown content.
"""

def query_ollama(prompt: str, model: str = "mistral"):
    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        raise Exception(f"Ollama error: {response.status_code} - {response.text}")

def save_to_markdown(keyword, content, output_dir="generated_pages"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{keyword.replace(' ', '_').lower()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# SEO Content for: {keyword}\n")
        f.write(f"*Generated on {datetime.now()}*\n\n")
        f.write(content)

def load_keywords(csv_file="keywords.csv"):
    df = pd.read_csv(csv_file)
    return df['keyword'].dropna().tolist()

def main():
    keywords = load_keywords()
    print(f"🧠 {len(keywords)} keywords found.")

    for kw in keywords:
        print(f"⚙️  Generating for: {kw}")
        try:
            prompt = build_prompt(kw)
            result = query_ollama(prompt)
            save_to_markdown(kw, result)
            print(f"✅ Done: {kw}")
        except Exception as e:
            print(f"❌ Error for {kw}: {e}")

if __name__ == "__main__":
    main()
