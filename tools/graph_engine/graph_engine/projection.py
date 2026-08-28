from __future__ import annotations

from collections.abc import Mapping

from .errors import InvalidSourceError
from .model import (
    Direction,
    Edge,
    EdgeGroup,
    GraphContribution,
    Node,
    Provenance,
    TraversalPolicy,
)


def project_graph_contribution(value: GraphContribution) -> dict[str, object]:
    return {
        "nodes": [_project_node(item) for item in value.nodes],
        "groups": [_project_group(item) for item in value.groups],
        "edges": [_project_edge(item) for item in value.edges],
    }


def load_graph_contribution(value: Mapping[str, object]) -> GraphContribution:
    selected = _mapping(value, {"nodes", "groups", "edges"}, "graph contribution")
    return GraphContribution(
        tuple(_load_node(item) for item in _array(selected["nodes"], "nodes")),
        tuple(_load_group(item) for item in _array(selected["groups"], "groups")),
        tuple(_load_edge(item) for item in _array(selected["edges"], "edges")),
    )


def _project_provenance(value: Provenance | None) -> dict[str, object] | None:
    if value is None:
        return None
    return {
        "source_id": value.source_id,
        "kind": value.kind,
        "locator": value.locator,
    }


def _load_provenance(value: object) -> Provenance | None:
    if value is None:
        return None
    selected = _mapping(value, {"source_id", "kind", "locator"}, "provenance")
    return Provenance(
        _string(selected["source_id"], "source_id"),
        _string(selected["kind"], "kind"),
        _string(selected["locator"], "locator"),
    )


def _project_node(value: Node) -> dict[str, object]:
    return {
        "id": value.id,
        "aliases": list(value.aliases),
        "provenance": _project_provenance(value.provenance),
        "metadata": dict(value.metadata),
    }


def _load_node(value: object) -> Node:
    selected = _mapping(value, {"id", "aliases", "provenance", "metadata"}, "node")
    return Node(
        _string(selected["id"], "id"),
        _strings(selected["aliases"], "aliases"),
        _load_provenance(selected["provenance"]),
        _string_mapping(selected["metadata"], "metadata"),
    )


def _project_group(value: EdgeGroup) -> dict[str, object]:
    return {
        "id": value.id,
        "purpose": value.purpose,
        "directions": sorted(item.value for item in value.traversal.directions),
        "transitive": value.traversal.transitive,
        "provenance": _project_provenance(value.provenance),
        "validator": value.validator,
        "metadata": dict(value.metadata),
    }


def _load_group(value: object) -> EdgeGroup:
    selected = _mapping(
        value,
        {
            "id",
            "purpose",
            "directions",
            "transitive",
            "provenance",
            "validator",
            "metadata",
        },
        "edge group",
    )
    transitive = selected["transitive"]
    validator = selected["validator"]
    provenance = _load_provenance(selected["provenance"])
    if type(transitive) is not bool:
        raise _failure("group transitive must be Boolean")
    if validator is not None and type(validator) is not str:
        raise _failure("group validator must be string or null")
    if provenance is None:
        raise _failure("group provenance is required")
    try:
        directions = frozenset(
            Direction(item) for item in _strings(selected["directions"], "directions")
        )
    except ValueError as error:
        raise _failure("group direction is unsupported") from error
    return EdgeGroup(
        _string(selected["id"], "id"),
        _string(selected["purpose"], "purpose"),
        TraversalPolicy(directions, transitive),
        provenance,
        validator,
        _string_mapping(selected["metadata"], "metadata"),
    )


def _project_edge(value: Edge) -> dict[str, object]:
    return {
        "id": value.id,
        "source": value.source,
        "target": value.target,
        "relation": value.relation,
        "groups": list(value.groups),
        "provenance": _project_provenance(value.provenance),
        "metadata": dict(value.metadata),
        "traversable": value.traversable,
    }


def _load_edge(value: object) -> Edge:
    selected = _mapping(
        value,
        {
            "id",
            "source",
            "target",
            "relation",
            "groups",
            "provenance",
            "metadata",
            "traversable",
        },
        "edge",
    )
    provenance = _load_provenance(selected["provenance"])
    traversable = selected["traversable"]
    if provenance is None:
        raise _failure("edge provenance is required")
    if type(traversable) is not bool:
        raise _failure("edge traversable must be Boolean")
    return Edge(
        _string(selected["id"], "id"),
        _string(selected["source"], "source"),
        _string(selected["target"], "target"),
        _string(selected["relation"], "relation"),
        _strings(selected["groups"], "groups"),
        provenance,
        _string_mapping(selected["metadata"], "metadata"),
        traversable,
    )


def _mapping(
    value: object, expected: set[str], description: str
) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise _failure(f"{description} fields differ from the closed projection")
    if any(type(key) is not str for key in value):
        raise _failure(f"{description} keys must be exact strings")
    return value


def _array(value: object, description: str) -> tuple[object, ...]:
    if type(value) is not list:
        raise _failure(f"{description} must be an array")
    return tuple(value)


def _strings(value: object, description: str) -> tuple[str, ...]:
    selected = _array(value, description)
    if any(type(item) is not str for item in selected):
        raise _failure(f"{description} must contain strings")
    return selected  # type: ignore[return-value]


def _string_mapping(value: object, description: str) -> dict[str, str]:
    if not isinstance(value, Mapping) or any(
        type(key) is not str or type(item) is not str for key, item in value.items()
    ):
        raise _failure(f"{description} must map strings to strings")
    return dict(value)  # type: ignore[arg-type]


def _string(value: object, field: str) -> str:
    if type(value) is not str or not value:
        raise _failure(f"{field} must be a nonempty string")
    return value


def _failure(message: str) -> InvalidSourceError:
    return InvalidSourceError(message)


__all__ = ("load_graph_contribution", "project_graph_contribution")
