from __future__ import annotations

import argparse
import base64
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from src.agent import MappingSQLAgent
from src.excel_mapping_parser import ExcelMappingParser
from src.mapping_loader import MappingLoader
from src.sample_excel_builder import SampleExcelBuilder
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
    version_store = VersionStore(VERSIONS_DIR)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self._serve_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
            return

        if parsed.path == "/api/example":
            example_mapping = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
            self._send_json({"mapping": example_mapping})
            return

        if parsed.path == "/api/template.xlsx":
            self._serve_template()
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
            asset_path = STATIC_DIR / parsed.path.lstrip("/")
            self._serve_asset(asset_path)
            return

        self._send_json({"error": "Not found."}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/generate":
            self._handle_generate()
            return
        if parsed.path == "/api/parse-excel":
            self._handle_parse_excel()
            return
        if parsed.path == "/api/compare-with-current":
            self._handle_compare_with_current()
            return

        self._send_json({"error": "Not found."}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args) -> None:
        return

    def _handle_generate(self) -> None:
        try:
            body = self._read_json_body()
            raw_mapping = body["mapping_text"]
            ai_config = body.get("ai_config", {})
            result = self._build_generation_result(raw_mapping, ai_config, save_version=True)
            self._send_json(result)
        except KeyError:
            self._send_json(
                {"error": "Request body must include a 'mapping_text' field."},
                status=HTTPStatus.BAD_REQUEST,
            )
        except json.JSONDecodeError:
            self._send_json(
                {"error": "Request body is not valid JSON."},
                status=HTTPStatus.BAD_REQUEST,
            )
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_parse_excel(self) -> None:
        try:
            body = self._read_json_body()
            filename = body.get("filename", "mapping.xlsx")
            file_base64 = body["file_base64"]
            content = base64.b64decode(file_base64)
            mapping = self.excel_parser.parse(content)
            self._send_json(
                {
                    "filename": filename,
                    "mapping": mapping,
                    "mapping_text": json.dumps(mapping, ensure_ascii=False, indent=2),
                    "message": "Excel mapping parsed successfully and has been filled into the editor.",
                }
            )
        except KeyError:
            self._send_json(
                {"error": "Request body must include a 'file_base64' field."},
                status=HTTPStatus.BAD_REQUEST,
            )
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_versions_list(self, query: str) -> None:
        params = parse_qs(query)
        task_name = params.get("task_name", [""])[0]
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
            detail = self.version_store.get_version(task_name, version_no)
            self._send_json(detail)
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
            result = self.version_store.compare_versions(task_name, left, right)
            self._send_json(result)
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _handle_compare_with_current(self) -> None:
        try:
            body = self._read_json_body()
            task_name = body["task_name"]
            version_no = int(body["version_no"])
            raw_mapping = body["mapping_text"]
            ai_config = body.get("ai_config", {})

            historical = self.version_store.get_version(task_name, version_no)
            current_result = self._build_generation_result(raw_mapping, ai_config, save_version=False)

            compare_payload = {
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
                    "user_requirement": ai_config.get("user_requirement", ""),
                },
                "sql_diff": self.version_store._line_diff(historical["sql"], current_result["sql"]),
                "mapping_diff": self.version_store._line_diff(
                    json.dumps(historical["mapping"], ensure_ascii=False, indent=2),
                    json.dumps(current_result["normalized_mapping"], ensure_ascii=False, indent=2),
                ),
            }
            self._send_json(compare_payload)
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def _build_generation_result(
        self,
        raw_mapping: str,
        ai_config: dict,
        save_version: bool,
    ) -> dict:
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
            'attachment; filename="mapping_template.xlsx"',
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

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Mapping SQL web application.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the web app.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the web app.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    server = ThreadingHTTPServer((args.host, args.port), MappingSQLRequestHandler)
    print(f"Mapping SQL Agent Web is running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
