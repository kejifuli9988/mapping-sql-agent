from __future__ import annotations


class SQLGenerator:
    """Generate SQL from mapping definitions."""

    def generate(self, mapping: dict) -> str:
        target_table = mapping["target_table"].lower()
        partition = mapping["target_partition"]

        with_section = self._build_with_section(mapping["sources"])
        select_section = self._build_select_section(mapping["target_columns"])
        from_section = self._build_from_section(mapping)
        where_section = self._build_where_section(mapping.get("filters", []))
        group_by_section = self._build_group_by_section(mapping["target_columns"])

        sql_parts = [
            f"-- task_name: {mapping['task_name']}",
            "WITH",
            with_section,
            f"INSERT OVERWRITE TABLE {target_table}",
            f"PARTITION ({partition})",
            "SELECT",
            select_section,
            from_section,
        ]

        if where_section:
            sql_parts.append(where_section)

        if group_by_section:
            sql_parts.append(group_by_section)

        return "\n".join(sql_parts) + ";"

    def _build_with_section(self, sources: list[dict]) -> str:
        ctes = []
        for source in sources:
            cte = (
                f"    {source['alias'].lower()} AS (\n"
                f"        SELECT\n"
                f"            *\n"
                f"        FROM {source['name'].lower()}\n"
                f"    )"
            )
            ctes.append(cte)
        return ",\n".join(ctes)

    def _build_select_section(self, target_columns: list[dict]) -> str:
        lines = []
        for index, column in enumerate(target_columns):
            suffix = "," if index < len(target_columns) - 1 else ""
            line = (
                f"    {column['expression']} AS {column['name'].lower()}"
                f"{suffix}"
            )
            lines.append(line)
        return "\n".join(lines)

    def _build_from_section(self, mapping: dict) -> str:
        sources = mapping["sources"]
        base = f"FROM {sources[0]['alias'].lower()}"
        joins = []

        for join in mapping.get("joins", []):
            joins.append(
                " ".join(
                    [
                        f"{join.get('type', 'LEFT').upper()} JOIN",
                        join["right_alias"].lower(),
                        "ON",
                        join["condition"],
                    ]
                )
            )

        if joins:
            return base + "\n" + "\n".join(joins)
        return base

    def _build_where_section(self, filters: list[str]) -> str:
        if not filters:
            return ""

        lines = ["WHERE"]
        for index, item in enumerate(filters):
            prefix = "    " if index == 0 else "    AND "
            lines.append(f"{prefix}{item}")
        return "\n".join(lines)

    def _build_group_by_section(self, target_columns: list[dict]) -> str:
        dimensions = [
            column["expression"]
            for column in target_columns
            if not self._is_aggregate_expression(column["expression"])
        ]

        if not dimensions:
            return ""

        lines = ["GROUP BY"]
        for index, expression in enumerate(dimensions):
            suffix = "," if index < len(dimensions) - 1 else ""
            lines.append(f"    {expression}{suffix}")
        return "\n".join(lines)

    def _is_aggregate_expression(self, expression: str) -> bool:
        normalized = expression.upper()
        aggregate_keywords = ("SUM(", "COUNT(", "MAX(", "MIN(", "AVG(")
        return any(keyword in normalized for keyword in aggregate_keywords)
