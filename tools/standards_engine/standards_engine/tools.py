from __future__ import annotations

import json
import tomllib
from collections.abc import Mapping
from pathlib import Path

from tools.standards_contracts.standards_contracts import (
    CompiledContracts,
    ContractError,
    OperationContract,
    compile_contracts,
)

from . import _generated_contract as generated_contract
from ._generated_contract import decode_contract
from .engine import StandardsEngine
from ._generated_contract import (
    AnalyzeProposalCall,
    CreateSnapshotCall,
    CreateProposalCall,
    DeleteSnapshotCall,
    FindSnapshotsCall,
    FindProposalsCall,
    InspectCall,
    PrepareCall,
    QueryCall,
    QueryProposalCall,
    ReviseProposalCall,
    ResolveCall,
    UndeleteSnapshotCall,
)


INTERFACE_SCHEMA = "tools/standards_engine/contracts/a1-contract.schema.json"
INTERFACE_CONTRACT = "tools/standards_engine/contracts/a1-interface.toml"


class InterfaceVersionError(ValueError):
    pass


class AgentToolFacade:
    """Validated structured transport over the native Standards Engine API."""

    def __init__(self, engine: StandardsEngine, contracts: CompiledContracts) -> None:
        self._engine = engine
        self._contracts = contracts
        self._operations = {
            operation.id: operation for operation in contracts.interface.operations
        }
        schema = contracts.schema
        self._handle_versions = self._derive_handle_versions(schema)
        self._result_types = {
            operation.id: self._concrete_model_types(
                schema, operation.result_definitions
            )
            for operation in contracts.interface.operations
        }

    @classmethod
    def open_repository(cls, root: Path) -> AgentToolFacade:
        repo_root = root.resolve()
        engine = StandardsEngine.open_repository(repo_root)
        try:
            return cls(engine, _contracts(repo_root))
        except Exception:
            engine.close()
            raise

    def close(self) -> None:
        self._engine.close()

    def __enter__(self) -> AgentToolFacade:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def create_snapshot(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection(
            "create_snapshot", arguments, CreateSnapshotCall
        )
        if isinstance(call, dict):
            return call
        return self._result("create_snapshot", self._engine.create_snapshot(call))

    def find_snapshots(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection("find_snapshots", arguments, FindSnapshotsCall)
        if isinstance(call, dict):
            return call
        return self._result("find_snapshots", self._engine.find_snapshots(call))

    def create_proposal(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection("create_proposal", arguments, CreateProposalCall)
        if isinstance(call, dict):
            return call
        return self._result("create_proposal", self._engine.create_proposal(call))

    def find_proposals(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection("find_proposals", arguments, FindProposalsCall)
        if isinstance(call, dict):
            return call
        return self._result("find_proposals", self._engine.find_proposals(call))

    def revise_proposal(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection("revise_proposal", arguments, ReviseProposalCall)
        if isinstance(call, dict):
            return call
        return self._result("revise_proposal", self._engine.revise_proposal(call))

    def query_proposal(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection("query_proposal", arguments, QueryProposalCall)
        if isinstance(call, dict):
            return call
        return self._result("query_proposal", self._engine.query_proposal(call))

    def analyze_proposal(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection(
            "analyze_proposal", arguments, AnalyzeProposalCall
        )
        if isinstance(call, dict):
            return call
        return self._result(
            "analyze_proposal", self._engine.analyze_proposal(call)
        )

    def delete_snapshot(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection(
            "delete_snapshot", arguments, DeleteSnapshotCall
        )
        if isinstance(call, dict):
            return call
        return self._result("delete_snapshot", self._engine.delete_snapshot(call))

    def undelete_snapshot(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection(
            "undelete_snapshot", arguments, UndeleteSnapshotCall
        )
        if isinstance(call, dict):
            return call
        return self._result("undelete_snapshot", self._engine.undelete_snapshot(call))

    def query(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection("query", arguments, QueryCall)
        if isinstance(call, dict):
            return call
        result = self._engine.query(call)
        return self._result("query", result)

    def prepare(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection("prepare", arguments, PrepareCall)
        if isinstance(call, dict):
            return call
        result = self._engine.prepare(call)
        return self._result("prepare", result)

    def resolve(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection("resolve", arguments, ResolveCall)
        if isinstance(call, dict):
            return call
        result = self._engine.resolve(call)
        return self._result("resolve", result)

    def inspect(self, arguments: object) -> dict[str, object]:
        call = self._call_or_rejection("inspect", arguments, InspectCall)
        if isinstance(call, dict):
            return call
        result = self._engine.inspect(call)
        return self._result("inspect", result)

    def _call_or_rejection(
        self, operation: str, arguments: object, expected_type: type
    ) -> object:
        try:
            return self._decode_call(operation, arguments, expected_type)
        except InterfaceVersionError as error:
            return self._rejected(
                "INTERFACE.UNSUPPORTED_VERSION", "unsupported", str(error)
            )
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))

    def _decode_call(self, operation: str, arguments: object, expected_type):
        contract = self._operation(operation)
        value = self._mapping(arguments)
        self._require_supported_handle_versions(value)
        call = decode_contract(contract.input_definition, value)
        if not isinstance(call, expected_type):
            raise RuntimeError(
                f"generated {contract.input_definition} decoder returned the wrong type"
            )
        return call

    def _result(self, operation: str, result) -> dict[str, object]:
        contract = self._operation(operation)
        definition = type(result).__definition__
        expected_type = generated_contract.MODEL_TYPES.get(definition)
        if (
            type(result) is expected_type
            and type(result) in self._result_types[contract.id]
        ):
            return result.as_contract()
        raise RuntimeError(
            f"engine returned {definition} outside the {operation} result algebra"
        )

    def _operation(self, operation: str) -> OperationContract:
        try:
            return self._operations[operation]
        except KeyError:
            raise RuntimeError(
                f"compiled interface does not declare operation {operation!r}"
            ) from None

    @staticmethod
    def _derive_handle_versions(schema: object) -> dict[str, int]:
        if not isinstance(schema, dict):
            raise TypeError("canonical schema must be an object")
        definitions = schema.get("$defs")
        if not isinstance(definitions, Mapping):
            raise TypeError("canonical schema definitions must be an object")
        versions: dict[str, int] = {}
        for definition in definitions.values():
            if not isinstance(definition, Mapping):
                continue
            properties = definition.get("properties")
            if not isinstance(properties, Mapping):
                continue
            kind_schema = properties.get("kind")
            version_schema = properties.get("schema_version")
            if not isinstance(kind_schema, Mapping) or not isinstance(
                version_schema, Mapping
            ):
                continue
            kind = kind_schema.get("const")
            version = version_schema.get("const")
            if isinstance(kind, str) and kind.endswith("-handle") and isinstance(
                version, int
            ):
                versions[kind] = version
        return versions

    @staticmethod
    def _concrete_model_types(
        schema: object, definitions: tuple[str, ...]
    ) -> frozenset[type]:
        if not isinstance(schema, Mapping):
            raise TypeError("canonical schema must be an object")
        nodes = schema.get("$defs")
        if not isinstance(nodes, Mapping):
            raise TypeError("canonical schema definitions must be an object")
        selected: set[type] = set()

        def collect(name: str) -> None:
            model_type = generated_contract.MODEL_TYPES.get(name)
            if model_type is not None:
                selected.add(model_type)
                return
            node = nodes.get(name)
            variants = node.get("oneOf") if isinstance(node, Mapping) else None
            if not isinstance(variants, list):
                raise RuntimeError(f"result definition {name!r} has no model algebra")
            for variant in variants:
                reference = variant.get("$ref") if isinstance(variant, Mapping) else None
                if not isinstance(reference, str):
                    raise RuntimeError(
                        f"result definition {name!r} contains a non-reference variant"
                    )
                collect(reference.rsplit("/", 1)[-1])

        for definition in definitions:
            collect(definition)
        return frozenset(selected)

    def _require_supported_handle_versions(self, value: object) -> None:
        if isinstance(value, Mapping):
            kind = value.get("kind")
            expected = self._handle_versions.get(str(kind))
            observed = value.get("schema_version")
            if expected is not None and observed != expected:
                raise InterfaceVersionError(
                    f"{kind} schema version {observed!r} is unsupported; "
                    f"expected {expected}"
                )
            for item in value.values():
                self._require_supported_handle_versions(item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                self._require_supported_handle_versions(item)

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


def _contracts(root: Path) -> CompiledContracts:
    schema = json.loads((root / INTERFACE_SCHEMA).read_text(encoding="utf-8"))
    with (root / INTERFACE_CONTRACT).open("rb") as source:
        interface = tomllib.load(source)
    return compile_contracts(schema, interface)
