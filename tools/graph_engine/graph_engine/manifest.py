from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .errors import InvalidSourceError
from .model import (
    Direction,
    Edge,
    EdgeGroup,
    EdgeSource,
    GraphContribution,
    Node,
    Provenance,
    TraversalPolicy,
)
from .paths import contained_path
from .registry import EdgeRegistry


DEFAULT_SOURCE_REGISTRY = "evaluation/standards-effectiveness/edge-source-registry.toml"


def _toml(root: Path, path: str) -> dict[str, Any]:
    source = contained_path(root, path, must_exist=True)
    try:
        with source.open("rb") as handle:
            raw = tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        raise InvalidSourceError("source contains invalid TOML", path=path) from error
    if not isinstance(raw, dict):
        raise InvalidSourceError("TOML root must be a table", path=path)
    return raw


def _strict(raw: Mapping[str, Any], allowed: set[str], required: set[str], owner: str) -> None:
    unknown = sorted(set(raw) - allowed)
    missing = sorted(required - set(raw))
    if unknown or missing:
        raise InvalidSourceError(
            "declaration contains unexpected or missing fields",
            owner=owner,
            field=(unknown or missing)[0],
        )


def _string(raw: Mapping[str, Any], field: str, owner: str) -> str:
    value = raw.get(field)
    if not isinstance(value, str) or not value:
        raise InvalidSourceError("field must be a non-empty string", owner=owner, field=field)
    return value


def _strings(raw: Mapping[str, Any], field: str, owner: str, *, allow_empty: bool) -> tuple[str, ...]:
    value = raw.get(field, [])
    if (
        not isinstance(value, list)
        or (not allow_empty and not value)
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise InvalidSourceError(
            "field must contain unique non-empty strings", owner=owner, field=field
        )
    return tuple(value)


def _metadata(raw: Mapping[str, Any], owner: str) -> dict[str, str]:
    value = raw.get("metadata", {})
    if not isinstance(value, dict) or any(
        not isinstance(key, str) or not key or not isinstance(item, str)
        for key, item in value.items()
    ):
        raise InvalidSourceError(
            "metadata must be a string-to-string table", owner=owner, field="metadata"
        )
    return value


@dataclass(frozen=True, slots=True)
class ManifestSource:
    repo_root: Path
    source_id: str
    path: str

    @property
    def id(self) -> str:
        return self.source_id

    def load(self) -> GraphContribution:
        raw = _toml(self.repo_root, self.path)
        _strict(
            raw,
            {"schema_version", "source_id", "nodes", "groups", "edges"},
            {"schema_version", "source_id", "nodes", "groups", "edges"},
            self.source_id,
        )
        if raw["schema_version"] != 1 or raw["source_id"] != self.source_id:
            raise InvalidSourceError(
                "manifest schema or source identity does not match registration",
                source=self.source_id,
                path=self.path,
            )
        provenance = Provenance(self.source_id, "manifest", self.path)
        raw_nodes = raw["nodes"]
        raw_groups = raw["groups"]
        raw_edges = raw["edges"]
        if not isinstance(raw_nodes, list) or not isinstance(raw_groups, list) or not isinstance(raw_edges, list):
            raise InvalidSourceError("nodes, groups, and edges must be arrays", source=self.source_id)

        nodes = []
        for item in raw_nodes:
            if not isinstance(item, dict):
                raise InvalidSourceError("node declaration must be a table", source=self.source_id)
            _strict(item, {"id", "aliases", "metadata"}, {"id"}, self.source_id)
            node_id = _string(item, "id", self.source_id)
            nodes.append(
                Node(
                    node_id,
                    _strings(item, "aliases", node_id, allow_empty=True),
                    provenance,
                    _metadata(item, node_id),
                )
            )

        groups = []
        for item in raw_groups:
            if not isinstance(item, dict):
                raise InvalidSourceError("group declaration must be a table", source=self.source_id)
            _strict(
                item,
                {"id", "purpose", "directions", "transitive", "validator", "metadata"},
                {"id", "purpose", "directions", "transitive"},
                self.source_id,
            )
            group_id = _string(item, "id", self.source_id)
            directions = frozenset(
                Direction.parse(value)
                for value in _strings(item, "directions", group_id, allow_empty=False)
            )
            transitive = item["transitive"]
            if not isinstance(transitive, bool):
                raise InvalidSourceError("group transitive must be a boolean", group=group_id)
            validator = item.get("validator")
            if validator is not None and (not isinstance(validator, str) or not validator):
                raise InvalidSourceError("group validator must be a non-empty string", group=group_id)
            groups.append(
                EdgeGroup(
                    group_id,
                    _string(item, "purpose", group_id),
                    TraversalPolicy(directions, transitive),
                    provenance,
                    validator,
                    _metadata(item, group_id),
                )
            )

        edges = []
        for item in raw_edges:
            if not isinstance(item, dict):
                raise InvalidSourceError("edge declaration must be a table", source=self.source_id)
            _strict(
                item,
                {"id", "source", "target", "relation", "groups", "traversable", "metadata"},
                {"id", "source", "target", "relation", "groups", "traversable"},
                self.source_id,
            )
            edge_id = _string(item, "id", self.source_id)
            traversable = item["traversable"]
            if not isinstance(traversable, bool):
                raise InvalidSourceError("edge traversable must be a boolean", edge=edge_id)
            edges.append(
                Edge(
                    edge_id,
                    _string(item, "source", edge_id),
                    _string(item, "target", edge_id),
                    _string(item, "relation", edge_id),
                    _strings(item, "groups", edge_id, allow_empty=False),
                    provenance,
                    _metadata(item, edge_id),
                    traversable,
                )
            )
        return GraphContribution(tuple(nodes), tuple(groups), tuple(edges))


def load_registry(
    repo_root: Path,
    registry_path: str = DEFAULT_SOURCE_REGISTRY,
    *,
    providers: Mapping[str, EdgeSource] | None = None,
) -> EdgeRegistry:
    root = repo_root.resolve()
    raw = _toml(root, registry_path)
    _strict(raw, {"schema_version", "sources"}, {"schema_version", "sources"}, registry_path)
    if raw["schema_version"] != 1:
        raise InvalidSourceError("source registry schema version must be 1", path=registry_path)
    raw_sources = raw["sources"]
    if not isinstance(raw_sources, list):
        raise InvalidSourceError("source registry sources must be an array", path=registry_path)
    sources: list[EdgeSource] = []
    available_providers = providers or {}
    for item in raw_sources:
        if not isinstance(item, dict):
            raise InvalidSourceError("source registration must be a table", path=registry_path)
        source_id = _string(item, "id", registry_path)
        kind = _string(item, "kind", source_id)
        if kind == "manifest":
            _strict(
                item,
                {"id", "kind", "path"},
                {"id", "kind", "path"},
                registry_path,
            )
            path = _string(item, "path", source_id)
            sources.append(ManifestSource(root, source_id, path))
        elif kind == "provider":
            _strict(
                item,
                {"id", "kind", "provider"},
                {"id", "kind", "provider"},
                registry_path,
            )
            provider_id = _string(item, "provider", source_id)
            provider = available_providers.get(provider_id)
            if provider is None:
                raise InvalidSourceError(
                    "registered deterministic provider is unavailable",
                    source=source_id,
                    provider=provider_id,
                )
            if provider.id != source_id:
                raise InvalidSourceError(
                    "provider source identity does not match registration",
                    source=source_id,
                    provider=provider.id,
                )
            sources.append(provider)
        else:
            raise InvalidSourceError(
                "source registry kind must be manifest or provider",
                source=source_id,
                kind=kind,
            )
    return EdgeRegistry(root, sources)


def load_manifest(repo_root: Path, manifest_path: str) -> EdgeRegistry:
    """Explicitly register and load one manifest selected by its caller."""

    root = repo_root.resolve()
    raw = _toml(root, manifest_path)
    source_id = raw.get("source_id")
    if not isinstance(source_id, str) or not source_id:
        raise InvalidSourceError(
            "manifest source_id must be a non-empty string", path=manifest_path
        )
    return EdgeRegistry(root, (ManifestSource(root, source_id, manifest_path),))
