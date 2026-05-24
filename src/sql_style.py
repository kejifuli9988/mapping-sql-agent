from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


class SQLStyleChecker:
    """Check whether generated SQL follows configurable platform conventions."""

    DEFAULT_RULES_PATH = Path(__file__).resolve().parents[1] / "config" / "sql_rules.json"
    FIELD_REF_PATTERN = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)\b")

    def __init__(self, rules_path: Path | None = None) -> None:
        self.rules_path = rules_path or self.DEFAULT_RULES_PATH
        self.rules = self._load_rules()

    def check(self, sql: str, mapping: dict) -> list[str]:
        issues: list[str] = []
        lowered_sql = sql.lower()

        for keyword in self.rules["required_keyword_blocks"]:
            if keyword not in sql:
                issues.append(f"Missing required keyword block: {keyword}")

        if self.rules["naming"]["target_table_lowercase"] and mapping["target_table"].lower() not in sql:
            issues.append("Target table name is not rendered in lowercase.")

        if self.rules["structure"]["forbid_main_select_star"] and re.search(
            r"INSERT\s+OVERWRITE\s+TABLE[\s\S]*?\nSELECT\s+\*\s+\nFROM",
            sql,
            flags=re.IGNORECASE,
        ):
            issues.append("Main query must not use SELECT *.")

        if self.rules["structure"]["require_semicolon"] and not sql.strip().endswith(";"):
            issues.append("SQL must end with a semicolon.")

        alias_pattern = re.compile(r"\bAS\s+[A-Z]")
        if self.rules["naming"]["target_field_alias_lowercase"] and alias_pattern.search(sql):
            issues.append("Target column aliases should stay lowercase.")

        if self.rules["structure"]["require_group_by_for_aggregate"] and "group by" not in lowered_sql and any(
            self._is_aggregate_expression(item["expression"])
            for item in mapping["target_columns"]
        ):
            issues.append("Aggregate expressions exist but GROUP BY is missing.")

        if not issues:
            issues.append("PASS - no blocking style issues detected.")

        return issues

    def check_fields(self, sql: str, mapping: dict) -> list[str]:
        """Validate field coverage and source alias references."""
        issues: list[str] = []
        target_columns = mapping["target_columns"]
        target_names = [item["name"].lower() for item in target_columns]
        source_aliases = {item["alias"].lower() for item in mapping["sources"]}

        if self.rules["field_validation"]["forbid_duplicate_target_columns"]:
            duplicates = sorted({name for name in target_names if target_names.count(name) > 1})
            for name in duplicates:
                issues.append(f"Duplicate target column in Mapping: {name}")

        if self.rules["field_validation"]["require_non_empty_expressions"]:
            for item in target_columns:
                if not str(item.get("expression", "")).strip():
                    issues.append(f"Target column has empty expression: {item.get('name', '<unknown>')}")

        if self.rules["naming"]["target_field_alias_lowercase"]:
            for item in target_columns:
                name = str(item["name"])
                if name != name.lower():
                    issues.append(f"Target column alias should be lowercase: {name}")

        if self.rules["naming"]["source_alias_lowercase"]:
            for item in mapping["sources"]:
                alias = str(item["alias"])
                if alias != alias.lower():
                    issues.append(f"Source alias should be lowercase: {alias}")

        if self.rules["field_validation"]["require_all_target_columns_in_sql"]:
            sql_aliases = self._extract_sql_aliases(sql)
            missing = [name for name in target_names if name not in sql_aliases]
            if missing:
                issues.append(f"SQL does not cover Mapping target columns: {', '.join(missing)}")
            else:
                issues.append(f"PASS - SQL covers all {len(target_names)} Mapping target columns.")

        if self.rules["field_validation"]["validate_referenced_source_aliases"]:
            unknown_aliases = self._find_unknown_aliases(mapping, source_aliases)
            if unknown_aliases:
                for alias, location in unknown_aliases:
                    issues.append(f"Unknown source alias '{alias}' referenced in {location}.")
            else:
                issues.append("PASS - all referenced source aliases are defined in Mapping sources.")

        if not issues:
            issues.append("PASS - field coverage and alias legality checks passed.")

        return issues

    def describe_rules(self) -> list[str]:
        rules = self.rules
        descriptions = [
            f"规则配置：{rules['profile_name']}",
            "必需结构块：" + " / ".join(rules["required_keyword_blocks"]),
        ]
        if rules["structure"]["forbid_main_select_star"]:
            descriptions.append("主查询禁止 SELECT *。")
        if rules["structure"]["require_group_by_for_aggregate"]:
            descriptions.append("存在聚合表达式时必须包含 GROUP BY。")
        if rules["field_validation"]["require_all_target_columns_in_sql"]:
            descriptions.append("生成 SQL 必须覆盖 Mapping 中全部 target_columns。")
        if rules["field_validation"]["validate_referenced_source_aliases"]:
            descriptions.append("表达式、Join、过滤条件中的来源别名必须在 sources 中定义。")
        return descriptions

    def _is_aggregate_expression(self, expression: str) -> bool:
        normalized = expression.upper()
        aggregate_keywords = ("SUM(", "COUNT(", "MAX(", "MIN(", "AVG(")
        return any(keyword in normalized for keyword in aggregate_keywords)

    def _load_rules(self) -> dict[str, Any]:
        with self.rules_path.open(encoding="utf-8") as file:
            return json.load(file)

    def _extract_sql_aliases(self, sql: str) -> set[str]:
        aliases = re.findall(r"\bAS\s+([A-Za-z_][A-Za-z0-9_]*)\b", sql, flags=re.IGNORECASE)
        return {alias.lower() for alias in aliases}

    def _find_unknown_aliases(
        self,
        mapping: dict,
        source_aliases: set[str],
    ) -> list[tuple[str, str]]:
        unknown: list[tuple[str, str]] = []

        for column in mapping["target_columns"]:
            self._collect_unknown_aliases(
                column["expression"],
                source_aliases,
                f"target column '{column['name']}'",
                unknown,
            )

        for index, join in enumerate(mapping.get("joins", []), start=1):
            right_alias = str(join.get("right_alias", "")).lower()
            if right_alias and right_alias not in source_aliases:
                unknown.append((right_alias, f"join #{index} right_alias"))
            self._collect_unknown_aliases(
                join.get("condition", ""),
                source_aliases,
                f"join #{index} condition",
                unknown,
            )

        for index, item in enumerate(mapping.get("filters", []), start=1):
            self._collect_unknown_aliases(item, source_aliases, f"filter #{index}", unknown)

        return unknown

    def _collect_unknown_aliases(
        self,
        expression: str,
        source_aliases: set[str],
        location: str,
        unknown: list[tuple[str, str]],
    ) -> None:
        for alias, _field in self.FIELD_REF_PATTERN.findall(str(expression)):
            normalized = alias.lower()
            if normalized not in source_aliases:
                unknown.append((alias, location))
