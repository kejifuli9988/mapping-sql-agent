from __future__ import annotations

import json
from pathlib import Path


class DeepSeekConfigService:
    """Load DeepSeek runtime configuration from local JSON."""

    DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "deepseek_config.json"

    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH

    def load_runtime_config(self) -> dict:
        payload = self._read_config()
        return {
            "api_key": str(payload.get("api_key", "")).strip(),
            "model": str(payload.get("model", "deepseek-v4-flash")).strip() or "deepseek-v4-flash",
            "base_url": str(payload.get("base_url", "https://api.deepseek.com")).strip() or "https://api.deepseek.com",
        }

    def get_public_status(self) -> dict:
        runtime = self.load_runtime_config()
        configured = bool(runtime["api_key"])
        return {
            "configured": configured,
            "model": runtime["model"],
            "base_url": runtime["base_url"],
            "source": str(self.config_path),
            "message": (
                f"已从本地 JSON 加载 DeepSeek 配置，当前模型为 {runtime['model']}。"
                if configured
                else f"本地 JSON 已接入，但 {self.config_path.name} 中尚未配置 API Key。"
            ),
        }

    def _read_config(self) -> dict:
        if not self.config_path.exists():
            return {}
        try:
            payload = json.loads(self.config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"DeepSeek 本地配置文件解析失败：{exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError("DeepSeek 本地配置文件必须是 JSON 对象。")
        return payload
