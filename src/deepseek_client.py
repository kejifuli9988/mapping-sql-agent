from __future__ import annotations

import json
import os
from urllib import error, request
from typing import Iterator


class DeepSeekClient:
    """Minimal DeepSeek API client based on the official chat completions API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "deepseek-v4-flash",
        base_url: str = "https://api.deepseek.com",
        timeout_seconds: int = 60,
    ) -> None:
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.model = model or "deepseek-v4-flash"
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def generate_sql(self, messages: list[dict]) -> str:
        return self.generate_text(messages)

    def generate_text(self, messages: list[dict]) -> str:
        if not self.api_key:
            raise ValueError("模型服务 API Key is required.")

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 4096,
            "stream": False,
        }

        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url=f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise ValueError(f"模型服务 API request failed: {detail}") from exc
        except error.URLError as exc:
            raise ValueError(f"模型服务 API connection failed: {exc.reason}") from exc

        try:
            content = response_payload["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("模型服务 API response is missing message content.") from exc

        return content.strip()

    def stream_text(self, messages: list[dict]) -> Iterator[str]:
        if not self.api_key:
            raise ValueError("模型服务 API Key is required.")

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 4096,
            "stream": True,
        }

        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url=f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                for raw_line in response:
                    line = raw_line.decode("utf-8", errors="ignore").strip()
                    if not line or not line.startswith("data: "):
                        continue
                    payload_text = line[6:]
                    if payload_text == "[DONE]":
                        break
                    try:
                        event = json.loads(payload_text)
                        delta = event["choices"][0]["delta"].get("content", "")
                    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
                        delta = ""
                    if delta:
                        yield delta
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise ValueError(f"模型服务 API request failed: {detail}") from exc
        except error.URLError as exc:
            raise ValueError(f"模型服务 API connection failed: {exc.reason}") from exc
