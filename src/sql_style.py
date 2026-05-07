from __future__ import annotations

import re


class SQLStyleChecker:
    """Check whether generated SQL follows baseline platform conventions."""

    REQUIRED_KEYWORDS = [
        "INSERT OVERWRITE TABLE",
        "PARTITION",
        "WITH",
        "SELECT",
        "FROM",
    ]

    def check(self, sql: str, mapping: dict) -> list[str]:
        issues: list[str] = []
        lowered_sql = sql.lower()

        for keyword in self.REQUIRED_KEYWORDS:
            if keyword not in sql:
                issues.append(f"Missing required keyword block: {keyword}")

        if mapping["target_table"].lower() not in sql:
            issues.append("Target table name is not rendered in lowercase.")

        if re.search(r"\nSELECT\s+\*\s+\nFROM", sql, flags=re.IGNORECASE):
            issues.append("Main query must not use SELECT *.")

        if not sql.strip().endswith(";"):
            issues.append("SQL must end with a semicolon.")

        alias_pattern = re.compile(r"\bAS\s+[A-Z]")
        if alias_pattern.search(sql):
            issues.append("Target column aliases should stay lowercase.")

        if "group by" not in lowered_sql and any(
            self._is_aggregate_expression(item["expression"])
            for item in mapping["target_columns"]
        ):
            issues.append("Aggregate expressions exist but GROUP BY is missing.")

        if not issues:
            issues.append("PASS - no blocking style issues detected.")

        return issues

    def _is_aggregate_expression(self, expression: str) -> bool:
        normalized = expression.upper()
        aggregate_keywords = ("SUM(", "COUNT(", "MAX(", "MIN(", "AVG(")
        return any(keyword in normalized for keyword in aggregate_keywords)
