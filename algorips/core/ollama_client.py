from __future__ import annotations

import requests


class OllamaClient:
    """Simple client to interact with an Ollama server."""

    def __init__(self, host: str = "localhost", port: int = 11434) -> None:
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    def send_prompt(self, prompt: str) -> dict:
        """Send PROMPT to the completions endpoint and return the JSON response."""
        url = f"{self.base_url}/v1/completions"
        response = requests.post(url, json={"prompt": prompt})
        response.raise_for_status()
        return response.json()
