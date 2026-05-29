from __future__ import annotations

import json
import re
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

    def save_skill(self, skill: dict[str, Any]) -> dict[str, Any]:
        normalized = self._normalize_skill(skill)
        skills = self.list_skills()
        if normalized["id"] == "none":
            raise ValueError("系统默认 Skill 不允许覆盖。")

        updated = False
        for index, item in enumerate(skills):
            if item.get("id") == normalized["id"]:
                skills[index] = normalized
                updated = True
                break
        if not updated:
            skills.append(normalized)

        self.payload["skills"] = skills
        self._write_config()
        return normalized

    def delete_skill(self, skill_id: str) -> None:
        if not skill_id or skill_id == "none":
            raise ValueError("系统默认 Skill 不允许删除。")
        skills = [item for item in self.list_skills() if item.get("id") != skill_id]
        if len(skills) == len(self.list_skills()):
            raise ValueError("未找到要删除的 Skill。")
        self.payload["skills"] = skills
        self._write_config()

    def generate_skill_draft(
        self,
        scenario: str,
        schema_text: str = "",
        requirement: str = "",
    ) -> dict[str, Any]:
        source_text = " ".join([scenario, schema_text, requirement]).strip()
        if not source_text:
            raise ValueError("请先输入业务场景或表结构内容。")

        name = self._infer_skill_name(source_text)
        skill_id = self._build_skill_id(name, source_text)
        dimensions = self._infer_dimensions(source_text)
        metrics = self._infer_metrics(source_text)
        filters = self._infer_filters(source_text)

        description = (
            f"适用于{name}场景下的 SQL 生成、拆解和优化，强调业务口径、字段角色、分区过滤和结果可复核。"
        )
        if requirement.strip():
            description += f" 典型需求：{requirement.strip()}"

        sql_pattern_parts = []
        if dimensions:
            sql_pattern_parts.append(f"按{self._join_cn(dimensions)}分组")
        if metrics:
            sql_pattern_parts.append(f"输出{self._join_cn(metrics)}等指标")
        if filters:
            sql_pattern_parts.append(f"优先使用{self._join_cn(filters)}过滤")
        sql_pattern = "；".join(sql_pattern_parts) or "基于业务主键、日期分区和金额指标生成可审查 SQL"

        examples = self._build_examples(name, dimensions, metrics)
        business_rules = self._build_business_rules(source_text, filters)

        return {
            "id": skill_id,
            "name": name,
            "description": description,
            "sql_pattern": sql_pattern,
            "examples": examples,
            "business_rules": business_rules,
        }

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
        if "清算" in suggestions or "clear" in field_names or "settle" in field_names:
            matched_ids.append("custody_clearing_reconcile")
        if "失败" in suggestions or "fail" in field_names or "error" in field_names:
            matched_ids.append("clearing_failure_analysis")
        if "估值" in suggestions or "净值" in suggestions or "valuation" in field_names or "nav" in field_names:
            matched_ids.append("custody_valuation_accounting")
        if "划拨" in suggestions or "到账" in suggestions or "transfer" in field_names:
            matched_ids.append("fund_transfer_verify")
        if "余额" in suggestions or "balance" in field_names:
            matched_ids.append("custody_balance_check")
        if "份额" in suggestions or "share" in field_names:
            matched_ids.append("share_registration_confirm")
        if "product" in field_names or "产品" in field_names or "多维聚合" in suggestions:
            matched_ids.append("product_clearing_summary")
        if key_fields.get("metric_fields"):
            matched_ids.append("custody_kpi_metrics")

        result: list[dict[str, Any]] = []
        for skill_id in matched_ids:
            skill = self.get_skill(skill_id)
            if skill and skill not in result:
                result.append(skill)
        return result

    def _load_config(self) -> dict[str, Any]:
        with self.config_path.open(encoding="utf-8") as file:
            return json.load(file)

    def _write_config(self) -> None:
        self.config_path.write_text(
            json.dumps(self.payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _normalize_skill(self, skill: dict[str, Any]) -> dict[str, Any]:
        name = str(skill.get("name", "")).strip()
        if not name:
            raise ValueError("Skill 名称不能为空。")
        skill_id = str(skill.get("id", "")).strip() or self._build_skill_id(name, json.dumps(skill, ensure_ascii=False))
        skill_id = re.sub(r"[^a-zA-Z0-9_]+", "_", skill_id.lower()).strip("_")
        if not skill_id:
            raise ValueError("Skill ID 无法为空。")

        examples = skill.get("examples", [])
        if isinstance(examples, str):
            examples = [item.strip() for item in examples.splitlines() if item.strip()]
        business_rules = skill.get("business_rules", [])
        if isinstance(business_rules, str):
            business_rules = [item.strip() for item in business_rules.splitlines() if item.strip()]

        normalized = {
            "id": skill_id,
            "name": name,
            "description": str(skill.get("description", "")).strip(),
            "sql_pattern": str(skill.get("sql_pattern", "")).strip(),
            "examples": examples if isinstance(examples, list) else [],
        }
        if business_rules:
            normalized["business_rules"] = business_rules if isinstance(business_rules, list) else []
        return normalized

    def _infer_skill_name(self, text: str) -> str:
        rules = [
            ("估值", "托管估值核算"),
            ("净值", "净值核算"),
            ("清算", "托管清算对账"),
            ("对账", "托管清算对账"),
            ("资金", "资金划拨核验"),
            ("份额", "份额登记确认"),
            ("余额", "托管账户余额核对"),
        ]
        for keyword, name in rules:
            if keyword in text:
                return name
        return "托管清核算业务"

    def _build_skill_id(self, name: str, text: str) -> str:
        pinyin_like = {
            "托管估值核算": "custody_valuation_accounting",
            "净值核算": "nav_accounting",
            "托管清算对账": "custody_clearing_reconcile",
            "资金划拨核验": "fund_transfer_verify",
            "份额登记确认": "share_registration_confirm",
            "托管账户余额核对": "custody_balance_check",
            "产品清算汇总": "product_clearing_summary",
            "清算失败原因分析": "clearing_failure_analysis",
            "清算KPI统计": "custody_kpi_metrics",
            "托管清核算业务": "custody_clearing_accounting",
        }
        base = pinyin_like.get(name, "custom_skill")
        existing_ids = {item.get("id") for item in self.list_skills()}
        if base not in existing_ids:
            return base
        suffix = abs(hash(text)) % 10000
        return f"{base}_{suffix}"

    def _infer_dimensions(self, text: str) -> list[str]:
        candidates = [
            ("产品", "产品"),
            ("基金", "基金"),
            ("组合", "组合"),
            ("账户", "账户"),
            ("交易日期", "交易日期"),
            ("清算日期", "清算日期"),
            ("业务日期", "业务日期"),
            ("渠道", "渠道"),
            ("状态", "状态"),
        ]
        return [name for keyword, name in candidates if keyword in text][:5]

    def _infer_metrics(self, text: str) -> list[str]:
        candidates = [
            ("金额", "金额"),
            ("份额", "份额"),
            ("笔数", "笔数"),
            ("净值", "净值"),
            ("余额", "余额"),
            ("成功", "成功笔数"),
            ("失败", "失败笔数"),
            ("差异", "差异金额"),
        ]
        metrics = [name for keyword, name in candidates if keyword in text]
        return metrics[:6] or ["金额", "笔数"]

    def _infer_filters(self, text: str) -> list[str]:
        filters = []
        if "dt" in text.lower() or "分区" in text:
            filters.append("分区日期")
        if "清算日期" in text:
            filters.append("清算日期")
        if "交易日期" in text:
            filters.append("交易日期")
        if "状态" in text:
            filters.append("状态")
        return filters[:4]

    def _build_examples(self, name: str, dimensions: list[str], metrics: list[str]) -> list[str]:
        dim_text = self._join_cn(dimensions) if dimensions else "产品、日期"
        metric_text = self._join_cn(metrics) if metrics else "金额、笔数"
        return [
            f"按{dim_text}统计{metric_text}",
            f"对{name}结果进行字段覆盖、分区过滤和异常状态复核",
        ]

    def _build_business_rules(self, text: str, filters: list[str]) -> list[str]:
        rules = [
            "生成 SQL 时应优先保留业务日期或分区日期条件，避免全表扫描。",
            "金额、份额、净值等指标字段应明确聚合方式，并注意空值处理。",
            "输出字段应与 Mapping 目标字段保持一致，避免新增无来源字段。",
        ]
        if "清算" in text or "对账" in text:
            rules.append("清算对账类 SQL 应区分成功、失败、处理中等状态，并保留差异核验字段。")
        if "估值" in text or "净值" in text:
            rules.append("估值核算类 SQL 应明确估值日期、产品或组合维度，并保留净值或估值金额口径。")
        if filters:
            rules.append(f"过滤条件优先参考{self._join_cn(filters)}。")
        return rules

    def _join_cn(self, items: list[str]) -> str:
        return "、".join(dict.fromkeys(item for item in items if item))
