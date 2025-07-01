# SEO Content Auto Generator

A Python-based toolkit for generating SEO-optimized content and embeddings for keywords using local LLMs (Ollama + Mistral) and Google Generative AI embeddings. Includes:
- CLI and script-based content generation
- FastAPI web API for programmatic access
- Google Embedding support
- Markdown output for easy publishing

## Features
- **Generate SEO landing pages** using local LLMs (Ollama + Mistral)
- **Google Embedding**: Get vector embeddings for keywords (free forever)
- **Batch processing** from CSV files
- **API access** via FastAPI
- **Customizable prompts and output**
- **Error logging**

## Requirements
- Python 3.8+
- [Ollama](https://ollama.com/) (for local LLM content generation)
- Google Generative AI API key (for embeddings)

## Installation
1. Clone this repo:
   ```sh
   git clone https://github.com/vyom-devgan/SEOContentAuto.git
   cd SEOContentAuto
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up your `.env` file:
   ```env
   GOOGLE_API_KEY=your-google-api-key
   # Optional: OLLAMA_BASE_URL=http://localhost:11434
   ```

## Usage

### 1. Generate SEO Content via CLI
Run the enhanced generator (Ollama + Mistral):
```sh
python seo_content_generator_enhanced.py --csv keywords.csv --model mistral:instruct --output generated_pages --content-type "landing page"
```

### 2. Generate Embeddings (Google)
Run the Google embedding script:
```sh
python seo_content_generator.py
```

### 3. Generate Content via FastAPI
Start the API server:
```sh
uvicorn api:app --reload
```
Then POST to `/generate` with JSON:
```json
{
  "keywords": ["Bill Gates", "best eSIM for travel"],
  "content_type": "landing page",
  "model": "mistral"
}
```

### 4. Generate Content (Offline, Ollama only)
```sh
python seo_content_generator_off.py
```

### 5. Main Script (Simple CLI)
```sh
python main.py
```

## File Structure
- `seo_content_generator_enhanced.py` — Main CLI for Ollama/Mistral content
- `seo_content_generator.py` — Google embedding generator
- `seo_content_generator_off.py` — Offline Ollama content generator
- `main.py` — Simple CLI for content generation
- `api.py` — FastAPI server
- `mistral_client.py` — Ollama API client
- `keywords.csv` — Input keywords (edit as needed)
- `generated_pages/` — Output Markdown files
- `logs/` — Error logs

## Notes
- Make sure Ollama is running (`ollama serve`) and the model (e.g., `mistral:instruct`) is pulled (`ollama pull mistral:instruct`).
- Google content generation is not free, but embeddings are.
- All output is in Markdown for easy publishing.

## Example
Sample `keywords.csv`:
```csv
keyword
Bill Gates
best eSIM for international travel
global SIM cards for business
```
