import os
import logging
from datetime import datetime
import pandas as pd
from mistral_client import generate_with_mistral
from dotenv import load_dotenv

# ---------------------------- SETUP ----------------------------

load_dotenv()

# Constants
CSV_FILE = "keywords.csv"
OUTPUT_DIR = "generated_pages"
MODEL = "mistral"
CONTENT_TYPE = "landing page"

# Create folders
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Logging
logging.basicConfig(
    filename="logs/error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------- PROMPT ----------------------------

def build_prompt(keyword: str, content_type: str = "landing page") -> str:
    return f"""
You are a professional SEO content writer. Write a high-quality {content_type} in Markdown format for the topic: "{keyword}".

Structure it with:
1. SEO-friendly title
2. Meta description (under 160 characters)
3. Short engaging introduction
4. 3 informative subheadings with detailed paragraphs
5. A strong call to action
6. Use Markdown formatting properly.
"""

# ---------------------------- GENERATE CONTENT ----------------------------

def generate_content(keyword: str, model: str, content_type: str) -> str:
    prompt = build_prompt(keyword, content_type)
    try:
        return generate_with_mistral(prompt, model=model)
    except Exception as e:
        logging.error(f"Error generating for '{keyword}': {e}")
        return None

# ---------------------------- SAVE TO MARKDOWN ----------------------------

def save_to_markdown(keyword: str, content: str, output_dir: str):
    safe_name = keyword.replace(" ", "_").lower()
    filename = os.path.join(output_dir, f"{safe_name}.md")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = f"""---
    title: "{keyword.title()} | SEO Page"
    date: {timestamp}
    tags: [SEO, AI, Content, Landing Page]
    generated_by: Mistral via Ollama
    ---

    # {keyword.title()}

    > *Generated on {timestamp} using the Mistral open-source LLM engine.*

    ---

    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(content.strip())
        f.write("\n\n---\n")
        f.write("_End of page_\n")

# ---------------------------- MAIN ----------------------------

def main():
    try:
        df = pd.read_csv(CSV_FILE)
        keywords = df['keyword'].dropna().tolist()
        print(f"📄 Loaded {len(keywords)} keywords from '{CSV_FILE}'")

        for kw in keywords:
            print(f"\n⚙️  Generating for: {kw}")
            content = generate_content(kw, MODEL, CONTENT_TYPE)
            if content:
                save_to_markdown(kw, content, OUTPUT_DIR)
                print(f"✅ Saved: {kw}")
            else:
                print(f"⚠️ Skipped: {kw}")

    except Exception as e:
        logging.error(f"Failed to load keywords from '{CSV_FILE}': {e}")
        print(f"❌ Could not load keywords. Check logs/error.log")

if __name__ == "__main__":
    main()
