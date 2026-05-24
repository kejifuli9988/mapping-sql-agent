from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from .mapping_loader import MappingLoader


NS_MAIN = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
NS_REL = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkg": "http://schemas.openxmlformats.org/package/2006/relationships",
}


@dataclass
class ExcelSheet:
    name: str
    rows: list[list[str]]


class ExcelMappingParser:
    """Parse a template-style Excel mapping workbook into normalized mapping JSON."""

    SHEET_ALIASES = {
        "overview": {"overview", "config", "meta", "basic", "基础信息", "配置", "概览"},
        "sources": {"sources", "source", "来源表", "源表"},
        "joins": {"joins", "join", "关联", "关联关系"},
        "filters": {"filters", "filter", "过滤", "过滤条件"},
        "target_columns": {
            "target_columns",
            "targetcolumn",
            "columns",
            "mapping",
            "字段映射",
            "目标字段",
        },
    }

    HEADER_ALIASES = {
        "task_name": {"taskname", "task_name", "任务名", "任务名称"},
        "target_table": {"targettable", "target_table", "目标表", "目标表名"},
        "target_partition": {"targetpartition", "target_partition", "目标分区", "分区"},
        "name": {"name", "字段名", "表名", "名称"},
        "alias": {"alias", "别名"},
        "type": {"type", "jointype", "关联类型"},
        "right_alias": {"rightalias", "right_alias", "右表别名", "关联表别名"},
        "condition": {"condition", "joincondition", "关联条件", "条件", "表达式"},
        "expression": {"expression", "expr", "映射表达式", "字段表达式"},
    }

    def __init__(self) -> None:
        self.loader = MappingLoader()

    def parse(self, content: bytes) -> dict:
        workbook = self._load_workbook(content)
        mapping = {
            **self._parse_overview(workbook),
            "sources": self._parse_table_sheet(workbook, "sources", ["name", "alias"]),
            "joins": self._parse_optional_joins(workbook),
            "filters": self._parse_optional_filters(workbook),
            "target_columns": self._parse_table_sheet(
                workbook,
                "target_columns",
                ["name", "expression"],
            ),
        }
        return self.loader.validate_mapping(mapping)

    def extract_text(self, content: bytes) -> str:
        workbook = self._load_workbook(content)
        sections: list[str] = []
        for sheet in workbook.values():
            sections.append(f"[sheet] {sheet.name}")
            for row in sheet.rows:
                sections.append(" | ".join((cell or "").strip() for cell in row))
            sections.append("")
        return "\n".join(sections).strip()

    def _load_workbook(self, content: bytes) -> dict[str, ExcelSheet]:
        with ZipFile(BytesIO(content)) as zf:
            shared_strings = self._load_shared_strings(zf)
            workbook_xml = ET.fromstring(zf.read("xl/workbook.xml"))
            rels_xml = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))

            relationship_targets: dict[str, str] = {}
            for rel in rels_xml.findall("pkg:Relationship", NS_REL):
                relationship_targets[rel.attrib["Id"]] = rel.attrib["Target"]

            sheets: dict[str, ExcelSheet] = {}
            for sheet in workbook_xml.findall("main:sheets/main:sheet", NS_MAIN):
                sheet_name = sheet.attrib["name"]
                rel_id = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
                target = relationship_targets.get(rel_id)
                if not target:
                    continue

                sheet_path = str(PurePosixPath("xl") / PurePosixPath(target))
                rows = self._read_sheet_rows(zf.read(sheet_path), shared_strings)
                sheets[sheet_name] = ExcelSheet(name=sheet_name, rows=rows)

        return sheets

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
            expected_index = 0
            for cell in row.findall("main:c", NS_MAIN):
                cell_ref = cell.attrib.get("r", "")
                column_index = self._column_index_from_ref(cell_ref)
                while expected_index < column_index:
                    current.append("")
                    expected_index += 1

                current.append(self._cell_value(cell, shared_strings))
                expected_index += 1

            while current and current[-1] == "":
                current.pop()

            if any(value != "" for value in current):
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

    def _column_index_from_ref(self, cell_ref: str) -> int:
        letters = "".join(ch for ch in cell_ref if ch.isalpha())
        index = 0
        for char in letters:
            index = index * 26 + (ord(char.upper()) - ord("A") + 1)
        return max(index - 1, 0)

    def _find_sheet(self, workbook: dict[str, ExcelSheet], sheet_type: str) -> ExcelSheet | None:
        aliases = self.SHEET_ALIASES[sheet_type]
        for name, sheet in workbook.items():
            if self._normalize_key(name) in {self._normalize_key(alias) for alias in aliases}:
                return sheet
        return None

    def _parse_overview(self, workbook: dict[str, ExcelSheet]) -> dict:
        sheet = self._find_sheet(workbook, "overview")
        if sheet is None:
            raise ValueError(
                "Excel Mapping 缺少 overview/config/基础信息 工作表，无法读取任务名和目标表信息。"
            )

        values: dict[str, str] = {}
        for row in sheet.rows:
            if len(row) < 2:
                continue
            key = self._map_header(row[0])
            if key in {"task_name", "target_table", "target_partition"}:
                values[key] = row[1].strip()

        missing = [key for key in ["task_name", "target_table", "target_partition"] if key not in values]
        if missing:
            raise ValueError(f"Excel Mapping 概览页缺少关键字段：{', '.join(missing)}。")
        return values

    def _parse_table_sheet(
        self,
        workbook: dict[str, ExcelSheet],
        sheet_type: str,
        required_headers: list[str],
    ) -> list[dict]:
        sheet = self._find_sheet(workbook, sheet_type)
        if sheet is None:
            aliases = "/".join(sorted(self.SHEET_ALIASES[sheet_type]))
            raise ValueError(f"Excel Mapping 缺少 {aliases} 工作表。")

        if not sheet.rows:
            raise ValueError(f"Excel Mapping 工作表 {sheet.name} 为空。")

        header_map = self._build_header_map(sheet.rows[0])
        missing = [header for header in required_headers if header not in header_map]
        if missing:
            raise ValueError(
                f"Excel Mapping 工作表 {sheet.name} 缺少列：{', '.join(missing)}。"
            )

        records: list[dict] = []
        for row in sheet.rows[1:]:
            if not any(cell.strip() for cell in row):
                continue

            record = {}
            for canonical, index in header_map.items():
                record[canonical] = row[index].strip() if index < len(row) else ""

            if any(record.get(header, "") for header in required_headers):
                records.append({header: record.get(header, "") for header in header_map})

        if not records:
            raise ValueError(f"Excel Mapping 工作表 {sheet.name} 没有有效数据行。")
        return records

    def _parse_optional_joins(self, workbook: dict[str, ExcelSheet]) -> list[dict]:
        sheet = self._find_sheet(workbook, "joins")
        if sheet is None or not sheet.rows:
            return []

        header_map = self._build_header_map(sheet.rows[0])
        if "condition" not in header_map:
            return []

        records: list[dict] = []
        for row in sheet.rows[1:]:
            if not any(cell.strip() for cell in row):
                continue
            condition = row[header_map["condition"]].strip() if header_map["condition"] < len(row) else ""
            if not condition:
                continue
            record = {
                "type": self._safe_value(row, header_map.get("type"), default="left"),
                "right_alias": self._safe_value(row, header_map.get("right_alias")),
                "condition": condition,
            }
            if record["right_alias"]:
                records.append(record)
        return records

    def _parse_optional_filters(self, workbook: dict[str, ExcelSheet]) -> list[str]:
        sheet = self._find_sheet(workbook, "filters")
        if sheet is None or not sheet.rows:
            return []

        header_map = self._build_header_map(sheet.rows[0])
        candidate_index = header_map.get("condition")
        if candidate_index is None:
            candidate_index = 0

        values: list[str] = []
        for row in sheet.rows[1:]:
            if candidate_index < len(row):
                item = row[candidate_index].strip()
                if item:
                    values.append(item)
        return values

    def _build_header_map(self, header_row: list[str]) -> dict[str, int]:
        header_map: dict[str, int] = {}
        for index, raw_header in enumerate(header_row):
            canonical = self._map_header(raw_header)
            if canonical:
                header_map[canonical] = index
        return header_map

    def _map_header(self, raw_header: str) -> str | None:
        normalized = self._normalize_key(raw_header)
        for canonical, aliases in self.HEADER_ALIASES.items():
            if normalized in {self._normalize_key(alias) for alias in aliases}:
                return canonical
        return normalized or None

    def _normalize_key(self, value: str) -> str:
        return re.sub(r"[\s_\-:：]+", "", value.strip().lower())

    def _safe_value(self, row: list[str], index: int | None, default: str = "") -> str:
        if index is None or index >= len(row):
            return default
        return row[index].strip() or default
