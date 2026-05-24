from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class BusinessMemoryService:
    """Load reusable business memories and skill definitions for SQL prompting."""

    DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "business_memory.json"

    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.payload = self._load_config()

    def list_skills(self) -> list[dict[str, Any]]:
        return list(self.payload.get("skills", []))

    def get_skill(self, skill_id: str) -> dict[str, Any] | None:
        for item in self.list_skills():
            if item.get("id") == skill_id:
                return item
        return None

    def build_prompt_context(self, skill_id: str = "", include_memory: bool = True) -> dict[str, Any]:
        selected_skill = self.get_skill(skill_id) if skill_id else None
        memory_items = self.payload.get("memory_items", []) if include_memory else []
        return {
            "selected_skill": selected_skill,
            "memory_items": memory_items,
        }

    def recommend_skills_from_schema(self, schema_analysis: dict[str, Any]) -> list[dict[str, Any]]:
        suggestions = " ".join(schema_analysis.get("reuse_suggestions", []))
        key_fields = schema_analysis.get("key_fields", {})
        field_names = " ".join(
            item.get("name", "")
            for item in schema_analysis.get("fields", [])
            if isinstance(item, dict)
        ).lower()

        matched_ids: list[str] = []
        if "同比" in suggestions:
            matched_ids.append("yoy_summary")
        if "环比" in suggestions or "趋势" in suggestions:
            matched_ids.append("mom_summary")
        if "分层" in suggestions or "segment" in field_names or "user_id" in field_names:
            matched_ids.append("user_segmentation")
        if "product" in field_names or "产品" in field_names or "多维聚合" in suggestions:
            matched_ids.append("product_aggregation")
        if key_fields.get("metric_fields"):
            matched_ids.append("kpi_metrics")

        result: list[dict[str, Any]] = []
        for skill_id in matched_ids:
            skill = self.get_skill(skill_id)
            if skill and skill not in result:
                result.append(skill)
        return result

    def _load_config(self) -> dict[str, Any]:
        with self.config_path.open(encoding="utf-8") as file:
            return json.load(file)
