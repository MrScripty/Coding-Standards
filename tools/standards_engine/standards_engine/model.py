from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class ReadRequest:
    target: str
    kind: str = "read"


@dataclass(frozen=True, slots=True)
class RelatedRequest:
    target: str
    groups: tuple[str, ...]
    direction: str
    transitive: bool = False
    kind: str = "related"


QueryRequest = ReadRequest | RelatedRequest


@dataclass(frozen=True, slots=True)
class QueryCall:
    snapshot: Mapping[str, object]
    request: QueryRequest


@dataclass(frozen=True, slots=True)
class InspectCall:
    handle: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class ContractResult:
    _value: Mapping[str, object]

    @classmethod
    def from_value(cls, value: dict[str, object]):
        return cls(_freeze(value))

    @property
    def kind(self) -> str:
        return str(self._value["kind"])

    def as_contract(self) -> dict[str, object]:
        return _thaw(self._value)


class ReadResult(ContractResult):
    pass


class RelatedResult(ContractResult):
    pass


class RejectedResult(ContractResult):
    pass


class SnapshotInspectionResult(ContractResult):
    pass


class PolicyInspectionResult(ContractResult):
    pass


class RelationshipInspectionResult(ContractResult):
    pass


class NavigationInspectionResult(ContractResult):
    pass


QueryResult = ReadResult | RelatedResult | RejectedResult
InspectionResult = (
    SnapshotInspectionResult
    | PolicyInspectionResult
    | RelationshipInspectionResult
    | NavigationInspectionResult
    | RejectedResult
)
