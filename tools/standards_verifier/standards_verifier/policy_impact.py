from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping

from .diagnostics import Diagnostic, EngineError
from .paths import contained_file


RELATION_TYPES = frozenset(
    {
        "normative-consumer",
        "router-projection",
        "prompt-projection",
        "template-projection",
        "fixture-projection",
        "enforcement-suite-projection",
    }
)
DEFAULT_MANIFEST = "evaluation/standards-effectiveness/policy-semantic-impact.toml"


def _load_module_metadata(root: Path, path: str, *, suite: str, check: str):
    from .checks.metadata import load_module_metadata

    return load_module_metadata(root, path, suite=suite, check=check)


def _valid_owner_id(value: str) -> bool:
    from .checks.metadata import ID_PATTERN

    return ID_PATTERN.fullmatch(value) is not None


@dataclass(frozen=True, slots=True)
class ImpactOwner:
    id: str
    path: str


@dataclass(frozen=True, slots=True)
class ImpactEdge:
    owner: str
    consumer: str
    relation: str
    applicability: str
    evidence_owner: str


@dataclass(frozen=True, slots=True)
class PolicyImpact:
    owners: tuple[ImpactOwner, ...]
    edges: tuple[ImpactEdge, ...]

    def consumers_for(self, owner: str) -> tuple[ImpactEdge, ...]:
        if owner not in {item.id for item in self.owners}:
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
                (edge for edge in self.edges if edge.owner == owner),
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
) -> EngineError:
    return EngineError(
        Diagnostic(
            code,
            "invalid",
            message,
            suite=suite,
            check=check,
            path=path,
            field=field,
            observed=observed,
        )
    )


def _load_toml(root: Path, manifest_path: str, *, suite: str, check: str) -> dict[str, object]:
    path = contained_file(root, manifest_path, suite=suite, check=check)
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        raise EngineError(
            Diagnostic(
                "POLICY_IMPACT.INVALID_TOML",
                "invalid",
                str(error),
                suite=suite,
                check=check,
                path=manifest_path,
            )
        ) from error
    return raw


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


def load_policy_impact(
    root: Path,
    manifest_path: str,
    suite_paths: Mapping[str, str],
    *,
    suite: str = "policy-impact-query",
    check: str = "manifest",
) -> PolicyImpact:
    raw = _load_toml(root, manifest_path, suite=suite, check=check)
    expected_root = {"schema_version", "owners", "edges"}
    if set(raw) != expected_root:
        raise _diagnostic(
            "POLICY_IMPACT.ROOT_FIELDS",
            "manifest requires exactly schema_version, owners, and edges",
            path=manifest_path,
            observed=",".join(sorted(set(raw) ^ expected_root)),
            suite=suite,
            check=check,
        )
    if raw["schema_version"] != 1:
        raise _diagnostic(
            "POLICY_IMPACT.SCHEMA_VERSION",
            "manifest schema version must be 1",
            path=manifest_path,
            field="schema_version",
            observed=str(raw["schema_version"]),
            suite=suite,
            check=check,
        )

    raw_owners = raw["owners"]
    if not isinstance(raw_owners, list) or not raw_owners:
        raise _diagnostic(
            "POLICY_IMPACT.OWNERS",
            "manifest requires at least one audited owner",
            path=manifest_path,
            field="owners",
            suite=suite,
            check=check,
        )
    owners: list[ImpactOwner] = []
    seen_owner_ids: set[str] = set()
    seen_owner_paths: set[str] = set()
    for raw_owner in raw_owners:
        if not isinstance(raw_owner, dict) or set(raw_owner) != {"id", "path", "coverage"}:
            raise _diagnostic(
                "POLICY_IMPACT.OWNER_FIELDS",
                "owner requires exactly id, path, and coverage",
                path=manifest_path,
                field="owners",
                suite=suite,
                check=check,
            )
        owner_id = raw_owner["id"]
        owner_path = raw_owner["path"]
        coverage = raw_owner["coverage"]
        if not isinstance(owner_id, str) or not _valid_owner_id(owner_id):
            raise _diagnostic(
                "POLICY_IMPACT.OWNER_ID",
                "owner id must be a canonical metadata identifier",
                path=manifest_path,
                field="id",
                observed=str(owner_id),
                suite=suite,
                check=check,
            )
        if not isinstance(owner_path, str) or not owner_path:
            raise _diagnostic(
                "POLICY_IMPACT.OWNER_PATH",
                "owner path must be a non-empty repository path",
                path=manifest_path,
                field="path",
                observed=str(owner_path),
                suite=suite,
                check=check,
            )
        if coverage != "audited":
            raise _diagnostic(
                "POLICY_IMPACT.COVERAGE",
                "listed owner coverage must be explicitly audited",
                path=manifest_path,
                field="coverage",
                observed=str(coverage),
                suite=suite,
                check=check,
            )
        if owner_id in seen_owner_ids or owner_path in seen_owner_paths:
            raise _diagnostic(
                "POLICY_IMPACT.DUPLICATE_OWNER",
                "owner ids and paths must be unique",
                path=manifest_path,
                field="owners",
                observed=owner_id,
                suite=suite,
                check=check,
            )
        module = _load_module_metadata(root, owner_path, suite=suite, check=check)
        if module.module_id != owner_id:
            raise _diagnostic(
                "POLICY_IMPACT.UNKNOWN_OWNER",
                "owner id does not match canonical metadata at its path",
                path=manifest_path,
                field="id",
                observed=owner_id,
                suite=suite,
                check=check,
            )
        seen_owner_ids.add(owner_id)
        seen_owner_paths.add(owner_path)
        owners.append(ImpactOwner(owner_id, owner_path))

    raw_edges = raw["edges"]
    if not isinstance(raw_edges, list) or not raw_edges:
        raise _diagnostic(
            "POLICY_IMPACT.EDGES",
            "manifest requires at least one semantic edge",
            path=manifest_path,
            field="edges",
            suite=suite,
            check=check,
        )
    edges: list[ImpactEdge] = []
    seen_edges: set[tuple[str, str, str]] = set()
    for raw_edge in raw_edges:
        edge_fields = {"owner", "consumer", "relation", "applicability", "evidence_owner"}
        if not isinstance(raw_edge, dict) or set(raw_edge) != edge_fields:
            raise _diagnostic(
                "POLICY_IMPACT.EDGE_FIELDS",
                "edge requires exactly owner, consumer, relation, applicability, and evidence_owner",
                path=manifest_path,
                field="edges",
                suite=suite,
                check=check,
            )
        if any(not isinstance(raw_edge[field], str) for field in edge_fields):
            raise _diagnostic(
                "POLICY_IMPACT.EDGE_VALUE",
                "edge fields must be strings",
                path=manifest_path,
                field="edges",
                suite=suite,
                check=check,
            )
        edge = ImpactEdge(
            raw_edge["owner"],
            raw_edge["consumer"],
            raw_edge["relation"],
            raw_edge["applicability"],
            raw_edge["evidence_owner"],
        )
        if edge.owner not in seen_owner_ids:
            raise _diagnostic(
                "POLICY_IMPACT.UNKNOWN_OWNER",
                "edge owner has no audited coverage entry",
                path=manifest_path,
                field="owner",
                observed=edge.owner,
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
        if not edge.applicability.strip():
            raise _diagnostic(
                "POLICY_IMPACT.APPLICABILITY",
                "edge applicability must be non-empty",
                path=manifest_path,
                field="applicability",
                suite=suite,
                check=check,
            )
        if not edge.evidence_owner.startswith("suite:"):
            raise _diagnostic(
                "POLICY_IMPACT.EVIDENCE_OWNER",
                "evidence owner must use suite:<registered-id>",
                path=manifest_path,
                field="evidence_owner",
                observed=edge.evidence_owner,
                suite=suite,
                check=check,
            )
        evidence_suite = edge.evidence_owner.removeprefix("suite:")
        if evidence_suite not in suite_paths:
            raise _diagnostic(
                "POLICY_IMPACT.EVIDENCE_OWNER",
                "evidence owner suite is not registered",
                path=manifest_path,
                field="evidence_owner",
                observed=edge.evidence_owner,
                suite=suite,
                check=check,
            )
        contained_file(root, suite_paths[evidence_suite], suite=suite, check=check)
        identity = (edge.owner, edge.consumer, edge.relation)
        if identity in seen_edges:
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
            edge,
            suite_paths,
            manifest_path=manifest_path,
            suite=suite,
            check=check,
        )
        seen_edges.add(identity)
        edges.append(edge)

    return PolicyImpact(tuple(owners), tuple(edges))
