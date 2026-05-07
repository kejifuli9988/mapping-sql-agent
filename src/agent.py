from __future__ import annotations

from pathlib import Path

from .deepseek_client import DeepSeekClient
from .mapping_loader import MappingLoader
from .mapping_repair import MappingRepairService
from .prompt_builder import PromptBuilder
from .sql_generator import SQLGenerator
from .sql_style import SQLStyleChecker


class MappingSQLAgent:
    """End-to-end agent that turns mapping documents into SQL."""

    def __init__(self) -> None:
        self.loader = MappingLoader()
        self.generator = SQLGenerator()
        self.style_checker = SQLStyleChecker()
        self.prompt_builder = PromptBuilder()
        self.mapping_repair = MappingRepairService()

    def run(self, mapping_path: Path) -> dict:
        mapping = self.loader.load(mapping_path)
        return self.run_mapping(mapping)

    def run_mapping(self, mapping: dict) -> dict:
        sql = self.generator.generate(mapping)
        return self._build_result(mapping, sql, mode="rule")

    def run_mapping_with_ai(self, mapping: dict, ai_config: dict) -> dict:
        draft_sql = self.generator.generate(mapping)
        messages = self.prompt_builder.build_sql_messages(mapping, draft_sql)
        client = DeepSeekClient(
            api_key=ai_config.get("api_key"),
            model=ai_config.get("model", "deepseek-v4-flash"),
        )

        sql = client.generate_sql(messages)
        if not sql:
            sql = draft_sql

        return self._build_result(mapping, sql, mode="deepseek", draft_sql=draft_sql)

    def _build_result(
        self,
        mapping: dict,
        sql: str,
        mode: str,
        draft_sql: str | None = None,
    ) -> dict:
        style_issues = self.style_checker.check(sql, mapping)

        summary = (
            f"task={mapping['task_name']}; "
            f"target={mapping['target_table']}; "
            f"sources={len(mapping['sources'])}; "
            f"columns={len(mapping['target_columns'])}; "
            f"mode={mode}"
        )

        result = {
            "summary": summary,
            "sql": sql,
            "style_issues": style_issues,
            "mode": mode,
        }
        if draft_sql is not None:
            result["draft_sql"] = draft_sql
        return result

    def repair_mapping_text(self, raw_mapping_text: str, ai_config: dict) -> dict:
        return self.mapping_repair.repair(raw_mapping_text, ai_config)
