from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    PolicyUnit,
    PolicyUnitCorpus,
    canonical_json_bytes,
    digest_bytes,
)
from tools.standards_policy_impact.standards_policy_impact import (
    RELATIONSHIP_KIND_CONTRACT_VERSION,
    CompiledPolicyImpactSet,
)

from .errors import AnalysisError, AnalysisFailure
from .serialization import identity


COVERAGE_CONTRACT_VERSION = "1"
ATTESTATION_CONTRACT_VERSION = "1"
AUTHORIZATION_CONTRACT_VERSION = "repository-reviewed-attestation:v1"
EVIDENCE_PROVIDER_CONTRACT_VERSION = "repository-content:v1"
IDENTITY_RESOLUTION_CONTRACT_VERSION = "standards-metadata:v1"
DEFAULT_HORIZON = "evaluation/standards-effectiveness/policy-coverage/horizons.toml"
DEFAULT_ATTESTATION_REGISTRY = (
    "evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml"
)
HORIZON_ID = "audit-horizon.policy-impact-consumers"
HORIZON_PROVIDER = "standards-analysis:policy-impact-consumer-horizon"


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
        raise _error(
            "COVERAGE.PATH",
            "coverage inputs must be normalized contained repository paths",
            path=value,
        )
    if not candidate.is_file():
        raise _error(
            "COVERAGE.INPUT_UNAVAILABLE",
            "coverage input is unavailable",
            path=value,
            unavailable=True,
        )
    return candidate


def _toml(root: Path, path: str) -> dict[str, Any]:
    source = _repository_file(root, path)
    try:
        with source.open("rb") as handle:
            return tomllib.load(handle)
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
    return digest_bytes(canonical_json_bytes(value))


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


@dataclass(frozen=True, slots=True)
class CoverageEvidence:
    id: str
    digest: str
    provider_contract_version: str = EVIDENCE_PROVIDER_CONTRACT_VERSION

    def as_projection(self) -> dict[str, str]:
        return {
            "id": self.id,
            "digest": self.digest,
            "provider_contract_version": self.provider_contract_version,
        }


@dataclass(frozen=True, slots=True)
class CoverageAuthorityView:
    handle: str
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
    identity_resolution_contract_version: str
    coverage_contract_version: str
    attestation_contract_version: str
    authorization_contract_version: str
    evidence_provider_contract_version: str

    def as_identity_projection(self) -> dict[str, object]:
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
            "applicability_program_digests": list(
                self.applicability_program_digests
            ),
            "fact_schema_digest": self.fact_schema_digest,
            "horizon": {
                "id": self.horizon_id,
                "provider": self.horizon_provider,
                "version": self.horizon_version,
                "digest": self.horizon_digest,
                "members": [member.as_projection() for member in self.horizon_members],
            },
            "identity_resolution_contract_version": self.identity_resolution_contract_version,
            "coverage_contract_version": self.coverage_contract_version,
            "attestation_contract_version": self.attestation_contract_version,
            "authorization_contract_version": self.authorization_contract_version,
            "evidence_provider_contract_version": self.evidence_provider_contract_version,
        }

    def as_projection(self) -> dict[str, object]:
        value = self.as_identity_projection()
        value.update(
            {
                "kind": "coverage-authority-view",
                "handle": {
                    "kind": "coverage-authority-view-handle",
                    "id": self.handle,
                    "schema_version": 1,
                },
            }
        )
        return value


@dataclass(frozen=True, slots=True)
class CoverageAuditRequirement:
    handle: str
    coverage_view: str
    subject: str
    owner: str
    semantic_revision: int
    relationship_kinds: tuple[str, ...]
    horizon: str
    derived_from_snapshot: str | None = None

    def as_projection(self) -> dict[str, object]:
        value: dict[str, object] = {
            "kind": "coverage-audit-requirement",
            "handle": {
                "kind": "coverage-requirement-handle",
                "id": self.handle,
                "schema_version": 1,
            },
            "coverage_view": {
                "kind": "coverage-authority-view-handle",
                "id": self.coverage_view,
                "schema_version": 1,
            },
            "subject": self.subject,
            "owner": self.owner,
            "semantic_revision": self.semantic_revision,
            "relationship_kinds": list(self.relationship_kinds),
            "horizon": self.horizon,
        }
        if self.derived_from_snapshot is not None:
            value["derived_from_snapshot"] = {
                "kind": "snapshot-handle",
                "id": self.derived_from_snapshot,
                "schema_version": 1,
            }
        return value


@dataclass(frozen=True, slots=True)
class CoverageAttestation:
    handle: str
    requirement: str
    conclusion: str
    evidence: tuple[CoverageEvidence, ...]
    explicit_exclusions: tuple[CoverageEvidence, ...]
    rationale: str
    auditor_provenance: str
    schema_version: int
    source: str

    def as_projection(self) -> dict[str, object]:
        return {
            "kind": "coverage-attestation",
            "handle": {
                "kind": "coverage-attestation-handle",
                "id": self.handle,
                "schema_version": 1,
            },
            "requirement": {
                "kind": "coverage-requirement-handle",
                "id": self.requirement,
                "schema_version": 1,
            },
            "conclusion": self.conclusion,
            "evidence": [item.as_projection() for item in self.evidence],
            "explicit_exclusions": [
                item.as_projection() for item in self.explicit_exclusions
            ],
            "rationale": self.rationale,
            "auditor_provenance": self.auditor_provenance,
            "schema_version": self.schema_version,
        }


@dataclass(frozen=True, slots=True)
class ConsumerCoverageCertificate:
    handle: str
    coverage_view: str
    requirement: str
    attestation: str
    subject: str
    owner: str
    semantic_revision: int
    horizon_digest: str
    relationship_digest: str
    evidence_digests: tuple[str, ...]
    coverage_contract_version: str
    attestation_contract_version: str

    def as_projection(self) -> dict[str, object]:
        return {
            "kind": "consumer-coverage-certificate",
            "handle": {
                "kind": "certificate-handle",
                "id": self.handle,
                "schema_version": 1,
            },
            "coverage_view": {
                "kind": "coverage-authority-view-handle",
                "id": self.coverage_view,
                "schema_version": 1,
            },
            "requirement": {
                "kind": "coverage-requirement-handle",
                "id": self.requirement,
                "schema_version": 1,
            },
            "attestation": {
                "kind": "coverage-attestation-handle",
                "id": self.attestation,
                "schema_version": 1,
            },
            "subject": self.subject,
            "owner": self.owner,
            "semantic_revision": self.semantic_revision,
            "horizon_digest": self.horizon_digest,
            "relationship_digest": self.relationship_digest,
            "evidence_digests": list(self.evidence_digests),
            "coverage_contract_version": self.coverage_contract_version,
            "attestation_contract_version": self.attestation_contract_version,
            "provenance": {
                "generator": "standards-analysis:consumer-coverage-certificate:v1",
                "generated_at": "reproducible-build-provenance",
            },
        }


@dataclass(frozen=True, slots=True)
class CoverageIndex:
    horizon: CoverageHorizon
    views: Mapping[str, CoverageAuthorityView]
    requirements: Mapping[str, CoverageAuditRequirement]
    attestations: Mapping[str, CoverageAttestation]
    certificates: Mapping[str, ConsumerCoverageCertificate]
    input_sources: tuple[str, ...]

    def __post_init__(self) -> None:
        for field in ("views", "requirements", "attestations", "certificates"):
            object.__setattr__(
                self,
                field,
                MappingProxyType(dict(sorted(getattr(self, field).items()))),
            )

    def certificate_for(self, policy_unit: str) -> ConsumerCoverageCertificate | None:
        return self.certificates.get(policy_unit)

    def uncovered_for_module(
        self,
        corpus: CanonicalStandardsCorpus,
        module_id: str,
    ) -> tuple[str, ...]:
        return tuple(
            unit.id
            for unit in corpus.policy_unit_corpus.for_module(module_id)
            if unit.id not in self.certificates
        )

    def uncovered_for_module_corpus(
        self,
        corpus: PolicyUnitCorpus,
        module_id: str,
    ) -> tuple[str, ...]:
        return tuple(
            unit.id
            for unit in corpus.for_module(module_id)
            if unit.id not in self.certificates
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


def _path_values(value: object) -> Iterable[str]:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key == "path" and isinstance(item, str):
                yield item
            yield from _path_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from _path_values(item)


def _file_fingerprint(root: Path, path: str) -> str:
    return digest_bytes(_repository_file(root, path).read_bytes())


def load_coverage_horizon(
    root: Path,
    corpus: CanonicalStandardsCorpus,
    path: str = DEFAULT_HORIZON,
) -> CoverageHorizon:
    repo_root = root.resolve()
    raw = _toml(repo_root, path)
    _exact(
        raw,
        required={
            "schema_version",
            "id",
            "provider",
            "version",
            "suite_registry",
            "edge_source_registry",
            "policy_impact_node_catalog",
        },
        allowed={
            "schema_version",
            "id",
            "provider",
            "version",
            "suite_registry",
            "edge_source_registry",
            "policy_impact_node_catalog",
        },
        path=path,
        field="horizon",
    )
    if raw["schema_version"] != 1 or raw["version"] != 1:
        raise _error("COVERAGE.HORIZON_VERSION", "unsupported horizon version", path=path)
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
            _file_fingerprint(repo_root, module.path),
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
    edge_registry = _toml(repo_root, edge_registry_path)
    for source in edge_registry.get("sources", []):
        if not isinstance(source, dict):
            raise _error("COVERAGE.EDGE_SOURCE", "edge source must be a table", path=edge_registry_path)
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
                _file_fingerprint(repo_root, source_path),
            )

    suite_registry_path = _text(
        raw["suite_registry"], path=path, field="suite_registry"
    )
    input_sources.add(suite_registry_path)
    suite_registry = _toml(repo_root, suite_registry_path)
    for entry in suite_registry.get("suites", []):
        if not isinstance(entry, dict):
            raise _error("COVERAGE.SUITE", "suite registration must be a table", path=suite_registry_path)
        suite_id = _text(entry.get("id"), path=suite_registry_path, field="id")
        suite_path = _text(entry.get("path"), path=suite_registry_path, field="path")
        input_sources.add(suite_path)
        suite_raw = _toml(repo_root, suite_path)
        if suite_raw.get("id") != suite_id:
            raise _error(
                "COVERAGE.SUITE_ID",
                "registered suite identity does not match its source",
                path=suite_path,
                observed=str(suite_raw.get("id")),
            )
        _merge_member(
            members,
            f"suite:{suite_id}",
            "registered-suite",
            _digest({"registration": entry, "content": _file_fingerprint(repo_root, suite_path)}),
        )
        _merge_member(
            members,
            f"repository:{suite_path}",
            "suite-definition",
            _file_fingerprint(repo_root, suite_path),
        )
        for input_path in sorted(set(_path_values(suite_raw))):
            input_sources.add(input_path)
            _merge_member(
                members,
                f"repository:{input_path}",
                "registered-suite-input",
                _file_fingerprint(repo_root, input_path),
            )

    node_catalog_path = _text(
        raw["policy_impact_node_catalog"],
        path=path,
        field="policy_impact_node_catalog",
    )
    input_sources.add(node_catalog_path)
    node_catalog = _toml(repo_root, node_catalog_path)
    for node in node_catalog.get("nodes", []):
        if not isinstance(node, dict):
            raise _error("COVERAGE.NODE", "policy-impact node must be a table", path=node_catalog_path)
        node_id = _text(node.get("id"), path=node_catalog_path, field="id")
        metadata = node.get("metadata", {})
        repository_path = metadata.get("repository_path") if isinstance(metadata, dict) else None
        fingerprint = (
            _file_fingerprint(repo_root, repository_path)
            if isinstance(repository_path, str)
            else _digest(node)
        )
        _merge_member(
            members,
            f"policy-impact-node:{node_id}",
            "supplemental-policy-impact-node",
            fingerprint,
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
    return CoverageHorizon(
        horizon_id,
        provider,
        raw["version"],
        resolved,
        horizon_digest,
        tuple(sorted(input_sources)),
    )


def derive_coverage_view(
    unit: PolicyUnit,
    compiled: CompiledPolicyImpactSet,
    horizon: CoverageHorizon,
    *,
    semantic_revision: int | None = None,
    representation_digest: str | None = None,
    structural_digest: str | None = None,
) -> CoverageAuthorityView:
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
    projection = {
        "subject": unit.id,
        "owner": unit.module,
        "semantic_revision": semantic_revision or unit.semantic_revision,
        "representation_digest": representation_digest or unit.representation_digest,
        "structural_digest": structural_digest or unit.structural_digest,
        "relationships": [
            {
                "edge": edge,
                "fingerprint": fingerprint,
                "kind": relation,
                "program": program,
            }
            for edge, fingerprint, relation, program in relationships
        ],
        "relationship_kind_contract_version": RELATIONSHIP_KIND_CONTRACT_VERSION,
        "relationship_provider_contract_digest": compiled.provider_contract_digest,
        "applicability_language_version": 1,
        "fact_schema_digest": compiled.fact_schema.digest,
        "horizon": {
            "id": horizon.id,
            "provider": horizon.provider,
            "version": horizon.version,
            "digest": horizon.digest,
            "members": [member.as_projection() for member in horizon.members],
        },
        "identity_resolution_contract_version": IDENTITY_RESOLUTION_CONTRACT_VERSION,
        "coverage_contract_version": COVERAGE_CONTRACT_VERSION,
        "attestation_contract_version": ATTESTATION_CONTRACT_VERSION,
        "authorization_contract_version": AUTHORIZATION_CONTRACT_VERSION,
        "evidence_provider_contract_version": EVIDENCE_PROVIDER_CONTRACT_VERSION,
    }
    handle = identity(
        "coding-standards:coverage-authority-view:v1",
        "coverage-view",
        projection,
    )
    return CoverageAuthorityView(
        handle,
        unit.id,
        unit.module,
        semantic_revision or unit.semantic_revision,
        representation_digest or unit.representation_digest,
        structural_digest or unit.structural_digest,
        tuple(sorted({relationship[2] for relationship in relationships})),
        tuple((relationship[0], relationship[1]) for relationship in relationships),
        RELATIONSHIP_KIND_CONTRACT_VERSION,
        compiled.provider_contract_digest,
        1,
        tuple(sorted({relationship[3] for relationship in relationships})),
        compiled.fact_schema.digest,
        horizon.id,
        horizon.provider,
        horizon.version,
        horizon.digest,
        horizon.members,
        IDENTITY_RESOLUTION_CONTRACT_VERSION,
        COVERAGE_CONTRACT_VERSION,
        ATTESTATION_CONTRACT_VERSION,
        AUTHORIZATION_CONTRACT_VERSION,
        EVIDENCE_PROVIDER_CONTRACT_VERSION,
    )


def derive_coverage_requirement(
    view: CoverageAuthorityView,
    *,
    derived_from_snapshot: str | None = None,
) -> CoverageAuditRequirement:
    value = {
        "coverage_view": view.handle,
        "subject": view.subject,
        "owner": view.owner,
        "semantic_revision": view.semantic_revision,
        "relationship_kinds": list(view.relationship_kinds),
        "horizon": view.horizon_id,
    }
    handle = identity(
        "coding-standards:coverage-audit-requirement:v1",
        "coverage-requirement",
        value,
    )
    return CoverageAuditRequirement(
        handle,
        view.handle,
        view.subject,
        view.owner,
        view.semantic_revision,
        view.relationship_kinds,
        view.horizon_id,
        derived_from_snapshot,
    )


def _load_attestations(
    root: Path,
    path: str,
) -> tuple[tuple[CoverageAttestation, ...], tuple[str, ...]]:
    registry = _toml(root, path)
    _exact(
        registry,
        required={"schema_version", "sources"},
        allowed={"schema_version", "sources"},
        path=path,
        field="registry",
    )
    if registry["schema_version"] != 1:
        raise _error("COVERAGE.ATTESTATION_VERSION", "unsupported attestation registry version", path=path)
    sources = _texts(registry["sources"], path=path, field="sources", allow_empty=True)
    result: list[CoverageAttestation] = []
    input_sources = {path}
    seen: set[str] = set()
    for source_path in sources:
        input_sources.add(source_path)
        raw = _toml(root, source_path)
        _exact(
            raw,
            required={"schema_version", "attestations"},
            allowed={"schema_version", "attestations"},
            path=source_path,
            field="source",
        )
        if raw["schema_version"] != 1 or not isinstance(raw["attestations"], list):
            raise _error("COVERAGE.ATTESTATION_VERSION", "unsupported attestation source version", path=source_path)
        for item in raw["attestations"]:
            if not isinstance(item, dict):
                raise _error("COVERAGE.ATTESTATION", "attestation must be a table", path=source_path)
            _exact(
                item,
                required={
                    "requirement",
                    "conclusion",
                    "evidence",
                    "explicit_exclusions",
                    "rationale",
                    "auditor_provenance",
                },
                allowed={
                    "requirement",
                    "conclusion",
                    "evidence",
                    "explicit_exclusions",
                    "rationale",
                    "auditor_provenance",
                },
                path=source_path,
                field="attestation",
            )
            conclusion = _text(item["conclusion"], path=source_path, field="conclusion")
            if conclusion != "complete":
                raise _error("COVERAGE.ATTESTATION_CONCLUSION", "only complete attestations can certify coverage", path=source_path)
            evidence_paths = _texts(
                item["evidence"], path=source_path, field="evidence"
            )
            exclusion_paths = _texts(
                item["explicit_exclusions"],
                path=source_path,
                field="explicit_exclusions",
                allow_empty=True,
            )
            input_sources.update(evidence_paths)
            input_sources.update(exclusion_paths)
            evidence = tuple(
                CoverageEvidence(path, _file_fingerprint(root, path))
                for path in evidence_paths
            )
            exclusions = tuple(
                CoverageEvidence(path, _file_fingerprint(root, path))
                for path in exclusion_paths
            )
            content = {
                "requirement": _text(item["requirement"], path=source_path, field="requirement"),
                "conclusion": conclusion,
                "evidence": [reference.as_projection() for reference in evidence],
                "explicit_exclusions": [
                    reference.as_projection() for reference in exclusions
                ],
                "rationale": _text(item["rationale"], path=source_path, field="rationale"),
                "auditor_provenance": _text(item["auditor_provenance"], path=source_path, field="auditor_provenance"),
                "schema_version": raw["schema_version"],
            }
            handle = identity(
                "coding-standards:coverage-attestation:v1",
                "coverage-attestation",
                content,
            )
            if handle in seen:
                raise _error("COVERAGE.DUPLICATE_ATTESTATION", "attestation content is duplicated", path=source_path, observed=handle)
            seen.add(handle)
            result.append(
                CoverageAttestation(
                    handle,
                    content["requirement"],
                    conclusion,
                    evidence,
                    exclusions,
                    content["rationale"],
                    content["auditor_provenance"],
                    raw["schema_version"],
                    source_path,
                )
            )
    return tuple(result), tuple(sorted(input_sources))


def _certificate(
    view: CoverageAuthorityView,
    requirement: CoverageAuditRequirement,
    attestation: CoverageAttestation,
) -> ConsumerCoverageCertificate:
    evidence_digests = tuple(sorted(item.digest for item in attestation.evidence))
    relationship_digest = _digest(
        [
            {"edge": edge, "fingerprint": fingerprint}
            for edge, fingerprint in view.relationship_fingerprints
        ]
    )
    value = {
        "coverage_view": view.handle,
        "requirement": requirement.handle,
        "attestation": attestation.handle,
        "subject": view.subject,
        "owner": view.owner,
        "semantic_revision": view.semantic_revision,
        "horizon_digest": view.horizon_digest,
        "relationship_digest": relationship_digest,
        "evidence_digests": list(evidence_digests),
        "coverage_contract_version": COVERAGE_CONTRACT_VERSION,
        "attestation_contract_version": ATTESTATION_CONTRACT_VERSION,
    }
    return ConsumerCoverageCertificate(
        identity(
            "coding-standards:consumer-coverage-certificate:v1",
            "certificate",
            value,
        ),
        view.handle,
        requirement.handle,
        attestation.handle,
        view.subject,
        view.owner,
        view.semantic_revision,
        view.horizon_digest,
        relationship_digest,
        evidence_digests,
        COVERAGE_CONTRACT_VERSION,
        ATTESTATION_CONTRACT_VERSION,
    )


def compile_coverage(
    root: Path,
    corpus: CanonicalStandardsCorpus,
    compiled: CompiledPolicyImpactSet,
    *,
    horizon_path: str = DEFAULT_HORIZON,
    attestation_registry_path: str = DEFAULT_ATTESTATION_REGISTRY,
    derived_from_snapshot: str | None = None,
) -> CoverageIndex:
    repo_root = root.resolve()
    horizon = load_coverage_horizon(repo_root, corpus, horizon_path)
    views = {
        unit.id: derive_coverage_view(unit, compiled, horizon)
        for unit in corpus.policy_units
    }
    requirements = {
        unit_id: derive_coverage_requirement(
            view,
            derived_from_snapshot=derived_from_snapshot,
        )
        for unit_id, view in views.items()
    }
    attestations, attestation_inputs = _load_attestations(
        repo_root,
        attestation_registry_path,
    )
    by_requirement = {requirement.handle: unit_id for unit_id, requirement in requirements.items()}
    certificates: dict[str, ConsumerCoverageCertificate] = {}
    attestation_index: dict[str, CoverageAttestation] = {}
    for attestation in attestations:
        unit_id = by_requirement.get(attestation.requirement)
        if unit_id is None:
            raise _error(
                "COVERAGE.STALE_ATTESTATION",
                "attestation does not match a current coverage requirement",
                path=attestation.source,
                observed=attestation.requirement,
                unavailable=True,
            )
        if unit_id in certificates:
            raise _error(
                "COVERAGE.DUPLICATE_SUBJECT",
                "coverage subject has more than one current attestation",
                path=attestation.source,
                observed=unit_id,
            )
        attestation_index[attestation.handle] = attestation
        certificates[unit_id] = _certificate(
            views[unit_id],
            requirements[unit_id],
            attestation,
        )
    return CoverageIndex(
        horizon,
        views,
        requirements,
        attestation_index,
        certificates,
        tuple(sorted({*horizon.input_sources, *attestation_inputs})),
    )
