from __future__ import annotations

from pathlib import Path
from typing import Iterable

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.graph_engine.graph_engine.manifest import ManifestSource

from .metadata import MetadataModule, metadata_dependency_source


POLICY_IMPACT_MANIFEST = (
    "evaluation/standards-effectiveness/policy-semantic-impact.toml"
)
POLICY_IMPACT_SOURCE_ID = "standards.policy-impact"


def standards_navigation_registry(
    root: Path,
    modules: Iterable[MetadataModule],
    policy_impact_manifest: str = POLICY_IMPACT_MANIFEST,
) -> EdgeRegistry:
    """Build the explicit graph view used for canonical standards navigation."""

    repo_root = root.resolve()
    sources = (
        metadata_dependency_source(modules),
        ManifestSource(repo_root, POLICY_IMPACT_SOURCE_ID, policy_impact_manifest),
    )
    return EdgeRegistry(repo_root, sources)
