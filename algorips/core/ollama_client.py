import os
import requests
from typing import Dict, Any


class OllamaClient:
    """Minimal client to interact with an Ollama service."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")

    def generate(self, prompt: str, model: str = "llama2") -> Dict[str, Any]:
        """Send a prompt to the Ollama service and return the response."""
        url = f"{self.base_url}/api/generate"
        response = requests.post(url, json={"model": model, "prompt": prompt})
        response.raise_for_status()
        return response.json()
