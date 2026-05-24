from __future__ import annotations

import csv
from dataclasses import dataclass
from io import BytesIO, StringIO
import json
from pathlib import PurePosixPath
import re
from typing import Any
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from .deepseek_client import DeepSeekClient
from .prompt_builder import PromptBuilder


NS_MAIN = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
NS_REL = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkg": "http://schemas.openxmlformats.org/package/2006/relationships",
}


@dataclass
class SchemaField:
    name: str
    type: str
    description: str


class SchemaInsightService:
    """Analyze schema inputs from DDL, JSON, CSV, or Excel."""

    def __init__(self) -> None:
        self.prompt_builder = PromptBuilder()

    def analyze_text(self, schema_text: str, input_format: str, ai_config: dict) -> dict[str, Any]:
        schema_text = schema_text.strip()
        if not schema_text:
            raise ValueError("表结构内容不能为空。")

        fallback = self._fallback_analysis(schema_text, input_format)
        if not ai_config.get("enabled"):
            fallback["fallback_used"] = False
            return fallback

        try:
            return self._analyze_with_ai(schema_text, input_format, ai_config, fallback)
        except Exception as exc:  # noqa: BLE001
            fallback["fallback_used"] = True
            fallback["fallback_reason"] = str(exc)
            return fallback

    def analyze_excel(self, content: bytes, ai_config: dict) -> dict[str, Any]:
        rows = self._extract_excel_rows(content)
        lines = []
        for row in rows:
            lines.append(" | ".join(row))
        schema_text = "\n".join(lines)
        return self.analyze_text(schema_text, "excel", ai_config)

    def _analyze_with_ai(
        self,
        schema_text: str,
        input_format: str,
        ai_config: dict,
        fallback: dict[str, Any],
    ) -> dict[str, Any]:
        client = DeepSeekClient(
            api_key=ai_config.get("api_key"),
            model=ai_config.get("model", "deepseek-v4-flash"),
            base_url=ai_config.get("base_url", "https://api.deepseek.com"),
        )
        messages = self.prompt_builder.build_schema_analysis_messages(schema_text, input_format)
        content = client.generate_text(messages)

        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("DeepSeek returned invalid JSON while analyzing schema.") from exc

        result = {
            "fields": self._normalize_fields(payload.get("fields", [])) or fallback["fields"],
            "table_purpose": str(payload.get("table_purpose", "")).strip() or fallback["table_purpose"],
            "key_fields": self._normalize_key_fields(payload.get("key_fields", {}), fallback["key_fields"]),
            "reuse_suggestions": self._normalize_list(payload.get("reuse_suggestions", [])) or fallback["reuse_suggestions"],
            "input_format": input_format,
        }
        result["fallback_used"] = False
        return result

    def _fallback_analysis(self, schema_text: str, input_format: str) -> dict[str, Any]:
        fields = self._extract_fields(schema_text, input_format)
        key_fields = self._infer_key_fields(fields)
        return {
            "fields": [field.__dict__ for field in fields],
            "table_purpose": self._infer_table_purpose(fields, schema_text),
            "key_fields": key_fields,
            "reuse_suggestions": self._infer_reuse_suggestions(key_fields),
            "input_format": input_format,
        }

    def _extract_fields(self, schema_text: str, input_format: str) -> list[SchemaField]:
        if input_format in {"ddl", "create_table", "sql"}:
            fields = self._extract_fields_from_ddl(schema_text)
            if fields:
                return fields
        if input_format == "json":
            fields = self._extract_fields_from_json(schema_text)
            if fields:
                return fields
        if input_format == "csv":
            fields = self._extract_fields_from_csv(schema_text)
            if fields:
                return fields
        return self._extract_fields_from_delimited_text(schema_text)

    def _extract_fields_from_ddl(self, schema_text: str) -> list[SchemaField]:
        match = re.search(r"\(([\s\S]+)\)", schema_text)
        body = match.group(1) if match else schema_text
        fields: list[SchemaField] = []
        for raw_line in self._split_ddl_columns(body):
            line = raw_line.strip().rstrip(",")
            if not line or line.upper().startswith(("PRIMARY KEY", "UNIQUE", "KEY", "INDEX", "PARTITIONED BY")):
                continue
            match = re.match(
                r"`?([A-Za-z_][A-Za-z0-9_]*)`?\s+([A-Za-z0-9_(),]+)(?:\s+COMMENT\s+'([^']*)')?",
                line,
                flags=re.IGNORECASE,
            )
            if match:
                fields.append(
                    SchemaField(
                        name=match.group(1),
                        type=match.group(2),
                        description=(match.group(3) or "").strip(),
                    )
                )
        return fields

    def _split_ddl_columns(self, body: str) -> list[str]:
        items: list[str] = []
        current: list[str] = []
        depth = 0
        in_quote = False

        for char in body:
            if char == "'" and (not current or current[-1] != "\\"):
                in_quote = not in_quote
            if not in_quote:
                if char == "(":
                    depth += 1
                elif char == ")" and depth > 0:
                    depth -= 1
                elif char == "," and depth == 0:
                    item = "".join(current).strip()
                    if item:
                        items.append(item)
                    current = []
                    continue
            current.append(char)

        tail = "".join(current).strip()
        if tail:
            items.append(tail)
        return items

    def _extract_fields_from_json(self, schema_text: str) -> list[SchemaField]:
        payload = json.loads(schema_text)
        if isinstance(payload, dict) and isinstance(payload.get("fields"), list):
            return [
                SchemaField(
                    name=str(item.get("name", "")),
                    type=str(item.get("type", "")),
                    description=str(item.get("description", "")),
                )
                for item in payload["fields"]
                if item.get("name")
            ]
        if isinstance(payload, list) and payload:
            first = payload[0]
            if isinstance(first, dict):
                return [SchemaField(name=str(key), type="string", description="") for key in first.keys()]
        if isinstance(payload, dict):
            return [SchemaField(name=str(key), type="string", description="") for key in payload.keys()]
        return []

    def _extract_fields_from_csv(self, schema_text: str) -> list[SchemaField]:
        rows = list(csv.reader(StringIO(schema_text)))
        if not rows:
            return []
        header = [item.strip().lower() for item in rows[0]]
        if {"字段名", "name"} & set(header):
            return self._extract_fields_from_delimited_text(schema_text)
        return [SchemaField(name=str(item).strip(), type="string", description="") for item in rows[0] if str(item).strip()]

    def _extract_fields_from_delimited_text(self, schema_text: str) -> list[SchemaField]:
        fields: list[SchemaField] = []
        for raw_line in schema_text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            parts = [part.strip() for part in re.split(r"[|,\t]", line)]
            if len(parts) >= 2 and self._looks_like_field_name(parts[0]):
                name = parts[0]
                field_type = parts[1]
                description = parts[2] if len(parts) >= 3 else ""
                if name.lower() not in {"字段名", "name"}:
                    fields.append(SchemaField(name=name, type=field_type, description=description))
        return fields

    def _extract_excel_rows(self, content: bytes) -> list[list[str]]:
        with ZipFile(BytesIO(content)) as zf:
            shared_strings = self._load_shared_strings(zf)
            workbook_xml = ET.fromstring(zf.read("xl/workbook.xml"))
            rels_xml = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
            relationship_targets: dict[str, str] = {}
            for rel in rels_xml.findall("pkg:Relationship", NS_REL):
                relationship_targets[rel.attrib["Id"]] = rel.attrib["Target"]

            first_sheet = workbook_xml.find("main:sheets/main:sheet", NS_MAIN)
            if first_sheet is None:
                return []
            rel_id = first_sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
            target = relationship_targets.get(rel_id, "")
            sheet_path = str(PurePosixPath("xl") / PurePosixPath(target))
            return self._read_sheet_rows(zf.read(sheet_path), shared_strings)

    def _load_shared_strings(self, zf: ZipFile) -> list[str]:
        if "xl/sharedStrings.xml" not in zf.namelist():
            return []
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
        values: list[str] = []
        for item in root.findall("main:si", NS_MAIN):
            parts = [node.text or "" for node in item.findall(".//main:t", NS_MAIN)]
            values.append("".join(parts))
        return values

    def _read_sheet_rows(self, xml_bytes: bytes, shared_strings: list[str]) -> list[list[str]]:
        root = ET.fromstring(xml_bytes)
        rows: list[list[str]] = []
        for row in root.findall("main:sheetData/main:row", NS_MAIN):
            current: list[str] = []
            for cell in row.findall("main:c", NS_MAIN):
                current.append(self._cell_value(cell, shared_strings))
            if any(item.strip() for item in current):
                rows.append(current)
        return rows

    def _cell_value(self, cell: ET.Element, shared_strings: list[str]) -> str:
        cell_type = cell.attrib.get("t")
        value_node = cell.find("main:v", NS_MAIN)
        inline_text = cell.find("main:is/main:t", NS_MAIN)
        if cell_type == "inlineStr" and inline_text is not None:
            return inline_text.text or ""
        if value_node is None:
            return ""
        if cell_type == "s":
            index = int(value_node.text or "0")
            return shared_strings[index] if 0 <= index < len(shared_strings) else ""
        return value_node.text or ""

    def _normalize_fields(self, value: Any) -> list[dict[str, str]]:
        if not isinstance(value, list):
            return []
        rows: list[dict[str, str]] = []
        for item in value:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", "")).strip()
            if not name:
                continue
            rows.append(
                {
                    "name": name,
                    "type": str(item.get("type", "")).strip() or "string",
                    "description": str(item.get("description", "")).strip(),
                }
            )
        return rows

    def _normalize_key_fields(self, value: Any, fallback: dict[str, list[str]]) -> dict[str, list[str]]:
        if not isinstance(value, dict):
            return fallback
        normalized: dict[str, list[str]] = {}
        for key in fallback.keys():
            normalized[key] = self._normalize_list(value.get(key, [])) or fallback[key]
        return normalized

    def _normalize_list(self, value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return []

    def _infer_table_purpose(self, fields: list[SchemaField], schema_text: str) -> str:
        lowered = schema_text.lower()
        if "dim_" in lowered or any(field.name.endswith("_name") for field in fields):
            return "维表，主要用于补充维度属性和描述字段。"
        if "dws_" in lowered or any("sum" in field.name.lower() or "cnt" in field.name.lower() for field in fields):
            return "汇总表，主要用于沉淀聚合统计结果和经营指标。"
        if "dwd_" in lowered or "ods_" in lowered:
            return "明细或事实表，主要用于承接原子交易或行为数据。"
        return "中间或通用分析表，建议结合业务链路进一步确认。"

    def _infer_key_fields(self, fields: list[SchemaField]) -> dict[str, list[str]]:
        names = [field.name for field in fields]
        return {
            "primary_candidates": [name for name in names if self._matches_any(name, ("id", "code", "no"))][:5],
            "join_keys": [name for name in names if self._matches_any(name, ("id", "code", "key"))][:8],
            "time_fields": [name for name in names if self._matches_any(name, ("dt", "date", "time", "month", "day"))][:8],
            "partition_fields": [name for name in names if self._matches_any(name, ("dt", "month", "partition"))][:5],
            "metric_fields": [name for name in names if self._matches_any(name, ("amt", "cnt", "num", "rate", "balance"))][:8],
            "dimension_fields": [name for name in names if self._matches_any(name, ("name", "type", "level", "category", "region", "city"))][:8],
        }

    def _infer_reuse_suggestions(self, key_fields: dict[str, list[str]]) -> list[str]:
        suggestions: list[str] = []
        if key_fields["time_fields"]:
            suggestions.append("该表适合做同比、环比、趋势分析等时间序列场景。")
        if key_fields["dimension_fields"] and key_fields["metric_fields"]:
            suggestions.append("该表适合做多维聚合统计与经营分析看板。")
        if key_fields["join_keys"]:
            suggestions.append("该表可作为事实表与维表 Join 的关键输入，适合复用到指标宽表构建。")
        if not suggestions:
            suggestions.append("建议优先梳理主键候选和时间字段，再判断适合的复用分析场景。")
        return suggestions

    def _matches_any(self, value: str, keywords: tuple[str, ...]) -> bool:
        lowered = value.lower()
        return any(keyword in lowered for keyword in keywords)

    def _looks_like_field_name(self, value: str) -> bool:
        return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", value))
