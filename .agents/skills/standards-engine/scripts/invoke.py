#!/usr/bin/env python3
"""Invoke one generated Standards Engine operation with JSON on standard input."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path

GENERATED_CONTRACT = Path("tools/standards_engine/contracts/generated/agent-tools.json")
AUTHORED_EXAMPLES = Path("tools/standards_engine/contracts/examples/a1-examples.json")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Invoke or inspect the generated Standards Engine Interface."
    )
    parser.add_argument("operation", nargs="?")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--list", action="store_true", dest="list_operations")
    mode.add_argument("--example", action="store_true")
    mode.add_argument("--schema", action="store_true")
    return parser


def _object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def _operations(contract: Mapping[str, object]) -> dict[str, Mapping[str, object]]:
    values = contract.get("operations")
    if not isinstance(values, list):
        raise ValueError("generated contract has no operations array")
    selected: dict[str, Mapping[str, object]] = {}
    for value in values:
        if not isinstance(value, Mapping) or not isinstance(value.get("id"), str):
            raise ValueError("generated contract contains an invalid operation")
        selected[str(value["id"])] = value
    return selected


def _operation(
    arguments: argparse.Namespace,
    operations: Mapping[str, Mapping[str, object]],
) -> Mapping[str, object]:
    if not arguments.operation:
        raise ValueError("an operation is required")
    try:
        return operations[arguments.operation]
    except KeyError as error:
        raise ValueError(f"unknown operation: {arguments.operation}") from error


def _schema_closure(
    contract: Mapping[str, object], operation: Mapping[str, object]
) -> dict[str, object]:
    definitions = contract.get("$defs")
    if not isinstance(definitions, Mapping):
        raise ValueError("generated contract has no definitions object")
    root = operation.get("input_schema")
    if not isinstance(root, Mapping):
        raise ValueError("operation has no input schema")
    selected: dict[str, object] = {}

    def visit(value: object) -> None:
        if isinstance(value, Mapping):
            reference = value.get("$ref")
            if isinstance(reference, str) and reference.startswith("#/$defs/"):
                name = reference.rsplit("/", 1)[-1]
                if name not in selected:
                    definition = definitions.get(name)
                    if definition is None:
                        raise ValueError(f"missing generated definition: {name}")
                    selected[name] = definition
                    visit(definition)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(root)
    return {"input_schema": root, "$defs": selected}


def _examples(root: Path, operation: Mapping[str, object]) -> list[object]:
    authored = _object(root / AUTHORED_EXAMPLES)
    values = authored.get("examples")
    definition = operation.get("input_definition")
    if not isinstance(values, list) or not isinstance(definition, str):
        raise ValueError("authored examples do not match the generated contract")
    selected = [
        value
        for value in values
        if isinstance(value, Mapping) and value.get("definition") == definition
    ]
    if not selected:
        raise ValueError(
            f"no authored example exists for {operation['id']}; use --schema"
        )
    return selected


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    root = arguments.repo_root.resolve()
    try:
        contract = _object(root / GENERATED_CONTRACT)
        operations = _operations(contract)
        if arguments.list_operations:
            print("\n".join(sorted(operations)))
            return 0
        operation = _operation(arguments, operations)
        if arguments.example:
            print(json.dumps(_examples(root, operation), indent=2, sort_keys=True))
            return 0
        if arguments.schema:
            print(
                json.dumps(
                    _schema_closure(contract, operation), indent=2, sort_keys=True
                )
            )
            return 0
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise ValueError("standard input must contain one JSON object")
        try:
            from tools.standards_engine.standards_engine import AgentToolFacade
        except ModuleNotFoundError as error:
            raise ValueError(
                "Engine runtime dependencies are unavailable; read "
                ".agents/skills/standards-engine/references/environment.md"
            ) from error
        with AgentToolFacade.open_repository(root) as facade:
            result = getattr(facade, str(operation["id"]))(request)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (
        AttributeError,
        json.JSONDecodeError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        print(f"standards-engine invocation error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
