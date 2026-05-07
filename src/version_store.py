from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import difflib
import json
from pathlib import Path
from typing import Any


@dataclass
class VersionRecord:
    version_no: int
    task_name: str
    target_table: str
    created_at: str
    mode: str
    mapping: dict[str, Any]
    sql: str
    style_issues: list[str]
    summary: str
    user_requirement: str


class VersionStore:
    """Persist generated mapping/sql versions and provide compare helpers."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        mapping: dict[str, Any],
        sql: str,
        mode: str,
        style_issues: list[str],
        summary: str,
        user_requirement: str = "",
    ) -> dict[str, Any]:
        task_name = self._sanitize_name(mapping["task_name"])
        task_dir = self.base_dir / task_name
        task_dir.mkdir(parents=True, exist_ok=True)

        next_version = self._next_version(task_dir)
        record = VersionRecord(
            version_no=next_version,
            task_name=mapping["task_name"],
            target_table=mapping["target_table"],
            created_at=datetime.now().isoformat(timespec="seconds"),
            mode=mode,
            mapping=mapping,
            sql=sql,
            style_issues=style_issues,
            summary=summary,
            user_requirement=user_requirement,
        )

        file_path = task_dir / f"v{next_version:04d}.json"
        file_path.write_text(
            json.dumps(record.__dict__, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return self._to_payload(record)

    def list_tasks(self) -> list[dict[str, Any]]:
        tasks: list[dict[str, Any]] = []
        for task_dir in sorted(self.base_dir.iterdir() if self.base_dir.exists() else [], key=lambda p: p.name):
            if not task_dir.is_dir():
                continue
            records = self._load_task_records(task_dir.name)
            if not records:
                continue
            latest = records[-1]
            tasks.append(
                {
                    "task_name": latest["task_name"],
                    "target_table": latest["target_table"],
                    "version_count": len(records),
                    "latest_version_no": latest["version_no"],
                    "latest_created_at": latest["created_at"],
                }
            )
        return tasks

    def list_versions(self, task_name: str) -> list[dict[str, Any]]:
        records = self._load_task_records(task_name)
        return [self._summary_payload(item) for item in records]

    def get_version(self, task_name: str, version_no: int) -> dict[str, Any]:
        record = self._load_version(task_name, version_no)
        return dict(record)

    def compare_versions(
        self,
        task_name: str,
        left_version_no: int,
        right_version_no: int,
    ) -> dict[str, Any]:
        left = self._load_version(task_name, left_version_no)
        right = self._load_version(task_name, right_version_no)

        return {
            "task_name": left["task_name"],
            "left": self._summary_payload(left),
            "right": self._summary_payload(right),
            "left_sql": left["sql"],
            "right_sql": right["sql"],
            "left_mapping": left["mapping"],
            "right_mapping": right["mapping"],
            "sql_diff": self._line_diff(left["sql"], right["sql"]),
            "mapping_diff": self._line_diff(
                json.dumps(left["mapping"], ensure_ascii=False, indent=2),
                json.dumps(right["mapping"], ensure_ascii=False, indent=2),
            ),
        }

    def _load_task_records(self, task_name: str) -> list[dict[str, Any]]:
        task_dir = self.base_dir / self._sanitize_name(task_name)
        if not task_dir.exists():
            return []

        records = []
        for file_path in sorted(task_dir.glob("v*.json")):
            records.append(json.loads(file_path.read_text(encoding="utf-8")))
        return records

    def _load_version(self, task_name: str, version_no: int) -> dict[str, Any]:
        file_path = self.base_dir / self._sanitize_name(task_name) / f"v{version_no:04d}.json"
        if not file_path.exists():
            raise ValueError(f"Version v{version_no:04d} for task '{task_name}' was not found.")
        return json.loads(file_path.read_text(encoding="utf-8"))

    def _next_version(self, task_dir: Path) -> int:
        files = sorted(task_dir.glob("v*.json"))
        if not files:
            return 1
        latest = files[-1].stem.replace("v", "")
        return int(latest) + 1

    def _sanitize_name(self, name: str) -> str:
        return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in name)

    def _to_payload(self, record: VersionRecord) -> dict[str, Any]:
        return {
            "version_no": record.version_no,
            "task_name": record.task_name,
            "target_table": record.target_table,
            "created_at": record.created_at,
            "mode": record.mode,
            "mapping": record.mapping,
            "sql": record.sql,
            "style_issues": record.style_issues,
            "summary": record.summary,
            "user_requirement": record.user_requirement,
        }

    def _summary_payload(self, record: dict[str, Any]) -> dict[str, Any]:
        return {
            "version_no": record["version_no"],
            "task_name": record["task_name"],
            "target_table": record["target_table"],
            "created_at": record["created_at"],
            "mode": record["mode"],
            "summary": record["summary"],
            "user_requirement": record.get("user_requirement", ""),
        }

    def _line_diff(self, left: str, right: str) -> list[dict[str, str]]:
        diff_lines = difflib.ndiff(left.splitlines(), right.splitlines())
        payload: list[dict[str, str]] = []
        for line in diff_lines:
            code = line[:2]
            text = line[2:]
            if code == "  ":
                payload.append({"type": "same", "text": text})
            elif code == "- ":
                payload.append({"type": "removed", "text": text})
            elif code == "+ ":
                payload.append({"type": "added", "text": text})
        return payload
