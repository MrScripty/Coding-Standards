from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from tools.graph_engine.graph_engine import (
    EdgeRegistry,
    GraphContribution,
    load_graph_contribution,
    project_graph_contribution,
)
from tools.standards_authority.standards_authority import (
    AuthorityReference,
    CodecContext,
    CodecSet,
    invalid,
)
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
    hash_identity,
)
from tools.standards_metadata.standards_metadata import CanonicalStandardsCorpus
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
    PolicyImpactSource,
)

from .metadata import metadata_dependency_source
from .policy_units import PolicyUnitGraphSource


@dataclass(frozen=True, slots=True)
class GraphSourceRecord:
    id: str
    contribution: GraphContribution

    def __post_init__(self) -> None:
        if type(self.id) is not str or not self.id:
            raise invalid("STANDARDS_GRAPH.INVALID_SOURCE", "source ID must be nonempty")


@dataclass(frozen=True, slots=True, init=False)
class StandardsGraphAuthority:
    metadata: AuthorityReference
    policy_impact: AuthorityReference
    sources: tuple[GraphSourceRecord, ...]

    def __init__(
        self,
        metadata: AuthorityReference,
        policy_impact: AuthorityReference,
        sources: Iterable[GraphSourceRecord],
    ) -> None:
        _require_kind(metadata, "canonical-standards-corpus")
        _require_kind(policy_impact, "compiled-policy-impact")
        selected = tuple(sorted(sources, key=lambda item: item.id))
        ids = tuple(item.id for item in selected)
        if not selected or len(set(ids)) != len(ids):
            raise invalid(
                "STANDARDS_GRAPH.SOURCE_CLOSURE",
                "graph sources must be nonempty and uniquely identified",
            )
        object.__setattr__(self, "metadata", metadata)
        object.__setattr__(self, "policy_impact", policy_impact)
        object.__setattr__(self, "sources", selected)

    def registry(self) -> EdgeRegistry:
        artifacts = {
            artifact
            for source in self.sources
            for node in source.contribution.nodes
            for artifact in (node.id, *node.aliases)
            if "/" in artifact
        }
        return EdgeRegistry(
            Path("/"),
            tuple(_StoredSource(item) for item in self.sources),
            logical_artifacts=artifacts,
        )


@dataclass(frozen=True, slots=True)
class _StoredSource:
    record: GraphSourceRecord

    @property
    def id(self) -> str:
        return self.record.id

    def load(self) -> GraphContribution:
        return self.record.contribution


class StandardsGraphCodec:
    object_kind = "standards-graph"
    payload_contract = "standards-graph.v1"
    allowed_dependency_kinds = frozenset(
        {"canonical-standards-corpus", "compiled-policy-impact"}
    )

    def encode(self, value: StandardsGraphAuthority) -> IdentityValue:
        return _authority_value(value)

    def decode(
        self, payload: IdentityValue, context: CodecContext
    ) -> StandardsGraphAuthority:
        members = _members(
            payload, {"metadata", "policy_impact", "sources"}, "standards graph"
        )
        metadata = _decode_reference(members["metadata"])
        policy_impact = _decode_reference(members["policy_impact"])
        context.resolve(metadata)
        context.resolve(policy_impact)
        sources = tuple(
            _decode_source(item) for item in _array(members["sources"], "sources")
        )
        result = StandardsGraphAuthority(metadata, policy_impact, sources)
        result.registry()
        return result

    def semantic_id(
        self, value: StandardsGraphAuthority, context: CodecContext
    ) -> str:
        context.resolve(value.metadata)
        context.resolve(value.policy_impact)
        value.registry()
        return hash_identity(
            "coding-standards:standards-graph:v1",
            "standards-graph",
            _authority_value(value),
        )

    def direct_dependencies(
        self, value: StandardsGraphAuthority
    ) -> tuple[AuthorityReference, ...]:
        return tuple(sorted((value.metadata, value.policy_impact)))


def compile_standards_graph_authority(
    metadata: AuthorityReference,
    policy_impact: AuthorityReference,
    corpus: CanonicalStandardsCorpus,
    compiled: CompiledPolicyImpactSet,
) -> StandardsGraphAuthority:
    sources = (
        metadata_dependency_source(corpus.modules),
        PolicyUnitGraphSource(corpus.policy_unit_corpus),
        PolicyImpactSource(compiled),
    )
    return StandardsGraphAuthority(
        metadata,
        policy_impact,
        (GraphSourceRecord(source.id, source.load()) for source in sources),
    )


def _authority_value(value: StandardsGraphAuthority) -> IdentityObject:
    return IdentityObject(
        (
            ("metadata", _reference_value(value.metadata)),
            ("policy_impact", _reference_value(value.policy_impact)),
            ("sources", IdentityArray(_source_value(item) for item in value.sources)),
        )
    )


def _source_value(value: GraphSourceRecord) -> IdentityObject:
    return IdentityObject(
        (
            ("id", value.id),
            ("contribution", _identity(project_graph_contribution(value.contribution))),
        )
    )


def _decode_source(value: IdentityValue) -> GraphSourceRecord:
    members = _members(value, {"id", "contribution"}, "graph source")
    contribution = _wire(members["contribution"])
    if not isinstance(contribution, dict):
        raise invalid(
            "STANDARDS_GRAPH.INVALID_PAYLOAD", "contribution must be an object"
        )
    return GraphSourceRecord(
        _string(members["id"], "id"), load_graph_contribution(contribution)
    )


def _reference_value(value: AuthorityReference) -> IdentityObject:
    return IdentityObject(
        (("object_kind", value.object_kind), ("semantic_id", value.semantic_id))
    )


def _decode_reference(value: IdentityValue) -> AuthorityReference:
    members = _members(value, {"object_kind", "semantic_id"}, "reference")
    return AuthorityReference(
        _string(members["object_kind"], "object_kind"),
        _string(members["semantic_id"], "semantic_id"),
    )


def _identity(value: object) -> IdentityValue:
    value_type = type(value)
    if value is None or value_type in {bool, int, str}:
        return value  # type: ignore[return-value]
    if value_type is list or value_type is tuple:
        return IdentityArray(_identity(item) for item in value)
    if isinstance(value, dict):
        if any(type(key) is not str for key in value):
            raise invalid(
                "STANDARDS_GRAPH.INVALID_VALUE", "mapping keys must be strings"
            )
        return IdentityObject(
            (key, _identity(value[key])) for key in sorted(value)
        )
    raise invalid("STANDARDS_GRAPH.INVALID_VALUE", repr(value_type))


def _wire(value: IdentityValue) -> object:
    if type(value) is IdentityArray:
        return [_wire(item) for item in value.values]
    if type(value) is IdentityObject:
        return {key: _wire(item) for key, item in value.members}
    return value


def _members(
    value: IdentityValue, expected: set[str], description: str
) -> dict[str, IdentityValue]:
    if type(value) is not IdentityObject:
        raise invalid(
            "STANDARDS_GRAPH.INVALID_PAYLOAD", f"{description} must be an object"
        )
    members = dict(value.members)
    if set(members) != expected:
        raise invalid(
            "STANDARDS_GRAPH.INVALID_PAYLOAD_FIELDS",
            f"{description} fields differ from the payload contract",
        )
    return members


def _array(value: IdentityValue, description: str) -> tuple[IdentityValue, ...]:
    if type(value) is not IdentityArray:
        raise invalid(
            "STANDARDS_GRAPH.INVALID_PAYLOAD", f"{description} must be an array"
        )
    return value.values


def _string(value: IdentityValue, field: str) -> str:
    if type(value) is not str or not value:
        raise invalid(
            "STANDARDS_GRAPH.INVALID_PAYLOAD", f"{field} must be a nonempty string"
        )
    return value


def _require_kind(reference: AuthorityReference, expected: str) -> None:
    if reference.object_kind != expected:
        raise invalid(
            "STANDARDS_GRAPH.INVALID_DEPENDENCY_KIND",
            f"expected {expected!r}, observed {reference.object_kind!r}",
        )


STANDARDS_GRAPH_CODEC = StandardsGraphCodec()
STANDARDS_GRAPH_CODECS = CodecSet("standards-graph", (STANDARDS_GRAPH_CODEC,))

__all__ = (
    "STANDARDS_GRAPH_CODEC",
    "STANDARDS_GRAPH_CODECS",
    "GraphSourceRecord",
    "StandardsGraphAuthority",
    "StandardsGraphCodec",
    "compile_standards_graph_authority",
)
