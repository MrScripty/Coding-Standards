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
METADATA_REQUIRES = "standards-requires"
METADATA_SPECIALIZES = "standards-specializes"
METADATA_DEPENDENCIES = "standards-dependencies"


class SuiteEntry(Protocol):
    id: str
    path: str
    requires: tuple[str, ...]


class MetadataModule(Protocol):
    module_id: str
    path: str
    requires: tuple[str, ...]
    specializes: tuple[str, ...]


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


def metadata_dependency_registry(
    root: Path,
    modules: Iterable[MetadataModule],
) -> EdgeRegistry:
    return EdgeRegistry(root, (metadata_dependency_source(modules),))


def metadata_dependency_source(
    modules: Iterable[MetadataModule],
) -> Provider:
    source_id = "standards-verifier.metadata-dependencies"
    selected = tuple(modules)
    provenance = Provenance(source_id, "generator", "canonical module metadata")
    directions = frozenset({Direction.INCOMING, Direction.OUTGOING})
    groups = (
        EdgeGroup(
            METADATA_REQUIRES,
            "Canonical standards routing prerequisites.",
            TraversalPolicy(directions, transitive=True),
            provenance,
            validator="standards-verifier:metadata-requires",
        ),
        EdgeGroup(
            METADATA_SPECIALIZES,
            "Canonical standards specialization relations.",
            TraversalPolicy(directions, transitive=True),
            provenance,
            validator="standards-verifier:metadata-specializes",
        ),
        EdgeGroup(
            METADATA_DEPENDENCIES,
            "Combined canonical standards prerequisites and specializations.",
            TraversalPolicy(directions, transitive=True),
            provenance,
            validator="standards-verifier:metadata-dependencies",
        ),
    )
    nodes = tuple(
        Node(
            module.module_id,
            (module.path,),
            provenance,
            {"repository_path": module.path},
        )
        for module in selected
    )
    requires = tuple(
        Edge(
            f"metadata-requires:{module.module_id}->{target}",
            module.module_id,
            target,
            "requires",
            (METADATA_REQUIRES, METADATA_DEPENDENCIES),
            provenance,
        )
        for module in selected
        for target in module.requires
    )
    specializes = tuple(
        Edge(
            f"metadata-specializes:{module.module_id}->{target}",
            module.module_id,
            target,
            "specializes",
            (METADATA_SPECIALIZES, METADATA_DEPENDENCIES),
            provenance,
        )
        for module in selected
        for target in module.specializes
    )
    return Provider(
        source_id,
        GraphContribution(nodes, groups, (*requires, *specializes)),
    )
