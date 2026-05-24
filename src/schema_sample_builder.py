from __future__ import annotations

from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile


CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""

ROOT_RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

WORKBOOK_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="schema_fields" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
"""

WORKBOOK_RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>
"""

STYLES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>
  <fills count="1"><fill><patternFill patternType="none"/></fill></fills>
  <borders count="1"><border/></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>
"""

CORE_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Schema Sample Template</dc:title>
  <dc:creator>Codex</dc:creator>
</cp:coreProperties>
"""

APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>
"""


class SchemaSampleExcelBuilder:
    """Generate a simple xlsx schema sample without external dependencies."""

    def build(self) -> bytes:
        rows = [
            ["name", "type", "description"],
            ["trade_id", "string", "交易流水号"],
            ["user_id", "string", "客户号"],
            ["product_id", "string", "产品编号"],
            ["trade_dt", "string", "交易日期"],
            ["trade_amt", "decimal(18,2)", "交易金额"],
            ["channel_code", "string", "渠道编码"],
            ["dt", "string", "分区日期"],
        ]

        unique_strings: list[str] = []
        seen: dict[str, int] = {}
        for row in rows:
            for item in row:
                if item not in seen:
                    seen[item] = len(unique_strings)
                    unique_strings.append(item)

        buffer = BytesIO()
        with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
            zf.writestr("_rels/.rels", ROOT_RELS_XML)
            zf.writestr("xl/workbook.xml", WORKBOOK_XML)
            zf.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS_XML)
            zf.writestr("xl/styles.xml", STYLES_XML)
            zf.writestr("docProps/core.xml", CORE_XML)
            zf.writestr("docProps/app.xml", APP_XML)
            zf.writestr("xl/sharedStrings.xml", self._shared_strings_xml(unique_strings))
            zf.writestr("xl/worksheets/sheet1.xml", self._sheet_xml(rows, seen))
        return buffer.getvalue()

    def _shared_strings_xml(self, values: list[str]) -> str:
        body = "".join(f"<si><t>{self._escape(value)}</t></si>" for value in values)
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            f'count="{len(values)}" uniqueCount="{len(values)}">{body}</sst>'
        )

    def _sheet_xml(self, rows: list[list[str]], string_index: dict[str, int]) -> str:
        row_xml: list[str] = []
        for row_num, row in enumerate(rows, start=1):
            cell_xml: list[str] = []
            for col_num, value in enumerate(row, start=1):
                ref = f"{self._col_name(col_num)}{row_num}"
                idx = string_index[value]
                cell_xml.append(f'<c r="{ref}" t="s"><v>{idx}</v></c>')
            row_xml.append(f'<row r="{row_num}">{"".join(cell_xml)}</row>')
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f'<sheetData>{"".join(row_xml)}</sheetData></worksheet>'
        )

    def _col_name(self, num: int) -> str:
        result = ""
        while num > 0:
            num, rem = divmod(num - 1, 26)
            result = chr(65 + rem) + result
        return result

    def _escape(self, value: str) -> str:
        return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
