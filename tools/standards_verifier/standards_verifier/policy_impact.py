from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping

from tools.graph_engine.graph_engine import EdgeRegistry, GraphError
from tools.graph_engine.graph_engine.manifest import ManifestSource
from tools.standards_applicability.standards_applicability import ApplicabilityProgram
from tools.standards_graph.standards_graph import metadata_dependency_source
from tools.standards_metadata.standards_metadata import (
    MetadataError,
    load_canonical_module_corpus,
    load_module_metadata,
)
from tools.standards_policy_impact.standards_policy_impact import (
    CATALOG_SOURCE_ID,
    CompiledPolicyImpactSet,
    PolicyImpactError,
    PolicyImpactSource,
    compile_policy_impact,
)

from .diagnostics import Diagnostic, EngineError
from .paths import contained_file


POLICY_GROUP = "policy-impact"
DEFAULT_SOURCE_REGISTRY = "evaluation/standards-effectiveness/edge-source-registry.toml"
DEFAULT_POLICY_REGISTRY = "evaluation/standards-effectiveness/policy-impact-registry.toml"


@dataclass(frozen=True, slots=True)
class ImpactEdge:
    edge_id: str
    owner: str
    consumer: str
    relation: str
    applicability_program: ApplicabilityProgram
    evidence_owner: str


@dataclass(frozen=True, slots=True)
class PolicyImpactAdapter:
    registry: EdgeRegistry
    compiled: CompiledPolicyImpactSet

    @property
    def audited_owners(self) -> frozenset[str]:
        return self.compiled.audited_owners

    def consumers_for(self, owner: str) -> tuple[ImpactEdge, ...]:
        if owner not in self.audited_owners:
            raise EngineError(
                Diagnostic(
                    "POLICY_IMPACT.OWNER_NOT_AUDITED",
                    "unavailable",
                    "policy owner has no audited semantic-impact coverage",
                    observed=owner,
                )
            )
        return tuple(
            sorted(
                (
                    _impact_edge(self.registry, self.compiled, view.edge.id)
                    for view in self.registry.outgoing(owner, (POLICY_GROUP,))
                ),
                key=lambda edge: (edge.consumer, edge.relation, edge.edge_id),
            )
        )


def _diagnostic(
    code: str,
    message: str,
    *,
    path: str | None = None,
    field: str | None = None,
    observed: str | None = None,
    suite: str | None = None,
    check: str | None = None,
    unavailable: bool = False,
) -> EngineError:
    return EngineError(
        Diagnostic(
            code,
            "unavailable" if unavailable else "invalid",
            message,
            suite=suite,
            check=check,
            path=path,
            field=field,
            observed=observed,
        )
    )


def _translate_policy_error(
    error: PolicyImpactError,
    *,
    suite: str,
    check: str,
) -> EngineError:
    failure = error.failure
    return _diagnostic(
        failure.code,
        failure.message,
        path=failure.path,
        field=failure.field,
        observed=failure.observed,
        suite=suite,
        check=check,
        unavailable=failure.outcome == "unavailable",
    )


def _repository_path(registry: EdgeRegistry, node_id: str, source_path: str) -> str:
    node = registry.nodes[node_id]
    value = node.metadata.get("repository_path")
    if not value:
        raise _diagnostic(
            "POLICY_IMPACT.UNKNOWN_CONSUMER",
            "policy-impact nodes require one repository_path",
            path=source_path,
            field="repository_path",
            observed=node_id,
        )
    return value


def _impact_edge(
    registry: EdgeRegistry,
    compiled: CompiledPolicyImpactSet,
    edge_id: str,
) -> ImpactEdge:
    edge = registry.edge(edge_id)
    semantics = compiled.semantics_for(edge_id)
    return ImpactEdge(
        edge.id,
        edge.source,
        _repository_path(registry, edge.target, semantics.declaration_source),
        edge.relation,
        semantics.applicability_program,
        semantics.evidence_owner,
    )


def _load_module(root: Path, path: str, *, suite: str, check: str):
    try:
        return load_module_metadata(root, path)
    except MetadataError as error:
        failure = error.failure
        raise _diagnostic(
            failure.code,
            failure.message,
            path=failure.path,
            field=failure.field,
            observed=failure.observed,
            suite=suite,
            check=check,
            unavailable=failure.outcome == "unavailable",
        ) from error


def _validate_consumer(
    root: Path,
    edge: ImpactEdge,
    suite_paths: Mapping[str, str],
    *,
    suite: str,
    check: str,
) -> None:
    contained_file(root, edge.consumer, suite=suite, check=check)
    path = PurePosixPath(edge.consumer)
    valid = False
    if edge.relation == "normative-consumer":
        _load_module(root, edge.consumer, suite=suite, check=check)
        valid = True
    elif edge.relation == "router-projection":
        valid = _load_module(root, edge.consumer, suite=suite, check=check).module_id == "router"
    elif edge.relation == "prompt-projection":
        valid = path.parts[:1] == ("prompts",) and path.suffix == ".md"
    elif edge.relation == "template-projection":
        valid = path.parts[:1] == ("templates",) and path.suffix == ".md"
    elif edge.relation == "reference-projection":
        valid = path.parts[:1] == ("reference",) and path.suffix == ".md"
    elif edge.relation == "documentation-projection":
        valid = path.suffix == ".md"
    elif edge.relation == "fixture-projection":
        valid = path.parts[:3] == (
            "evaluation",
            "standards-effectiveness",
            "fixtures",
        )
    elif edge.relation == "enforcement-suite-projection":
        valid = edge.consumer in set(suite_paths.values())
    if not valid:
        raise _diagnostic(
            "POLICY_IMPACT.UNKNOWN_CONSUMER",
            "consumer does not resolve for its declared semantic relation",
            path=edge.consumer,
            field="consumer",
            observed=edge.consumer,
            suite=suite,
            check=check,
        )


def _suite_owners(
    root: Path,
    suite_paths: Mapping[str, str],
    *,
    suite: str,
    check: str,
) -> dict[str, str]:
    owners: dict[str, str] = {}
    for suite_id, suite_path in suite_paths.items():
        source = contained_file(root, suite_path, suite=suite, check=check)
        try:
            with source.open("rb") as handle:
                raw = tomllib.load(handle)
        except tomllib.TOMLDecodeError as error:
            raise _diagnostic(
                "POLICY_IMPACT.INVALID_TOML",
                str(error),
                path=suite_path,
                suite=suite,
                check=check,
            ) from error
        if raw.get("id") != suite_id:
            raise _diagnostic(
                "POLICY_IMPACT.SUITE_ID",
                "registered suite ID does not match its suite file",
                path=suite_path,
                field="id",
                observed=str(raw.get("id")),
                suite=suite,
                check=check,
            )
        owner = raw.get("owner")
        if not isinstance(owner, str) or not owner:
            raise _diagnostic(
                "POLICY_IMPACT.SUITE_OWNER",
                "registered suite owner must be a non-empty string",
                path=suite_path,
                field="owner",
                observed=str(owner),
                suite=suite,
                check=check,
            )
        owners[suite_id] = owner
    return owners


def _validate_adapter(
    root: Path,
    adapter: PolicyImpactAdapter,
    suite_paths: Mapping[str, str],
    *,
    suite: str,
    check: str,
) -> PolicyImpactAdapter:
    identities: set[tuple[str, str, str]] = set()
    for owner in sorted(adapter.audited_owners):
        for edge in adapter.consumers_for(owner):
            _validate_consumer(root, edge, suite_paths, suite=suite, check=check)
            identities.add((edge.owner, edge.consumer, edge.relation))

    for suite_id, owner in sorted(
        _suite_owners(root, suite_paths, suite=suite, check=check).items()
    ):
        if owner not in adapter.audited_owners:
            continue
        identity = (owner, suite_paths[suite_id], "enforcement-suite-projection")
        if identity not in identities:
            raise _diagnostic(
                "POLICY_IMPACT.MISSING_ENFORCEMENT_SUITE_EDGE",
                "suite owned by an audited policy owner requires an enforcement-suite edge",
                field="relationships",
                observed=f"{suite_id}|{suite_paths[suite_id]}",
                suite=suite,
                check=check,
            )
    return adapter


def load_policy_impact(
    root: Path,
    registry_path: str,
    suite_paths: Mapping[str, str],
    *,
    suite: str = "policy-impact-query",
    check: str = "registry",
) -> PolicyImpactAdapter:
    repo_root = root.resolve()
    try:
        modules = load_canonical_module_corpus(repo_root)
        compiled = compile_policy_impact(repo_root, modules.modules, registry_path)
        registry = EdgeRegistry(
            repo_root,
            (
                metadata_dependency_source(modules.modules),
                ManifestSource(repo_root, CATALOG_SOURCE_ID, compiled.node_catalog),
                PolicyImpactSource(compiled),
            ),
        )
    except PolicyImpactError as error:
        raise _translate_policy_error(error, suite=suite, check=check) from error
    except MetadataError as error:
        failure = error.failure
        raise _diagnostic(
            failure.code,
            failure.message,
            path=failure.path,
            field=failure.field,
            observed=failure.observed,
            suite=suite,
            check=check,
            unavailable=failure.outcome == "unavailable",
        ) from error
    except GraphError as error:
        raise _diagnostic(
            error.failure.code,
            error.failure.message,
            observed=str(error.failure.details),
            suite=suite,
            check=check,
        ) from error
    return _validate_adapter(
        repo_root,
        PolicyImpactAdapter(registry, compiled),
        suite_paths,
        suite=suite,
        check=check,
    )


def load_registered_policy_impact(
    root: Path,
    source_registry_path: str,
    suite_paths: Mapping[str, str],
    *,
    suite: str = "policy-impact-query",
    check: str = "registry",
) -> PolicyImpactAdapter:
    from .repository_graph import load_compiled_policy_impact, load_repository_registry

    try:
        compiled = load_compiled_policy_impact(root)
        registry = load_repository_registry(root, source_registry_path)
    except GraphError as error:
        raise _diagnostic(
            error.failure.code,
            error.failure.message,
            observed=str(error.failure.details),
            suite=suite,
            check=check,
        ) from error
    return _validate_adapter(
        root.resolve(),
        PolicyImpactAdapter(registry, compiled),
        suite_paths,
        suite=suite,
        check=check,
    )
