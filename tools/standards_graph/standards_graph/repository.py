from __future__ import annotations

from pathlib import Path
from typing import Iterable

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.graph_engine.graph_engine.manifest import ManifestSource
from tools.standards_policy_impact.standards_policy_impact import (
    CATALOG_SOURCE_ID,
    CompiledPolicyImpactSet,
    DEFAULT_REGISTRY,
    PolicyImpactSource,
    compile_policy_impact,
)

from .metadata import MetadataModule, metadata_dependency_source


POLICY_IMPACT_NODE_CATALOG = (
    "evaluation/standards-effectiveness/policy-impact-node-catalog.toml"
)
POLICY_IMPACT_REGISTRY = DEFAULT_REGISTRY


def standards_navigation_registry(
    root: Path,
    modules: Iterable[MetadataModule],
    policy_impact_registry: str = POLICY_IMPACT_REGISTRY,
    *,
    compiled_policy_impact: CompiledPolicyImpactSet | None = None,
) -> EdgeRegistry:
    """Build the explicit graph view used for canonical standards navigation."""

    repo_root = root.resolve()
    selected_modules = tuple(modules)
    compiled = (
        compiled_policy_impact
        or compile_policy_impact(
            repo_root,
            selected_modules,
            policy_impact_registry,
        )
    )
    sources = (
        metadata_dependency_source(selected_modules),
        ManifestSource(
            repo_root,
            CATALOG_SOURCE_ID,
            POLICY_IMPACT_NODE_CATALOG,
        ),
        PolicyImpactSource(compiled),
    )
    return EdgeRegistry(repo_root, sources)
