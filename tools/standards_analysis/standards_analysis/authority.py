from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar, Mapping

from tools.standards_applicability.standards_applicability import (
    FactSchema,
    compile_fact_schema,
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

from .routing import RouteRule, RouterProjection
from .coverage import CoverageHorizon, CoverageHorizonMember


DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class RoutingProjectionAuthority:
    content: AuthorityReference
    metadata: AuthorityReference
    projection: RouterProjection

    def __post_init__(self) -> None:
        _require_kind(self.content, "content-snapshot")
        _require_kind(self.metadata, "canonical-standards-corpus")


class RoutingProjectionCodec:
    object_kind = "routing-projection"
    payload_contract = "routing-projection.v1"
    allowed_dependency_kinds = frozenset(
        {"content-snapshot", "canonical-standards-corpus"}
    )

    def encode(self, value: RoutingProjectionAuthority) -> IdentityValue:
        return _routing_value(value)

    def decode(
        self, payload: IdentityValue, context: CodecContext
    ) -> RoutingProjectionAuthority:
        members = _members(
            payload,
            {
                "content",
                "metadata",
                "id",
                "owner",
                "source",
                "base_modules",
                "fact_schema",
                "rules",
            },
            "routing projection",
        )
        content = _decode_reference(members["content"])
        metadata = _decode_reference(members["metadata"])
        context.resolve(content)
        context.resolve(metadata)
        fact_declaration = _wire(members["fact_schema"])
        if not isinstance(fact_declaration, dict):
            raise invalid(
                "ANALYSIS.INVALID_ROUTING_PAYLOAD", "fact schema must be an object"
            )
        fact_schema = compile_fact_schema(fact_declaration)
        rules = tuple(
            _decode_route_rule(item, fact_schema)
            for item in _array(members["rules"], "route rules")
        )
        projection = RouterProjection(
            _string(members["id"], "id"),
            _string(members["owner"], "owner"),
            _string(members["source"], "source"),
            tuple(_strings(members["base_modules"], "base_modules")),
            fact_schema.definitions,
            rules,
            fact_schema,
        )
        return RoutingProjectionAuthority(content, metadata, projection)

    def semantic_id(
        self, value: RoutingProjectionAuthority, context: CodecContext
    ) -> str:
        context.resolve(value.content)
        context.resolve(value.metadata)
        return hash_identity(
            "coding-standards:routing-projection:v1",
            "routing-projection",
            _routing_value(value),
        )

    def direct_dependencies(
        self, value: RoutingProjectionAuthority
    ) -> tuple[AuthorityReference, ...]:
        return tuple(sorted((value.content, value.metadata)))


@dataclass(frozen=True, slots=True)
class CoverageHorizonAuthority:
    content: AuthorityReference
    metadata: AuthorityReference
    policy_impact: AuthorityReference
    graph: AuthorityReference
    horizon: CoverageHorizon

    def __post_init__(self) -> None:
        _require_kind(self.content, "content-snapshot")
        _require_kind(self.metadata, "canonical-standards-corpus")
        _require_kind(self.policy_impact, "compiled-policy-impact")
        _require_kind(self.graph, "standards-graph")


class CoverageHorizonCodec:
    object_kind = "coverage-horizon"
    payload_contract = "coverage-horizon.v1"
    allowed_dependency_kinds = frozenset(
        {
            "content-snapshot",
            "canonical-standards-corpus",
            "compiled-policy-impact",
            "standards-graph",
        }
    )

    def encode(self, value: CoverageHorizonAuthority) -> IdentityValue:
        return _coverage_horizon_value(value)

    def decode(
        self, payload: IdentityValue, context: CodecContext
    ) -> CoverageHorizonAuthority:
        members = _members(
            payload,
            {
                "content",
                "metadata",
                "policy_impact",
                "graph",
                "id",
                "provider",
                "version",
                "members",
                "digest",
                "input_sources",
            },
            "coverage horizon",
        )
        content = _decode_reference(members["content"])
        metadata = _decode_reference(members["metadata"])
        policy_impact = _decode_reference(members["policy_impact"])
        graph = _decode_reference(members["graph"])
        for reference in (content, metadata, policy_impact, graph):
            context.resolve(reference)
        horizon = CoverageHorizon(
            _string(members["id"], "id"),
            _string(members["provider"], "provider"),
            _positive_integer(members["version"], "version"),
            tuple(
                _decode_horizon_member(item)
                for item in _array(members["members"], "horizon members")
            ),
            _string(members["digest"], "digest"),
            tuple(_strings(members["input_sources"], "input_sources")),
        )
        result = CoverageHorizonAuthority(
            content, metadata, policy_impact, graph, horizon
        )
        if _coverage_horizon_value(result) != payload:
            raise invalid(
                "ANALYSIS.COVERAGE_HORIZON_CONTRADICTION",
                "coverage horizon does not reproduce its stored payload",
            )
        return result

    def semantic_id(
        self, value: CoverageHorizonAuthority, context: CodecContext
    ) -> str:
        for reference in (
            value.content,
            value.metadata,
            value.policy_impact,
            value.graph,
        ):
            context.resolve(reference)
        return hash_identity(
            "coding-standards:coverage-horizon:v1",
            "coverage-horizon",
            _coverage_horizon_value(value),
        )

    def direct_dependencies(
        self, value: CoverageHorizonAuthority
    ) -> tuple[AuthorityReference, ...]:
        return tuple(
            sorted((value.content, value.metadata, value.policy_impact, value.graph))
        )


def _routing_value(value: RoutingProjectionAuthority) -> IdentityObject:
    projection = value.projection
    return IdentityObject(
        (
            ("content", _reference_value(value.content)),
            ("metadata", _reference_value(value.metadata)),
            ("id", projection.id),
            ("owner", projection.owner),
            ("source", projection.source),
            ("base_modules", IdentityArray(projection.base_modules)),
            ("fact_schema", _identity(projection.fact_schema.as_declaration())),
            (
                "rules",
                IdentityArray(
                    IdentityObject(
                        (
                            ("id", item.id),
                            ("target", item.target),
                            ("program", _identity(item.program.as_projection())),
                        )
                    )
                    for item in projection.rules
                ),
            ),
        )
    )


def _coverage_horizon_value(value: CoverageHorizonAuthority) -> IdentityObject:
    horizon = value.horizon
    return IdentityObject(
        (
            ("content", _reference_value(value.content)),
            ("metadata", _reference_value(value.metadata)),
            ("policy_impact", _reference_value(value.policy_impact)),
            ("graph", _reference_value(value.graph)),
            ("id", horizon.id),
            ("provider", horizon.provider),
            ("version", horizon.version),
            (
                "members",
                IdentityArray(
                    IdentityObject(
                        (
                            ("id", item.id),
                            ("roles", IdentityArray(item.roles)),
                            ("fingerprint", item.fingerprint),
                        )
                    )
                    for item in horizon.members
                ),
            ),
            ("digest", horizon.digest),
            ("input_sources", IdentityArray(horizon.input_sources)),
        )
    )


def _decode_horizon_member(value: IdentityValue) -> CoverageHorizonMember:
    members = _members(value, {"id", "roles", "fingerprint"}, "horizon member")
    return CoverageHorizonMember(
        _string(members["id"], "id"),
        tuple(_strings(members["roles"], "roles")),
        _string(members["fingerprint"], "fingerprint"),
    )


def _decode_route_rule(value: IdentityValue, fact_schema: FactSchema) -> RouteRule:
    members = _members(value, {"id", "target", "program"}, "route rule")
    projected = _wire(members["program"])
    if not isinstance(projected, dict):
        raise invalid("ANALYSIS.INVALID_ROUTING_PAYLOAD", "program must be an object")
    program = fact_schema.compile(
        projected["normalized_expression"],
        language_version=projected["language_version"],
    )
    if program.as_projection() != projected:
        raise invalid(
            "ANALYSIS.ROUTING_PROGRAM_CONTRADICTION",
            "stored route program does not reproduce",
        )
    return RouteRule(
        _string(members["id"], "id"),
        _string(members["target"], "target"),
        program,
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
            raise invalid("ANALYSIS.INVALID_VALUE", "mapping keys must be strings")
        return IdentityObject(
            (key, _identity(value[key])) for key in sorted(value)
        )
    raise invalid("ANALYSIS.INVALID_VALUE", repr(value_type))


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
        raise invalid("ANALYSIS.INVALID_PAYLOAD", f"{description} must be an object")
    members = dict(value.members)
    if set(members) != expected:
        raise invalid(
            "ANALYSIS.INVALID_PAYLOAD_FIELDS",
            f"{description} fields differ from the payload contract",
        )
    return members


def _array(value: IdentityValue, description: str) -> tuple[IdentityValue, ...]:
    if type(value) is not IdentityArray:
        raise invalid("ANALYSIS.INVALID_PAYLOAD", f"{description} must be an array")
    return value.values


def _strings(value: IdentityValue, description: str) -> tuple[str, ...]:
    selected = _array(value, description)
    if any(type(item) is not str for item in selected):
        raise invalid("ANALYSIS.INVALID_PAYLOAD", f"{description} must contain strings")
    return selected  # type: ignore[return-value]


def _string(value: IdentityValue, field: str) -> str:
    if type(value) is not str or not value:
        raise invalid("ANALYSIS.INVALID_PAYLOAD", f"{field} must be nonempty string")
    return value


def _positive_integer(value: IdentityValue, field: str) -> int:
    if type(value) is not int or value < 1:
        raise invalid(
            "ANALYSIS.INVALID_PAYLOAD", f"{field} must be a positive exact integer"
        )
    return value


def _require_kind(reference: AuthorityReference, expected: str) -> None:
    if reference.object_kind != expected:
        raise invalid(
            "ANALYSIS.INVALID_DEPENDENCY_KIND",
            f"expected {expected!r}, observed {reference.object_kind!r}",
        )


def _projection(
    value: IdentityValue, expected: frozenset[str], description: str
) -> IdentityObject:
    if type(value) is not IdentityObject:
        raise invalid("ANALYSIS.INVALID_PROJECTION", f"{description} must be an object")
    if {key for key, _ in value.members} != expected:
        raise invalid(
            "ANALYSIS.INVALID_PROJECTION_FIELDS",
            f"{description} fields differ from the semantic contract",
        )
    return value


@dataclass(frozen=True, slots=True)
class AnalysisContextAuthority:
    metadata: AuthorityReference
    projection: IdentityObject

    FIELDS: ClassVar = frozenset({"subjects", "changes", "semantic_proposals"})

    def __post_init__(self) -> None:
        _require_kind(self.metadata, "canonical-standards-corpus")
        _projection(self.projection, self.FIELDS, "analysis context")


@dataclass(frozen=True, slots=True)
class FactRequirementAuthority:
    context: AuthorityReference
    policy_impact: AuthorityReference
    projection: IdentityObject

    FIELDS: ClassVar = frozenset(
        {
            "fact",
            "fact_semantic_revision",
            "fact_contract_digest",
            "value_contract",
            "answer_contract",
            "evidence_contract",
            "authorization_capability",
        }
    )

    def __post_init__(self) -> None:
        _require_kind(self.context, "analysis-context")
        _require_kind(self.policy_impact, "compiled-policy-impact")
        _projection(self.projection, self.FIELDS, "fact requirement")


@dataclass(frozen=True, slots=True)
class ProviderAuthority:
    provider_id: str
    semantic_revision: int
    input_contract: str
    evidence_contract: str
    inputs: tuple[AuthorityReference, ...]

    ALLOWED_INPUT_KINDS: ClassVar = frozenset(
        {
            "content-snapshot",
            "canonical-standards-corpus",
            "compiled-policy-impact",
            "standards-graph",
            "coverage-horizon",
            "analysis-context",
            "fact-requirement",
        }
    )

    def __post_init__(self) -> None:
        _string(self.provider_id, "provider_id")
        _positive_integer(self.semantic_revision, "semantic_revision")
        _string(self.input_contract, "input_contract")
        _string(self.evidence_contract, "evidence_contract")
        if self.inputs != tuple(sorted(set(self.inputs))):
            raise invalid(
                "ANALYSIS.INVALID_PROVIDER_INPUTS",
                "provider inputs must be sorted and unique",
            )
        if any(item.object_kind not in self.ALLOWED_INPUT_KINDS for item in self.inputs):
            raise invalid(
                "ANALYSIS.INVALID_PROVIDER_INPUT_KIND",
                "provider input kind is not admitted",
            )


@dataclass(frozen=True, slots=True, order=True)
class AuthorityEvidence:
    provider_contract: str
    provider_contract_version: str
    id: str
    digest: str

    def __post_init__(self) -> None:
        for field, value in (
            ("provider_contract", self.provider_contract),
            ("provider_contract_version", self.provider_contract_version),
            ("id", self.id),
            ("digest", self.digest),
        ):
            _string(value, field)
        if DIGEST_PATTERN.fullmatch(self.digest) is None:
            raise invalid(
                "ANALYSIS.INVALID_EVIDENCE_DIGEST",
                "evidence digest must be a lowercase SHA-256 digest",
            )


@dataclass(frozen=True, slots=True)
class AuthorizationGrant:
    issuer_id: str
    issuer_semantic_revision: int
    grant_id: str
    principal_id: str
    capability: str
    action: str
    subject_kind: str
    subject_id: str
    authorization_evidence: tuple[AuthorityEvidence, ...]
    revocation_authority_id: str
    revocation_authority_semantic_revision: int
    revocation_evidence: tuple[AuthorityEvidence, ...]

    ACTION_SUBJECTS: ClassVar = {
        "provide-fact": "fact-requirement",
        "consumer-disposition": "consumer-obligation",
        "impact-disposition": "impact-obligation",
        "coverage-attestation": "coverage-requirement",
    }

    def __post_init__(self) -> None:
        for field, value in (
            ("issuer_id", self.issuer_id),
            ("grant_id", self.grant_id),
            ("principal_id", self.principal_id),
            ("capability", self.capability),
            ("subject_id", self.subject_id),
            ("revocation_authority_id", self.revocation_authority_id),
        ):
            _string(value, field)
        _positive_integer(self.issuer_semantic_revision, "issuer_semantic_revision")
        _positive_integer(
            self.revocation_authority_semantic_revision,
            "revocation_authority_semantic_revision",
        )
        if self.ACTION_SUBJECTS.get(self.action) != self.subject_kind:
            raise invalid(
                "ANALYSIS.AUTHORIZATION_SUBJECT_MISMATCH",
                "authorization action and subject kind differ",
            )
        _evidence_set(self.authorization_evidence, "authorization_evidence")
        _evidence_set(self.revocation_evidence, "revocation_evidence")


@dataclass(frozen=True, slots=True)
class FactObservationAuthority:
    requirement: AuthorityReference
    authorization: AuthorityReference
    provider: AuthorityReference | None
    projection: IdentityObject

    FIELDS: ClassVar = frozenset({"value", "evidence"})

    def __post_init__(self) -> None:
        _require_kind(self.requirement, "fact-requirement")
        _require_kind(self.authorization, "authorization-grant")
        if self.provider is not None:
            _require_kind(self.provider, "provider-authority")
        _projection(self.projection, self.FIELDS, "fact observation")


@dataclass(frozen=True, slots=True)
class CoverageViewAuthority:
    metadata: AuthorityReference
    policy_impact: AuthorityReference
    graph: AuthorityReference
    horizon: AuthorityReference
    projection: IdentityObject

    FIELDS: ClassVar = frozenset(
        {
            "subject",
            "owner",
            "semantic_revision",
            "representation_digest",
            "structural_digest",
            "relationship_kinds",
            "relationship_fingerprints",
            "applicability_program_digests",
            "fact_schema_digest",
            "horizon",
        }
    )

    def __post_init__(self) -> None:
        _require_kind(self.metadata, "canonical-standards-corpus")
        _require_kind(self.policy_impact, "compiled-policy-impact")
        _require_kind(self.graph, "standards-graph")
        _require_kind(self.horizon, "coverage-horizon")
        _projection(self.projection, self.FIELDS, "coverage view")


@dataclass(frozen=True, slots=True)
class CoverageRequirementAuthority:
    coverage_view: AuthorityReference
    projection: IdentityObject

    FIELDS: ClassVar = frozenset(
        {
            "subject",
            "owner",
            "semantic_revision",
            "relationship_kinds",
            "horizon",
            "required_evidence_contract",
        }
    )

    def __post_init__(self) -> None:
        _require_kind(self.coverage_view, "coverage-view")
        _projection(self.projection, self.FIELDS, "coverage requirement")


@dataclass(frozen=True, slots=True)
class CoverageAttestationAuthority:
    requirement: AuthorityReference
    authorization: AuthorityReference
    projection: IdentityObject

    FIELDS: ClassVar = frozenset(
        {
            "conclusion",
            "evidence",
            "explicit_exclusions",
            "rationale",
            "auditor_provenance",
            "schema_version",
        }
    )

    def __post_init__(self) -> None:
        _require_kind(self.requirement, "coverage-requirement")
        _require_kind(self.authorization, "authorization-grant")
        _projection(self.projection, self.FIELDS, "coverage attestation")


@dataclass(frozen=True, slots=True)
class CoverageCertificateAuthority:
    coverage_view: AuthorityReference
    requirement: AuthorityReference
    attestation: AuthorityReference
    projection: IdentityObject

    FIELDS: ClassVar = frozenset(
        {
            "subject",
            "owner",
            "semantic_revision",
            "horizon_digest",
            "relationship_digest",
            "evidence_digests",
            "provenance",
            "fact_schema_digest",
        }
    )

    def __post_init__(self) -> None:
        _require_kind(self.coverage_view, "coverage-view")
        _require_kind(self.requirement, "coverage-requirement")
        _require_kind(self.attestation, "coverage-attestation")
        _projection(self.projection, self.FIELDS, "coverage certificate")


@dataclass(frozen=True, slots=True)
class AnalysisRootAuthority:
    closure: AuthorityReference
    context: AuthorityReference
    observations: tuple[AuthorityReference, ...]
    attestations: tuple[AuthorityReference, ...]
    projection: IdentityObject

    FIELDS: ClassVar = frozenset({"dispositions"})

    def __post_init__(self) -> None:
        _require_kind(self.closure, "execution-closure")
        _require_kind(self.context, "analysis-context")
        _reference_set(self.observations, "fact-observation", "observations")
        _reference_set(
            self.attestations, "coverage-attestation", "coverage attestations"
        )
        _projection(self.projection, self.FIELDS, "analysis root")


class _RecordCodec:
    object_kind: str
    payload_contract: str
    identity_domain: str
    identity_label: str
    allowed_dependency_kinds: frozenset[str]
    value_type: type

    def encode(self, value: object) -> IdentityValue:
        return self._value(value)

    def decode(self, payload: IdentityValue, context: CodecContext) -> object:
        value = self._decode(payload)
        for reference in self.direct_dependencies(value):
            context.resolve(reference)
        if self._value(value) != payload:
            raise invalid(
                "ANALYSIS.OWNER_CONTRADICTION",
                f"{self.object_kind} does not reproduce its stored payload",
            )
        return value

    def semantic_id(self, value: object, context: CodecContext) -> str:
        for reference in self.direct_dependencies(value):
            context.resolve(reference)
        return hash_identity(
            self.identity_domain, self.identity_label, self._value(value)
        )

    def direct_dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        if not isinstance(value, self.value_type):
            raise invalid(
                "ANALYSIS.INVALID_OWNER_VALUE",
                f"{self.object_kind} received {type(value)!r}",
            )
        return self._dependencies(value)

    def _value(self, value: object) -> IdentityObject:
        raise NotImplementedError

    def _decode(self, payload: IdentityValue) -> object:
        raise NotImplementedError

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        raise NotImplementedError


class AnalysisContextCodec(_RecordCodec):
    object_kind = "analysis-context"
    payload_contract = "analysis-context.v1"
    identity_domain = "coding-standards:analysis-context:v2"
    identity_label = "analysis-context"
    allowed_dependency_kinds = frozenset({"canonical-standards-corpus"})
    value_type = AnalysisContextAuthority

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, AnalysisContextAuthority)
        return _dependent_projection("metadata", value.metadata, value.projection)

    def _decode(self, payload: IdentityValue) -> AnalysisContextAuthority:
        dependency, projection = _decode_dependent_projection(
            payload, "metadata", "canonical-standards-corpus", AnalysisContextAuthority.FIELDS
        )
        return AnalysisContextAuthority(dependency, projection)

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, AnalysisContextAuthority)
        return (value.metadata,)


class FactRequirementCodec(_RecordCodec):
    object_kind = "fact-requirement"
    payload_contract = "fact-requirement.v1"
    identity_domain = "coding-standards:fact-requirement:v2"
    identity_label = "fact-requirement"
    allowed_dependency_kinds = frozenset(
        {"analysis-context", "compiled-policy-impact"}
    )
    value_type = FactRequirementAuthority

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, FactRequirementAuthority)
        return _references_projection(
            (("context", value.context), ("policy_impact", value.policy_impact)),
            value.projection,
        )

    def _decode(self, payload: IdentityValue) -> FactRequirementAuthority:
        references, projection = _decode_references_projection(
            payload,
            (("context", "analysis-context"), ("policy_impact", "compiled-policy-impact")),
            FactRequirementAuthority.FIELDS,
        )
        return FactRequirementAuthority(references[0], references[1], projection)

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, FactRequirementAuthority)
        return tuple(sorted((value.context, value.policy_impact)))


class ProviderAuthorityCodec(_RecordCodec):
    object_kind = "provider-authority"
    payload_contract = "provider-authority.v1"
    identity_domain = "coding-standards:provider-authority:v1"
    identity_label = "provider-authority"
    allowed_dependency_kinds = ProviderAuthority.ALLOWED_INPUT_KINDS
    value_type = ProviderAuthority

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, ProviderAuthority)
        return IdentityObject(
            (
                ("provider_id", value.provider_id),
                ("semantic_revision", value.semantic_revision),
                ("input_contract", value.input_contract),
                ("evidence_contract", value.evidence_contract),
                ("inputs", IdentityArray(_reference_value(item) for item in value.inputs)),
            )
        )

    def _decode(self, payload: IdentityValue) -> ProviderAuthority:
        members = _members(
            payload,
            {"provider_id", "semantic_revision", "input_contract", "evidence_contract", "inputs"},
            "provider authority",
        )
        return ProviderAuthority(
            _string(members["provider_id"], "provider_id"),
            _positive_integer(members["semantic_revision"], "semantic_revision"),
            _string(members["input_contract"], "input_contract"),
            _string(members["evidence_contract"], "evidence_contract"),
            tuple(_decode_reference(item) for item in _array(members["inputs"], "inputs")),
        )

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, ProviderAuthority)
        return value.inputs


class AuthorizationGrantCodec(_RecordCodec):
    object_kind = "authorization-grant"
    payload_contract = "authorization-grant.v1"
    identity_domain = "coding-standards:authorization-grant:v1"
    identity_label = "authorization-grant"
    allowed_dependency_kinds = frozenset[str]()
    value_type = AuthorizationGrant

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, AuthorizationGrant)
        return _authorization_value(value)

    def _decode(self, payload: IdentityValue) -> AuthorizationGrant:
        return _decode_authorization(payload)

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        return ()


class FactObservationCodec(_RecordCodec):
    object_kind = "fact-observation"
    payload_contract = "fact-observation.v1"
    identity_domain = "coding-standards:fact-observation:v2"
    identity_label = "fact-observation"
    allowed_dependency_kinds = frozenset(
        {"fact-requirement", "provider-authority", "authorization-grant"}
    )
    value_type = FactObservationAuthority

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, FactObservationAuthority)
        return IdentityObject(
            (
                ("requirement", _reference_value(value.requirement)),
                ("authorization", _reference_value(value.authorization)),
                ("provider", None if value.provider is None else _reference_value(value.provider)),
                ("projection", value.projection),
            )
        )

    def _decode(self, payload: IdentityValue) -> FactObservationAuthority:
        members = _members(
            payload, {"requirement", "authorization", "provider", "projection"}, "fact observation"
        )
        provider = (
            None
            if members["provider"] is None
            else _decode_reference(members["provider"])
        )
        return FactObservationAuthority(
            _decode_reference(members["requirement"]),
            _decode_reference(members["authorization"]),
            provider,
            _projection(members["projection"], FactObservationAuthority.FIELDS, "fact observation"),
        )

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, FactObservationAuthority)
        return tuple(
            sorted(
                (
                    value.requirement,
                    value.authorization,
                    *((value.provider,) if value.provider is not None else ()),
                )
            )
        )


class CoverageViewCodec(_RecordCodec):
    object_kind = "coverage-view"
    payload_contract = "coverage-view.v1"
    identity_domain = "coding-standards:coverage-authority-view:v3"
    identity_label = "coverage-view"
    allowed_dependency_kinds = frozenset(
        {"canonical-standards-corpus", "compiled-policy-impact", "standards-graph", "coverage-horizon"}
    )
    value_type = CoverageViewAuthority

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, CoverageViewAuthority)
        return _references_projection(
            (
                ("metadata", value.metadata),
                ("policy_impact", value.policy_impact),
                ("graph", value.graph),
                ("horizon", value.horizon),
            ),
            value.projection,
        )

    def _decode(self, payload: IdentityValue) -> CoverageViewAuthority:
        references, projection = _decode_references_projection(
            payload,
            (
                ("metadata", "canonical-standards-corpus"),
                ("policy_impact", "compiled-policy-impact"),
                ("graph", "standards-graph"),
                ("horizon", "coverage-horizon"),
            ),
            CoverageViewAuthority.FIELDS,
        )
        return CoverageViewAuthority(*references, projection)

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, CoverageViewAuthority)
        return tuple(sorted((value.metadata, value.policy_impact, value.graph, value.horizon)))


class CoverageRequirementCodec(_RecordCodec):
    object_kind = "coverage-requirement"
    payload_contract = "coverage-requirement.v1"
    identity_domain = "coding-standards:coverage-audit-requirement:v3"
    identity_label = "coverage-requirement"
    allowed_dependency_kinds = frozenset({"coverage-view"})
    value_type = CoverageRequirementAuthority

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, CoverageRequirementAuthority)
        return _dependent_projection("coverage_view", value.coverage_view, value.projection)

    def _decode(self, payload: IdentityValue) -> CoverageRequirementAuthority:
        reference, projection = _decode_dependent_projection(
            payload, "coverage_view", "coverage-view", CoverageRequirementAuthority.FIELDS
        )
        return CoverageRequirementAuthority(reference, projection)

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, CoverageRequirementAuthority)
        return (value.coverage_view,)


class CoverageAttestationCodec(_RecordCodec):
    object_kind = "coverage-attestation"
    payload_contract = "coverage-attestation.v1"
    identity_domain = "coding-standards:coverage-attestation:v3"
    identity_label = "coverage-attestation"
    allowed_dependency_kinds = frozenset({"coverage-requirement", "authorization-grant"})
    value_type = CoverageAttestationAuthority

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, CoverageAttestationAuthority)
        return _references_projection(
            (("requirement", value.requirement), ("authorization", value.authorization)),
            value.projection,
        )

    def _decode(self, payload: IdentityValue) -> CoverageAttestationAuthority:
        references, projection = _decode_references_projection(
            payload,
            (("requirement", "coverage-requirement"), ("authorization", "authorization-grant")),
            CoverageAttestationAuthority.FIELDS,
        )
        return CoverageAttestationAuthority(references[0], references[1], projection)

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, CoverageAttestationAuthority)
        return tuple(sorted((value.requirement, value.authorization)))


class CoverageCertificateCodec(_RecordCodec):
    object_kind = "coverage-certificate"
    payload_contract = "coverage-certificate.v1"
    identity_domain = "coding-standards:consumer-coverage-certificate:v3"
    identity_label = "coverage-certificate"
    allowed_dependency_kinds = frozenset(
        {"coverage-view", "coverage-requirement", "coverage-attestation"}
    )
    value_type = CoverageCertificateAuthority

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, CoverageCertificateAuthority)
        return _references_projection(
            (
                ("coverage_view", value.coverage_view),
                ("requirement", value.requirement),
                ("attestation", value.attestation),
            ),
            value.projection,
        )

    def _decode(self, payload: IdentityValue) -> CoverageCertificateAuthority:
        references, projection = _decode_references_projection(
            payload,
            (
                ("coverage_view", "coverage-view"),
                ("requirement", "coverage-requirement"),
                ("attestation", "coverage-attestation"),
            ),
            CoverageCertificateAuthority.FIELDS,
        )
        return CoverageCertificateAuthority(*references, projection)

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, CoverageCertificateAuthority)
        return tuple(sorted((value.coverage_view, value.requirement, value.attestation)))


class AnalysisRootCodec(_RecordCodec):
    object_kind = "analysis-root"
    payload_contract = "analysis-root.v1"
    identity_domain = "coding-standards:analysis:v4"
    identity_label = "analysis-root"
    allowed_dependency_kinds = frozenset(
        {"execution-closure", "analysis-context", "fact-observation", "coverage-attestation"}
    )
    value_type = AnalysisRootAuthority

    def _value(self, value: object) -> IdentityObject:
        assert isinstance(value, AnalysisRootAuthority)
        return IdentityObject(
            (
                ("closure", _reference_value(value.closure)),
                ("context", _reference_value(value.context)),
                ("observations", IdentityArray(_reference_value(item) for item in value.observations)),
                ("attestations", IdentityArray(_reference_value(item) for item in value.attestations)),
                ("projection", value.projection),
            )
        )

    def _decode(self, payload: IdentityValue) -> AnalysisRootAuthority:
        members = _members(
            payload, {"closure", "context", "observations", "attestations", "projection"}, "analysis root"
        )
        return AnalysisRootAuthority(
            _decode_reference(members["closure"]),
            _decode_reference(members["context"]),
            tuple(_decode_reference(item) for item in _array(members["observations"], "observations")),
            tuple(_decode_reference(item) for item in _array(members["attestations"], "attestations")),
            _projection(members["projection"], AnalysisRootAuthority.FIELDS, "analysis root"),
        )

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, AnalysisRootAuthority)
        return tuple(
            sorted((value.closure, value.context, *value.observations, *value.attestations))
        )


def _evidence_set(values: tuple[AuthorityEvidence, ...], field: str) -> None:
    if not values or values != tuple(sorted(values)):
        raise invalid("ANALYSIS.INVALID_EVIDENCE_ORDER", f"{field} must be nonempty and sorted")
    keys = tuple(
        (item.provider_contract, item.provider_contract_version, item.id)
        for item in values
    )
    if len(set(keys)) != len(keys):
        raise invalid("ANALYSIS.DUPLICATE_EVIDENCE", f"{field} repeats a logical evidence key")


def _reference_set(
    values: tuple[AuthorityReference, ...], kind: str, field: str
) -> None:
    if values != tuple(sorted(set(values))):
        raise invalid("ANALYSIS.INVALID_REFERENCE_SET", f"{field} must be sorted and unique")
    for value in values:
        _require_kind(value, kind)


def _dependent_projection(
    name: str, reference: AuthorityReference, projection: IdentityObject
) -> IdentityObject:
    return IdentityObject(((name, _reference_value(reference)), ("projection", projection)))


def _decode_dependent_projection(
    payload: IdentityValue,
    name: str,
    kind: str,
    projection_fields: frozenset[str],
) -> tuple[AuthorityReference, IdentityObject]:
    members = _members(payload, {name, "projection"}, name)
    reference = _decode_reference(members[name])
    _require_kind(reference, kind)
    return reference, _projection(members["projection"], projection_fields, name)


def _references_projection(
    references: tuple[tuple[str, AuthorityReference], ...],
    projection: IdentityObject,
) -> IdentityObject:
    return IdentityObject(
        (
            *((name, _reference_value(reference)) for name, reference in references),
            ("projection", projection),
        )
    )


def _decode_references_projection(
    payload: IdentityValue,
    references: tuple[tuple[str, str], ...],
    projection_fields: frozenset[str],
) -> tuple[tuple[AuthorityReference, ...], IdentityObject]:
    names = {name for name, _ in references}
    members = _members(payload, {*names, "projection"}, "authority projection")
    selected = tuple(_decode_reference(members[name]) for name, _ in references)
    for reference, (_, kind) in zip(selected, references, strict=True):
        _require_kind(reference, kind)
    return selected, _projection(
        members["projection"], projection_fields, "authority projection"
    )


def _evidence_value(value: AuthorityEvidence) -> IdentityObject:
    return IdentityObject(
        (
            ("id", value.id),
            ("digest", value.digest),
            ("provider_contract", value.provider_contract),
            ("provider_contract_version", value.provider_contract_version),
        )
    )


def _decode_evidence(value: IdentityValue) -> AuthorityEvidence:
    members = _members(
        value,
        {"id", "digest", "provider_contract", "provider_contract_version"},
        "evidence reference",
    )
    return AuthorityEvidence(
        _string(members["provider_contract"], "provider_contract"),
        _string(members["provider_contract_version"], "provider_contract_version"),
        _string(members["id"], "id"),
        _string(members["digest"], "digest"),
    )


def _authorization_value(value: AuthorizationGrant) -> IdentityObject:
    return IdentityObject(
        (
            ("issuer_id", value.issuer_id),
            ("issuer_semantic_revision", value.issuer_semantic_revision),
            ("grant_id", value.grant_id),
            ("principal_id", value.principal_id),
            ("capability", value.capability),
            ("action", value.action),
            (
                "subject",
                IdentityObject((("kind", value.subject_kind), ("id", value.subject_id))),
            ),
            ("authorization_contract", "authorization-grant.v1"),
            (
                "authorization_evidence",
                IdentityArray(_evidence_value(item) for item in value.authorization_evidence),
            ),
            ("revocation_authority_id", value.revocation_authority_id),
            (
                "revocation_authority_semantic_revision",
                value.revocation_authority_semantic_revision,
            ),
            ("revocation_contract", "authorization-revocation.v1"),
            (
                "revocation_evidence",
                IdentityArray(_evidence_value(item) for item in value.revocation_evidence),
            ),
            ("revocation_state", "not-revoked"),
            ("decision", "allow"),
        )
    )


def _decode_authorization(value: IdentityValue) -> AuthorizationGrant:
    expected = {
        "issuer_id",
        "issuer_semantic_revision",
        "grant_id",
        "principal_id",
        "capability",
        "action",
        "subject",
        "authorization_contract",
        "authorization_evidence",
        "revocation_authority_id",
        "revocation_authority_semantic_revision",
        "revocation_contract",
        "revocation_evidence",
        "revocation_state",
        "decision",
    }
    members = _members(value, expected, "authorization grant")
    if (
        members["authorization_contract"] != "authorization-grant.v1"
        or members["revocation_contract"] != "authorization-revocation.v1"
        or members["revocation_state"] != "not-revoked"
        or members["decision"] != "allow"
    ):
        raise invalid(
            "ANALYSIS.INVALID_AUTHORIZATION_GRANT",
            "authorization grant contracts or decision are invalid",
        )
    subject = _members(members["subject"], {"kind", "id"}, "authorization subject")
    return AuthorizationGrant(
        _string(members["issuer_id"], "issuer_id"),
        _positive_integer(members["issuer_semantic_revision"], "issuer_semantic_revision"),
        _string(members["grant_id"], "grant_id"),
        _string(members["principal_id"], "principal_id"),
        _string(members["capability"], "capability"),
        _string(members["action"], "action"),
        _string(subject["kind"], "subject.kind"),
        _string(subject["id"], "subject.id"),
        tuple(
            _decode_evidence(item)
            for item in _array(members["authorization_evidence"], "authorization_evidence")
        ),
        _string(members["revocation_authority_id"], "revocation_authority_id"),
        _positive_integer(
            members["revocation_authority_semantic_revision"],
            "revocation_authority_semantic_revision",
        ),
        tuple(
            _decode_evidence(item)
            for item in _array(members["revocation_evidence"], "revocation_evidence")
        ),
    )


ROUTING_PROJECTION_CODEC = RoutingProjectionCodec()
COVERAGE_HORIZON_CODEC = CoverageHorizonCodec()
ANALYSIS_CONTEXT_CODEC = AnalysisContextCodec()
FACT_REQUIREMENT_CODEC = FactRequirementCodec()
PROVIDER_AUTHORITY_CODEC = ProviderAuthorityCodec()
AUTHORIZATION_GRANT_CODEC = AuthorizationGrantCodec()
FACT_OBSERVATION_CODEC = FactObservationCodec()
COVERAGE_VIEW_CODEC = CoverageViewCodec()
COVERAGE_REQUIREMENT_CODEC = CoverageRequirementCodec()
COVERAGE_ATTESTATION_CODEC = CoverageAttestationCodec()
COVERAGE_CERTIFICATE_CODEC = CoverageCertificateCodec()
ANALYSIS_ROOT_CODEC = AnalysisRootCodec()
ANALYSIS_CODECS = CodecSet(
    "standards-analysis",
    (
        ROUTING_PROJECTION_CODEC,
        COVERAGE_HORIZON_CODEC,
        ANALYSIS_CONTEXT_CODEC,
        FACT_REQUIREMENT_CODEC,
        PROVIDER_AUTHORITY_CODEC,
        AUTHORIZATION_GRANT_CODEC,
        FACT_OBSERVATION_CODEC,
        COVERAGE_VIEW_CODEC,
        COVERAGE_REQUIREMENT_CODEC,
        COVERAGE_ATTESTATION_CODEC,
        COVERAGE_CERTIFICATE_CODEC,
        ANALYSIS_ROOT_CODEC,
    ),
)

__all__ = (
    "ANALYSIS_CODECS",
    "ANALYSIS_CONTEXT_CODEC",
    "ANALYSIS_ROOT_CODEC",
    "AUTHORIZATION_GRANT_CODEC",
    "COVERAGE_ATTESTATION_CODEC",
    "COVERAGE_CERTIFICATE_CODEC",
    "COVERAGE_HORIZON_CODEC",
    "COVERAGE_REQUIREMENT_CODEC",
    "COVERAGE_VIEW_CODEC",
    "FACT_OBSERVATION_CODEC",
    "FACT_REQUIREMENT_CODEC",
    "PROVIDER_AUTHORITY_CODEC",
    "AnalysisContextAuthority",
    "AnalysisRootAuthority",
    "AuthorityEvidence",
    "AuthorizationGrant",
    "CoverageAttestationAuthority",
    "CoverageCertificateAuthority",
    "CoverageHorizonAuthority",
    "CoverageHorizonCodec",
    "CoverageRequirementAuthority",
    "CoverageViewAuthority",
    "FactObservationAuthority",
    "FactRequirementAuthority",
    "ProviderAuthority",
    "ROUTING_PROJECTION_CODEC",
    "RoutingProjectionAuthority",
    "RoutingProjectionCodec",
)
