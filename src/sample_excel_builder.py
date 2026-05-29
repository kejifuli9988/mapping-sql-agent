from __future__ import annotations

from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile


CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet4.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet5.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
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
    <sheet name="overview" sheetId="1" r:id="rId1"/>
    <sheet name="sources" sheetId="2" r:id="rId2"/>
    <sheet name="joins" sheetId="3" r:id="rId3"/>
    <sheet name="filters" sheetId="4" r:id="rId4"/>
    <sheet name="target_columns" sheetId="5" r:id="rId5"/>
  </sheets>
</workbook>
"""

WORKBOOK_RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet4.xml"/>
  <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet5.xml"/>
  <Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
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
  <dc:title>Mapping Template</dc:title>
  <dc:creator>Codex</dc:creator>
</cp:coreProperties>
"""

APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>
"""


class SampleExcelBuilder:
    """Generate a small xlsx mapping template without external dependencies."""

    def build(self) -> bytes:
        sheets = {
            "sheet1.xml": [
                ["key", "value"],
                ["task_name", "dws_custody_product_clearing_day"],
                ["target_table", "dws_custody_product_clearing_day"],
                ["target_partition", "dt='${biz_date}'"],
            ],
            "sheet2.xml": [
                ["name", "alias"],
                ["dwd_custody_clearing_detail_di", "cl"],
                ["dim_custody_product_df", "dp"],
            ],
            "sheet3.xml": [
                ["type", "right_alias", "condition"],
                ["left", "dp", "cl.product_id = dp.product_id"],
            ],
            "sheet4.xml": [
                ["condition"],
                ["cl.dt = '${biz_date}'"],
                ["cl.clear_status in ('success', 'fail')"],
            ],
            "sheet5.xml": [
                ["name", "expression"],
                ["dt", "'${biz_date}'"],
                ["product_id", "cl.product_id"],
                ["product_name", "dp.product_name"],
                ["clear_amt", "SUM(cl.clear_amt)"],
                ["clear_cnt", "COUNT(DISTINCT cl.clear_id)"],
                ["fail_cnt", "SUM(CASE WHEN cl.clear_status = 'fail' THEN 1 ELSE 0 END)"],
            ],
        }

        shared_strings: list[str] = []
        for rows in sheets.values():
            for row in rows:
                shared_strings.extend(row)

        unique_strings: list[str] = []
        seen: dict[str, int] = {}
        for item in shared_strings:
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
            for filename, rows in sheets.items():
                zf.writestr(f"xl/worksheets/{filename}", self._sheet_xml(rows, seen))
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
        return (
            value.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
