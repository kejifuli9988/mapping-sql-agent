from __future__ import annotations

import json

from .deepseek_client import DeepSeekClient
from .mapping_loader import MappingLoader
from .prompt_builder import PromptBuilder


class MappingRepairService:
    """Repair malformed mapping input with AI assistance."""

    def __init__(self) -> None:
        self.loader = MappingLoader()
        self.prompt_builder = PromptBuilder()

    def repair(self, raw_mapping_text: str, ai_config: dict) -> dict:
        client = DeepSeekClient(
            api_key=ai_config.get("api_key"),
            model=ai_config.get("model", "deepseek-v4-flash"),
            base_url=ai_config.get("base_url", "https://api.deepseek.com"),
        )
        messages = self.prompt_builder.build_mapping_repair_messages(raw_mapping_text)
        content = client.generate_sql(messages)

        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "模型服务返回了无法解析的 Mapping 修复 JSON。"
            ) from exc

        if "normalized_mapping" not in payload:
            raise ValueError(
                "模型服务的 Mapping 修复结果缺少 normalized_mapping 字段。"
            )

        normalized_mapping = self.loader.validate_mapping(payload["normalized_mapping"])
        diagnosis = payload.get("diagnosis", [])
        if not isinstance(diagnosis, list):
            diagnosis = [str(diagnosis)]

        return {
            "mapping": normalized_mapping,
            "diagnosis": [str(item) for item in diagnosis],
        }
