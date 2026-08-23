from __future__ import annotations

import hashlib
import json
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import quote

from tools.graph_engine.graph_engine import Edge, GraphContribution, Provenance
from tools.graph_engine.graph_engine.errors import GraphError
from tools.graph_engine.graph_engine.manifest import ManifestSource
from tools.graph_engine.graph_engine.paths import contained_path
from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    ApplicabilityProgram,
    FactSchema,
    compile_fact_schema,
)
from tools.standards_metadata.standards_metadata import CanonicalStandardsCorpus

from .errors import PolicyImpactError, PolicyImpactFailure
from .model import (
    CompiledPolicyImpactSet,
    PolicyImpactSemantics,
    RelationshipKind,
    freeze,
    thaw,
)


DEFAULT_REGISTRY = "evaluation/standards-effectiveness/policy-impact-registry.toml"
POLICY_GROUP = "policy-impact"
SEMANTIC_GROUP = "semantic"
SOURCE_ID = "standards.policy-impact"
CATALOG_SOURCE_ID = "standards.policy-impact-catalog"
RELATIONSHIP_KIND_CONTRACT_VERSION = 1
RELATIONSHIP_KINDS = {
    kind: RelationshipKind(
        kind,
        (POLICY_GROUP, SEMANTIC_GROUP),
        "source-to-consumer",
        True,
        True,
    )
    for kind in (
        "normative-consumer",
        "router-projection",
        "prompt-projection",
        "template-projection",
        "reference-projection",
        "documentation-projection",
        "fixture-projection",
        "enforcement-suite-projection",
    )
}
RELATION_FIELDS = {
    "source",
    "consumer",
    "relation",
    "applicability",
    "evidence_owner",
    "rationale",
    "source_scope",
    "consumer_scope",
}


def _error(
    code: str,
    message: str,
    *,
    path: str | None = None,
    field: str | None = None,
    observed: str | None = None,
    unavailable: bool = False,
) -> PolicyImpactError:
    return PolicyImpactError(
        PolicyImpactFailure(
            code,
            "unavailable" if unavailable else "invalid",
            message,
            path,
            field,
            observed,
        )
    )


def _load_toml(root: Path, path: str) -> dict[str, Any]:
    try:
        source = contained_path(root, path, must_exist=True)
    except GraphError as error:
        details = error.failure.details
        code = (
            "PATH.OUTSIDE_REPOSITORY"
            if error.failure.code == "GRAPH.PATH_ESCAPE"
            else "INPUT.UNAVAILABLE"
        )
        raise _error(
            code,
            error.failure.message,
            path=str(details.get("path", path)),
            unavailable=code == "INPUT.UNAVAILABLE",
        ) from error
    try:
        with source.open("rb") as handle:
            raw = tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        raise _error("POLICY_IMPACT.INVALID_TOML", str(error), path=path) from error
    if not isinstance(raw, dict):
        raise _error("POLICY_IMPACT.INVALID", "TOML root must be a table", path=path)
    return raw


def _exact(
    raw: Mapping[str, object],
    *,
    allowed: set[str],
    required: set[str],
    path: str,
    owner: str,
) -> None:
    unknown = sorted(set(raw) - allowed)
    missing = sorted(required - set(raw))
    if unknown or missing:
        field = (unknown or missing)[0]
        raise _error(
            "POLICY_IMPACT.INVALID",
            "declaration contains unexpected or missing fields",
            path=path,
            field=field,
            observed=owner,
        )


def _text(raw: Mapping[str, object], field: str, path: str) -> str:
    value = raw.get(field)
    if not isinstance(value, str) or not value.strip():
        raise _error(
            "POLICY_IMPACT.INVALID",
            "field must be a non-empty string",
            path=path,
            field=field,
        )
    return value


def _texts(raw: Mapping[str, object], field: str, path: str) -> tuple[str, ...]:
    value = raw.get(field)
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise _error(
            "POLICY_IMPACT.INVALID",
            "field must contain unique non-empty strings",
            path=path,
            field=field,
        )
    return tuple(value)


def _scope(value: object, path: str, field: str) -> Mapping[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise _error(
            "POLICY_IMPACT.SCOPE",
            "scope must be a table",
            path=path,
            field=field,
        )
    kind = value.get("kind")
    heading = value.get("heading_path")
    valid = (
        set(value) == {"kind"}
        and kind == "whole-artifact"
        or set(value) == {"kind", "heading_path"}
        and kind == "structured"
        and isinstance(heading, list)
        and bool(heading)
        and all(isinstance(item, str) and item for item in heading)
    )
    if not valid:
        raise _error(
            "POLICY_IMPACT.SCOPE",
            "scope is invalid",
            path=path,
            field=field,
        )
    return freeze(value)


def _digest(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _load_facts(root: Path, path: str) -> FactSchema:
    raw = _load_toml(root, path)
    _exact(
        raw,
        allowed={"schema_version", "id", "facts"},
        required={"schema_version", "id", "facts"},
        path=path,
        owner=path,
    )
    facts = raw["facts"]
    if raw["schema_version"] != 1 or not isinstance(facts, list):
        raise _error("POLICY_IMPACT.FACTS", "fact catalog is invalid", path=path)
    try:
        return compile_fact_schema(
            {
                "kind": "applicability-fact-schema",
                "id": _text(raw, "id", path),
                "version": raw["schema_version"],
                "facts": facts,
            }
        )
    except ApplicabilityError as error:
        failure = error.failure
        raise _error(
            "POLICY_IMPACT.FACTS",
            failure.message,
            path=path,
            field=failure.field,
            observed=failure.observed,
            unavailable=failure.outcome == "unavailable",
        ) from error


def _load_audits(
    root: Path,
    path: str,
) -> tuple[tuple[str, str, frozenset[str]], ...]:
    raw = _load_toml(root, path)
    _exact(
        raw,
        allowed={"schema_version", "audits"},
        required={"schema_version", "audits"},
        path=path,
        owner=path,
    )
    audits = raw["audits"]
    if raw["schema_version"] != 1 or not isinstance(audits, list):
        raise _error("POLICY_IMPACT.AUDIT", "audit catalog is invalid", path=path)
    result = []
    seen = set()
    for item in audits:
        if not isinstance(item, dict):
            raise _error("POLICY_IMPACT.AUDIT", "audit must be a table", path=path)
        _exact(
            item,
            allowed={"id", "owner", "relationship_kinds", "scope", "horizon", "evidence"},
            required={"id", "owner", "relationship_kinds", "scope", "horizon", "evidence"},
            path=path,
            owner="audit",
        )
        audit_id = _text(item, "id", path)
        if audit_id in seen:
            raise _error(
                "POLICY_IMPACT.AUDIT",
                "audit identity is duplicated",
                path=path,
                observed=audit_id,
            )
        if item["scope"] != "whole-owner":
            raise _error(
                "POLICY_IMPACT.AUDIT",
                "initial audit scope must be whole-owner",
                path=path,
                observed=audit_id,
            )
        _text(item, "horizon", path)
        _text(item, "evidence", path)
        seen.add(audit_id)
        result.append(
            (
                audit_id,
                _text(item, "owner", path),
                frozenset(_texts(item, "relationship_kinds", path)),
            )
        )
    return tuple(result)


@dataclass(frozen=True, slots=True)
class _Declaration:
    owner: str
    source: str
    consumer: str
    relation: str
    applicability_program: ApplicabilityProgram
    source_scope: Mapping[str, object] | None
    consumer_scope: Mapping[str, object] | None
    evidence_owner: str
    rationale: str
    source_path: str


def _load_declarations(
    root: Path,
    paths: tuple[str, ...],
    fact_schema: FactSchema,
) -> tuple[_Declaration, ...]:
    result = []
    for path in paths:
        raw = _load_toml(root, path)
        _exact(
            raw,
            allowed={"schema_version", "owner", "relationships"},
            required={"schema_version", "owner", "relationships"},
            path=path,
            owner=path,
        )
        owner = _text(raw, "owner", path)
        relationships = raw["relationships"]
        if raw["schema_version"] != 1 or not isinstance(relationships, list):
            raise _error(
                "POLICY_IMPACT.INVALID",
                "relationship source is invalid",
                path=path,
            )
        for item in relationships:
            if not isinstance(item, dict):
                raise _error(
                    "POLICY_IMPACT.INVALID",
                    "relationship must be a table",
                    path=path,
                )
            if "applicability" not in item:
                raise _error(
                    "POLICY_IMPACT.APPLICABILITY",
                    "relationship requires typed applicability",
                    path=path,
                    field="applicability",
                )
            _exact(
                item,
                allowed=RELATION_FIELDS,
                required={
                    "source",
                    "consumer",
                    "relation",
                    "applicability",
                    "evidence_owner",
                    "rationale",
                },
                path=path,
                owner=owner,
            )
            source = _text(item, "source", path)
            evidence = _text(item, "evidence_owner", path)
            try:
                applicability_program = fact_schema.compile(item["applicability"])
            except ApplicabilityError as error:
                failure = error.failure
                raise _error(
                    "POLICY_IMPACT.APPLICABILITY",
                    failure.message,
                    path=path,
                    field=failure.field or "applicability",
                    observed=failure.observed,
                ) from error
            result.append(
                _Declaration(
                    owner,
                    source,
                    _text(item, "consumer", path),
                    _text(item, "relation", path),
                    applicability_program,
                    _scope(item.get("source_scope"), path, "source_scope"),
                    _scope(item.get("consumer_scope"), path, "consumer_scope"),
                    evidence,
                    _text(item, "rationale", path),
                    path,
                )
            )
    return tuple(result)


def policy_impact_edge_id(source: str, relation: str, consumer: str) -> str:
    encoded = (quote(value, safe="-._~") for value in (source, relation, consumer))
    return "policy-impact:v1/" + "/".join(encoded)


def compile_policy_impact(
    root: Path,
    corpus: CanonicalStandardsCorpus,
    registry_path: str = DEFAULT_REGISTRY,
) -> CompiledPolicyImpactSet:
    repo_root = root.resolve()
    raw = _load_toml(repo_root, registry_path)
    _exact(
        raw,
        allowed={
            "schema_version",
            "source_id",
            "node_catalog",
            "fact_catalog",
            "audit_catalog",
            "declaration_sources",
        },
        required={
            "schema_version",
            "source_id",
            "node_catalog",
            "fact_catalog",
            "audit_catalog",
            "declaration_sources",
        },
        path=registry_path,
        owner=registry_path,
    )
    if raw["schema_version"] != 1 or raw["source_id"] != SOURCE_ID:
        raise _error(
            "POLICY_IMPACT.REGISTRY",
            "registry schema or source identity is invalid",
            path=registry_path,
        )
    node_catalog = _text(raw, "node_catalog", registry_path)
    fact_catalog = _text(raw, "fact_catalog", registry_path)
    audit_catalog = _text(raw, "audit_catalog", registry_path)
    declaration_sources = _texts(raw, "declaration_sources", registry_path)

    try:
        catalog = ManifestSource(
            repo_root,
            CATALOG_SOURCE_ID,
            node_catalog,
        ).load()
    except GraphError as error:
        raise _error(
            "POLICY_IMPACT.CATALOG",
            error.failure.message,
            path=node_catalog,
            observed=str(error.failure.details),
        ) from error
    if catalog.edges:
        raise _error(
            "POLICY_IMPACT.DUAL_AUTHORITY",
            "node and group catalog must not declare policy-impact edges",
            path=node_catalog,
        )

    module_ids = {module.module_id for module in corpus.modules}
    policy_units = corpus.policy_unit_corpus
    node_ids = module_ids | {unit.id for unit in policy_units.units} | {
        node.id for node in catalog.nodes
    }
    groups = {group.id for group in catalog.groups}
    kinds = RELATIONSHIP_KINDS
    facts = _load_facts(repo_root, fact_catalog)
    audits = _load_audits(repo_root, audit_catalog)
    declarations = _load_declarations(repo_root, declaration_sources, facts)

    suite_nodes: dict[str, list[str]] = {}
    for node in catalog.nodes:
        suite_id = node.metadata.get("suite_id")
        if suite_id:
            suite_nodes.setdefault(suite_id, []).append(node.id)

    semantics: dict[str, PolicyImpactSemantics] = {}
    edges = []
    natural_keys: set[tuple[str, str, str]] = set()
    audited_owners: set[str] = set()
    for declaration in declarations:
        if declaration.owner not in module_ids:
            raise _error(
                "POLICY_IMPACT.UNKNOWN_OWNER",
                "declaration owner must be a canonical module ID",
                path=declaration.source_path,
                observed=declaration.owner,
            )
        source_unit = policy_units.active_by_id(declaration.source)
        resolved_source = policy_units.resolve(declaration.source)
        if declaration.source in module_ids:
            raise _error(
                "POLICY_IMPACT.MODULE_SOURCE",
                "policy-impact relationships must originate from policy units, not modules",
                path=declaration.source_path,
                observed=declaration.source,
            )
        if source_unit is None:
            code = (
                "POLICY_IMPACT.NONCANONICAL_SOURCE"
                if resolved_source is not None
                else "POLICY_IMPACT.UNKNOWN_SOURCE"
            )
            raise _error(
                code,
                "relationship source must be one exact active policy-unit ID",
                path=declaration.source_path,
                observed=declaration.source,
            )
        if source_unit.module != declaration.owner:
            raise _error(
                "POLICY_IMPACT.CROSS_OWNER_SOURCE",
                "relationship source must belong to its declaration owner module",
                path=declaration.source_path,
                observed=declaration.source,
            )
        if declaration.consumer not in node_ids:
            raise _error(
                "POLICY_IMPACT.UNKNOWN_CONSUMER",
                "relationship consumer is not a canonical node",
                path=declaration.source_path,
                observed=declaration.consumer,
            )
        kind = kinds.get(declaration.relation)
        if kind is None:
            raise _error(
                "POLICY_IMPACT.RELATION",
                "relationship kind is not registered",
                path=declaration.source_path,
                observed=declaration.relation,
            )
        missing_groups = sorted(set(kind.groups) - groups)
        if missing_groups:
            raise _error(
                "POLICY_IMPACT.GROUP",
                "relationship kind references an unknown graph group",
                path=registry_path,
                observed=missing_groups[0],
            )
        natural_key = (
            declaration.source,
            declaration.relation,
            declaration.consumer,
        )
        if natural_key in natural_keys:
            raise _error(
                "POLICY_IMPACT.DUPLICATE_EDGE",
                "source, relation, and consumer must identify one relationship",
                path=declaration.source_path,
                observed="|".join(natural_key),
            )
        natural_keys.add(natural_key)

        evidence_owner = declaration.evidence_owner
        if not evidence_owner.startswith("suite:"):
            raise _error(
                "POLICY_IMPACT.EVIDENCE_OWNER",
                "evidence owner must use suite:<registered-id>",
                path=declaration.source_path,
                observed=evidence_owner,
            )
        matches = suite_nodes.get(evidence_owner.removeprefix("suite:"), [])
        if len(matches) != 1:
            raise _error(
                "POLICY_IMPACT.EVIDENCE_OWNER",
                "evidence owner must resolve to exactly one canonical suite node",
                path=declaration.source_path,
                observed=evidence_owner,
                unavailable=not matches,
            )

        audit_matches = [
            audit_id
            for audit_id, owner, relations in audits
            if owner == declaration.owner and declaration.relation in relations
        ]
        if len(audit_matches) > 1:
            raise _error(
                "POLICY_IMPACT.AUDIT",
                "relationship matches more than one audit declaration",
                path=audit_catalog,
                observed="|".join(natural_key),
            )
        audit_id = audit_matches[0] if audit_matches else None
        if audit_id is not None:
            audited_owners.add(declaration.owner)

        edge_id = policy_impact_edge_id(*natural_key)
        propagation = kind.propagation
        dependency = {
            "source": declaration.source,
            "consumer": declaration.consumer,
            "relation": declaration.relation,
            "groups": list(kind.groups),
            "traversable": kind.traversable,
            "propagation": propagation,
            "applicability_program": declaration.applicability_program.as_projection(),
            "source_scope": thaw(declaration.source_scope),
            "consumer_scope": thaw(declaration.consumer_scope),
            "evidence_owner": evidence_owner,
            "audit_declaration": audit_id,
            "rationale": declaration.rationale,
            "node_catalog": node_catalog,
            "relationship_kind_contract_version": RELATIONSHIP_KIND_CONTRACT_VERSION,
            "fact_catalog": fact_catalog,
            "audit_catalog": audit_catalog,
        }
        semantics[edge_id] = PolicyImpactSemantics(
            edge_id,
            declaration.source,
            declaration.consumer,
            declaration.relation,
            declaration.applicability_program,
            declaration.source_scope,
            declaration.consumer_scope,
            propagation,
            evidence_owner,
            audit_id,
            declaration.rationale,
            declaration.source_path,
            _digest(dependency),
        )
        edges.append(
            Edge(
                edge_id,
                declaration.source,
                declaration.consumer,
                declaration.relation,
                kind.groups,
                Provenance(SOURCE_ID, "generator", declaration.source_path),
                {},
                kind.traversable,
            )
        )

    declaration_digest = _digest(
        [
            {
                "edge_id": edge_id,
                "fingerprint": semantics[edge_id].dependency_fingerprint,
            }
            for edge_id in sorted(semantics)
        ]
    )
    return CompiledPolicyImpactSet(
        GraphContribution((), (), tuple(sorted(edges, key=lambda edge: edge.id))),
        semantics,
        facts,
        frozenset(audited_owners),
        node_catalog,
        declaration_sources,
        (
            registry_path,
            node_catalog,
            fact_catalog,
            audit_catalog,
            *declaration_sources,
        ),
        declaration_digest,
    )
