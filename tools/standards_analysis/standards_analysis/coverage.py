from __future__ import annotations

import hashlib
import re
import tomllib
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from tools.standards_applicability.standards_applicability import LANGUAGE_VERSION
from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    ContentSource,
    ContentSourceInput,
    MetadataError,
    PolicyUnit,
    SuiteInputManifest,
    content_source,
    load_suite_input_manifest,
)
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
)

from .errors import AnalysisError, AnalysisFailure
from .keys import analysis_identity, analysis_key_bytes, analysis_value_digest, raw_digest
from .trust import (
    AnalysisExecutionContext,
    AuthorizationAuthorityContract,
    AuthorizationClaim,
    AuthorizationRequest,
    EvidenceContractKey,
    EvidenceReference,
    ResolvedEvidence,
    construct_authorization_record,
)


DEFAULT_HORIZON = "evaluation/standards-effectiveness/policy-coverage/horizons.toml"
HORIZON_ID = "audit-horizon.policy-impact-consumers"
HORIZON_PROVIDER = "standards-analysis:policy-impact-consumer-horizon"
HORIZON_VERSION = 6
DEFAULT_ATTESTATION_REGISTRY = (
    "evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml"
)
DEFAULT_AUTHORIZATION_AUTHORITY = (
    "evaluation/standards-effectiveness/policy-coverage/authorization-authority.toml"
)
DEFAULT_REVOCATIONS = (
    "evaluation/standards-effectiveness/policy-coverage/revocations.toml"
)
COVERAGE_EVIDENCE_CONTRACT = "coverage-evidence.v1"


def _error(
    code: str,
    message: str,
    *,
    path: str | None = None,
    field: str | None = None,
    observed: str | None = None,
    unavailable: bool = False,
) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure(
            code,
            "unavailable" if unavailable else "invalid",
            message,
            path=path,
            field=field,
            observed=observed,
        )
    )


def _read(source: ContentSource, path: str) -> bytes:
    try:
        return source.read_bytes(path)
    except MetadataError as error:
        failure = error.failure
        raise _error(
            "COVERAGE.INPUT_UNAVAILABLE"
            if failure.outcome == "unavailable"
            else "COVERAGE.PATH",
            failure.message,
            path=failure.path or path,
            unavailable=failure.outcome == "unavailable",
        ) from error


def _toml(source: ContentSource, path: str) -> dict[str, Any]:
    try:
        return tomllib.loads(_read(source, path).decode("utf-8"))
    except UnicodeDecodeError as error:
        raise _error("COVERAGE.INVALID_UTF8", str(error), path=path) from error
    except tomllib.TOMLDecodeError as error:
        raise _error("COVERAGE.INVALID_TOML", str(error), path=path) from error


def _exact(
    value: Mapping[str, object],
    *,
    required: set[str],
    allowed: set[str],
    path: str,
    field: str,
) -> None:
    missing = sorted(required - set(value))
    extra = sorted(set(value) - allowed)
    if missing or extra:
        raise _error(
            "COVERAGE.FIELDS",
            "coverage record fields are invalid",
            path=path,
            field=field,
            observed=(missing or extra)[0],
        )


def _text(value: object, *, path: str, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise _error(
            "COVERAGE.VALUE",
            "coverage field must be a non-empty string",
            path=path,
            field=field,
        )
    return value


def _texts(
    value: object,
    *,
    path: str,
    field: str,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or (not allow_empty and not value)
        or any(not isinstance(item, str) or not item for item in value)
        or len(value) != len(set(value))
    ):
        raise _error(
            "COVERAGE.VALUE",
            "coverage field must contain unique non-empty strings",
            path=path,
            field=field,
        )
    return tuple(value)


def _digest(value: object) -> str:
    return raw_digest(analysis_key_bytes(value))


@dataclass(frozen=True, slots=True)
class CoverageHorizonMember:
    id: str
    roles: tuple[str, ...]
    fingerprint: str

    def as_projection(self) -> dict[str, object]:
        return {
            "id": self.id,
            "roles": list(self.roles),
            "fingerprint": self.fingerprint,
        }


@dataclass(frozen=True, slots=True)
class CoverageHorizon:
    id: str
    provider: str
    version: int
    members: tuple[CoverageHorizonMember, ...]
    digest: str
    input_sources: tuple[str, ...]
    suite_inputs: SuiteInputManifest
    consumer_members: Mapping[str, CoverageHorizonMember]


@dataclass(frozen=True, slots=True)
class CoverageViewDefinition:
    subject: str
    owner: str
    semantic_revision: int
    representation_digest: str
    structural_digest: str
    relationship_kinds: tuple[str, ...]
    relationship_fingerprints: tuple[tuple[str, str], ...]
    relationship_kind_contract_version: int
    relationship_provider_contract_digest: str
    applicability_language_version: int
    applicability_program_digests: tuple[str, ...]
    fact_schema_digest: str
    horizon_id: str
    horizon_provider: str
    horizon_version: int
    horizon_digest: str
    horizon_members: tuple[CoverageHorizonMember, ...]

    def as_projection(self) -> dict[str, object]:
        return {
            "subject": self.subject,
            "owner": self.owner,
            "semantic_revision": self.semantic_revision,
            "representation_digest": self.representation_digest,
            "structural_digest": self.structural_digest,
            "relationship_kinds": list(self.relationship_kinds),
            "relationship_fingerprints": [
                {"edge": edge, "fingerprint": fingerprint}
                for edge, fingerprint in self.relationship_fingerprints
            ],
            "relationship_kind_contract_version": self.relationship_kind_contract_version,
            "relationship_provider_contract_digest": self.relationship_provider_contract_digest,
            "applicability_language_version": self.applicability_language_version,
            "applicability_program_digests": list(self.applicability_program_digests),
            "fact_schema_digest": self.fact_schema_digest,
            "horizon": {
                "id": self.horizon_id,
                "provider": self.horizon_provider,
                "version": self.horizon_version,
                "digest": self.horizon_digest,
                "members": [member.as_projection() for member in self.horizon_members],
            },
        }


@dataclass(frozen=True, slots=True)
class CoverageRequirementDefinition:
    subject: str
    owner: str
    semantic_revision: int
    relationship_kinds: tuple[str, ...]
    horizon: str

    def as_projection(self) -> dict[str, object]:
        return {
            "subject": self.subject,
            "owner": self.owner,
            "semantic_revision": self.semantic_revision,
            "relationship_kinds": list(self.relationship_kinds),
            "horizon": self.horizon,
        }


@dataclass(frozen=True, slots=True)
class CoverageDefinitionIndex:
    horizon: CoverageHorizon
    views: Mapping[str, CoverageViewDefinition]
    requirements: Mapping[str, CoverageRequirementDefinition]
    input_sources: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RepositoryCoverageDecisions:
    attestations: Mapping[str, Mapping[str, object]]
    authorization_records: Mapping[str, Mapping[str, object]]
    input_sources: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "attestations",
            MappingProxyType(dict(sorted(self.attestations.items()))),
        )
        object.__setattr__(
            self,
            "authorization_records",
            MappingProxyType(dict(sorted(self.authorization_records.items()))),
        )
        object.__setattr__(self, "input_sources", tuple(sorted(self.input_sources)))

    @property
    def covered_subjects(self) -> frozenset[str]:
        return frozenset(self.attestations)


@dataclass(frozen=True, slots=True)
class _RepositoryAuthorization:
    source: ContentSource
    contract: AuthorizationAuthorityContract
    capability: str
    evidence: tuple[ResolvedEvidence, ...]
    revocation_evidence: tuple[ResolvedEvidence, ...]
    revoked: frozenset[str]
    inputs: tuple[str, ...]

    def authorize(self, request: AuthorizationRequest) -> AuthorizationClaim:
        if request.capability != self.capability:
            raise _error(
                "COVERAGE.AUTHORIZATION_CAPABILITY",
                "repository authority does not grant the requested capability",
            )
        return AuthorizationClaim(
            request.action,
            request.subject_kind,
            request.subject_id,
            request.capability,
            tuple(
                ResolvedEvidence(item, _read(self.source, item.id))
                for item in request.evidence
            ),
            self.evidence,
            self.revocation_evidence,
            "not-revoked",
            "allow",
        )



def _merge_member(
    members: dict[str, tuple[set[str], str]],
    member_id: str,
    role: str,
    fingerprint: str,
) -> None:
    previous = members.get(member_id)
    if previous is None:
        members[member_id] = ({role}, fingerprint)
        return
    roles, previous_fingerprint = previous
    if previous_fingerprint != fingerprint:
        raise _error(
            "COVERAGE.MEMBER_CONFLICT",
            "one horizon member resolved to contradictory content",
            observed=member_id,
        )
    roles.add(role)


def _file_fingerprint(source: ContentSource, path: str) -> str:
    return raw_digest(_read(source, path))


def _load_coverage_horizon(
    source: ContentSourceInput,
    corpus: CanonicalStandardsCorpus,
    compiled: CompiledPolicyImpactSet,
    path: str = DEFAULT_HORIZON,
) -> CoverageHorizon:
    selected_source = content_source(source)
    raw = _toml(selected_source, path)
    _exact(
        raw,
        required={
            "schema_version",
            "id",
            "provider",
            "version",
            "suite_registry",
            "suite_inputs",
            "edge_source_registry",
        },
        allowed={
            "schema_version",
            "id",
            "provider",
            "version",
            "suite_registry",
            "suite_inputs",
            "edge_source_registry",
        },
        path=path,
        field="horizon",
    )
    if raw["schema_version"] != 1 or raw["version"] != HORIZON_VERSION:
        raise _error(
            "COVERAGE.HORIZON_VERSION", "unsupported horizon version", path=path
        )
    horizon_id = _text(raw["id"], path=path, field="id")
    provider = _text(raw["provider"], path=path, field="provider")
    if horizon_id != HORIZON_ID or provider != HORIZON_PROVIDER:
        raise _error(
            "COVERAGE.HORIZON_PROVIDER",
            "horizon must use the registered policy-impact consumer provider",
            path=path,
        )

    members: dict[str, tuple[set[str], str]] = {}
    input_sources = {
        path,
        *corpus.module_corpus.members,
        *corpus.policy_unit_corpus.sources,
    }
    for module in corpus.modules:
        _merge_member(
            members,
            f"repository:{module.path}",
            "canonical-module",
            _file_fingerprint(selected_source, module.path),
        )
    for unit in corpus.policy_units:
        _merge_member(
            members,
            f"policy-unit:{unit.id}",
            "policy-unit",
            _digest(
                {
                    "id": unit.id,
                    "module": unit.module,
                    "semantic_revision": unit.semantic_revision,
                    "representation_digest": unit.representation_digest,
                    "structural_digest": unit.structural_digest,
                }
            ),
        )

    edge_registry_path = _text(
        raw["edge_source_registry"], path=path, field="edge_source_registry"
    )
    input_sources.add(edge_registry_path)
    edge_registry = _toml(selected_source, edge_registry_path)
    for source in edge_registry.get("sources", []):
        if not isinstance(source, dict):
            raise _error(
                "COVERAGE.EDGE_SOURCE",
                "edge source must be a table",
                path=edge_registry_path,
            )
        source_id = _text(source.get("id"), path=edge_registry_path, field="id")
        _merge_member(
            members,
            f"graph-provider:{source_id}",
            "edge-source-registration",
            _digest(source),
        )
        source_path = source.get("path")
        if isinstance(source_path, str):
            input_sources.add(source_path)
            _merge_member(
                members,
                f"repository:{source_path}",
                "edge-source-manifest",
                _file_fingerprint(selected_source, source_path),
            )

    suite_registry_path = _text(raw["suite_registry"], path=path, field="suite_registry")
    suite_inputs_path = _text(raw["suite_inputs"], path=path, field="suite_inputs")
    try:
        suite_inputs = load_suite_input_manifest(selected_source, suite_inputs_path)
    except MetadataError as error:
        failure = error.failure
        raise _error(
            failure.code,
            failure.message,
            path=failure.path,
            field=failure.field,
            observed=failure.observed,
            unavailable=failure.outcome == "unavailable",
        ) from error
    if suite_inputs.registry_path != suite_registry_path:
        raise _error(
            "COVERAGE.SUITE_REGISTRY",
            "horizon and suite-input manifest select different registries",
            path=path,
            observed=f"{suite_inputs.registry_path} (expected {suite_registry_path})",
        )
    input_sources.update(
        {
            suite_inputs_path,
            suite_inputs.registry_path,
            *(suite.path for suite in suite_inputs.suites),
            *(item.path for item in suite_inputs.files if item.state == "present"),
        }
    )
    for suite in suite_inputs.suites:
        dependency = suite_inputs.dependency(suite.id)
        _merge_member(
            members,
            f"suite:{suite.id}",
            "registered-suite",
            dependency.fingerprint,
        )

    input_sources.update(compiled.input_sources)
    for artifact in compiled.artifacts.values():
        input_sources.add(artifact.repository_path)
        _merge_member(
            members,
            f"policy-impact-node:{artifact.id}",
            "supplemental-policy-impact-node",
            _digest(
                {
                    "artifact": artifact.coverage_fingerprint,
                    "content": _file_fingerprint(
                        selected_source,
                        artifact.repository_path,
                    ),
                }
            ),
        )

    resolved = tuple(
        CoverageHorizonMember(member_id, tuple(sorted(roles)), fingerprint)
        for member_id, (roles, fingerprint) in sorted(members.items())
    )
    horizon_digest = _digest(
        {
            "id": horizon_id,
            "provider": provider,
            "version": raw["version"],
            "members": [member.as_projection() for member in resolved],
        }
    )
    members_by_id = {member.id: member for member in resolved}
    consumer_members = {
        module.module_id: members_by_id[f"repository:{module.path}"]
        for module in corpus.modules
    }
    consumer_members.update(
        {
            unit.id: members_by_id[f"policy-unit:{unit.id}"]
            for unit in corpus.policy_units
        }
    )
    consumer_members.update(
        {
            artifact.id: members_by_id[f"policy-impact-node:{artifact.id}"]
            for artifact in compiled.artifacts.values()
        }
    )
    return CoverageHorizon(
        horizon_id,
        provider,
        raw["version"],
        resolved,
        horizon_digest,
        tuple(sorted(input_sources)),
        suite_inputs,
        MappingProxyType(dict(sorted(consumer_members.items()))),
    )


def load_coverage_horizon(
    source: ContentSourceInput,
    corpus: CanonicalStandardsCorpus,
    compiled: CompiledPolicyImpactSet,
    path: str = DEFAULT_HORIZON,
) -> CoverageHorizon:
    return _load_coverage_horizon(source, corpus, compiled, path)


def derive_coverage_view(
    unit: PolicyUnit,
    compiled: CompiledPolicyImpactSet,
    horizon: CoverageHorizon,
    *,
    semantic_revision: int | None = None,
    representation_digest: str | None = None,
    structural_digest: str | None = None,
) -> CoverageViewDefinition:
    relationships = tuple(
        sorted(
            (
                edge_id,
                semantics.dependency_fingerprint,
                semantics.relation,
                semantics.applicability_program.dependency_digest,
            )
            for edge_id, semantics in compiled.semantics.items()
            if semantics.source == unit.id
        )
    )
    local_members: dict[str, CoverageHorizonMember] = {}
    for edge_id, _fingerprint, _relation, _program in relationships:
        semantics = compiled.semantics[edge_id]
        try:
            consumer = horizon.consumer_members[semantics.consumer]
        except KeyError as error:
            raise _error(
                "COVERAGE.CONSUMER_MISSING",
                "relationship consumer is absent from the coverage horizon",
                observed=semantics.consumer,
            ) from error
        local_members[consumer.id] = consumer
        suite_id = semantics.evidence_owner.removeprefix("suite:")
        if not semantics.evidence_owner.startswith("suite:"):
            raise _error(
                "COVERAGE.EVIDENCE_OWNER",
                "relationship evidence owner must be a registered suite",
                observed=semantics.evidence_owner,
            )
        try:
            dependency = horizon.suite_inputs.dependency(suite_id)
        except KeyError as error:
            raise _error(
                "COVERAGE.EVIDENCE_SUITE_MISSING",
                "relationship evidence suite is absent from the suite manifest",
                observed=suite_id,
            ) from error
        member_id = f"suite-dependency:{suite_id}"
        local_members[member_id] = CoverageHorizonMember(
            member_id,
            ("evidence-suite-dependency",),
            dependency.fingerprint,
        )
    selected_members = tuple(local_members[key] for key in sorted(local_members))
    local_horizon_digest = _digest(
        {
            "id": horizon.id,
            "provider": horizon.provider,
            "version": horizon.version,
            "members": [member.as_projection() for member in selected_members],
        }
    )
    return CoverageViewDefinition(
        unit.id,
        unit.module,
        semantic_revision or unit.semantic_revision,
        representation_digest or unit.representation_digest,
        structural_digest or unit.structural_digest,
        tuple(sorted({relationship[2] for relationship in relationships})),
        tuple((relationship[0], relationship[1]) for relationship in relationships),
        compiled.relationship_kind_contract_version,
        compiled.provider_contract_digest,
        LANGUAGE_VERSION,
        tuple(sorted({relationship[3] for relationship in relationships})),
        compiled.fact_schema.digest,
        horizon.id,
        horizon.provider,
        horizon.version,
        local_horizon_digest,
        selected_members,
    )


def derive_coverage_requirement(
    view: CoverageViewDefinition,
) -> CoverageRequirementDefinition:
    return CoverageRequirementDefinition(
        view.subject,
        view.owner,
        view.semantic_revision,
        view.relationship_kinds,
        view.horizon_id,
    )


def compile_coverage_definitions(
    corpus: CanonicalStandardsCorpus,
    compiled: CompiledPolicyImpactSet,
    horizon: CoverageHorizon,
) -> CoverageDefinitionIndex:
    views = {
        unit.id: derive_coverage_view(unit, compiled, horizon)
        for unit in corpus.policy_units
    }
    requirements = {
        subject: derive_coverage_requirement(view) for subject, view in views.items()
    }
    return CoverageDefinitionIndex(
        horizon,
        views,
        requirements,
        horizon.input_sources,
    )


def coverage_requirement_projection(
    requirement: CoverageRequirementDefinition,
    view: CoverageViewDefinition,
) -> dict[str, object]:
    return {
        **requirement.as_projection(),
        "required_evidence_contract": COVERAGE_EVIDENCE_CONTRACT,
        "view_digest": analysis_value_digest(view.as_projection()),
    }


def coverage_requirement_id(
    requirement: CoverageRequirementDefinition,
    view: CoverageViewDefinition,
) -> str:
    return raw_digest(
        analysis_key_bytes(coverage_requirement_projection(requirement, view))
    )


def load_repository_coverage_decisions(
    source_input: ContentSourceInput,
    definitions: CoverageDefinitionIndex,
    *,
    attestation_registry: str = DEFAULT_ATTESTATION_REGISTRY,
    authorization_authority: str = DEFAULT_AUTHORIZATION_AUTHORITY,
    revocations: str = DEFAULT_REVOCATIONS,
) -> RepositoryCoverageDecisions:
    source = content_source(source_input)
    authority = _load_repository_authorization(
        source, authorization_authority, revocations
    )
    requirement_subjects = {
        coverage_requirement_id(definitions.requirements[subject], view): subject
        for subject, view in definitions.views.items()
    }
    if len(requirement_subjects) != len(definitions.requirements):
        raise _error(
            "COVERAGE.REQUIREMENT_IDENTITY_COLLISION",
            "coverage requirements do not have unique identities",
        )
    registry = _toml(source, attestation_registry)
    registry_version = registry.get("schema_version")
    registry_fields = {"schema_version", "sources"}
    if registry_version == 3:
        registry_fields.add("engine_sources")
    _exact(
        registry,
        required=registry_fields,
        allowed=registry_fields,
        path=attestation_registry,
        field="attestation registry",
    )
    if type(registry_version) is not int or registry_version not in {2, 3}:
        raise _error(
            "COVERAGE.ATTESTATION_VERSION",
            "unsupported repository attestation registry version",
            path=attestation_registry,
        )
    claim_sources = _texts(
        registry["sources"],
        path=attestation_registry,
        field="sources",
        allow_empty=True,
    )
    attestations: dict[str, Mapping[str, object]] = {}
    authorizations: dict[str, Mapping[str, object]] = {}
    inputs = {attestation_registry, *claim_sources, *authority.inputs}
    for claim_source in claim_sources:
        declaration = _toml(source, claim_source)
        _exact(
            declaration,
            required={"schema_version", "attestations"},
            allowed={"schema_version", "attestations"},
            path=claim_source,
            field="attestation source",
        )
        claims = declaration["attestations"]
        version = declaration["schema_version"]
        if (
            type(version) is not int
            or version not in {5, 6}
            or not isinstance(claims, list)
        ):
            raise _error(
                "COVERAGE.ATTESTATION_VERSION",
                "unsupported repository attestation source version",
                path=claim_source,
            )
        for raw_claim in claims:
            if not isinstance(raw_claim, dict):
                raise _error(
                    "COVERAGE.ATTESTATION",
                    "attestation must be a table",
                    path=claim_source,
                )
            claim = _coverage_claim(raw_claim, claim_source, version)
            inputs.update(
                item.id if isinstance(item, EvidenceReference) else item
                for item in (*claim["evidence"], *claim["explicit_exclusions"])
            )
            requirement_id = str(claim["requirement_id"])
            subject = requirement_subjects.get(requirement_id)
            if subject is None:
                continue
            if subject in attestations:
                raise _error(
                    "COVERAGE.DUPLICATE_SUBJECT",
                    "coverage subject has more than one current attestation",
                    path=claim_source,
                    observed=subject,
                )
            if claim["auditor_provenance"] != authority.contract.principal_id:
                raise _error(
                    "COVERAGE.UNAUTHORIZED_PRINCIPAL",
                    "attestation provenance is not authorized",
                    path=claim_source,
                    observed=str(claim["auditor_provenance"]),
                )
            evidence = tuple(
                item
                if isinstance(item, EvidenceReference)
                else _repository_evidence(source, item)
                for item in claim["evidence"]
            )
            exclusions = tuple(
                item
                if isinstance(item, EvidenceReference)
                else _repository_evidence(source, item)
                for item in claim["explicit_exclusions"]
            )
            authorization = construct_authorization_record(
                AnalysisExecutionContext(authority),
                AuthorizationRequest(
                    "coverage-attestation",
                    "coverage-requirement",
                    requirement_id,
                    authority.capability,
                    (*evidence, *exclusions),
                ),
            )
            legacy_grant = analysis_identity(
                "coding-standards:repository-coverage-grant-key:v1",
                "coverage-grant",
                {
                    "issuer": authority.contract.issuer_id,
                    "principal": authority.contract.principal_id,
                    "requirement": requirement_id,
                    "capability": authority.capability,
                },
            )
            authorization_id = str(authorization.reference["id"])
            if (
                legacy_grant in authority.revoked
                or authorization_id in authority.revoked
            ):
                raise _error(
                    "COVERAGE.AUTHORIZATION_REVOKED",
                    "repository coverage authorization is revoked",
                    path=revocations,
                    observed=authorization_id,
                )
            attestations[subject] = MappingProxyType(
                {
                    "requirement_id": requirement_id,
                    "conclusion": claim["conclusion"],
                    "evidence": [item.as_contract() for item in evidence],
                    "explicit_exclusions": [item.as_contract() for item in exclusions],
                    "rationale": claim["rationale"],
                    "auditor_provenance": claim["auditor_provenance"],
                    "schema_version": 4,
                    "authorization_id": authorization_id,
                }
            )
            authorizations[authorization_id] = MappingProxyType(
                authorization.as_contract()
            )
    if registry_version == 3:
        from .coverage_publication import load_engine_coverage_receipt

        for path in _texts(registry["engine_sources"], path=attestation_registry, field="engine_sources", allow_empty=True):
            inputs.add(path)
            loaded = load_engine_coverage_receipt(
                source, path, definitions, authority.revoked
            )
            if loaded is None:
                continue
            subject, claim, authorization, evidence_paths = loaded
            if subject in attestations:
                raise _error(
                    "COVERAGE.DUPLICATE_SUBJECT",
                    "coverage subject has more than one current attestation",
                    path=path,
                    observed=subject,
                )
            inputs.update(evidence_paths)
            attestations[subject] = MappingProxyType(claim)
            authorizations[claim["authorization_id"]] = MappingProxyType(authorization)
    return RepositoryCoverageDecisions(
        attestations,
        authorizations,
        tuple(sorted(inputs)),
    )


def _load_repository_authorization(
    source: ContentSource,
    path: str,
    revocations_path: str,
) -> _RepositoryAuthorization:
    raw = _toml(source, path)
    fields = {
        "schema_version",
        "issuer_id",
        "issuer_semantic_revision",
        "principal_id",
        "capability",
        "authorization_evidence",
        "revocation_authority_id",
        "revocation_authority_semantic_revision",
        "revocations",
    }
    _exact(raw, required=fields, allowed=fields, path=path, field="authorization")
    if raw["schema_version"] != 1 or raw["revocations"] != revocations_path:
        raise _error(
            "COVERAGE.AUTHORIZATION_VERSION",
            "unsupported or contradictory repository authorization authority",
            path=path,
        )
    revoked = _toml(source, revocations_path)
    revoked_fields = {
        "schema_version",
        "authority_id",
        "semantic_revision",
        "revoked_grants",
    }
    _exact(
        revoked,
        required=revoked_fields,
        allowed=revoked_fields,
        path=revocations_path,
        field="revocations",
    )
    if (
        revoked["schema_version"] != 1
        or revoked["authority_id"] != raw["revocation_authority_id"]
        or revoked["semantic_revision"]
        != raw["revocation_authority_semantic_revision"]
    ):
        raise _error(
            "COVERAGE.REVOCATION_AUTHORITY_MISMATCH",
            "revocation authority does not match authorization authority",
            path=revocations_path,
        )
    evidence_paths = _texts(
        raw["authorization_evidence"],
        path=path,
        field="authorization_evidence",
    )
    evidence = tuple(
        _resolved_repository_evidence(source, item) for item in evidence_paths
    )
    revocation_evidence = (
        _resolved_repository_evidence(source, revocations_path),
    )
    evidence_contracts = tuple(
        sorted(
            {
                EvidenceContractKey(
                    item.reference.provider_contract,
                    item.reference.provider_contract_version,
                )
                for item in evidence
            }
        )
    )
    revocation_contracts = tuple(
        EvidenceContractKey(
            item.reference.provider_contract,
            item.reference.provider_contract_version,
        )
        for item in revocation_evidence
    )
    contract = AuthorizationAuthorityContract(
        _text(raw["issuer_id"], path=path, field="issuer_id"),
        _positive_integer(
            raw["issuer_semantic_revision"],
            path=path,
            field="issuer_semantic_revision",
        ),
        _text(raw["principal_id"], path=path, field="principal_id"),
        "authorization-grant.v1",
        evidence_contracts,
        _text(
            raw["revocation_authority_id"],
            path=path,
            field="revocation_authority_id",
        ),
        _positive_integer(
            raw["revocation_authority_semantic_revision"],
            path=path,
            field="revocation_authority_semantic_revision",
        ),
        "authorization-revocation.v1",
        revocation_contracts,
    )
    return _RepositoryAuthorization(
        source,
        contract,
        _text(raw["capability"], path=path, field="capability"),
        evidence,
        revocation_evidence,
        frozenset(
            _texts(
                revoked["revoked_grants"],
                path=revocations_path,
                field="revoked_grants",
                allow_empty=True,
            )
        ),
        tuple(sorted({path, revocations_path, *evidence_paths})),
    )


def _coverage_claim(
    raw: Mapping[str, object], path: str, version: int = 5
) -> dict[str, object]:
    fields = {
        "requirement_id",
        "conclusion",
        "evidence",
        "explicit_exclusions",
        "rationale",
        "auditor_provenance",
    }
    _exact(raw, required=fields, allowed=fields, path=path, field="attestation")
    conclusion = _text(raw["conclusion"], path=path, field="conclusion")
    if conclusion != "complete":
        raise _error(
            "COVERAGE.ATTESTATION_INVALID",
            "coverage attestation conclusion must be complete",
            path=path,
        )
    return {
        "requirement_id": _coverage_requirement_digest(
            raw["requirement_id"], path=path
        ),
        "conclusion": conclusion,
        "evidence": _claim_evidence(
            raw["evidence"], path=path, field="evidence", version=version
        ),
        "explicit_exclusions": _claim_evidence(
            raw["explicit_exclusions"],
            path=path,
            field="explicit_exclusions",
            allow_empty=True,
            version=version,
        ),
        "rationale": _text(raw["rationale"], path=path, field="rationale"),
        "auditor_provenance": _text(
            raw["auditor_provenance"], path=path, field="auditor_provenance"
        ),
    }


def _claim_evidence(
    value: object, *, path: str, field: str, version: int, allow_empty: bool = False
) -> tuple[str, ...] | tuple[EvidenceReference, ...]:
    if version == 5:
        return _texts(value, path=path, field=field, allow_empty=allow_empty)
    if not isinstance(value, list) or (not value and not allow_empty):
        raise _error(
            "COVERAGE.EVIDENCE",
            "pinned evidence must be an array",
            path=path,
            field=field,
        )
    references = []
    fields = {"id", "digest", "provider_contract", "provider_contract_version"}
    for item in value:
        if not isinstance(item, dict):
            raise _error(
                "COVERAGE.EVIDENCE",
                "pinned evidence must contain reference tables",
                path=path,
                field=field,
            )
        _exact(item, required=fields, allowed=fields, path=path, field=field)
        reference = EvidenceReference(
            **{
                key: _text(item[key], path=path, field=f"{field}.{key}")
                for key in fields
            }
        )
        if (
            reference.provider_contract != "repository-content"
            or reference.provider_contract_version != "1"
            or re.fullmatch(r"sha256:[0-9a-f]{64}", reference.digest) is None
        ):
            raise _error(
                "COVERAGE.EVIDENCE",
                "pinned repository evidence requires a SHA-256 digest and repository-content version 1",
                path=path,
                field=field,
            )
        references.append(reference)
    if len({item.id for item in references}) != len(references):
        raise _error(
            "COVERAGE.EVIDENCE",
            "pinned evidence paths must be unique",
            path=path,
            field=field,
        )
    return tuple(references)


def _coverage_requirement_digest(value: object, *, path: str) -> str:
    requirement_id = _text(value, path=path, field="requirement_id")
    if re.fullmatch(r"sha256:[0-9a-f]{64}", requirement_id) is None:
        raise _error(
            "COVERAGE.REQUIREMENT_ID",
            "coverage requirement identity must be one SHA-256 digest",
            path=path,
            field="requirement_id",
            observed=requirement_id,
        )
    return requirement_id


def _positive_integer(value: object, *, path: str, field: str) -> int:
    if type(value) is not int or value < 1:
        raise _error(
            "COVERAGE.VALUE",
            "coverage field must be a positive integer",
            path=path,
            field=field,
        )
    return value


def _repository_evidence(source: ContentSource, path: str) -> EvidenceReference:
    return EvidenceReference(
        path,
        "sha256:" + hashlib.sha256(_read(source, path)).hexdigest(),
        "repository-content",
        "1",
    )


def _resolved_repository_evidence(
    source: ContentSource,
    path: str,
) -> ResolvedEvidence:
    return ResolvedEvidence(_repository_evidence(source, path), _read(source, path))


__all__ = (
    "CoverageDefinitionIndex",
    "CoverageHorizon",
    "CoverageHorizonMember",
    "CoverageRequirementDefinition",
    "CoverageViewDefinition",
    "RepositoryCoverageDecisions",
    "COVERAGE_EVIDENCE_CONTRACT",
    "DEFAULT_ATTESTATION_REGISTRY",
    "DEFAULT_AUTHORIZATION_AUTHORITY",
    "DEFAULT_REVOCATIONS",
    "DEFAULT_HORIZON",
    "HORIZON_ID",
    "HORIZON_PROVIDER",
    "compile_coverage_definitions",
    "coverage_requirement_id",
    "coverage_requirement_projection",
    "derive_coverage_requirement",
    "derive_coverage_view",
    "load_coverage_horizon",
    "load_repository_coverage_decisions",
)
