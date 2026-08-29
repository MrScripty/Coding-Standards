from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

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
HORIZON_VERSION = 4
SUITE_INPUT_CONTRACT = "standards-verifier:suite-input-projection:v1"


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


def _repository_path(root: Path, value: str) -> Path:
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
    return candidate


def _repository_file(root: Path, value: str) -> Path:
    candidate = _repository_path(root, value)
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


def _json(root: Path, path: str) -> dict[str, Any]:
    source = _repository_file(root, path)
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError) as error:
        raise _error("COVERAGE.INVALID_JSON", str(error), path=path) from error
    if not isinstance(value, dict):
        raise _error(
            "COVERAGE.JSON_ROOT",
            "coverage JSON root must be an object",
            path=path,
        )
    return value


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


def _file_fingerprint(root: Path, path: str) -> str:
    return raw_digest(_repository_file(root, path).read_bytes())


def _suite_inputs(
    root: Path,
    projection_path: str,
    registry_path: str,
    registry_entries: list[object],
) -> tuple[tuple[str, str, str, object], ...]:
    projection = _json(root, projection_path)
    _exact(
        projection,
        required={"schema_version", "contract", "registry", "suites", "inputs"},
        allowed={"schema_version", "contract", "registry", "suites", "inputs"},
        path=projection_path,
        field="suite-input-projection",
    )
    if (
        type(projection["schema_version"]) is not int
        or projection["schema_version"] != 1
        or projection["contract"] != SUITE_INPUT_CONTRACT
    ):
        raise _error(
            "COVERAGE.SUITE_INPUT_VERSION",
            "suite-input projection contract is unsupported",
            path=projection_path,
        )

    registry = projection["registry"]
    if not isinstance(registry, dict):
        raise _error(
            "COVERAGE.SUITE_INPUT_REGISTRY",
            "suite-input registry binding must be an object",
            path=projection_path,
        )
    _exact(
        registry,
        required={"path", "digest"},
        allowed={"path", "digest"},
        path=projection_path,
        field="registry",
    )
    if (
        registry.get("path") != registry_path
        or registry.get("digest") != _file_fingerprint(root, registry_path)
    ):
        raise _error(
            "COVERAGE.SUITE_INPUT_STALE",
            "suite-input projection does not bind the current suite registry",
            path=projection_path,
            field="registry",
        )

    suites = projection["suites"]
    if not isinstance(suites, list) or len(suites) != len(registry_entries):
        raise _error(
            "COVERAGE.SUITE_INPUT_SUITES",
            "suite-input projection must bind every registered suite exactly once",
            path=projection_path,
        )
    expected_suites = []
    for entry in registry_entries:
        if not isinstance(entry, dict):
            raise _error(
                "COVERAGE.SUITE",
                "suite registration must be a table",
                path=registry_path,
            )
        suite_id = _text(entry.get("id"), path=registry_path, field="id")
        suite_path = _text(entry.get("path"), path=registry_path, field="path")
        expected_suites.append(
            {
                "id": suite_id,
                "path": suite_path,
                "digest": _file_fingerprint(root, suite_path),
            }
        )
    if suites != expected_suites:
        raise _error(
            "COVERAGE.SUITE_INPUT_STALE",
            "suite-input projection does not bind the current suite definitions",
            path=projection_path,
            field="suites",
        )

    inputs = projection["inputs"]
    if not isinstance(inputs, list):
        raise _error(
            "COVERAGE.SUITE_INPUTS",
            "suite-input projection inputs must be an array",
            path=projection_path,
        )
    resolved = []
    previous_path: str | None = None
    suite_ids = {item["id"] for item in expected_suites}
    for index, item in enumerate(inputs):
        field = f"inputs[{index}]"
        if not isinstance(item, dict):
            raise _error(
                "COVERAGE.SUITE_INPUT",
                "suite input must be an object",
                path=projection_path,
                field=field,
            )
        state = item.get("state")
        required = {"path", "state", "uses", "digest"}
        if state == "absent":
            required.remove("digest")
        _exact(
            item,
            required=required,
            allowed={"path", "state", "uses", "digest"},
            path=projection_path,
            field=field,
        )
        input_path = _text(item.get("path"), path=projection_path, field=field)
        if previous_path is not None and input_path <= previous_path:
            raise _error(
                "COVERAGE.SUITE_INPUT_ORDER",
                "suite inputs must be sorted and unique by path",
                path=projection_path,
                field=field,
            )
        previous_path = input_path
        if state not in {"present", "absent"}:
            raise _error(
                "COVERAGE.SUITE_INPUT_STATE",
                "suite input state must be present or absent",
                path=projection_path,
                field=field,
            )
        uses = item.get("uses")
        if not isinstance(uses, list) or not uses:
            raise _error(
                "COVERAGE.SUITE_INPUT_USE",
                "suite input must identify at least one owning check",
                path=projection_path,
                field=field,
            )
        normalized_uses = []
        for use in uses:
            if not isinstance(use, dict):
                raise _error(
                    "COVERAGE.SUITE_INPUT_USE",
                    "suite input use must be an object",
                    path=projection_path,
                    field=field,
                )
            _exact(
                use,
                required={"suite", "check", "role"},
                allowed={"suite", "check", "role"},
                path=projection_path,
                field=field,
            )
            suite = _text(use.get("suite"), path=projection_path, field=field)
            check = _text(use.get("check"), path=projection_path, field=field)
            role = _text(use.get("role"), path=projection_path, field=field)
            if suite not in suite_ids:
                raise _error(
                    "COVERAGE.SUITE_INPUT_USE",
                    "suite input use names an unregistered suite",
                    path=projection_path,
                    field=field,
                    observed=suite,
                )
            normalized_uses.append((suite, check, role))
        if normalized_uses != sorted(set(normalized_uses)):
            raise _error(
                "COVERAGE.SUITE_INPUT_USE_ORDER",
                "suite input uses must be sorted and unique",
                path=projection_path,
                field=field,
            )

        candidate = _repository_path(root, input_path)
        if state == "present":
            if not candidate.is_file():
                raise _error(
                    "COVERAGE.INPUT_UNAVAILABLE",
                    "required suite input is unavailable",
                    path=input_path,
                    unavailable=True,
                )
            digest = raw_digest(candidate.read_bytes())
            if item.get("digest") != digest:
                raise _error(
                    "COVERAGE.SUITE_INPUT_STALE",
                    "suite-input projection has a stale content digest",
                    path=projection_path,
                    field=field,
                    observed=input_path,
                )
        else:
            if candidate.exists() or candidate.is_symlink():
                raise _error(
                    "COVERAGE.SUITE_INPUT_ABSENCE",
                    "suite input asserted absent is present",
                    path=input_path,
                )
            digest = _digest(
                {
                    "path": input_path,
                    "state": "absent",
                    "uses": normalized_uses,
                }
            )
        resolved.append((input_path, state, digest, normalized_uses))
    return tuple(resolved)


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
    registry_entries = suite_registry.get("suites", [])
    if not isinstance(registry_entries, list):
        raise _error(
            "COVERAGE.SUITE",
            "suite registry suites must be an array",
            path=suite_registry_path,
        )
    for entry in registry_entries:
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
    suite_inputs_path = _text(
        raw["suite_inputs"], path=path, field="suite_inputs"
    )
    input_sources.add(suite_inputs_path)
    _merge_member(
        members,
        f"repository:{suite_inputs_path}",
        "suite-input-projection",
        _file_fingerprint(repo_root, suite_inputs_path),
    )
    for input_path, state, fingerprint, _uses in _suite_inputs(
        repo_root,
        suite_inputs_path,
        suite_registry_path,
        registry_entries,
    ):
        if state == "present":
            input_sources.add(input_path)
            _merge_member(
                members,
                f"repository:{input_path}",
                "registered-suite-input",
                fingerprint,
            )
        else:
            _merge_member(
                members,
                f"repository-state:{input_path}",
                "registered-suite-input-absence",
                fingerprint,
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
