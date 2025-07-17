from __future__ import annotations

import os
from urllib.parse import urlparse

import requests


class OllamaClient:
    """Simple client to interact with an Ollama server."""

    def __init__(
        self, host: str | None = None, port: int | None = None, model: str | None = None
    ) -> None:
        url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        parsed = urlparse(url)
        self.host = host or parsed.hostname or "localhost"
        self.port = port or parsed.port or 11434
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")
        self.base_url = f"http://{self.host}:{self.port}"

    def set_model(self, model: str) -> None:
        """Change the target MODEL used for completions."""
        self.model = model

    def send_prompt(self, prompt: str) -> dict:
        """Send PROMPT to the completions endpoint and return the JSON response."""
        url = f"{self.base_url}/v1/completions"
        payload = {"prompt": prompt, "model": self.model}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
