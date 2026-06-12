from __future__ import annotations

import argparse
import base64
import json
import os
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from src.agent import MappingSQLAgent
from src.business_memory import BusinessMemoryService
from src.deepseek_config import DeepSeekConfigService
from src.demo_samples import get_demo_samples
from src.excel_mapping_parser import ExcelMappingParser
from src.mapping_impact import MappingImpactAnalyzer
from src.mapping_loader import MappingLoader
from src.sample_excel_builder import SampleExcelBuilder
from src.schema_sample_builder import SchemaSampleExcelBuilder
from src.schema_insight import SchemaInsightService
from src.sql_insight import SQLInsightService
from src.version_store import VersionStore


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "web"
EXAMPLE_PATH = BASE_DIR / "examples" / "mapping_sales_summary.json"
VERSIONS_DIR = BASE_DIR / "storage" / "versions"


class MappingSQLRequestHandler(BaseHTTPRequestHandler):
    agent = MappingSQLAgent()
    loader = MappingLoader()
    excel_parser = ExcelMappingParser()
    sample_excel_builder = SampleExcelBuilder()
    schema_sample_builder = SchemaSampleExcelBuilder()
    version_store = VersionStore(VERSIONS_DIR)
    impact_analyzer = MappingImpactAnalyzer()
    sql_insight = SQLInsightService()
    business_memory = BusinessMemoryService()
    schema_insight = SchemaInsightService()
    deepseek_config = DeepSeekConfigService()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self._serve_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/api/example":
            example_mapping = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
            self._send_json({"mapping": example_mapping})
            return
        if parsed.path == "/api/demo-samples":
            self._send_json(get_demo_samples())
            return
        if parsed.path == "/api/skills":
            self._send_json({"skills": self.business_memory.list_skills()})
            return
        if parsed.path == "/api/deepseek-config":
            self._send_json(self.deepseek_config.get_public_status())
            return
        if parsed.path == "/api/template.xlsx":
            self._serve_template()
            return
        if parsed.path == "/api/template-enhanced.xlsx":
            self._serve_enhanced_template()
            return
        if parsed.path == "/api/schema-template.xlsx":
            self._serve_schema_template()
            return
        if parsed.path == "/api/version-tasks":
            self._send_json({"tasks": self.version_store.list_tasks()})
            return
        if parsed.path == "/api/versions":
            self._handle_versions_list(parsed.query)
            return
        if parsed.path == "/api/version-detail":
            self._handle_version_detail(parsed.query)
            return
        if parsed.path == "/api/compare":
            self._handle_compare(parsed.query)
            return
        if parsed.path.startswith("/assets/"):
            self._serve_asset(STATIC_DIR / parsed.path.lstrip("/"))
            return

        self._send_json({"error": "Not found."}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)

        if parsed.path == "/api/generate":
            self._handle_generate()
            return
        if parsed.path == "/api/generate-stream":
            self._handle_generate_stream()
            return
        if parsed.path == "/api/parse-excel":
            self._handle_parse_excel()
            return
        if parsed.path == "/api/load-mapping-file":
            self._handle_load_mapping_file()
            return
        if parsed.path == "/api/compare-with-current":
            self._handle_compare_with_current()
            return
        if parsed.path == "/api/compare-with-current-stream":
            self._handle_compare_with_current_stream()
            return
        if parsed.path == "/api/demo-compare-setup":
            self._handle_demo_compare_setup()
            return
        if parsed.path == "/api/sql-insight":
            self._handle_sql_insight()
            return
        if parsed.path == "/api/schema-insight":
            self._handle_schema_insight()
            return
        if parsed.path == "/api/skills/save":
            self._handle_save_skill()
            return
        if parsed.path == "/api/skills/delete":
            self._handle_delete_skill()
            return
        if parsed.path == "/api/skills/generate-draft":
            self._handle_generate_skill_draft()
            return

        self._send_json({"error": "Not found."}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args) -> None:
        return

    def _handle_generate(self) -> None:
        try:
            body = self._read_json_body()
            result = self._build_generation_result(
                raw_mapping=body["mapping_text"],
                ai_config=body.get("ai_config", {}),
                save_version=True,
            )
            self._send_json(result)
        except KeyError:
            self._send_json(
                {"error": "Request body must include a 'mapping_text' field."},
                status=HTTPStatus.BAD_REQUEST,
            )
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_generate_stream(self) -> None:
        stream_started = False
        try:
            body = self._read_json_body()
            self._start_sse()
            stream_started = True
            self._stream_steps(
                [
                    "Step 1: 解析 Mapping 结构",
                    "Step 2: 识别来源表与目标字段",
                    "Step 3: 推导 Join 与过滤条件",
                    "Step 4: 注入 Skill / Memory 业务逻辑",
                    "Step 5: 输出 SQL 与校验结果",
                ]
            )
            result = self._build_generation_result(
                raw_mapping=body["mapping_text"],
                ai_config=body.get("ai_config", {}),
                save_version=True,
            )
            self._write_sse_event("result", result)
            self._write_sse_event("done", {"ok": True})
            self.close_connection = True
        except Exception as exc:  # noqa: BLE001
            self._safe_sse_error(exc, stream_started)

    def _handle_parse_excel(self) -> None:
        try:
            body = self._read_json_body()
            filename = body.get("filename", "mapping.xlsx")
            content = base64.b64decode(body["file_base64"])
            parsed = self.excel_parser.parse_with_metadata(content)
            mapping = parsed["mapping"]
            self._send_json(
                {
                    "filename": filename,
                    "mapping": mapping,
                    "mapping_text": json.dumps(mapping, ensure_ascii=False, indent=2),
                    "format": parsed["format"],
                    "diagnostics": parsed["diagnostics"],
                    "message": parsed["message"],
                    "schema_text": parsed.get("schema_text", ""),
                    "schema_source": parsed.get("schema_source", ""),
                }
            )
        except KeyError:
            self._send_json(
                {"error": "Request body must include a 'file_base64' field."},
                status=HTTPStatus.BAD_REQUEST,
            )
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_load_mapping_file(self) -> None:
        try:
            body = self._read_json_body()
            filename = body.get("filename", "")
            mode = body.get("mode", "rule")
            if not filename:
                raise ValueError("filename is required.")

            content = base64.b64decode(body["file_base64"])
            lower_name = filename.lower()

            if lower_name.endswith(".xlsx"):
                parsed = self.excel_parser.parse_with_metadata(content)
                mapping_text = json.dumps(parsed["mapping"], ensure_ascii=False, indent=2)
                message = parsed["message"]
            elif lower_name.endswith((".csv", ".md", ".markdown", ".json", ".txt")):
                mapping_text = content.decode("utf-8", errors="ignore").strip()
                if not mapping_text:
                    raise ValueError("上传文件内容为空。")
                message = "文件内容已加载到编辑区，智能体会结合内容自动分析 Mapping 结构。"
            else:
                raise ValueError("当前仅支持 .xlsx、.csv、.md、.markdown、.json、.txt 文件。")

            self._send_json(
                {
                    "filename": filename,
                    "mapping_text": mapping_text,
                    "format": parsed["format"] if lower_name.endswith(".xlsx") else "raw_text",
                    "diagnostics": parsed["diagnostics"] if lower_name.endswith(".xlsx") else [],
                    "schema_text": parsed.get("schema_text", "") if lower_name.endswith(".xlsx") else "",
                    "schema_source": parsed.get("schema_source", "") if lower_name.endswith(".xlsx") else "",
                    "message": message,
                }
            )
        except KeyError:
            self._send_json(
                {"error": "Request body must include filename and file_base64."},
                status=HTTPStatus.BAD_REQUEST,
            )
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_versions_list(self, query: str) -> None:
        task_name = parse_qs(query).get("task_name", [""])[0]
        if not task_name:
            self._send_json({"error": "task_name is required."}, status=HTTPStatus.BAD_REQUEST)
            return
        self._send_json({"versions": self.version_store.list_versions(task_name)})

    def _handle_version_detail(self, query: str) -> None:
        try:
            params = parse_qs(query)
            task_name = params.get("task_name", [""])[0]
            version_no = int(params.get("version_no", ["0"])[0])
            if not task_name or not version_no:
                raise ValueError("task_name and version_no are required.")
            self._send_json(self.version_store.get_version(task_name, version_no))
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_compare(self, query: str) -> None:
        try:
            params = parse_qs(query)
            task_name = params.get("task_name", [""])[0]
            left = int(params.get("left", ["0"])[0])
            right = int(params.get("right", ["0"])[0])
            if not task_name or not left or not right:
                raise ValueError("task_name, left, and right are required.")
            self._send_json(self.version_store.compare_versions(task_name, left, right))
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_compare_with_current(self) -> None:
        try:
            body = self._read_json_body()
            compare_payload = self._build_compare_payload(
                task_name=body["task_name"],
                version_no=int(body["version_no"]),
                raw_mapping=body["mapping_text"],
                ai_config=body.get("ai_config", {}),
            )
            self._send_json(compare_payload)
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_compare_with_current_stream(self) -> None:
        stream_started = False
        try:
            body = self._read_json_body()
            self._start_sse()
            stream_started = True
            self._stream_steps(
                [
                    "Step 1: 读取历史版本与当前 Mapping",
                    "Step 2: 解析当前来源表、字段与过滤条件",
                    "Step 3: 注入 Skill / Memory 逻辑并生成 SQL",
                    "Step 4: 分析 Mapping 变化与 SQL 影响",
                    "Step 5: 输出对比结果",
                ]
            )
            compare_payload = self._build_compare_payload(
                task_name=body["task_name"],
                version_no=int(body["version_no"]),
                raw_mapping=body["mapping_text"],
                ai_config=body.get("ai_config", {}),
            )
            self._write_sse_event("result", compare_payload)
            self._write_sse_event("done", {"ok": True})
            self.close_connection = True
        except Exception as exc:  # noqa: BLE001
            self._safe_sse_error(exc, stream_started)

    def _handle_demo_compare_setup(self) -> None:
        try:
            samples = get_demo_samples()
            compare_sample = samples["compare"]
            history_versions = compare_sample.get("history", [])
            current_sample = compare_sample.get("current", {})
            task_name = (
                current_sample.get("mapping", {}).get("task_name")
                or history_versions[0].get("mapping", {}).get("task_name")
            )
            if not task_name:
                raise ValueError("版本对比样例缺少 task_name。")
            existing_versions = self.version_store.list_versions(task_name)

            if len(existing_versions) < 2:
                for version in history_versions:
                    result = self.agent.run_mapping(version["mapping"])
                    self.version_store.save(
                        mapping=version["mapping"],
                        sql=result["sql"],
                        mode=version.get("mode", "rule"),
                        style_issues=result["style_issues"],
                        summary=result["summary"],
                        user_requirement=version.get("requirement", ""),
                    )
                existing_versions = self.version_store.list_versions(task_name)

            self._send_json(
                {
                    "task_name": task_name,
                    "versions": existing_versions,
                    "selected_version_no": 2 if len(existing_versions) >= 2 else 1,
                    "current": {
                        "mode": current_sample.get("mode", "deepseek"),
                        "skill_id": current_sample.get("skill_id", "none"),
                        "requirement": current_sample.get("requirement", ""),
                        "mapping": current_sample.get("mapping", {}),
                    },
                    "description": compare_sample["description"],
                }
            )
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_sql_insight(self) -> None:
        try:
            body = self._read_json_body()
            ai_config = self._resolve_ai_config(body.get("ai_config", {}))
            memory_enabled = bool(ai_config.get("include_memory")) and ai_config.get("skill_id", "none") != "none"
            memory_context = self.business_memory.build_prompt_context(
                skill_id=ai_config.get("skill_id", "none"),
                include_memory=memory_enabled,
            )
            ai_config["selected_skill_detail"] = memory_context["selected_skill"] or self.business_memory.get_skill("none")
            ai_config["memory_items"] = memory_context["memory_items"]
            result = self.sql_insight.analyze(body["sql_text"], ai_config)
            result["sql_diff"] = self.version_store._line_diff(
                result["original_sql"],
                result["optimized_sql"],
            )
            result["requested_ai_enabled"] = bool(ai_config.get("enabled"))
            result["selected_skill"] = ai_config.get("skill_id", "none")
            result["selected_skill_detail"] = ai_config["selected_skill_detail"]
            result["memory_enabled"] = memory_enabled
            result["memory_items_used"] = memory_context["memory_items"]
            result["schema_analysis_used"] = ai_config.get("schema_analysis") if ai_config.get("use_schema_assist") else None
            self._send_json(result)
        except KeyError:
            self._send_json(
                {"error": "Request body must include a 'sql_text' field."},
                status=HTTPStatus.BAD_REQUEST,
            )
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_schema_insight(self) -> None:
        try:
            body = self._read_json_body()
            ai_config = self._resolve_ai_config(body.get("ai_config", {}))
            filename = body.get("filename", "")
            if body.get("file_base64"):
                content = base64.b64decode(body["file_base64"])
                if filename.lower().endswith(".xlsx"):
                    result = self.schema_insight.analyze_excel(content, ai_config)
                else:
                    schema_text = content.decode("utf-8", errors="ignore")
                    input_format = self._detect_schema_format(schema_text, filename)
                    result = self.schema_insight.analyze_text(schema_text, input_format, ai_config)
            else:
                schema_text = body["schema_text"]
                input_format = self._detect_schema_format(schema_text, filename)
                result = self.schema_insight.analyze_text(schema_text, input_format, ai_config)
            result["recommended_skills"] = self.business_memory.recommend_skills_from_schema(result)
            self._send_json(result)
        except KeyError:
            self._send_json(
                {"error": "Request body must include 'schema_text' or 'file_base64'."},
                status=HTTPStatus.BAD_REQUEST,
            )
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_save_skill(self) -> None:
        try:
            body = self._read_json_body()
            skill = self.business_memory.save_skill(body.get("skill", {}))
            self._send_json({"skill": skill, "skills": self.business_memory.list_skills()})
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_delete_skill(self) -> None:
        try:
            body = self._read_json_body()
            self.business_memory.delete_skill(body.get("skill_id", ""))
            self._send_json({"skills": self.business_memory.list_skills()})
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_generate_skill_draft(self) -> None:
        try:
            body = self._read_json_body()
            draft = self.business_memory.generate_skill_draft(
                scenario=body.get("scenario", ""),
                schema_text=body.get("schema_text", ""),
                requirement=body.get("requirement", ""),
            )
            self._send_json({"skill": draft})
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _build_generation_result(self, raw_mapping: str, ai_config: dict, save_version: bool) -> dict:
        ai_config = self._resolve_ai_config(ai_config)
        use_ai = bool(ai_config.get("enabled"))
        mapping_diagnosis: list[str] = []
        mapping_repaired = False

        try:
            mapping = self.loader.load_from_text(raw_mapping)
        except Exception as parse_exc:  # noqa: BLE001
            if not use_ai:
                raise ValueError(
                    f"Mapping parse failed: {parse_exc}. Rule mode requires valid JSON input."
                ) from parse_exc
            repair_result = self.agent.repair_mapping_text(raw_mapping, ai_config)
            mapping = repair_result["mapping"]
            mapping_diagnosis = repair_result["diagnosis"]
            mapping_repaired = True

        if use_ai:
            try:
                result = self.agent.run_mapping_with_ai(mapping, ai_config)
                result["fallback_used"] = False
            except Exception as exc:  # noqa: BLE001
                result = self.agent.run_mapping(mapping)
                result["fallback_used"] = True
                result["fallback_reason"] = str(exc)
        else:
            result = self.agent.run_mapping(mapping)
            result["fallback_used"] = False

        result["normalized_mapping"] = mapping
        result["mapping_diagnosis"] = mapping_diagnosis
        result["mapping_repaired"] = mapping_repaired
        result["requested_ai_enabled"] = use_ai
        result["selected_skill"] = ai_config.get("skill_id", "none")
        memory_enabled = bool(ai_config.get("include_memory")) and ai_config.get("skill_id", "none") != "none"
        result["memory_enabled"] = memory_enabled
        memory_context = self.business_memory.build_prompt_context(
            skill_id=ai_config.get("skill_id", "none"),
            include_memory=memory_enabled,
        )
        result["selected_skill_detail"] = memory_context["selected_skill"] or self.business_memory.get_skill("none")
        result["memory_items_used"] = memory_context["memory_items"]
        result["schema_analysis_used"] = ai_config.get("schema_analysis") if ai_config.get("use_schema_assist") else None

        if save_version:
            version_record = self.version_store.save(
                mapping=mapping,
                sql=result["sql"],
                mode=result.get("mode", "rule"),
                style_issues=result["style_issues"],
                summary=result["summary"],
                user_requirement=ai_config.get("user_requirement", ""),
            )
            result["version_record"] = {
                "version_no": version_record["version_no"],
                "created_at": version_record["created_at"],
                "task_name": version_record["task_name"],
            }
            result["user_requirement"] = ai_config.get("user_requirement", "")

        return result

    def _resolve_ai_config(self, ai_config: dict | None) -> dict:
        config = dict(ai_config or {})
        if not config.get("enabled"):
            return config
        runtime = self.deepseek_config.load_runtime_config()
        config["api_key"] = runtime["api_key"]
        config["model"] = runtime["model"]
        config["base_url"] = runtime["base_url"]
        config["config_loaded_from_server"] = True
        config["config_status"] = self.deepseek_config.get_public_status()
        return config

    def _build_compare_payload(
        self,
        task_name: str,
        version_no: int,
        raw_mapping: str,
        ai_config: dict,
    ) -> dict:
        historical = self.version_store.get_version(task_name, version_no)
        current_result = self._build_generation_result(raw_mapping, ai_config, save_version=False)
        return {
            "task_name": task_name,
            "historical": {
                "version_no": historical["version_no"],
                "created_at": historical["created_at"],
                "mode": historical["mode"],
                "summary": historical["summary"],
                "mapping": historical["mapping"],
                "sql": historical["sql"],
                "user_requirement": historical.get("user_requirement", ""),
            },
            "current": {
                "summary": current_result["summary"],
                "mapping": current_result["normalized_mapping"],
                "sql": current_result["sql"],
                "mode": current_result.get("mode", "rule"),
                "mapping_diagnosis": current_result["mapping_diagnosis"],
                "mapping_repaired": current_result["mapping_repaired"],
                "requested_ai_enabled": current_result["requested_ai_enabled"],
                "fallback_used": current_result["fallback_used"],
                "style_issues": current_result["style_issues"],
                "field_checks": current_result["field_checks"],
                "user_requirement": ai_config.get("user_requirement", ""),
                "selected_skill": current_result["selected_skill"],
                "selected_skill_detail": current_result["selected_skill_detail"],
                "memory_enabled": current_result["memory_enabled"],
                "memory_items_used": current_result["memory_items_used"],
            },
            "mapping_impacts": self.impact_analyzer.analyze(
                historical["mapping"],
                current_result["normalized_mapping"],
            ),
            "sql_diff": self.version_store._line_diff(historical["sql"], current_result["sql"]),
            "mapping_diff": self.version_store._line_diff(
                json.dumps(historical["mapping"], ensure_ascii=False, indent=2),
                json.dumps(current_result["normalized_mapping"], ensure_ascii=False, indent=2),
            ),
        }

    def _detect_schema_format(self, schema_text: str, filename: str = "") -> str:
        lower_name = filename.lower()
        lowered = schema_text.lower().strip()
        if lower_name.endswith(".xlsx"):
            return "excel"
        if lower_name.endswith(".csv"):
            return "csv"
        if lowered.startswith("[table]") or lowered.startswith("[schema]") or lowered.startswith("[字段需求]"):
            return "text"
        if lower_name.endswith(".json") or lowered.startswith("{") or lowered.startswith("[{") or lowered.startswith('["') or lowered == "[]":
            return "json"
        if lower_name.endswith(".sql") or "create table" in lowered:
            return "ddl"
        if "," in schema_text and "\n" in schema_text:
            return "csv"
        return "text"

    def _read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(content_length)
        return json.loads(payload.decode("utf-8"))

    def _serve_template(self) -> None:
        content = self.sample_excel_builder.build()
        self.send_response(HTTPStatus.OK)
        self.send_header(
            "Content-Type",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.send_header(
            "Content-Disposition",
            'attachment; filename="business_requirement_sample.xlsx"',
        )
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _serve_enhanced_template(self) -> None:
        content = self.sample_excel_builder.build_enhanced()
        self.send_response(HTTPStatus.OK)
        self.send_header(
            "Content-Type",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.send_header(
            "Content-Disposition",
            'attachment; filename="business_requirement_enhanced_sample.xlsx"',
        )
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _serve_schema_template(self) -> None:
        content = self.schema_sample_builder.build()
        self.send_response(HTTPStatus.OK)
        self.send_header(
            "Content-Type",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.send_header(
            "Content-Disposition",
            'attachment; filename="schema_sample.xlsx"',
        )
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _serve_asset(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self._send_json({"error": "Asset not found."}, status=HTTPStatus.NOT_FOUND)
            return

        content_type = "text/plain; charset=utf-8"
        if path.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"
        self._serve_file(path, content_type)

    def _serve_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self._send_json({"error": "File not found."}, status=HTTPStatus.NOT_FOUND)
            return

        content = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _start_sse(self) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

    def _write_sse_event(self, event_type: str, payload: dict) -> None:
        body = json.dumps({"type": event_type, "payload": payload}, ensure_ascii=False)
        self.wfile.write(f"data: {body}\n\n".encode("utf-8"))
        self.wfile.flush()

    def _stream_steps(self, steps: list[str]) -> None:
        for item in steps:
            self._write_sse_event("step", {"message": item})
            time.sleep(0.08)

    def _safe_sse_error(self, exc: Exception, stream_started: bool) -> None:
        try:
            if not stream_started:
                self._start_sse()
            self._write_sse_event("error", {"message": str(exc)})
            self.close_connection = True
        except Exception:  # noqa: BLE001
            pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Mapping SQL web application.")
    parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"), help="Host to bind the web app.")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")), help="Port to bind the web app.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    server = ThreadingHTTPServer((args.host, args.port), MappingSQLRequestHandler)
    print(f"Mapping SQL Agent Web is running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
