from __future__ import annotations

from pathlib import Path
from tools.graph_engine.graph_engine import EdgeRegistry
from tools.graph_engine.graph_engine.manifest import ManifestSource
from tools.standards_policy_impact.standards_policy_impact import (
    CATALOG_SOURCE_ID,
    CompiledPolicyImpactSet,
    DEFAULT_REGISTRY,
    PolicyImpactSource,
    compile_policy_impact,
)
from tools.standards_metadata.standards_metadata import CanonicalStandardsCorpus

from .metadata import metadata_dependency_source
from .policy_units import PolicyUnitGraphSource


POLICY_IMPACT_NODE_CATALOG = (
    "evaluation/standards-effectiveness/policy-impact-node-catalog.toml"
)
POLICY_IMPACT_REGISTRY = DEFAULT_REGISTRY


def standards_navigation_registry(
    root: Path,
    corpus: CanonicalStandardsCorpus,
    policy_impact_registry: str = POLICY_IMPACT_REGISTRY,
    *,
    compiled_policy_impact: CompiledPolicyImpactSet | None = None,
) -> EdgeRegistry:
    """Build the explicit graph view used for canonical standards navigation."""

    repo_root = root.resolve()
    compiled = (
        compiled_policy_impact
        or compile_policy_impact(
            repo_root,
            corpus,
            policy_impact_registry,
        )
    )
    sources = (
        metadata_dependency_source(corpus.modules),
        PolicyUnitGraphSource(corpus.policy_unit_corpus),
        ManifestSource(
            repo_root,
            CATALOG_SOURCE_ID,
            POLICY_IMPACT_NODE_CATALOG,
        ),
        PolicyImpactSource(compiled),
    )
    return EdgeRegistry(repo_root, sources)
