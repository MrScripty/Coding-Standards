from __future__ import annotations

import hashlib
import json
import tomllib
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import quote

from tools.graph_engine.graph_engine import (
    Direction,
    Edge,
    EdgeGroup,
    GraphError,
    GraphContribution,
    Node,
    Provenance,
    TraversalPolicy,
)
from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    ApplicabilityProgram,
    FactSchema,
    compile_fact_schema,
)
from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    ContentSource,
    ContentSourceInput,
    MetadataError,
    content_source,
)

from .errors import PolicyImpactError, PolicyImpactFailure
from .model import (
    CompiledPolicyImpactSet,
    PolicyImpactArtifact,
    PolicyImpactSemantics,
    RelationshipKind,
    freeze,
    thaw,
)


DEFAULT_REGISTRY = "evaluation/standards-effectiveness/policy-impact-registry.toml"
DEFAULT_AUTHORING_CONTRACT = (
    "tools/standards_policy_impact/contracts/policy-impact-authoring-v2.toml"
)
POLICY_GROUP = "policy-impact"
SEMANTIC_GROUP = "semantic"
SOURCE_ID = "standards.policy-impact"
CATALOG_SOURCE_ID = "standards.policy-impact-catalog"
RELATIONSHIP_KIND_CONTRACT_VERSION = 2
EVIDENCE_OWNER_RULE = "required-registered-suite"
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


def _load_toml(source: ContentSource, path: str) -> dict[str, Any]:
    try:
        raw = tomllib.loads(source.read_bytes(path).decode("utf-8"))
    except MetadataError as error:
        failure = error.failure
        raise _error(
            failure.code,
            failure.message,
            path=failure.path or path,
            unavailable=failure.outcome == "unavailable",
        ) from error
    except UnicodeDecodeError as error:
        raise _error("POLICY_IMPACT.INVALID_UTF8", str(error), path=path) from error
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


def _integer(raw: Mapping[str, object], field: str, path: str) -> int:
    value = raw.get(field)
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise _error(
            "POLICY_IMPACT.INVALID",
            "field must be a positive integer",
            path=path,
            field=field,
        )
    return value


def _boolean(raw: Mapping[str, object], field: str, path: str) -> bool:
    value = raw.get(field)
    if not isinstance(value, bool):
        raise _error(
            "POLICY_IMPACT.INVALID",
            "field must be a boolean",
            path=path,
            field=field,
        )
    return value


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


@dataclass(frozen=True, slots=True)
class _AuthoringContract:
    provider_version: int
    catalog_version: int
    declaration_version: int
    relationship_kind_version: int
    evidence_owner_rule: str
    artifact_kinds: frozenset[str]
    groups: tuple[EdgeGroup, ...]
    relationship_kinds: Mapping[str, RelationshipKind]
    digest: str
    source_path: str


@dataclass(frozen=True, slots=True)
class _ArtifactCatalog:
    nodes: tuple[Node, ...]
    artifacts: Mapping[str, PolicyImpactArtifact]
    digest: str


def _load_authoring_contract(source: ContentSource, path: str) -> _AuthoringContract:
    raw = _load_toml(source, path)
    _exact(
        raw,
        allowed={
            "schema_version",
            "provider_contract_version",
            "catalog_contract_version",
            "declaration_schema_version",
            "relationship_kind_contract_version",
            "evidence_owner_rule",
            "artifact_kinds",
            "groups",
            "relationship_kinds",
        },
        required={
            "schema_version",
            "provider_contract_version",
            "catalog_contract_version",
            "declaration_schema_version",
            "relationship_kind_contract_version",
            "evidence_owner_rule",
            "artifact_kinds",
            "groups",
            "relationship_kinds",
        },
        path=path,
        owner=path,
    )
    if _integer(raw, "schema_version", path) != 2:
        raise _error(
            "POLICY_IMPACT.UNSUPPORTED_CONTRACT",
            "authoring contract version is unsupported",
            path=path,
            field="schema_version",
            observed=str(raw["schema_version"]),
        )
    artifact_kinds = frozenset(_texts(raw, "artifact_kinds", path))
    evidence_owner_rule = _text(raw, "evidence_owner_rule", path)
    if evidence_owner_rule != EVIDENCE_OWNER_RULE:
        raise _error(
            "POLICY_IMPACT.UNSUPPORTED_CONTRACT",
            "evidence-owner rule is unsupported",
            path=path,
            field="evidence_owner_rule",
            observed=evidence_owner_rule,
        )
    group_items = raw["groups"]
    if not isinstance(group_items, list) or not group_items:
        raise _error("POLICY_IMPACT.CONTRACT", "groups must be non-empty", path=path)
    groups: list[EdgeGroup] = []
    for item in group_items:
        if not isinstance(item, dict):
            raise _error("POLICY_IMPACT.CONTRACT", "group must be a table", path=path)
        _exact(
            item,
            allowed={"id", "purpose", "directions", "transitive", "validator"},
            required={"id", "purpose", "directions", "transitive"},
            path=path,
            owner="group",
        )
        group_id = _text(item, "id", path)
        purpose = _text(item, "purpose", path)
        directions = _texts(item, "directions", path)
        transitive = _boolean(item, "transitive", path)
        validator = _text(item, "validator", path) if "validator" in item else None
        try:
            traversal = TraversalPolicy(
                frozenset(Direction.parse(value) for value in directions),
                transitive,
            )
            groups.append(
                EdgeGroup(
                    group_id,
                    purpose,
                    traversal,
                    Provenance(SOURCE_ID, "generator", path),
                    validator,
                )
            )
        except (GraphError, ValueError) as error:
            raise _error("POLICY_IMPACT.CONTRACT", str(error), path=path) from error
    if len({group.id for group in groups}) != len(groups):
        raise _error("POLICY_IMPACT.CONTRACT", "group IDs must be unique", path=path)

    kind_items = raw["relationship_kinds"]
    if not isinstance(kind_items, list) or not kind_items:
        raise _error(
            "POLICY_IMPACT.CONTRACT",
            "relationship_kinds must be non-empty",
            path=path,
        )
    kinds: dict[str, RelationshipKind] = {}
    group_ids = {group.id for group in groups}
    admitted_targets = artifact_kinds | {
        "canonical-non-reference-module",
        "canonical-reference-module",
        "router",
    }
    for item in kind_items:
        if not isinstance(item, dict):
            raise _error(
                "POLICY_IMPACT.CONTRACT",
                "relationship kind must be a table",
                path=path,
            )
        _exact(
            item,
            allowed={
                "id",
                "target_class",
                "groups",
                "propagation",
                "traversable",
            },
            required={
                "id",
                "target_class",
                "groups",
                "propagation",
                "traversable",
            },
            path=path,
            owner="relationship_kind",
        )
        kind_id = _text(item, "id", path)
        target_class = _text(item, "target_class", path)
        groups_for_kind = _texts(item, "groups", path)
        if kind_id in kinds or not set(groups_for_kind).issubset(group_ids):
            raise _error(
                "POLICY_IMPACT.CONTRACT",
                "relationship kind ID and groups must resolve uniquely",
                path=path,
                observed=kind_id,
            )
        if target_class not in admitted_targets:
            raise _error(
                "POLICY_IMPACT.CONTRACT",
                "relationship target class is not admitted",
                path=path,
                observed=target_class,
            )
        propagation = _text(item, "propagation", path)
        if propagation != "source-to-consumer":
            raise _error(
                "POLICY_IMPACT.CONTRACT",
                "relationship propagation is unsupported",
                path=path,
                observed=propagation,
            )
        kinds[kind_id] = RelationshipKind(
            kind_id,
            target_class,
            groups_for_kind,
            propagation,
            _boolean(item, "traversable", path),
        )
    relationship_version = _integer(raw, "relationship_kind_contract_version", path)
    if relationship_version != RELATIONSHIP_KIND_CONTRACT_VERSION:
        raise _error(
            "POLICY_IMPACT.UNSUPPORTED_CONTRACT",
            "relationship-kind contract version is unsupported",
            path=path,
            observed=str(relationship_version),
        )
    return _AuthoringContract(
        _integer(raw, "provider_contract_version", path),
        _integer(raw, "catalog_contract_version", path),
        _integer(raw, "declaration_schema_version", path),
        relationship_version,
        evidence_owner_rule,
        artifact_kinds,
        tuple(groups),
        dict(sorted(kinds.items())),
        _digest(raw),
        path,
    )


def _load_catalog(
    source: ContentSource,
    path: str,
    contract: _AuthoringContract,
) -> _ArtifactCatalog:
    raw = _load_toml(source, path)
    _exact(
        raw,
        allowed={"schema_version", "source_id", "nodes"},
        required={"schema_version", "source_id", "nodes"},
        path=path,
        owner=path,
    )
    if raw["schema_version"] != contract.catalog_version or raw["source_id"] != CATALOG_SOURCE_ID:
        raise _error(
            "POLICY_IMPACT.CATALOG",
            "catalog schema or source identity is invalid",
            path=path,
        )
    items = raw["nodes"]
    if not isinstance(items, list):
        raise _error("POLICY_IMPACT.CATALOG", "nodes must be an array", path=path)
    nodes: list[Node] = []
    artifacts: dict[str, PolicyImpactArtifact] = {}
    for item in items:
        if not isinstance(item, dict):
            raise _error("POLICY_IMPACT.CATALOG", "node must be a table", path=path)
        _exact(
            item,
            allowed={"id", "aliases", "metadata"},
            required={"id", "metadata"},
            path=path,
            owner="node",
        )
        metadata = item["metadata"]
        if not isinstance(metadata, dict):
            raise _error("POLICY_IMPACT.CATALOG", "node metadata must be a table", path=path)
        _exact(
            metadata,
            allowed={"repository_path", "artifact_kind", "authority", "suite_id"},
            required={"repository_path", "artifact_kind", "authority"},
            path=path,
            owner="node.metadata",
        )
        node_id = _text(item, "id", path)
        aliases_value = item.get("aliases", [])
        if not isinstance(aliases_value, list) or any(
            not isinstance(alias, str) or not alias for alias in aliases_value
        ) or len(set(aliases_value)) != len(aliases_value):
            raise _error("POLICY_IMPACT.CATALOG", "node aliases are invalid", path=path)
        artifact_kind = _text(metadata, "artifact_kind", path)
        if artifact_kind not in contract.artifact_kinds:
            raise _error(
                "POLICY_IMPACT.ARTIFACT_KIND",
                "artifact kind is not admitted by the authoring contract",
                path=path,
                observed=artifact_kind,
            )
        authority = _text(metadata, "authority", path)
        if authority not in {"projection", "evidence"}:
            raise _error(
                "POLICY_IMPACT.ARTIFACT_AUTHORITY",
                "artifact authority must be projection or evidence",
                path=path,
                observed=authority,
            )
        suite_id = metadata.get("suite_id")
        if suite_id is not None and (not isinstance(suite_id, str) or not suite_id):
            raise _error("POLICY_IMPACT.CATALOG", "suite_id is invalid", path=path)
        if artifact_kind == "enforcement-suite" and suite_id is None:
            raise _error(
                "POLICY_IMPACT.CATALOG",
                "enforcement-suite artifacts require suite_id",
                path=path,
                observed=node_id,
            )
        if artifact_kind != "enforcement-suite" and suite_id is not None:
            raise _error(
                "POLICY_IMPACT.CATALOG",
                "only enforcement-suite artifacts may declare suite_id",
                path=path,
                observed=node_id,
            )
        repository_path = _text(metadata, "repository_path", path)
        artifact = PolicyImpactArtifact(
            node_id,
            tuple(aliases_value),
            repository_path,
            artifact_kind,
            authority,
            suite_id,
            _digest(
                {
                    "id": node_id,
                    "aliases": aliases_value,
                    "repository_path": repository_path,
                    "artifact_kind": artifact_kind,
                    "suite_id": suite_id,
                }
            ),
            path,
        )
        if node_id in artifacts:
            raise _error("POLICY_IMPACT.CATALOG", "node IDs must be unique", path=path)
        artifacts[node_id] = artifact
        nodes.append(
            Node(
                node_id,
                tuple(aliases_value),
                Provenance(SOURCE_ID, "generator", path),
                {key: str(value) for key, value in metadata.items()},
            )
        )
    return _ArtifactCatalog(
        tuple(nodes),
        dict(sorted(artifacts.items())),
        _digest(raw),
    )


def _load_suite_registry(source: ContentSource, path: str) -> Mapping[str, str]:
    raw = _load_toml(source, path)
    if raw.get("schema_version") != 1 or not isinstance(raw.get("suites"), list):
        raise _error("POLICY_IMPACT.SUITE_REGISTRY", "suite registry is invalid", path=path)
    suites: dict[str, str] = {}
    for item in raw["suites"]:
        if not isinstance(item, dict):
            raise _error("POLICY_IMPACT.SUITE_REGISTRY", "suite must be a table", path=path)
        suite_id = _text(item, "id", path)
        suite_path = _text(item, "path", path)
        if suite_id in suites:
            raise _error("POLICY_IMPACT.SUITE_REGISTRY", "suite IDs must be unique", path=path)
        suites[suite_id] = suite_path
    return dict(sorted(suites.items()))


def _load_facts(source: ContentSource, path: str) -> FactSchema:
    raw = _load_toml(source, path)
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
    source: ContentSource,
    paths: tuple[str, ...],
    fact_schema: FactSchema,
    contract: _AuthoringContract,
) -> tuple[_Declaration, ...]:
    result = []
    for path in paths:
        raw = _load_toml(source, path)
        _exact(
            raw,
            allowed={"schema_version", "owner", "relationships"},
            required={"schema_version", "owner", "relationships"},
            path=path,
            owner=path,
        )
        owner = _text(raw, "owner", path)
        relationships = raw["relationships"]
        if (
            raw["schema_version"] != contract.declaration_version
            or not isinstance(relationships, list)
        ):
            raise _error(
                "POLICY_IMPACT.UNSUPPORTED_DECLARATION",
                "relationship source schema is unsupported or invalid",
                path=path,
                field="schema_version",
                observed=str(raw["schema_version"]),
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
            required = {
                "source",
                "consumer",
                "relation",
                "applicability",
                "rationale",
            }
            if contract.evidence_owner_rule == EVIDENCE_OWNER_RULE:
                required.add("evidence_owner")
            _exact(
                item,
                allowed=RELATION_FIELDS,
                required=required,
                path=path,
                owner=owner,
            )
            relationship_source = _text(item, "source", path)
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
                    relationship_source,
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


def _target_matches(
    consumer: str,
    target_class: str,
    modules: Mapping[str, str],
    artifacts: Mapping[str, PolicyImpactArtifact],
) -> bool:
    module_role = modules.get(consumer)
    if target_class == "canonical-non-reference-module":
        return module_role is not None and module_role != "reference"
    if target_class == "canonical-reference-module":
        return module_role == "reference"
    if target_class == "router":
        return module_role == "router" or (
            consumer in artifacts
            and artifacts[consumer].artifact_kind == "routing-projection"
        )
    return (
        consumer in artifacts
        and artifacts[consumer].artifact_kind == target_class
    )


def compile_policy_impact(
    source: ContentSourceInput,
    corpus: CanonicalStandardsCorpus,
    registry_path: str = DEFAULT_REGISTRY,
) -> CompiledPolicyImpactSet:
    selected_source = content_source(source)
    raw = _load_toml(selected_source, registry_path)
    _exact(
        raw,
        allowed={
            "schema_version",
            "source_id",
            "authoring_contract",
            "node_catalog",
            "fact_catalog",
            "suite_registry",
            "declaration_sources",
        },
        required={
            "schema_version",
            "source_id",
            "authoring_contract",
            "node_catalog",
            "fact_catalog",
            "suite_registry",
            "declaration_sources",
        },
        path=registry_path,
        owner=registry_path,
    )
    if raw["schema_version"] != 2 or raw["source_id"] != SOURCE_ID:
        raise _error(
            "POLICY_IMPACT.REGISTRY",
            "registry schema or source identity is invalid",
            path=registry_path,
        )
    authoring_contract = _text(raw, "authoring_contract", registry_path)
    contract = _load_authoring_contract(selected_source, authoring_contract)
    node_catalog = _text(raw, "node_catalog", registry_path)
    fact_catalog = _text(raw, "fact_catalog", registry_path)
    suite_registry = _text(raw, "suite_registry", registry_path)
    declaration_sources = _texts(raw, "declaration_sources", registry_path)
    catalog = _load_catalog(selected_source, node_catalog, contract)
    suites = _load_suite_registry(selected_source, suite_registry)

    modules = {module.module_id: module.role for module in corpus.modules}
    module_ids = set(modules)
    policy_units = corpus.policy_unit_corpus
    node_ids = module_ids | {unit.id for unit in policy_units.units} | set(catalog.artifacts)
    groups = {group.id for group in contract.groups}
    kinds = contract.relationship_kinds
    facts = _load_facts(selected_source, fact_catalog)
    declarations = _load_declarations(
        selected_source,
        declaration_sources,
        facts,
        contract,
    )

    suite_nodes: dict[str, list[str]] = {}
    for artifact in catalog.artifacts.values():
        suite_id = artifact.suite_id
        if suite_id:
            if suites.get(suite_id) != artifact.repository_path:
                raise _error(
                    "POLICY_IMPACT.SUITE_REGISTRY",
                    "enforcement-suite artifact must match one registered suite",
                    path=node_catalog,
                    observed=suite_id,
                )
            suite_nodes.setdefault(suite_id, []).append(artifact.id)

    semantics: dict[str, PolicyImpactSemantics] = {}
    edges = []
    natural_keys: set[tuple[str, str, str]] = set()
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
        if not _target_matches(
            declaration.consumer,
            kind.target_class,
            modules,
            catalog.artifacts,
        ):
            raise _error(
                "POLICY_IMPACT.INCOMPATIBLE_TARGET",
                "relationship target is incompatible with its typed target class",
                path=declaration.source_path,
                field="consumer",
                observed=declaration.consumer,
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
            "rationale": declaration.rationale,
            "relationship_kind_contract_version": contract.relationship_kind_version,
            "evidence_owner_rule": contract.evidence_owner_rule,
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
    provider_contract_digest = _digest(
        {
            "source_id": SOURCE_ID,
            "registry_schema_version": raw["schema_version"],
            "provider_contract_version": contract.provider_version,
            "catalog_contract_version": contract.catalog_version,
            "declaration_schema_version": contract.declaration_version,
            "edge_identity_version": 1,
            "relationship_kind_contract_version": contract.relationship_kind_version,
            "authoring_contract_digest": contract.digest,
            "catalog_digest": catalog.digest,
            "relationship_kinds": [
                {
                    "id": kind.id,
                    "target_class": kind.target_class,
                    "groups": list(kind.groups),
                    "propagation": kind.propagation,
                    "traversable": kind.traversable,
                }
                for kind in sorted(kinds.values(), key=lambda item: item.id)
            ],
        }
    )
    return CompiledPolicyImpactSet(
        GraphContribution(
            tuple(sorted(catalog.nodes, key=lambda node: node.id)),
            tuple(sorted(contract.groups, key=lambda group: group.id)),
            tuple(sorted(edges, key=lambda edge: edge.id)),
        ),
        semantics,
        catalog.artifacts,
        kinds,
        facts,
        node_catalog,
        declaration_sources,
        (
            registry_path,
            authoring_contract,
            node_catalog,
            fact_catalog,
            suite_registry,
            *declaration_sources,
        ),
        declaration_digest,
        catalog.digest,
        contract.digest,
        provider_contract_digest,
        contract.relationship_kind_version,
    )
