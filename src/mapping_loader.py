from __future__ import annotations

import json
from pathlib import Path


class MappingLoader:
    """Load structured mapping documents."""

    REQUIRED_TOP_LEVEL_FIELDS = {
        "task_name",
        "target_table",
        "target_partition",
        "sources",
        "target_columns",
    }

    def load(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Mapping file not found: {path}")

        if path.suffix.lower() != ".json":
            raise ValueError("Current prototype supports JSON mapping files only.")

        data = json.loads(path.read_text(encoding="utf-8"))
        return self.validate_mapping(data)

    def validate_mapping(self, data: dict) -> dict:
        self._validate(data)
        return data

    def load_from_text(self, raw_text: str) -> dict:
        data = json.loads(raw_text)
        return self.validate_mapping(data)

    def _validate(self, data: dict) -> None:
        missing = sorted(self.REQUIRED_TOP_LEVEL_FIELDS - set(data))
        if missing:
            raise ValueError(f"Mapping is missing required fields: {', '.join(missing)}")

        if not data["sources"]:
            raise ValueError("Mapping must include at least one source table.")

        if not data["target_columns"]:
            raise ValueError("Mapping must include at least one target column.")

        for source in data["sources"]:
            if "name" not in source or "alias" not in source:
                raise ValueError("Each source must contain 'name' and 'alias'.")

        for column in data["target_columns"]:
            if "name" not in column or "expression" not in column:
                raise ValueError(
                    "Each target column must contain 'name' and 'expression'."
                )
