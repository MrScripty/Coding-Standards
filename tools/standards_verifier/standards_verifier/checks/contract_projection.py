from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from typing import Any

from tools.standards_contracts.standards_contracts import (
    ContractError,
    compile_contracts,
)

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file


@dataclass(frozen=True, slots=True)
class ContractProjectionCheck:
    id: str
    schema: str
    interface: str
    python: str
    agent_tools: str
    examples: str

    def run(self, context: CheckContext) -> list[Diagnostic]:
        try:
            schema_path = contained_file(
                context.repo_root,
                self.schema,
                suite=context.suite_id,
                check=self.id,
            )
            interface_path = contained_file(
                context.repo_root,
                self.interface,
                suite=context.suite_id,
                check=self.id,
            )
            python_path = contained_file(
                context.repo_root,
                self.python,
                suite=context.suite_id,
                check=self.id,
            )
            tools_path = contained_file(
                context.repo_root,
                self.agent_tools,
                suite=context.suite_id,
                check=self.id,
            )
            examples_path = contained_file(
                context.repo_root,
                self.examples,
                suite=context.suite_id,
                check=self.id,
            )
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            with interface_path.open("rb") as source:
                interface = tomllib.load(source)
            contracts = compile_contracts(schema, interface)
            projection = contracts.project()
        except (
            ContractError,
            json.JSONDecodeError,
            OSError,
            tomllib.TOMLDecodeError,
            UnicodeError,
            ValueError,
        ) as error:
            return [
                Diagnostic(
                    "CONTRACT_PROJECTION.UNAVAILABLE",
                    "unavailable",
                    f"canonical contract projection cannot be compiled: {error}",
                    suite=context.suite_id,
                    check=self.id,
                )
            ]
        try:
            _validate_examples(
                json.loads(examples_path.read_text(encoding="utf-8")), contracts
            )
        except (ContractError, json.JSONDecodeError, OSError, UnicodeError, ValueError) as error:
            return [
                Diagnostic(
                    "CONTRACT_EXAMPLES.INVALID",
                    "invalid",
                    f"authored contract examples are invalid: {error}",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.examples,
                )
            ]

        diagnostics: list[Diagnostic] = []
        for path, observed, expected in (
            (
                self.python,
                python_path.read_text(encoding="utf-8"),
                projection.python_source,
            ),
            (
                self.agent_tools,
                tools_path.read_text(encoding="utf-8"),
                projection.agent_tools_json,
            ),
        ):
            if observed != expected:
                diagnostics.append(
                    Diagnostic(
                        "CONTRACT_PROJECTION.STALE",
                        "invalid",
                        "generated contract projection differs from compiler output",
                        suite=context.suite_id,
                        check=self.id,
                        path=path,
                    )
                )
        return diagnostics


def parse_contract_projection_check(
    raw: dict[str, Any],
    suite_id: str,
) -> ContractProjectionCheck:
    allowed = {
        "id",
        "type",
        "schema",
        "interface",
        "python",
        "agent_tools",
        "examples",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "contract_projection check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    values = {
        field: raw.get(field)
        for field in (
            "id",
            "schema",
            "interface",
            "python",
            "agent_tools",
            "examples",
        )
    }
    invalid = next(
        (
            field
            for field, value in values.items()
            if type(value) is not str or not value
        ),
        None,
    )
    if invalid is not None:
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING",
                "invalid",
                "contract_projection fields must be nonempty strings",
                suite=suite_id,
                field=invalid,
            )
        )
    return ContractProjectionCheck(
        values["id"],
        values["schema"],
        values["interface"],
        values["python"],
        values["agent_tools"],
        values["examples"],
    )


def _validate_examples(raw: object, contracts: object) -> None:
    if type(raw) is not dict or set(raw) != {
        "schema_version",
        "interface_schema_version",
        "examples",
    }:
        raise ValueError("example corpus envelope is incomplete or has unknown fields")
    if raw["schema_version"] != 2:
        raise ValueError("example corpus schema version is unsupported")
    if raw["interface_schema_version"] != contracts.interface.interface_schema_version:
        raise ValueError("example corpus targets another interface schema version")
    examples = raw["examples"]
    if type(examples) is not list or not examples:
        raise ValueError("example corpus must contain at least one example")
    names: set[str] = set()
    for example in examples:
        if type(example) is not dict or set(example) != {"name", "definition", "value"}:
            raise ValueError("each example must contain only name, definition, and value")
        name = example["name"]
        definition = example["definition"]
        if type(name) is not str or not name or name in names:
            raise ValueError("example names must be nonempty and unique")
        if type(definition) is not str or not definition:
            raise ValueError(f"example {name!r} has no definition")
        names.add(name)
        contracts.validate(definition, example["value"])


__all__ = ("ContractProjectionCheck", "parse_contract_projection_check")
