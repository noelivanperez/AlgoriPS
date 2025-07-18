from __future__ import annotations

import os
from urllib.parse import urlparse

import requests


class OllamaClient:
    """Simple client to interact with an Ollama server."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        model: str | None = None,
        *,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
    ) -> None:
        url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        parsed = urlparse(url)
        self.host = host or parsed.hostname or "localhost"
        self.port = port or parsed.port or 11434
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")
        self.temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.7")) if temperature is None else temperature
        self.top_p = float(os.getenv("OLLAMA_TOP_P", "0.9")) if top_p is None else top_p
        self.max_tokens = int(os.getenv("OLLAMA_MAX_TOKENS", "1024")) if max_tokens is None else max_tokens
        self.base_url = f"http://{self.host}:{self.port}"

    def set_model(self, model: str) -> None:
        """Change the target MODEL used for completions."""
        self.model = model

    def set_params(
        self,
        *,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
    ) -> None:
        """Update generation parameters used for completions."""
        if temperature is not None:
            self.temperature = temperature
        if top_p is not None:
            self.top_p = top_p
        if max_tokens is not None:
            self.max_tokens = max_tokens

    def send_prompt(self, prompt: str) -> dict:
        """Send PROMPT to the completions endpoint and return the JSON response."""
        url = f"{self.base_url}/v1/completions"
        payload = {
            "prompt": prompt,
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
