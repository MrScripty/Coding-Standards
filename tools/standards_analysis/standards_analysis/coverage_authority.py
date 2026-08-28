from __future__ import annotations

import hashlib
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Callable, Iterable, Mapping

from tools.standards_authority.standards_authority import (
    CONTENT_SNAPSHOT_CODEC,
    AuthorityCodec,
    AuthorityReference,
    AuthorityRepository,
    CaptureRequest,
    CodecSet,
    ContentSnapshot,
    MemoryObjectStore,
    NativeCaptureSource,
    RepositoryPath,
)
from tools.standards_identity.standards_identity import IdentityArray, IdentityObject
from tools.standards_metadata.standards_metadata import (
    CANONICAL_MODULE_CORPUS,
    CANONICAL_STANDARDS_CORPUS_CODEC,
    METADATA_CODECS,
    POLICY_UNIT_REGISTRY,
    CanonicalCorpusAuthority,
    CanonicalStandardsCorpus,
    PolicyUnitCorpus,
    load_canonical_standards_corpus,
)
from tools.standards_policy_impact.standards_policy_impact import (
    COMPILED_POLICY_IMPACT_CODEC,
    DEFAULT_REGISTRY,
    POLICY_IMPACT_CODECS,
    CompiledPolicyImpactAuthority,
    CompiledPolicyImpactSet,
    compile_policy_impact,
)

from .authority import (
    AUTHORIZATION_GRANT_CODEC,
    COVERAGE_ATTESTATION_CODEC,
    COVERAGE_CERTIFICATE_CODEC,
    COVERAGE_REQUIREMENT_CODEC,
    COVERAGE_VIEW_CODEC,
    AuthorityEvidence,
    AuthorizationGrant,
    CoverageAttestationAuthority,
    CoverageCertificateAuthority,
    CoverageRequirementAuthority,
    CoverageViewAuthority,
)
from .coverage import (
    CoverageDefinitionIndex,
    CoverageRequirementDefinition,
    CoverageViewDefinition,
    compile_coverage_definitions,
)
from .errors import AnalysisError, AnalysisFailure
from .keys import analysis_identity, analysis_key, analysis_key_bytes, raw_digest


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


@dataclass(frozen=True, slots=True)
class StoredCoverageAttestation:
    reference: AuthorityReference
    value: CoverageAttestationAuthority


@dataclass(frozen=True, slots=True)
class CoverageSubjectAuthority:
    definition: CoverageViewDefinition
    requirement_definition: CoverageRequirementDefinition
    view: AuthorityReference
    requirement: AuthorityReference
    attestation: StoredCoverageAttestation | None
    certificate: AuthorityReference | None


@dataclass(frozen=True, slots=True)
class CoverageAuthorityIndex:
    definitions: CoverageDefinitionIndex
    subjects: Mapping[str, CoverageSubjectAuthority]
    input_sources: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "subjects",
            MappingProxyType(dict(sorted(self.subjects.items()))),
        )

    @property
    def views(self) -> Mapping[str, CoverageViewDefinition]:
        return self.definitions.views

    @property
    def requirements(self) -> Mapping[str, CoverageRequirementDefinition]:
        return self.definitions.requirements

    def certificate_for(self, policy_unit: str) -> AuthorityReference | None:
        subject = self.subjects.get(policy_unit)
        return None if subject is None else subject.certificate

    def uncovered_for_module_corpus(
        self,
        corpus: PolicyUnitCorpus,
        module_id: str,
    ) -> tuple[str, ...]:
        return tuple(
            unit.id
            for unit in corpus.for_module(module_id)
            if self.certificate_for(unit.id) is None
        )


@dataclass(frozen=True, slots=True)
class RepositoryAuthorizationAuthority:
    issuer_id: str
    issuer_semantic_revision: int
    principal_id: str
    capability: str
    authorization_evidence: tuple[AuthorityEvidence, ...]
    revocation_authority_id: str
    revocation_authority_semantic_revision: int
    revocation_evidence: tuple[AuthorityEvidence, ...]
    revoked_grants: frozenset[str]
    input_sources: tuple[str, ...]


def covered_repository_policy_units(
    root: Path,
    *,
    graph_codecs: CodecSet,
    graph_codec: AuthorityCodec[object],
    build_graph: Callable[
        [
            AuthorityReference,
            AuthorityReference,
            CanonicalStandardsCorpus,
            CompiledPolicyImpactSet,
        ],
        object,
    ],
) -> frozenset[str]:
    from .authority import (
        ANALYSIS_CODECS,
        COVERAGE_HORIZON_CODEC,
        CoverageHorizonAuthority,
    )
    from .coverage import load_coverage_horizon

    repository_root = root.resolve()
    initial_corpus = load_canonical_standards_corpus(repository_root)
    initial_impact = compile_policy_impact(
        repository_root, initial_corpus, DEFAULT_REGISTRY
    )
    initial_horizon = load_coverage_horizon(
        repository_root, initial_corpus, initial_impact
    )
    scope = _repository_coverage_scope(
        repository_root,
        initial_corpus,
        initial_impact.input_sources,
        initial_horizon.input_sources,
    )
    snapshot = NativeCaptureSource(repository_root).capture(
        CaptureRequest(RepositoryPath(path.split("/")) for path in scope)
    )
    with tempfile.TemporaryDirectory(prefix="standards-coverage-") as directory:
        workspace = Path(directory)
        for item in snapshot.files:
            target = workspace.joinpath(*item.path.components)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(item.content)
        corpus = load_canonical_standards_corpus(workspace)
        impact = compile_policy_impact(workspace, corpus, DEFAULT_REGISTRY)
        horizon = load_coverage_horizon(workspace, corpus, impact)
        if (
            corpus.module_corpus.members != initial_corpus.module_corpus.members
            or corpus.policy_unit_corpus.sources
            != initial_corpus.policy_unit_corpus.sources
            or impact.input_sources != initial_impact.input_sources
            or horizon.input_sources != initial_horizon.input_sources
        ):
            raise _error(
                "COVERAGE.CAPTURE_CONTRADICTION",
                "captured coverage authority differs from discovery",
            )
        repository = AuthorityRepository(
            MemoryObjectStore(),
            (
                CodecSet("standards-authority", (CONTENT_SNAPSHOT_CODEC,)),
                METADATA_CODECS,
                POLICY_IMPACT_CODECS,
                graph_codecs,
                ANALYSIS_CODECS,
            ),
        )
        metadata_snapshot = repository.publish(
            CONTENT_SNAPSHOT_CODEC,
            _snapshot_subset(
                snapshot,
                {
                    CANONICAL_MODULE_CORPUS,
                    POLICY_UNIT_REGISTRY,
                    *corpus.module_corpus.members,
                    *corpus.policy_unit_corpus.sources,
                },
            ),
        )
        policy_snapshot = repository.publish(
            CONTENT_SNAPSHOT_CODEC,
            _snapshot_subset(snapshot, impact.input_sources),
        )
        horizon_snapshot = repository.publish(
            CONTENT_SNAPSHOT_CODEC,
            _snapshot_subset(snapshot, horizon.input_sources),
        )
        metadata = repository.publish(
            CANONICAL_STANDARDS_CORPUS_CODEC,
            CanonicalCorpusAuthority(metadata_snapshot.reference, corpus),
        )
        policy = repository.publish(
            COMPILED_POLICY_IMPACT_CODEC,
            CompiledPolicyImpactAuthority(
                policy_snapshot.reference, metadata.reference, impact
            ),
        )
        graph = repository.publish(
            graph_codec,
            build_graph(metadata.reference, policy.reference, corpus, impact),
        )
        horizon_handle = repository.publish(
            COVERAGE_HORIZON_CODEC,
            CoverageHorizonAuthority(
                horizon_snapshot.reference,
                metadata.reference,
                policy.reference,
                graph.reference,
                horizon,
            ),
        )
        definitions = compile_coverage_definitions(corpus, impact, horizon)
        coverage = publish_coverage_definitions(
            repository,
            definitions,
            metadata=metadata.reference,
            policy_impact=policy.reference,
            graph=graph.reference,
            horizon=horizon_handle.reference,
        )
        coverage = load_repository_coverage_authority(workspace, repository, coverage)
        return frozenset(
            subject
            for subject in coverage.subjects
            if coverage.certificate_for(subject) is not None
        )


def publish_coverage_definitions(
    repository: AuthorityRepository,
    definitions: CoverageDefinitionIndex,
    *,
    metadata: AuthorityReference,
    policy_impact: AuthorityReference,
    graph: AuthorityReference,
    horizon: AuthorityReference,
) -> CoverageAuthorityIndex:
    subjects = {}
    for subject, definition in definitions.views.items():
        requirement = definitions.requirements[subject]
        view_handle = repository.publish(
            COVERAGE_VIEW_CODEC,
            CoverageViewAuthority(
                metadata,
                policy_impact,
                graph,
                horizon,
                _view_projection(definition),
            ),
        )
        requirement_handle = repository.publish(
            COVERAGE_REQUIREMENT_CODEC,
            CoverageRequirementAuthority(
                view_handle.reference,
                _requirement_projection(requirement),
            ),
        )
        subjects[subject] = CoverageSubjectAuthority(
            definition,
            requirement,
            view_handle.reference,
            requirement_handle.reference,
            None,
            None,
        )
    return CoverageAuthorityIndex(
        definitions,
        subjects,
        definitions.input_sources,
    )


def publish_coverage_attestation(
    repository: AuthorityRepository,
    *,
    requirement: AuthorityReference,
    authorization: AuthorityReference,
    conclusion: str,
    evidence: Iterable[AuthorityEvidence],
    explicit_exclusions: Iterable[AuthorityEvidence],
    rationale: str,
    auditor_provenance: str,
) -> StoredCoverageAttestation:
    selected_evidence = tuple(sorted(evidence))
    selected_exclusions = tuple(sorted(explicit_exclusions))
    if conclusion != "complete" or not selected_evidence:
        raise _error(
            "COVERAGE.ATTESTATION_INVALID",
            "coverage attestations must be complete and carry evidence",
        )
    value = CoverageAttestationAuthority(
        requirement,
        authorization,
        _identity(
            {
                "conclusion": conclusion,
                "evidence": [_evidence_projection(item) for item in selected_evidence],
                "explicit_exclusions": [
                    _evidence_projection(item) for item in selected_exclusions
                ],
                "rationale": rationale,
                "auditor_provenance": auditor_provenance,
                "schema_version": 3,
            }
        ),
    )
    handle = repository.publish(COVERAGE_ATTESTATION_CODEC, value)
    return StoredCoverageAttestation(handle.reference, value)


def publish_coverage_certificate(
    repository: AuthorityRepository,
    subject: CoverageSubjectAuthority,
    attestation: StoredCoverageAttestation,
) -> AuthorityReference:
    if attestation.value.requirement != subject.requirement:
        raise _error(
            "COVERAGE.STALE_ATTESTATION",
            "attestation does not match the current coverage requirement",
            outcome="unavailable",
        )
    evidence = _projection(attestation.value.projection)["evidence"]
    certificate = CoverageCertificateAuthority(
        subject.view,
        subject.requirement,
        attestation.reference,
        _identity(
            {
                "subject": subject.definition.subject,
                "owner": subject.definition.owner,
                "semantic_revision": subject.definition.semantic_revision,
                "horizon_digest": subject.definition.horizon_digest,
                "relationship_digest": raw_digest(
                    analysis_key_bytes(
                        [
                            {"edge": edge, "fingerprint": fingerprint}
                            for edge, fingerprint in subject.definition.relationship_fingerprints
                        ]
                    )
                ),
                "evidence_digests": sorted(str(item["digest"]) for item in evidence),
                "provenance": {
                    "generator": "standards-analysis:consumer-coverage-certificate:v3"
                },
                "fact_schema_digest": subject.definition.fact_schema_digest,
            }
        ),
    )
    return repository.publish(COVERAGE_CERTIFICATE_CODEC, certificate).reference


def load_repository_coverage_authority(
    root: Path,
    repository: AuthorityRepository,
    index: CoverageAuthorityIndex,
    *,
    attestation_registry: str = DEFAULT_ATTESTATION_REGISTRY,
    authorization_authority: str = DEFAULT_AUTHORIZATION_AUTHORITY,
    revocations: str = DEFAULT_REVOCATIONS,
) -> CoverageAuthorityIndex:
    repo_root = root.resolve()
    authority = _load_authorization_authority(
        repo_root, authorization_authority, revocations
    )
    claims, claim_inputs = _load_claims(repo_root, attestation_registry)
    subjects = dict(index.subjects)
    seen_subjects: set[str] = set()
    for claim in claims:
        subject_id = claim["subject"]
        subject = subjects.get(subject_id)
        if subject is None:
            raise _error(
                "COVERAGE.UNKNOWN_SUBJECT",
                "coverage claim subject is not one active policy unit",
                path=claim["source"],
                observed=subject_id,
            )
        if not _claim_matches(claim, subject.definition):
            continue
        if subject_id in seen_subjects:
            raise _error(
                "COVERAGE.DUPLICATE_SUBJECT",
                "coverage subject has more than one current attestation",
                path=claim["source"],
                observed=subject_id,
            )
        if claim["auditor_provenance"] != authority.principal_id:
            raise _error(
                "COVERAGE.UNAUTHORIZED_PRINCIPAL",
                "attestation provenance is not authorized by repository authority",
                path=claim["source"],
                observed=claim["auditor_provenance"],
                outcome="unauthorized",
            )
        evidence = tuple(_repository_evidence(repo_root, path) for path in claim["evidence"])
        exclusions = tuple(
            _repository_evidence(repo_root, path)
            for path in claim["explicit_exclusions"]
        )
        grant_id = analysis_identity(
            "coding-standards:repository-coverage-grant-key:v1",
            "coverage-grant",
            {
                "issuer": authority.issuer_id,
                "principal": authority.principal_id,
                "requirement": subject.requirement.semantic_id,
                "capability": authority.capability,
            },
        )
        if grant_id in authority.revoked_grants:
            raise _error(
                "COVERAGE.AUTHORIZATION_REVOKED",
                "repository coverage authorization grant is revoked",
                path=revocations,
                observed=grant_id,
                outcome="unauthorized",
            )
        grant = AuthorizationGrant(
            authority.issuer_id,
            authority.issuer_semantic_revision,
            grant_id,
            authority.principal_id,
            authority.capability,
            "coverage-attestation",
            "coverage-requirement",
            subject.requirement.semantic_id,
            authority.authorization_evidence,
            authority.revocation_authority_id,
            authority.revocation_authority_semantic_revision,
            authority.revocation_evidence,
        )
        grant_ref = repository.publish(AUTHORIZATION_GRANT_CODEC, grant).reference
        attestation = publish_coverage_attestation(
            repository,
            requirement=subject.requirement,
            authorization=grant_ref,
            conclusion=claim["conclusion"],
            evidence=evidence,
            explicit_exclusions=exclusions,
            rationale=claim["rationale"],
            auditor_provenance=claim["auditor_provenance"],
        )
        certificate = publish_coverage_certificate(repository, subject, attestation)
        subjects[subject_id] = CoverageSubjectAuthority(
            subject.definition,
            subject.requirement_definition,
            subject.view,
            subject.requirement,
            attestation,
            certificate,
        )
        seen_subjects.add(subject_id)
    return CoverageAuthorityIndex(
        index.definitions,
        subjects,
        tuple(sorted({*index.input_sources, *authority.input_sources, *claim_inputs})),
    )


def _load_authorization_authority(
    root: Path,
    path: str,
    revocations_path: str,
) -> RepositoryAuthorizationAuthority:
    raw = _toml(root, path)
    _exact(
        raw,
        {
            "schema_version",
            "issuer_id",
            "issuer_semantic_revision",
            "principal_id",
            "capability",
            "authorization_evidence",
            "revocation_authority_id",
            "revocation_authority_semantic_revision",
            "revocations",
        },
        path,
        "authorization authority",
    )
    if raw["schema_version"] != 1 or raw["revocations"] != revocations_path:
        raise _error(
            "COVERAGE.AUTHORIZATION_VERSION",
            "unsupported or contradictory repository authorization authority",
            path=path,
        )
    revocations = _toml(root, revocations_path)
    _exact(
        revocations,
        {"schema_version", "authority_id", "semantic_revision", "revoked_grants"},
        revocations_path,
        "revocation authority",
    )
    if (
        revocations["schema_version"] != 1
        or revocations["authority_id"] != raw["revocation_authority_id"]
        or revocations["semantic_revision"]
        != raw["revocation_authority_semantic_revision"]
    ):
        raise _error(
            "COVERAGE.REVOCATION_AUTHORITY_MISMATCH",
            "revocation authority does not match authorization authority",
            path=revocations_path,
        )
    evidence_paths = _strings(raw["authorization_evidence"], path, "authorization_evidence")
    revoked = _strings(revocations["revoked_grants"], revocations_path, "revoked_grants", allow_empty=True)
    return RepositoryAuthorizationAuthority(
        _string(raw["issuer_id"], path, "issuer_id"),
        _positive_integer(raw["issuer_semantic_revision"], path, "issuer_semantic_revision"),
        _string(raw["principal_id"], path, "principal_id"),
        _string(raw["capability"], path, "capability"),
        tuple(_repository_evidence(root, item) for item in evidence_paths),
        _string(raw["revocation_authority_id"], path, "revocation_authority_id"),
        _positive_integer(
            raw["revocation_authority_semantic_revision"],
            path,
            "revocation_authority_semantic_revision",
        ),
        (_repository_evidence(root, revocations_path),),
        frozenset(revoked),
        tuple(sorted({path, revocations_path, *evidence_paths})),
    )


def _load_claims(root: Path, registry_path: str) -> tuple[tuple[dict[str, object], ...], tuple[str, ...]]:
    registry = _toml(root, registry_path)
    _exact(registry, {"schema_version", "sources"}, registry_path, "attestation registry")
    if registry["schema_version"] != 2:
        raise _error(
            "COVERAGE.ATTESTATION_VERSION",
            "unsupported repository attestation registry version",
            path=registry_path,
        )
    sources = _strings(registry["sources"], registry_path, "sources", allow_empty=True)
    claims = []
    inputs = {registry_path, *sources}
    for source_path in sources:
        raw = _toml(root, source_path)
        _exact(raw, {"schema_version", "attestations"}, source_path, "attestation source")
        if raw["schema_version"] != 4 or not isinstance(raw["attestations"], list):
            raise _error(
                "COVERAGE.ATTESTATION_VERSION",
                "unsupported repository attestation source version",
                path=source_path,
            )
        for item in raw["attestations"]:
            if not isinstance(item, dict):
                raise _error("COVERAGE.ATTESTATION", "attestation must be a table", path=source_path)
            _exact(
                item,
                {
                    "subject",
                    "semantic_revision",
                    "horizon_provider",
                    "horizon_version",
                    "relationship_kind_contract_version",
                    "applicability_language_version",
                    "coverage_evidence_contract",
                    "conclusion",
                    "evidence",
                    "explicit_exclusions",
                    "rationale",
                    "auditor_provenance",
                },
                source_path,
                "attestation",
            )
            evidence = _strings(item["evidence"], source_path, "evidence")
            exclusions = _strings(item["explicit_exclusions"], source_path, "explicit_exclusions", allow_empty=True)
            inputs.update(evidence)
            inputs.update(exclusions)
            claims.append(
                {
                    "source": source_path,
                    "subject": _string(item["subject"], source_path, "subject"),
                    "semantic_revision": _positive_integer(
                        item["semantic_revision"], source_path, "semantic_revision"
                    ),
                    "horizon_provider": _string(
                        item["horizon_provider"], source_path, "horizon_provider"
                    ),
                    "horizon_version": _positive_integer(
                        item["horizon_version"], source_path, "horizon_version"
                    ),
                    "relationship_kind_contract_version": _positive_integer(
                        item["relationship_kind_contract_version"],
                        source_path,
                        "relationship_kind_contract_version",
                    ),
                    "applicability_language_version": _positive_integer(
                        item["applicability_language_version"],
                        source_path,
                        "applicability_language_version",
                    ),
                    "coverage_evidence_contract": _string(
                        item["coverage_evidence_contract"],
                        source_path,
                        "coverage_evidence_contract",
                    ),
                    "conclusion": _string(item["conclusion"], source_path, "conclusion"),
                    "evidence": evidence,
                    "explicit_exclusions": exclusions,
                    "rationale": _string(item["rationale"], source_path, "rationale"),
                    "auditor_provenance": _string(item["auditor_provenance"], source_path, "auditor_provenance"),
                }
            )
    return tuple(claims), tuple(sorted(inputs))


def _claim_matches(
    claim: Mapping[str, object], definition: CoverageViewDefinition
) -> bool:
    return (
        claim["semantic_revision"] == definition.semantic_revision
        and claim["horizon_provider"] == definition.horizon_provider
        and claim["horizon_version"] == definition.horizon_version
        and claim["relationship_kind_contract_version"]
        == definition.relationship_kind_contract_version
        and claim["applicability_language_version"]
        == definition.applicability_language_version
        and claim["coverage_evidence_contract"] == COVERAGE_EVIDENCE_CONTRACT
    )


def _view_projection(value: CoverageViewDefinition) -> IdentityObject:
    return _identity(
        {
            "subject": value.subject,
            "owner": value.owner,
            "semantic_revision": value.semantic_revision,
            "representation_digest": value.representation_digest,
            "structural_digest": value.structural_digest,
            "relationship_kinds": list(value.relationship_kinds),
            "relationship_fingerprints": [
                {"edge": edge, "fingerprint": fingerprint}
                for edge, fingerprint in value.relationship_fingerprints
            ],
            "applicability_program_digests": list(value.applicability_program_digests),
            "fact_schema_digest": value.fact_schema_digest,
            "horizon": {
                "id": value.horizon_id,
                "provider": value.horizon_provider,
                "version": value.horizon_version,
                "digest": value.horizon_digest,
                "members": [item.as_projection() for item in value.horizon_members],
            },
        }
    )


def _requirement_projection(value: CoverageRequirementDefinition) -> IdentityObject:
    return _identity(
        {
            **value.as_projection(),
            "required_evidence_contract": COVERAGE_EVIDENCE_CONTRACT,
        }
    )


def _repository_evidence(root: Path, path: str) -> AuthorityEvidence:
    source = _repository_file(root, path)
    return AuthorityEvidence(
        "repository-content",
        "1",
        path,
        "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest(),
    )


def _evidence_projection(value: AuthorityEvidence) -> dict[str, str]:
    return {
        "id": value.id,
        "digest": value.digest,
        "provider_contract": value.provider_contract,
        "provider_contract_version": value.provider_contract_version,
    }


def _identity(value: Mapping[str, object]) -> IdentityObject:
    selected = analysis_key(value)
    assert isinstance(selected, IdentityObject)
    return selected


def _projection(value: IdentityObject) -> dict[str, object]:
    return {key: _plain(item) for key, item in value.members}


def _plain(value: object) -> object:
    if isinstance(value, IdentityObject):
        return {key: _plain(item) for key, item in value.members}
    if isinstance(value, IdentityArray):
        return [_plain(item) for item in value.values]
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _toml(root: Path, path: str) -> dict[str, object]:
    source = _repository_file(root, path)
    try:
        with source.open("rb") as handle:
            return tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        raise _error("COVERAGE.INVALID_TOML", str(error), path=path) from error


def _repository_file(root: Path, value: str) -> Path:
    logical = PurePosixPath(value)
    candidate = (root / Path(*logical.parts)).resolve(strict=False)
    if (
        not value
        or logical.is_absolute()
        or ".." in logical.parts
        or value.startswith("./")
        or str(logical) != value
        or not candidate.is_relative_to(root)
    ):
        raise _error("COVERAGE.PATH", "coverage path must be normalized and contained", path=value)
    if not candidate.is_file():
        raise _error(
            "COVERAGE.INPUT_UNAVAILABLE",
            "coverage input is unavailable",
            path=value,
            outcome="unavailable",
        )
    return candidate


def _exact(value: Mapping[str, object], fields: set[str], path: str, record: str) -> None:
    if set(value) != fields:
        observed = sorted(set(value) ^ fields)[0]
        raise _error(
            "COVERAGE.FIELDS",
            f"{record} fields are invalid",
            path=path,
            observed=observed,
        )


def _string(value: object, path: str, field: str) -> str:
    if type(value) is not str or not value:
        raise _error("COVERAGE.VALUE", "field must be a nonempty string", path=path, observed=field)
    return value


def _positive_integer(value: object, path: str, field: str) -> int:
    if type(value) is not int or value < 1:
        raise _error("COVERAGE.VALUE", "field must be a positive integer", path=path, observed=field)
    return value


def _strings(value: object, path: str, field: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or (not allow_empty and not value)
        or any(type(item) is not str or not item for item in value)
        or len(value) != len(set(value))
    ):
        raise _error("COVERAGE.VALUE", "field must contain unique nonempty strings", path=path, observed=field)
    return tuple(value)


def _repository_coverage_scope(
    root: Path,
    corpus: CanonicalStandardsCorpus,
    policy_inputs: Iterable[str],
    horizon_inputs: Iterable[str],
) -> tuple[str, ...]:
    registry = _toml(root, DEFAULT_ATTESTATION_REGISTRY)
    attestation_sources = tuple(registry.get("sources", ()))
    attestation_inputs = set(attestation_sources)
    for source_path in attestation_sources:
        if type(source_path) is not str:
            continue
        declaration = _toml(root, source_path)
        for attestation in declaration.get("attestations", ()):
            if not isinstance(attestation, Mapping):
                continue
            for field in ("evidence", "explicit_exclusions"):
                values = attestation.get(field, ())
                if isinstance(values, list):
                    attestation_inputs.update(
                        item for item in values if type(item) is str
                    )
    authorization = _toml(root, DEFAULT_AUTHORIZATION_AUTHORITY)
    authorization_inputs = {
        DEFAULT_AUTHORIZATION_AUTHORITY,
        str(authorization.get("revocations", DEFAULT_REVOCATIONS)),
        *(
            item
            for item in authorization.get("authorization_evidence", ())
            if type(item) is str
        ),
    }
    return tuple(
        sorted(
            {
                CANONICAL_MODULE_CORPUS,
                POLICY_UNIT_REGISTRY,
                DEFAULT_ATTESTATION_REGISTRY,
                *authorization_inputs,
                *corpus.module_corpus.members,
                *corpus.policy_unit_corpus.sources,
                *policy_inputs,
                *horizon_inputs,
                *attestation_inputs,
            }
        )
    )


def _snapshot_subset(
    snapshot: ContentSnapshot, paths: Iterable[str]
) -> ContentSnapshot:
    indexed = {str(item.path): item for item in snapshot.files}
    selected = tuple(sorted(set(paths)))
    missing = tuple(path for path in selected if path not in indexed)
    if missing:
        raise _error(
            "COVERAGE.CAPTURE_INCOMPLETE",
            "captured coverage snapshot omits an owner input",
            path=missing[0],
        )
    return ContentSnapshot(indexed[path] for path in selected)


def _error(
    code: str,
    message: str,
    *,
    path: str | None = None,
    observed: str | None = None,
    outcome: str = "invalid",
) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure(code, outcome, message, path=path, observed=observed)
    )


__all__ = (
    "CoverageAuthorityIndex",
    "CoverageSubjectAuthority",
    "COVERAGE_EVIDENCE_CONTRACT",
    "DEFAULT_ATTESTATION_REGISTRY",
    "DEFAULT_AUTHORIZATION_AUTHORITY",
    "DEFAULT_REVOCATIONS",
    "StoredCoverageAttestation",
    "covered_repository_policy_units",
    "load_repository_coverage_authority",
    "publish_coverage_attestation",
    "publish_coverage_certificate",
    "publish_coverage_definitions",
)
