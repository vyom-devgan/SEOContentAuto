import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set in .env file.")

genai.configure(api_key=api_key)

# Fully free forever embedding model (no generation)
embedding_model = genai.GenerativeModel("models/embedding-gecko-001")

def embed_keyword(keyword: str):
    try:
        response = embedding_model.embed_text(keyword)
        return response.embeddings[0]  # vector embedding
    except Exception as e:
        print(f"❌ Error generating embedding for '{keyword}': {e}")
        return None

def generate_content(keyword: str) -> str:
    # Content generation is not free forever on Google Cloud
    # So, here we do NOT call any paid generate_content API to avoid cost
    print(f"⚠️ Making Generation for '{keyword}' — using Google Cloud vector embedding - embedding-gecko-001.")
    return f"**The keyword for embedding is '{keyword}' - using Google Cloud vector embedding - embedding-gecko-001]**"

def save_to_markdown(keyword: str, content: str, output_dir="generated_pages"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, keyword.replace(" ", "_").lower() + ".md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# SEO Page – {keyword}\n")
        f.write(f"*Generated on {datetime.now():%Y-%m-%d %H:%M:%S}*\n\n")
        f.write(content)

def load_keywords(csv_file="keywords.csv"):
    try:
        return pd.read_csv(csv_file)['keyword'].dropna().tolist()
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return []

def main():
    keywords = load_keywords()
    print(f"📄 {len(keywords)} keywords found.")
    for kw in keywords:
        print(f"⚙️ Generating embedding for: {kw}")
        embedding = embed_keyword(kw)
        if embedding is not None:
            print(f"✅ Embedding generated for: {kw}")
        else:
            print(f"⚠️ Embedding failed for: {kw}")

        print(f"⚙️ Generating content for: {kw}")
        content = generate_content(kw)
        save_to_markdown(kw, content)
        print(f"✅ Saved: {kw}")

if __name__ == "__main__":
    main()
