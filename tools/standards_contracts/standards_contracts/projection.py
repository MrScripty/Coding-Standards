from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path

from .compiler import compile_contracts


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPOSITORY_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json"
INTERFACE_PATH = REPOSITORY_ROOT / "tools/standards_engine/contracts/a1-interface.toml"
PYTHON_PATH = (
    REPOSITORY_ROOT
    / "tools/standards_engine/standards_engine/_generated_contract.py"
)
TOOLS_PATH = (
    REPOSITORY_ROOT / "tools/standards_engine/contracts/generated/agent-tools.json"
)


def render_repository_projections() -> dict[Path, str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    with INTERFACE_PATH.open("rb") as source:
        interface = tomllib.load(source)
    artifacts = compile_contracts(schema, interface).project()
    return {
        PYTHON_PATH: artifacts.python_source,
        TOOLS_PATH: artifacts.agent_tools_json,
    }


def projection_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile the canonical A1c schema and interface projections."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when a committed projection differs from compiler output",
    )
    arguments = parser.parse_args(argv)
    projections = render_repository_projections()
    if arguments.check:
        stale = [
            path
            for path, content in projections.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            for path in stale:
                print(
                    "stale generated contract projection: "
                    f"{path.relative_to(REPOSITORY_ROOT)}"
                )
            return 1
        return 0
    for path, content in projections.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(projection_main())
