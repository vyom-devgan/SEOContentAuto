# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os

from mistral_client import generate_with_mistral

# ------------ FastAPI Setup ------------
app = FastAPI(title="SEO Content Generator", version="1.0")

# ------------ Request Model ------------
class GenerationRequest(BaseModel):
    keywords: List[str]
    content_type: str = "landing page"
    model: str = "mistral"

# ------------ Prompt Builder ------------
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

# ------------ POST Endpoint ------------
@app.post("/generate")
def generate_seo_content(request: GenerationRequest):
    results = []

    for keyword in request.keywords:
        try:
            prompt = build_prompt(keyword, request.content_type)
            print(f"🔍 Generating for: {keyword}")
            response = generate_with_mistral(prompt, model=request.model)

            md_output = f"# SEO Page: {keyword}\n"
            md_output += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
            md_output += response

            results.append({"keyword": keyword, "content": md_output})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error for '{keyword}': {str(e)}")

    return {"results": results}
