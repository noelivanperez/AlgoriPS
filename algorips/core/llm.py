from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from typing import List

import requests

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract interface for language model providers."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    @abstractmethod
    def list_models(self) -> List[str]:
        """Return a list of available model names."""

    @abstractmethod
    def send_prompt(self, prompt: str, model: str) -> dict:
        """Send *prompt* to *model* and return the JSON response."""

    def health(self) -> bool:
        try:
            if hasattr(requests, "head"):
                r = requests.head(self.base_url, timeout=3)
                return getattr(r, "ok", False)
            # fallback for stubbed requests
            requests.post(self.base_url, timeout=3)
            return True
        except Exception:
            return False


class OllamaProvider(LLMProvider):
    """LLMProvider implementation for Ollama."""

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        super().__init__(base_url)

    def list_models(self) -> List[str]:
        url = f"{self.base_url}/api/tags"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return [m.get("name") for m in data.get("models", [])]

    def model_exists(self, name: str) -> bool:
        try:
            return name in self.list_models()
        except Exception:
            return False

    def send_prompt(self, prompt: str, model: str) -> dict:
        url = f"{self.base_url}/v1/chat/completions"
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        backoff = 1.0
        for _ in range(3):
            start = time.time()
            try:
                logger.info("sending prompt at %s", start)
                resp = requests.post(url, json=payload, timeout=10)
                resp.raise_for_status()
                logger.info("received response at %s", time.time())
                return resp.json()
            except requests.Timeout:
                logger.warning("timeout talking to Ollama, retrying")
                time.sleep(backoff)
                backoff *= 2
        raise RuntimeError("failed to communicate with Ollama")
