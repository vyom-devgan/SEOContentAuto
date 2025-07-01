# api.py

from fastapi import FastAPI, HTTPException, Header, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import logging

from mistral_client import generate_with_mistral
from dotenv import load_dotenv

# ------------ SETUP ------------
app = FastAPI(title="🔐 SEO Content Generator", version="1.1")

load_dotenv()
API_KEY = os.getenv("API_KEY")

# Create folders
os.makedirs("logs", exist_ok=True)
os.makedirs("generated_pages", exist_ok=True)

# Logging Configurations
logging.basicConfig(level=logging.INFO)
error_log = logging.getLogger("error_logger")
usage_log = logging.getLogger("usage_logger")

# Separate log files
error_handler = logging.FileHandler("logs/error.log")
error_handler.setLevel(logging.ERROR)
error_log.addHandler(error_handler)

usage_handler = logging.FileHandler("logs/usage.log")
usage_handler.setLevel(logging.INFO)
usage_log.addHandler(usage_handler)

# ------------ AUTH CHECK + LOGGING ------------
def verify_api_key(request: Request, x_api_key: Optional[str] = Header(None)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not set.")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key.")

    # Log the usage
    usage_log.info(f"{datetime.now()} - {request.client.host} - {request.method} {request.url.path} - Used API_KEY: {x_api_key}")
    return True

# ------------ REQUEST MODEL ------------
class GenerationRequest(BaseModel):
    keywords: List[str]
    content_type: str = "landing page"
    model: str = "mistral"

# ------------ PROMPT GENERATOR ------------
def build_prompt(keyword: str, content_type: str) -> str:
    return f"""
You are a professional SEO content writer. Write a high-quality {content_type} in Markdown format for the topic: "{keyword}".

Include:
1. SEO-friendly title
2. Meta description (under 160 characters)
3. Engaging introduction
4. 3 informative subheadings with detailed paragraphs
5. Strong call to action
6. Use Markdown formatting properly
"""

# ------------ MARKDOWN SAVER ------------
def save_to_markdown(keyword: str, content: str, output_dir: str = "generated_pages"):
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

# ------------ MAIN POST ROUTE ------------
@app.post("/generate", dependencies=[Depends(verify_api_key)])
def generate_seo_content(request: GenerationRequest):
    results = []

    for keyword in request.keywords:
        try:
            prompt = build_prompt(keyword, request.content_type)
            print(f"🔍 Generating for: {keyword}")
            content = generate_with_mistral(prompt, model=request.model)

            save_to_markdown(keyword, content)
            results.append({
                "keyword": keyword,
                "message": "✅ Generated and saved",
                "filename": f"{keyword.replace(' ', '_').lower()}.md"
            })

        except Exception as e:
            error_log.error(f"❌ Failed for {keyword}: {e}")
            raise HTTPException(status_code=500, detail=f"Error for '{keyword}': {str(e)}")

    return {"results": results}
