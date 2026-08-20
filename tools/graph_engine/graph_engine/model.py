from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Protocol

from .errors import InvalidEdgeError, InvalidGroupError, InvalidSourceError


def _text(value: str, field_name: str, error_type: type[Exception]) -> str:
    if not isinstance(value, str) or not value.strip():
        raise error_type(f"{field_name} must be a non-empty string", field=field_name)
    return value


def _metadata(value: Mapping[str, str], owner: str) -> Mapping[str, str]:
    selected: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not key or not isinstance(item, str):
            raise InvalidSourceError(
                "extension metadata must contain non-empty string keys and string values",
                owner=owner,
            )
        selected[key] = item
    return MappingProxyType(dict(sorted(selected.items())))


class Direction(str, Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"
    BOTH = "both"

    @classmethod
    def parse(cls, value: str) -> Direction:
        try:
            return cls(value)
        except ValueError as error:
            raise InvalidGroupError(
                "direction must be incoming, outgoing, or both",
                direction=str(value),
            ) from error


@dataclass(frozen=True, slots=True)
class Provenance:
    source_id: str
    kind: str
    locator: str

    def __post_init__(self) -> None:
        _text(self.source_id, "source_id", InvalidSourceError)
        if self.kind not in {"manifest", "generator", "provider"}:
            raise InvalidSourceError("provenance kind is not supported", kind=self.kind)
        _text(self.locator, "locator", InvalidSourceError)


@dataclass(frozen=True, slots=True)
class TraversalPolicy:
    directions: frozenset[Direction]
    transitive: bool = False

    def __post_init__(self) -> None:
        if not self.directions or Direction.BOTH in self.directions:
            raise InvalidGroupError(
                "group directions must explicitly contain incoming, outgoing, or both directions separately"
            )
        if not self.directions.issubset({Direction.INCOMING, Direction.OUTGOING}):
            raise InvalidGroupError("group has an unsupported traversal direction")
        if not isinstance(self.transitive, bool):
            raise InvalidGroupError("transitive must be a boolean")

    def permits(self, direction: Direction) -> bool:
        if direction is Direction.BOTH:
            return {
                Direction.INCOMING,
                Direction.OUTGOING,
            }.issubset(self.directions)
        return direction in self.directions


@dataclass(frozen=True, slots=True)
class Node:
    id: str
    aliases: tuple[str, ...] = ()
    provenance: Provenance | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _text(self.id, "node.id", InvalidSourceError)
        if any(not isinstance(alias, str) or not alias for alias in self.aliases):
            raise InvalidSourceError("node aliases must be non-empty strings", node=self.id)
        if len(set(self.aliases)) != len(self.aliases):
            raise InvalidSourceError("node aliases must be unique", node=self.id)
        object.__setattr__(self, "metadata", _metadata(self.metadata, self.id))


@dataclass(frozen=True, slots=True)
class EdgeGroup:
    id: str
    purpose: str
    traversal: TraversalPolicy
    provenance: Provenance
    validator: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _text(self.id, "group.id", InvalidGroupError)
        _text(self.purpose, "group.purpose", InvalidGroupError)
        if self.validator is not None:
            _text(self.validator, "group.validator", InvalidGroupError)
        object.__setattr__(self, "metadata", _metadata(self.metadata, self.id))


@dataclass(frozen=True, slots=True)
class Edge:
    id: str
    source: str
    target: str
    relation: str
    groups: tuple[str, ...]
    provenance: Provenance
    metadata: Mapping[str, str] = field(default_factory=dict)
    traversable: bool = True

    def __post_init__(self) -> None:
        for field_name in ("id", "source", "target", "relation"):
            _text(getattr(self, field_name), f"edge.{field_name}", InvalidEdgeError)
        if not self.groups or any(not isinstance(group, str) or not group for group in self.groups):
            raise InvalidEdgeError("edge must belong to at least one named group", edge=self.id)
        if len(set(self.groups)) != len(self.groups):
            raise InvalidEdgeError("edge group memberships must be unique", edge=self.id)
        if not isinstance(self.traversable, bool):
            raise InvalidEdgeError("edge traversable must be a boolean", edge=self.id)
        object.__setattr__(self, "metadata", _metadata(self.metadata, self.id))


@dataclass(frozen=True, slots=True)
class GraphContribution:
    nodes: tuple[Node, ...]
    groups: tuple[EdgeGroup, ...]
    edges: tuple[Edge, ...]


class EdgeSource(Protocol):
    @property
    def id(self) -> str: ...

    def load(self) -> GraphContribution: ...
