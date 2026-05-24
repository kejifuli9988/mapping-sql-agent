from __future__ import annotations

from typing import Any


class MappingImpactAnalyzer:
    """Summarize Mapping changes and the SQL areas they affect."""

    def analyze(self, historical: dict[str, Any], current: dict[str, Any]) -> list[str]:
        impacts: list[str] = []
        impacts.extend(self._table_impacts(historical, current))
        impacts.extend(self._source_impacts(historical, current))
        impacts.extend(self._join_impacts(historical, current))
        impacts.extend(self._filter_impacts(historical, current))
        impacts.extend(self._target_column_impacts(historical, current))

        if not impacts:
            impacts.append("未发现 Mapping 结构变化，SQL 只需关注生成器或规范配置差异。")

        return impacts

    def _table_impacts(self, historical: dict[str, Any], current: dict[str, Any]) -> list[str]:
        impacts: list[str] = []
        if historical.get("target_table") != current.get("target_table"):
            impacts.append(
                "目标表变更："
                f"{historical.get('target_table')} -> {current.get('target_table')}，"
                "SQL INSERT 目标表需同步调整。"
            )
        if historical.get("target_partition") != current.get("target_partition"):
            impacts.append(
                "分区规则变更："
                f"{historical.get('target_partition')} -> {current.get('target_partition')}，"
                "SQL PARTITION 写入规则需同步调整。"
            )
        return impacts

    def _source_impacts(self, historical: dict[str, Any], current: dict[str, Any]) -> list[str]:
        impacts: list[str] = []
        old_sources = self._by_key(historical.get("sources", []), "alias")
        new_sources = self._by_key(current.get("sources", []), "alias")

        for alias in sorted(new_sources.keys() - old_sources.keys()):
            source = new_sources[alias]
            impacts.append(
                f"新增来源表：{source['name']} AS {alias}，SQL WITH/FROM 或 JOIN 依赖需新增。"
            )
        for alias in sorted(old_sources.keys() - new_sources.keys()):
            source = old_sources[alias]
            impacts.append(
                f"删除来源表：{source['name']} AS {alias}，SQL 中相关字段、JOIN、过滤条件需移除。"
            )
        for alias in sorted(old_sources.keys() & new_sources.keys()):
            if old_sources[alias].get("name") != new_sources[alias].get("name"):
                impacts.append(
                    f"来源表替换：别名 {alias} 从 {old_sources[alias].get('name')} "
                    f"变为 {new_sources[alias].get('name')}，SQL 字段来源需复核。"
                )

        return impacts

    def _join_impacts(self, historical: dict[str, Any], current: dict[str, Any]) -> list[str]:
        impacts: list[str] = []
        old_joins = self._join_signatures(historical.get("joins", []))
        new_joins = self._join_signatures(current.get("joins", []))

        for item in sorted(new_joins - old_joins):
            impacts.append(f"新增 Join：{item}，SQL JOIN 关系需新增。")
        for item in sorted(old_joins - new_joins):
            impacts.append(f"删除 Join：{item}，SQL JOIN 关系及依赖字段需移除或改写。")

        return impacts

    def _filter_impacts(self, historical: dict[str, Any], current: dict[str, Any]) -> list[str]:
        impacts: list[str] = []
        old_filters = set(historical.get("filters", []))
        new_filters = set(current.get("filters", []))

        for item in sorted(new_filters - old_filters):
            impacts.append(f"新增过滤条件：{item}，SQL WHERE 条件需新增。")
        for item in sorted(old_filters - new_filters):
            impacts.append(f"删除过滤条件：{item}，SQL WHERE 条件需移除。")

        return impacts

    def _target_column_impacts(self, historical: dict[str, Any], current: dict[str, Any]) -> list[str]:
        impacts: list[str] = []
        old_columns = self._by_key(historical.get("target_columns", []), "name")
        new_columns = self._by_key(current.get("target_columns", []), "name")

        for name in sorted(new_columns.keys() - old_columns.keys()):
            expression = new_columns[name].get("expression", "")
            impacts.append(
                f"新增目标字段：{name} = {expression}，SQL SELECT"
                f"{' 和 GROUP BY' if not self._is_aggregate_expression(expression) else ''} 需同步新增。"
            )
        for name in sorted(old_columns.keys() - new_columns.keys()):
            impacts.append(f"删除目标字段：{name}，SQL SELECT 及下游依赖需移除。")
        for name in sorted(old_columns.keys() & new_columns.keys()):
            old_expression = old_columns[name].get("expression", "")
            new_expression = new_columns[name].get("expression", "")
            if old_expression != new_expression:
                impacts.append(
                    f"目标字段表达式变更：{name} 从 {old_expression} 变为 {new_expression}，"
                    "SQL SELECT 计算逻辑需同步调整。"
                )

        return impacts

    def _by_key(self, items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
        return {str(item[key]).lower(): item for item in items if key in item}

    def _join_signatures(self, joins: list[dict[str, Any]]) -> set[str]:
        signatures = set()
        for join in joins:
            join_type = str(join.get("type", "LEFT")).upper()
            right_alias = join.get("right_alias", "")
            condition = join.get("condition", "")
            signatures.add(f"{join_type} JOIN {right_alias} ON {condition}")
        return signatures

    def _is_aggregate_expression(self, expression: str) -> bool:
        normalized = expression.upper()
        aggregate_keywords = ("SUM(", "COUNT(", "MAX(", "MIN(", "AVG(")
        return any(keyword in normalized for keyword in aggregate_keywords)
