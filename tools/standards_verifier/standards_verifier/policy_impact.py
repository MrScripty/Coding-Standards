from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping

from tools.graph_engine.graph_engine import (
    AliasConflictError,
    EdgeRegistry,
    GraphError,
    InvalidEdgeError,
    InvalidGroupError,
    InvalidSourceError,
    MissingArtifactError,
    PathEscapeError,
    UnknownGroupError,
    load_manifest,
)

from .diagnostics import Diagnostic, EngineError
from .paths import contained_file


RELATION_TYPES = frozenset(
    {
        "normative-consumer",
        "router-projection",
        "prompt-projection",
        "template-projection",
        "reference-projection",
        "fixture-projection",
        "enforcement-suite-projection",
    }
)
POLICY_GROUP = "policy-impact"
DEFAULT_SOURCE_REGISTRY = "evaluation/standards-effectiveness/edge-source-registry.toml"


def _load_module_metadata(root: Path, path: str, *, suite: str, check: str):
    from .checks.metadata import load_module_metadata

    return load_module_metadata(root, path, suite=suite, check=check)


@dataclass(frozen=True, slots=True)
class ImpactEdge:
    edge_id: str
    owner: str
    consumer: str
    relation: str
    applicability: str
    evidence_owner: str


@dataclass(frozen=True, slots=True)
class PolicyImpactAdapter:
    registry: EdgeRegistry
    audited_owners: frozenset[str]

    def consumers_for(self, owner: str) -> tuple[ImpactEdge, ...]:
        if owner not in self.audited_owners:
            raise EngineError(
                Diagnostic(
                    "POLICY_IMPACT.OWNER_NOT_AUDITED",
                    "unavailable",
                    "policy owner has no audited semantic-impact coverage",
                    observed=owner,
                ),
                exit_code=3,
            )
        return tuple(
            sorted(
                (
                    _impact_edge(self.registry, view.edge)
                    for view in self.registry.outgoing(owner, (POLICY_GROUP,))
                ),
                key=lambda edge: (
                    edge.consumer,
                    edge.relation,
                    edge.applicability,
                    edge.evidence_owner,
                ),
            )
        )


def _diagnostic(
    code: str,
    message: str,
    *,
    path: str,
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
        ),
        exit_code=3 if unavailable else 2,
    )


def _translate_graph_error(
    error: GraphError,
    manifest_path: str,
    *,
    suite: str,
    check: str,
) -> EngineError:
    details = error.failure.details
    if isinstance(error, PathEscapeError):
        return _diagnostic(
            "PATH.OUTSIDE_REPOSITORY",
            error.failure.message,
            path=details.get("path", manifest_path),
            suite=suite,
            check=check,
        )
    if isinstance(error, MissingArtifactError):
        return _diagnostic(
            "INPUT.UNAVAILABLE",
            error.failure.message,
            path=details.get("path", manifest_path),
            suite=suite,
            check=check,
            unavailable=True,
        )
    if isinstance(error, InvalidEdgeError):
        if "duplicated" in error.failure.message:
            code = "POLICY_IMPACT.DUPLICATE_EDGE"
            field = "edges"
        elif details.get("endpoint") == "source":
            code = "POLICY_IMPACT.UNKNOWN_OWNER"
            field = "owner"
        elif details.get("endpoint") == "target":
            code = "POLICY_IMPACT.UNKNOWN_CONSUMER"
            field = "consumer"
        else:
            code = "POLICY_IMPACT.GRAPH_INVALID"
            field = "edges"
        return _diagnostic(
            code,
            error.failure.message,
            path=manifest_path,
            field=field,
            observed=details.get("node", details.get("edge")),
            suite=suite,
            check=check,
        )
    if isinstance(error, (InvalidGroupError, UnknownGroupError)):
        code = "POLICY_IMPACT.GROUP"
    elif isinstance(error, AliasConflictError):
        code = "POLICY_IMPACT.DUPLICATE_OWNER"
    elif isinstance(error, InvalidSourceError):
        code = "POLICY_IMPACT.GRAPH_INVALID"
    else:
        code = "POLICY_IMPACT.GRAPH_INVALID"
    return _diagnostic(
        code,
        error.failure.message,
        path=manifest_path,
        observed=next(iter(details.values()), None),
        suite=suite,
        check=check,
    )


def _repository_path(registry: EdgeRegistry, node_id: str, manifest_path: str) -> str:
    node = registry.nodes[node_id]
    value = node.metadata.get("repository_path")
    if not value:
        raise _diagnostic(
            "POLICY_IMPACT.UNKNOWN_CONSUMER",
            "policy-impact nodes require one repository_path",
            path=manifest_path,
            field="repository_path",
            observed=node_id,
        )
    return value


def _impact_edge(registry: EdgeRegistry, edge) -> ImpactEdge:
    return ImpactEdge(
        edge.id,
        edge.source,
        _repository_path(registry, edge.target, edge.provenance.locator),
        edge.relation,
        edge.metadata["applicability"],
        edge.metadata["evidence_owner"],
    )


def _consumer_matches_relation(
    root: Path,
    edge: ImpactEdge,
    suite_paths: Mapping[str, str],
    *,
    manifest_path: str,
    suite: str,
    check: str,
) -> None:
    contained_file(root, edge.consumer, suite=suite, check=check)
    path = PurePosixPath(edge.consumer)
    valid = False
    if edge.relation == "normative-consumer":
        _load_module_metadata(root, edge.consumer, suite=suite, check=check)
        valid = True
    elif edge.relation == "router-projection":
        module = _load_module_metadata(root, edge.consumer, suite=suite, check=check)
        valid = module.module_id == "router"
    elif edge.relation == "prompt-projection":
        valid = path.parts[:1] == ("prompts",) and path.suffix == ".md"
    elif edge.relation == "template-projection":
        valid = path.parts[:1] == ("templates",) and path.suffix == ".md"
    elif edge.relation == "reference-projection":
        valid = path.parts[:1] == ("reference",) and path.suffix == ".md"
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
            path=manifest_path,
            field="consumer",
            observed=edge.consumer,
            suite=suite,
            check=check,
        )


def _load_toml(root: Path, path: str, *, suite: str, check: str) -> dict[str, object]:
    source = contained_file(root, path, suite=suite, check=check)
    try:
        with source.open("rb") as handle:
            return tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        raise _diagnostic(
            "POLICY_IMPACT.INVALID_TOML",
            str(error),
            path=path,
            suite=suite,
            check=check,
        ) from error


def _registered_suite_owners(
    root: Path,
    suite_paths: Mapping[str, str],
    *,
    suite: str,
    check: str,
) -> dict[str, str]:
    owners: dict[str, str] = {}
    for suite_id, suite_path in suite_paths.items():
        raw = _load_toml(root, suite_path, suite=suite, check=check)
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


def load_policy_impact(
    root: Path,
    manifest_path: str,
    suite_paths: Mapping[str, str],
    *,
    suite: str = "policy-impact-query",
    check: str = "manifest",
    _registry: EdgeRegistry | None = None,
) -> PolicyImpactAdapter:
    if _registry is None:
        try:
            registry = load_manifest(root, manifest_path)
            registry.edges_for_group(POLICY_GROUP)
        except GraphError as error:
            raise _translate_graph_error(
                error, manifest_path, suite=suite, check=check
            ) from error
    else:
        registry = _registry

    audited_owners = frozenset(
        node.id
        for node in registry.nodes.values()
        if node.metadata.get("policy_impact_coverage") == "audited"
    )
    if not audited_owners:
        raise _diagnostic(
            "POLICY_IMPACT.OWNERS",
            "manifest requires at least one explicitly audited owner",
            path=manifest_path,
            field="nodes",
            suite=suite,
            check=check,
        )
    for owner in sorted(audited_owners):
        owner_path = _repository_path(registry, owner, manifest_path)
        module = _load_module_metadata(root, owner_path, suite=suite, check=check)
        if module.module_id != owner:
            raise _diagnostic(
                "POLICY_IMPACT.UNKNOWN_OWNER",
                "owner id does not match canonical metadata at its path",
                path=manifest_path,
                field="id",
                observed=owner,
                suite=suite,
                check=check,
            )

    impact_edges: list[ImpactEdge] = []
    seen: set[tuple[str, str, str]] = set()
    for edge in registry.edges_for_group(POLICY_GROUP):
        if edge.source not in audited_owners:
            raise _diagnostic(
                "POLICY_IMPACT.UNKNOWN_OWNER",
                "edge owner has no audited coverage entry",
                path=manifest_path,
                field="owner",
                observed=edge.source,
                suite=suite,
                check=check,
            )
        if edge.relation not in RELATION_TYPES:
            raise _diagnostic(
                "POLICY_IMPACT.RELATION",
                "edge relation is not supported",
                path=manifest_path,
                field="relation",
                observed=edge.relation,
                suite=suite,
                check=check,
            )
        applicability = edge.metadata.get("applicability", "")
        evidence_owner = edge.metadata.get("evidence_owner", "")
        if not applicability.strip():
            raise _diagnostic(
                "POLICY_IMPACT.APPLICABILITY",
                "edge applicability must be non-empty",
                path=manifest_path,
                field="applicability",
                suite=suite,
                check=check,
            )
        if not evidence_owner.startswith("suite:"):
            raise _diagnostic(
                "POLICY_IMPACT.EVIDENCE_OWNER",
                "evidence owner must use suite:<registered-id>",
                path=manifest_path,
                field="evidence_owner",
                observed=evidence_owner,
                suite=suite,
                check=check,
            )
        evidence_suite = evidence_owner.removeprefix("suite:")
        if evidence_suite not in suite_paths:
            raise _diagnostic(
                "POLICY_IMPACT.EVIDENCE_OWNER",
                "evidence owner suite is not registered",
                path=manifest_path,
                field="evidence_owner",
                observed=evidence_owner,
                suite=suite,
                check=check,
            )
        consumer = _repository_path(registry, edge.target, manifest_path)
        impact = ImpactEdge(
            edge.id,
            edge.source,
            consumer,
            edge.relation,
            applicability,
            evidence_owner,
        )
        identity = (impact.owner, impact.consumer, impact.relation)
        if identity in seen:
            raise _diagnostic(
                "POLICY_IMPACT.DUPLICATE_EDGE",
                "owner, consumer, and relation must identify one edge",
                path=manifest_path,
                field="edges",
                observed="|".join(identity),
                suite=suite,
                check=check,
            )
        _consumer_matches_relation(
            root,
            impact,
            suite_paths,
            manifest_path=manifest_path,
            suite=suite,
            check=check,
        )
        seen.add(identity)
        impact_edges.append(impact)

    suite_owners = _registered_suite_owners(
        root, suite_paths, suite=suite, check=check
    )
    for suite_id, suite_owner in sorted(suite_owners.items()):
        if suite_owner not in audited_owners:
            continue
        suite_path = suite_paths[suite_id]
        identity = (suite_owner, suite_path, "enforcement-suite-projection")
        if identity not in seen:
            raise _diagnostic(
                "POLICY_IMPACT.MISSING_ENFORCEMENT_SUITE_EDGE",
                "suite owned by an audited policy owner requires an enforcement-suite edge",
                path=manifest_path,
                field="edges",
                observed=f"{suite_id}|{suite_path}",
                suite=suite,
                check=check,
            )
    return PolicyImpactAdapter(registry, audited_owners)


def load_registered_policy_impact(
    root: Path,
    source_registry_path: str,
    suite_paths: Mapping[str, str],
    *,
    suite: str = "policy-impact-query",
    check: str = "registry",
) -> PolicyImpactAdapter:
    from .repository_graph import load_repository_registry

    try:
        registry = load_repository_registry(root, source_registry_path)
        edges = registry.edges_for_group(POLICY_GROUP)
    except GraphError as error:
        raise _translate_graph_error(
            error, source_registry_path, suite=suite, check=check
        ) from error
    if not edges:
        raise _diagnostic(
            "POLICY_IMPACT.EDGES",
            "registered policy-impact group requires at least one edge",
            path=source_registry_path,
            field="sources",
            suite=suite,
            check=check,
        )
    return load_policy_impact(
        root,
        source_registry_path,
        suite_paths,
        suite=suite,
        check=check,
        _registry=registry,
    )
