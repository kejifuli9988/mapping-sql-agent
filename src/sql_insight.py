from __future__ import annotations

import json
import re
from typing import Any

from .deepseek_client import DeepSeekClient
from .prompt_builder import PromptBuilder


class SQLInsightService:
    """Analyze SQL semantics and provide optimization suggestions."""

    SECTION_NAMES = ("SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY", "WINDOW")

    def __init__(self) -> None:
        self.prompt_builder = PromptBuilder()

    def analyze(self, sql_text: str, ai_config: dict) -> dict[str, Any]:
        sql_text = sql_text.strip()
        if not sql_text:
            raise ValueError("SQL 内容不能为空。")

        use_ai = bool(ai_config.get("enabled"))
        if use_ai:
            try:
                return self._analyze_with_ai(sql_text, ai_config)
            except Exception as exc:  # noqa: BLE001
                fallback = self._fallback_analysis(sql_text)
                fallback["fallback_used"] = True
                fallback["fallback_reason"] = str(exc)
                return fallback

        result = self._fallback_analysis(sql_text)
        result["fallback_used"] = False
        return result

    def _analyze_with_ai(self, sql_text: str, ai_config: dict) -> dict[str, Any]:
        client = DeepSeekClient(
            api_key=ai_config.get("api_key"),
            model=ai_config.get("model", "deepseek-v4-flash"),
            base_url=ai_config.get("base_url", "https://api.deepseek.com"),
        )
        messages = self.prompt_builder.build_sql_analysis_messages(
            sql_text,
            selected_skill=ai_config.get("selected_skill_detail"),
            memory_items=ai_config.get("memory_items", []),
            schema_context=ai_config.get("schema_analysis") if ai_config.get("use_schema_assist") else None,
        )
        content = client.generate_text(messages)

        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("模型服务返回了无法解析的 SQL 分析 JSON。") from exc

        result = {
            "purpose_analysis": self._normalize_list(payload.get("purpose_analysis", [])),
            "structure_breakdown": self._normalize_structure(payload.get("structure_breakdown", {}), sql_text),
            "optimization_suggestions": self._normalize_list(payload.get("optimization_suggestions", [])),
            "optimized_sql": str(payload.get("optimized_sql", "")).strip() or sql_text,
        }
        if result["optimized_sql"] == sql_text:
            result["optimized_sql"] = self._build_fallback_optimized_sql(sql_text)
        result["original_sql"] = sql_text
        return result

    def _fallback_analysis(self, sql_text: str) -> dict[str, Any]:
        structure = self._normalize_structure({}, sql_text)
        source_tables = self._extract_source_tables(sql_text)
        joins = self._extract_joins(sql_text)
        output_table = self._extract_output_table(sql_text)
        suggestions = self._build_fallback_suggestions(sql_text)
        optimized_sql = self._build_fallback_optimized_sql(sql_text)

        purpose = [
            f"该 SQL 主要处理 {len(source_tables) or 1} 个来源表的数据。",
            f"Join 关系数量约为 {len(joins)} 个，最终写入目标为 {output_table or '查询结果集'}。",
        ]
        if structure["group_by"]:
            purpose.append("SQL 包含聚合逻辑，主要用于汇总统计或指标计算。")
        if structure["where"]:
            purpose.append("SQL 包含过滤条件，用于约束分区或业务口径。")

        return {
            "purpose_analysis": purpose,
            "structure_breakdown": structure,
            "optimization_suggestions": suggestions,
            "optimized_sql": optimized_sql,
            "original_sql": sql_text,
        }

    def _normalize_list(self, value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return []

    def _normalize_structure(self, value: Any, sql_text: str) -> dict[str, str]:
        extracted = self._extract_sections(sql_text)
        if not isinstance(value, dict):
            return extracted

        normalized: dict[str, str] = {}
        key_map = {
            "select": "select",
            "from": "from",
            "join": "join",
            "where": "where",
            "group_by": "group_by",
            "order_by": "order_by",
            "window": "window",
        }
        for key, output_key in key_map.items():
            ai_value = str(value.get(key, "")).strip()
            normalized[output_key] = self._localize_structure_text(ai_value or extracted[output_key], output_key)
        return normalized

    def _extract_sections(self, sql_text: str) -> dict[str, str]:
        upper = sql_text.upper()
        sections: dict[str, str] = {}
        main_select = upper.rfind("SELECT")
        if main_select < 0:
            return {
                "select": "未识别到该结构。",
                "from": "未识别到该结构。",
                "join": "未识别到 JOIN 结构。",
                "where": "未识别到该结构。",
                "group_by": "未识别到该结构。",
                "order_by": "未识别到该结构。",
                "window": "未识别到该结构。",
            }

        from_pos = upper.find("FROM", main_select)
        where_pos = upper.find("WHERE", from_pos if from_pos >= 0 else main_select)
        group_pos = upper.find("GROUP BY", from_pos if from_pos >= 0 else main_select)
        order_pos = upper.find("ORDER BY", from_pos if from_pos >= 0 else main_select)
        window_pos = upper.find("WINDOW", from_pos if from_pos >= 0 else main_select)

        sections["select"] = self._slice_section(sql_text, main_select, [from_pos])
        sections["from"] = self._slice_section(sql_text, from_pos, [where_pos, group_pos, order_pos, window_pos])
        sections["where"] = self._slice_section(sql_text, where_pos, [group_pos, order_pos, window_pos])
        sections["group_by"] = self._slice_section(sql_text, group_pos, [order_pos, window_pos])
        sections["order_by"] = self._slice_section(sql_text, order_pos, [window_pos])
        sections["window"] = self._slice_section(sql_text, window_pos, [])
        sections["join"] = "\n".join(self._extract_joins(sql_text)) or "未识别到 JOIN 结构。"
        return sections

    def _slice_section(self, sql_text: str, start: int, candidates: list[int]) -> str:
        if start < 0:
            return "未识别到该结构。"
        valid_candidates = [item for item in candidates if item >= 0]
        end = min(valid_candidates) if valid_candidates else len(sql_text)
        return sql_text[start:end].strip()

    def _extract_source_tables(self, sql_text: str) -> list[str]:
        pattern = re.compile(r"\bFROM\s+([A-Za-z0-9_.$]+)|\bJOIN\s+([A-Za-z0-9_.$]+)", re.IGNORECASE)
        tables: list[str] = []
        for left, right in pattern.findall(sql_text):
            table_name = left or right
            if table_name and table_name not in tables:
                tables.append(table_name)
        return tables

    def _extract_joins(self, sql_text: str) -> list[str]:
        pattern = re.compile(r"(?:LEFT|RIGHT|INNER|FULL|CROSS)?\s*JOIN\s+[^\n]+", re.IGNORECASE)
        return [item.strip() for item in pattern.findall(sql_text)]

    def _extract_output_table(self, sql_text: str) -> str:
        match = re.search(r"INSERT\s+OVERWRITE\s+TABLE\s+([A-Za-z0-9_.$]+)", sql_text, flags=re.IGNORECASE)
        return match.group(1) if match else ""

    def _build_fallback_suggestions(self, sql_text: str) -> list[str]:
        suggestions: list[str] = []
        if re.search(r"SELECT\s+\*", sql_text, flags=re.IGNORECASE):
            suggestions.append("避免使用 SELECT *，改为显式列出所需字段。")
        if "WITH" not in sql_text.upper() and sql_text.count("SELECT") > 1:
            suggestions.append("存在子查询时可考虑改写为 WITH CTE，提升可读性。")
        if "GROUP BY" in sql_text.upper():
            suggestions.append("请复核 GROUP BY 字段是否仅保留必要维度，避免冗余分组。")
        if "WHERE" in sql_text.upper():
            suggestions.append("可检查过滤条件是否可以前置到更早层级，减少中间数据量。")
        if not suggestions:
            suggestions.append("SQL 结构较规整，建议重点复核字段选择、过滤条件和 Join 基数。")
        return suggestions

    def _localize_structure_text(self, text: str, section: str) -> str:
        cleaned = text.strip()
        if not cleaned:
            return "未识别到该结构。"

        replacements = {
            "None": "未识别到该结构。",
            "none": "未识别到该结构。",
            "No JOIN detected.": "未识别到 JOIN 结构。",
            "No join detected.": "未识别到 JOIN 结构。",
            "CTE ": "公共表达式 ",
            "from ": "来源 ",
        }
        for source, target in replacements.items():
            cleaned = cleaned.replace(source, target)

        if section == "join" and cleaned.lower() == "none":
            return "未识别到 JOIN 结构。"
        return cleaned

    def _build_fallback_optimized_sql(self, sql_text: str) -> str:
        optimized = sql_text
        optimized = self._replace_select_star_in_cte(optimized)
        return optimized

    def _replace_select_star_in_cte(self, sql_text: str) -> str:
        pattern = re.compile(
            r"WITH\s+([A-Za-z_][A-Za-z0-9_]*)\s+AS\s*\(\s*SELECT\s*\n\s*\*\s*\n(\s*FROM[\s\S]+?\))",
            flags=re.IGNORECASE,
        )
        match = pattern.search(sql_text)
        if not match:
            return sql_text

        cte_name = match.group(1)
        inferred_columns = self._infer_cte_columns(sql_text, cte_name)
        if not inferred_columns:
            return sql_text

        replacement = "WITH " + cte_name + " AS (\n    SELECT\n" + "".join(
            f"        {column}{',' if index < len(inferred_columns) - 1 else ''}\n"
            for index, column in enumerate(inferred_columns)
        ) + match.group(2)

        return pattern.sub(replacement, sql_text, count=1)

    def _infer_cte_columns(self, sql_text: str, cte_name: str) -> list[str]:
        upper = sql_text.upper()
        from_pos = upper.rfind(f"FROM {cte_name.upper()}")
        if from_pos < 0:
            return []

        select_pos = upper.rfind("SELECT", 0, from_pos)
        group_pos = upper.find("GROUP BY", from_pos)
        order_pos = upper.find("ORDER BY", from_pos)
        end_pos_candidates = [item for item in (group_pos, order_pos) if item >= 0]
        end_pos = min(end_pos_candidates) if end_pos_candidates else len(sql_text)
        outer_select = sql_text[select_pos:end_pos]

        columns: list[str] = []
        for raw_line in outer_select.splitlines():
            line = raw_line.strip().rstrip(",")
            if not line or line.upper() == "SELECT":
                continue
            expr = re.split(r"\s+AS\s+", line, flags=re.IGNORECASE)[0]
            expr = re.sub(r"\b(COUNT|SUM|AVG|MIN|MAX|DISTINCT|CASE|WHEN|THEN|ELSE|END|NULLIF)\b", " ", expr, flags=re.IGNORECASE)
            expr = expr.replace("(", " ").replace(")", " ")
            for token in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", expr):
                upper_token = token.upper()
                if upper_token in {"SELECT", "FROM", "WHERE", "GROUP", "BY", "ORDER"}:
                    continue
                if token.lower() == cte_name.lower():
                    continue
                if token not in columns:
                    columns.append(token)
        return columns
