# test_api.py

from fastapi.testclient import TestClient
from api import app
import os

client = TestClient(app)
VALID_API_KEY = os.getenv("API_KEY") or "test123"

def test_generate_with_valid_key():
    response = client.post(
        "/generate",
        headers={"X-API-KEY": VALID_API_KEY},
        json={
            "keywords": ["secure SEO endpoint test"],
            "content_type": "landing page",
            "model": "mistral"
        }
    )
    assert response.status_code == 200
    assert "results" in response.json()

def test_generate_with_invalid_key():
    response = client.post(
        "/generate",
        headers={"X-API-KEY": "wrong_key"},
        json={
            "keywords": ["should fail"],
            "content_type": "blog",
            "model": "mistral"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API key."

def test_generate_with_missing_key():
    response = client.post(
        "/generate",
        json={
            "keywords": ["no key given"],
            "content_type": "blog",
            "model": "mistral"
        }
    )
    assert response.status_code == 403 or response.status_code == 422  # Depending on header enforcement
