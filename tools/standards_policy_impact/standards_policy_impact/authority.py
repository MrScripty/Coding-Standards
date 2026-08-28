from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.graph_engine.graph_engine import (
    load_graph_contribution,
    project_graph_contribution,
)
from tools.standards_applicability.standards_applicability import compile_fact_schema
from tools.standards_authority.standards_authority import (
    AuthorityBoundValue,
    AuthorityReference,
    CodecContext,
    CodecSet,
    ExecutionAuthorityRoot,
    invalid,
)
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
    hash_identity,
)

from .model import (
    CompiledPolicyImpactSet,
    PolicyImpactArtifact,
    PolicyImpactSemantics,
    RelationshipKind,
)


@dataclass(frozen=True, slots=True)
class CompiledPolicyImpactAuthority:
    content: AuthorityReference
    metadata: AuthorityReference
    compiled: CompiledPolicyImpactSet

    def __post_init__(self) -> None:
        _require_kind(self.content, "content-snapshot")
        _require_kind(self.metadata, "canonical-standards-corpus")

    def authority_bound(
        self, reference: AuthorityReference, side: str
    ) -> AuthorityBoundValue[object]:
        if reference.object_kind != "compiled-policy-impact":
            raise invalid(
                "POLICY_IMPACT.INVALID_AUTHORITY_BINDING",
                "policy-impact binding requires its compiled authority",
            )
        return AuthorityBoundValue(
            self, (ExecutionAuthorityRoot(side, "policy-impact", reference),)
        )


class CompiledPolicyImpactCodec:
    object_kind = "compiled-policy-impact"
    payload_contract = "compiled-policy-impact.v1"
    allowed_dependency_kinds = frozenset(
        {"content-snapshot", "canonical-standards-corpus"}
    )

    def encode(self, value: CompiledPolicyImpactAuthority) -> IdentityValue:
        return _authority_value(value)

    def decode(
        self, payload: IdentityValue, context: CodecContext
    ) -> CompiledPolicyImpactAuthority:
        members = _members(
            payload,
            {
                "content",
                "metadata",
                "graph",
                "semantics",
                "artifacts",
                "relationship_kinds",
                "fact_schema",
                "node_catalog",
                "declaration_sources",
                "input_sources",
                "declaration_digest",
                "catalog_digest",
                "authoring_contract_digest",
                "provider_contract_digest",
                "relationship_kind_contract_version",
            },
            "compiled policy impact",
        )
        content = _decode_reference(members["content"])
        metadata = _decode_reference(members["metadata"])
        context.resolve(content)
        context.resolve(metadata)
        fact_schema = compile_fact_schema(_wire(members["fact_schema"]))
        graph = load_graph_contribution(_wire(members["graph"]))
        semantics = {
            item.edge_id: item
            for item in (
                _decode_semantics(raw, fact_schema)
                for raw in _array(members["semantics"], "semantics")
            )
        }
        artifacts = {
            item.id: item
            for item in (
                _decode_artifact(raw)
                for raw in _array(members["artifacts"], "artifacts")
            )
        }
        relationship_kinds = {
            item.id: item
            for item in (
                _decode_relationship_kind(raw)
                for raw in _array(
                    members["relationship_kinds"], "relationship kinds"
                )
            )
        }
        compiled = CompiledPolicyImpactSet(
            graph,
            MappingProxyType(semantics),
            MappingProxyType(artifacts),
            MappingProxyType(relationship_kinds),
            fact_schema,
            _string(members["node_catalog"], "node_catalog"),
            tuple(_strings(members["declaration_sources"], "declaration_sources")),
            tuple(_strings(members["input_sources"], "input_sources")),
            _string(members["declaration_digest"], "declaration_digest"),
            _string(members["catalog_digest"], "catalog_digest"),
            _string(
                members["authoring_contract_digest"], "authoring_contract_digest"
            ),
            _string(
                members["provider_contract_digest"], "provider_contract_digest"
            ),
            _positive_integer(
                members["relationship_kind_contract_version"],
                "relationship_kind_contract_version",
            ),
        )
        return CompiledPolicyImpactAuthority(content, metadata, compiled)

    def semantic_id(
        self, value: CompiledPolicyImpactAuthority, context: CodecContext
    ) -> str:
        context.resolve(value.content)
        context.resolve(value.metadata)
        return hash_identity(
            "coding-standards:compiled-policy-impact:v1",
            "compiled-policy-impact",
            _authority_value(value),
        )

    def direct_dependencies(
        self, value: CompiledPolicyImpactAuthority
    ) -> tuple[AuthorityReference, ...]:
        return tuple(sorted((value.content, value.metadata)))


def _authority_value(value: CompiledPolicyImpactAuthority) -> IdentityObject:
    compiled = value.compiled
    return IdentityObject(
        (
            ("content", _reference_value(value.content)),
            ("metadata", _reference_value(value.metadata)),
            ("graph", _identity(project_graph_contribution(compiled.graph))),
            (
                "semantics",
                IdentityArray(
                    _semantics_value(compiled.semantics[key])
                    for key in sorted(compiled.semantics)
                ),
            ),
            (
                "artifacts",
                IdentityArray(
                    _artifact_value(compiled.artifacts[key])
                    for key in sorted(compiled.artifacts)
                ),
            ),
            (
                "relationship_kinds",
                IdentityArray(
                    _relationship_kind_value(compiled.relationship_kinds[key])
                    for key in sorted(compiled.relationship_kinds)
                ),
            ),
            ("fact_schema", _fact_schema_value(compiled.fact_schema)),
            ("node_catalog", compiled.node_catalog),
            ("declaration_sources", IdentityArray(compiled.declaration_sources)),
            ("input_sources", IdentityArray(compiled.input_sources)),
            ("declaration_digest", compiled.declaration_digest),
            ("catalog_digest", compiled.catalog_digest),
            ("authoring_contract_digest", compiled.authoring_contract_digest),
            ("provider_contract_digest", compiled.provider_contract_digest),
            (
                "relationship_kind_contract_version",
                compiled.relationship_kind_contract_version,
            ),
        )
    )


def _fact_schema_value(value: object) -> IdentityValue:
    return _identity(
        {
            "kind": "applicability-fact-schema",
            "id": value.id,
            "version": value.version,
            "facts": [
                {
                    **item.semantic_projection(),
                    "aliases": list(item.aliases),
                    "prompt": item.prompt,
                }
                for item in value.definitions
            ],
        }
    )


def _semantics_value(value: PolicyImpactSemantics) -> IdentityObject:
    return IdentityObject(
        (
            ("edge_id", value.edge_id),
            ("source", value.source),
            ("consumer", value.consumer),
            ("relation", value.relation),
            ("applicability", _identity(value.applicability_program.as_projection())),
            ("source_scope", _identity(_thaw(value.source_scope))),
            ("consumer_scope", _identity(_thaw(value.consumer_scope))),
            ("propagation", value.propagation),
            ("evidence_owner", value.evidence_owner),
            ("rationale", value.rationale),
            ("declaration_source", value.declaration_source),
            ("dependency_fingerprint", value.dependency_fingerprint),
        )
    )


def _decode_semantics(value: IdentityValue, fact_schema: object) -> PolicyImpactSemantics:
    members = _members(
        value,
        {
            "edge_id",
            "source",
            "consumer",
            "relation",
            "applicability",
            "source_scope",
            "consumer_scope",
            "propagation",
            "evidence_owner",
            "rationale",
            "declaration_source",
            "dependency_fingerprint",
        },
        "policy-impact semantics",
    )
    projection = _wire(members["applicability"])
    program = fact_schema.compile(
        projection["normalized_expression"],
        language_version=projection["language_version"],
    )
    if program.as_projection() != projection:
        raise invalid(
            "POLICY_IMPACT.PROGRAM_CONTRADICTION",
            "stored applicability program does not reproduce",
        )
    source_scope = _wire(members["source_scope"])
    consumer_scope = _wire(members["consumer_scope"])
    return PolicyImpactSemantics(
        _string(members["edge_id"], "edge_id"),
        _string(members["source"], "source"),
        _string(members["consumer"], "consumer"),
        _string(members["relation"], "relation"),
        program,
        source_scope,
        consumer_scope,
        _string(members["propagation"], "propagation"),
        _string(members["evidence_owner"], "evidence_owner"),
        _string(members["rationale"], "rationale", allow_empty=True),
        _string(members["declaration_source"], "declaration_source"),
        _string(members["dependency_fingerprint"], "dependency_fingerprint"),
    )


def _artifact_value(value: PolicyImpactArtifact) -> IdentityObject:
    return IdentityObject(
        (
            ("id", value.id),
            ("aliases", IdentityArray(value.aliases)),
            ("repository_path", value.repository_path),
            ("artifact_kind", value.artifact_kind),
            ("authority", value.authority),
            ("suite_id", value.suite_id),
            ("coverage_fingerprint", value.coverage_fingerprint),
            ("source_path", value.source_path),
        )
    )


def _decode_artifact(value: IdentityValue) -> PolicyImpactArtifact:
    members = _members(
        value,
        {
            "id",
            "aliases",
            "repository_path",
            "artifact_kind",
            "authority",
            "suite_id",
            "coverage_fingerprint",
            "source_path",
        },
        "policy-impact artifact",
    )
    suite_id = members["suite_id"]
    if suite_id is not None and type(suite_id) is not str:
        raise invalid("POLICY_IMPACT.INVALID_PAYLOAD", "suite_id must be string or null")
    return PolicyImpactArtifact(
        _string(members["id"], "id"),
        tuple(_strings(members["aliases"], "aliases")),
        _string(members["repository_path"], "repository_path"),
        _string(members["artifact_kind"], "artifact_kind"),
        _string(members["authority"], "authority"),
        suite_id,
        _string(members["coverage_fingerprint"], "coverage_fingerprint"),
        _string(members["source_path"], "source_path"),
    )


def _relationship_kind_value(value: RelationshipKind) -> IdentityObject:
    return IdentityObject(
        (
            ("id", value.id),
            ("target_class", value.target_class),
            ("groups", IdentityArray(value.groups)),
            ("propagation", value.propagation),
            ("traversable", value.traversable),
        )
    )


def _decode_relationship_kind(value: IdentityValue) -> RelationshipKind:
    members = _members(
        value,
        {"id", "target_class", "groups", "propagation", "traversable"},
        "relationship kind",
    )
    traversable = members["traversable"]
    if type(traversable) is not bool:
        raise invalid("POLICY_IMPACT.INVALID_PAYLOAD", "traversable must be Boolean")
    return RelationshipKind(
        _string(members["id"], "id"),
        _string(members["target_class"], "target_class"),
        tuple(_strings(members["groups"], "groups")),
        _string(members["propagation"], "propagation"),
        traversable,
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
    if isinstance(value, Mapping):
        if any(type(key) is not str for key in value):
            raise invalid("POLICY_IMPACT.INVALID_VALUE", "mapping keys must be strings")
        return IdentityObject(
            (key, _identity(value[key])) for key in sorted(value)
        )
    raise invalid("POLICY_IMPACT.INVALID_VALUE", repr(value_type))


def _wire(value: IdentityValue) -> object:
    if type(value) is IdentityArray:
        return [_wire(item) for item in value.values]
    if type(value) is IdentityObject:
        return {key: _wire(item) for key, item in value.members}
    return value


def _thaw(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _members(
    value: IdentityValue, expected: set[str], description: str
) -> dict[str, IdentityValue]:
    if type(value) is not IdentityObject:
        raise invalid("POLICY_IMPACT.INVALID_PAYLOAD", f"{description} must be an object")
    members = dict(value.members)
    if set(members) != expected:
        raise invalid(
            "POLICY_IMPACT.INVALID_PAYLOAD_FIELDS",
            f"{description} fields differ from the payload contract",
        )
    return members


def _array(value: IdentityValue, description: str) -> tuple[IdentityValue, ...]:
    if type(value) is not IdentityArray:
        raise invalid("POLICY_IMPACT.INVALID_PAYLOAD", f"{description} must be an array")
    return value.values


def _strings(value: IdentityValue, description: str) -> tuple[str, ...]:
    selected = _array(value, description)
    if any(type(item) is not str for item in selected):
        raise invalid("POLICY_IMPACT.INVALID_PAYLOAD", f"{description} must contain strings")
    return selected  # type: ignore[return-value]


def _string(value: IdentityValue, field: str, *, allow_empty: bool = False) -> str:
    if type(value) is not str or (not allow_empty and not value):
        raise invalid("POLICY_IMPACT.INVALID_PAYLOAD", f"{field} must be a string")
    return value


def _positive_integer(value: IdentityValue, field: str) -> int:
    if type(value) is not int or value < 1:
        raise invalid("POLICY_IMPACT.INVALID_PAYLOAD", f"{field} must be positive integer")
    return value


def _require_kind(reference: AuthorityReference, expected: str) -> None:
    if reference.object_kind != expected:
        raise invalid(
            "POLICY_IMPACT.INVALID_DEPENDENCY_KIND",
            f"expected {expected!r}, observed {reference.object_kind!r}",
        )


COMPILED_POLICY_IMPACT_CODEC = CompiledPolicyImpactCodec()
POLICY_IMPACT_CODECS = CodecSet(
    "standards-policy-impact", (COMPILED_POLICY_IMPACT_CODEC,)
)

__all__ = (
    "COMPILED_POLICY_IMPACT_CODEC",
    "POLICY_IMPACT_CODECS",
    "CompiledPolicyImpactAuthority",
    "CompiledPolicyImpactCodec",
)
