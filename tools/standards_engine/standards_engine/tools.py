from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from tools.standards_engine.contracts.validate_contracts import ContractError, validate

from .engine import StandardsEngine
from .model import InspectCall, QueryCall, ReadRequest, RelatedRequest, RouteRequest


INTERFACE_SCHEMA = "tools/standards_engine/contracts/a1-contract.schema.json"


class AgentToolFacade:
    """Validated structured transport over the native Standards Engine API."""

    def __init__(self, engine: StandardsEngine, schema: Mapping[str, object]) -> None:
        self._engine = engine
        self._schema = schema

    @classmethod
    def open_repository(cls, root: Path) -> AgentToolFacade:
        repo_root = root.resolve()
        schema = json.loads((repo_root / INTERFACE_SCHEMA).read_text(encoding="utf-8"))
        return cls(StandardsEngine.open_repository(repo_root), schema)

    @property
    def snapshot(self) -> Mapping[str, object]:
        return self._engine.snapshot

    def query(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("QueryCall", value)
            request = self._mapping(value["request"])
            kind = request["kind"]
            if kind == "route":
                typed = RouteRequest(self._mapping(request["facts"]))
            elif kind == "read":
                typed = ReadRequest(str(request["target"]))
            elif kind == "related":
                typed = RelatedRequest(
                    str(request["target"]),
                    tuple(request["groups"]),
                    str(request["direction"]),
                    bool(request["transitive"]),
                )
            else:
                return self._rejected("INTERFACE.UNSUPPORTED_REQUEST", "unsupported")
            result = self._engine.query(QueryCall(self._mapping(value["snapshot"]), typed))
            output = result.as_contract()
            self._validate_result(output)
            return output
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))

    def inspect(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("InspectCall", value)
            result = self._engine.inspect(InspectCall(self._mapping(value["handle"])))
            output = result.as_contract()
            self._validate_result(output)
            return output
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))

    def _validate(self, definition: str, value: object) -> None:
        validate(
            self._schema,
            self._schema["$defs"][definition],
            value,
            "$arguments",
        )

    def _validate_result(self, value: dict[str, object]) -> None:
        definition = {
            "route-result": "RouteResult",
            "read-result": "ReadResult",
            "related-result": "RelatedResult",
            "snapshot-inspection-result": "SnapshotInspectionResult",
            "policy-inspection-result": "PolicyInspectionResult",
            "relationship-inspection-result": "RelationshipInspectionResult",
            "navigation-inspection-result": "NavigationInspectionResult",
            "rejected-result": "RejectedResult",
        }[str(value["kind"])]
        self._validate(definition, value)

    @staticmethod
    def _mapping(value: object) -> dict[str, object]:
        if not isinstance(value, Mapping):
            raise TypeError("structured tool arguments must be an object")
        return dict(value)

    @staticmethod
    def _rejected(
        code: str,
        outcome: str,
        message: str = "Structured tool arguments do not satisfy the interface contract.",
    ) -> dict[str, object]:
        return {
            "kind": "rejected-result",
            "code": code,
            "outcome": outcome,
            "message": message,
            "details": {},
            "next_operations": [],
        }
