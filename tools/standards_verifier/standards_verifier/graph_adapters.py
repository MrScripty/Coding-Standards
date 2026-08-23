from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol

from tools.graph_engine.graph_engine import (
    Direction,
    Edge,
    EdgeGroup,
    EdgeRegistry,
    GraphContribution,
    Node,
    Provenance,
    TraversalPolicy,
)


SUITE_DEPENDENCIES = "suite-dependencies"


class SuiteEntry(Protocol):
    id: str
    path: str
    requires: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Provider:
    id: str
    contribution: GraphContribution

    def load(self) -> GraphContribution:
        return self.contribution


def suite_dependency_registry(
    root: Path,
    entries: Iterable[SuiteEntry],
    registry_path: str,
    *,
    include_path_aliases: bool,
) -> EdgeRegistry:
    source = suite_dependency_source(
        entries,
        registry_path,
        include_path_aliases=include_path_aliases,
    )
    return EdgeRegistry(root, (source,))


def suite_dependency_source(
    entries: Iterable[SuiteEntry],
    registry_path: str,
    *,
    include_path_aliases: bool,
) -> Provider:
    source_id = "standards-verifier.suite-dependencies"
    provenance = Provenance(source_id, "generator", registry_path)
    selected = tuple(entries)
    nodes = tuple(
        Node(
            entry.id,
            (entry.path,) if include_path_aliases else (),
            provenance,
            {"repository_path": entry.path},
        )
        for entry in selected
    )
    group = EdgeGroup(
        SUITE_DEPENDENCIES,
        "Registered suite execution dependencies.",
        TraversalPolicy(
            frozenset({Direction.INCOMING, Direction.OUTGOING}),
            transitive=True,
        ),
        provenance,
        validator="standards-verifier:suite-dependencies",
    )
    edges = tuple(
        Edge(
            f"suite-requires:{entry.id}->{dependency}",
            entry.id,
            dependency,
            "requires",
            (SUITE_DEPENDENCIES,),
            provenance,
        )
        for entry in selected
        for dependency in entry.requires
    )
    return Provider(source_id, GraphContribution(nodes, (group,), edges))
