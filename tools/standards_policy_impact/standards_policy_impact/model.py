from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from tools.graph_engine.graph_engine import GraphContribution
from tools.standards_applicability.standards_applicability import (
    ApplicabilityProgram,
    FactSchema,
)


def freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): freeze(item) for key, item in sorted(value.items())}
        )
    if isinstance(value, (list, tuple)):
        return tuple(freeze(item) for item in value)
    return value


def thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class RelationshipKind:
    id: str
    groups: tuple[str, ...]
    propagation: str
    traversable: bool
    evidence_required: bool


@dataclass(frozen=True, slots=True)
class PolicyImpactSemantics:
    edge_id: str
    source: str
    consumer: str
    relation: str
    applicability_program: ApplicabilityProgram
    source_scope: Mapping[str, object] | None
    consumer_scope: Mapping[str, object] | None
    propagation: str
    evidence_owner: str
    rationale: str
    declaration_source: str
    dependency_fingerprint: str

    def __post_init__(self) -> None:
        if self.source_scope is not None:
            object.__setattr__(self, "source_scope", freeze(self.source_scope))
        if self.consumer_scope is not None:
            object.__setattr__(self, "consumer_scope", freeze(self.consumer_scope))


@dataclass(frozen=True, slots=True)
class CompiledPolicyImpactSet:
    graph: GraphContribution
    semantics: Mapping[str, PolicyImpactSemantics]
    fact_schema: FactSchema
    node_catalog: str
    declaration_sources: tuple[str, ...]
    input_sources: tuple[str, ...]
    declaration_digest: str
    provider_contract_digest: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "semantics",
            MappingProxyType(dict(sorted(self.semantics.items()))),
        )

    def semantics_for(self, edge_id: str) -> PolicyImpactSemantics:
        return self.semantics[edge_id]


@dataclass(frozen=True, slots=True)
class PolicyImpactSource:
    compiled: CompiledPolicyImpactSet
    id: str = "standards.policy-impact"

    def load(self) -> GraphContribution:
        return self.compiled.graph
