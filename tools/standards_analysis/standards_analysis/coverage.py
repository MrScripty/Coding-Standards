from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from tools.standards_applicability.standards_applicability import LANGUAGE_VERSION
from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    PolicyUnit,
)
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
)

from .errors import AnalysisError, AnalysisFailure
from .keys import analysis_key_bytes, raw_digest


DEFAULT_HORIZON = "evaluation/standards-effectiveness/policy-coverage/horizons.toml"
HORIZON_ID = "audit-horizon.policy-impact-consumers"
HORIZON_PROVIDER = "standards-analysis:policy-impact-consumer-horizon"
HORIZON_VERSION = 3


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
    return raw_digest(_repository_file(root, path).read_bytes())


def load_coverage_horizon(
    root: Path,
    corpus: CanonicalStandardsCorpus,
    compiled: CompiledPolicyImpactSet,
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
        },
        allowed={
            "schema_version",
            "id",
            "provider",
            "version",
            "suite_registry",
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
                _file_fingerprint(repo_root, source_path),
            )

    suite_registry_path = _text(
        raw["suite_registry"], path=path, field="suite_registry"
    )
    input_sources.add(suite_registry_path)
    suite_registry = _toml(repo_root, suite_registry_path)
    for entry in suite_registry.get("suites", []):
        if not isinstance(entry, dict):
            raise _error(
                "COVERAGE.SUITE",
                "suite registration must be a table",
                path=suite_registry_path,
            )
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
            _digest(
                {
                    "registration": entry,
                    "content": _file_fingerprint(repo_root, suite_path),
                }
            ),
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
                    "content": _file_fingerprint(repo_root, artifact.repository_path),
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
        horizon.digest,
        horizon.members,
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
        subject: derive_coverage_requirement(view)
        for subject, view in views.items()
    }
    return CoverageDefinitionIndex(
        horizon,
        views,
        requirements,
        horizon.input_sources,
    )


__all__ = (
    "CoverageDefinitionIndex",
    "CoverageHorizon",
    "CoverageHorizonMember",
    "CoverageRequirementDefinition",
    "CoverageViewDefinition",
    "DEFAULT_HORIZON",
    "HORIZON_ID",
    "HORIZON_PROVIDER",
    "compile_coverage_definitions",
    "derive_coverage_requirement",
    "derive_coverage_view",
    "load_coverage_horizon",
)
