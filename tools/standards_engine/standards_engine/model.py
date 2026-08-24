from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from tools.standards_analysis.standards_analysis import (
    AnalysisState,
    ChangeDescriptor,
    SemanticProposal,
)


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
class RouteRequest:
    facts: Mapping[str, object]
    kind: str = "route"


@dataclass(frozen=True, slots=True)
class RelatedRequest:
    target: str
    groups: tuple[str, ...]
    direction: str
    transitive: bool = False
    kind: str = "related"


QueryRequest = RouteRequest | ReadRequest | RelatedRequest


@dataclass(frozen=True, slots=True)
class QueryCall:
    snapshot: Mapping[str, object]
    request: QueryRequest


@dataclass(frozen=True, slots=True)
class InspectCall:
    handle: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class AnalysisRequest:
    base_snapshot: Mapping[str, object]
    proposed_snapshot: Mapping[str, object]
    changes: tuple[ChangeDescriptor, ...]
    semantic_proposals: tuple[SemanticProposal, ...]
    prior_analysis: Mapping[str, object] | None = None
    contract_version: int = 2
    kind: str = "analysis-request"

    def __post_init__(self) -> None:
        object.__setattr__(self, "base_snapshot", _freeze(self.base_snapshot))
        object.__setattr__(
            self,
            "proposed_snapshot",
            _freeze(self.proposed_snapshot),
        )
        if self.prior_analysis is not None:
            object.__setattr__(
                self,
                "prior_analysis",
                _freeze(self.prior_analysis),
            )


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


class RouteResult(ContractResult):
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


QueryResult = RouteResult | ReadResult | RelatedResult | RejectedResult
InspectionResult = (
    AnalysisState
    | SnapshotInspectionResult
    | PolicyInspectionResult
    | RelationshipInspectionResult
    | NavigationInspectionResult
    | RejectedResult
)
