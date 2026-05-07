from __future__ import annotations

import argparse
from pathlib import Path

from src.agent import MappingSQLAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate data-platform SQL from a mapping document."
    )
    parser.add_argument(
        "--mapping",
        required=True,
        help="Path to the mapping document in JSON format.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write the generated SQL file.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    agent = MappingSQLAgent()
    result = agent.run(Path(args.mapping))

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(result["sql"] + "\n", encoding="utf-8")

    print("=== TASK SUMMARY ===")
    print(result["summary"])
    print()
    print("=== GENERATED SQL ===")
    print(result["sql"])
    print()
    print("=== STYLE CHECK ===")
    for issue in result["style_issues"]:
        print(f"- {issue}")


if __name__ == "__main__":
    main()
