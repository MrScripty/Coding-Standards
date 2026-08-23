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


METADATA_REQUIRES = "standards-requires"
METADATA_SPECIALIZES = "standards-specializes"
METADATA_DEPENDENCIES = "standards-dependencies"
METADATA_SOURCE_ID = "standards-verifier.metadata-dependencies"


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


def metadata_dependency_registry(
    root: Path,
    modules: Iterable[MetadataModule],
) -> EdgeRegistry:
    return EdgeRegistry(root, (metadata_dependency_source(modules),))


def metadata_dependency_source(
    modules: Iterable[MetadataModule],
) -> Provider:
    selected = tuple(modules)
    provenance = Provenance(
        METADATA_SOURCE_ID,
        "generator",
        "canonical module metadata",
    )
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
        METADATA_SOURCE_ID,
        GraphContribution(nodes, groups, (*requires, *specializes)),
    )
