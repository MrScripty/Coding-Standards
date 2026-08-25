from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

from tools.standards_analysis.standards_analysis import (
    AuthorizationReference,
    FactObservationProvider,
)
from tools.standards_engine.contracts.validate_contracts import ContractError, validate

from ._generated_contract import RESULT_KIND_TO_DEFINITION, decode_contract
from .engine import AnalysisStateStore, StandardsEngine
from .model import (
    InspectCall,
    PrepareCall,
    QueryCall,
    ResolveCall,
)


INTERFACE_SCHEMA = "tools/standards_engine/contracts/a1-contract.schema.json"


class InterfaceVersionError(ValueError):
    pass


class AgentToolFacade:
    """Validated structured transport over the native Standards Engine API."""

    def __init__(self, engine: StandardsEngine, schema: Mapping[str, object]) -> None:
        self._engine = engine
        self._schema = schema
        self._handle_versions = self._derive_handle_versions(schema)

    @classmethod
    def open_repository(cls, root: Path) -> AgentToolFacade:
        repo_root = root.resolve()
        schema = json.loads((repo_root / INTERFACE_SCHEMA).read_text(encoding="utf-8"))
        return cls(StandardsEngine.open_repository(repo_root), schema)

    @classmethod
    def open_analysis(
        cls,
        base_root: Path,
        proposed_root: Path,
        *,
        authorizations: tuple[AuthorizationReference, ...] = (),
        analysis_store: AnalysisStateStore | None = None,
        fact_providers: Iterable[FactObservationProvider] = (),
    ) -> AgentToolFacade:
        repo_root = proposed_root.resolve()
        schema = json.loads((repo_root / INTERFACE_SCHEMA).read_text(encoding="utf-8"))
        return cls(
            StandardsEngine.open_analysis(
                base_root,
                proposed_root,
                authorizations=authorizations,
                analysis_store=analysis_store,
                fact_providers=fact_providers,
            ),
            schema,
        )

    @property
    def snapshot(self) -> Mapping[str, object]:
        return self._engine.snapshot

    @property
    def snapshots(self) -> tuple[Mapping[str, object], ...]:
        return self._engine.snapshots

    def query(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("QueryCall", value)
            call = decode_contract("QueryCall", value)
            if not isinstance(call, QueryCall):
                raise RuntimeError("generated QueryCall decoder returned the wrong type")
        except InterfaceVersionError as error:
            return self._rejected("INTERFACE.UNSUPPORTED_VERSION", "unsupported", str(error))
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))
        result = self._engine.query(call)
        output = result.as_contract()
        self._validate_result(output)
        return output

    def prepare(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("PrepareCall", value)
            call = decode_contract("PrepareCall", value)
            if not isinstance(call, PrepareCall):
                raise RuntimeError("generated PrepareCall decoder returned the wrong type")
        except InterfaceVersionError as error:
            return self._rejected("INTERFACE.UNSUPPORTED_VERSION", "unsupported", str(error))
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))
        result = self._engine.prepare(call.request)
        output = result.as_contract()
        self._validate_result(output)
        return output

    def resolve(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("ResolveCall", value)
            call = decode_contract("ResolveCall", value)
            if not isinstance(call, ResolveCall):
                raise RuntimeError("generated ResolveCall decoder returned the wrong type")
        except InterfaceVersionError as error:
            return self._rejected("INTERFACE.UNSUPPORTED_VERSION", "unsupported", str(error))
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))
        result = self._engine.resolve(call.analysis, call.submission)
        output = result.as_contract()
        self._validate_result(output)
        return output

    def inspect(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("InspectCall", value)
            call = decode_contract("InspectCall", value)
            if not isinstance(call, InspectCall):
                raise RuntimeError("generated InspectCall decoder returned the wrong type")
        except InterfaceVersionError as error:
            return self._rejected("INTERFACE.UNSUPPORTED_VERSION", "unsupported", str(error))
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))
        result = self._engine.inspect(call)
        output = result.as_contract()
        self._validate_result(output)
        return output

    def _validate(self, definition: str, value: object) -> None:
        self._require_supported_handle_versions(value)
        validate(
            self._schema,
            self._schema["$defs"][definition],
            value,
            "$arguments",
        )

    @staticmethod
    def _derive_handle_versions(schema: Mapping[str, object]) -> dict[str, int]:
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

    def _validate_result(self, value: dict[str, object]) -> None:
        definition = RESULT_KIND_TO_DEFINITION[str(value["kind"])]
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
